# -*- coding: utf-8 -*-
from __future__ import print_function

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


class Texture:

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

        # TODO remplacer les [:-1] pour enlever les '\n' par .strip()
        # p = Texture(file)
        # if os.path.splitext(file)[1] == '.gz':
            # f_in = _gz.open(p.filename)
        # else:
            # f_in = open(p.filename)
            # print('b')
        #
        # p.textype = f_in.read(5)
        # if p.textype not in textypes:
            # raise TypeError, "On char 0: Texture type not regular, it should be \'ascii\' or \'binar\'"
        #
        # BINAR
        # if p.textype == textypes[1]:
            # p.byteorder = byteordertypes.get(f_in.read(4))
            # if p.byteorder == None:
                # raise TypeError, 'Dataorder not recognized.'
            # if p.byteorder == byteordertypes.get('ABCD'):
                # raise TypeError, 'Littleindian byteorder not supported yet.'
            #
            # datatypesize = (_np.frombuffer(f_in.read(4),_np.uint32))[0]
            # print('datatypesize', datatypesize)
            # try:
                # datatype     = datatypes[f_in.read(datatypesize)]
                # print('c', datatype)
            # except:
                # raise TypeError, 'Datatype not recognized.'
            #
            # nb_t    = (_np.frombuffer(f_in.read(4), _np.uint32))[0]
            # print('nb_t', nb_t)
            #
            # TODO some sanity check on data length
            # p.data = []
            # for t in range(nb_t):
                # current_t = (_np.frombuffer(f_in.read(4), _np.uint32))[0]
                # print('current_t', current_t)
                # nbitems = (_np.frombuffer(f_in.read(4), _np.uint32))[0]
                # print('nbitems', nbitems)
                # size = nbitems*datatype().nbytes
                # print('size', size)
                # p.data.append(_np.frombuffer(f_in.read(size),datatype))
                # print('d')
        #
        # ASCII
        # else:
            # f_in.readline() #vire le \n de la fin de la premiere ligne
            # p.byteorder = byteordertypes.get('DCBA') # par defaut
            # datatypetemp = f_in.readline()
            # try:
                # datatype = datatypes[datatypetemp[:-1]] #vire le \n a la fin
            # except:
                # raise TypeError, 'Datatype not recognized.'
            #
            # nb_t = _np.int(f_in.readline()[:-1]) # on vire le\n
            # datatemp = _np.fromstring(string=f_in.read().replace('\n',' ').strip(), sep=' ')
            # nb_t = int(datatemp[0])
            # p.data = []
            # pos = 1
            # for t in range(nb_t):
                # current_t = _np.int(datatemp[pos])
                # pos += 1
                # nbitems = _np.int(datatemp[pos])
                # pos += 1
                # p.data.append(_np.array(datatemp[pos:pos+nbitems]))
                # pos += nbitems
        #
        # p.data = _np.array(p.data, dtype=datatype)
        # p.data = p.data.squeeze()
        # f_in.close()
        # return p

    def write(self, filename=None):
        if filename == None:
            filename = self.filename
        # anatomist desn't currently reaf float64 textrues :
        # FIXME after it is allowed in Anatomist...
        if self.data.dtype == _np.float64:
            self.data = self.data.astype(_np.float32)
        aims.write(aims.TimeTexture(self.data), filename)
        # car aims n'ouvre pas les float64 :
        # if self.data.dtype == _np.float64:
            # self.data = self.data.astype(_np.float32)
        # try:
            # test = self.data.shape[1]
            # nb_t = _np.uint32(self.data.shape[0])
        # except:
            # nb_t = _np.uint32(1)

        # if filename==None:
            # print('2')
            # filename = self.filename

        # zip = False
        # if os.path.splitext(filename)[1] == '.gz':
            # filename = os.path.splitext(filename)[0]
            # zip = True

        # f_out = open(filename, 'w')

        # si ascii :
        # if self.textype == textypes[0]:
            # f_out.write(self.textype+'\n')
            # f_out.write([k for k, v in datatypes.items()
                         # if v == self.data.dtype][0]+'\n')
            # f_out.write(str(nb_t)+'\n')

            # ecrit les donnees en gerant la dimension t
            # if nb_t>1 :
                # for t in range(nb_t):
                    # e = self.data[t]
                    # f_out.write(str(t)+' '+str(len(e))+' ')
                    # e.tofile(f_out, sep=' ')
                    # f_out.write(' ')
            # else:
                # f_out.write('0 '+str(len(self.data))+' ')
                # self.data.tofile(f_out, sep=' ')
                # f_out.write(' ')

        # si binaire
        # else:
            # print('8')
            # self.convertToBinary()
            # f_out.write(self.textype)
            # print('textype', self.textype)
            # f_out.write([k for k, v in byteordertypes.items()
                         # if v == self.byteorder][0])
            # print('byte orders', self.byteorder)
            # print('datatype.items', datatypes.items()            )
            # datatype = [k for k, v in datatypes.items()
                        # if v == self.data.dtype][0]
            # print('datatype', datatype)
            # datatypesize = _np.uint32(len(datatype))
            # print('datatypesize'; datatypesize)
            # f_out.write(datatypesize.tostring())
            # print('01', datatypesize.tostring())
            # f_out.write(datatype)
            # print('02', datatype)
            # f_out.write(nb_t.tostring())
            # print('03', nb_t.tostring())

            # ecrit les donnees en gerant la dimension t
            # if nb_t==1 :
                # print('9')
                # f_out.write('\x00\x00\x00\x00')
                # f_out.write(_np.uint32(len(self.data)).tostring())
                # f_out.write(self.data.tostring())
                # print('data.tostring', self.data.tostring())
            # else:
                # for t in range(nb_t):
                    # f_out.write(_np.uint32(t).tostring())
                    # e = self.data[t]
                    # f_out.write(_np.uint32(len(e)).tostring())
                    # f_out.write(e.tostring())

        # f_out.close()
        # if zip: # not optimal, should be done directly when writing texture.
            # gzip_file(filename)
            # os.remove(filename)
