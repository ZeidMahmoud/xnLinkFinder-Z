#!/usr/bin/env python
import os
import shutil
from setuptools import setup, find_packages

target_directory = (
    os.path.join(os.getenv("APPDATA", ""), "xnLinkFinder")
    if os.name == "nt"
    else (
        os.path.join(os.path.expanduser("~"), ".config", "xnLinkFinder")
        if os.name == "posix"
        else (
            os.path.join(
                os.path.expanduser("~"),
                "Library",
                "Application Support",
                "xnLinkFinder",
            )
            if os.name == "darwin"
            else None
        )
    )
)

# Copy the config.yml file to the target directory if it exists
configNew = False
if target_directory and os.path.isfile("config.yml"):
    os.makedirs(target_directory, exist_ok=True)
    # If file already exists, create a new one
    if os.path.isfile(target_directory + "/config.yml"):
        configNew = True
        os.rename(
            target_directory + "/config.yml", target_directory + "/config.yml.OLD"
        )
        shutil.copy("config.yml", target_directory)
        os.rename(
            target_directory + "/config.yml", target_directory + "/config.yml.NEW"
        )
        os.rename(
            target_directory + "/config.yml.OLD", target_directory + "/config.yml"
        )
    else:
        shutil.copy("config.yml", target_directory)

setup(
    name="xnlinkfinder",
    packages=find_packages(),
    version=__import__("xnLinkFinder").__version__,
    description="A python script to find endpoints from a URL, a file of URLs, a directory of files, a Burp XML file or a ZAP ASCII message file. It also gets potential parameters and a target specific wordlist.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="@xnl-h4ck3r",
    url="https://github.com/xnl-h4ck3r/xnlLinkFinder",
    py_modules=["xnLinkFinder"],
    install_requires=[
        "requests>=2.31.0",
        "psutil>=5.9.0",
        "pyyaml>=6.0.0",
        "termcolor>=2.3.0",
        "urlparse3>=1.1.0",
        "beautifulsoup4>=4.12.0",
        "lxml>=4.9.0",
        "html5lib>=1.1",
        "urllib3>=2.0.0",
        "tldextract>=5.0.0",
        "inflect>=7.3.0",
        "playwright>=1.40.0",
        "pypdf>=3.17.0",
        # New advanced features dependencies
        "aiohttp>=3.9.0",
        "aiodns>=3.1.0",
        "rich>=13.0.0",
        "textual>=0.40.0",
        "sqlalchemy>=2.0.0",
        "alembic>=1.12.0",
        "regex>=2023.0.0",
        "jinja2>=3.1.0",
        "bloom-filter2>=2.0.0",
        "scikit-learn>=1.3.0",
        "numpy>=1.24.0",
        "python-dateutil>=2.8.0",
    ],
    entry_points={
        "console_scripts": [
            "xnLinkFinder = xnLinkFinder.xnLinkFinder:main",
        ],
    },
)

if configNew:
    print(
        "\n\033[33mIMPORTANT: The file "
        + target_directory
        + "/config.yml already exists.\nCreating config.yml.NEW but leaving existing config.\nIf you need the new file, then remove the current one and rename config.yml.NEW to config.yml\n\033[0m"
    )
else:
    print(
        "\n\033[92mThe file "
        + target_directory
        + "/config.yml has been created.\n\033[0m"
    )

# If the OS is linux and pdftotext or ocrmypdf is not installed, then suggest it
if os.name == "posix":
    if shutil.which("pdftotext") is None or shutil.which("ocrmypdf") is None:
        print(
            "\n\033[33mNOTE: To get the best results for extracting links from PDF files:"
        )
        if shutil.which("pdftotext") is None:
            print("- Install poppler-utils: sudo apt install -y poppler-utils")
        if shutil.which("ocrmypdf") is None:
            print(
                "- Install ocrmypdf for OCR fallback on scanned PDFs: sudo apt install -y ocrmypdf"
            )
        print("\033[0m")
