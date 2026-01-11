# Python wrapper for Mermaid CLI

This repository contains a small **Python** script (`mermaid.py`) that **renders Mermaid diagrams** (`.mmd`) to **PDF, SVG, or PNG** by calling the **Mermaid CLI (`mmdc`)**.

It is meant for **reproducible**, **automatable** diagram generation (papers, theses, appendices, technical documentation), avoiding the friction and limitations of browser-based tools.

---

## Why this script exists

The **Mermaid Live Editor** and other web tools are convenient, but they often impose practical limitations for academic/technical workflows, such as:

- inconsistent or limited **PDF export** (page fitting, scaling, transparency);
- hard to standardize **theme**, **background**, and output options across machines;
- offline / restricted network environments (private repos, air-gapped machines);
- poor support for **batch rendering** (CI/CD, build scripts, Makefile targets);
- large or complex diagrams may fail or be painful to export reliably.

This script enables **local rendering** with consistent results and easy integration into a pipeline (e.g., `make diagrams`, GitHub Actions, release artifacts).

---

## What it does

`mermaid.py` uses `subprocess` to run Mermaid CLI (`mmdc`) with a standardized set of flags:

- input: `-i <file.mmd>`
- output: `-o <file.pdf|svg|png>`
- theme: `-t default`
- background: `-b transparent`
- PDF-only: `--pdfFit` (fits the PDF page to the diagram bounds)

---

## Requirements

### 1) Python
- Python **3.10+** (works with 3.11 too)

### 2) Node.js (IMPORTANT)
Mermaid CLI uses Puppeteer internally. If Node is too old, you may hit errors like:

> `SyntaxError: Unexpected token '??='`

Recommended: Node **18+** (or Node **20+**).

### 3) Mermaid CLI
- npm package: `@mermaid-js/mermaid-cli` (provides the `mmdc` executable)

---

## Installation

### Option A (recommended): install everything in **WSL/Linux**
This avoids the common WSL pitfall where `mmdc` resolves to the **Windows** binary under `/mnt/c/...`.

#### 1) Install Node LTS via NVM
```bash
# install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.nvm/nvm.sh

# install Node LTS (18/20+)
nvm install --lts
nvm use --lts

node -v
````

#### 2) Install Mermaid CLI

```bash
npm i -g @mermaid-js/mermaid-cli

which mmdc
mmdc --version
```

#### 3) Chromium dependencies (only if Puppeteer complains)

On some distros/WSL setups, Puppeteer needs extra system libraries:

```bash
sudo apt-get update
sudo apt-get install -y \
  libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 \
  libxkbcommon0 libxcomposite1 libxdamage1 libxrandr2 \
  libgbm1 libasound2 libpangocairo-1.0-0 libpango-1.0-0 \
  libgtk-3-0
```

---

### Option B: use it on **Windows** (no WSL)

1. Install Node **18+** / **20+**
2. Install Mermaid CLI:

```powershell
npm i -g @mermaid-js/mermaid-cli
mmdc --version
```

> Note: If you run the script from WSL but it calls `mmdc` from `/mnt/c/...`, then the **Windows Node version** is the one that matters.

---

## Usage

### Basic usage

```bash
python3 mermaid.py file.mmd flow.pdf
```

### Examples

```bash
# render SVG
python3 mermaid.py diagram.mmd diagram.svg

# render PNG
python3 mermaid.py diagram.mmd diagram.png

# render PDF with auto-fit (pdfFit)
python3 mermaid.py diagram.mmd diagram.pdf
```

---

## Parameters & behavior

The script expects **two positional arguments**:

1. **Input**: path to the `.mmd` file
2. **Output**: output file path (`.pdf`, `.svg`, `.png`, etc.)

The output format is inferred from the **output file extension**.

### `mmdc` flags used

The script builds a command equivalent to:

```bash
mmdc -i <input.mmd> -o <output.ext> -t default -b transparent [--pdfFit]
```

* `-t default`: sets the default theme (edit the script if you want a different theme)
* `-b transparent`: transparent background (great for papers/slides)
* `--pdfFit`: appended only when output is `.pdf` to fit the PDF page to the diagram

---

## Troubleshooting

### Error: `Unexpected token '??='`

This indicates a **Node.js version mismatch** (Node too old for the Puppeteer/mermaid-cli toolchain).

**Fix**

* Upgrade Node to **18+** (or 20+)
* Reinstall Mermaid CLI:

```bash
npm i -g @mermaid-js/mermaid-cli
```

### WSL is calling the Windows `mmdc`

Check:

```bash
which mmdc
node -v
```

If `which mmdc` points to `/mnt/c/...`, install Mermaid CLI inside WSL (Option A) and ensure the WSL `mmdc` appears first in your PATH.

---

## Repository structure

```text
.
├── mermaid.py
├── diagram.mmd
└── README.md
```

---

## References (official docs)

Copy/paste links:

```text
Mermaid (main project)
https://mermaid.js.org/

Mermaid CLI (@mermaid-js/mermaid-cli)
https://github.com/mermaid-js/mermaid-cli

Puppeteer (used by mmdc for headless rendering)
https://pptr.dev/

Node.js (required runtime)
https://nodejs.org/

NVM (Node Version Manager)
https://github.com/nvm-sh/nvm
```

---

## License

MIT License

Copyright (c) 2026 Jefferson Rodrigo Speck

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```
