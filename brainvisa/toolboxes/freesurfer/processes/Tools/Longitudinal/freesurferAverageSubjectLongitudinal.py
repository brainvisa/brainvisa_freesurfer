# -*- coding: utf-8 -*-
from __future__ import print_function

from __future__ import absolute_import
from brainvisa.processes import *
from freesurfer.brainvisaFreesurfer \
    import launchFreesurferCommand, testFreesurferCommand
from six.moves import range


name = "Average Subject Longitudinal Pipeline"
userLevel = 3


def validation():
    testFreesurferCommand()


signature = Signature(
    'number_of_time_point', Choice(1, 2, 3, 4, 5),
    'anat_tp1', ReadDiskItem(
        'RawFreesurferAnat',
        'FreesurferMGZ'),
    'subject_tp1', String(),
    'anat_tp2', ReadDiskItem(
        'RawFreesurferAnat',
        'FreesurferMGZ'),
    'subject_tp2', String(),
    'anat_tp3', ReadDiskItem(
        'RawFreesurferAnat',
        'FreesurferMGZ'),
    'subject_tp3', String(),
    'anat_tp4', ReadDiskItem(
        'RawFreesurferAnat',
        'FreesurferMGZ'),
    'subject_tp4', String(),
    'anat_tp5', ReadDiskItem(
        'RawFreesurferAnat',
        'FreesurferMGZ'),
    'subject_tp5', String(),
    'database', ReadDiskItem('Directory', 'Directory'),
    'template_name', String(),
    'template_anat', WriteDiskItem(
        'RawFreesurferAnat',
        'FreesurferMGZ'),
    'add_options', String(),

    # liens non visible:
    #'leftPial', WriteDiskItem('BaseFreesurferType',
                              #'FreesurferPial',
                              # requiredAttributes = {'side': 'left'}),
    #'leftWhite', WriteDiskItem('BaseFreesurferType',
                               #'FreesurferWhite',
                               # requiredAttributes = {'side': 'left'}),
    #'leftSphereReg', WriteDiskItem('BaseFreesurferType',
                                   #'FreesurferSphereReg',
                                   # requiredAttributes = {'side': 'left'}),
    #'leftThickness', WriteDiskItem('BaseFreesurferType',
                                   #'FreesurferThickness',
                                   # requiredAttributes = {'side': 'left'}),
    #'leftCurv', WriteDiskItem('BaseFreesurferType',
                              #'FreesurferCurv',
                              # requiredAttributes = {'side': 'left'}),
    #'leftAvgCurv', WriteDiskItem('BaseFreesurferType',
                                 #'FreesurferAvgCurv',
                                 # requiredAttributes = {'side': 'left'}),
    #'leftCurvPial', WriteDiskItem('BaseFreesurferType',
                                  #'FreesurferCurvPial',
                                  # requiredAttributes = {'side': 'left'}),
    #'leftGyri', WriteDiskItem('FreesurferGyriTexture',
                              #'FreesurferParcellation',
                              # requiredAttributes = {'side': 'left'}),
    #'leftSulciGyri', WriteDiskItem('FreesurferSulciGyriTexture',
                                   #'FreesurferParcellation',
                                   # requiredAttributes = {'side': 'left'}),
    #'rightPial', WriteDiskItem('BaseFreesurferType',
                               #'FreesurferPial',
                               # requiredAttributes = {'side': 'right'}),
    #'rightWhite', WriteDiskItem('BaseFreesurferType',
                                #'FreesurferWhite',
                                # requiredAttributes = {'side': 'right'}),
    #'rightSphereReg', WriteDiskItem('BaseFreesurferType',
                                    #'FreesurferSphereReg',
                                    # requiredAttributes = {'side': 'right'}),
    #'rightThickness', WriteDiskItem('BaseFreesurferType',
                                    #'FreesurferThickness',
                                    # requiredAttributes = {'side': 'right'}),
    #'rightCurv', WriteDiskItem('BaseFreesurferType',
                               #'FreesurferCurv',
                               # requiredAttributes = {'side': 'right'}),
    #'rightAvgCurv', WriteDiskItem('BaseFreesurferType',
                                  #'FreesurferAvgCurv',
                                  # requiredAttributes = {'side': 'right'}),
    #'rightCurvPial', WriteDiskItem('BaseFreesurferType',
                                   #'FreesurferCurvPial',
                                   # requiredAttributes = {'side': 'right'}),
    #'rightGyri', WriteDiskItem('FreesurferGyriTexture',
                               #'FreesurferParcellation',
                               # requiredAttributes = {'side': 'right'}),
    #'rightSulciGyri', WriteDiskItem('FreesurferSulciGyriTexture',
                                    #'FreesurferParcellation',
                                    # requiredAttributes = {'side': 'right'}),
)


