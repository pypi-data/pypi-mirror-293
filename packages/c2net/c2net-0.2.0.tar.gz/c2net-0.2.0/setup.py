# python setup.py sdist bdist_wheel
# twine upload dist/*
# twine upload --repository testpypi dist/*
# pip install -i https://test.pypi.org/pypi/ --extra-index-url https://pypi.org/simple <your_package_in_testpypi>

from setuptools import find_packages, setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="c2net",
    version="0.2.0",
    description="A package for c2net pypi",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://openi.pcl.ac.cn/OpenIOSSG/c2net-pypi',
    author='liuzx',
    author_email='gsunfeng@163.com',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Operating System :: OS Independent',
    ],
)