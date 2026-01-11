import subprocess
import shutil
import sys
from pathlib import Path


def get_mmdc_executable() -> str:
    """
    Tenta localizar o executável do Mermaid CLI (mmdc).
    Primeiro usa o PATH, depois tenta o caminho padrão do npm no Windows.
    """
    exe = shutil.which("mmdc")
    if exe:
        return exe

    home = Path.home()
    candidate = home / "AppData" / "Roaming" / "npm" / "mmdc.cmd"
    if candidate.exists():
        return str(candidate)

    raise RuntimeError(
        "Não encontrei o executável 'mmdc'. "
        "Verifique se o Mermaid CLI está instalado com:\n"
        "  npm install -g @mermaid-js/mermaid-cli\n"
        "e se a pasta do npm global está no PATH."
    )


def render_mermaid(input_mmd: str, output_file: str):
    """
    input_mmd   -> caminho para arquivo .mmd
    output_file -> saída (ex.: 'fluxo_poc.svg' ou 'fluxo_poc.pdf')
    O formato é inferido pela extensão do arquivo de saída.
    """
    mmdc = get_mmdc_executable()
    ext = Path(output_file).suffix.lower()

    cmd = [
        mmdc,
        "-i", input_mmd,
        "-o", output_file,
        "-t", "default",      # tema
        "-b", "transparent",  # background
    ]

    # Se for PDF, ajusta a página para caber exatamente no diagrama
    if ext == ".pdf":
        cmd.append("--pdfFit")

    print(f"Executando: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python mermaid.py <entrada.mmd> <saida.(svg|pdf|png)>")
        sys.exit(1)

    input_mmd = sys.argv[1]
    output_file = sys.argv[2]

    render_mermaid(input_mmd, output_file)
