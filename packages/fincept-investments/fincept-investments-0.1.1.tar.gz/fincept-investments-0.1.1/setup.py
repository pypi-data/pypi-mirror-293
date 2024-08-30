from setuptools import setup, find_packages

# Read the README.md file with utf-8 encoding
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='fincept-investments',
    version='0.1.1',
    author='Fincept Corporation',
    author_email='dev@fincept.in',
    description='A Terminal for Financial Market Analysis and Fetching all kinds of Data.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Fincept-Corporation/fincept-investments',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests',
        'rich',
        'gnews',
        'click',
    ],
    entry_points={
        'console_scripts': [
            'fincept=fincept.cli:cli',  # Point to the cli function, not the start subcommand
        ],
    },
    include_package_data=True,
    package_data={
        '': ['*.txt', '*.md'],
    },
)
