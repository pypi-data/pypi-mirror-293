from setuptools import setup, find_packages

setup(
    name='yellowwavesttt',  # Nom du package
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'yellowwavesttt=yellowwavesttt.__init__:main',  # Mise à jour ici
        ],
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='A simple hello world package',
    long_description='This is a simple hello world package that prints "Hello, World!" when run from the command line.',
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/yellowwavestest',  # Mettez à jour votre URL si nécessaire
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
