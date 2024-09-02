from setuptools import setup, find_packages
setup(
name='dl_multi_class',
version='0.1.7',
author='Sastry K V S R',
author_email='pllsudha@gmail.com',
description='A sample package to create a sample multi class classification model',
packages=find_packages(include=['dl_multi_class', 'dl_multi_class.*']),
install_requires=[
  'tensorflow'
 ],
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.6',
)
