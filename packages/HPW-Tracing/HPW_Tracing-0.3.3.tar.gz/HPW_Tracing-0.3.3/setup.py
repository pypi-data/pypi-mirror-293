from setuptools import setup, find_packages
import os
with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read the contents of your requirements file
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='HPW_Tracing',
    version='0.3.3',
    packages=find_packages(),
    include_package_data=True,
    package_data={'HPW_Tracing': ['config.py']},
    license='MIT',
    author='Peng Xie',
    author_email= 'xphn1985@gmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
    install_requires=required,
)



