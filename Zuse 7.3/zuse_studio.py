# FILE: zuse_studio.py
# VERSION: 7.0 (Transpiler Edition)
# Neu: Vollständige Transpiler-Integration mit 4 Ziel-Sprachen

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import os
import sys
import threading
import queue
import re
import json
import traceback

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from language_loader import lade_sprache
    from lexer import tokenize
    from parser import Parser
    from interpreter import Interpreter
    from debugger import ZuseDebugger
    from error_hints import format_error_with_hint
    from error_i18n import set_language
    try: from translate import uebersetze_code
    except: uebersetze_code = None
    try:
        from transpiler import transpile, BACKENDS, BACKEND_DISPLAY_NAMES
        TRANSPILER_AVAILABLE = True
    except Exception as e:
        TRANSPILER_AVAILABLE = False
        print(f"[Warnung] Transpiler nicht verfügbar: {e}")
except ImportError as e:
    messagebox.showerror("Boot Error", f"Module fehlen: {e}")
    sys.exit(1)

# UI i18n - safe import with fallback
try:
    from studio_i18n import ui, set_ui_language
    _STUDIO_I18N = True
except Exception:
    _STUDIO_I18N = False
    def ui(key, **kwargs): return key
    def set_ui_language(lang_name): pass


class TranspilerDialog(tk.Toplevel):
    BACKEND_ICONS = {
        "python":     "PY",
        "javascript": "JS",
        "java":       "JV",
        "csharp":     "C#",
    }
    BACKEND_COLORS = {
        "python":     "#3572A5",
        "javascript": "#c9a227",
        "java":       "#b07219",
        "csharp":     "#178600",
    }

    def __init__(self, parent, zuse_code, source_lang):
        super().__init__(parent)
        self.title(ui("TRANS_TITLE"))
        self.geometry("980x720")
        self.configure(bg="#1e1e2e")
        self.resizable(True, True)
        self.zuse_code = zuse_code
        self.source_lang = source_lang
        self.current_result = None
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self._build_ui()
        self._run_transpile("python")

    def _build_ui(self):
        top = tk.Frame(self, bg="#181825")
        top.pack(fill="x")
        tk.Label(top, text="  " + ui("TRANS_TITLE") + " 1.0",
                 font=("Consolas", 13, "bold"),
                 bg="#181825", fg="#cba6f7").pack(side="left", pady=8)
        tk.Label(top, text="  " + ui("TRANS_SUBTITLE"),
                 font=("Consolas", 9), bg="#181825", fg="#6c7086").pack(side="left")

        btn_frame = tk.Frame(self, bg="#1e1e2e")
        btn_frame.pack(fill="x", padx=10, pady=8)
        tk.Label(btn_frame, text=ui("TRANS_TARGET"), font=("Consolas", 10, "bold"),
                 bg="#1e1e2e", fg="#cdd6f4").pack(side="left")

        self._backend_btns = {}
        for key, label in [("python","Python 3"),("javascript","JavaScript"),("java","Java 11"),("csharp","C# 10")]:
            btn = tk.Button(btn_frame, text=f"[{self.BACKEND_ICONS[key]}] {label}",
                            font=("Consolas", 10), bg="#313244", fg="#cdd6f4",
                            relief="flat", padx=10, pady=5, cursor="hand2",
                            command=lambda k=key: self._on_select(k))
            btn.pack(side="left", padx=3)
            self._backend_btns[key] = btn

        self._warn_var = tk.StringVar(value="")
        tk.Label(self, textvariable=self._warn_var, font=("Consolas", 9),
                 bg="#1e1e2e", fg="#f9e2af", wraplength=940, anchor="w",
                 justify="left").pack(fill="x", padx=12)

        split = tk.Frame(self, bg="#1e1e2e")
        split.pack(fill="both", expand=True, padx=10, pady=4)

        left = tk.Frame(split, bg="#1e1e2e")
        left.pack(side="left", fill="both", expand=True, padx=(0,4))
        tk.Label(left, text=ui("TRANS_SOURCE"), font=("Consolas", 9, "bold"),
                 bg="#1e1e2e", fg="#89dceb").pack(anchor="w")
        self._zuse_view = tk.Text(left, bg="#181825", fg="#cdd6f4",
                                  font=("Consolas", 10), relief="flat", wrap="none")
        self._zuse_view.pack(fill="both", expand=True)
        self._zuse_view.insert("1.0", self.zuse_code)
        self._zuse_view.config(state="disabled")

        right = tk.Frame(split, bg="#1e1e2e")
        right.pack(side="left", fill="both", expand=True)
        self._out_label = tk.Label(right, text=ui("TRANS_OUTPUT"),
                                   font=("Consolas", 9, "bold"),
                                   bg="#1e1e2e", fg="#a6e3a1")
        self._out_label.pack(anchor="w")
        self._out_view = tk.Text(right, bg="#181825", fg="#a6e3a1",
                                 font=("Consolas", 10), relief="flat", wrap="none")
        self._out_view.pack(fill="both", expand=True)

        actions = tk.Frame(self, bg="#181825")
        actions.pack(fill="x", padx=10, pady=8)
        tk.Button(actions, text=ui("TRANS_SAVE"), font=("Consolas", 10),
                  bg="#313244", fg="#a6e3a1", relief="flat", padx=12, pady=6,
                  cursor="hand2", command=self._save).pack(side="left", padx=3)
        tk.Button(actions, text=ui("TRANS_COPY"), font=("Consolas", 10),
                  bg="#313244", fg="#89b4fa", relief="flat", padx=12, pady=6,
                  cursor="hand2", command=self._copy).pack(side="left", padx=3)
        tk.Button(actions, text=ui("TRANS_CLOSE"), font=("Consolas", 10),
                  bg="#313244", fg="#f38ba8", relief="flat", padx=12, pady=6,
                  cursor="hand2", command=self.destroy).pack(side="right", padx=3)
        self._status = tk.Label(actions, text="", font=("Consolas", 9),
                                bg="#181825", fg="#89b4fa")
        self._status.pack(side="left", padx=8)

    def _on_select(self, key):
        for k, btn in self._backend_btns.items():
            if k == key:
                btn.config(bg=self.BACKEND_COLORS[k], fg="#1e1e2e")
            else:
                btn.config(bg="#313244", fg="#cdd6f4")
        self._run_transpile(key)

    def _run_transpile(self, key):
        try:
            result = transpile(self.zuse_code, self.source_lang, key,
                               include_stdlib=False, base_dir=self.base_dir)
            self.current_result = result
            self._out_view.config(state="normal")
            self._out_view.delete("1.0", tk.END)
            self._out_view.insert("1.0", result['code'])
            self._out_label.config(text=f"[{self.BACKEND_ICONS.get(key,'?')}] {result['backend']}")
            warns = result['warnings']
            self._warn_var.set(("Hinweise: " + " | ".join(warns)) if warns else ui("TRANS_SUCCESS"))
        except Exception as e:
            self._out_view.config(state="normal")
            self._out_view.delete("1.0", tk.END)
            self._out_view.insert("1.0", f"FEHLER:\n\n{e}")
            self._warn_var.set(f"Fehler: {e}")

    def _save(self):
        if not self.current_result: return
        ext = self.current_result['extension']
        p = filedialog.asksaveasfilename(defaultextension=ext,
            filetypes=[(self.current_result['backend'], f"*{ext}"),("Alle","*.*")])
        if p:
            with open(p, "w", encoding="utf-8") as f:
                f.write(self._out_view.get("1.0", tk.END))
            self._status.config(text=ui("TRANS_SAVED", path=os.path.basename(p)))

    def _copy(self):
        self.clipboard_clear()
        self.clipboard_append(self._out_view.get("1.0", tk.END))
        self._status.config(text=ui("TRANS_COPIED"))
        self.after(2000, lambda: self._status.config(text=""))


