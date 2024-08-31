from setuptools import setup, find_packages

setup(
    name='mango_test_framework',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'mango_test_framework>=0.1.0'
    ],
    include_package_data=True,
    description='A simple testing framework in Python.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Scott',
    author_email='pessiartist@gmail.com',
    url='https://github.com/najasnake12/mango-test',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
