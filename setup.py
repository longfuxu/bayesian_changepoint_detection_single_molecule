#!/usr/bin/env python3
# This repo is modified for single-molecule studies, from original repo from 'http://github.com/hildensia/bayesian_changepoint_detection'. 

from setuptools import setup
import bayesian_changepoint_detection

setup(
    name='ChangePointDetection',
    version=bayesian_changepoint_detection.__version__,
    description='Bayesian changepoint detection algorithms intended for single-molecule stepwise and piecewise datasets',
    author='Longfu Xu',
    author_email='longfu2.xu@gmail.com',
    url='http://github.com/longfuxu/bayesian_changepoint_detection_single_molecule',
    packages=['bayesian_changepoint_detection'],
    install_requires=['scipy', 'numpy', 'decorator'],
    extras_require={
        'dev': ['pytest'],
        'plot': ['matplotlib'],
    }
)
