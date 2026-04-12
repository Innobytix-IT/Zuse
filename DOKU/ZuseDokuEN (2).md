# ZUSE v7.3  Open Source GNU GPL v3
> **"Simple because 'Simple' is simple."**

![Version](https://img.shields.io/badge/Version-7.3-blue) ![Language](https://img.shields.io/badge/Made_with-Python-yellow) ![Status](https://img.shields.io/badge/Status-Stable-green) ![Tests](https://img.shields.io/badge/Tests-1086+-brightgreen)

**Zuse** is an object-oriented, transpiling programming language designed to break the barrier between "Learning Languages" (like Scratch) and "Pro Languages" (like Python/C++).

It enables programming in your native language (DE, EN, ES, FR, IT, PT, HI, ZH), offers a seamless transition from simple graphics programming to controlling complex hardware, and transpiles Zuse code into 5 target languages.

---

## Features

*   **Multilingual:** The interpreter understands 8 languages natively (German, English, Spanish, French, Italian, Portuguese, Hindi, Chinese).
*   **Dual Mode:**
    *   **Learning Mode:** Sandbox environment for kids/beginners (safe commands only).
    *   **Pro Mode ("God Mode"):** Full access to the Python Runtime (including hardware control).
*   **5 Transpiler Backends:** Translate Zuse code into Python, JavaScript, Java, C#, or WebAssembly.
*   **Game Engine (Spielfeld):** Full 2D game engine with sprites, collision detection, keyboard/mouse input, and game loop (60 FPS).
*   **Turtle Graphics (Painter):** Draw stars, spirals, and fractals — in your native language.
*   **Zuse Studio:** A custom IDE with syntax highlighting, debugger, live translation, and integrated transpiler.
*   **Debugger:** Breakpoints, step-by-step execution, variable inspection.
*   **LSP Server:** Language Server Protocol for VS Code and other editors (go-to-definition, hover docs).
*   **Semantic Analysis:** Detects variable shadowing, unreachable code, and duplicate parameters.
*   **Web Playground:** Run Zuse in the browser — no installation needed (Pyodide + CodeMirror).
*   **Package Manager (zpkg):** Install and share packages with SemVer versioning.
*   **Environment Aware:** Zuse automatically detects whether it is running inside the IDE, as a standalone application, or in the browser, and adapts dynamically.
*   **50+ built-in functions:** Math, text, lists, files, random, type checking, formatting.
*   **1102+ automated tests** across 31 test modules.

---

## System Architecture

Zuse is based on a **multi-stage pipeline architecture**:

### 1. The Core (Lexer → Parser → AST)
The **Lexer** (`lexer.py`) recognizes keywords via interchangeable language mappings (JSON) and generates canonical tokens. The **Parser** (`parser.py`) produces a language-independent AST (Abstract Syntax Tree).

### 2. The Interpreter (Visitor Pattern)
The engine (`interpreter.py`) executes the AST. It features a **Smart Import Mechanism**, a **Sentinel Pattern** for safe attribute access, and recognizes constructors across languages (`ERSTELLE`, `CREATE`, `CREAR`, `CREER`, `CREA`, `CRIAR`).

### 3. The Transpiler (5 Backends)
The AST is translated by specialized backends into **Python**, **JavaScript**, **Java**, **C#**, or **WebAssembly**. Java and C# backends use **variable tracking** to prevent duplicate declarations.

### 4. The IDE (Zuse Studio)
The Studio (`zuse_studio.py`) is thread-safe and features learning/pro mode, a **debugger** with breakpoints, **pre-flight check** logic, and integrated transpiler controls.

### 5. The Standard Library (8 Languages)
The `.zuse` files in the `bibliothek/` folder provide **Painter** (turtle graphics) and **Game Engine** (2D games) in all 8 languages.

### 6. Additional Tools
*   **LSP Server** (`zuse_lsp_server.py`) for editor integration
*   **Semantic Analysis** for code quality checks
*   **Web Playground** (`playground/`) for the browser
*   **Package Manager** (`zpkg_core.py`) for package management

---

## Syntax Examples (English)

### Hello World & Logic
```zuse
text = "Hello Zuse"
number = 42

IF number > 10 THEN
    PRINT text
ELSE
    PRINT "Number is small"
END IF
```

### Loops
```zuse
LOOP FOR i IN RANGE(5) DO
    PRINT "Iteration: " + AS_TEXT(i)
END LOOP
```

### Functions with Lambda
```zuse
DEFINE square(x):
    RETURN x ^ 2
END FUNCTION

numbers = [1, 2, 3, 4, 5]
even = FILTER(numbers, LAMBDA(x): x % 2 == 0)
PRINT even    # [2, 4]
```

### Object Orientation with Inheritance
```zuse
CLASS Animal:
    DEFINE CREATE(name):
        SELF.name = name
    END FUNCTION

    DEFINE speak():
        PRINT SELF.name + " makes a sound."
    END FUNCTION
END CLASS

CLASS Dog(Animal):
    DEFINE speak():
        PRINT SELF.name + " says: Woof!"
    END FUNCTION
END CLASS

buddy = Dog("Buddy")
buddy.speak()    # Buddy says: Woof!
```

### Error Handling
```zuse
TRY
    result = 10 / 0
CATCH error
    PRINT "Error: " + error
END TRY
```

### Graphics (The Painter)
```zuse
IMPORT english AS lib
brush = lib.Painter()

brush.color("blue")
brush.thickness(5)

LOOP FOR i IN RANGE(4) DO
    brush.forward(100)
    brush.turn_right(90)
END LOOP

brush.done()
```

### Game Engine (Spielfeld)
```zuse
IMPORT english AS lib

game = lib.GameField("My Game", 800, 600, "black")
player = game.new_sprite(400, 300, 30, 30, "blue")

DEFINE update()
    IF game.key_pressed("Left") THEN
        player.move(-5, 0)
    END IF
    IF game.key_pressed("Right") THEN
        player.move(5, 0)
    END IF
END FUNCTION

game.game_loop(update, 60)
game.start()
```

---

## Usage

### Start the IDE
```bash
python zuse_studio.py
```

### Run a Program (Standalone)
```bash
python main.py my_script.zuse english
```

### Start the Web Playground
```bash
python playground/server.py
```

---

## Hardware & Deployment

Thanks to **Pro Mode**, Zuse can access hardware directly.

**Example: Controlling Arduino**
```zuse
IMPORT pyfirmata
board = pyfirmata.Arduino("COM3")
led = board.get_pin("d:13:o")
led.write(1)
```

---

## Transpiler — Translate Zuse Code

```zuse
# This Zuse program...
DEFINE factorial(n):
    IF n <= 1 THEN
        RETURN 1
    ELSE
        RETURN n * factorial(n - 1)
    END IF
END FUNCTION
```

...becomes **JavaScript**:
```javascript
function factorial(n) {
    if (n <= 1) { return 1; }
    else { return n * factorial(n - 1); }
}
```

...or **Java**:
```java
static Object factorial(Object n) {
    if ((int)n <= 1) { return 1; }
    else { return (int)n * (int)factorial((int)n - 1); }
}
```

---

## Roadmap (Zuse: The Universal Vision)

*   [x] **v6.9:** Stable interpreter, IDE, libraries (DE/EN/ES/PT/FR/IT).
*   [x] **v7.3:** 8 languages (DE/EN/ES/FR/IT/PT/HI/ZH), 5 transpiler backends (Python, JS, Java, C#, WASM), game engine, debugger, LSP server, web playground, package manager, semantic analysis, 1102+ tests.
*   [ ] **vNext (Zuse Universal):** Further optimization, additional languages, extended IDE features.

<img width="585" height="584" alt="image" src="https://github.com/user-attachments/assets/4b5ab1b0-38c5-4da5-9b72-8daa45b87e40" />

---

**Architect:** Manuel Person

**License:** Open Source GNU GPL v3
