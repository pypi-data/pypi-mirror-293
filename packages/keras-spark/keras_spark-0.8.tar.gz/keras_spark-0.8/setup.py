from setuptools import setup

setup(
   name='keras_spark',
   version='0.8',
   long_description = 'seamless support for spark datasets in keras fit() and .redict()',
   description='seamless support for spark datasets in keras fit() and .redict()',
   author='christian sommeregger',
   author_email='csommeregger@gmail.com',
   packages=["keras_spark"],
   install_requires=['keras','tensorflow','numpy','pandas','pyspark']
)