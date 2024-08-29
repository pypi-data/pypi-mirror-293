# security_tools/install_tools.py

import subprocess
import sys
import platform
import os
import urllib.request
import zipfile


def gitleaks():
    print("Attempting to install Gitleaks...")

    if platform.system() == "Darwin":  # macOS
        try:
            subprocess.run(["brew", "install", "gitleaks"], check=True)
            print("Gitleaks installed successfully.")
        except subprocess.CalledProcessError:
            print("Failed to install Gitleaks using Homebrew.")
    elif platform.system() == "Linux":
        try:
            url = "https://github.com/gitleaks/gitleaks/releases/download/v8.18.4/gitleaks_8.18.4_linux_armv6.tar.gz"
            # url = "https://sourceforge.net/projects/gitleaks.mirror/files/latest/download"
            subprocess.run(["curl", "-sSL", url, "-o", "gitleaks.zip"], check=True)
            subprocess.run(["unzip", "gitleaks.zip"], check=True)
            subprocess.run(["sudo", "mv", "gitleaks", "/usr/local/bin"], check=True)
            print("Gitleaks installed successfully.")
        except subprocess.CalledProcessError:
            print("Failed to install Gitleaks.")
    elif platform.system() == "Windows":
        try:
            # Replace with the correct URL for the latest Gitleaks release
            url = "https://github.com/gitleaks/gitleaks/releases/latest/download/gitleaks-windows-amd64-vX.Y.Z.zip"
            download_path = "gitleaks.zip"
            extract_path = "gitleaks"

            # Download Gitleaks
            print(f"Downloading Gitleaks from {url}...")
            urllib.request.urlretrieve(url, download_path)
            print("Download complete.")

            # Extract the ZIP file
            print("Extracting Gitleaks...")
            with zipfile.ZipFile(download_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)
            print("Extraction complete.")

            # Move the executable to a directory in PATH
            gitleaks_executable = os.path.join(extract_path, "gitleaks.exe")
            if os.path.exists(gitleaks_executable):
                # Optionally, move it to a directory in PATH, e.g., C:\Windows\System32
                destination = os.path.join(os.getenv('SystemRoot', 'C:\\Windows'), 'System32', 'gitleaks.exe')
                os.rename(gitleaks_executable, destination)
                print(f"Gitleaks installed and moved to {destination}.")
            else:
                print("Gitleaks executable not found after extraction.")

            # Clean up
            os.remove(download_path)
            os.rmdir(extract_path)
        except Exception as e:
            print(f"Failed to install Gitleaks: {e}")
    else:
        print("Gitleaks installation is currently supported only on Windows.")
        print("Please install Gitleaks manually from https://github.com/gitleaks/gitleaks")

def main():
    print("Installing security tools...")
    subprocess.run(["trufflehog", "--help"])

def install_gitleaks_command():
    gitleaks()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "gitleaks":
        install_gitleaks_command()
    else:
        main()
