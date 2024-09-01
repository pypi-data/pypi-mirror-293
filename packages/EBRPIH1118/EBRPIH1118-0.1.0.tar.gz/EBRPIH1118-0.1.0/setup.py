from setuptools import setup, find_packages

setup(
    name='EBRPIH1118',
    version='0.1.0',
    author='ElectronBits',
    author_email='info@electronbits.com',
    description='A Python package to interface with the board, and control relays, digital inputs/outputs, and analog inputs on Raspberry Pi.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/electronbits/Py_EBRPIH1118',  # Replace with your package URL
    packages=find_packages(),
    install_requires=[
        'RPi.GPIO',
        'spidev'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
