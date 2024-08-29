# Setup Security Tools

This package installs OWASP ZAP, Gitleaks, and TruffleHog on a Windows machine using Chocolatey and pip.

## Create a Package:

Install setuptools and wheel if you haven't already:

```bash
pip install setuptools wheel
```
Build the package:

```bash
python setup.py sdist bdist_wheel
```

## Usage

To use this package, install it locally and run the command:



```bash
pip install dist/setup_security_tools-0.1-py3-none-any.whl
```
```bash
setup-security-tools
```