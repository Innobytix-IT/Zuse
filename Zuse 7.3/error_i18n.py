# FILE: error_i18n.py
# Zentrales i18n-Modul fuer Zuse-Fehlermeldungen
# Haelt die aktuelle Sprache und bietet t()-Funktion fuer Uebersetzungen

from error_messages import MESSAGES

# Mapping: Sprach-Dateiname -> ISO-Code
LANG_MAP = {
    "deutsch":   "de",
    "english":   "en",
    "espaniol":  "es",
    "francais":  "fr",
    "italiano":  "it",
    "portugues": "pt",
    "hindi":     "hi",
    "zhongwen":  "zh",
}

# Reverse-Mapping: ISO-Code -> Sprach-Dateiname
LANG_MAP_REVERSE = {v: k for k, v in LANG_MAP.items()}

# Modul-Level State (Default: Deutsch)
_current_lang = "de"
_current_lang_name = "deutsch"


def set_language(lang_name):
    """Setzt die aktuelle Fehler-Sprache.

    Args:
        lang_name: Sprach-Dateiname wie 'deutsch', 'english', etc.
                   Akzeptiert auch ISO-Codes wie 'de', 'en', etc.
    """
    global _current_lang, _current_lang_name
    if lang_name in LANG_MAP:
        _current_lang = LANG_MAP[lang_name]
        _current_lang_name = lang_name
    elif lang_name in LANG_MAP_REVERSE:
        _current_lang = lang_name
        _current_lang_name = LANG_MAP_REVERSE[lang_name]
    # Unbekannte Sprache -> bleibt bei aktuellem Wert


def get_language():
    """Gibt den aktuellen ISO-Code zurueck (z.B. 'de', 'en')."""
    return _current_lang


def get_language_name():
    """Gibt den aktuellen Sprach-Dateinamen zurueck (z.B. 'deutsch', 'english')."""
    return _current_lang_name


def t(key, **kwargs):
    """Uebersetzt einen Fehler-Schluessel in die aktuelle Sprache.

    Args:
        key: Fehler-Schluessel wie 'ERR_VAR_NOT_DEFINED'
        **kwargs: Platzhalter-Werte wie line=5, name='x'

    Returns:
        Uebersetzte Fehlermeldung als String.
        Fallback: Deutsch, dann der rohe Schluessel.
    """
    msg_dict = MESSAGES.get(key)
    if not msg_dict:
        # Schluessel nicht im Katalog -> Schluessel selbst zurueckgeben
        return key

    # Versuche aktuelle Sprache, dann Deutsch als Fallback
    template = msg_dict.get(_current_lang) or msg_dict.get("de", key)

    try:
        return template.format(**kwargs)
    except (KeyError, IndexError) as e:
        # Fehlende Platzhalter: Template mit verfügbaren Werten füllen, Rest als {name} belassen
        import string
        try:
            formatter = string.Formatter()
            result = []
            for literal, field_name, spec, conv in formatter.parse(template):
                result.append(literal)
                if field_name is not None:
                    if field_name in kwargs:
                        result.append(str(kwargs[field_name]))
                    else:
                        result.append(f"<?{field_name}>")
            return "".join(result)
        except Exception:
            return template
