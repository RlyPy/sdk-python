from setuptools import setup, find_packages
import os

# Читаем README.md для длинного описания
with open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="rollypay",
    version="0.1.4",
    description="Официальный Python SDK для платежной системы RollyPay",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="RollyPay Team",
    author_email="support@rollypay.io",
    url="https://rolly.pro",
    project_urls={
        "Homepage": "https://rolly.pro",
        "Documentation": "https://rollypay.io",
        "Source": "https://github.com/RlyPy/sdk-python",
        "Tracker": "https://github.com/RlyPy/sdk-python/issues",
    },
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business :: Financial :: Point-Of-Sale",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="rollypay, payments, sdk, api, crypto, acquiring, payment-gateway",
)
