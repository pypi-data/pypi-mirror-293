from itertools import chain

from setuptools import find_packages, setup
from Cython.Build import cythonize
import numpy as np

REPO_URL = "https://github.com/neuralmmo/environment"

extra = {
    'docs': [
        'sphinx==5.0.0',
        'sphinx-rtd-theme==0.5.1',
        'sphinxcontrib-youtube==1.0.1',
        'myst-parser==1.0.0',
        'sphinx-rtd-theme==0.5.1',
        'sphinx-design==0.4.1',
        'furo==2023.3.27',
    ],
}

extra['all'] = list(set(chain.from_iterable(extra.values())))

with open('nmmo/version.py', encoding="utf-8") as vf:
  ver = vf.read().split()[-1].strip("'")

setup(
  name="nmmo",
  description="Neural MMO is a platform for multiagent intelligence research " + \
              "inspired by Massively Multiplayer Online (MMO) role-playing games. " + \
              "Documentation hosted at neuralmmo.github.io.",
  long_description_content_type="text/markdown",
  version=ver,
  packages=find_packages(),
  include_package_data=True,
  install_requires=[
    'cython>=3.0.0',
    'numpy==1.23.3',
    'scipy==1.10.0',
    'pytest==7.3.0',
    'pytest-benchmark==3.4.1',
    'imageio>=2.27',
    'ordered-set==4.1.0',
    'pettingzoo==1.24.1',
    'gymnasium==0.29.1',
    'pylint==2.16.0',
    'psutil<6',
    'tqdm<5',
    'py==1.11.0',
    'dill<0.4',
  ],
  ext_modules = cythonize(["nmmo/lib/cython_helper.pyx"]),
  include_dirs=[np.get_include()],
  extras_require=extra,
  python_requires=">=3.7,<3.11",
  license="MIT",
  author="Joseph Suarez",
  author_email="jsuarez@mit.edu",
  url=REPO_URL,
  keywords=["Neural MMO", "MMO"],
  classifiers=[
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Science/Research",
    "Intended Audience :: Developers",
    "Environment :: Console",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
  ],
)
