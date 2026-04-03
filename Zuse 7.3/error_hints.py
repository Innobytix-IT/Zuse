# FILE: error_hints.py
# Anfaengerfreundliche Fehlertipps fuer Zuse — mehrsprachig
# Tipps werden ueber Fehler-Schluessel zugeordnet (nicht mehr via Regex auf deutschen Text)

from error_i18n import get_language

# Schluessel-basierte Tipps: ERR_KEY -> {lang: tipp}
KEY_HINTS = {
    "ERR_SYNTAX_EXPECTED_TYPE:KW_DANN": {
        "de": "Tipp: Nach einer WENN-Bedingung fehlt das Wort DANN.\nRichtig: WENN x > 5 DANN",
        "en": "Tip: The word THEN is missing after an IF condition.\nCorrect: IF x > 5 THEN",
        "es": "Consejo: Falta la palabra ENTONCES despues de una condicion SI.\nCorrecto: SI x > 5 ENTONCES",
        "fr": "Conseil: Le mot ALORS manque apres une condition SI.\nCorrect: SI x > 5 ALORS",
        "it": "Suggerimento: Manca la parola ALLORA dopo una condizione SE.\nCorretto: SE x > 5 ALLORA",
        "pt": "Dica: Falta a palavra ENTAO depois de uma condicao SE.\nCorreto: SE x > 5 ENTAO",
    },
    "ERR_SYNTAX_EXPECTED_TYPE:KW_MACHE": {
        "de": "Tipp: Nach SOLANGE/FÜR fehlt das Wort MACHE.\nRichtig: SOLANGE x > 0 MACHE",
        "en": "Tip: The word DO is missing after WHILE/FOR.\nCorrect: WHILE x > 0 DO",
        "es": "Consejo: Falta la palabra HACER despues de MIENTRAS/PARA.\nCorrecto: MIENTRAS x > 0 HACER",
        "fr": "Conseil: Le mot FAIRE manque apres TANT_QUE/POUR.\nCorrect: TANT_QUE x > 0 FAIRE",
        "it": "Suggerimento: Manca la parola FAI dopo FINCHE/PER.\nCorretto: FINCHE x > 0 FAI",
        "pt": "Dica: Falta a palavra FACA depois de ENQUANTO/PARA.\nCorreto: ENQUANTO x > 0 FACA",
    },
    "ERR_SYNTAX_EXPECTED_TYPE:KW_ENDE_WENN": {
        "de": "Tipp: Du hast vergessen, deine WENN-Bedingung mit ENDE WENN abzuschliessen.\nJeder WENN-Block braucht am Ende: ENDE WENN",
        "en": "Tip: You forgot to close your IF condition with END IF.\nEvery IF block needs: END IF",
        "es": "Consejo: Olvidaste cerrar tu condicion SI con FIN SI.\nCada bloque SI necesita: FIN SI",
        "fr": "Conseil: Tu as oublie de fermer ta condition SI avec FIN SI.\nChaque bloc SI a besoin de: FIN SI",
        "it": "Suggerimento: Hai dimenticato di chiudere la condizione SE con FINE SE.\nOgni blocco SE ha bisogno di: FINE SE",
        "pt": "Dica: Voce esqueceu de fechar a condicao SE com FIM SE.\nCada bloco SE precisa de: FIM SE",
    },
    "ERR_SYNTAX_EXPECTED_TYPE:KW_ENDE_FUNKTION": {
        "de": "Tipp: Du hast vergessen, deine Funktion mit ENDE FUNKTION abzuschliessen.\nJeder DEFINIERE-Block braucht am Ende: ENDE FUNKTION",
        "en": "Tip: You forgot to close your function with END FUNCTION.\nEvery DEFINE block needs: END FUNCTION",
        "es": "Consejo: Olvidaste cerrar tu funcion con FIN FUNCION.\nCada bloque DEFINIR necesita: FIN FUNCION",
        "fr": "Conseil: Tu as oublie de fermer ta fonction avec FIN FONCTION.\nChaque bloc DEFINIR a besoin de: FIN FONCTION",
        "it": "Suggerimento: Hai dimenticato di chiudere la funzione con FINE FUNZIONE.\nOgni blocco DEFINISCI ha bisogno di: FINE FUNZIONE",
        "pt": "Dica: Voce esqueceu de fechar a funcao com FIM FUNCAO.\nCada bloco DEFINIR precisa de: FIM FUNCAO",
    },
    "ERR_SYNTAX_EXPECTED_TYPE:KW_ENDE_SCHLEIFE": {
        "de": "Tipp: Du hast vergessen, deine Schleife mit ENDE SCHLEIFE abzuschliessen.\nJede Schleife braucht am Ende: ENDE SCHLEIFE",
        "en": "Tip: You forgot to close your loop with END LOOP.\nEvery loop needs: END LOOP",
        "es": "Consejo: Olvidaste cerrar tu bucle con FIN BUCLE.\nCada bucle necesita: FIN BUCLE",
        "fr": "Conseil: Tu as oublie de fermer ta boucle avec FIN BOUCLE.\nChaque boucle a besoin de: FIN BOUCLE",
        "it": "Suggerimento: Hai dimenticato di chiudere il ciclo con FINE CICLO.\nOgni ciclo ha bisogno di: FINE CICLO",
        "pt": "Dica: Voce esqueceu de fechar o laco com FIM LACO.\nCada laco precisa de: FIM LACO",
    },
    "ERR_SYNTAX_EXPECTED_TYPE:KW_ENDE_KLASSE": {
        "de": "Tipp: Du hast vergessen, deine Klasse mit ENDE KLASSE abzuschliessen.\nJede KLASSE braucht am Ende: ENDE KLASSE",
        "en": "Tip: You forgot to close your class with END CLASS.\nEvery CLASS needs: END CLASS",
        "es": "Consejo: Olvidaste cerrar tu clase con FIN CLASE.\nCada CLASE necesita: FIN CLASE",
        "fr": "Conseil: Tu as oublie de fermer ta classe avec FIN CLASSE.\nChaque CLASSE a besoin de: FIN CLASSE",
        "it": "Suggerimento: Hai dimenticato di chiudere la classe con FINE CLASSE.\nOgni CLASSE ha bisogno di: FINE CLASSE",
        "pt": "Dica: Voce esqueceu de fechar a classe com FIM CLASSE.\nCada CLASSE precisa de: FIM CLASSE",
    },
    "ERR_LOOP_EXPECTED_FOR_WHILE": {
        "de": "Tipp: Nach SCHLEIFE muss entweder FÜR oder SOLANGE kommen.\nBeispiel: SCHLEIFE FÜR i IN BEREICH(10) MACHE",
        "en": "Tip: After LOOP, either FOR or WHILE must follow.\nExample: LOOP FOR i IN RANGE(10) DO",
        "es": "Consejo: Despues de BUCLE, debe seguir PARA o MIENTRAS.\nEjemplo: BUCLE PARA i EN RANGO(10) HACER",
        "fr": "Conseil: Apres BOUCLE, il faut POUR ou TANT_QUE.\nExemple: BOUCLE POUR i DANS PLAGE(10) FAIRE",
        "it": "Suggerimento: Dopo CICLO, deve seguire PER o FINCHE.\nEsempio: CICLO PER i IN INTERVALLO(10) FAI",
        "pt": "Dica: Depois de LACO, deve seguir PARA ou ENQUANTO.\nExemplo: LACO PARA i EM INTERVALO(10) FACA",
    },
    "ERR_UNEXPECTED_TOKEN": {
        "de": "Tipp: In dieser Zeile steht etwas, das Zuse nicht versteht.\nPruefe Rechtschreibung und Einrueckung.",
        "en": "Tip: There is something on this line that Zuse doesn't understand.\nCheck spelling and indentation.",
        "es": "Consejo: Hay algo en esta linea que Zuse no entiende.\nRevisa la ortografia y la indentacion.",
        "fr": "Conseil: Il y a quelque chose sur cette ligne que Zuse ne comprend pas.\nVerifie l'orthographe et l'indentation.",
        "it": "Suggerimento: C'e qualcosa in questa riga che Zuse non capisce.\nControlla l'ortografia e l'indentazione.",
        "pt": "Dica: Ha algo nesta linha que Zuse nao entende.\nVerifique a ortografia e a indentacao.",
    },
    "ERR_VAR_NOT_DEFINED": {
        "de": "Tipp: Die Variable existiert noch nicht.\nWeise ihr zuerst einen Wert zu: variable = ...",
        "en": "Tip: The variable doesn't exist yet.\nAssign a value first: variable = ...",
        "es": "Consejo: La variable aun no existe.\nAsignale un valor primero: variable = ...",
        "fr": "Conseil: La variable n'existe pas encore.\nAssigne-lui d'abord une valeur: variable = ...",
        "it": "Suggerimento: La variabile non esiste ancora.\nAssegnale prima un valore: variabile = ...",
        "pt": "Dica: A variavel ainda nao existe.\nAtribua um valor primeiro: variavel = ...",
    },
    "ERR_DIVISION_BY_ZERO": {
        "de": "Tipp: Du versuchst durch 0 zu teilen — das ist mathematisch nicht erlaubt.\nPruefe den Wert des Nenners mit einer WENN-Abfrage.",
        "en": "Tip: You're trying to divide by 0 — that's not allowed in math.\nCheck the denominator value with an IF statement.",
        "es": "Consejo: Intentas dividir por 0 — no esta permitido en matematicas.\nVerifica el valor del denominador con una instruccion SI.",
        "fr": "Conseil: Tu essaies de diviser par 0 — c'est interdit en mathematiques.\nVerifie la valeur du denominateur avec une instruction SI.",
        "it": "Suggerimento: Stai cercando di dividere per 0 — non e consentito in matematica.\nControlla il valore del denominatore con un'istruzione SE.",
        "pt": "Dica: Voce esta tentando dividir por 0 — nao e permitido em matematica.\nVerifique o valor do denominador com uma instrucao SE.",
    },
    "ERR_INCOMPATIBLE_TYPES": {
        "de": "Tipp: Du versuchst verschiedene Datentypen zu kombinieren.\nNutze str() um Zahlen in Text umzuwandeln: \"Ergebnis: \" + str(42)",
        "en": "Tip: You're trying to combine different data types.\nUse str() to convert numbers to text: \"Result: \" + str(42)",
        "es": "Consejo: Intentas combinar diferentes tipos de datos.\nUsa str() para convertir numeros a texto: \"Resultado: \" + str(42)",
        "fr": "Conseil: Tu essaies de combiner differents types de donnees.\nUtilise str() pour convertir les nombres en texte: \"Resultat: \" + str(42)",
        "it": "Suggerimento: Stai cercando di combinare tipi di dati diversi.\nUsa str() per convertire i numeri in testo: \"Risultato: \" + str(42)",
        "pt": "Dica: Voce esta tentando combinar diferentes tipos de dados.\nUse str() para converter numeros em texto: \"Resultado: \" + str(42)",
    },
    "ERR_NOT_ITERABLE": {
        "de": "Tipp: Du versuchst ueber etwas zu schleifen, das keine Liste ist.\nNutze BEREICH() fuer Zahlen: SCHLEIFE FÜR i IN BEREICH(10) MACHE",
        "en": "Tip: You're trying to loop over something that is not a list.\nUse RANGE() for numbers: LOOP FOR i IN RANGE(10) DO",
        "es": "Consejo: Intentas iterar sobre algo que no es una lista.\nUsa RANGO() para numeros: BUCLE PARA i EN RANGO(10) HACER",
        "fr": "Conseil: Tu essaies de boucler sur quelque chose qui n'est pas une liste.\nUtilise PLAGE() pour les nombres: BOUCLE POUR i DANS PLAGE(10) FAIRE",
        "it": "Suggerimento: Stai cercando di iterare su qualcosa che non e una lista.\nUsa INTERVALLO() per i numeri: CICLO PER i IN INTERVALLO(10) FAI",
        "pt": "Dica: Voce esta tentando iterar sobre algo que nao e uma lista.\nUse INTERVALO() para numeros: LACO PARA i EM INTERVALO(10) FACA",
    },
    "ERR_MAX_RECURSION": {
        "de": "Tipp: Deine Funktion ruft sich selbst zu oft auf (Endlosrekursion).\nPruefe deine Abbruchbedingung — wann soll die Rekursion stoppen?",
        "en": "Tip: Your function calls itself too often (infinite recursion).\nCheck your base case — when should the recursion stop?",
        "es": "Consejo: Tu funcion se llama a si misma demasiadas veces (recursion infinita).\nRevisa tu caso base — cuando debe parar la recursion?",
        "fr": "Conseil: Ta fonction s'appelle elle-meme trop souvent (recursion infinie).\nVerifie ta condition d'arret — quand la recursion doit-elle s'arreter?",
        "it": "Suggerimento: La tua funzione chiama se stessa troppo spesso (ricorsione infinita).\nControlla il caso base — quando deve fermarsi la ricorsione?",
        "pt": "Dica: Sua funcao chama a si mesma muitas vezes (recursao infinita).\nVerifique o caso base — quando a recursao deve parar?",
    },
    "ERR_NOT_A_CLASS": {
        "de": "Tipp: Dieses Objekt wurde nicht als KLASSE definiert.\nKlassen werden so definiert: KLASSE Name: ... ENDE KLASSE",
        "en": "Tip: This object was not defined as a CLASS.\nClasses are defined like: CLASS Name: ... END CLASS",
        "es": "Consejo: Este objeto no fue definido como una CLASE.\nLas clases se definen asi: CLASE Nombre: ... FIN CLASE",
        "fr": "Conseil: Cet objet n'a pas ete defini comme une CLASSE.\nLes classes se definissent: CLASSE Nom: ... FIN CLASSE",
        "it": "Suggerimento: Questo oggetto non e stato definito come una CLASSE.\nLe classi si definiscono: CLASSE Nome: ... FINE CLASSE",
        "pt": "Dica: Este objeto nao foi definido como uma CLASSE.\nClasses sao definidas assim: CLASSE Nome: ... FIM CLASSE",
    },
    "ERR_MODULE_NOT_FOUND": {
        "de": "Tipp: Das Modul konnte nicht geladen werden.\nIst es installiert? Nutze zpkg fuer Zuse-Pakete.",
        "en": "Tip: The module could not be loaded.\nIs it installed? Use zpkg for Zuse packages.",
        "es": "Consejo: El modulo no se pudo cargar.\nEsta instalado? Usa zpkg para paquetes Zuse.",
        "fr": "Conseil: Le module n'a pas pu etre charge.\nEst-il installe? Utilise zpkg pour les paquets Zuse.",
        "it": "Suggerimento: Il modulo non puo essere caricato.\nE installato? Usa zpkg per i pacchetti Zuse.",
        "pt": "Dica: O modulo nao pode ser carregado.\nEsta instalado? Use zpkg para pacotes Zuse.",
    },
    "ERR_SECURITY_BLOCK": {
        "de": "Tipp: Im Lernmodus ist dieses Modul gesperrt.\nWechsle in den Profi-Modus um alle Module zu nutzen.",
        "en": "Tip: This module is blocked in learning mode.\nSwitch to expert mode to use all modules.",
        "es": "Consejo: Este modulo esta bloqueado en modo aprendizaje.\nCambia al modo experto para usar todos los modulos.",
        "fr": "Conseil: Ce module est bloque en mode apprentissage.\nPasse en mode expert pour utiliser tous les modules.",
        "it": "Suggerimento: Questo modulo e bloccato in modalita apprendimento.\nPassa alla modalita esperto per usare tutti i moduli.",
        "pt": "Dica: Este modulo esta bloqueado no modo aprendizagem.\nMude para o modo especialista para usar todos os modulos.",
    },
    "ERR_MULTI_ASSIGN_MISMATCH": {
        "de": "Tipp: Links und rechts vom = muessen gleich viele Werte stehen.",
        "en": "Tip: The number of targets and values on each side of = must match.",
        "es": "Consejo: El numero de objetivos y valores a cada lado del = debe coincidir.",
        "fr": "Conseil: Le nombre de cibles et de valeurs de chaque cote du = doit correspondre.",
        "it": "Suggerimento: Il numero di obiettivi e valori su ogni lato del = deve corrispondere.",
        "pt": "Dica: O numero de alvos e valores de cada lado do = deve ser igual.",
    },
    "ERR_CANNOT_SET_ATTR": {
        "de": "Tipp: Das Attribut kann nicht gesetzt werden.\nIst das Objekt vom richtigen Typ?",
        "en": "Tip: The attribute cannot be set.\nIs the object of the correct type?",
        "es": "Consejo: El atributo no se puede establecer.\nEs el objeto del tipo correcto?",
        "fr": "Conseil: L'attribut ne peut pas etre defini.\nL'objet est-il du bon type?",
        "it": "Suggerimento: L'attributo non puo essere impostato.\nL'oggetto e del tipo corretto?",
        "pt": "Dica: O atributo nao pode ser definido.\nO objeto e do tipo correto?",
    },
}


