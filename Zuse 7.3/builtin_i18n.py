# FILE: builtin_i18n.py — Mehrsprachige Builtin-Übersetzungen für ZUSE 7.3
#
# Jede Builtin-Funktion hat einen kanonischen (deutschen) Namen.
# Diese Tabelle mappt den deutschen Namen auf Übersetzungen in allen Sprachen.
# Deutsch ist IMMER als Fallback verfügbar.

# ─── Builtin-Funktionen ──────────────────────────────────────────────
# Schlüssel = deutscher Originalname
# Werte = {sprach_code: übersetzter Name}

BUILTIN_TRANSLATIONS = {
    # ─── Typ-Konvertierung & Utilities ────────────────────────────────
    'str': {
        'de': 'str', 'en': 'str', 'es': 'str', 'fr': 'str', 'it': 'str', 'pt': 'str'
    },
    'int': {
        'de': 'int', 'en': 'int', 'es': 'int', 'fr': 'int', 'it': 'int', 'pt': 'int'
    },
    'float': {
        'de': 'float', 'en': 'float', 'es': 'float', 'fr': 'float', 'it': 'float', 'pt': 'float'
    },
    'len': {
        'de': 'len', 'en': 'len', 'es': 'len', 'fr': 'len', 'it': 'len', 'pt': 'len'
    },
    'typ': {
        'de': 'typ', 'en': 'type', 'es': 'tipo', 'fr': 'type', 'it': 'tipo', 'pt': 'tipo'
    },
    'liste': {
        'de': 'liste', 'en': 'list', 'es': 'lista', 'fr': 'liste', 'it': 'lista', 'pt': 'lista'
    },
    'dict': {
        'de': 'dict', 'en': 'dict', 'es': 'dict', 'fr': 'dict', 'it': 'dict', 'pt': 'dict'
    },

    # ─── Bereich ──────────────────────────────────────────────────────
    'BEREICH': {
        'de': 'BEREICH', 'en': 'RANGE', 'es': 'RANGO', 'fr': 'PLAGE', 'it': 'INTERVALLO', 'pt': 'INTERVALO'
    },
    'BEREICH_LISTE': {
        'de': 'BEREICH_LISTE', 'en': 'RANGE_LIST', 'es': 'LISTA_RANGO', 'fr': 'LISTE_PLAGE', 'it': 'LISTA_INTERVALLO', 'pt': 'LISTA_INTERVALO'
    },
    'FORMAT': {
        'de': 'FORMAT', 'en': 'FORMAT', 'es': 'FORMATO', 'fr': 'FORMAT', 'it': 'FORMATO', 'pt': 'FORMATO'
    },

    # ─── Mathe ────────────────────────────────────────────────────────
    'PI': {
        'de': 'PI', 'en': 'PI', 'es': 'PI', 'fr': 'PI', 'it': 'PI', 'pt': 'PI'
    },
    'E': {
        'de': 'E', 'en': 'E', 'es': 'E', 'fr': 'E', 'it': 'E', 'pt': 'E'
    },
    'WURZEL': {
        'de': 'WURZEL', 'en': 'SQRT', 'es': 'RAIZ', 'fr': 'RACINE', 'it': 'RADICE', 'pt': 'RAIZ'
    },
    'SINUS': {
        'de': 'SINUS', 'en': 'SIN', 'es': 'SENO', 'fr': 'SINUS', 'it': 'SENO', 'pt': 'SENO'
    },
    'COSINUS': {
        'de': 'COSINUS', 'en': 'COS', 'es': 'COSENO', 'fr': 'COSINUS', 'it': 'COSENO', 'pt': 'COSENO'
    },
    'TANGENS': {
        'de': 'TANGENS', 'en': 'TAN', 'es': 'TANGENTE', 'fr': 'TANGENTE', 'it': 'TANGENTE', 'pt': 'TANGENTE'
    },
    'RUNDEN': {
        'de': 'RUNDEN', 'en': 'ROUND', 'es': 'REDONDEAR', 'fr': 'ARRONDIR', 'it': 'ARROTONDARE', 'pt': 'ARREDONDAR'
    },
    'ABSOLUT': {
        'de': 'ABSOLUT', 'en': 'ABS', 'es': 'ABSOLUTO', 'fr': 'ABSOLU', 'it': 'ASSOLUTO', 'pt': 'ABSOLUTO'
    },
    'POTENZ': {
        'de': 'POTENZ', 'en': 'POWER', 'es': 'POTENCIA', 'fr': 'PUISSANCE', 'it': 'POTENZA', 'pt': 'POTENCIA'
    },
    'LOGARITHMUS': {
        'de': 'LOGARITHMUS', 'en': 'LOG', 'es': 'LOGARITMO', 'fr': 'LOGARITHME', 'it': 'LOGARITMO', 'pt': 'LOGARITMO'
    },
    'MINIMUM': {
        'de': 'MINIMUM', 'en': 'MIN', 'es': 'MINIMO', 'fr': 'MINIMUM', 'it': 'MINIMO', 'pt': 'MINIMO'
    },
    'MAXIMUM': {
        'de': 'MAXIMUM', 'en': 'MAX', 'es': 'MAXIMO', 'fr': 'MAXIMUM', 'it': 'MASSIMO', 'pt': 'MAXIMO'
    },
    'SUMME': {
        'de': 'SUMME', 'en': 'SUM', 'es': 'SUMA', 'fr': 'SOMME', 'it': 'SOMMA', 'pt': 'SOMA'
    },
    'BODEN': {
        'de': 'BODEN', 'en': 'FLOOR', 'es': 'PISO', 'fr': 'PLANCHER', 'it': 'PAVIMENTO', 'pt': 'PISO'
    },
    'DECKE': {
        'de': 'DECKE', 'en': 'CEIL', 'es': 'TECHO', 'fr': 'PLAFOND', 'it': 'SOFFITTO', 'pt': 'TETO'
    },
    'ZUFALL': {
        'de': 'ZUFALL', 'en': 'RANDOM', 'es': 'AZAR', 'fr': 'HASARD', 'it': 'CASUALE', 'pt': 'ACASO'
    },
    'ZUFALL_BEREICH': {
        'de': 'ZUFALL_BEREICH', 'en': 'RANDOM_RANGE', 'es': 'AZAR_RANGO', 'fr': 'HASARD_PLAGE', 'it': 'CASUALE_INTERVALLO', 'pt': 'ACASO_INTERVALO'
    },

    # ─── Text ─────────────────────────────────────────────────────────
    'GROSSBUCHSTABEN': {
        'de': 'GROSSBUCHSTABEN', 'en': 'UPPERCASE', 'es': 'MAYUSCULAS', 'fr': 'MAJUSCULES', 'it': 'MAIUSCOLO', 'pt': 'MAIUSCULAS'
    },
    'KLEINBUCHSTABEN': {
        'de': 'KLEINBUCHSTABEN', 'en': 'LOWERCASE', 'es': 'MINUSCULAS', 'fr': 'MINUSCULES', 'it': 'MINUSCOLO', 'pt': 'MINUSCULAS'
    },
    'ERSETZE': {
        'de': 'ERSETZE', 'en': 'REPLACE', 'es': 'REEMPLAZAR', 'fr': 'REMPLACER', 'it': 'SOSTITUIRE', 'pt': 'SUBSTITUIR'
    },
    'TEILE': {
        'de': 'TEILE', 'en': 'SPLIT', 'es': 'DIVIDIR', 'fr': 'DIVISER', 'it': 'DIVIDERE', 'pt': 'DIVIDIR'
    },
    'TRIMME': {
        'de': 'TRIMME', 'en': 'TRIM', 'es': 'RECORTAR', 'fr': 'ROGNER', 'it': 'TAGLIARE', 'pt': 'APARAR'
    },
    'ENTHAELT': {
        'de': 'ENTHAELT', 'en': 'CONTAINS', 'es': 'CONTIENE', 'fr': 'CONTIENT', 'it': 'CONTIENE', 'pt': 'CONTEM'
    },
    'LAENGE': {
        'de': 'LAENGE', 'en': 'LENGTH', 'es': 'LONGITUD', 'fr': 'LONGUEUR', 'it': 'LUNGHEZZA', 'pt': 'COMPRIMENTO'
    },
    'FINDE': {
        'de': 'FINDE', 'en': 'FIND', 'es': 'BUSCAR', 'fr': 'CHERCHER', 'it': 'CERCARE', 'pt': 'BUSCAR'
    },
    'BEGINNT_MIT': {
        'de': 'BEGINNT_MIT', 'en': 'STARTS_WITH', 'es': 'EMPIEZA_CON', 'fr': 'COMMENCE_PAR', 'it': 'INIZIA_CON', 'pt': 'COMECA_COM'
    },
    'ENDET_MIT': {
        'de': 'ENDET_MIT', 'en': 'ENDS_WITH', 'es': 'TERMINA_CON', 'fr': 'FINIT_PAR', 'it': 'FINISCE_CON', 'pt': 'TERMINA_COM'
    },
    'VERBINDE': {
        'de': 'VERBINDE', 'en': 'JOIN', 'es': 'UNIR', 'fr': 'JOINDRE', 'it': 'UNIRE', 'pt': 'JUNTAR'
    },

    # ─── Listen ───────────────────────────────────────────────────────
    'SORTIEREN': {
        'de': 'SORTIEREN', 'en': 'SORT', 'es': 'ORDENAR', 'fr': 'TRIER', 'it': 'ORDINARE', 'pt': 'ORDENAR'
    },
    'FILTERN': {
        'de': 'FILTERN', 'en': 'FILTER', 'es': 'FILTRAR', 'fr': 'FILTRER', 'it': 'FILTRARE', 'pt': 'FILTRAR'
    },
    'UMWANDELN': {
        'de': 'UMWANDELN', 'en': 'MAP', 'es': 'MAPEAR', 'fr': 'TRANSFORMER', 'it': 'MAPPARE', 'pt': 'MAPEAR'
    },
    'UMKEHREN': {
        'de': 'UMKEHREN', 'en': 'REVERSE', 'es': 'INVERTIR', 'fr': 'INVERSER', 'it': 'INVERTIRE', 'pt': 'INVERTER'
    },
    'FLACH': {
        'de': 'FLACH', 'en': 'FLAT', 'es': 'APLANAR', 'fr': 'APLATIR', 'it': 'APPIATTIRE', 'pt': 'ACHATAR'
    },
    'EINDEUTIG': {
        'de': 'EINDEUTIG', 'en': 'UNIQUE', 'es': 'UNICO', 'fr': 'UNIQUE', 'it': 'UNICO', 'pt': 'UNICO'
    },
    'AUFZAEHLEN': {
        'de': 'AUFZAEHLEN', 'en': 'ENUMERATE', 'es': 'ENUMERAR', 'fr': 'ENUMERER', 'it': 'ENUMERARE', 'pt': 'ENUMERAR'
    },
    'KOMBINIEREN': {
        'de': 'KOMBINIEREN', 'en': 'ZIP', 'es': 'COMBINAR', 'fr': 'COMBINER', 'it': 'COMBINARE', 'pt': 'COMBINAR'
    },
    'ANHAENGEN': {
        'de': 'ANHAENGEN', 'en': 'APPEND', 'es': 'AGREGAR', 'fr': 'AJOUTER', 'it': 'AGGIUNGERE', 'pt': 'ADICIONAR'
    },

    # ─── Dateien ──────────────────────────────────────────────────────
    'LESE_DATEI': {
        'de': 'LESE_DATEI', 'en': 'READ_FILE', 'es': 'LEER_ARCHIVO', 'fr': 'LIRE_FICHIER', 'it': 'LEGGI_FILE', 'pt': 'LER_ARQUIVO'
    },
    'SCHREIBE_DATEI': {
        'de': 'SCHREIBE_DATEI', 'en': 'WRITE_FILE', 'es': 'ESCRIBIR_ARCHIVO', 'fr': 'ECRIRE_FICHIER', 'it': 'SCRIVI_FILE', 'pt': 'ESCREVER_ARQUIVO'
    },
    'ERGAENZE_DATEI': {
        'de': 'ERGAENZE_DATEI', 'en': 'APPEND_FILE', 'es': 'AGREGAR_ARCHIVO', 'fr': 'AJOUTER_FICHIER', 'it': 'AGGIUNGI_FILE', 'pt': 'ADICIONAR_ARQUIVO'
    },
    'EXISTIERT': {
        'de': 'EXISTIERT', 'en': 'EXISTS', 'es': 'EXISTE', 'fr': 'EXISTE', 'it': 'ESISTE', 'pt': 'EXISTE'
    },
    'LESE_ZEILEN': {
        'de': 'LESE_ZEILEN', 'en': 'READ_LINES', 'es': 'LEER_LINEAS', 'fr': 'LIRE_LIGNES', 'it': 'LEGGI_RIGHE', 'pt': 'LER_LINHAS'
    },
    'LOESCHE_DATEI': {
        'de': 'LOESCHE_DATEI', 'en': 'DELETE_FILE', 'es': 'BORRAR_ARCHIVO', 'fr': 'SUPPRIMER_FICHIER', 'it': 'ELIMINA_FILE', 'pt': 'APAGAR_ARQUIVO'
    },

    # ─── Spielfeld ────────────────────────────────────────────────────
    'Spielfeld': {
        'de': 'Spielfeld', 'en': 'Playground', 'es': 'Campo', 'fr': 'Terrain', 'it': 'Campo', 'pt': 'Campo'
    },

    # ─── Typ-Prüfung & Konvertierung (7.2) ───────────────────────────
    'IST_ZAHL': {
        'de': 'IST_ZAHL', 'en': 'IS_NUMBER', 'es': 'ES_NUMERO', 'fr': 'EST_NOMBRE', 'it': 'E_NUMERO', 'pt': 'E_NUMERO'
    },
    'IST_TEXT': {
        'de': 'IST_TEXT', 'en': 'IS_TEXT', 'es': 'ES_TEXTO', 'fr': 'EST_TEXTE', 'it': 'E_TESTO', 'pt': 'E_TEXTO'
    },
    'IST_LISTE': {
        'de': 'IST_LISTE', 'en': 'IS_LIST', 'es': 'ES_LISTA', 'fr': 'EST_LISTE', 'it': 'E_LISTA', 'pt': 'E_LISTA'
    },
    'IST_DICT': {
        'de': 'IST_DICT', 'en': 'IS_DICT', 'es': 'ES_DICT', 'fr': 'EST_DICT', 'it': 'E_DICT', 'pt': 'E_DICT'
    },
    'IST_BOOL': {
        'de': 'IST_BOOL', 'en': 'IS_BOOL', 'es': 'ES_BOOL', 'fr': 'EST_BOOL', 'it': 'E_BOOL', 'pt': 'E_BOOL'
    },
    'IST_NICHTS': {
        'de': 'IST_NICHTS', 'en': 'IS_NONE', 'es': 'ES_NADA', 'fr': 'EST_RIEN', 'it': 'E_NIENTE', 'pt': 'E_NADA'
    },
    'ALS_ZAHL': {
        'de': 'ALS_ZAHL', 'en': 'TO_NUMBER', 'es': 'A_NUMERO', 'fr': 'EN_NOMBRE', 'it': 'A_NUMERO', 'pt': 'PARA_NUMERO'
    },
    'ALS_TEXT': {
        'de': 'ALS_TEXT', 'en': 'TO_TEXT', 'es': 'A_TEXTO', 'fr': 'EN_TEXTE', 'it': 'A_TESTO', 'pt': 'PARA_TEXTO'
    },
}

