# setup.py

from setuptools import setup, find_packages

setup(
    name="onwut",  # ライブラリの名前
    version="0.5",
    packages=find_packages(),  # パッケージを自動検出
    install_requires=[
        'requests',
        'beautifulsoup4',
        'PyPDF2',
        'lxml',
    ],  # 必要なライブラリ
    author="Your Name",
    author_email="your.email@example.com",
    description="onwut は、経済産業省のウェブサイトからPDFレポートをスクレイピングして処理するためのPythonライブラリです。",
    url="https://github.com/yourusername/onwut",
)
