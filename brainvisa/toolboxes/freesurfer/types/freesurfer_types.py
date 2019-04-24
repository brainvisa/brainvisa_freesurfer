# -*- coding: utf-8 -*-
# Copyright CEA and IFR 49 (2000-2005)
#
#  This software and supporting documentation were developed by
#      CEA/DSV/SHFJ and IFR 49
#      4 place du General Leclerc
#      91401 Orsay cedex
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

include('builtin')
include('snapshots')

from brainvisa.tools import aimsGlobals

Format( 'FreesurferPial', "f|*.pial" )
Format( 'FreesurferWhite', "f|*.white" )
Format( 'FreesurferSphereReg', "f|*.sphere.reg" )
Format( 'FreesurferThickness', "f|*.thickness" )
Format( 'FreesurferCurv', "f|*.curv" )
Format( 'FreesurferAvgCurv', "f|*.avg_curv" )
Format( 'FreesurferCurvPial', "f|*.curv.pial" )
Format( 'FreesurferParcellation', "f|*.annot")
#Format( 'FreesurferMGZ', "f|*.mgz")
Format( 'FreesurferIsin', "f|*.isin")
Format( 'FreesurferLabel', "f|*.label")

FileType( 'FreesurferType', 'Any Type')
FileType( 'FreesurferMesh', 'Mesh')
#FileType( 'FreesurferAnaT', 'FreesurferMGZ')

# Group
FileType( 'Freesurfer Group definition', 'Group definition', 'XML')
FileType( 'AimsWhite', 'White Mesh')
FileType( 'AverageBrainWhite', 'AimsWhite')
FileType( 'BothAverageBrainWhite', 'AverageBrainWhite')


# Mri / Orig
FileType( 'FreesurferAnat', 'T1 MRI', aimsGlobals.aimsVolumeFormats + [ 'FreesurferMGZ' ] )
FileType( 'RawFreesurferAnat', 'FreesurferAnat' )


#Mri
FileType('T1 FreesurferAnat', 'FreesurferAnat')
FileType('Nu FreesurferAnat', 'T1 FreesurferAnat')
FileType('Freesurfer Brain Mask',
         'Label volume',
         aimsGlobals.aimsVolumeFormats + [ 'FreesurferMGZ' ])
FileType('Ribbon Freesurfer',
         'Label volume',
         aimsGlobals.aimsVolumeFormats + [ 'FreesurferMGZ' ])
FileType('Freesurfer aseg',
         'Label volume',
         aimsGlobals.aimsVolumeFormats + [ 'FreesurferMGZ' ])
FileType('Freesurfer Cortical Parcellation',
         'Label volume',
         aimsGlobals.aimsVolumeFormats + [ 'FreesurferMGZ' ])
#FileType('Freesurfer Cortical Parcellation using Destrieux Atlas',
         #'Label volume',
         #aimsGlobals.aimsVolumeFormats + [ 'FreesurferMGZ' ])

#mri / transforms
FileType('Talairach Auto Freesurfer', 'MINC transformation matrix')
FileType('Referential of Raw T1 MRI', 'Referential')
FileType('Referential of Pial', 'Referential')
FileType('Freesurfer Anat To Meshes Transformation', 'Transformation')
FileType('Freesurfer Scanner To MNI Transformation', 'Transformation')

# Surf
FileType( 'SphereReg', 'FreesurferMesh')
FileType( 'BaseFreesurferType', 'FreesurferType')
FileType( 'Pial', 'FreesurferMesh')
FileType( 'White', 'White Mesh')
FileType( 'ResampledPial', 'FreesurferMesh')
FileType( 'ResampledWhite', 'White Mesh')
FileType( 'AimsPial', 'FreesurferMesh')
FileType( 'AimsNativePial', 'FreesurferMesh')
FileType( 'AimsNativeWhite', 'FreesurferMesh')
FileType( 'AimsNormalizedWhite', 'FreesurferMesh')
FileType( 'AimsInflatedWhite', 'AimsWhite')
FileType( 'DataTexture', 'Texture')
FileType( 'FreesurferAvgCurvType', 'DataTexture')
FileType( 'FreesurferCurvPialType', 'DataTexture')
FileType( 'FreesurferCurvType', 'DataTexture')
FileType( 'ResampledDataTexture', 'DataTexture')
FileType( 'AimsInflatedWhiteCurvTex', 'ResampledDataTexture')
FileType( 'FreesurferThicknessType', 'DataTexture')
FileType( 'ResampledFreesurferAvgCurvType', 'ResampledDataTexture')
FileType( 'ResampledFreesurferCurvPialType', 'ResampledDataTexture')
FileType( 'ResampledFreesurferCurvType', 'ResampledDataTexture')
FileType( 'ResampledFreesurferThicknessType', 'ResampledDataTexture')
#
FileType( 'AimsBothWhite', 'AimsWhite')
FileType( 'AimsBothPial', 'FreesurferMesh')
FileType( 'AimsBothInflatedWhite', 'AimsInflatedWhite')

# Label
FileType( 'FreesurferParcellationPath', 'FreesurferType')
FileType( 'FreesurferGyriTexture', 'ROI Texture', ['FreesurferParcellation'])
FileType( 'FreesurferSulciGyriTexture', 'ROI Texture',
         ['FreesurferParcellation'])
FileType( 'FreesurferReadableGyriTexture', 'FreesurferType')
FileType( 'FreesurferReadableSulciGyriTexture', 'FreesurferType')
FileType( 'FreesurferParcellationType', 'ROI Texture')
FileType( 'FreesurferResampledParcellationType', 'ROI Texture')
FileType( 'FreesurferGyri', 'FreesurferParcellationType')
FileType( 'FreesurferSulciGyri', 'FreesurferParcellationType')
FileType( 'ResampledGyri', 'FreesurferResampledParcellationType')
FileType( 'ResampledSulciGyri', 'FreesurferResampledParcellationType')

#
FileType( 'FreesurferResampledBothParcellationType', 'ROI Texture')
FileType( 'BothResampledGyri', 'ResampledGyri')
FileType( 'BothResampledSulciGyri', 'ResampledSulciGyri')
FileType( 'BothAverageResampledGyri', 'ResampledGyri' )
