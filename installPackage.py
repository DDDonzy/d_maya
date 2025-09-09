import sys
import subprocess
from pathlib import Path


def install_requirements(requirements_file):
    """# Runs the 'pip install -r' command to install packages."""

    command = [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)]

    print(f"{'':=^{120}}")
    print(f"Executing command: \n{' '.join(command)}")

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,  # Will raise CalledProcessError on non-zero exit codes
            encoding="utf-8",
        )
        print(f"{' SUCCESS ':=^{120}}")
        print(result.stdout)
        return True

    except subprocess.CalledProcessError as e:
        print(f"{' ERROR ':=^{120}}")
        print(e.stderr)


def install_package():
    """Main execution function."""
    print("\n" * 4)
    print(f"{'':=^{120}}")
    print(f"{' Starting Installer ':=^{120}}")
    print(f"{'':=^{120}}")

    # Locate the requirements.txt file relative to this script
    try:
        script_path = Path(__file__).resolve()
        script_dir = script_path.parent
        requirements_file = script_dir / "requirements.txt"

        print(f"\nScriptPath: {script_dir}\n")

        if not requirements_file.is_file():
            print(f"{'':=^{120}}")
            print("ERROR: 'requirements.txt' not found in the script's directory.")
            print("Please ensure 'install.py' and 'requirements.txt' are in the same folder.")
            print(f"{'':=^{120}}")
            return

    except NameError:
        print(f"{'':=^{120}}")
        print("ERROR: Could not determine script path.")
        print("Please run this by dragging the .py file into the Maya viewport instead of copy-pasting.")
        print(f"{'':=^{120}}")
        return
    

    # Run the installation process
    if install_requirements(requirements_file):
        import site
        import importlib

        importlib.invalidate_caches()
        site.main()

        print("\n")
        print(f"{'':=^{120}}")
        print("SUCCESS All dependencies installed or up-to-date!")
        print(f"{'':=^{120}}")

    else:
        print("\n")
        print(f"{'':=^{120}}")
        print("ERROR: Some or all dependencies failed to install.")
        print(f"{'':=^{120}}")

if __name__ == "__main__":
    install_package()
