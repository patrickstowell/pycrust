from setuptools import setup, find_packages

setup(
    name='pycrust',
    version='0.1.0',
    author='Patrick Stowell',
    author_email='p.stowell@sheffield.ac.uk',
    description='Geometry helper tools and examples using g4ppyy',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/patrikstowell/G4ppyy',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
    install_requires=[
        'g4ppyy',
    ],
)

