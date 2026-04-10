# FILE: parser.py (Version ZUSE 4.9 SMART LOOPS)
from error_i18n import t as _t

class Parser:
    def __init__(self, tokens):
        self.tokens = [t for t in tokens if t['type'] != 'KOMMENTAR']
        self.pos = 0

    def aktuelles_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else {'type': 'EOF'}

    def aktuelle_zeile(self):
        """Gibt die Zeilennummer des aktuellen Tokens zurueck."""
        return self.aktuelles_token().get('line', 0)

    def gehe_weiter(self):
        self.pos += 1

    def peek_token(self, offset=1):
        idx = self.pos + offset
        return self.tokens[idx] if idx < len(self.tokens) else {'type': 'EOF'}

    def erwarte(self, typ, value=None):
        tok = self.aktuelles_token()
        if tok['type'] != typ:
            raise RuntimeError(_t("ERR_SYNTAX_EXPECTED_TYPE", line=tok.get('line','?'), expected=typ, found=tok['type'], value=tok.get('value')))
        if value and tok.get('value') != value:
            if typ == 'KEYWORD' and tok.get('value') == value: pass
            else: raise RuntimeError(_t("ERR_SYNTAX_EXPECTED_VALUE", line=tok.get('line','?'), expected=value, found=tok.get('value')))
        self.gehe_weiter()
        return tok

    def ist_kw(self, canonical_key):
        t = self.aktuelles_token()
        return t['type'] == 'KEYWORD' and t['value'] == canonical_key

    def parse(self):
        anweisungen = []
        fehler = []
        while self.aktuelles_token()['type'] != 'EOF':
            if self.aktuelles_token()['type'] == 'NEUEZEILE':
                self.gehe_weiter(); continue
            try:
                anweisungen.append(self.parse_anweisung())
            except RuntimeError as e:
                fehler.append(str(e))
                # Zur nächsten Zeile springen (Error-Recovery)
                while (self.aktuelles_token()['type'] not in ('NEUEZEILE', 'EOF')):
                    self.gehe_weiter()
                if self.aktuelles_token()['type'] == 'NEUEZEILE':
                    self.gehe_weiter()
        if fehler:
            raise RuntimeError("\n".join(fehler))
        return {'type': 'PROGRAMM', 'body': anweisungen}

    def parse_anweisung(self):
        token = self.aktuelles_token()

        if token['type'] == 'KEYWORD':
            val = token['value']
            if val == 'KW_DEFINIERE': return self.parse_funktions_definition()
            if val == 'KW_KLASSE':    return self.parse_klassen_definition()
            if val == 'KW_VERSUCHE':  return self.parse_versuche_anweisung()
            if val == 'KW_AUSGABE':   return self.parse_ausgabe_anweisung()
            if val == 'KW_ERGEBNIS':  return self.parse_ergebnis_anweisung()
            if val == 'KW_WENN':      return self.parse_wenn_anweisung()
            if val == 'KW_BENUTZE':   return self.parse_import_anweisung()
            if val == 'KW_GLOBAL':    return self.parse_global_anweisung()
            if val == 'KW_WAEHLE':   return self.parse_waehle_anweisung()

            if val == 'KW_ABBRUCH':
                zeile = self.aktuelle_zeile(); self.gehe_weiter()
                return {'type': 'ABBRUCH_ANWEISUNG', 'line': zeile}
            if val == 'KW_WEITER':
                zeile = self.aktuelle_zeile(); self.gehe_weiter()
                return {'type': 'WEITER_ANWEISUNG', 'line': zeile}

            # FIX: Erlaube 'SCHLEIFE', 'FÜR' und 'SOLANGE' als Start einer Schleife
            if val in ['KW_SCHLEIFE', 'KW_FUER', 'KW_SOLANGE']:
                return self.parse_schleife_anweisung()

        if token['type'] == 'NAME' or (token['type'] == 'KEYWORD' and token['value'] in ['KW_SELBST', 'KW_ELTERN']):
            expr = self.parse_ausdruck()

            # Mehrfach-Zuweisung: a, b = 1, 2
            if self.aktuelles_token()['type'] == 'KOMMA':
                ziele = [expr]
                while self.aktuelles_token()['type'] == 'KOMMA':
                    self.gehe_weiter()
                    ziele.append(self.parse_ausdruck())
                if self.aktuelles_token()['type'] == 'OPERATOR' and self.aktuelles_token()['value'] == '=':
                    self.gehe_weiter()
                    werte = [self.parse_ausdruck()]
                    while self.aktuelles_token()['type'] == 'KOMMA':
                        self.gehe_weiter()
                        werte.append(self.parse_ausdruck())
                    valid_types = ['VARIABLE', 'ATTRIBUT_ZUGRIFF', 'INDEX_ZUGRIFF']
                    for z in ziele:
                        if z['type'] not in valid_types:
                            raise RuntimeError(_t("ERR_SYNTAX_INVALID_MULTI_TARGET", line=token.get('line')))
                    return {'type': 'MEHRFACH_ZUWEISUNG', 'ziele': ziele, 'werte': werte, 'line': token.get('line', 0)}

            if self.aktuelles_token()['type'] == 'OPERATOR' and self.aktuelles_token()['value'] == '=':
                self.gehe_weiter()
                wert = self.parse_ausdruck()
                valid_types = ['VARIABLE', 'ATTRIBUT_ZUGRIFF', 'INDEX_ZUGRIFF', 'ATTRIBUT_ZUWEISUNG']
                if expr['type'] not in valid_types:
                    raise RuntimeError(_t("ERR_SYNTAX_INVALID_TARGET", line=token.get('line')))
                return {'type': 'ZUWEISUNG', 'ziel': expr, 'wert': wert, 'line': token.get('line', 0)}
            return expr

        return self.parse_ausdruck()

    def parse_klassen_definition(self):
        zeile = self.aktuelle_zeile()
        self.erwarte('KEYWORD', 'KW_KLASSE')
        name = self.erwarte('NAME').get('value')

        elternklasse = None
        if self.aktuelles_token()['type'] == 'KLAMMER_AUF':
            self.gehe_weiter()
            elternklasse = self.erwarte('NAME').get('value')
            self.erwarte('KLAMMER_ZU')

        if self.aktuelles_token()['type'] == 'DOPPELPUNKT': self.gehe_weiter()
        self.erwarte('NEUEZEILE')

        methoden = []
        while not self.ist_kw('KW_ENDE_KLASSE'):
            if self.aktuelles_token()['type'] == 'EOF':
                raise RuntimeError(_t("ERR_SYNTAX_EXPECTED_VALUE", line=zeile, expected='KW_ENDE_KLASSE', found='EOF'))
            if self.aktuelles_token()['type'] == 'NEUEZEILE': self.gehe_weiter(); continue
            if self.ist_kw('KW_DEFINIERE'): methoden.append(self.parse_funktions_definition())
            else: raise RuntimeError(_t("ERR_ONLY_DEFINE_IN_CLASS"))
        self.erwarte('KEYWORD', 'KW_ENDE_KLASSE')
        return {'type': 'KLASSEN_DEFINITION', 'name': name, 'elternklasse': elternklasse, 'methoden': methoden, 'line': zeile}

    def parse_versuche_anweisung(self):
        zeile = self.aktuelle_zeile()
        self.erwarte('KEYWORD', 'KW_VERSUCHE'); self.erwarte('NEUEZEILE'); v = []; f = []
        while not self.ist_kw('KW_FANGE'):
            if self.aktuelles_token()['type'] == 'EOF':
                raise RuntimeError(_t("ERR_SYNTAX_EXPECTED_VALUE", line=zeile, expected='KW_FANGE', found='EOF'))
            if self.aktuelles_token()['type'] == 'NEUEZEILE': self.gehe_weiter(); continue
            v.append(self.parse_anweisung())
        self.erwarte('KEYWORD', 'KW_FANGE')
        fehler_var = None
        if self.aktuelles_token()['type'] == 'NAME':
            fehler_var = self.aktuelles_token()['value']
            self.gehe_weiter()
        self.erwarte('NEUEZEILE')
        while not self.ist_kw('KW_ENDE_VERSUCHE'):
             if self.aktuelles_token()['type'] == 'EOF':
                 raise RuntimeError(_t("ERR_SYNTAX_EXPECTED_VALUE", line=zeile, expected='KW_ENDE_VERSUCHE', found='EOF'))
             if self.aktuelles_token()['type'] == 'NEUEZEILE': self.gehe_weiter(); continue
             f.append(self.parse_anweisung())
        self.erwarte('KEYWORD', 'KW_ENDE_VERSUCHE')
        return {'type': 'VERSUCHE_ANWEISUNG', 'versuche_block': v, 'fange_block': f, 'fehler_var': fehler_var, 'line': zeile}

    def parse_waehle_anweisung(self):
        """Parst: WÄHLE ausdruck / FALL wert DANN ... / SONST ... / ENDE WÄHLE"""
        zeile = self.aktuelle_zeile()
        self.erwarte('KEYWORD', 'KW_WAEHLE')
        ausdruck = self.parse_ausdruck()
        self.erwarte('NEUEZEILE')
        faelle = []
        sonst_block = None
        # Überspringe leere Zeilen
        while self.aktuelles_token()['type'] == 'NEUEZEILE':
            self.gehe_weiter()
        # Parse FALL-Blöcke
        while self.ist_kw('KW_FALL'):
            self.erwarte('KEYWORD', 'KW_FALL')
            wert = self.parse_ausdruck()
            self.erwarte('KEYWORD', 'KW_DANN')
            self.erwarte('NEUEZEILE')
            block = []
            while (not self.ist_kw('KW_FALL') and
                   not self.ist_kw('KW_SONST') and
                   not self.ist_kw('KW_ENDE_WAEHLE')):
                if self.aktuelles_token()['type'] == 'EOF':
                    raise RuntimeError(_t("ERR_SYNTAX_EXPECTED_VALUE", line=zeile, expected='KW_ENDE_WAEHLE', found='EOF'))
                if self.aktuelles_token()['type'] == 'NEUEZEILE':
                    self.gehe_weiter(); continue
                block.append(self.parse_anweisung())
            faelle.append({'wert': wert, 'block': block})
        # Optionaler SONST-Block
        if self.ist_kw('KW_SONST'):
            self.erwarte('KEYWORD', 'KW_SONST')
            self.erwarte('NEUEZEILE')
            sonst_block = []
            while not self.ist_kw('KW_ENDE_WAEHLE'):
                if self.aktuelles_token()['type'] == 'EOF':
                    raise RuntimeError(_t("ERR_SYNTAX_EXPECTED_VALUE", line=zeile, expected='KW_ENDE_WAEHLE', found='EOF'))
                if self.aktuelles_token()['type'] == 'NEUEZEILE':
                    self.gehe_weiter(); continue
                sonst_block.append(self.parse_anweisung())
        self.erwarte('KEYWORD', 'KW_ENDE_WAEHLE')
        return {'type': 'WAEHLE_ANWEISUNG', 'ausdruck': ausdruck, 'faelle': faelle,
                'sonst_block': sonst_block, 'line': zeile}

    def parse_funktions_definition(self):
        zeile = self.aktuelle_zeile()
        self.erwarte('KEYWORD', 'KW_DEFINIERE'); name = self.erwarte('NAME').get('value'); self.erwarte('KLAMMER_AUF')
        params = []
        defaults = {}
        if self.aktuelles_token()['type'] != 'KLAMMER_ZU':
            p_name = self.erwarte('NAME').get('value')
            params.append(p_name)
            if self.aktuelles_token()['type'] == 'OPERATOR' and self.aktuelles_token()['value'] == '=':
                self.gehe_weiter()
                defaults[p_name] = self.parse_ausdruck()
            while self.aktuelles_token()['type'] == 'KOMMA':
                self.gehe_weiter()
                p_name = self.erwarte('NAME').get('value')
                params.append(p_name)
                if self.aktuelles_token()['type'] == 'OPERATOR' and self.aktuelles_token()['value'] == '=':
                    self.gehe_weiter()
                    defaults[p_name] = self.parse_ausdruck()
        self.erwarte('KLAMMER_ZU')
        # Doppelte Parameternamen erkennen
        gesehen = set()
        for p in params:
            if p in gesehen:
                raise RuntimeError(_t("ERR_SYNTAX_EXPECTED_VALUE", line=zeile, expected=f"eindeutiger Parameter", found=f"'{p}' (doppelt)"))
            gesehen.add(p)
        if self.aktuelles_token()['type'] == 'DOPPELPUNKT': self.gehe_weiter()
        self.erwarte('NEUEZEILE'); body = []
        while not self.ist_kw('KW_ENDE_FUNKTION'):
            if self.aktuelles_token()['type'] == 'EOF':
                raise RuntimeError(_t("ERR_SYNTAX_EXPECTED_VALUE", line=zeile, expected='KW_ENDE_FUNKTION', found='EOF'))
            if self.aktuelles_token()['type'] == 'NEUEZEILE': self.gehe_weiter(); continue
            body.append(self.parse_anweisung())
        self.erwarte('KEYWORD', 'KW_ENDE_FUNKTION')
        return {'type': 'FUNKTIONS_DEFINITION', 'name': name, 'parameter': params, 'defaults': defaults, 'body': body, 'line': zeile}

    def parse_wenn_anweisung(self):
        zeile = self.aktuelle_zeile()
        self.erwarte('KEYWORD', 'KW_WENN')
        faelle = [] 
        bed = self.parse_ausdruck()
        self.erwarte('KEYWORD', 'KW_DANN')
        
        if self.aktuelles_token()['type'] == 'NEUEZEILE': self.gehe_weiter()
        
        body = []
        while not (self.ist_kw('KW_SONST') or self.ist_kw('KW_SONST_WENN') or self.ist_kw('KW_ENDE_WENN')):
            if self.aktuelles_token()['type'] == 'EOF':
                raise RuntimeError(_t("ERR_SYNTAX_EXPECTED_VALUE", line=zeile, expected='KW_ENDE_WENN', found='EOF'))
            if self.aktuelles_token()['type'] == 'NEUEZEILE': self.gehe_weiter(); continue
            body.append(self.parse_anweisung())
        faelle.append((bed, body))

        sonst_body = None
        while self.ist_kw('KW_SONST') or self.ist_kw('KW_SONST_WENN'):
            ist_sonst_wenn = self.ist_kw('KW_SONST_WENN')
            self.gehe_weiter()
            if ist_sonst_wenn or self.ist_kw('KW_WENN'):
                if not ist_sonst_wenn:
                    self.gehe_weiter()
                bed = self.parse_ausdruck()
                self.erwarte('KEYWORD', 'KW_DANN')
                if self.aktuelles_token()['type'] == 'NEUEZEILE': self.gehe_weiter()
                body = []
                while not (self.ist_kw('KW_SONST') or self.ist_kw('KW_SONST_WENN') or self.ist_kw('KW_ENDE_WENN')):
                    if self.aktuelles_token()['type'] == 'EOF':
                        raise RuntimeError(_t("ERR_SYNTAX_EXPECTED_VALUE", line=zeile, expected='KW_ENDE_WENN', found='EOF'))
                    if self.aktuelles_token()['type'] == 'NEUEZEILE': self.gehe_weiter(); continue
                    body.append(self.parse_anweisung())
                faelle.append((bed, body))
            else:
                if self.aktuelles_token()['type'] == 'NEUEZEILE': self.gehe_weiter()
                sonst_body = []
                while not self.ist_kw('KW_ENDE_WENN'):
                    if self.aktuelles_token()['type'] == 'EOF':
                        raise RuntimeError(_t("ERR_SYNTAX_EXPECTED_VALUE", line=zeile, expected='KW_ENDE_WENN', found='EOF'))
                    if self.aktuelles_token()['type'] == 'NEUEZEILE': self.gehe_weiter(); continue
                    sonst_body.append(self.parse_anweisung())
                break

        self.erwarte('KEYWORD', 'KW_ENDE_WENN')
        return {'type': 'WENN_ANWEISUNG', 'faelle': faelle, 'sonst_koerper': sonst_body, 'line': zeile}

    def parse_schleife_anweisung(self):
        zeile = self.aktuelle_zeile()
        # FIX: Das Wort 'SCHLEIFE' ist jetzt optional!
        if self.ist_kw('KW_SCHLEIFE'):
            self.gehe_weiter()

        if self.ist_kw('KW_SOLANGE'):
            self.gehe_weiter(); bed = self.parse_ausdruck(); self.erwarte('KEYWORD', 'KW_MACHE')
            if self.aktuelles_token()['type'] == 'NEUEZEILE': self.gehe_weiter()
            k = []
            while not self.ist_kw('KW_ENDE_SCHLEIFE'):
                if self.aktuelles_token()['type'] == 'EOF':
                    raise RuntimeError(_t("ERR_SYNTAX_EXPECTED_VALUE", line=zeile, expected='KW_ENDE_SCHLEIFE', found='EOF'))
                if self.aktuelles_token()['type'] == 'NEUEZEILE': self.gehe_weiter(); continue
                k.append(self.parse_anweisung())
            self.erwarte('KEYWORD', 'KW_ENDE_SCHLEIFE')
            return {'type': 'SCHLEIFE_SOLANGE', 'bedingung': bed, 'koerper': k, 'line': zeile}

        elif self.ist_kw('KW_FUER'):
            self.gehe_weiter(); var = self.erwarte('NAME').get('value'); self.erwarte('KEYWORD', 'KW_IN'); lst = self.parse_ausdruck(); self.erwarte('KEYWORD', 'KW_MACHE')
            if self.aktuelles_token()['type'] == 'NEUEZEILE': self.gehe_weiter()
            k = []
            while not self.ist_kw('KW_ENDE_SCHLEIFE'):
                if self.aktuelles_token()['type'] == 'EOF':
                    raise RuntimeError(_t("ERR_SYNTAX_EXPECTED_VALUE", line=zeile, expected='KW_ENDE_SCHLEIFE', found='EOF'))
                if self.aktuelles_token()['type'] == 'NEUEZEILE': self.gehe_weiter(); continue
                k.append(self.parse_anweisung())
            self.erwarte('KEYWORD', 'KW_ENDE_SCHLEIFE')
            return {'type': 'SCHLEIFE_FÜR', 'variable': var, 'liste': lst, 'koerper': k, 'line': zeile}

        raise RuntimeError(_t("ERR_LOOP_EXPECTED_FOR_WHILE", line=self.aktuelles_token().get('line')))

    def parse_global_anweisung(self):
        zeile = self.aktuelle_zeile()
        self.erwarte('KEYWORD', 'KW_GLOBAL'); n = self.erwarte('NAME').get('value')
        return {'type': 'GLOBAL_ANWEISUNG', 'name': n, 'line': zeile}
    def parse_import_anweisung(self):
        zeile = self.aktuelle_zeile()
        self.erwarte('KEYWORD', 'KW_BENUTZE'); m = self.erwarte('NAME').get('value'); a = None
        if self.ist_kw('KW_ALS'): self.gehe_weiter(); a = self.erwarte('NAME').get('value')
        return {'type': 'IMPORT_ANWEISUNG', 'modul': m, 'alias': a or m, 'line': zeile}
    def parse_ausgabe_anweisung(self):
        zeile = self.aktuelle_zeile()
        self.erwarte('KEYWORD', 'KW_AUSGABE'); w = self.parse_ausdruck()
        return {'type': 'AUSGABE_ANWEISUNG', 'wert': w, 'line': zeile}
    def parse_ergebnis_anweisung(self):
        zeile = self.aktuelle_zeile()
        self.erwarte('KEYWORD', 'KW_ERGEBNIS'); w = self.parse_ausdruck()
        return {'type': 'ERGEBNIS_ANWEISUNG', 'wert': w, 'line': zeile}

    def parse_ausdruck(self): return self.parse_oder()

    def parse_oder(self):
        links = self.parse_und()
        while self.ist_kw('KW_ODER'):
            self.gehe_weiter()
            rechts = self.parse_und()
            links = {'type': 'BINÄRER_AUSDRUCK', 'links': links, 'operator': 'oder', 'rechts': rechts}
        return links

    def parse_und(self):
        links = self.parse_nicht()
        while self.ist_kw('KW_UND'):
            self.gehe_weiter()
            rechts = self.parse_nicht()
            links = {'type': 'BINÄRER_AUSDRUCK', 'links': links, 'operator': 'und', 'rechts': rechts}
        return links

    def parse_nicht(self):
        if self.ist_kw('KW_NICHT'):
            self.gehe_weiter()
            operand = self.parse_nicht()
            return {'type': 'UNAER_NICHT', 'wert': operand}
        return self.parse_vergleich()

    def parse_vergleich(self):
        links = self.parse_arithmetik()
        while self.aktuelles_token()['type'] == 'OPERATOR' and self.aktuelles_token()['value'] in ['==','!=','<','>','<=','>=']:
            op = self.erwarte('OPERATOR').get('value')
            rechts = self.parse_arithmetik()
            links = {'type': 'BINÄRER_AUSDRUCK', 'links': links, 'operator': op, 'rechts': rechts}
        return links
    def parse_arithmetik(self):
        links = self.parse_term()
        while self.aktuelles_token()['type'] == 'OPERATOR' and self.aktuelles_token()['value'] in ['+', '-']:
            op = self.erwarte('OPERATOR').get('value')
            rechts = self.parse_term()
            links = {'type': 'BINÄRER_AUSDRUCK', 'links': links, 'operator': op, 'rechts': rechts}
        return links
    def parse_term(self):
        links = self.parse_faktor()
        while self.aktuelles_token()['type'] == 'OPERATOR' and self.aktuelles_token()['value'] in ['*', '/', '%']:
            op = self.erwarte('OPERATOR').get('value')
            rechts = self.parse_faktor()
            links = {'type': 'BINÄRER_AUSDRUCK', 'links': links, 'operator': op, 'rechts': rechts}
        return links
    def parse_faktor(self):
        if self.aktuelles_token()['type'] == 'OPERATOR' and self.aktuelles_token()['value'] == '-':
            self.gehe_weiter()
            return {'type': 'UNAER_MINUS', 'wert': self.parse_faktor()}
        links = self.parse_atom()
        if self.aktuelles_token()['type'] == 'OPERATOR' and self.aktuelles_token()['value'] == '^':
            op = self.erwarte('OPERATOR').get('value')
            rechts = self.parse_faktor()
            return {'type': 'BINÄRER_AUSDRUCK', 'links': links, 'operator': op, 'rechts': rechts}
        return links

    def parse_atom(self):
        node = self._parse_basis()
        while True:
            t = self.aktuelles_token()
            if t['type'] == 'PUNKT':
                self.gehe_weiter(); attr = self.erwarte('NAME').get('value')
                if self.aktuelles_token()['type'] == 'KLAMMER_AUF':
                    res = self._parse_argument_liste()
                    node = {'type': 'METHODEN_AUFRUF', 'objekt': node, 'methode': attr, 'args': res['args'], 'kwargs': res['kwargs']}
                else:
                    node = {'type': 'ATTRIBUT_ZUGRIFF', 'objekt': node, 'attribut': attr}
            elif t['type'] == 'KLAMMER_AUF_ECKIG':
                self.gehe_weiter()
                start = None
                if self.aktuelles_token()['type'] != 'DOPPELPUNKT': start = self.parse_ausdruck()
                if self.aktuelles_token()['type'] == 'DOPPELPUNKT':
                    self.gehe_weiter(); ende = None
                    if self.aktuelles_token()['type'] != 'KLAMMER_ZU_ECKIG': ende = self.parse_ausdruck()
                    self.erwarte('KLAMMER_ZU_ECKIG')
                    node = {'type': 'SLICING', 'objekt': node, 'start': start, 'ende': ende}
                else:
                    self.erwarte('KLAMMER_ZU_ECKIG')
                    node = {'type': 'INDEX_ZUGRIFF', 'objekt': node, 'index': start}
            else: break
        return node

    def _parse_basis(self):
        t = self.aktuelles_token()
        if t['type'] == 'KEYWORD':
            val = t['value']
            if val == 'KW_SELBST': self.gehe_weiter(); return {'type': 'VARIABLE', 'name': 'SELBST'}
            if val == 'KW_ELTERN': self.gehe_weiter(); return {'type': 'ELTERN_ZUGRIFF'}
            if val == 'CONST_WAHR': self.gehe_weiter(); return {'type': 'VARIABLE', 'name': 'wahr'}
            if val == 'CONST_FALSCH': self.gehe_weiter(); return {'type': 'VARIABLE', 'name': 'falsch'}
            if val == 'CONST_NICHTS': self.gehe_weiter(); return {'type': 'VARIABLE', 'name': 'NICHTS'}
            if val == 'KW_LAMBDA': return self.parse_lambda()
            if val == 'FUNC_EINGABE_TEXT':
                self.gehe_weiter(); prompt = self.parse_ausdruck()
                return {'type': 'EINGABE_AUFRUF', 'modus': 'text', 'prompt': prompt}
            if val == 'FUNC_EINGABE_ZAHL':
                self.gehe_weiter(); prompt = self.parse_ausdruck()
                return {'type': 'EINGABE_AUFRUF', 'modus': 'zahl', 'prompt': prompt}
        if t['type'] == 'ZAHL': self.gehe_weiter(); return {'type': 'ZAHL_LITERAL', 'wert': t['value']}
        if t['type'] == 'STRING': self.gehe_weiter(); return {'type': 'STRING_LITERAL', 'wert': t['value']}
        if t['type'] == 'KLAMMER_AUF': 
            self.gehe_weiter(); node = self.parse_ausdruck(); self.erwarte('KLAMMER_ZU')
            return node
        if t['type'] == 'KLAMMER_AUF_ECKIG': return self.parse_listen_literal()
        if t['type'] == 'GESCHWEIFT_AUF': return self.parse_dict_literal()
        if t['type'] == 'NAME':
            name = t['value']; self.gehe_weiter()
            if self.aktuelles_token()['type'] == 'KLAMMER_AUF':
                res = self._parse_argument_liste()
                return {'type': 'FUNKTIONS_AUFRUF', 'name': name, 'args': res['args'], 'kwargs': res['kwargs']}
            return {'type': 'VARIABLE', 'name': name}
        raise RuntimeError(_t("ERR_UNEXPECTED_TOKEN", value=t.get('value'), line=t.get('line')))

    def parse_dict_literal(self):
        self.erwarte('GESCHWEIFT_AUF'); paare = []
        if self.aktuelles_token()['type'] != 'GESCHWEIFT_ZU':
            k = self.parse_ausdruck(); self.erwarte('DOPPELPUNKT'); v = self.parse_ausdruck(); paare.append((k, v))
            while self.aktuelles_token()['type'] == 'KOMMA':
                self.gehe_weiter(); k = self.parse_ausdruck(); self.erwarte('DOPPELPUNKT'); v = self.parse_ausdruck(); paare.append((k, v))
        self.erwarte('GESCHWEIFT_ZU')
        return {'type': 'DICT_LITERAL', 'paare': paare}

    def _parse_argument_liste(self):
        self.erwarte('KLAMMER_AUF')
        args = []
        kwargs = [] 
        
        if self.aktuelles_token()['type'] != 'KLAMMER_ZU':
            while True:
                is_kwarg = False
                if self.aktuelles_token()['type'] == 'NAME':
                    nxt = self.peek_token()
                    if nxt['type'] == 'OPERATOR' and nxt['value'] == '=':
                        is_kwarg = True
                
                if is_kwarg:
                    k = self.erwarte('NAME').get('value')
                    self.erwarte('OPERATOR', '=')
                    v = self.parse_ausdruck()
                    kwargs.append((k, v))
                else:
                    args.append(self.parse_ausdruck())
                
                if self.aktuelles_token()['type'] == 'KOMMA':
                    self.gehe_weiter()
                else:
                    break
                    
        self.erwarte('KLAMMER_ZU')
        return {'args': args, 'kwargs': kwargs}

    def parse_listen_literal(self):
        self.erwarte('KLAMMER_AUF_ECKIG'); el = []
        if self.aktuelles_token()['type'] != 'KLAMMER_ZU_ECKIG':
            el.append(self.parse_ausdruck())
            while self.aktuelles_token()['type'] == 'KOMMA':
                self.gehe_weiter()
                if self.aktuelles_token()['type'] == 'KLAMMER_ZU_ECKIG': break
                el.append(self.parse_ausdruck())
        self.erwarte('KLAMMER_ZU_ECKIG')
        return {'type': 'LISTEN_LITERAL', 'elemente': el}

    def parse_lambda(self):
        self.erwarte('KEYWORD', 'KW_LAMBDA')
        params = []
        if self.aktuelles_token()['type'] == 'KLAMMER_AUF':
            self.gehe_weiter()
            if self.aktuelles_token()['type'] != 'KLAMMER_ZU':
                params.append(self.erwarte('NAME').get('value'))
                while self.aktuelles_token()['type'] == 'KOMMA':
                    self.gehe_weiter(); params.append(self.erwarte('NAME').get('value'))
            self.erwarte('KLAMMER_ZU')
        else:
            params.append(self.erwarte('NAME').get('value'))
            while self.aktuelles_token()['type'] == 'KOMMA':
                self.gehe_weiter(); params.append(self.erwarte('NAME').get('value'))

        self.erwarte('DOPPELPUNKT')
        body = self.parse_ausdruck()
        return {'type': 'LAMBDA_ERSTELLUNG', 'params': params, 'body': body}