# def buildNewSignature(self, number):
    # signature_params = ['number_of_time_point', Choice(1, 2, 3, 4, 5)]
    # for i in range(number):
        # signature_params += ['anat_tp'+str(i+1),
                             # ReadDiskItem('RawFreesurferAnat',
                                          #'FreesurferMGZ'),
                             #'subject_tp'+str(i+1), String()]
    # signature_params += [
        #'database', ReadDiskItem('Directory', 'Directory'),
        #'template_name', String(),
        #'template_anat', WriteDiskItem(
            #'RawFreesurferAnat',
            #'FreesurferMGZ'),
        #'add_options', String()]

    # signature = Signature(*signature_params)
    # self.changeSignature(signature)

def updateSignature(self, number):
    for i in range(2, 6):
        if i <= number:
            self.setEnable('anat_tp' + str(i))
            self.setEnable('subject_tp' + str(i))
        else:
            self.setDisable('anat_tp' + str(i))
            self.setDisable('subject_tp' + str(i))
    self.changeSignature(self.signature)


def initialization(self):

    def linkDB(proc, dummy):
        databases = []
        for i in range(self.number_of_time_point):
            anat = self.__dict__['anat_tp' + str(i + 1)]
            if anat is not None:
                databases.append(anat.get('_database'))
        if len(databases) == self.number_of_time_point:
            if all(x == databases[0] for x in databases):
                return databases[0]
            else:
                # context.Error('Anat images were selected from different
                # databases')
                print('Anat images were selected from different databases')

    def linkSubjectName(param, proc, dummy):
        if self.__dict__[param] is not None:
            subject = self.__dict__[param].get('subject')
            return subject

    def linkTemplateName(proc, dummy):
        subjects = []
        tp = []
        for i in range(self.number_of_time_point):
            sub = self.__dict__['subject_tp' + str(i + 1)]
            if sub is not None:
                subjects.append(sub.split('_')[0])
                tp.append(sub.split('_')[1])
        if len(subjects) == self.number_of_time_point:
            if len(set(subjects)) == 1:
                subject_ave = list(set(subjects))[
                    0] + '_avgtemplate_' + '_'.join(tp)
                return subject_ave
            else:
                # context.Error('Error in subject name')
                print('Error in subject name')

    def linkAnatTemplatePath(proc, dummy):
        if self.template_name is not None and self.database is not None:
            dirname = self.database.fullPath()
            filepath = os.path.join(dirname,
                                    self.template_name,
                                    'mri/orig/001.mgz')
            return filepath

    self.addLink(None, 'number_of_time_point', self.updateSignature)

    for i in range(1, 6):
        self.linkParameters('subject_tp' + str(i), 'anat_tp' + str(i),
                            partial(linkSubjectName,
                                    'anat_tp' + str(i)))
    self.linkParameters('database',
                        ('anat_tp1', 'anat_tp2', 'anat_tp3',
                         'anat_tp4', 'anat_tp5'),
                        linkDB)
    self.linkParameters('template_name',
                        ('subject_tp1', 'subject_tp2', 'subject_tp3',
                         'subject_tp4', 'subject_tp5'),
                        linkTemplateName)
    self.linkParameters('template_anat',
                        ('template_name', 'database'),
                        linkAnatTemplatePath)

    self.number_of_time_point = 2
    self.setOptional('add_options')

    # self.linkParameters('leftPial', 'templateAnatImage')
    # self.linkParameters('leftWhite', 'templateAnatImage')
    # self.linkParameters('leftSphereReg', 'templateAnatImage')
    # self.linkParameters('leftThickness', 'templateAnatImage')
    # self.linkParameters('leftCurv', 'templateAnatImage')
    # self.linkParameters('leftAvgCurv', 'templateAnatImage')
    # self.linkParameters('leftCurvPial', 'templateAnatImage')
    # self.linkParameters('leftGyri', 'templateAnatImage')
    # self.linkParameters('leftSulciGyri', 'templateAnatImage')
    # self.linkParameters('rightPial', 'templateAnatImage')
    # self.linkParameters('rightWhite', 'templateAnatImage')
    # self.linkParameters('rightSphereReg', 'templateAnatImage')
    # self.linkParameters('rightThickness', 'templateAnatImage')
    # self.linkParameters('rightCurv', 'templateAnatImage')
    # self.linkParameters('rightAvgCurv', 'templateAnatImage')
    # self.linkParameters('rightCurvPial', 'templateAnatImage')
    # self.linkParameters('rightGyri', 'templateAnatImage')
    # self.linkParameters('rightSulciGyri', 'templateAnatImage')

    # self.signature['leftPial'].userLevel = 3
    # self.signature['leftWhite'].userLevel = 3
    # self.signature['leftSphereReg'].userLevel = 3
    # self.signature['leftThickness'].userLevel = 3
    # self.signature['leftCurv'].userLevel = 3
    # self.signature['leftAvgCurv'].userLevel = 3
    # self.signature['leftCurvPial'].userLevel = 3
    # self.signature['leftGyri'].userLevel = 3
    # self.signature['leftSulciGyri'].userLevel = 3
    # self.signature['rightPial'].userLevel = 3
    # self.signature['rightWhite'].userLevel = 3
    # self.signature['rightSphereReg'].userLevel = 3
    # self.signature['rightThickness'].userLevel = 3
    # self.signature['rightCurv'].userLevel = 3
    # self.signature['rightAvgCurv'].userLevel = 3
    # self.signature['rightCurvPial'].userLevel = 3
    # self.signature['rightGyri'].userLevel = 3
    # self.signature['rightSulciGyri'].userLevel = 3

    # self.signature['subject_tp1'].userLevel = 3
    # self.signature['subject_tp2'].userLevel = 3
    # self.signature['database'].userLevel = 3


