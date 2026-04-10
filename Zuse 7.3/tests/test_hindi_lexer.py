import re, json, sys, os
sys.stdout.reconfigure(encoding='utf-8')

ZUSE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ZUSE_DIR)

with open(os.path.join(ZUSE_DIR, 'sprachen', 'hindi.json'), encoding='utf-8') as f:
    conf = json.load(f)

# Test: Build keyword regex like lexer does
test_code = 'अगर उम्र >= 18 तो'
print(f"Test code: {test_code}")
print()

for key in ['KW_WENN', 'KW_DANN', 'KW_IN', 'KW_MACHE', 'KW_SCHLEIFE', 'KW_FUER']:
    value = conf[key]
    escaped = re.escape(value)
    pattern = rf'\b{escaped}\b'
    matches = list(re.finditer(pattern, test_code))
    print(f'{key} = "{value}" -> pattern: {pattern} -> matches: {len(matches)}')

print()
# Test NAME regex matching
NAME = r'[A-Za-z_\u00C0-\u024F\u0900-\u097F\u4E00-\u9FFF\u3400-\u4DBF\uF900-\uFAFF][A-Za-z0-9_\u00C0-\u024F\u0900-\u097F\u4E00-\u9FFF\u3400-\u4DBF\uF900-\uFAFF]*'
print("NAME regex matches:")
for m in re.finditer(NAME, test_code):
    print(f'  "{m.group()}" at pos {m.start()}')

print()
# Key test: does \b work with Devanagari?
print("\\b test with तो:")
p = re.compile(r'\bतो\b')
for test in ['अगर उम्र >= 18 तो', 'तो', ' तो ', 'अगरतो']:
    matches = list(p.finditer(test))
    print(f'  "{test}" -> {len(matches)} match(es)')

print()
# Test full lexer
print("=== Full lexer test ===")
from lexer import Lexer
lexer = Lexer(conf)
try:
    tokens = lexer.tokenize(test_code)
    for tok in tokens:
        print(f'  {tok["type"]:15} {tok.get("value",""):20} (original: {tok.get("original","")})')
except Exception as e:
    print(f'ERROR: {e}')
