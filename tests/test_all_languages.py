#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZUSE v7.3 — Vollständiger Runtime-Test für alle 8 Sprachen
Testet: Variablen, Ausgabe, If/Else, Schleifen, Funktionen, Klassen, Try/Catch, Lambda, Switch/Case
"""
import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'Zuse 7.3')
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import json
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

# ============================================================
# Testprogramme für jede Sprache
# ============================================================

TESTS = {
    # ─── DEUTSCH ───────────────────────────────────────────
    "deutsch": """
x = 10
y = 20
summe = x + y
AUSGABE "=== DEUTSCH ==="
AUSGABE "Summe: " + str(summe)

WENN x < y DANN
    AUSGABE "x ist kleiner"
SONST
    AUSGABE "x ist groesser"
ENDE WENN

SCHLEIFE FÜR i IN [1, 2, 3] MACHE
    AUSGABE "Zahl: " + str(i)
ENDE SCHLEIFE

zähler = 0
SCHLEIFE SOLANGE zähler < 3 MACHE
    zähler = zähler + 1
ENDE SCHLEIFE
AUSGABE "Zähler: " + str(zähler)

DEFINIERE verdopple(n):
    ERGEBNIS IST n * 2
ENDE FUNKTION
AUSGABE "Verdoppelt: " + str(verdopple(7))

KLASSE Tier:
    DEFINIERE ERSTELLE(name):
        MEIN.name = name
    ENDE FUNKTION
    DEFINIERE sprechen():
        ERGEBNIS IST MEIN.name + " sagt Hallo"
    ENDE FUNKTION
ENDE KLASSE
t = Tier("Hund")
AUSGABE t.sprechen()

VERSUCHE
    x = 1 / 0
FANGE fehler
    AUSGABE "Fehler gefangen: OK"
ENDE VERSUCHE

doppel = AKTION(a): a * 2
AUSGABE "Lambda: " + str(doppel(5))

WÄHLE 2
    FALL 1 DANN
        AUSGABE "Eins"
    FALL 2 DANN
        AUSGABE "Zwei"
    FALL 3 DANN
        AUSGABE "Drei"
ENDE WÄHLE

AUSGABE "--- DEUTSCH OK ---"
""",

    # ─── ENGLISH ───────────────────────────────────────────
    "english": """
x = 10
y = 20
total = x + y
PRINT "=== ENGLISH ==="
PRINT "Sum: " + str(total)

IF x < y THEN
    PRINT "x is smaller"
ELSE
    PRINT "x is bigger"
END IF

LOOP FOR i IN [1, 2, 3] DO
    PRINT "Number: " + str(i)
END LOOP

counter = 0
LOOP WHILE counter < 3 DO
    counter = counter + 1
END LOOP
PRINT "Counter: " + str(counter)

DEFINE double(n):
    RETURN n * 2
END FUNCTION
PRINT "Doubled: " + str(double(7))

CLASS Animal:
    DEFINE NEW(name):
        SELF.name = name
    END FUNCTION
    DEFINE speak():
        RETURN SELF.name + " says Hello"
    END FUNCTION
END CLASS
a = Animal("Dog")
PRINT a.speak()

TRY
    x = 1 / 0
CATCH error
    PRINT "Error caught: OK"
END TRY

dbl = LAMBDA(a): a * 2
PRINT "Lambda: " + str(dbl(5))

SWITCH 2
    CASE 1 THEN
        PRINT "One"
    CASE 2 THEN
        PRINT "Two"
    CASE 3 THEN
        PRINT "Three"
END SWITCH

PRINT "--- ENGLISH OK ---"
""",

    # ─── ESPAÑOL ───────────────────────────────────────────
    "espaniol": """
x = 10
y = 20
suma = x + y
IMPRIMIR "=== ESPAÑOL ==="
IMPRIMIR "Suma: " + str(suma)

SI x < y ENTONCES
    IMPRIMIR "x es menor"
SINO
    IMPRIMIR "x es mayor"
FIN SI

BUCLE PARA i EN [1, 2, 3] HACER
    IMPRIMIR "Numero: " + str(i)
FIN BUCLE

contador = 0
BUCLE MIENTRAS contador < 3 HACER
    contador = contador + 1
FIN BUCLE
IMPRIMIR "Contador: " + str(contador)

DEFINIR duplicar(n):
    RETORNO n * 2
FIN FUNCION
IMPRIMIR "Duplicado: " + str(duplicar(7))

CLASE Animal:
    DEFINIR CREAR(nombre):
        MIO.nombre = nombre
    FIN FUNCION
    DEFINIR hablar():
        RETORNO MIO.nombre + " dice Hola"
    FIN FUNCION
