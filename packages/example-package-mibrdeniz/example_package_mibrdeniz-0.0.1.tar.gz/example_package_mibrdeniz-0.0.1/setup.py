from setuptools import setup, find_packages

setup(
    name='example_package_mibrdeniz',
    version='0.0.1',
    description='This package is to test if it is success or not.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Mahmut İbrahim DENİZ',
    author_email='mdeniz20@ku.edu.tr',
    url='https://github.com/mdeniz20/example_package.git',
    packages=find_packages(),
    install_requires=[
        # List your package dependencies here
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

