from setuptools import setup, find_packages

setup(
    name="mediterrania_orchestrator",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'numpy>=1.21.0',
        'pandas>=1.3.0',
        'pytest>=6.2.5',
    ],
    author="Federico Peliti",
    author_email="",
    description="Un orchestratore per la creazione di piani alimentari personalizzati",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AhUhmm/mediterrania_orchestrator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)