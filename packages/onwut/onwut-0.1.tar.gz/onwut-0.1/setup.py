# setup.py

from setuptools import setup, find_packages

setup(
    name="onwut",  # ライブラリの名前
    version="0.1",
    packages=find_packages(),  # パッケージを自動検出
    install_requires=[
        'requests',
        'beautifulsoup4',
        'PyPDF2',
        'lxml',
    ],  # 必要なライブラリ
    author="Your Name",
    author_email="your.email@example.com",
    description="A library for scraping and processing METI PDF reports",
    url="https://github.com/yourusername/onwut",
)
