from setuptools import setup, find_packages

setup(
    name='tivwordnet',
    version='0.1.0',
    description='A semantic network for the Tiv language, modeled after WordNet',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Daniel Kumaga',
    author_email='danterkum16@gmail.com',
    url='https://github.com/Dankummzy/tivwordnet',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'tivwordnet': ['data/*.txt'],
    },
    install_requires=[
        ###
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