# ─── Methoden-Übersetzungen ──────────────────────────────────────────
# Schlüssel = deutscher Methodenname
# Werte = {sprach_code: übersetzter Name}
# Alle werden auf den gleichen Python-Methodennamen gemappt.

METHODEN_TRANSLATIONS = {
    # ─── Listen-Methoden ──────────────────────────────────────────────
    'hinzufuegen': {  # → append
        'de': 'hinzufuegen', 'en': 'add', 'es': 'agregar', 'fr': 'ajouter', 'it': 'aggiungere', 'pt': 'adicionar'
    },
    'einfuegen': {  # → insert
        'de': 'einfuegen', 'en': 'insert', 'es': 'insertar', 'fr': 'inserer', 'it': 'inserire', 'pt': 'inserir'
    },
    'entfernen': {  # → remove
        'de': 'entfernen', 'en': 'remove', 'es': 'eliminar', 'fr': 'supprimer', 'it': 'rimuovere', 'pt': 'remover'
    },
    'sortieren': {  # → sort
        'de': 'sortieren', 'en': 'sort', 'es': 'ordenar', 'fr': 'trier', 'it': 'ordinare', 'pt': 'ordenar'
    },
    'umkehren': {  # → reverse
        'de': 'umkehren', 'en': 'reverse', 'es': 'invertir', 'fr': 'inverser', 'it': 'invertire', 'pt': 'inverter'
    },
    'laenge': {  # → __len__
        'de': 'laenge', 'en': 'length', 'es': 'longitud', 'fr': 'longueur', 'it': 'lunghezza', 'pt': 'comprimento'
    },
    'index': {  # → index
        'de': 'index', 'en': 'index', 'es': 'indice', 'fr': 'index', 'it': 'indice', 'pt': 'indice'
    },
    'zaehle': {  # → count
        'de': 'zaehle', 'en': 'count', 'es': 'contar', 'fr': 'compter', 'it': 'contare', 'pt': 'contar'
    },
    'leeren': {  # → clear
        'de': 'leeren', 'en': 'clear', 'es': 'limpiar', 'fr': 'vider', 'it': 'svuotare', 'pt': 'limpar'
    },
    'kopie': {  # → copy
        'de': 'kopie', 'en': 'copy', 'es': 'copia', 'fr': 'copie', 'it': 'copia', 'pt': 'copia'
    },

    # ─── String-Methoden ──────────────────────────────────────────────
    'gross': {  # → upper
        'de': 'gross', 'en': 'upper', 'es': 'mayus', 'fr': 'majus', 'it': 'maius', 'pt': 'maius'
    },
    'klein': {  # → lower
        'de': 'klein', 'en': 'lower', 'es': 'minus', 'fr': 'minus', 'it': 'minus', 'pt': 'minus'
    },
    'ersetze': {  # → replace
        'de': 'ersetze', 'en': 'replace', 'es': 'reemplazar', 'fr': 'remplacer', 'it': 'sostituire', 'pt': 'substituir'
    },
    'teile': {  # → split
        'de': 'teile', 'en': 'split', 'es': 'dividir', 'fr': 'diviser', 'it': 'dividere', 'pt': 'dividir'
    },
    'trimme': {  # → strip
        'de': 'trimme', 'en': 'trim', 'es': 'recortar', 'fr': 'rogner', 'it': 'tagliare', 'pt': 'aparar'
    },
    'beginnt_mit': {  # → startswith
        'de': 'beginnt_mit', 'en': 'starts_with', 'es': 'empieza_con', 'fr': 'commence_par', 'it': 'inizia_con', 'pt': 'comeca_com'
    },
    'endet_mit': {  # → endswith
        'de': 'endet_mit', 'en': 'ends_with', 'es': 'termina_con', 'fr': 'finit_par', 'it': 'finisce_con', 'pt': 'termina_com'
    },
    'enthaelt': {  # → __contains__
        'de': 'enthaelt', 'en': 'contains', 'es': 'contiene', 'fr': 'contient', 'it': 'contiene', 'pt': 'contem'
    },
    'finde': {  # → find
        'de': 'finde', 'en': 'find', 'es': 'buscar', 'fr': 'chercher', 'it': 'cercare', 'pt': 'buscar'
    },
}

