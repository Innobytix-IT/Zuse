# FILE: builtin_i18n.py — Mehrsprachige Builtin-Übersetzungen für ZUSE 7.3
#
# Jede Builtin-Funktion hat einen kanonischen (deutschen) Namen.
# Diese Tabelle mappt den deutschen Namen auf Übersetzungen in allen Sprachen.
# Deutsch ist IMMER als Fallback verfügbar.
# Unterstützte Sprachen: de, en, es, fr, it, pt, hi (Hindi), zh (中文)

# ─── Builtin-Funktionen ──────────────────────────────────────────────
# Schlüssel = deutscher Originalname
# Werte = {sprach_code: übersetzter Name}

BUILTIN_TRANSLATIONS = {
    # ─── Typ-Konvertierung & Utilities ────────────────────────────────
    'str': {
        'de': 'str', 'en': 'str', 'es': 'str', 'fr': 'str', 'it': 'str', 'pt': 'str', 'hi': 'str', 'zh': 'str'
    },
    'int': {
        'de': 'int', 'en': 'int', 'es': 'int', 'fr': 'int', 'it': 'int', 'pt': 'int', 'hi': 'int', 'zh': 'int'
    },
    'float': {
        'de': 'float', 'en': 'float', 'es': 'float', 'fr': 'float', 'it': 'float', 'pt': 'float', 'hi': 'float', 'zh': 'float'
    },
    'len': {
        'de': 'len', 'en': 'len', 'es': 'len', 'fr': 'len', 'it': 'len', 'pt': 'len', 'hi': 'len', 'zh': 'len'
    },
    'typ': {
        'de': 'typ', 'en': 'type', 'es': 'tipo', 'fr': 'type', 'it': 'tipo', 'pt': 'tipo', 'hi': 'प्रकार', 'zh': '类型'
    },
    'liste': {
        'de': 'liste', 'en': 'list', 'es': 'lista', 'fr': 'liste', 'it': 'lista', 'pt': 'lista', 'hi': 'सूची', 'zh': '列表'
    },
    'dict': {
        'de': 'dict', 'en': 'dict', 'es': 'dict', 'fr': 'dict', 'it': 'dict', 'pt': 'dict', 'hi': 'dict', 'zh': 'dict'
    },

    # ─── Bereich ──────────────────────────────────────────────────────
    'BEREICH': {
        'de': 'BEREICH', 'en': 'RANGE', 'es': 'RANGO', 'fr': 'PLAGE', 'it': 'INTERVALLO', 'pt': 'INTERVALO', 'hi': 'श्रेणी', 'zh': '范围'
    },
    'BEREICH_LISTE': {
        'de': 'BEREICH_LISTE', 'en': 'RANGE_LIST', 'es': 'LISTA_RANGO', 'fr': 'LISTE_PLAGE', 'it': 'LISTA_INTERVALLO', 'pt': 'LISTA_INTERVALO', 'hi': 'श्रेणी_सूची', 'zh': '范围_列表'
    },
    'FORMAT': {
        'de': 'FORMAT', 'en': 'FORMAT', 'es': 'FORMATO', 'fr': 'FORMAT', 'it': 'FORMATO', 'pt': 'FORMATO', 'hi': 'प्रारूप', 'zh': '格式'
    },

    # ─── Mathe ────────────────────────────────────────────────────────
    'PI': {
        'de': 'PI', 'en': 'PI', 'es': 'PI', 'fr': 'PI', 'it': 'PI', 'pt': 'PI', 'hi': 'PI', 'zh': 'PI'
    },
    'E': {
        'de': 'E', 'en': 'E', 'es': 'E', 'fr': 'E', 'it': 'E', 'pt': 'E', 'hi': 'E', 'zh': 'E'
    },
    'WURZEL': {
        'de': 'WURZEL', 'en': 'SQRT', 'es': 'RAIZ', 'fr': 'RACINE', 'it': 'RADICE', 'pt': 'RAIZ', 'hi': 'वर्गमूल', 'zh': '平方根'
    },
    'SINUS': {
        'de': 'SINUS', 'en': 'SIN', 'es': 'SENO', 'fr': 'SINUS', 'it': 'SENO', 'pt': 'SENO', 'hi': 'ज्या', 'zh': '正弦'
    },
    'COSINUS': {
        'de': 'COSINUS', 'en': 'COS', 'es': 'COSENO', 'fr': 'COSINUS', 'it': 'COSENO', 'pt': 'COSENO', 'hi': 'कोज्या', 'zh': '余弦'
    },
    'TANGENS': {
        'de': 'TANGENS', 'en': 'TAN', 'es': 'TANGENTE', 'fr': 'TANGENTE', 'it': 'TANGENTE', 'pt': 'TANGENTE', 'hi': 'स्पर्शज्या', 'zh': '正切'
    },
    'RUNDEN': {
        'de': 'RUNDEN', 'en': 'ROUND', 'es': 'REDONDEAR', 'fr': 'ARRONDIR', 'it': 'ARROTONDARE', 'pt': 'ARREDONDAR', 'hi': 'गोल', 'zh': '四舍五入'
    },
    'ABSOLUT': {
        'de': 'ABSOLUT', 'en': 'ABS', 'es': 'ABSOLUTO', 'fr': 'ABSOLU', 'it': 'ASSOLUTO', 'pt': 'ABSOLUTO', 'hi': 'निरपेक्ष', 'zh': '绝对值'
    },
    'POTENZ': {
        'de': 'POTENZ', 'en': 'POWER', 'es': 'POTENCIA', 'fr': 'PUISSANCE', 'it': 'POTENZA', 'pt': 'POTENCIA', 'hi': 'घात', 'zh': '幂'
    },
    'LOGARITHMUS': {
        'de': 'LOGARITHMUS', 'en': 'LOG', 'es': 'LOGARITMO', 'fr': 'LOGARITHME', 'it': 'LOGARITMO', 'pt': 'LOGARITMO', 'hi': 'लघुगणक', 'zh': '对数'
    },
    'MINIMUM': {
        'de': 'MINIMUM', 'en': 'MIN', 'es': 'MINIMO', 'fr': 'MINIMUM', 'it': 'MINIMO', 'pt': 'MINIMO', 'hi': 'न्यूनतम', 'zh': '最小值'
    },
    'MAXIMUM': {
        'de': 'MAXIMUM', 'en': 'MAX', 'es': 'MAXIMO', 'fr': 'MAXIMUM', 'it': 'MASSIMO', 'pt': 'MAXIMO', 'hi': 'अधिकतम', 'zh': '最大值'
    },
    'SUMME': {
        'de': 'SUMME', 'en': 'SUM', 'es': 'SUMA', 'fr': 'SOMME', 'it': 'SOMMA', 'pt': 'SOMA', 'hi': 'योग', 'zh': '求和'
    },
    'BODEN': {
        'de': 'BODEN', 'en': 'FLOOR', 'es': 'PISO', 'fr': 'PLANCHER', 'it': 'PAVIMENTO', 'pt': 'PISO', 'hi': 'तल', 'zh': '下取整'
    },
    'DECKE': {
        'de': 'DECKE', 'en': 'CEIL', 'es': 'TECHO', 'fr': 'PLAFOND', 'it': 'SOFFITTO', 'pt': 'TETO', 'hi': 'छत', 'zh': '上取整'
    },
    'ZUFALL': {
        'de': 'ZUFALL', 'en': 'RANDOM', 'es': 'AZAR', 'fr': 'HASARD', 'it': 'CASUALE', 'pt': 'ACASO', 'hi': 'यादृच्छिक', 'zh': '随机'
    },
    'ZUFALL_BEREICH': {
        'de': 'ZUFALL_BEREICH', 'en': 'RANDOM_RANGE', 'es': 'AZAR_RANGO', 'fr': 'HASARD_PLAGE', 'it': 'CASUALE_INTERVALLO', 'pt': 'ACASO_INTERVALO', 'hi': 'यादृच्छिक_श्रेणी', 'zh': '随机_范围'
    },

    # ─── Text ─────────────────────────────────────────────────────────
    'GROSSBUCHSTABEN': {
        'de': 'GROSSBUCHSTABEN', 'en': 'UPPERCASE', 'es': 'MAYUSCULAS', 'fr': 'MAJUSCULES', 'it': 'MAIUSCOLO', 'pt': 'MAIUSCULAS', 'hi': 'बड़े_अक्षर', 'zh': '大写'
    },
    'KLEINBUCHSTABEN': {
        'de': 'KLEINBUCHSTABEN', 'en': 'LOWERCASE', 'es': 'MINUSCULAS', 'fr': 'MINUSCULES', 'it': 'MINUSCOLO', 'pt': 'MINUSCULAS', 'hi': 'छोटे_अक्षर', 'zh': '小写'
    },
    'ERSETZE': {
        'de': 'ERSETZE', 'en': 'REPLACE', 'es': 'REEMPLAZAR', 'fr': 'REMPLACER', 'it': 'SOSTITUIRE', 'pt': 'SUBSTITUIR', 'hi': 'बदलो', 'zh': '替换'
    },
    'TEILE': {
        'de': 'TEILE', 'en': 'SPLIT', 'es': 'DIVIDIR', 'fr': 'DIVISER', 'it': 'DIVIDERE', 'pt': 'DIVIDIR', 'hi': 'विभाजित', 'zh': '分割'
    },
    'TRIMME': {
        'de': 'TRIMME', 'en': 'TRIM', 'es': 'RECORTAR', 'fr': 'ROGNER', 'it': 'TAGLIARE', 'pt': 'APARAR', 'hi': 'छाँटो', 'zh': '修剪'
    },
    'ENTHAELT': {
        'de': 'ENTHAELT', 'en': 'CONTAINS', 'es': 'CONTIENE', 'fr': 'CONTIENT', 'it': 'CONTIENE', 'pt': 'CONTEM', 'hi': 'शामिल_है', 'zh': '包含'
    },
    'LAENGE': {
        'de': 'LAENGE', 'en': 'LENGTH', 'es': 'LONGITUD', 'fr': 'LONGUEUR', 'it': 'LUNGHEZZA', 'pt': 'COMPRIMENTO', 'hi': 'लंबाई', 'zh': '长度'
    },
    'FINDE': {
        'de': 'FINDE', 'en': 'FIND', 'es': 'BUSCAR', 'fr': 'CHERCHER', 'it': 'CERCARE', 'pt': 'BUSCAR', 'hi': 'खोजो', 'zh': '查找'
    },
    'BEGINNT_MIT': {
        'de': 'BEGINNT_MIT', 'en': 'STARTS_WITH', 'es': 'EMPIEZA_CON', 'fr': 'COMMENCE_PAR', 'it': 'INIZIA_CON', 'pt': 'COMECA_COM', 'hi': 'शुरू_होता', 'zh': '开头是'
    },
    'ENDET_MIT': {
        'de': 'ENDET_MIT', 'en': 'ENDS_WITH', 'es': 'TERMINA_CON', 'fr': 'FINIT_PAR', 'it': 'FINISCE_CON', 'pt': 'TERMINA_COM', 'hi': 'अंत_होता', 'zh': '结尾是'
    },
    'VERBINDE': {
        'de': 'VERBINDE', 'en': 'JOIN', 'es': 'UNIR', 'fr': 'JOINDRE', 'it': 'UNIRE', 'pt': 'JUNTAR', 'hi': 'जोड़ो', 'zh': '连接'
    },

    # ─── Listen ───────────────────────────────────────────────────────
    'SORTIEREN': {
        'de': 'SORTIEREN', 'en': 'SORT', 'es': 'ORDENAR', 'fr': 'TRIER', 'it': 'ORDINARE', 'pt': 'ORDENAR', 'hi': 'क्रमबद्ध', 'zh': '排序'
    },
    'FILTERN': {
        'de': 'FILTERN', 'en': 'FILTER', 'es': 'FILTRAR', 'fr': 'FILTRER', 'it': 'FILTRARE', 'pt': 'FILTRAR', 'hi': 'छानो', 'zh': '过滤'
    },
    'UMWANDELN': {
        'de': 'UMWANDELN', 'en': 'MAP', 'es': 'MAPEAR', 'fr': 'TRANSFORMER', 'it': 'MAPPARE', 'pt': 'MAPEAR', 'hi': 'बदलो_सब', 'zh': '映射'
    },
    'UMKEHREN': {
        'de': 'UMKEHREN', 'en': 'REVERSE', 'es': 'INVERTIR', 'fr': 'INVERSER', 'it': 'INVERTIRE', 'pt': 'INVERTER', 'hi': 'उलटाओ', 'zh': '反转'
    },
    'FLACH': {
        'de': 'FLACH', 'en': 'FLAT', 'es': 'APLANAR', 'fr': 'APLATIR', 'it': 'APPIATTIRE', 'pt': 'ACHATAR', 'hi': 'समतल', 'zh': '展平'
    },
    'EINDEUTIG': {
        'de': 'EINDEUTIG', 'en': 'UNIQUE', 'es': 'UNICO', 'fr': 'UNIQUE', 'it': 'UNICO', 'pt': 'UNICO', 'hi': 'अद्वितीय', 'zh': '唯一'
    },
    'AUFZAEHLEN': {
        'de': 'AUFZAEHLEN', 'en': 'ENUMERATE', 'es': 'ENUMERAR', 'fr': 'ENUMERER', 'it': 'ENUMERARE', 'pt': 'ENUMERAR', 'hi': 'गिनती', 'zh': '枚举'
    },
    'KOMBINIEREN': {
        'de': 'KOMBINIEREN', 'en': 'ZIP', 'es': 'COMBINAR', 'fr': 'COMBINER', 'it': 'COMBINARE', 'pt': 'COMBINAR', 'hi': 'मिलाओ', 'zh': '组合'
    },
    'ANHAENGEN': {
        'de': 'ANHAENGEN', 'en': 'APPEND', 'es': 'AGREGAR', 'fr': 'AJOUTER', 'it': 'AGGIUNGERE', 'pt': 'ADICIONAR', 'hi': 'जोड़ो_अंत', 'zh': '追加'
    },

    # ─── Dateien ──────────────────────────────────────────────────────
    'LESE_DATEI': {
        'de': 'LESE_DATEI', 'en': 'READ_FILE', 'es': 'LEER_ARCHIVO', 'fr': 'LIRE_FICHIER', 'it': 'LEGGI_FILE', 'pt': 'LER_ARQUIVO', 'hi': 'पढ़ो_फ़ाइल', 'zh': '读取_文件'
    },
    'SCHREIBE_DATEI': {
        'de': 'SCHREIBE_DATEI', 'en': 'WRITE_FILE', 'es': 'ESCRIBIR_ARCHIVO', 'fr': 'ECRIRE_FICHIER', 'it': 'SCRIVI_FILE', 'pt': 'ESCREVER_ARQUIVO', 'hi': 'लिखो_फ़ाइल', 'zh': '写入_文件'
    },
    'ERGAENZE_DATEI': {
        'de': 'ERGAENZE_DATEI', 'en': 'APPEND_FILE', 'es': 'AGREGAR_ARCHIVO', 'fr': 'AJOUTER_FICHIER', 'it': 'AGGIUNGI_FILE', 'pt': 'ADICIONAR_ARQUIVO', 'hi': 'जोड़ो_फ़ाइल', 'zh': '追加_文件'
    },
    'EXISTIERT': {
        'de': 'EXISTIERT', 'en': 'EXISTS', 'es': 'EXISTE', 'fr': 'EXISTE', 'it': 'ESISTE', 'pt': 'EXISTE', 'hi': 'मौजूद_है', 'zh': '存在'
    },
    'LESE_ZEILEN': {
        'de': 'LESE_ZEILEN', 'en': 'READ_LINES', 'es': 'LEER_LINEAS', 'fr': 'LIRE_LIGNES', 'it': 'LEGGI_RIGHE', 'pt': 'LER_LINHAS', 'hi': 'पढ़ो_पंक्तियाँ', 'zh': '读取_行'
    },
    'LOESCHE_DATEI': {
        'de': 'LOESCHE_DATEI', 'en': 'DELETE_FILE', 'es': 'BORRAR_ARCHIVO', 'fr': 'SUPPRIMER_FICHIER', 'it': 'ELIMINA_FILE', 'pt': 'APAGAR_ARQUIVO', 'hi': 'हटाओ_फ़ाइल', 'zh': '删除_文件'
    },

    # ─── Spielfeld ────────────────────────────────────────────────────
    'Spielfeld': {
        'de': 'Spielfeld', 'en': 'Playground', 'es': 'Campo', 'fr': 'Terrain', 'it': 'Campo', 'pt': 'Campo', 'hi': 'खेल_मैदान', 'zh': '游戏场'
    },

    # ─── Typ-Prüfung & Konvertierung (7.2+) ──────────────────────────
    'IST_ZAHL': {
        'de': 'IST_ZAHL', 'en': 'IS_NUMBER', 'es': 'ES_NUMERO', 'fr': 'EST_NOMBRE', 'it': 'E_NUMERO', 'pt': 'E_NUMERO', 'hi': 'है_संख्या', 'zh': '是_数字'
    },
    'IST_TEXT': {
        'de': 'IST_TEXT', 'en': 'IS_TEXT', 'es': 'ES_TEXTO', 'fr': 'EST_TEXTE', 'it': 'E_TESTO', 'pt': 'E_TEXTO', 'hi': 'है_पाठ', 'zh': '是_文字'
    },
    'IST_LISTE': {
        'de': 'IST_LISTE', 'en': 'IS_LIST', 'es': 'ES_LISTA', 'fr': 'EST_LISTE', 'it': 'E_LISTA', 'pt': 'E_LISTA', 'hi': 'है_सूची', 'zh': '是_列表'
    },
    'IST_DICT': {
        'de': 'IST_DICT', 'en': 'IS_DICT', 'es': 'ES_DICT', 'fr': 'EST_DICT', 'it': 'E_DICT', 'pt': 'E_DICT', 'hi': 'है_शब्दकोश', 'zh': '是_字典'
    },
    'IST_BOOL': {
        'de': 'IST_BOOL', 'en': 'IS_BOOL', 'es': 'ES_BOOL', 'fr': 'EST_BOOL', 'it': 'E_BOOL', 'pt': 'E_BOOL', 'hi': 'है_बूल', 'zh': '是_布尔'
    },
    'IST_NICHTS': {
        'de': 'IST_NICHTS', 'en': 'IS_NONE', 'es': 'ES_NADA', 'fr': 'EST_RIEN', 'it': 'E_NIENTE', 'pt': 'E_NADA', 'hi': 'है_कुछनहीं', 'zh': '是_空'
    },
    'ALS_ZAHL': {
        'de': 'ALS_ZAHL', 'en': 'TO_NUMBER', 'es': 'A_NUMERO', 'fr': 'EN_NOMBRE', 'it': 'A_NUMERO', 'pt': 'PARA_NUMERO', 'hi': 'संख्या_में', 'zh': '转为_数字'
    },
    'ALS_TEXT': {
        'de': 'ALS_TEXT', 'en': 'TO_TEXT', 'es': 'A_TEXTO', 'fr': 'EN_TEXTE', 'it': 'A_TESTO', 'pt': 'PARA_TEXTO', 'hi': 'पाठ_में', 'zh': '转为_文字'
    },
}

