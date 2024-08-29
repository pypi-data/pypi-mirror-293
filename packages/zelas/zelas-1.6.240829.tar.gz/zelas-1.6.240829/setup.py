import codecs
import os
from setuptools import setup, find_packages


'''
# these things are needed for the README.md show on pypi (if you dont need delete it)
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()
'''
# you need to change all these
VERSION = '1.6.240829'
DESCRIPTION = 'Professor Liying Wang official point clouds algorithm library'
LONG_DESCRIPTION = 'Produced by CCG.Lidar Point Clouds Research Institute'

setup(
    name="zelas",
    version=VERSION,
    author="Ze You, Huaxin Chen, Yimo Geng, Mengyao Gao",
    author_email="youze1997@163.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'point clouds'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.8",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
