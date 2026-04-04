# FILE: lexer.py (Version ZUSE 7.3)
import re
from error_i18n import t

# Keyword-Aliase: Alias-Key → kanonischer Key
# Aliase werden im Lexer auf den kanonischen Key normalisiert,
# sodass der Parser unverändert bleibt.
KEYWORD_ALIASES = {
    # DE: ZEIGE → AUSGABE (Verb statt Substantiv)
    'KW_ZEIGE': 'KW_AUSGABE',
    # DE: LADE → BENUTZE (logischer: man lädt ein Modul)
    'KW_LADE': 'KW_BENUTZE',
    # DE: ERGEBNIS (Kurzform) → ERGEBNIS IST
    'KW_ERGEBNIS_KURZ': 'KW_ERGEBNIS',
    # DE: OBER → ELTERN (Singular statt Plural)
    'KW_OBER': 'KW_ELTERN',
    # Großschreib-Aliase: WAHR/FALSCH → wahr/falsch
    'CONST_WAHR_GROSS': 'CONST_WAHR',
    'CONST_FALSCH_GROSS': 'CONST_FALSCH',
}

STATIC_TOKENS = [
    ('STRING',     r'"(?:[^"\\]|\\.)*"'),
    ('ZAHL',       r'\d+\.\d+|\.\d+|\d+'), 
    ('NAME',       r'[A-Za-z_\u00C0-\u024F\u0900-\u097F\u4E00-\u9FFF\u3400-\u4DBF\uF900-\uFAFF][A-Za-z0-9_\u00C0-\u024F\u0900-\u097F\u4E00-\u9FFF\u3400-\u4DBF\uF900-\uFAFF]*'),
    ('OPERATOR',   r'==|!=|<=|>=|[+\-*/=<>\^%]'),
    ('KLAMMER_AUF',r'\('),
    ('KLAMMER_ZU', r'\)'),
    ('KLAMMER_AUF_ECKIG', r'\['),
    ('KLAMMER_ZU_ECKIG',  r'\]'),
    ('GESCHWEIFT_AUF',    r'\{'),
    ('GESCHWEIFT_ZU',     r'\}'),
    ('KOMMA',      r','),
    ('PUNKT',      r'\.'),
    ('DOPPELPUNKT', r':'),
    ('NEUEZEILE',  r'\n'),
    ('LEERZEICHEN',r'[ \t]+'),
    ('KOMMENTAR',  r'#.*'),
    ('UNBEKANNT',  r'.'),
]

class Lexer:
    def __init__(self, sprach_config):
        self.sprach_config = sprach_config
        self.token_regex = self._baue_regex()

    def _baue_regex(self):
        keywords = []
        # Unicode-kompatible Word-Boundary (funktioniert mit Devanagari, CJK etc.)
        _WB_LEFT = r'(?<![A-Za-z0-9_\u00C0-\u024F\u0900-\u097F\u0901-\u0963\u0966-\u096F\u4E00-\u9FFF\u3400-\u4DBF\uF900-\uFAFF])'
        _WB_RIGHT = r'(?![A-Za-z0-9_\u00C0-\u024F\u0900-\u097F\u0901-\u0963\u0966-\u096F\u4E00-\u9FFF\u3400-\u4DBF\uF900-\uFAFF])'
        for key, value in self.sprach_config.items():
            escaped = re.escape(value)
            pattern_str = escaped.replace(r'\ ', r'\s+')
            pattern = rf'{_WB_LEFT}{pattern_str}{_WB_RIGHT}'
            keywords.append((key, pattern))
        
        keywords.sort(key=lambda x: len(x[1]), reverse=True)
        alle_regeln = keywords + STATIC_TOKENS
        regex_parts = [f'(?P<{name}>{pattern})' for name, pattern in alle_regeln]
        return re.compile('|'.join(regex_parts))

    def tokenize(self, code, start_line=1): # <--- WICHTIG: Hier muss start_line stehen
        tokens = []
        line_num = start_line 
        
        for mo in self.token_regex.finditer(code):
            kind = mo.lastgroup
            value = mo.group()
            start_pos = mo.start()
            end_pos = mo.end()

            if kind == 'NEUEZEILE':
                tokens.append({'type': kind, 'value': value, 'line': line_num, 'start': start_pos, 'end': end_pos})
                line_num += 1
                continue
            elif kind in ['LEERZEICHEN', 'KOMMENTAR']:
                if kind == 'KOMMENTAR':
                     tokens.append({'type': kind, 'value': value, 'line': line_num, 'start': start_pos, 'end': end_pos})
                continue
            elif kind == 'UNBEKANNT':
                # Spaltenposition berechnen
                line_start = code.rfind('\n', 0, start_pos) + 1
                col = start_pos - line_start + 1
                raise RuntimeError(t("ERR_LEXER_UNKNOWN_CHAR", line=line_num, char=value) + f" (Spalte {col})")
            
            if kind.startswith('KW_') or kind.startswith('CONST_') or kind.startswith('FUNC_'):
                canonical = KEYWORD_ALIASES.get(kind, kind)
                tokens.append({
                    'type': 'KEYWORD',
                    'value': canonical,
                    'original': value,
                    'line': line_num,
                    'start': start_pos,
                    'end': end_pos
                })
            else:
                tokens.append({'type': kind, 'value': value, 'line': line_num, 'start': start_pos, 'end': end_pos})
                
        tokens.append({'type': 'EOF', 'line': line_num, 'value': '', 'start': len(code), 'end': len(code)})
        return tokens

# WICHTIG: Auch die Wrapper-Funktion muss das neue Argument annehmen
def tokenize(code, config, start_line=1):
    return Lexer(config).tokenize(code, start_line)