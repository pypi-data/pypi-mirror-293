from setuptools import setup, find_packages

setup(
    name="vizutils",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "matplotlib",
        "seaborn",
        "plotly",
        "pandas"
    ],
    author="Omkar Singh",
    author_email="singhomkar20.1995@gmail.com",
    description="A library for creating visualizations for data analysis.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/omkars20/vizutils_package.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
