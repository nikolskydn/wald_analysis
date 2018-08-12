#!/usr/bin/python3
from setuptools import setup

setup(name='wald_analysis', version='0.0.0', 
      packages=['wald_analysis'],
      description='Module performs a sequential analysis of Wald.',
      author='Nikolskii D. N.', author_email='nikolskydn@mail.ru',
      entry_points={'console_scripts': 
          ['wald_analyze_statistic=wald_analysis.analyze:main',
           'wald_draw_statistic=wald_analysis.draw_statistic:main',
           'wald_make_statistic=wald_analysis.make_statistic:main']},
)

