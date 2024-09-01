from setuptools import setup, find_packages

setup(
    name="filesense",
    version="1.0.1",
    packages=find_packages(),
    install_requires=[
        "langchain_community",
        "pypdf",
        "google-generativeai",
        "pillow",
        "docx2txt",
        "unstructured",
        "python-pptx"
        
    ],
    author="Mayur Dabade",
    author_email="mayurdabade1103@gmail.com",
    description="A package to rename files based on their content using Generative AI.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mayurd8862/FileSense.AI-Semantic-File-Renamer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)
