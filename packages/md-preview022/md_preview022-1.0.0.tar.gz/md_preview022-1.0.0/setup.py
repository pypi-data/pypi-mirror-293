from setuptools import setup, find_packages

setup(
    name='md_preview022',
    version='1.0.0',
    author='Akash Verma',
    author_email='ahmvaad@gmail.com',
    description='A simple Markdown preview tool for the terminal.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/akaashvaa/preview_md_file',
    packages=find_packages(),
    install_requires=[
        'markdown',
        'rich',
    ],
    entry_points={
        'console_scripts': [
            'mdm=mdm.mdm:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

