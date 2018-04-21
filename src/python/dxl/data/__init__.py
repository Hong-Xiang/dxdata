"""
=====================
Data Analysis Library
=====================

Introduction
============

Module: dxl.data

Data analysis libraries is designed to provide easy to use and reuseable tools
for data analysis, i.e. "data cleaning".

An object oriented warp on data is provided, and valid operations to these data
were implemented as member method. It can be called in syntax like ::

    data = (CSVFile('data.csv')
            .load()
            .map_to(Person)
            .split_by('name')
            .select('Tim'))

By composing reuseable blocks, we are trying to achieve process of "data cleaning"
with following properties (with decreasing priority):

1.  Easy to develop, thus provide useful API and provide more hints by member 
methods.

2.  Reuseability. Try to achieve DRY as much as possible.

3.  Scalable. Able to be running on multiple computers, thus aiming to used in
cloud or through micro service.

4.  Fast.

"""

from .core import *