def execution(self, context):
    # subject_tp1 = self.subject_tp1 #AnatImageTimepoint1.get('subject')
    # if subject_tp1 is None:
        # subject_tp1 = os.path.basename( os.path.dirname( os.path.dirname( os.path.dirname( self.AnatImageTimepoint1.fullPath() ) ) ) )
    # subject_tp2 = self.subject_tp2 #AnatImageTimepoint1.get('subject')
    # if subject_tp2 is None:
        # subject_tp2 = os.path.basename( os.path.dirname( os.path.dirname(
        # os.path.dirname( self.AnatImageTimepoint2.fullPath() ) ) ) )

    # subject_ave = self.template_name #templateAnatImage.get('subject')

    if not self.database:
        database = os.path.dirname(
            os.path.dirname(
                os.path.dirname(os.path.dirname(self.template_anat.fullPath()))))
    else:
        database = self.database.fullPath()

    kwargs = {}
    args = ['recon-all', '-base', self.template_name]
    for i in range(self.number_of_time_point):
        args.append('-tp')
        sub = 'subject_tp' + str(i + 1)
        args.append(self.__dict__[sub])
    args.append('-all')

    if self.add_options is not None:
        liste_option = string.split(self.add_options)
        for option in liste_option:
            args.append(option)

    context.write('Create the freesurfer average template from time points')
    # context.write('recon-all -base %s -tp %s -tp %s
    # -all'%(self.template_name, self.subject_tp1, self.subject_tp2))
    context.write(args)
    launchFreesurferCommand(context, database, *args, **kwargs)

    # neuroHierarchy.databases.update([os.path.join(self.database,
    # self.template_name)])