# ─── Modul-Übersetzungen ─────────────────────────────────────────────
# ALLOWED_MODULES: deutsche Modulnamen → mehrsprachige Aliase

MODULE_TRANSLATIONS = {
    'mathe': {
        'de': 'mathe', 'en': 'math', 'es': 'mate', 'fr': 'maths', 'it': 'mate', 'pt': 'mate'
    },
    'zufall': {
        'de': 'zufall', 'en': 'random', 'es': 'azar', 'fr': 'hasard', 'it': 'casuale', 'pt': 'acaso'
    },
    'zeit': {
        'de': 'zeit', 'en': 'time', 'es': 'tiempo', 'fr': 'temps', 'it': 'tempo', 'pt': 'tempo'
    },
    'datum': {
        'de': 'datum', 'en': 'date', 'es': 'fecha', 'fr': 'date', 'it': 'data', 'pt': 'data'
    },
    'tkinter': {
        'de': 'tkinter', 'en': 'tkinter', 'es': 'tkinter', 'fr': 'tkinter', 'it': 'tkinter', 'pt': 'tkinter'
    },
}

# ─── Sprach-Code Mapping ─────────────────────────────────────────────

LANG_TO_ISO = {
    'deutsch': 'de',
    'english': 'en',
    'espaniol': 'es',
    'francais': 'fr',
    'italiano': 'it',
    'portugues': 'pt',
}


