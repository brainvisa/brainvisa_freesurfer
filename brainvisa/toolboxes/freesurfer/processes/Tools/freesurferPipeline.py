# -*- coding: utf-8 -*-
from __future__ import absolute_import
from brainvisa.processes import *

from freesurfer.brainvisaFreesurfer \
    import launchFreesurferCommand, testFreesurferCommand

name = "02 Launch Freesurfer full pipeline recon-all"
userLevel = 1


def validation():
    """
    """
    testFreesurferCommand()


signature = Signature(
    'AnatImage', ReadDiskItem('RawFreesurferAnat', 'FreesurferMGZ'),
    'database', ReadDiskItem('Directory', 'Directory'),
    'subject', String(),
    'force_fov_to_256', Boolean(),
    'qcache_for_group_analysis', Boolean(),
    'add_other_options', String(),

    # liens non visible
    'nu', WriteDiskItem('Nu FreesurferAnat',
                        'FreesurferMGZ'),
    'ribbon', WriteDiskItem('Ribbon Freesurfer',
                            'FreesurferMGZ',
                            requiredAttributes={'side': 'both',
                                                'space': 'freesurfer analysis'}),

    'leftPial', WriteDiskItem('BaseFreesurferType',
                              'FreesurferPial',
                              requiredAttributes={'side': 'left'}),
    'leftWhite', WriteDiskItem('BaseFreesurferType',
                               'FreesurferWhite',
                               requiredAttributes={'side': 'left'}),
    'leftSphereReg', WriteDiskItem('BaseFreesurferType',
                                   'FreesurferSphereReg',
                                   requiredAttributes={'side': 'left'}),
    'leftThickness', WriteDiskItem('BaseFreesurferType',
                                   'FreesurferThickness',
                                   requiredAttributes={'side': 'left'}),
    'leftCurv', WriteDiskItem('BaseFreesurferType',
                              'FreesurferCurv',
                              requiredAttributes={'side': 'left'}),
    'leftAvgCurv', WriteDiskItem('BaseFreesurferType',
                                 'FreesurferAvgCurv',
                                 requiredAttributes={'side': 'left'}),
    'leftCurvPial', WriteDiskItem('BaseFreesurferType',
                                  'FreesurferCurvPial',
                                  requiredAttributes={'side': 'left'}),
    'leftGyri', WriteDiskItem('FreesurferGyriTexture',
                              'FreesurferParcellation',
                              requiredAttributes={'side': 'left'}),
    'leftSulciGyri', WriteDiskItem('FreesurferSulciGyriTexture',
                                   'FreesurferParcellation',
                                   requiredAttributes={'side': 'left'}),

    'rightPial', WriteDiskItem('BaseFreesurferType',
                               'FreesurferPial',
                               requiredAttributes={'side': 'right'}),
    'rightWhite', WriteDiskItem('BaseFreesurferType',
                                'FreesurferWhite',
                                requiredAttributes={'side': 'right'}),
    'rightSphereReg', WriteDiskItem('BaseFreesurferType',
                                    'FreesurferSphereReg',
                                    requiredAttributes={'side': 'right'}),
    'rightThickness', WriteDiskItem('BaseFreesurferType',
                                    'FreesurferThickness',
                                    requiredAttributes={'side': 'right'}),
    'rightCurv', WriteDiskItem('BaseFreesurferType',
                               'FreesurferCurv',
                               requiredAttributes={'side': 'right'}),
    'rightAvgCurv', WriteDiskItem('BaseFreesurferType',
                                  'FreesurferAvgCurv',
                                  requiredAttributes={'side': 'right'}),
    'rightCurvPial', WriteDiskItem('BaseFreesurferType',
                                   'FreesurferCurvPial',
                                   requiredAttributes={'side': 'right'}),
    'rightGyri', WriteDiskItem('FreesurferGyriTexture',
                               'FreesurferParcellation',
                               requiredAttributes={'side': 'right'}),
    'rightSulciGyri', WriteDiskItem('FreesurferSulciGyriTexture',
                                    'FreesurferParcellation',
                                    requiredAttributes={'side': 'right'}),
)


