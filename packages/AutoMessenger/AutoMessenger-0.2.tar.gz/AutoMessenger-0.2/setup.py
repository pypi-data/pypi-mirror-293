# setup.py
from setuptools import setup, find_packages

setup(
    name='AutoMessenger',  # The name of your package on PyPI
    version='0.2',         # The initial release version
    description='A Python package to send automated messages using pyautogui',
    long_description=open('README.md').read(),  # Project description from README
    long_description_content_type='text/markdown',
    url='https://github.com/imzulkar/automessnger',  
    author='GM Zulkar Nine',
    author_email='gmzulkar@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'pyautogui',  # Add external dependencies
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify the minimum Python version
)
