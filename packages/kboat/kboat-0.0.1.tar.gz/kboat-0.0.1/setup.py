from setuptools import setup, find_packages

setup(
    name='kboat',
    version='0.0.1',
    description='PYPI tutorial package creation written by TeddyNote',
    author='somsaetnag',
    author_email='somsaetang@naver.com',
    url='https://github.com/somsaetang/kboat',
    install_requires=[],
    packages=find_packages(exclude=[]),
    keywords=['kboat', '경정'],
    python_requires='>=3.10',
    package_data={},
    zip_safe=False,
    classifiers = [
    "Programming Language :: Python :: 3"
]
)