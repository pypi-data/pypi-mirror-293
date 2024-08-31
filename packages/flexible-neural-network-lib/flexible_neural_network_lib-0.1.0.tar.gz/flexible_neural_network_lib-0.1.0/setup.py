from setuptools import setup, find_packages

setup(
    name='flexible_neural_network_lib',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy'
    ],
    description='A simple neural network implementation',
    author='Isaac Morrow',
    author_email='isaac@frzbee.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
