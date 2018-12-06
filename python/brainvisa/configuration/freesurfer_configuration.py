# -*- coding: utf-8 -*-

#  This software and supporting documentation were developed by
#  NeuroSpin and IFR 49
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


'''
@author: Denis Rivière
@organization: U{NeuroSpin<http://www.neurospin.org>} and U{IFR 49<http://www.ifr49.org>}
@license: U{CeCILL version 2<http://www.cecill.info/licences/Licence_CeCILL_V2-en.html>}
'''

from __future__ import print_function

__docformat__ = "epytext en"

import os
import distutils.spawn
from soma.configuration import ConfigurationGroup
from soma.signature.api import Signature, Unicode, FileName, Sequence, Boolean


#Pour initialiser Freesurfer, plusieurs possibiités
# accessible par un raccourcis
# accessible en ligne de commande

#il vaut mieux toujours lancer le script Freesurfer + ligne de commande

#Pour tester et localiser Freesurfer
#utiliser les valeurs données dans les preferences
#si marche ok
#si ca marche pas -> rechecher par le path
#tester dans le path
#retour variable environnement
#si rien de trouvé : rendre les traitement inacessibles


#FreeSurferEnv.csh or FreeSurferEnv.sh

#------------------------------------------------------------------------------
class FreeSurferConfiguration( ConfigurationGroup ):
  label = 'FREESURFER'
  icon = 'freesurfer.png'

  signature = Signature(
    #'check_freesurfer_path', Boolean, dict( defaultValue=True, doc='check where FREESURFER is installed' ),
    'freesurfer_home_path', FileName( directoryOnly=True ), dict( defaultValue='', doc='location of FREESURFER installation directory' ),
    'subjects_dir_path', FileName( directoryOnly=True ), dict( defaultValue='', doc='value of SUBJECTS_DIR variable' ),
    #'executable_freesurfer', FileName, dict( defaultValue='', doc='path of executable' ),
  )



  def _get_freesurfer_home_path( self ):
    #/i2bm/local/x86_64/freesurfer
    #print(" -- Funtion _get_freesurfer_home_path --")
    if not self._freesurfer_home_path : 
      self._freesurfer_home_path = os.getenv( 'FREESURFER_HOME' )
    #print(self._freesurfer_home_path)
    return self._freesurfer_home_path
    
  def _set_freesurfer_home_path( self, value ):
    #/volatile/ALL_DATABASE_BRAINVISA/db_fs_1
    #print(" -- Funtion _set_freesurfer_home_path --")
    #print("VALUE")
    #print(value)
    self._freesurfer_home_path = value
    
  freesurfer_home_path = property(_get_freesurfer_home_path,
                                  _set_freesurfer_home_path)
  
  
  
  
  def _get_subjects_dir_path( self ):
    #print(" -- Function _get_subjects_dir_path --")
    if not self._subjects_dir_path : 
      self._subjects_dir_path = os.getenv( 'SUBJECTS_DIR' )
    #print(self._subjects_dir_path)
    return self._subjects_dir_path
    
  def _set_subjects_dir_path( self, value ):
    #print(" -- Function _set_subjects_dir_path --")
    #print("VALUE")
    #print(value)
    self._subjects_dir_path = value
    
  subjects_dir_path = property( _get_subjects_dir_path, _set_subjects_dir_path )



  #def _get_executable_freesurfer( self ):
    ##print(" -- Function _get_executable_freesurfer --")
    ##print(self._executable_freesurfer)
    #return self._executable_freesurfer
    
  #def _set_executable_freesurfer( self, value ):
    ##print(" -- Function _set_executable_freesurfer --")
    #if not value : 
      #value = distutils.spawn.find_executable("freesurfer")
    ##print(value)
    #self._executable_freesurfer = value
    
  #executable_freesurfer = property( _get_executable_freesurfer, _set_executable_freesurfer )



  def __init__( self, *args, **kwargs ):
    #print(" -- Function __init__ de FreeSurfer ")
    #print(args)
    #print(kwargs)
    self._freesurfer_home_path = None
    self._subjects_dir_path = None
    self._executable_freesurfer = None
    super( FreeSurferConfiguration, self ).__init__( *args, **kwargs )
    
