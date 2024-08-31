from setuptools import setup, find_packages

setup(
    name="holobit",
    version="0.1.0",
    author="Adolfo González Hernández",
    author_email="adolfogonzal@gmail.com",
    description="A quantum holographic library for simulating and visualizing quantum states.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/Alphonsus411/holobit',  # Reemplaza con tu repositorio de GitHub si tienes uno
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "numpy",
        "matplotlib",
    ],
)