# ─── Methoden-Übersetzungen ──────────────────────────────────────────
# Schlüssel = deutscher Methodenname
# Werte = {sprach_code: übersetzter Name}
# Alle werden auf den gleichen Python-Methodennamen gemappt.

METHODEN_TRANSLATIONS = {
    # ─── Listen-Methoden ──────────────────────────────────────────────
    'hinzufuegen': {  # → append
        'de': 'hinzufuegen', 'en': 'add', 'es': 'agregar', 'fr': 'ajouter', 'it': 'aggiungere', 'pt': 'adicionar', 'hi': 'जोड़ो', 'zh': '添加'
    },
    'einfuegen': {  # → insert
        'de': 'einfuegen', 'en': 'insert', 'es': 'insertar', 'fr': 'inserer', 'it': 'inserire', 'pt': 'inserir', 'hi': 'डालो', 'zh': '插入'
    },
    'entfernen': {  # → remove
        'de': 'entfernen', 'en': 'remove', 'es': 'eliminar', 'fr': 'supprimer', 'it': 'rimuovere', 'pt': 'remover', 'hi': 'हटाओ', 'zh': '移除'
    },
    'sortieren': {  # → sort
        'de': 'sortieren', 'en': 'sort', 'es': 'ordenar', 'fr': 'trier', 'it': 'ordinare', 'pt': 'ordenar', 'hi': 'क्रमबद्ध', 'zh': '排序'
    },
    'umkehren': {  # → reverse
        'de': 'umkehren', 'en': 'reverse', 'es': 'invertir', 'fr': 'inverser', 'it': 'invertire', 'pt': 'inverter', 'hi': 'उलटाओ', 'zh': '反转'
    },
    'laenge': {  # → __len__
        'de': 'laenge', 'en': 'length', 'es': 'longitud', 'fr': 'longueur', 'it': 'lunghezza', 'pt': 'comprimento', 'hi': 'लंबाई', 'zh': '长度'
    },
    'index': {  # → index
        'de': 'index', 'en': 'index', 'es': 'indice', 'fr': 'index', 'it': 'indice', 'pt': 'indice', 'hi': 'स्थान', 'zh': '索引'
    },
    'zaehle': {  # → count
        'de': 'zaehle', 'en': 'count', 'es': 'contar', 'fr': 'compter', 'it': 'contare', 'pt': 'contar', 'hi': 'गिनो', 'zh': '计数'
    },
    'leeren': {  # → clear
        'de': 'leeren', 'en': 'clear', 'es': 'limpiar', 'fr': 'vider', 'it': 'svuotare', 'pt': 'limpar', 'hi': 'खाली_करो', 'zh': '清空'
    },
    'kopie': {  # → copy
        'de': 'kopie', 'en': 'copy', 'es': 'copia', 'fr': 'copie', 'it': 'copia', 'pt': 'copia', 'hi': 'प्रतिलिपि', 'zh': '复制'
    },

    # ─── String-Methoden ──────────────────────────────────────────────
    'gross': {  # → upper
        'de': 'gross', 'en': 'upper', 'es': 'mayus', 'fr': 'majus', 'it': 'maius', 'pt': 'maius', 'hi': 'बड़ा', 'zh': '大写'
    },
    'klein': {  # → lower
        'de': 'klein', 'en': 'lower', 'es': 'minus', 'fr': 'minus', 'it': 'minus', 'pt': 'minus', 'hi': 'छोटा', 'zh': '小写'
    },
    'ersetze': {  # → replace
        'de': 'ersetze', 'en': 'replace', 'es': 'reemplazar', 'fr': 'remplacer', 'it': 'sostituire', 'pt': 'substituir', 'hi': 'बदलो', 'zh': '替换'
    },
    'teile': {  # → split
        'de': 'teile', 'en': 'split', 'es': 'dividir', 'fr': 'diviser', 'it': 'dividere', 'pt': 'dividir', 'hi': 'विभाजित', 'zh': '分割'
    },
    'trimme': {  # → strip
        'de': 'trimme', 'en': 'trim', 'es': 'recortar', 'fr': 'rogner', 'it': 'tagliare', 'pt': 'aparar', 'hi': 'छाँटो', 'zh': '修剪'
    },
    'beginnt_mit': {  # → startswith
        'de': 'beginnt_mit', 'en': 'starts_with', 'es': 'empieza_con', 'fr': 'commence_par', 'it': 'inizia_con', 'pt': 'comeca_com', 'hi': 'शुरू_होता', 'zh': '开头是'
    },
    'endet_mit': {  # → endswith
        'de': 'endet_mit', 'en': 'ends_with', 'es': 'termina_con', 'fr': 'finit_par', 'it': 'finisce_con', 'pt': 'termina_com', 'hi': 'अंत_होता', 'zh': '结尾是'
    },
    'enthaelt': {  # → __contains__
        'de': 'enthaelt', 'en': 'contains', 'es': 'contiene', 'fr': 'contient', 'it': 'contiene', 'pt': 'contem', 'hi': 'शामिल_है', 'zh': '包含'
    },
    'finde': {  # → find
        'de': 'finde', 'en': 'find', 'es': 'buscar', 'fr': 'chercher', 'it': 'cercare', 'pt': 'buscar', 'hi': 'खोजो', 'zh': '查找'
    },
}

