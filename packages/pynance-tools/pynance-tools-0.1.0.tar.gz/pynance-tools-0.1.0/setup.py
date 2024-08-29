from setuptools import setup, find_packages

# Read the contents of your README file
with open("readme.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pynance-tools',
    version='0.1.0',
    author='Rithvik Reddygari',
    author_email='reddygari.rithvik@gmail.com',
    description='A Python library for financial calculations and formulas of TVM, and asset valuation.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ricky122-5/pynance',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'scipy',
    ],
    tests_require=['unittest'],
    test_suite='test',
    include_package_data=True,
)
