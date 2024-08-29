from setuptools import setup, find_packages

setup(
    name='dlph',
    version='0.1.0',
    packages=find_packages(),
    description='Deep Learning Print Helper',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Lihao Wang',
    author_email='lihaowang@yahoo.com',
    url='',
    install_requires=[
        'numpy',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)

