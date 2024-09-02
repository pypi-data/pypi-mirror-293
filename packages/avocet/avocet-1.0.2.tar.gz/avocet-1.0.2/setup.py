from setuptools import setup, find_packages

setup(
    name="avocet",
    version="1.0.2",
    description="An easy to use Python package for encryption and decryption needs",
    author="Siddharth Krishnan",
    author_email="sid@sidkrishnan.com",
    url="https://github.com/sidkris/avocet",
    license="MIT",
    install_requires=["pycryptodomex"],
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
