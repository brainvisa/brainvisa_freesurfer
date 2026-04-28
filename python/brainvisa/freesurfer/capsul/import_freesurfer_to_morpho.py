
from capsul.api import Process, get_process_instance
from capsul.attributes.completion_engine import ProcessCompletionEngine
from traits.api import File, Enum, List, Undefined
import os
import os.path as osp
from soma import aims
from soma.qt_gui.qtThread import QtThreadCall
import subprocess
import tempfile


# FIXME
aims_vol_ext = ['.nii.gz', '.svs', '.dcm', '', '.i', '.v', '.fdf',
                '.mgh', '.mgz', '.ima', '.dim', '.ndpi', '.vms', '.vmu',
                '.jpg', '.scn', '.mnc', '.nii', '.img', '.hdr', '.svslide',
                '.tiff', '.tif', '.bif', '.czi', '.mnc.gz']


class ImportFreesurferToMorpho(Process):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_trait('T1_orig', File(allowed_extensions=aims_vol_ext))
        self.add_trait('ribbon_image', File(allowed_extensions=aims_vol_ext))
        self.add_trait('scanner_based_referential',
                       File(allowed_extensions=['.referential'],
                            optional=True))
        self.add_trait('Talairach_Auto', File(allowed_extensions=['.xfm']))
        self.add_trait('T1_output', File(allowed_extensions=aims_vol_ext,
                                         output=True))
        self.add_trait('T1_referential',
                       File(allowed_extensions=['.referential'], output=True))
        self.add_trait('transform_to_scanner_based',
                       File(output=True, optional=True))
        self.add_trait('bias_corrected_output', File(output=True))
        self.add_trait('normalization_transformation', File(output=True))
        self.add_trait('talairach_transform', File(output=True))
        self.add_trait('commissure_coordinates', File(output=True))
        self.add_trait('histo_analysis', File(output=True))
        self.add_trait('brain_mask_output', File(output=True))
        self.add_trait('split_brain_output', File(output=True))
        self.add_trait('left_grey_white_output', File(output=True))
        self.add_trait('right_grey_white_output', File(output=True))
        # self.add_trait('use_morphologist',
        #                Enum(['graphically', 'batch', 'none']))
        self.add_trait('mni_referential', File())
        self.add_trait('transform_chain_ACPC_to_Normalized', File())
        self.add_trait('acpc_referential', File())
        # self.add_trait('allow_multithreading', Bool())
        # self.add_trait('perform_morpho_report', Bool())

        # self.allow_multithreading = True
        # self.perform_morpho_report = True

    def _run_process(self):
        temps = []
        try:
            self.run_process_func(temps)
        finally:
            self.remove_temp(temps)

    def run_process_func(self, temps):

        # Import Data
        import_p = get_process_instance('morphologist.capsul.import_t1_mri')
        print("Import data into database with brainvisa ontology")
        import_p(input=self.T1_orig, output=self.T1_output,
                 referential=self.T1_referential)
        t1ref = aims.read(self.T1_referential)

        f = aims.Finder()
        f.check(self.T1_output)
        t1h = f.header()

        if self.transform_to_scanner_based is not None:
            tr = aims.AffineTransformation3d(t1h['transformations'][-1])
            tr.header()['source_referential'] = t1ref['uuid']
            if self.scanner_based_referential not in (None, Undefined, ''):
                sb = aims.read(self.scanner_based_referential)
                tr.header()['destination_referential'] = sb['uuid']
            aims.write(tr, self.transform_to_scanner_based)

        ribbon = aims.read(self.ribbon_image).astype('S16')
        ribbon.header()['referential'] = t1ref['uuid']
        aims.write(ribbon, self.split_brain_output)

        if self.Talairach_Auto is not None:
            # import / convert transformation to MNI space
            print("Convert Talairach_Auto into AC-PC File")
            talairach_freesurfer = aims.read(self.Talairach_Auto)
            f = aims.Finder()
            f.check(self.T1_output)
            header_nifti = aims.AffineTransformation3d(
                t1h['transformations'][-1])
            t1aims2mni = talairach_freesurfer * header_nifti
            t1aims2mni.header()['source_referential'] = t1ref['uuid']
            t1aims2mni.header()['destination_referential'] \
                = aims.StandardReferentials.mniTemplateReferentialID()
            aims.write(t1aims2mni, self.normalization_transformation)

            if self.talairach_transform is not None:
                proc = get_process_instance(
                    'morphologist.capsul.axon.talairachtransformationfromnormalization')
                proc(
                    normalization_transformation=
                        self.normalization_transformation,
                    Talairach_transform=self.talairach_transform,
                    commissure_coordinates=self.commissure_coordinates,
                    t1mri=self.T1_output,
                    source_referential=self.T1_referential,
                    normalized_referential=self.mni_referential,
                    transform_chain_ACPC_to_Normalized=
                        [self.transform_chain_ACPC_to_Normalized],
                    acpc_referential=self.acpc_referential)

        # change labels for Split Brain
        print("Create right/left grey white files from ribbon freesurfer data")
        greyStatClassif_f = tempfile.mkstemp(prefix='bv_fs_', suffix='.nii.gz')
        greyStatClassif = greyStatClassif_f[1]
        os.close(greyStatClassif_f[0])
        temps.append(greyStatClassif)
        temps.append(greyStatClassif + '.minf')
        subprocess.check_call([
            'AimsReplaceLevel',
            '-i', self.split_brain_output,
            '-o', greyStatClassif,
            '-g', '42', '41', '2', '3', '110', '120', '10', '20',
            '-n', '100', '200', '200', '100',
            '100', '200', '100', '200'])
        subprocess.check_call([
            'AimsReplaceLevel',
            '-i', self.split_brain_output,
            '-o', self.right_grey_white_output,
            '-g', '42', '41', '2', '3', '110', '120', '10', '20',
            '-n', '100', '200', '0', '0', '100', '200', '0', '0'])
        subprocess.check_call([
            'AimsReplaceLevel',
            '-i', self.split_brain_output,
            '-o', self.left_grey_white_output,
            '-g', '42', '41', '2', '3', '110', '120', '10', '20',
            '-n', '0', '0', '200', '100', '0', '0', '100', '200'])

        print("Create brain mask file from ribbon freesurfer data")
        subprocess.check_call([
            'AimsReplaceLevel',
            '-i', self.split_brain_output,
            '-o', self.brain_mask_output,
            '-g', '42', '41', '2', '3', '110', '120', '10', '20',
            '-n', '255', '255', '255', '255', '255', '255', '255', '255'])

        print("Create split brain file from ribbon freesurfer data")
        subprocess.check_call([
            'AimsReplaceLevel',
            '-i', self.split_brain_output,
            '-o', self.split_brain_output,
            '-g', '42', '41', '2', '3', '110', '120', '10', '20',
            '-n', '1', '1', '2', '2', '1', '1', '2', '2'])

        # Launch VipT1BiaisCorrection
        print("Launch T1BiasCorrection")
        tmp_f = tempfile.mkstemp(prefix='bv_fs_', suffix='.nii.gz')
        tmp = tmp_f[1]
        os.close(tmp_f[0])
        temps.append(tmp)
        temps.append(tmp + '.minf')

        proc = get_process_instance(
            'morphologist.capsul.axon.t1biascorrection')
        proc(
            t1mri=self.T1_output,
            commissure_coordinates=self.commissure_coordinates,
            delete_last_n_slices='0',
            t1mri_nobias=self.bias_corrected_output,
            field='',
            write_hfiltered='no',
            hfiltered=tmp,
            write_wridges='no',
            white_ridges=tmp,
            write_variance='no',
            variance=tmp,
            write_edges='no',
            edges=tmp,
            meancurvature='')

        # Launch VipGreyStatFromClassif to generate a histo analysis file
        print(
            "Launch VipGreyStatFromClassif to generate a histo analysis file")
        subprocess.check_call([
            'VipGreyStatFromClassif',
            '-i', self.bias_corrected_output,
            '-c', greyStatClassif,
            '-a', self.histo_analysis,
            '-g', '100', '-w', '200'])

        # # Launch Morphologist
        # if self.use_morphologist != 'none':
        #     engine = self.get_study_config().engine
        #     morphologist = engine.get_process_instance(
        #         'morphologist.capsul.morphologist')
        #     if not self.perform_morpho_report:
        #         morphologist.nodes['Report'].enabled = False
        #
        #     morphologist.t1mri = self.T1_output
        #     morphologist.t1mri_nobias = self.bias_corrected_output
        #     morphologist.histo_analysis = self.histo_analysis
        #     morphologist.split_brain = self.split_brain_output
        #
        #     nodes = morphologist.nodes
        #
        #     print(
        #         'Now run the last part of the regular Morphologist pipeline.')
        #
        #     nodes['PrepareSubject'].enabled = False
        #     nodes['BiasCorrection'].enabled = False
        #     nodes['HistoAnalysis'].enabled = False
        #     nodes['BrainSegmentation'].enabled = False
        #     nodes['Renorm'].enabled = False
        #     nodes['SplitBrain'].enabled = False
        #     nodes['TalairachTransformation'].enabled = False
        #     # nodes['HeadMesh'].enabled = False
        #     nodes['GreyWhiteClassification'].enabled = False
        #     nodes['GreyWhiteClassification_1'].enabled = False
        #
        #     morphologist.allow_multithreading = self.allow_multithreading
        #
        #     # completion
        #     engine.load_modules(['fom', 'axon'])
        #
        #     sub = osp.basename(self.T1_output).split('.')[0]
        #     print('sub:', sub)
        #     fom = 'morphologist-bids-2.0'
        #     d = osp.dirname
        #     bdir = d(d(d(d(self.T1_output))))
        #     if sub.startswith('sub-') and '_ses-' in sub:
        #         fom = 'morphologist-bids-2.0'
        #         bdir = d(d(d(d(self.T1_output))))
        #         print('BIDS2')
        #     elif osp.basename(d(d(self.T1_output))) == 't1mri':
        #         fom = 'morphologist-auto-nonoverlap-1.0'
        #         bdir = d(d(d(d(d(self.T1_output)))))
        #         print('traditional BV')
        #     else:
        #         print('FOM not recognized')
        #
        #     print('fom:', fom)
        #     print('bdir:', bdir)
        #
        #     with engine.settings as session:
        #         config = session.config('fom', 'global')
        #         config.input_fom = fom
        #         config.output_fom = fom
        #         config.input_directory = bdir
        #         config.output_directory = bdir
        #
        #     fom_atts = {}
        #     # pc = ProcessCompletionEngine.get_completion_engine(self)
        #     pc = ProcessCompletionEngine.get_completion_engine(morphologist)  # FIXME
        #     pta = engine._modules_data['fom'].get('fom_pta', {}).get('output')
        #     if pta is not None:
        #         for alist in pta.parse_path(osp.relpath(self.T1_output, bdir)):
        #             print(alist)
        #             atts = alist[2]
        #             # if atts.get('fom_parameter') == 'T1_output':
        #             if atts.get('fom_parameter') == 'imported_t1mri':  # FIXME
        #                 fom_atts = atts
        #                 break
        #
        #     pc = ProcessCompletionEngine.get_completion_engine(morphologist)
        #     print('pc:', pc)
        #     print('attr:', pc.get_attribute_values().user_traits().keys())
        #     print('completion config:', engine.settings.export_config_dict())
        #
        #     attrs = pc.get_attribute_values()
        #     fom_atts = {k: v for k, v in fom_atts.items()
        #                 if attrs.trait(k) is not None}
        #     attrs.import_from_dict(fom_atts)
        #     print('compl attr:')
        #     print(pc.get_attribute_values().export_to_dict())
        #     pc.complete_parameters()
        #     print('commissure_coordinates:', morphologist.commissure_coordinates)
        #     print('output graph:', morphologist.left_labelled_graph)
        #
        # if self.use_morphologist == 'graphically':
        #     print('Display pipeline...')
        #     QtThreadCall().call(pc.capsul_attributes.on_trait_change,
        #                         pc.attributes_changed)
        #     QtThreadCall().call(self.show_morpho_gui, morphologist)
        #
        # if self.use_morphologist != 'none':
        #     print('running Morphologist...')
        #     print('commissure_coordinates:', morphologist.commissure_coordinates)
        #     print('output graph:', morphologist.left_labelled_graph)
        #     morphologist()
        # else:
        #     print('Pipeline not run since the "use_morphologist" parameter '
        #           'prevents it')

        print('OK')

    def remove_temp(self, temps):
        while temps:
            tf = temps.pop(0)
            os.unlink(tf)

    def show_morpho_gui(self, morphologist):
        from soma.qt_gui.qt_backend import Qt
        from capsul.qt_gui.widgets.attributed_process_widget \
            import AttributedProcessWidget

        qapp = Qt.QApplication.instance()
        if not isinstance(qapp, Qt.QApplication):
            qapp = Qt.QApplication([])

        pcv = AttributedProcessWidget(morphologist,
                                      enable_attr_from_filename=True,
                                      enable_load_buttons=True)
        pcv.show()
        qapp.exec()
        del pcv
        del qapp


