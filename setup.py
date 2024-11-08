from setuptools import setup, find_packages

setup(
    name="mediterrania_orchestrator",
    version="0.1.0",
    package_dir={'': 'src'},  # Set the base directory to 'src'
    packages=find_packages(where='src'),
    package_data={
        'mediterrania_orchestrator': ['data/*.json'],
    },
    include_package_data=True,
    install_requires=[
        'numpy>=1.21.0',
        'pandas>=1.3.0',
        'pytest>=6.2.5',
    ],
    author="Federico Peliti",
    author_email="",
    description="Un orchestratore per la creazione di piani alimentari personalizzati",
    #long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AhUhmm/mediterrania_orchestrator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)