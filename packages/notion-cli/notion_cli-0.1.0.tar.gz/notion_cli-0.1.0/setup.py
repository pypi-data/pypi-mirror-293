from setuptools import setup, find_packages

setup(
    name='notion-cli',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'notion-client',
        'click',
        'rich'
    ],
    entry_points={
        'console_scripts': [
            'notion-cli = notion_cli.notion_api:main',  # This creates the CLI command
        ],
    },
    author='Rao Abdul',
    author_email='raoabdulhadi952@gmail.com',
    description='A CLI tool to update Notion tasks utilising the Notion API',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
