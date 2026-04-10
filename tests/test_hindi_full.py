import sys
import os
sys.stdout.reconfigure(encoding='utf-8')

ZUSE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ZUSE_DIR)

import json
from lexer import Lexer

with open(os.path.join(ZUSE_DIR, 'sprachen', 'hindi.json'), encoding='utf-8') as f:
    conf = json.load(f)

lexer = Lexer(conf)

tests = [
    'दिखाओ "नमस्ते दुनिया!"',
    'अगर उम्र >= 18 तो',
    'अंत अगर',
    'चक्र हर i में [1, 2, 3, 4] करो',
    'अंत चक्र',
    'परिभाषा नया():',
    'अंत फलन',
    'वर्ग चित्रकार:',
    'अंत वर्ग',
    'प्रयास',
    'पकड़ो',
    'अंत प्रयास',
    'मेरा.नाम = "ज़ूज़"',
    'वरना अगर साफ == "लाल" तो',
]

for code in tests:
    print(f'Code: {code}')
    try:
        tokens = lexer.tokenize(code)
        for tok in tokens:
            if tok['type'] != 'EOF':
                orig = tok.get('original', '')
                if orig:
                    print(f'  {tok["type"]:15} {tok["value"]:25} (orig: {orig})')
                else:
                    print(f'  {tok["type"]:15} {tok["value"]}')
    except Exception as e:
        print(f'  ERROR: {e}')
    print()
