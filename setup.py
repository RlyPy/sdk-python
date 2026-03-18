from setuptools import setup, find_packages

setup(
    name="rollypay",
    version="0.1.0",
    description="Официальный Python SDK для RollyPay API",
    long_description="Официальный Python SDK для платежной системы RollyPay (https://rollypay.io). Позволяет работать с кассами, платежами, статистикой и курсами валют.",
    author="RollyPay Team",
    author_email="support@rollypay.io",
    url="https://rolly.pro",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
