from setuptools import setup, find_packages

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="echocmdlib",
    version="0.1.7",
    packages=find_packages(),
    install_requires=[
        'colorama',
        'pyfiglet',
        "rich"
    ],
    long_description=long_description,
    long_description_content_type="text/x-rst", 
    author="Timothy Wu",
    author_email="wuxiaoyu1107g@gmail.com",
    url="https://github.com/codetimothy/echocmdlib",  # 可选
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
