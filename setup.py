from setuptools import setup, find_packages

setup(
    name="ebook_processor",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "spacy",
        "elevenlabs",
        "pdfplumber",
        "openai",
        "regex",
        "num2words",
    ],
    author="Str8-Up",
    author_email="david@kampusmedia.com",
    description="Processes PDF files through various scripts to extract, clean, format and export text from a PDF file",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ebook_processor",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