def get_builtin_aliases(sprache):
    """Gibt ein Dict zurück: {übersetzter_name: deutsche_original_name} für die Sprache.

    Deutsch ist IMMER enthalten als Fallback.
    Wenn sprache='english', enthält das Dict sowohl deutsche als auch englische Namen.
    """
    iso = LANG_TO_ISO.get(sprache, 'de')
    aliases = {}

    for de_name, translations in BUILTIN_TRANSLATIONS.items():
        # Deutscher Name ist immer verfügbar
        aliases[de_name] = de_name
        # Übersetzter Name (falls anders als Deutsch)
        translated = translations.get(iso, de_name)
        if translated != de_name:
            aliases[translated] = de_name

    return aliases


def get_methoden_map(sprache):
    """Gibt den erweiterten _METHODEN_MAP zurück — Deutsch + aktive Sprache.

    Ergebnis: {methoden_name_in_sprache: python_methode}
    """
    # Basis: Deutsche Methoden → Python
    _PYTHON_MAP = {
        'hinzufuegen': 'append',
        'einfuegen': 'insert',
        'entfernen': 'remove',
        'sortieren': 'sort',
        'umkehren': 'reverse',
        'laenge': '__len__',
        'index': 'index',
        'zaehle': 'count',
        'leeren': 'clear',
        'kopie': 'copy',
        'gross': 'upper',
        'klein': 'lower',
        'ersetze': 'replace',
        'teile': 'split',
        'trimme': 'strip',
        'beginnt_mit': 'startswith',
        'endet_mit': 'endswith',
        'enthaelt': '__contains__',
        'finde': 'find',
    }

    iso = LANG_TO_ISO.get(sprache, 'de')
    result = {}

    for de_name, python_method in _PYTHON_MAP.items():
        # Deutscher Name immer verfügbar
        result[de_name] = python_method
        # Übersetzter Name hinzufügen
        translations = METHODEN_TRANSLATIONS.get(de_name, {})
        translated = translations.get(iso, de_name)
        if translated != de_name:
            result[translated] = python_method

    return result


def get_module_aliases(sprache):
    """Gibt ein Dict zurück: {übersetzter_modulname: python_modul_objekt_key}

    Der Wert ist der deutsche Originalname (Schlüssel in ALLOWED_MODULES).
    """
    iso = LANG_TO_ISO.get(sprache, 'de')
    aliases = {}

    for de_name, translations in MODULE_TRANSLATIONS.items():
        # Deutscher Name immer verfügbar
        aliases[de_name] = de_name
        # Übersetzter Name
        translated = translations.get(iso, de_name)
        if translated != de_name:
            aliases[translated] = de_name

    return aliases
