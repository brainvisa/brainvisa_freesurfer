# -*- coding: utf-8 -*-
#  This software and supporting documentation are distributed by
#      Institut Federatif de Recherche 49
#      CEA/NeuroSpin, Batiment 145,
#      91191 Gif-sur-Yvette cedex
#      France
#
# This software is governed by the CeCILL license version 2 under
# French law and abiding by the rules of distribution of free software.
# You can  use, modify and/or redistribute the software under the
# terms of the CeCILL license version 2 as circulated by CEA, CNRS
# and INRIA at the following URL "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license version 2 and that you accept its terms.

from __future__ import absolute_import
from brainvisa.processes import *
import distutils.spawn
from freesurfer.brainvisaFreesurfer \
    import launchFreesurferCommand, testFreesurferCommand

name = 'FreeSurfer from MGZ Converter'
roles = ('converter',)
userLevel = 0
rolePriority = 2  # set higher priority than aims converter


def validation():
    testFreesurferCommand()

signature = Signature(
    'read', ReadDiskItem('4D Volume', 'FreesurferMGZ', enableConversion=False),
    'write', WriteDiskItem('4D Volume',
                           ['NIFTI-1 image', 'gz compressed NIFTI-1 image']),
)


def initialization(self):
    self.linkParameters('write', 'read')


def execution(self, context):
    # mri_convert will not write a .minf, so we have to take care if it
    # already exists from a previous data
    if os.path.exists(self.write.minfFileName()):
        self.write.clearMinf(saveMinf=True)
    launchFreesurferCommand(context, None, 'mri_convert', self.read,
                            self.write)
    self.write.readAndUpdateMinf()
    self.write.saveMinf()