# ─── Modul-Übersetzungen ─────────────────────────────────────────────
# ALLOWED_MODULES: deutsche Modulnamen → mehrsprachige Aliase

MODULE_TRANSLATIONS = {
    'mathe': {
        'de': 'mathe', 'en': 'math', 'es': 'mate', 'fr': 'maths', 'it': 'mate', 'pt': 'mate', 'hi': 'गणित', 'zh': '数学'
    },
    'zufall': {
        'de': 'zufall', 'en': 'random', 'es': 'azar', 'fr': 'hasard', 'it': 'casuale', 'pt': 'acaso', 'hi': 'भाग्य', 'zh': '随机'
    },
    'zeit': {
        'de': 'zeit', 'en': 'time', 'es': 'tiempo', 'fr': 'temps', 'it': 'tempo', 'pt': 'tempo', 'hi': 'समय', 'zh': '时间'
    },
    'datum': {
        'de': 'datum', 'en': 'date', 'es': 'fecha', 'fr': 'date', 'it': 'data', 'pt': 'data', 'hi': 'तारीख', 'zh': '日期'
    },
    'tkinter': {
        'de': 'tkinter', 'en': 'tkinter', 'es': 'tkinter', 'fr': 'tkinter', 'it': 'tkinter', 'pt': 'tkinter', 'hi': 'tkinter', 'zh': 'tkinter'
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
    'hindi': 'hi',
    'zhongwen': 'zh',
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
