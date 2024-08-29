# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 14:34:55 2024

@author: luca_
"""

import numpy as np 

def prop(array):
    
    '''

    Parameters
    ----------
    array : a np array.

    Returns
    -------
    - array shape
    - array ndim
    - type(array)
    - array.dtype

    '''
    
    print(array)
    print(f'array shape: {array.shape}')
    print(f'array ndim: {array.ndim}')
    print(f'array type: {type(array)}')
    print(f'array dtype: {array.dtype}')
    
    return array.shape, array.ndim, type(array), array.dtype
