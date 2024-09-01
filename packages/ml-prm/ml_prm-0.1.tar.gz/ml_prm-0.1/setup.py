from setuptools import setup, find_packages

setup(
    name='ml_prm',
    version='0.1',
    description='A Python package for machine learning projects including model training and evaluation.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Arasu',
    author_email='arasu6262@gmail.com',
    packages=find_packages(),
    install_requires=[
        'scikit-learn>=0.24',
        'numpy>=1.21',
        'scipy>=1.7'
    ],
    extras_require={
        'excel': [
            'openpyxl',
            'pandas'
        ],
        'dev': [
            'pytest',
            'black',
            'flake8',
        ],
    },
    entry_points={
        'console_scripts': [
            'ml-prm = ml_prm.cli:main'
        ]
    },
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
)