def get_hint(error_key_or_message, context=None):
    """
    Gibt einen hilfreichen Tipp zurueck.

    Akzeptiert entweder:
    - Einen ERR_* Schluessel (z.B. 'ERR_VAR_NOT_DEFINED') mit optionalem Kontext
    - Einen Fehlermeldungs-Text (Rueckwaertskompatibilitaet) — wird per Fallback gematcht

    Args:
        error_key_or_message: ERR_*-Schluessel oder Fehlermeldungs-Text
        context: Optionaler Kontext-String (z.B. 'KW_DANN')
    Returns:
        Tipp-String in der aktuellen Sprache oder None.
    """
    lang = get_language()

    # Versuche spezifischen Schluessel mit Kontext
    if context:
        specific_key = f"{error_key_or_message}:{context}"
        if specific_key in KEY_HINTS:
            hints = KEY_HINTS[specific_key]
            return hints.get(lang) or hints.get("de")

    # Versuche allgemeinen Schluessel
    if error_key_or_message in KEY_HINTS:
        hints = KEY_HINTS[error_key_or_message]
        return hints.get(lang) or hints.get("de")

    # Fallback: Text-basiertes Matching (Rueckwaertskompatibilitaet)
    return _fallback_hint_match(str(error_key_or_message))


def format_error_with_hint(error_message, error_key=None, context=None):
    """
    Formatiert eine Fehlermeldung mit optionalem Tipp.

    Args:
        error_message: Die Fehlermeldung (String oder Exception)
        error_key: Optionaler ERR_* Schluessel fuer praezise Tipp-Zuordnung
        context: Optionaler Kontext fuer spezifischere Tipps
    Returns:
        Formatierte Fehlermeldung mit Tipp (falls vorhanden).
    """
    msg = str(error_message)
    hint = None

    # Primaer: Schluessel-basierte Zuordnung
    if error_key:
        hint = get_hint(error_key, context)

    # Fallback: Versuche alle Schluessel via einfaches Matching
    if not hint:
        hint = _fallback_hint_match(msg)

    if hint:
        return f"{msg}\n\n{hint}"
    return msg


