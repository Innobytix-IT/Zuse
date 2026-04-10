# FILE: studio_i18n.py
# Mehrsprachige UI-Strings fuer Zuse Studio
# Wird von zuse_studio.py verwendet, um die Oberflaeche zu uebersetzen.

UI_STRINGS = {
    # ─── Toolbar Buttons ─────────────────────────────────────────────────
    "BTN_START": {
        "de": "START", "en": "START", "es": "INICIO", "fr": "LANCER",
        "it": "AVVIA", "pt": "INICIAR", "hi": "शुरू", "zh": "运行",
    },
    "BTN_DEBUG": {
        "de": "DEBUG", "en": "DEBUG", "es": "DEPURAR", "fr": "DEBOGUER",
        "it": "DEBUG", "pt": "DEPURAR", "hi": "डीबग", "zh": "调试",
    },
    "BTN_STOP": {
        "de": "STOP", "en": "STOP", "es": "PARAR", "fr": "ARRETER",
        "it": "FERMA", "pt": "PARAR", "hi": "रोको", "zh": "停止",
    },
    "BTN_SAVE": {
        "de": "SPEICHERN", "en": "SAVE", "es": "GUARDAR", "fr": "SAUVER",
        "it": "SALVA", "pt": "SALVAR", "hi": "सहेजें", "zh": "保存",
    },
    "BTN_LOAD": {
        "de": "LADEN", "en": "LOAD", "es": "CARGAR", "fr": "CHARGER",
        "it": "CARICA", "pt": "CARREGAR", "hi": "लोड", "zh": "加载",
    },
    "BTN_EXAMPLES": {
        "de": "BEISPIELE", "en": "EXAMPLES", "es": "EJEMPLOS", "fr": "EXEMPLES",
        "it": "ESEMPI", "pt": "EXEMPLOS", "hi": "उदाहरण", "zh": "示例",
    },
    "BTN_TRANSPILE": {
        "de": "TRANSPILIEREN", "en": "TRANSPILE", "es": "TRANSPILAR", "fr": "TRANSPILER",
        "it": "TRANSPILA", "pt": "TRANSPILAR", "hi": "ट्रांसपाइल", "zh": "转译",
    },
    "BTN_CONTINUE": {
        "de": "\u25b6 Weiter", "en": "\u25b6 Continue", "es": "\u25b6 Seguir", "fr": "\u25b6 Continuer",
        "it": "\u25b6 Continua", "pt": "\u25b6 Continuar", "hi": "\u25b6 जारी", "zh": "\u25b6 继续",
    },
    "BTN_STEP": {
        "de": "\u2193 Step", "en": "\u2193 Step", "es": "\u2193 Paso", "fr": "\u2193 Pas",
        "it": "\u2193 Passo", "pt": "\u2193 Passo", "hi": "\u2193 कदम", "zh": "\u2193 步进",
    },
    "BTN_OVER": {
        "de": "\u2192 Over", "en": "\u2192 Over", "es": "\u2192 Sobre", "fr": "\u2192 Passer",
        "it": "\u2192 Sopra", "pt": "\u2192 Sobre", "hi": "\u2192 ऊपर", "zh": "\u2192 跳过",
    },

    # ─── Labels ──────────────────────────────────────────────────────────
    "LBL_CONSOLE": {
        "de": " Konsole", "en": " Console", "es": " Consola", "fr": " Console",
        "it": " Console", "pt": " Console", "hi": " कंसोल", "zh": " 控制台",
    },
    "LBL_VARIABLES": {
        "de": " Variablen", "en": " Variables", "es": " Variables", "fr": " Variables",
        "it": " Variabili", "pt": " Variaveis", "hi": " चर", "zh": " 变量",
    },
    "LBL_GUI_MODE": {
        "de": "GUI-Modus", "en": "GUI Mode", "es": "Modo GUI", "fr": "Mode GUI",
        "it": "Modalita GUI", "pt": "Modo GUI", "hi": "GUI मोड", "zh": "GUI模式",
    },
    "LBL_MODE": {
        "de": "Modus:", "en": "Mode:", "es": "Modo:", "fr": "Mode:",
        "it": "Modalita:", "pt": "Modo:", "hi": "मोड:", "zh": "模式:",
    },
    "LBL_LANGUAGE": {
        "de": "Sprache:", "en": "Language:", "es": "Idioma:", "fr": "Langue:",
        "it": "Lingua:", "pt": "Idioma:", "hi": "भाषा:", "zh": "语言:",
    },
    "LBL_FUNCTION": {
        "de": "<Funktion>", "en": "<Function>", "es": "<Funcion>", "fr": "<Fonction>",
        "it": "<Funzione>", "pt": "<Funcao>", "hi": "<फ़ंक्शन>", "zh": "<函数>",
    },

    # ─── Mode Dropdown ───────────────────────────────────────────────────
    "MODE_EXPERT": {
        "de": "Profi", "en": "Expert", "es": "Experto", "fr": "Expert",
        "it": "Esperto", "pt": "Experto", "hi": "विशेषज्ञ", "zh": "专家",
    },
    "MODE_LEARN": {
        "de": "Lernen", "en": "Learn", "es": "Aprender", "fr": "Apprendre",
        "it": "Impara", "pt": "Aprender", "hi": "सीखें", "zh": "学习",
    },

    # ─── Dialog Messages ─────────────────────────────────────────────────
    "DLG_SECURITY_STOP_TITLE": {
        "de": "Sicherheits-Stopp", "en": "Safety Stop", "es": "Parada de seguridad",
        "fr": "Arret de securite", "it": "Arresto di sicurezza", "pt": "Parada de seguranca",
        "hi": "सुरक्षा रोक", "zh": "安全停止",
    },
    "DLG_SECURITY_STOP_MSG": {
        "de": "Dein Programm nutzt grafische Elemente!\n\nBitte aktiviere 'GUI-Modus', sonst stuerzt das Studio ab.",
        "en": "Your program uses graphical elements!\n\nPlease enable 'GUI Mode', otherwise the Studio will crash.",
        "es": "Tu programa usa elementos graficos!\n\nPor favor activa 'Modo GUI', de lo contrario el Studio se bloqueara.",
        "fr": "Ton programme utilise des elements graphiques!\n\nActive le 'Mode GUI', sinon le Studio plantera.",
        "it": "Il tuo programma usa elementi grafici!\n\nAttiva la 'Modalita GUI', altrimenti lo Studio si blocchera.",
        "pt": "Seu programa usa elementos graficos!\n\nAtive o 'Modo GUI', caso contrario o Studio travara.",
        "hi": "आपका प्रोग्राम ग्राफ़िकल तत्वों का उपयोग करता है!\n\nकृपया 'GUI मोड' सक्रिय करें, अन्यथा स्टूडियो क्रैश हो जाएगा।",
        "zh": "你的程序使用了图形元素！\n\n请启用'GUI模式'，否则Studio会崩溃。",
    },
    "DLG_GUI_HINT_TITLE": {
        "de": "Hinweis", "en": "Notice", "es": "Aviso", "fr": "Avis",
        "it": "Avviso", "pt": "Aviso", "hi": "सूचना", "zh": "提示",
    },
    "DLG_GUI_HINT_MSG": {
        "de": "Dein Programm nutzt keine Grafik.\nGUI-Modus blockiert das Studio.\nTrotzdem?",
        "en": "Your program doesn't use graphics.\nGUI mode blocks the Studio.\nContinue anyway?",
        "es": "Tu programa no usa graficos.\nEl modo GUI bloquea el Studio.\nContinuar de todos modos?",
        "fr": "Ton programme n'utilise pas de graphiques.\nLe mode GUI bloque le Studio.\nContinuer quand meme?",
        "it": "Il tuo programma non usa grafica.\nLa modalita GUI blocca lo Studio.\nContinuare comunque?",
        "pt": "Seu programa nao usa graficos.\nO modo GUI bloqueia o Studio.\nContinuar mesmo assim?",
        "hi": "आपका प्रोग्राम ग्राफ़िक्स का उपयोग नहीं करता।\nGUI मोड स्टूडियो को ब्लॉक करता है।\nफिर भी जारी रखें?",
        "zh": "你的程序不使用图形。\nGUI模式会阻塞Studio。\n仍然继续？",
    },
    "DLG_INPUT_TITLE": {
        "de": "Eingabe", "en": "Input", "es": "Entrada", "fr": "Saisie",
        "it": "Input", "pt": "Entrada", "hi": "इनपुट", "zh": "输入",
    },
    "DLG_DEBUG_TITLE": {
        "de": "Debug", "en": "Debug", "es": "Depuracion", "fr": "Debogage",
        "it": "Debug", "pt": "Depuracao", "hi": "डीबग", "zh": "调试",
    },
    "DLG_DEBUG_NO_CODE": {
        "de": "Bitte schreibe zuerst Zuse-Code.", "en": "Please write some Zuse code first.",
        "es": "Por favor, escribe codigo Zuse primero.", "fr": "Ecris d'abord du code Zuse.",
        "it": "Scrivi prima del codice Zuse.", "pt": "Por favor, escreva codigo Zuse primeiro.",
        "hi": "कृपया पहले ज़ूज़ कोड लिखें।", "zh": "请先编写Zuse代码。",
    },
    "DLG_TRANSPILER_TITLE": {
        "de": "Transpiler", "en": "Transpiler", "es": "Transpilador", "fr": "Transpileur",
        "it": "Transpiler", "pt": "Transpilador", "hi": "ट्रांसपाइलर", "zh": "转译器",
    },
    "DLG_TRANSPILER_NO_CODE": {
        "de": "Bitte schreibe zuerst etwas Zuse-Code.",
        "en": "Please write some Zuse code first.",
        "es": "Por favor, escribe algo de codigo Zuse primero.",
        "fr": "Ecris d'abord du code Zuse.",
        "it": "Scrivi prima del codice Zuse.",
        "pt": "Por favor, escreva algo de codigo Zuse primeiro.",
        "hi": "कृपया पहले कुछ ज़ूज़ कोड लिखें।",
        "zh": "请先编写一些Zuse代码。",
    },
    "DLG_EXAMPLES_TITLE": {
        "de": "Beispiele laden", "en": "Load Examples", "es": "Cargar ejemplos",
        "fr": "Charger exemples", "it": "Carica esempi", "pt": "Carregar exemplos",
        "hi": "उदाहरण लोड करें", "zh": "加载示例",
    },
    "DLG_EXAMPLES_CHOOSE": {
        "de": "Beispielprogramm waehlen:", "en": "Choose example program:",
        "es": "Elegir programa de ejemplo:", "fr": "Choisir un programme exemple:",
        "it": "Scegli programma esempio:", "pt": "Escolher programa exemplo:",
        "hi": "उदाहरण प्रोग्राम चुनें:", "zh": "选择示例程序:",
    },
    "DLG_EXAMPLES_NONE": {
        "de": "Keine Beispieldateien gefunden.", "en": "No example files found.",
        "es": "No se encontraron archivos de ejemplo.", "fr": "Aucun fichier exemple trouve.",
        "it": "Nessun file esempio trovato.", "pt": "Nenhum arquivo exemplo encontrado.",
        "hi": "कोई उदाहरण फ़ाइल नहीं मिली।", "zh": "未找到示例文件。",
    },
    "DLG_EXAMPLES_NO_DIR": {
        "de": "Kein beispiele/ Ordner gefunden.", "en": "No examples/ folder found.",
        "es": "No se encontro la carpeta ejemplos/.", "fr": "Pas de dossier exemples/ trouve.",
        "it": "Nessuna cartella esempi/ trovata.", "pt": "Nenhuma pasta exemplos/ encontrada.",
        "hi": "उदाहरण/ फ़ोल्डर नहीं मिला।", "zh": "未找到示例文件夹。",
    },

    # ─── Console Messages ────────────────────────────────────────────────
    "MSG_STARTING": {
        "de": "Starte Programm...", "en": "Starting program...", "es": "Iniciando programa...",
        "fr": "Demarrage du programme...", "it": "Avvio del programma...",
        "pt": "Iniciando programa...", "hi": "प्रोग्राम शुरू हो रहा है...", "zh": "正在启动程序...",
    },
    "MSG_FINISHED": {
        "de": "[Programm beendet]", "en": "[Program finished]", "es": "[Programa terminado]",
        "fr": "[Programme termine]", "it": "[Programma terminato]",
        "pt": "[Programa terminado]", "hi": "[प्रोग्राम समाप्त]", "zh": "[程序结束]",
    },
    "MSG_STOP_SIGNAL": {
        "de": "\n[STOP SIGNAL]\n", "en": "\n[STOP SIGNAL]\n", "es": "\n[SENAL DE PARADA]\n",
        "fr": "\n[SIGNAL D'ARRET]\n", "it": "\n[SEGNALE DI STOP]\n",
        "pt": "\n[SINAL DE PARADA]\n", "hi": "\n[रोक संकेत]\n", "zh": "\n[停止信号]\n",
    },
    "MSG_GUI_ACTIVE": {
        "de": "[INFO] GUI-Modus aktiv.", "en": "[INFO] GUI mode active.",
        "es": "[INFO] Modo GUI activo.", "fr": "[INFO] Mode GUI actif.",
        "it": "[INFO] Modalita GUI attiva.", "pt": "[INFO] Modo GUI ativo.",
        "hi": "[जानकारी] GUI मोड सक्रिय।", "zh": "[信息] GUI模式已激活。",
    },
    "MSG_DEBUG_START": {
        "de": "[Debug] Starte Debugger...", "en": "[Debug] Starting debugger...",
        "es": "[Debug] Iniciando depurador...", "fr": "[Debug] Demarrage du debogueur...",
        "it": "[Debug] Avvio del debugger...", "pt": "[Debug] Iniciando depurador...",
        "hi": "[डीबग] डीबगर शुरू हो रहा है...", "zh": "[调试] 正在启动调试器...",
    },
    "MSG_DEBUG_PAUSED": {
        "de": "[Debug] Pausiert in Zeile {line}", "en": "[Debug] Paused at line {line}",
        "es": "[Debug] Pausado en linea {line}", "fr": "[Debug] Pause a la ligne {line}",
        "it": "[Debug] In pausa alla riga {line}", "pt": "[Debug] Pausado na linha {line}",
        "hi": "[डीबग] पंक्ति {line} पर रुका", "zh": "[调试] 在第{line}行暂停",
    },
    "MSG_DEBUG_FINISHED": {
        "de": "[Debug] Programm beendet.", "en": "[Debug] Program finished.",
        "es": "[Debug] Programa terminado.", "fr": "[Debug] Programme termine.",
        "it": "[Debug] Programma terminato.", "pt": "[Debug] Programa terminado.",
        "hi": "[डीबग] प्रोग्राम समाप्त।", "zh": "[调试] 程序结束。",
    },
    "MSG_LIB_ERROR": {
        "de": "[Warnung] Lib Fehler: {error}", "en": "[Warning] Lib error: {error}",
        "es": "[Advertencia] Error de lib: {error}", "fr": "[Avertissement] Erreur de lib: {error}",
        "it": "[Avviso] Errore lib: {error}", "pt": "[Aviso] Erro de lib: {error}",
        "hi": "[चेतावनी] लाइब्रेरी त्रुटि: {error}", "zh": "[警告] 库错误: {error}",
    },
    "MSG_TRANSPILER_NA": {
        "de": "[Transpiler nicht verfuegbar]", "en": "[Transpiler not available]",
        "es": "[Transpilador no disponible]", "fr": "[Transpileur non disponible]",
        "it": "[Transpiler non disponibile]", "pt": "[Transpilador nao disponivel]",
        "hi": "[ट्रांसपाइलर उपलब्ध नहीं]", "zh": "[转译器不可用]",
    },

    # ─── Transpiler Dialog ───────────────────────────────────────────────
    "TRANS_TITLE": {
        "de": "Zuse Transpiler", "en": "Zuse Transpiler", "es": "Transpilador Zuse",
        "fr": "Transpileur Zuse", "it": "Transpiler Zuse", "pt": "Transpilador Zuse",
        "hi": "ज़ूज़ ट्रांसपाइलर", "zh": "Zuse转译器",
    },
    "TRANS_SUBTITLE": {
        "de": "Konvertiere deinen Code in eine andere Sprache",
        "en": "Convert your code to another language",
        "es": "Convierte tu codigo a otro lenguaje",
        "fr": "Convertis ton code dans un autre langage",
        "it": "Converti il tuo codice in un altro linguaggio",
        "pt": "Converta seu codigo para outra linguagem",
        "hi": "अपने कोड को दूसरी भाषा में बदलें",
        "zh": "将你的代码转换为其他语言",
    },
    "TRANS_TARGET": {
        "de": "Ziel:", "en": "Target:", "es": "Destino:", "fr": "Cible:",
        "it": "Obiettivo:", "pt": "Destino:", "hi": "लक्ष्य:", "zh": "目标:",
    },
    "TRANS_SOURCE": {
        "de": "Zuse-Quellcode", "en": "Zuse Source Code", "es": "Codigo fuente Zuse",
        "fr": "Code source Zuse", "it": "Codice sorgente Zuse", "pt": "Codigo fonte Zuse",
        "hi": "ज़ूज़ स्रोत कोड", "zh": "Zuse源代码",
    },
    "TRANS_OUTPUT": {
        "de": "Generierter Code", "en": "Generated Code", "es": "Codigo generado",
        "fr": "Code genere", "it": "Codice generato", "pt": "Codigo gerado",
        "hi": "उत्पन्न कोड", "zh": "生成的代码",
    },
    "TRANS_SAVE": {
        "de": "Speichern", "en": "Save", "es": "Guardar", "fr": "Sauver",
        "it": "Salva", "pt": "Salvar", "hi": "सहेजें", "zh": "保存",
    },
    "TRANS_COPY": {
        "de": "Kopieren", "en": "Copy", "es": "Copiar", "fr": "Copier",
        "it": "Copia", "pt": "Copiar", "hi": "कॉपी", "zh": "复制",
    },
    "TRANS_CLOSE": {
        "de": "Schliessen", "en": "Close", "es": "Cerrar", "fr": "Fermer",
        "it": "Chiudi", "pt": "Fechar", "hi": "बंद", "zh": "关闭",
    },
    "TRANS_SUCCESS": {
        "de": "OK - Erfolgreich transpiliert", "en": "OK - Successfully transpiled",
        "es": "OK - Transpilado exitosamente", "fr": "OK - Transpile avec succes",
        "it": "OK - Transpilato con successo", "pt": "OK - Transpilado com sucesso",
        "hi": "OK - सफलतापूर्वक ट्रांसपाइल किया गया", "zh": "OK - 转译成功",
    },
    "TRANS_SAVED": {
        "de": "Gespeichert: {path}", "en": "Saved: {path}", "es": "Guardado: {path}",
        "fr": "Sauvegarde: {path}", "it": "Salvato: {path}", "pt": "Salvo: {path}",
        "hi": "सहेजा गया: {path}", "zh": "已保存: {path}",
    },
    "TRANS_COPIED": {
        "de": "In Zwischenablage kopiert!", "en": "Copied to clipboard!",
        "es": "Copiado al portapapeles!", "fr": "Copie dans le presse-papiers!",
        "it": "Copiato negli appunti!", "pt": "Copiado para a area de transferencia!",
        "hi": "क्लिपबोर्ड पर कॉपी किया गया!", "zh": "已复制到剪贴板！",
    },

    # ─── Misc ────────────────────────────────────────────────────────────
    "BTN_LOAD_EXAMPLE": {
        "de": "Laden", "en": "Load", "es": "Cargar", "fr": "Charger",
        "it": "Carica", "pt": "Carregar", "hi": "लोड", "zh": "加载",
    },
}

# Mapping: Sprach-Dateiname -> ISO-Code
_LANG_MAP = {
    "deutsch": "de", "english": "en", "espaniol": "es", "francais": "fr",
    "italiano": "it", "portugues": "pt", "hindi": "hi", "zhongwen": "zh",
}

_current_ui_lang = "de"


def set_ui_language(lang_name):
    """Setzt die UI-Sprache (akzeptiert 'deutsch', 'english', etc. oder 'de', 'en', etc.)."""
    global _current_ui_lang
    if lang_name in _LANG_MAP:
        _current_ui_lang = _LANG_MAP[lang_name]
    elif lang_name in _LANG_MAP.values():
        _current_ui_lang = lang_name


def ui(key, **kwargs):
    """Gibt den UI-String in der aktuellen Sprache zurueck."""
    entry = UI_STRINGS.get(key)
    if not entry:
        return key
    text = entry.get(_current_ui_lang) or entry.get("de", key)
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, IndexError):
            return text
    return text
