from setuptools import setup, find_packages

setup(
    name='setup_trufflehog_gitleaks',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # List any external dependencies here
        'truffleHog',  # Adds truffleHog as a dependency
        'gitleaks',    # Adds gitleaks as a dependency
    ],
    entry_points={
        'console_scripts': [
            'install-security-package-tools=setup_security_tools.install_tools:main',
        ],
    },
    description='A package to install security tools like OWASP ZAP, TruffleHog, and Gitleaks',
    long_description=open('README.md').read(),
    # long_description_content_type='text/markdown',
    # author='Udit',
    # author_email='uditrajsingh815@example.com',
    # url='https://github.com/uditthakur2001/package',
)
