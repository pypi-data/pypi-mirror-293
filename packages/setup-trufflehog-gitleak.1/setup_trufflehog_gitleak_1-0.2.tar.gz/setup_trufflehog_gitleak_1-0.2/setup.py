from setuptools import setup, find_packages

setup(
    name='setup-trufflehog-gitleak.1',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'truffleHog',  # Adds truffleHog as a dependency
    ],
    entry_points={
        'console_scripts': [
            'install-security-package-tools=setup_security_tools.install_tools:main',
            'install-gitleaks=setup_security_tools.install_tools:install_gitleaks',  # Custom command to install gitleaks
        ],
    },
    description='A package to install security tools like TruffleHog and manage Gitleaks installation',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