FIN CLASE
a = Animal("Perro")
IMPRIMIR a.hablar()

INTENTAR
    x = 1 / 0
CAPTURAR error
    IMPRIMIR "Error capturado: OK"
FIN INTENTAR

doble = ACCION(a): a * 2
IMPRIMIR "Lambda: " + str(doble(5))

ELEGIR 2
    CASO 1 ENTONCES
        IMPRIMIR "Uno"
    CASO 2 ENTONCES
        IMPRIMIR "Dos"
    CASO 3 ENTONCES
        IMPRIMIR "Tres"
FIN ELEGIR

IMPRIMIR "--- ESPAÑOL OK ---"
""",

    # ─── FRANÇAIS ──────────────────────────────────────────
    "francais": """
x = 10
y = 20
somme = x + y
IMPRIMER "=== FRANÇAIS ==="
IMPRIMER "Somme: " + str(somme)

SI x < y ALORS
    IMPRIMER "x est plus petit"
SINON
    IMPRIMER "x est plus grand"
FIN SI

BOUCLE POUR i DANS [1, 2, 3] FAIRE
    IMPRIMER "Nombre: " + str(i)
FIN BOUCLE

compteur = 0
BOUCLE TANTQUE compteur < 3 FAIRE
    compteur = compteur + 1
FIN BOUCLE
IMPRIMER "Compteur: " + str(compteur)

DEFINIR doubler(n):
    RETOURNER n * 2
FIN FONCTION
IMPRIMER "Double: " + str(doubler(7))

CLASSE Animal:
    DEFINIR CREER(nom):
        MOI.nom = nom
    FIN FONCTION
    DEFINIR parler():
        RETOURNER MOI.nom + " dit Bonjour"
    FIN FONCTION
FIN CLASSE
a = Animal("Chien")
IMPRIMER a.parler()

ESSAYER
    x = 1 / 0
ATTRAPER erreur
    IMPRIMER "Erreur attrapee: OK"
FIN ESSAYER

dbl = ACTION(a): a * 2
IMPRIMER "Lambda: " + str(dbl(5))

CHOISIR 2
    CAS 1 ALORS
        IMPRIMER "Un"
    CAS 2 ALORS
        IMPRIMER "Deux"
    CAS 3 ALORS
        IMPRIMER "Trois"
FIN CHOISIR

IMPRIMER "--- FRANÇAIS OK ---"
""",

    # ─── ITALIANO ──────────────────────────────────────────
    "italiano": """
x = 10
y = 20
somma = x + y
STAMPA "=== ITALIANO ==="
STAMPA "Somma: " + str(somma)

SE x < y ALLORA
    STAMPA "x e minore"
ALTRIMENTI
    STAMPA "x e maggiore"
FINE SE

CICLO PER i IN [1, 2, 3] FARE
    STAMPA "Numero: " + str(i)
FINE CICLO

contatore = 0
CICLO MENTRE contatore < 3 FARE
    contatore = contatore + 1
FINE CICLO
STAMPA "Contatore: " + str(contatore)

DEFINIRE raddoppiare(n):
    RITORNA n * 2
FINE FUNZIONE
STAMPA "Raddoppiato: " + str(raddoppiare(7))

CLASSE Animale:
    DEFINIRE CREARE(nome):
        MIO.nome = nome
    FINE FUNZIONE
    DEFINIRE parlare():
        RITORNA MIO.nome + " dice Ciao"
    FINE FUNZIONE
FINE CLASSE
a = Animale("Cane")
STAMPA a.parlare()

PROVA
    x = 1 / 0
CATTURA errore
    STAMPA "Errore catturato: OK"
FINE PROVA

doppio = AZIONE(a): a * 2
STAMPA "Lambda: " + str(doppio(5))

SCEGLI 2
    CASO 1 ALLORA
        STAMPA "Uno"
    CASO 2 ALLORA
        STAMPA "Due"
    CASO 3 ALLORA
        STAMPA "Tre"
FINE SCEGLI

STAMPA "--- ITALIANO OK ---"
""",

    # ─── PORTUGUÊS ─────────────────────────────────────────
    "portugues": """
x = 10
y = 20
soma = x + y
IMPRIMIR "=== PORTUGUÊS ==="
IMPRIMIR "Soma: " + str(soma)

SE x < y ENTAO
    IMPRIMIR "x e menor"
SENAO
    IMPRIMIR "x e maior"
FIM SE

CICLO PARA i EM [1, 2, 3] FACA
    IMPRIMIR "Numero: " + str(i)
FIM CICLO

contador = 0
CICLO ENQUANTO contador < 3 FACA
    contador = contador + 1