class ZuseEditorWidget(tk.Frame):
    def __init__(self, master, studio_ref, **kwargs):
        super().__init__(master, **kwargs)
        self.studio = studio_ref
        self.text_font = ("Consolas", 12)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.on_scroll)
        self.scrollbar.pack(side="right", fill="y")
        self.linenumbers = tk.Text(self, width=4, padx=4, takefocus=0, border=0,
                                   background="#333", foreground="#888",
                                   state="disabled", font=self.text_font)
        self.linenumbers.pack(side="left", fill="y")
        self.text = tk.Text(self, font=self.text_font, undo=True,
                            yscrollcommand=self.on_text_scroll,
                            bg="#1a1a2e", fg="#cdd6f4", insertbackground="#cdd6f4")
        self.text.pack(side="left", fill="both", expand=True)
        self.text.tag_configure("keyword",    foreground="#FFA500", font=(self.text_font[0], self.text_font[1], "bold"))
        self.text.tag_configure("string",     foreground="#98C379")
        self.text.tag_configure("comment",    foreground="#7F848E")
        self.text.tag_configure("number",     foreground="#56B6C2")
        self.text.tag_configure("definition", foreground="#61AFEF", font=(self.text_font[0], self.text_font[1], "bold"))
        self.text.tag_configure("debug_line", background="#3d3800")
        self.text.bind("<KeyRelease>", self.on_content_changed)
        self.text.bind("<MouseWheel>", self.on_text_scroll_event)
        self.breakpoints = set()
        self.linenumbers.tag_configure("breakpoint", foreground="#f38ba8", font=(self.text_font[0], self.text_font[1], "bold"))
        self.linenumbers.bind("<Button-1>", self.on_linenumber_click)
        self.update_linenumbers()

    def on_scroll(self, *args):
        self.text.yview(*args)
        self.linenumbers.yview(*args)

    def on_text_scroll(self, *args):
        self.scrollbar.set(*args)
        self.linenumbers.yview_moveto(args[0])

    def on_text_scroll_event(self, event):
        self.linenumbers.yview_scroll(int(-1*(event.delta/120)), "units")

    def on_content_changed(self, event=None):
        self.update_linenumbers()
        self.highlight_syntax()

    def update_linenumbers(self):
        line_count = self.text.get('1.0', tk.END).count('\n')
        if line_count == 0: line_count = 1
        self.linenumbers.config(state="normal")
        self.linenumbers.delete("1.0", tk.END)
        for i in range(1, line_count + 1):
            marker = "\u25cf" if i in self.breakpoints else str(i)
            if i > 1:
                self.linenumbers.insert("end", "\n")
            self.linenumbers.insert("end", marker)
            if i in self.breakpoints:
                self.linenumbers.tag_add("breakpoint", f"{i}.0", f"{i}.end")
        self.linenumbers.config(state="disabled")
        self.linenumbers.yview_moveto(self.text.yview()[0])

    def highlight_syntax(self):
        code = self.text.get("1.0", tk.END)
        for tag in ["keyword","string","comment","number","definition"]:
            self.text.tag_remove(tag, "1.0", tk.END)
        lang_config = lade_sprache(self.studio.current_lang)
        keywords = sorted(lang_config.values(), key=len, reverse=True)
        kw_pattern = r'\b(' + '|'.join(re.escape(k) for k in keywords) + r')\b'
        self.apply_regex(kw_pattern, "keyword")
        self.apply_regex(r'"[^"]*"', "string")
        self.apply_regex(r'#.*', "comment")
        self.apply_regex(r'\b\d+\b', "number")
        kw_def   = lang_config.get("KW_DEFINIERE", "DEFINIERE")
        kw_class = lang_config.get("KW_KLASSE", "KLASSE")
        def_pat = rf'(?:{re.escape(kw_def)}|{re.escape(kw_class)})\s+([A-Za-z_][A-Za-z0-9_]*)'
        for m in re.finditer(def_pat, code):
            self.text.tag_add("definition", f"1.0 + {m.start(1)} chars", f"1.0 + {m.end(1)} chars")

    def apply_regex(self, pattern, tag):
        code = self.text.get("1.0", tk.END)
        for m in re.finditer(pattern, code):
            self.text.tag_add(tag, f"1.0 + {m.start()} chars", f"1.0 + {m.end()} chars")

    def on_linenumber_click(self, event):
        index = self.linenumbers.index(f"@{event.x},{event.y}")
        line = int(index.split(".")[0])
        if line in self.breakpoints:
            self.breakpoints.discard(line)
        else:
            self.breakpoints.add(line)
        self.update_linenumbers()

    def highlight_debug_line(self, line):
        self.text.tag_remove("debug_line", "1.0", tk.END)
        if line and line > 0:
            self.text.tag_add("debug_line", f"{line}.0", f"{line}.end")
            self.text.see(f"{line}.0")

    def clear_debug_line(self):
        self.text.tag_remove("debug_line", "1.0", tk.END)


