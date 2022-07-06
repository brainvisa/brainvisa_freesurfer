# -*- coding: utf-8 -*-
from __future__ import print_function

from __future__ import absolute_import
import os
import numpy as _np
import gzip as _gz
from soma import aims

# from zip import *

__all__ = ['Texture']

textypes = ['ascii', 'binar']

byteordertypes = {'DCBA': 'bigindian',
                  'ABCD': 'littleindian'}

datatypes = {'U8': _np.uint8,
             'S8': _np.int8,
             'U16': _np.uint16,
             'S16': _np.int16,
             'U32': _np.uint32,
             'S32': _np.int32,
             'FLOAT': _np.float32,
             'DOUBLE': _np.float64,
             'CFLOAT': _np.clongfloat,
             'CDOUBLE': _np.clongdouble
             }


class Texture(object):

    def __init__(self, filename, textype='binar',
                 byteorder='bigindian', data=None):
        if data is None:
            data = _np.array([], dtype=_np.float32)
        else:
            self.data = data

        self.filename = filename
        self.textype = textype
        self.byteorder = byteorder

    def show(self):
        print('textype:', self.textype)
        print('byteorder:', self.byteorder)
        print('datatype:', self.data.dtype)
        print('data shape', self.data.shape)

    def copy(self):
        return Texture(filename=self.filename, textype=self.textype,
                       byteorder=self.byteorder,
                       data=_np.array(self.data))

    def convertToBinary(self):
        self.textype = textypes[1]

    def convertToAscii(self):
        self.textype = textypes[0]

    def convertToType(self, t):
        typename = [k for k, v in datatypes.items() if v == t]
        if len(typename) == 0:
            print("not this one")
            return
        self.data = self.data.astype(t)

    @staticmethod
    def read(file):
        p = Texture(file)
        aimstex = aims.read(file)
        p.data = _np.array(aimstex[0], copy=False)
        p.data = p.data.squeeze()  # not needed I think
        return p


    def write(self, filename=None):
        if filename == None:
            filename = self.filename
        # anatomist desn't currently read float64 textrues :
        # FIXME after it is allowed in Anatomist...
        if self.data.dtype == _np.float64:
            self.data = self.data.astype(_np.float32)
        aims.write(aims.TimeTexture(self.data), filename)
