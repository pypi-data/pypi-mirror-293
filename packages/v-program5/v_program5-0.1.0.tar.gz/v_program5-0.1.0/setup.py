from setuptools import setup, find_packages

setup(
    name="v-program5",
    version="0.1.0",
    description="A Python package for training and predicting with a neural network using backpropagation.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Arasu",
    author_email="arasu6262@gmail.com",
    packages=find_packages(include=['v_program5', 'v_program5.*']),
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'pandas',
    ],
    extras_require={
        'dev': [
            'pytest',
            'black',
            'flake8',
        ],
    },
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
    entry_points={
    'console_scripts': [
        'v-program5-cli=v_program5.cli:main',
    ],
},
 # Adjust if necessary
        
    
)