FIM CICLO
IMPRIMIR "Contador: " + str(contador)

DEFINIR dobrar(n):
    RETORNO n * 2
FIM FUNCAO
IMPRIMIR "Dobrado: " + str(dobrar(7))

CLASSE Animal:
    DEFINIR CRIAR(nome):
        MEU.nome = nome
    FIM FUNCAO
    DEFINIR falar():
        RETORNO MEU.nome + " diz Ola"
    FIM FUNCAO
FIM CLASSE
a = Animal("Cao")
IMPRIMIR a.falar()

TENTAR
    x = 1 / 0
PEGAR erro
    IMPRIMIR "Erro capturado: OK"
FIM TENTAR

dobro = ACAO(a): a * 2
IMPRIMIR "Lambda: " + str(dobro(5))

ESCOLHER 2
    CASO 1 ENTAO
        IMPRIMIR "Um"
    CASO 2 ENTAO
        IMPRIMIR "Dois"
    CASO 3 ENTAO
        IMPRIMIR "Tres"
FIM ESCOLHER

IMPRIMIR "--- PORTUGUÊS OK ---"
""",

    # ─── हिन्दी (HINDI) ────────────────────────────────────
    "hindi": """
x = 10
y = 20
योग = x + y
दिखाओ "=== हिन्दी ==="
दिखाओ "योग: " + str(योग)

अगर x < y तो
    दिखाओ "x छोटा है"
वरना
    दिखाओ "x बड़ा है"
अंत अगर

चक्र हर i में [1, 2, 3] करो
    दिखाओ "संख्या: " + str(i)
अंत चक्र

गिनती = 0
चक्र जबतक गिनती < 3 करो
    गिनती = गिनती + 1
अंत चक्र
दिखाओ "गिनती: " + str(गिनती)

परिभाषा दुगुना(n):
    परिणाम है n * 2
अंत फलन
दिखाओ "दुगुना: " + str(दुगुना(7))

वर्ग पशु:
    परिभाषा नया(नाम):
        मेरा.नाम = नाम
    अंत फलन
    परिभाषा बोलो():
        परिणाम है मेरा.नाम + " कहता नमस्ते"
    अंत फलन
अंत वर्ग
p = पशु("कुत्ता")
दिखाओ p.बोलो()

प्रयास
    x = 1 / 0
पकड़ो त्रुटि
    दिखाओ "त्रुटि पकड़ी: OK"
अंत प्रयास

दो_गुना = क्रिया(a): a * 2
दिखाओ "Lambda: " + str(दो_गुना(5))

चुनो 2
    स्थिति 1 तो
        दिखाओ "एक"
    स्थिति 2 तो
        दिखाओ "दो"
    स्थिति 3 तो
        दिखाओ "तीन"
अंत चुनो

दिखाओ "--- हिन्दी OK ---"
""",

    # ─── 中文 (CHINESE) ────────────────────────────────────
    "zhongwen": """
x = 10
y = 20
总和 = x + y
输出 "=== 中文 ==="
输出 "总和: " + str(总和)

如果 x < y 则
    输出 "x 更小"
否则
    输出 "x 更大"
结束 如果

循环 每个 i 在 [1, 2, 3] 执行
    输出 "数字: " + str(i)
结束 循环

计数 = 0
循环 当 计数 < 3 执行
    计数 = 计数 + 1
结束 循环
输出 "计数: " + str(计数)

定义 翻倍(n):
    返回 n * 2
结束 函数
输出 "翻倍: " + str(翻倍(7))

类 动物:
    定义 创建(名字):
        自己.名字 = 名字
    结束 函数
    定义 说话():
        返回 自己.名字 + " 说你好"
    结束 函数
结束 类
a = 动物("狗")
输出 a.说话()

尝试
    x = 1 / 0
捕获 错误
    输出 "错误捕获: OK"
结束 尝试

双倍 = 匿名(a): a * 2
输出 "Lambda: " + str(双倍(5))

选择 2
    情况 1 则
        输出 "一"
    情况 2 则
        输出 "二"
    情况 3 则
        输出 "三"
结束 选择