def initialization(self):
    """
    """

    def linkDB(self, dummy):
        if self.AnatImage:
            return self.AnatImage.get('_database')

    def linkSubject(self, dummy):
        if self.AnatImage:
            return self.AnatImage.get('subject')

    self.setOptional('add_other_options')
    self.force_fov_to_256 = False
    self.qcache_for_group_analysis = False
    self.linkParameters('database', 'AnatImage', linkDB)
    self.linkParameters('subject', 'AnatImage', linkSubject)
    self.signature['database'].userLevel = 2
    self.signature['subject'].userLevel = 2

    self.linkParameters('nu', 'AnatImage')
    self.linkParameters('ribbon', 'AnatImage')

    self.linkParameters('leftPial', 'AnatImage')
    self.linkParameters('leftWhite', 'AnatImage')
    self.linkParameters('leftSphereReg', 'AnatImage')
    self.linkParameters('leftThickness', 'AnatImage')
    self.linkParameters('leftCurv', 'AnatImage')
    self.linkParameters('leftAvgCurv', 'AnatImage')
    self.linkParameters('leftCurvPial', 'AnatImage')
    self.linkParameters('leftGyri', 'AnatImage')
    self.linkParameters('leftSulciGyri', 'AnatImage')

    self.linkParameters('rightPial', 'AnatImage')
    self.linkParameters('rightWhite', 'AnatImage')
    self.linkParameters('rightSphereReg', 'AnatImage')
    self.linkParameters('rightThickness', 'AnatImage')
    self.linkParameters('rightCurv', 'AnatImage')
    self.linkParameters('rightAvgCurv', 'AnatImage')
    self.linkParameters('rightCurvPial', 'AnatImage')
    self.linkParameters('rightGyri', 'AnatImage')
    self.linkParameters('rightSulciGyri', 'AnatImage')

    self.signature['nu'].userLevel = 3
    self.signature['ribbon'].userLevel = 3

    self.signature['leftPial'].userLevel = 3
    self.signature['leftWhite'].userLevel = 3
    self.signature['leftSphereReg'].userLevel = 3
    self.signature['leftThickness'].userLevel = 3
    self.signature['leftCurv'].userLevel = 3
    self.signature['leftAvgCurv'].userLevel = 3
    self.signature['leftCurvPial'].userLevel = 3
    self.signature['leftGyri'].userLevel = 3
    self.signature['leftSulciGyri'].userLevel = 3

    self.signature['rightPial'].userLevel = 3
    self.signature['rightWhite'].userLevel = 3
    self.signature['rightSphereReg'].userLevel = 3
    self.signature['rightThickness'].userLevel = 3
    self.signature['rightCurv'].userLevel = 3
    self.signature['rightAvgCurv'].userLevel = 3
    self.signature['rightCurvPial'].userLevel = 3
    self.signature['rightGyri'].userLevel = 3
    self.signature['rightSulciGyri'].userLevel = 3


def execution(self, context):
    """
    """
    subject = self.subject
    if subject is None:
        subject = os.path.basename(
            os.path.dirname(
                os.path.dirname(os.path.dirname(self.AnatImage.fullPath()))))
    context.write('Launch the Freesurfer pipeline on subject ' + subject)
    database = self.database
    if not database:
        database = os.path.dirname(
            os.path.dirname(
                os.path.dirname(os.path.dirname(self.AnatImage.fullPath()))))
    else:
        database = database.fullPath()

    context.write('recon-all -autorecon-all -subjid %s' % subject)

    # launchFreesurferCommand(context, database, args)
    kwargs = {}
    args = ['recon-all', '-autorecon-all', '-subjid', subject]
    if self.force_fov_to_256:
        args.append('-cw256')
    if self.qcache_for_group_analysis:
        args.append('-qcache')
    if self.add_other_options is not None:
        liste_option = self.add_other_options.split()
        for option in liste_option:
            args.append(option)

    launchFreesurferCommand(context, database, *args, **kwargs)

    neuroHierarchy.databases.update([os.path.join(database, subject)])
