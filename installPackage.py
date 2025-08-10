import sys
import subprocess
from pathlib import Path


def get_mayapy():
    """
    Get path of mayapy.exe

    Return (str): path of mayapy.exe
    """

    # Infer mayapy path from the running maya executable
    current_executable = Path(sys.executable)  # r"C:/Program Files/Autodesk/Maya2024/bin/maya.exe"
    mayapy_path = current_executable.parent / "mayapy.exe"  # r'C:/Program Files/Autodesk/Maya2024/bin/mayapy.exe'

    # Verify that the inferred mayapy executable exists
    if not mayapy_path.is_file():
        raise (f"ERROR: Could not find 'mayapy' at the expected location: {mayapy_path}")

    return mayapy_path


def install_requirements(mayapy_path, requirements_file):
    """# Runs the 'pip install -r' command to install packages."""

    command = [str(mayapy_path), "-m", "pip", "install", "-r", str(requirements_file)]

    print("-" * 50)
    print(f"Executing command: \n{' '.join(command)}")
    print("-" * 50)

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,  # Will raise CalledProcessError on non-zero exit codes
            encoding="utf-8",
        )
        print("--- SUCCESS ---")
        print(result.stdout)
        return True

    except subprocess.CalledProcessError as e:
        print("--- ERROR ---")
        print("Error Details:")
        print(e.stderr)


def install_package():
    """Main execution function."""
    print("\n" * 10)
    print("=" * 70)
    print("Starting Maya Plugin Dependency Installer")
    print("=" * 70)

    # Locate the requirements.txt file relative to this script
    try:
        script_path = Path(__file__).resolve()
        script_dir = script_path.parent
        requirements_file = script_dir / "requirements.txt"

        print(f"\nScriptPath: {script_dir}\n")

        if not requirements_file.is_file():
            print("=" * 70)
            print("\n")
            print("ERROR: 'requirements.txt' not found in the script's directory.")
            print("Please ensure 'install.py' and 'requirements.txt' are in the same folder.")
            print("=" * 70)
            return

    except NameError:
        print("=" * 70)
        print("ERROR: Could not determine script path.")
        print("Please run this by dragging the .py file into the Maya viewport instead of copy-pasting.")
        print("=" * 70)
        return

    # Get Maya environment details
    maya_info = get_mayapy()
    if not maya_info:
        return

    # Run the installation process

    if install_requirements(get_mayapy(), requirements_file):
        import site
        import importlib

        importlib.invalidate_caches()
        site.main()

        print("\n")
        print("=" * 70)
        print("SUCCESS All dependencies installed or up-to-date!")
        print("=" * 70)

    else:
        print("\n")
        print("=" * 70)
        print("ERROR: Some or all dependencies failed to install.")
        print("=" * 70)


def onMayaDroppedPythonFile(*args, **kwargs):
    """Dropped to maya functions"""
    install_package()
