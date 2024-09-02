from setuptools import setup, find_packages
setup(
name='dl_multi_class',
version='0.1.1',
author='Sastry K V S R',
author_email='pllsudha@gmail.com',
description='A sample package to create a sample multi class classification model',
packages=find_packages(["tensorflow"]),
package_dir={
        "": ".",
        "tensorflow": "/Users/sudha_sastry/anaconda3/envs/anj/lib/python3.11/site-packages/tensorflow",
    },
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.6',
)
