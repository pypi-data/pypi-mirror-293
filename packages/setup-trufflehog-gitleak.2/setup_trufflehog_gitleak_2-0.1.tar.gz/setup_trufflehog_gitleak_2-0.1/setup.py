from setuptools import setup, find_packages
from setuptools.command.install import install as _install
import subprocess
import sys

class InstallWithGitleaks(_install):
    """Custom installation with Gitleaks setup"""
    def run(self):
        _install.run(self)
        self.run_gitleaks_installer()

    def run_gitleaks_installer(self):
        print("Running Gitleaks installer...")
        subprocess.check_call([sys.executable, 'install_gitleaks.py'])

setup(
    name='setup-trufflehog-gitleak.2',
    version='0.1',
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
