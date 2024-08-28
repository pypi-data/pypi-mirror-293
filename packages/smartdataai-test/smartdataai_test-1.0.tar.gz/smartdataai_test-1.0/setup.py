from setuptools import setup, find_packages

setup(
    name='smartdataai_test',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'matplotlib',
        'seaborn',
        'scikit-learn',
        'statsmodels',
        'scipy',
        'langchain',
        'langchain-community',
        'langchain-core',
        'langchain-experimental',
        'langchain-openai',
    ],
    include_package_data=True,
    description='A package for SmartData management and operations.',
    author='Talent AI Now',
    author_email='catjohnabc3@gmail.com',
    url='https://github.com/yourusername/smartdataai',  # Update with your repository URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
