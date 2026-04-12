import subprocess, sys, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS = [
    ("de_1_grundlagen.zuse", "deutsch"),
    ("de_2_bibliotheken.zuse", "deutsch"),
    ("en_1_basics.zuse", "english"),
    ("en_2_libraries.zuse", "english"),
    ("es_1_basico.zuse", "espaniol"),
    ("es_2_bibliotecas.zuse", "espaniol"),
    ("fr_1_bases.zuse", "francais"),
    ("fr_2_bibliotheques.zuse", "francais"),
    ("it_1_base.zuse", "italiano"),
    ("it_2_librerie.zuse", "italiano"),
    ("pt_1_basico.zuse", "portugues"),
    ("pt_2_bibliotecas.zuse", "portugues"),
    ("hi_1_aadhar.zuse", "hindi"),
    ("hi_2_pustakalay.zuse", "hindi"),
    ("zh_1_jichu.zuse", "zhongwen"),
    ("zh_2_kubaozang.zuse", "zhongwen"),
]

# Diese Strings dürfen in stdout stehen ohne als Fehler zu gelten
# (z.B. absichtlich gefangene Fehler im FANGE-Block)
ERLAUBTE_FEHLER = [
    "Fehler abgefangen",       # deutsch
    "Error capturado",         # español
    "Erreur capturée",         # français
    "Errore catturato",        # italiano
    "Erro capturado",          # português
    "Error caught",            # english
    "त्रुटि पकड़ी",            # hindi
    "捕获到错误",               # chinese
]

def ist_echter_fehler(stdout, stderr):
    if stderr:
        return True
    lines = stdout.split('\n')
    for line in lines:
        # Syntaxfehler / uncaught errors
        if any(kw in line for kw in ['Syntaxfehler', 'Syntax error', 'Error de sintaxis',
                                      'Erreur de syntaxe', 'Errore di sintassi',
                                      'Erro de sintaxe', 'codec can\'t',
                                      'Traceback', 'RuntimeError']):
            return True
        # "Fehler:" am Zeilenanfang = uncaught
        if line.strip().startswith('Fehler:'):
            return True
    return False

results = []
for fname, lang in TESTS:
    fpath = os.path.join(BASE, "sprach_tests", fname)
    r = subprocess.run(
        [sys.executable, os.path.join(BASE, "main.py"), fpath, lang],
        capture_output=True, text=True, encoding='utf-8', errors='replace',
        timeout=30, cwd=BASE
    )
    ok = r.returncode == 0 and not ist_echter_fehler(r.stdout, r.stderr)
    results.append((fname, lang, ok, r.stdout, r.stderr))
    status = "OK  " if ok else "FAIL"
    print(f"{status} [{lang:10s}] {fname}")
    if not ok:
        if r.stderr:
            print("       STDERR: " + r.stderr[:300].replace('\n',' '))
        for line in r.stdout.split('\n'):
            if any(kw in line for kw in ['Fehler:', 'Error', 'Syntax', 'codec', 'Traceback']):
                print("       STDOUT: " + line)

print()
print("=" * 55)
print("ERGEBNIS: " + str(sum(1 for _,_,ok,_,_ in results if ok)) + "/16 Programme erfolgreich")
print("=" * 55)
fehler = [(f,l,o,e) for f,l,ok,o,e in results if not ok]
if fehler:
    print("\nFEHLERDETAILS:")
    for fname, lang, out, err in fehler:
        print(f"\n  [{lang}] {fname}:")
        if err:
            print("    STDERR: " + err[:500])
        err_lines = [l for l in out.split('\n') if l.strip() and
                     any(kw in l for kw in ['Fehler:', 'Error', 'Syntax', 'codec', 'Zeile', 'ligne', 'linea', 'riga'])]
        for l in err_lines[:8]:
            print("    " + l)
else:
    print("\nAlle Programme laufen fehlerfrei!")
