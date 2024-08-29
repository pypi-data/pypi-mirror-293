from setuptools import setup, find_packages
from setuptools.command.install import install as _install
import os
import platform
import urllib.request
import zipfile
import subprocess

class InstallWithGitleaks(_install):
    """Custom installation with Gitleaks setup"""
    def run(self):
        _install.run(self)
        self.install_gitleaks()

    def install_gitleaks(self):
        if platform.system() == "Windows":
            url = "https://github.com/gitleaks/gitleaks/releases/download/v8.18.4/gitleaks_8.18.4_windows_armv6.zip"
            download_path = "gitleaks.zip"
            extract_path = "gitleaks"

            print("Downloading Gitleaks...")
            urllib.request.urlretrieve(url, download_path)

            print("Extracting Gitleaks...")
            with zipfile.ZipFile(download_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)

            print("Installing Gitleaks...")
            gitleaks_executable = os.path.join(extract_path, "gitleaks.exe")
            destination = os.path.join(os.getenv('SystemRoot', 'C:\\Windows'), 'System32', 'gitleaks.exe')
            os.rename(gitleaks_executable, destination)

            print(f"Gitleaks installed to {destination}.")
        else:
            print("Gitleaks installation is supported only on Windows.")
            print("Please install Gitleaks manually from https://github.com/gitleaks/gitleaks")

setup(
    name='setup-trufflehog-gitleak.1',
    version='0.5',
    packages=find_packages(),
    install_requires=[
        'truffleHog',  # Include truffleHog as a dependency
    ],
    cmdclass={
        'install': InstallWithGitleaks,
    },
    entry_points={
        'console_scripts': [
            'install-security-package-tools=security_tools.install_tools:main',
            # Add other entry points if needed
        ],
    },
    description='A package to install and use security tools like TruffleHog and Gitleaks.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
