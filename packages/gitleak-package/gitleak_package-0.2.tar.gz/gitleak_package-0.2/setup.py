from setuptools import setup, find_packages
import platform

# Determine the operating system
system = platform.system().lower()

# Define entry points based on the OS
if system == 'windows':
    entry_points = {
        'console_scripts': [
            'install-gitleaks=gitleaks_installer.installer:install_gitleaks',
            'add-gitleaks-path=gitleaks_installer.installer:add_gitleaks_to_path',
        ],
    }
else:
    entry_points = {
        'console_scripts': [
            'install-gitleaks=gitleaks_installer.installer:install_gitleaks',
            'add-gitleaks-path=gitleaks_installer.installer:add_gitleaks_to_path',
        ],
    }

setup(
    name="gitleak-package",
    version="0.2",
    packages=find_packages(),
    install_requires=[],  # No external dependencies
    entry_points=entry_points,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
