from setuptools import setup, find_packages

setup(
    name='open-strawberry',
    version='0.1.0',
    description='A Python package named pyminion with internal directory minion',
    author='Your Name',
    author_email='femtowin@gmail.com',
    url='https://github.com/femto/minion',
    package_dir={'': 'src'},  # Specify that packages are under the src directory
    packages=find_packages(where='src'),  # Automatically find packages in the src directory
    install_requires=[
        # Add your dependencies here
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License with good intention limit',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
