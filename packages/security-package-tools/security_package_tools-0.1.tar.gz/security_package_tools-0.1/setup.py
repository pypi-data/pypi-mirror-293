from setuptools import setup, find_packages

setup(
    name='security_package_tools',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # List any external dependencies here
    ],
    entry_points={
        'console_scripts': [
            'install-security-package-tools=security_tools.install_tools:main',
        ],
    },
    description='A package to install security tools like OWASP ZAP, TruffleHog, and Gitleaks',
    long_description=open('README.md').read(),
    # long_description_content_type='text/markdown',
    # author='Your Name',
    # author_email='your.email@example.com',
    # url='https://github.com/yourusername/security_tools',
)
