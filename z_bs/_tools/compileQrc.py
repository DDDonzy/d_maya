from pathlib import Path
import subprocess
import sys

pyside2_rcc = r"C:\Program Files\Autodesk\Maya2024\bin\pyside2-rcc.exe"

source_qrc = r"T:\d_maya\z_bs\icon\_qrc.qrc"


dir = Path(source_qrc).parent
out_qrcPy = dir / "_qrc.py"
out_qrcPy = str(out_qrcPy.resolve())


def compile_resources():
    """Compile .qrc resource file"""
    print("Compiling resources...")
    cmd = [pyside2_rcc, source_qrc, "-o", out_qrcPy]
    subprocess.run(cmd, check=True)
    print("Resource compilation finished!")




if __name__ == "__main__":
    compile_resources()