from setuptools import setup, find_packages

setup(
    name='meta_cleaner',
    version='0.4.2',
    description='A Python package to clean text from META tags using a BERT large Longformer NER model.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Tim Isbister',
    author_email='tim.isbister@pirr.me',
    url='https://github.com/pirr-me/meta_cleaner',
    packages=find_packages(),
    install_requires=[
        'torch>=2.0.0',
        'transformers>=4.0.0',
        'tqdm>=4.0',
        'langdetect>=1.0.8'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
