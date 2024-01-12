#! /usr/bin/env python

from soma import aims
from .tio import Texture


def giftiToTex(filename, output):
    g = aims.read(filename)
    t = Texture(filename=output, data=g[0].np)
    t.write()
