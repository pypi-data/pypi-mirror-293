from setuptools import setup, find_packages

setup(
    name='Tigrinya_alphabets',
    version='0.1.0',
    description='A library for encoding and decoding Tigrinya alphabets',
    author='Gide Segid',
    author_email='gidesegid@gmail.com',
    packages=find_packages(),
    install_requires=[
        # List any dependencies your package has here
    ],
    entry_points={
        'console_scripts': [
            'tigrinya-coder-decoder=tigrinya_alphabets.Tigrinya_alphabet_coder_decoder:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