class ZuseStudio:
    def __init__(self, root):
        self.root = root
        self.root.title("Zuse Studio 7.0 - Transpiler Edition")
        self.root.geometry("1200x850")
        self.root.configure(bg="#1e1e2e")
        self.current_lang = "deutsch"
        self.output_queue = queue.Queue()
        self.input_request_queue = queue.Queue()
        self.active_interpreter = None
        self._debugger = None
        self._debug_update_queue = queue.Queue()
        self._build_ui()
        self.root.after(100, self.check_queues)

    def _build_ui(self):
        main = tk.Frame(self.root, bg="#1e1e2e")
        main.pack(fill="both", expand=True)

        bar = tk.Frame(main, bg="#181825", height=50)
        bar.pack(fill="x", side="top")
        bar.pack_propagate(False)

        def btn(parent, text, bg, cmd):
            return tk.Button(parent, text=text, bg=bg, fg="#1e1e2e",
                             font=("Consolas", 10, "bold"), relief="flat",
                             padx=10, pady=6, cursor="hand2", command=cmd)

        self._btn_start = btn(bar, "START",  "#a6e3a1", self.run_decider)
        self._btn_start.pack(side="left", padx=(8,2), pady=8)
        self._btn_debug = btn(bar, "DEBUG",  "#f9e2af", self.debug_start)
        self._btn_debug.pack(side="left", padx=2, pady=8)
        self._btn_stop = btn(bar, "STOP",   "#f38ba8", self.stop_thread)
        self._btn_stop.pack(side="left", padx=2, pady=8)
        self._btn_save = btn(bar, "SAVE",   "#89b4fa", self.save)
        self._btn_save.pack(side="left", padx=2, pady=8)
        self._btn_load = btn(bar, "LOAD",   "#89b4fa", self.load)
        self._btn_load.pack(side="left", padx=2, pady=8)

        tk.Frame(bar, bg="#45475a", width=2).pack(side="left", padx=8, fill="y", pady=8)

        self.btn_continue = btn(bar, "\u25b6 Weiter", "#a6e3a1", self.debug_continue)
        self.btn_continue.pack(side="left", padx=2, pady=8)
        self.btn_step_into = btn(bar, "\u2193 Step", "#89dceb", self.debug_step_into)
        self.btn_step_into.pack(side="left", padx=2, pady=8)
        self.btn_step_over = btn(bar, "\u2192 Over", "#89dceb", self.debug_step_over)
        self.btn_step_over.pack(side="left", padx=2, pady=8)
        self._set_debug_buttons_state("disabled")

        tk.Frame(bar, bg="#45475a", width=2).pack(side="left", padx=8, fill="y", pady=8)

        self._btn_examples = btn(bar, "BEISPIELE", "#f5c2e7", self.open_examples)
        self._btn_examples.pack(side="left", padx=2, pady=8)

        tk.Frame(bar, bg="#45475a", width=2).pack(side="left", padx=8, fill="y", pady=8)

        if TRANSPILER_AVAILABLE:
            self._btn_transpile = btn(bar, "TRANSPILIEREN", "#cba6f7", self.open_transpiler)
            self._btn_transpile.pack(side="left", padx=2, pady=8)
        else:
            self._btn_transpile = None
            self._lbl_transpile_na = tk.Label(bar, text="[Transpiler nicht verfügbar]",
                     bg="#181825", fg="#f38ba8", font=("Consolas", 8))
            self._lbl_transpile_na.pack(side="left", padx=6)

        tk.Frame(bar, bg="#45475a", width=2).pack(side="left", padx=8, fill="y", pady=8)

        self.gui_mode_var = tk.BooleanVar(value=False)
        self._chk_gui = tk.Checkbutton(bar, text="GUI-Modus", variable=self.gui_mode_var,
                       bg="#181825", fg="#cdd6f4", selectcolor="#313244",
                       activebackground="#181825",
                       font=("Consolas", 9))
        self._chk_gui.pack(side="left", padx=4)

        self._lbl_mode = tk.Label(bar, text="Modus:", bg="#181825", fg="#6c7086",
                 font=("Consolas", 9))
        self._lbl_mode.pack(side="left", padx=(8,2))
        self.mode_var = tk.StringVar(value=ui("MODE_EXPERT"))
        ttk.Combobox(bar, textvariable=self.mode_var,
                     values=[ui("MODE_EXPERT"), ui("MODE_LEARN")], state="readonly",
                     width=7).pack(side="left")

        self._lbl_lang = tk.Label(bar, text="Sprache:", bg="#181825", fg="#6c7086",
                 font=("Consolas", 9))
        self._lbl_lang.pack(side="left", padx=(10,2))
        self.lang_var = tk.StringVar(value="deutsch")
        self.cb_lang = ttk.Combobox(bar, textvariable=self.lang_var,
                                    values=self.get_langs(), state="readonly", width=12)
        self.cb_lang.pack(side="left")
        self.cb_lang.bind("<<ComboboxSelected>>", self.translate_view)

        editor_frame = tk.Frame(main, bg="#1e1e2e")
        editor_frame.pack(fill="both", expand=True)

        self.editor = ZuseEditorWidget(editor_frame, self, bg="#1e1e2e")
        self.editor.pack(fill="both", expand=True, padx=6, pady=(4,0))

        bottom = tk.Frame(main, bg="#1e1e2e")
        bottom.pack(fill="both", side="bottom", padx=6, pady=(0,6))

        cons_frame = tk.Frame(bottom, bg="#1e1e2e")
        cons_frame.pack(side="left", fill="both", expand=True)
        self._lbl_console = tk.Label(cons_frame, text=" Konsole", bg="#181825", fg="#6c7086",
                 font=("Consolas", 9), anchor="w")
        self._lbl_console.pack(fill="x")
        self.cons = tk.Text(cons_frame, height=9, bg="#181825", fg="#a6e3a1",
                            font=("Consolas", 11), relief="flat",
                            insertbackground="#a6e3a1")
        self.cons.pack(fill="both", expand=True)

        self.var_frame = tk.Frame(bottom, bg="#1e1e2e", width=280)
        self.var_frame.pack(side="right", fill="y", padx=(4,0))
        self.var_frame.pack_propagate(False)
        self._lbl_variables = tk.Label(self.var_frame, text=" Variablen", bg="#181825", fg="#f9e2af",
                 font=("Consolas", 9), anchor="w")
        self._lbl_variables.pack(fill="x")
        self.var_text = tk.Text(self.var_frame, bg="#181825", fg="#cdd6f4",
                                font=("Consolas", 10), relief="flat", state="disabled")
        self.var_text.pack(fill="both", expand=True)

    def _update_ui_labels(self):
        """Aktualisiert alle UI-Texte nach Sprachwechsel."""
        if not _STUDIO_I18N:
            return
        self._btn_start.config(text=ui("BTN_START"))
        self._btn_debug.config(text=ui("BTN_DEBUG"))
        self._btn_stop.config(text=ui("BTN_STOP"))
        self._btn_save.config(text=ui("BTN_SAVE"))
        self._btn_load.config(text=ui("BTN_LOAD"))
        self._btn_examples.config(text=ui("BTN_EXAMPLES"))
        if self._btn_transpile:
            self._btn_transpile.config(text=ui("BTN_TRANSPILE"))
        elif hasattr(self, '_lbl_transpile_na'):
            self._lbl_transpile_na.config(text=ui("MSG_TRANSPILER_NA"))
        self.btn_continue.config(text=ui("BTN_CONTINUE"))
        self.btn_step_into.config(text=ui("BTN_STEP"))
        self.btn_step_over.config(text=ui("BTN_OVER"))
        self._chk_gui.config(text=ui("LBL_GUI_MODE"))
        self._lbl_mode.config(text=ui("LBL_MODE"))
        self._lbl_lang.config(text=ui("LBL_LANGUAGE"))
        self._lbl_console.config(text=ui("LBL_CONSOLE"))
        self._lbl_variables.config(text=ui("LBL_VARIABLES"))
        # Mode-Dropdown Werte aktualisieren
        current_is_learn = self.mode_var.get() not in (ui("MODE_EXPERT"), "Profi", "Expert", "Experto", "Expert", "Esperto", "Experto")
        self.mode_var.set(ui("MODE_LEARN") if current_is_learn else ui("MODE_EXPERT"))

    def _set_debug_buttons_state(self, state):
        for b in (self.btn_continue, self.btn_step_into, self.btn_step_over):
            b.config(state=state)

    def _update_var_panel(self, variables):
        self.var_text.config(state="normal")
        self.var_text.delete("1.0", tk.END)
        for name, val in sorted(variables.items()):
            valstr = repr(val) if not callable(val) else "<Funktion>"
            self.var_text.insert("end", f"{name} = {valstr}\n")
        self.var_text.config(state="disabled")

    def _on_debug_pause(self, dbg):
        self._debug_update_queue.put(("pause", dbg._current_line, dbg.get_variables()))

    def _process_debug_updates(self):
        try:
            while True:
                msg = self._debug_update_queue.get_nowait()
                if msg[0] == "pause":
                    _, line, variables = msg
                    self.editor.highlight_debug_line(line)
                    self._update_var_panel(variables)
                    self._set_debug_buttons_state("normal")
                    self.output_queue.put(ui("MSG_DEBUG_PAUSED", line=line))
                elif msg[0] == "done":
                    self.editor.clear_debug_line()
                    self._set_debug_buttons_state("disabled")
                    self._debugger = None
        except queue.Empty:
            pass
        if self._debugger is not None:
            self.root.after(100, self._process_debug_updates)

    def debug_start(self):
        code = self.editor.text.get("1.0", tk.END).strip()
        if not code:
            messagebox.showinfo(ui("DLG_DEBUG_TITLE"), ui("DLG_DEBUG_NO_CODE"))
            return
        self.cons.delete("1.0", tk.END)
        self.cons.insert("end", ui("MSG_DEBUG_START") + "\n")
        bp = self.editor.breakpoints
        self._debugger = ZuseDebugger(source_code=code, on_pause=self._on_debug_pause)
        for line in bp:
            self._debugger.set_breakpoint(line)
        if not bp:
            self._debugger.do_step_into()
        self._set_debug_buttons_state("disabled")
        self.root.after(100, self._process_debug_updates)
        lang = self.current_lang
        t = threading.Thread(target=self._debug_execute, args=(code, lang), daemon=True)
        t.start()

    def _debug_execute(self, code, lang):
        try:
            set_language(lang)
            conf = lade_sprache(lang)
            tokens = tokenize(code, conf)
            ast = Parser(tokens).parse()
            interp = Interpreter(
                output_callback=self.output_queue.put,
                input_callback=self._interpreter_input_callback,
                safe_mode=False,
                sprache=lang)
            interp._debugger = self._debugger
            self.active_interpreter = interp
            interp.interpretiere(ast)
            self.output_queue.put(ui("MSG_DEBUG_FINISHED"))
        except Exception as e:
            self.output_queue.put("[Debug] " + format_error_with_hint(e))
        finally:
            self.active_interpreter = None
            self._debug_update_queue.put(("done",))

    def debug_continue(self):
        if self._debugger and self._debugger.is_paused:
            self._set_debug_buttons_state("disabled")
            self.editor.clear_debug_line()
            self._debugger.do_continue()

    def debug_step_into(self):
        if self._debugger and self._debugger.is_paused:
            self._set_debug_buttons_state("disabled")
            self._debugger.do_step_into()

    def debug_step_over(self):
        if self._debugger and self._debugger.is_paused:
            self._set_debug_buttons_state("disabled")
            self._debugger.do_step_over()

    def open_examples(self):
        beispiele_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "beispiele")
        if not os.path.exists(beispiele_dir):
            messagebox.showinfo(ui("BTN_EXAMPLES"), ui("DLG_EXAMPLES_NO_DIR"))
            return
        files = sorted(f for f in os.listdir(beispiele_dir) if f.endswith(".zuse"))
        if not files:
            messagebox.showinfo(ui("BTN_EXAMPLES"), ui("DLG_EXAMPLES_NONE"))
            return
        dialog = tk.Toplevel(self.root)
        dialog.title(ui("DLG_EXAMPLES_TITLE"))
        dialog.geometry("420x480")
        dialog.configure(bg="#1e1e2e")
        dialog.transient(self.root)
        tk.Label(dialog, text=ui("DLG_EXAMPLES_CHOOSE"),
                 font=("Consolas", 11, "bold"), bg="#1e1e2e", fg="#f5c2e7").pack(pady=(12,6))
        listbox = tk.Listbox(dialog, bg="#181825", fg="#cdd6f4",
                             font=("Consolas", 11), selectbackground="#45475a",
                             relief="flat", activestyle="none")
        listbox.pack(fill="both", expand=True, padx=12, pady=4)
        for f in files:
            name = f.replace(".zuse", "").replace("_", " ")
            listbox.insert("end", name)

        def on_load():
            sel = listbox.curselection()
            if not sel:
                return
            path = os.path.join(beispiele_dir, files[sel[0]])
            with open(path, "r", encoding="utf-8") as fh:
                code = fh.read()
            self.editor.text.delete("1.0", tk.END)
            self.editor.text.insert("1.0", code)
            self.editor.highlight_syntax()
            self.editor.update_linenumbers()
            dialog.destroy()

        listbox.bind("<Double-1>", lambda e: on_load())
        tk.Button(dialog, text=ui("BTN_LOAD_EXAMPLE"), font=("Consolas", 10, "bold"),
                  bg="#a6e3a1", fg="#1e1e2e", relief="flat", padx=20, pady=8,
                  cursor="hand2", command=on_load).pack(pady=10)

    def open_transpiler(self):
        code = self.editor.text.get("1.0", tk.END).strip()
        if not code:
            messagebox.showinfo(ui("DLG_TRANSPILER_TITLE"), ui("DLG_TRANSPILER_NO_CODE"))
            return
        TranspilerDialog(self.root, code, self.current_lang)

    def get_langs(self):
        d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sprachen")
        if not os.path.exists(d): return ["deutsch"]
        return [f.replace(".json","") for f in os.listdir(d) if f.endswith(".json")]

    def check_queues(self):
        try:
            while True:
                msg = self.output_queue.get_nowait()
                self.cons.insert("end", str(msg) + "\n")
                self.cons.see("end")
        except queue.Empty: pass
        try:
            req = self.input_request_queue.get_nowait()
            prompt, modus, container, evt = req
            if modus == 'zahl': res = simpledialog.askfloat(ui("DLG_INPUT_TITLE"), prompt)
            else: res = simpledialog.askstring(ui("DLG_INPUT_TITLE"), prompt)
            container['value'] = res if res is not None else ""
            evt.set()
        except queue.Empty: pass
        self.root.after(100, self.check_queues)

    def stop_thread(self):
        if self._debugger:
            self._debugger.do_stop()
            self._debugger = None
            self.editor.clear_debug_line()
            self._set_debug_buttons_state("disabled")
        if self.active_interpreter:
            self.active_interpreter.running = False
            self.output_queue.put(ui("MSG_STOP_SIGNAL"))

    def check_gui_usage(self, code):
        gui_keywords = ['tkinter','turtle','Maler','Fenster','Painter','Window',
                        'Pintor','Janela','Peintre','Fenetre','Pittore','Finestra',
                        'चित्रकार','खिड़की','画家','画笔','窗口']
        for kw in gui_keywords:
            if kw in code: return True
        return False

    def run_decider(self):
        code = self.editor.text.get("1.0", tk.END)
        needs_gui = self.check_gui_usage(code)
        is_gui_mode = self.gui_mode_var.get()
        if needs_gui and not is_gui_mode:
            messagebox.showerror(ui("DLG_SECURITY_STOP_TITLE"), ui("DLG_SECURITY_STOP_MSG"))
            return
        if not needs_gui and is_gui_mode:
            if not messagebox.askyesno(ui("DLG_GUI_HINT_TITLE"), ui("DLG_GUI_HINT_MSG")):
                return
        self.cons.delete("1.0", tk.END)
        self.cons.insert("end", ui("MSG_STARTING") + "\n")
        lang = self.current_lang
        if self.gui_mode_var.get():
            self.output_queue.put(ui("MSG_GUI_ACTIVE"))
            self.root.after(100, lambda: self._execute_logic(code, lang, threaded=False))
        else:
            t = threading.Thread(target=self._execute_logic, args=(code, lang, True))
            t.daemon = True
            t.start()

    def _interpreter_input_callback(self, prompt, modus):
        if threading.current_thread() is threading.main_thread():
            if modus == 'zahl': return simpledialog.askfloat(ui("DLG_INPUT_TITLE"), prompt) or 0
            return simpledialog.askstring(ui("DLG_INPUT_TITLE"), prompt) or ""
        evt = threading.Event()
        container = {'value': None}
        self.input_request_queue.put((prompt, modus, container, evt))
        evt.wait()
        return container['value']

    def _execute_logic(self, code, lang, threaded=True):
        try:
            set_language(lang)
            base_path = os.path.dirname(os.path.abspath(__file__))
            lib_path = os.path.join(base_path, "bibliothek", f"{lang}.zuse")
            final_code = code
            start_line_offset = 1
            ist_lernmodus = (self.mode_var.get() == ui("MODE_LEARN"))
            if os.path.exists(lib_path):
                try:
                    with open(lib_path, "r", encoding="utf-8") as f:
                        lib_code = f.read()
                        lib_lines = lib_code.count('\n') + 2
                        start_line_offset = 1 - lib_lines
                        final_code = lib_code + "\n\n" + code
                except Exception as e:
                    self.output_queue.put(ui("MSG_LIB_ERROR", error=e))
            conf = lade_sprache(lang)
            tokens = tokenize(final_code, conf, start_line=start_line_offset)
            ast = Parser(tokens).parse()
            self.active_interpreter = Interpreter(
                output_callback=self.output_queue.put,
                input_callback=self._interpreter_input_callback,
                safe_mode=ist_lernmodus,
                sprache=lang)
            self.active_interpreter.global_env.set("__UMGEBUNG__", "STUDIO")
            self.active_interpreter.interpretiere(ast)
            self.output_queue.put(ui("MSG_FINISHED"))
        except Exception as e:
            self.output_queue.put(format_error_with_hint(e))
            traceback.print_exc()
        finally:
            self.active_interpreter = None

    def translate_view(self, event):
        new_l = self.lang_var.get()
        if new_l == self.current_lang: return
        old_l = self.current_lang
        self.current_lang = new_l
        set_ui_language(new_l)
        self._update_ui_labels()
        self.editor.highlight_syntax()
        if uebersetze_code:
            code = self.editor.text.get("1.0", tk.END)
            if len(code.strip()) > 0:
                try:
                    res = uebersetze_code(code, old_l, new_l)
                    self.editor.text.delete("1.0", tk.END)
                    self.editor.text.insert("1.0", res)
                    self.editor.highlight_syntax()
                    self.editor.update_linenumbers()
                except Exception as e:
                    print(f"[Info] Auto-Uebersetzung uebersprungen: {e}")

    def save(self):
        p = filedialog.asksaveasfilename(defaultextension=".zuse",
            filetypes=[("Zuse Dateien","*.zuse"),("Alle","*.*")])
        if p:
            with open(p,"w",encoding="utf-8") as f: f.write(self.editor.text.get("1.0",tk.END))

    def load(self):
        p = filedialog.askopenfilename(filetypes=[("Zuse Dateien","*.zuse"),("Alle","*.*")])
        if p:
            with open(p,"r",encoding="utf-8") as f:
                self.editor.text.delete("1.0",tk.END)
                self.editor.text.insert("1.0",f.read())
            self.editor.highlight_syntax()
            self.editor.update_linenumbers()

if __name__ == "__main__":
    root = tk.Tk()
    ZuseStudio(root)
    root.mainloop()