输出 "--- 中文 OK ---"
""",
}

# ============================================================
# Erwartete Ausgaben (vereinfacht — Kernprüfungen)
# ============================================================
EXPECTED_LINES = {
    "deutsch":  ["=== DEUTSCH ===", "Summe: 30", "x ist kleiner", "Zahl: 1", "Zähler: 3", "Verdoppelt: 14", "Hund sagt Hallo", "Fehler gefangen: OK", "Lambda: 10", "Zwei", "--- DEUTSCH OK ---"],
    "english":  ["=== ENGLISH ===", "Sum: 30", "x is smaller", "Number: 1", "Counter: 3", "Doubled: 14", "Dog says Hello", "Error caught: OK", "Lambda: 10", "Two", "--- ENGLISH OK ---"],
    "espaniol": ["=== ESPAÑOL ===", "Suma: 30", "x es menor", "Numero: 1", "Contador: 3", "Duplicado: 14", "Perro dice Hola", "Error capturado: OK", "Lambda: 10", "Dos", "--- ESPAÑOL OK ---"],
    "francais": ["=== FRANÇAIS ===", "Somme: 30", "x est plus petit", "Nombre: 1", "Compteur: 3", "Double: 14", "Chien dit Bonjour", "Erreur attrapee: OK", "Lambda: 10", "Deux", "--- FRANÇAIS OK ---"],
    "italiano": ["=== ITALIANO ===", "Somma: 30", "x e minore", "Numero: 1", "Contatore: 3", "Raddoppiato: 14", "Cane dice Ciao", "Errore catturato: OK", "Lambda: 10", "Due", "--- ITALIANO OK ---"],
    "portugues":["=== PORTUGUÊS ===", "Soma: 30", "x e menor", "Numero: 1", "Contador: 3", "Dobrado: 14", "Cao diz Ola", "Erro capturado: OK", "Lambda: 10", "Dois", "--- PORTUGUÊS OK ---"],
    "hindi":    ["=== हिन्दी ===", "योग: 30", "x छोटा है", "संख्या: 1", "गिनती: 3", "दुगुना: 14", "कुत्ता कहता नमस्ते", "त्रुटि पकड़ी: OK", "Lambda: 10", "दो", "--- हिन्दी OK ---"],
    "zhongwen": ["=== 中文 ===", "总和: 30", "x 更小", "数字: 1", "计数: 3", "翻倍: 14", "狗 说你好", "错误捕获: OK", "Lambda: 10", "二", "--- 中文 OK ---"],
}

# ============================================================
# Test-Runner
# ============================================================
def run_test(lang_name, code):
    """Führt ein Zuse-Programm durch Lexer → Parser → Interpreter."""
    config_path = f'Zuse 7.3/sprachen/{lang_name}.json'
    with open(config_path, encoding='utf-8') as f:
        config = json.load(f)

    output_lines = []
    def capture(text):
        output_lines.append(str(text))

    try:
        lexer = Lexer(config)
        tokens = lexer.tokenize(code)
        parser = Parser(tokens)
        ast = parser.parse()
        interp = Interpreter(output_callback=capture, sprache=lang_name)
        interp.interpretiere(ast)
        return output_lines, None
    except Exception as e:
        return output_lines, str(e)


def main():
    total_pass = 0
    total_fail = 0
    failed_langs = []

    print("=" * 70)
    print("  ZUSE v7.3 — VOLLSTÄNDIGER RUNTIME-TEST (8 Sprachen)")
    print("=" * 70)
    print()

    for lang in ["deutsch", "english", "espaniol", "francais", "italiano", "portugues", "hindi", "zhongwen"]:
        code = TESTS[lang]
        expected = EXPECTED_LINES[lang]

        output, error = run_test(lang, code)

        if error:
            print(f"  ❌ {lang.upper():12} — FEHLER: {error}")
            total_fail += 1
            failed_langs.append((lang, f"Exception: {error}"))
            print()
            continue

        # Prüfe erwartete Ausgaben
        missing = []
        for exp_line in expected:
            if not any(exp_line in out for out in output):
                missing.append(exp_line)

        if missing:
            print(f"  ❌ {lang.upper():12} — {len(missing)} fehlende Ausgaben:")
            for m in missing:
                print(f"       FEHLT: \"{m}\"")
            print(f"       TATSÄCHLICH ({len(output)} Zeilen):")
            for o in output:
                print(f"         > {o}")
            total_fail += 1
            failed_langs.append((lang, f"Missing: {missing}"))
        else:
            print(f"  ✅ {lang.upper():12} — ALLE {len(expected)} Prüfungen bestanden")
            total_pass += 1

        print()

    # Zusammenfassung
    print("=" * 70)
    print(f"  ERGEBNIS: {total_pass}/8 Sprachen bestanden, {total_fail} fehlgeschlagen")
    print("=" * 70)
    if failed_langs:
        print("\n  Fehlgeschlagene Sprachen:")
        for lang, reason in failed_langs:
            print(f"    - {lang}: {reason}")
    else:
        print("\n  🎉 ALLE 8 SPRACHEN FUNKTIONIEREN EINWANDFREI!")
    print()

if __name__ == '__main__':
    main()