def _fallback_hint_match(error_message):
    """Fallback-Matching: Erkennt Fehlertyp anhand von Mustern in der Nachricht.
    Funktioniert fuer Fehlermeldungen aller Sprachen."""
    import re
    lang = get_language()
    msg = str(error_message)

    # ── Schritt 1: Fuer Syntax-Fehler das ERWARTETE Token extrahieren ──
    # Fehlermeldungen haben das Format: "... Erwartet 'KW_XYZ', gefunden ..."
    # Wir matchen NUR auf das erwartete Token, nicht auf das gefundene.
    expected_match = re.search(
        r"(?:Erwartet|Expected|Esperado|Attendu|Previsto)\s+'(KW_\w+)'", msg
    )
    if expected_match:
        expected_kw = expected_match.group(1)
        # Direkt im KEY_HINTS nachschlagen
        hint = get_hint("ERR_SYNTAX_EXPECTED_TYPE", expected_kw)
        if hint:
            return hint

    # ── Schritt 2: Allgemeine Muster (nicht-Syntax-Fehler) ──
    FALLBACK_PATTERNS = [
        (r"Erwartet F.R oder SOLANGE|Expected FOR or WHILE|Loop error|Schleifenfehler", "ERR_LOOP_EXPECTED_FOR_WHILE", None),
        (r"Unerwartetes Token|Unexpected token|Token inesperado|Jeton inattendu|Token inaspettato", "ERR_UNEXPECTED_TOKEN", None),
        (r"nicht definiert|not defined|no definid|non defini|nao definid", "ERR_VAR_NOT_DEFINED", None),
        (r"Division durch Null|Division by zero|division por cero|division par zero|divisione per zero|Divisao por zero", "ERR_DIVISION_BY_ZERO", None),
        (r"Unvertr.gliche Typen|Incompatible types|Tipos incompatible|Types incompatible|Tipi incompatibil", "ERR_INCOMPATIBLE_TYPES", None),
        (r"nicht iterierbar|not iterable|no es iterable|pas iterable|non .+ iterabil|nao .+ iteravel", "ERR_NOT_ITERABLE", None),
        (r"Rekursionstiefe|recursion depth|profundidad.*recursion|profondeur.*recursion|ricorsione|recursao", "ERR_MAX_RECURSION", None),
        (r"keine Klasse|not a class|no es una clase|pas une classe|non .+ classe|nao .+ classe", "ERR_NOT_A_CLASS", None),
        (r"Modul.*nicht gefunden|Module.*not found|[Mm]odulo.*no encontrad|[Mm]odule.*non trouv|[Mm]odulo.*non trovato|[Mm]odulo.*nao encontrad", "ERR_MODULE_NOT_FOUND", None),
        (r"Sicherheits-Sperre|Security lock|Bloqueo de seguridad|Verrou de securite|Blocco di sicurezza|Bloqueio de seguranca", "ERR_SECURITY_BLOCK", None),
        (r"Mehrfach-Zuweisung|Multiple assignment|Asignacion multiple|Affectation multiple|Assegnazione multipla|Atribuicao multipla", "ERR_MULTI_ASSIGN_MISMATCH", None),
        (r"Kann Attribut|Cannot set attribute|No se puede establecer|Impossible de definir|Impossibile impostare|Nao e possivel definir", "ERR_CANNOT_SET_ATTR", None),
    ]

    for pattern, err_key, ctx in FALLBACK_PATTERNS:
        if re.search(pattern, msg, re.IGNORECASE):
            hint = get_hint(err_key, ctx)
            if hint:
                return hint

    return None
