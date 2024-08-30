from setuptools import setup, find_packages

setup(
    name='Linkify-Linkedlist',  # Library name
    version='0.1.1',  # Initial version
    description='A Python library to convert arrays to linked lists',  # Short description
    long_description=open('README.md').read(),  # Long description from README.md
    long_description_content_type='text/markdown',  # Format of long description
    author='Shankhosuvro Ghosh',  # Your name
    author_email='shankhosuvro.ghosh@gmail.com',  # Your email
    url='https://github.com/Shankhosuvro-G/linkify',  # URL to the project (replace with your URL)
    packages=find_packages(),  # Automatically find and include all packages
    install_requires=[],  # List of dependencies (empty if none)
    tests_require=['unittest'],  # Dependencies required for running tests
    python_requires='>=3.6',  # Minimum Python version required
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
