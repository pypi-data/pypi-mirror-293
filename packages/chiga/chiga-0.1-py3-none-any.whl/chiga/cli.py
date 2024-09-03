import subprocess
import sys
import os

REQUIREMENTS_FILE = "requirements.txt"

def install_package(package_name):
    # Run pip to install the package
    subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
    
    # Update the requirements.txt file
    if os.path.exists(REQUIREMENTS_FILE):
        with open(REQUIREMENTS_FILE, "r") as f:
            installed_packages = f.read().splitlines()
    else:
        installed_packages = []
    
    if package_name not in installed_packages:
        with open(REQUIREMENTS_FILE, "a") as f:
            f.write(f"{package_name}\n")

def main():
    if len(sys.argv) < 3 or sys.argv[1] != "install":
        print("Usage: pp install <package_name>")
        sys.exit(1)
    
    package_name = sys.argv[2]
    install_package(package_name)
