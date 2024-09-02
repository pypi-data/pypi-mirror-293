from setuptools import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
   name='keras_spark',
   version='0.93',
   long_description=long_description,
   long_description_content_type='text/markdown',
   description='seamless support for spark datasets in keras fit() and .redict()',
   author='christian sommeregger',
   author_email='csommeregger@gmail.com',
   packages=["keras_spark"],
   install_requires=['tensorflow','numpy','pandas','pyspark']
)