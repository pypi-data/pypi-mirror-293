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
            extract_path = os.path.join(os.getenv('USERPROFILE'), 'bin', 'gitleaks')

            # Create user bin directory if it does not exist
            os.makedirs(extract_path, exist_ok=True)

            print("Downloading Gitleaks...")
            urllib.request.urlretrieve(url, download_path)

            print("Extracting Gitleaks...")
            with zipfile.ZipFile(download_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)

            print("Gitleaks installed in user bin directory.")
            # Optionally add the directory to PATH
            self.add_to_path(extract_path)
        else:
            print("Gitleaks installation is supported only on Windows.")
            print("Please install Gitleaks manually from https://github.com/gitleaks/gitleaks")

    def add_to_path(self, directory):
        path = os.environ.get('PATH', '')
        if directory not in path:
            new_path = f"{path};{directory}"
            os.environ['PATH'] = new_path
            print(f"Added {directory} to PATH.")
            # Update the user's PATH environment variable permanently
            with open(os.path.expanduser("~/.bashrc"), "a") as file:
                file.write(f'export PATH="{directory}:$PATH"\n')
            # Notify user to restart their terminal or system
            print("Please restart your terminal or system to apply the PATH changes.")

setup(
    name='setup-trufflehog-gitleak.1',
    version='0.6',
    packages=find_packages(),
    install_requires=[
        'truffleHog',  # Include truffleHog as a dependency
    ],
    cmdclass={
        'install': InstallWithGitleaks,
    },
    entry_points={
        'console_scripts': [
            'install-security-package-tools=setup_security_tools.install_tools:main',
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
