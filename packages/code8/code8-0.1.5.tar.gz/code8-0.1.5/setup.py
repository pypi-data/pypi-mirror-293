from setuptools import setup, find_packages

setup(
    name='code8',
    version='0.1.5',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'code8': ['templates/*', 'static/*'],
    },
    install_requires=[
        'Flask',
        'openai',
        'anthropic',
        'argparse',
    ],
    entry_points={
        'console_scripts': [
            'code8=code8.cli:main',
        ],
    },
    author='Naser Jamal',
    author_email='naser.dll@hotmail.com',
    description='a dashboard to use LLMs to directly on your code files, save and load custom profiles with custom prompts and more.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/naserjamal/code8',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)