if __name__ == '__main__':
    from capsul.process import runprocess
    import sys
    from soma.qt_gui.qt_backend import Qt
    from capsul.qt_gui.widgets.attributed_process_widget \
        import AttributedProcessWidget

    qapp = Qt.QApplication([])

    args = [
        'capsul',
        'brainvisa.freesurfer.capsul.import_freesurfer_to_morpho.ImportFreesurferToMorpho',
        'T1_orig=/home/dr144257/data/freesurfer_data/subjects/mni_icbm152_t1_tal_nlin_asym_09c/mri/orig.mgz',
        'ribbon_image=/home/dr144257/data/freesurfer_data/subjects/mni_icbm152_t1_tal_nlin_asym_09c/mri/ribbon.mgz',
        'scanner_based_referential=/volatile/home/dr144257/data/freesurfer_data/subjects/mni_icbm152_t1_tal_nlin_asym_09c/mri/transforms/orig_mni_icbm152_t1_tal_nlin_asym_09c_Scanner_Based.referential',
        'Talairach_Auto=/volatile/home/dr144257/data/freesurfer_data/subjects/mni_icbm152_t1_tal_nlin_asym_09c/mri/transforms/talairach.auto.xfm',
        'T1_output=/volatile/home/dr144257/data/baseessai/freesurfer/mni_icbm152_nlin_asym_09c/t1mri/default_acquisition/mni_icbm152_nlin_asym_09c.nii.gz',
        'T1_referential=/volatile/home/dr144257/data/baseessai/freesurfer/mni_icbm152_nlin_asym_09c/t1mri/default_acquisition/registration/RawT1-mni_icbm152_nlin_asym_09c_default_acquisition.referential',
        'transform_to_scanner_based=/volatile/home/dr144257/data/baseessai/freesurfer/mni_icbm152_nlin_asym_09c/t1mri/default_acquisition/registration/RawT1-mni_icbm152_nlin_asym_09c_default_acquisition_TO_Scanner_Based.trm',
        'bias_corrected_output=/volatile/home/dr144257/data/baseessai/freesurfer/mni_icbm152_nlin_asym_09c/t1mri/default_acquisition/default_analysis/nobias_mni_icbm152_nlin_asym_09c.nii.gz',
        'normalization_transformation=/volatile/home/dr144257/data/baseessai/freesurfer/mni_icbm152_nlin_asym_09c/t1mri/default_acquisition/registration/RawT1-mni_icbm152_nlin_asym_09c_default_acquisition_TO_Talairach-MNI.trm',
        'talairach_transform=/volatile/home/dr144257/data/baseessai/freesurfer/mni_icbm152_nlin_asym_09c/t1mri/default_acquisition/registration/RawT1-mni_icbm152_nlin_asym_09c_default_acquisition_TO_Talairach-ACPC.trm',
        'commissure_coordinates=/volatile/home/dr144257/data/baseessai/freesurfer/mni_icbm152_nlin_asym_09c/t1mri/default_acquisition/mni_icbm152_nlin_asym_09c.APC',
        'histo_analysis=/volatile/home/dr144257/data/baseessai/freesurfer/mni_icbm152_nlin_asym_09c/t1mri/default_acquisition/default_analysis/nobias_mni_icbm152_nlin_asym_09c.han',
        'brain_mask_output=/volatile/home/dr144257/data/baseessai/freesurfer/mni_icbm152_nlin_asym_09c/t1mri/default_acquisition/default_analysis/segmentation/brain_mni_icbm152_nlin_asym_09c.nii.gz',
        'split_brain_output=/volatile/home/dr144257/data/baseessai/freesurfer/mni_icbm152_nlin_asym_09c/t1mri/default_acquisition/default_analysis/segmentation/voronoi_mni_icbm152_nlin_asym_09c.nii.gz',
        'left_grey_white_output=/volatile/home/dr144257/data/baseessai/freesurfer/mni_icbm152_nlin_asym_09c/t1mri/default_acquisition/default_analysis/segmentation/Lgrey_white_mni_icbm152_nlin_asym_09c.nii.gz',
        'right_grey_white_output=/volatile/home/dr144257/data/baseessai/freesurfer/mni_icbm152_nlin_asym_09c/t1mri/default_acquisition/default_analysis/segmentation/Rgrey_white_mni_icbm152_nlin_asym_09c.nii.gz',
        'use_morphologist=graphically',
        'mni_referential=/volatile/home/dr144257/brainvisa-6.0/build/share/brainvisa-share-6.0/registration/Talairach-MNI_template-SPM.referential',
        'transform_chain_ACPC_to_Normalized=["/volatile/home/dr144257/brainvisa-6.0/build/share/brainvisa-share-6.0/transformation/talairach_TO_spm_template_novoxels.trm"]',
        'acpc_referential=/volatile/home/dr144257/brainvisa-6.0/build/share/brainvisa-share-6.0/registration/Talairach-AC_PC-Anatomist.referential',
        'allow_multithreading=True',
        'perform_morpho_report=True',
    ]

    sys.argv = args
    runprocess.main()
