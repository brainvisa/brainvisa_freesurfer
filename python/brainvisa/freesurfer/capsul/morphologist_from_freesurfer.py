# -*- coding: utf-8 -*-

from capsul.api import Pipeline
import traits.api as traits


class MorphologistFromFreesurfer(Pipeline):

    def pipeline_definition(self):
        # nodes
        self.add_process("import_fs", "brainvisa.freesurfer.capsul.import_freesurfer_to_morpho.ImportFreesurferToMorpho")
        self.nodes["import_fs"].set_plug_value("T1_output", '/tmp/input_data/sub-rototo/ses-0/run-0/sub-rototo_ses-0_run-0_T1w.nii.gz')
        self.nodes["import_fs"].set_plug_value("talairach_transform", '/tmp/input_data/sub-rototo/ses-0/run-0/registration/sub-rototo_ses-0_run-0_T1w_TO_Talairach-ACPC.trm')
        self.nodes["import_fs"].set_plug_value("split_brain_output", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/segmentation/sub-rototo_ses-0_run-0_voronoi.nii.gz')
        self.nodes["import_fs"].set_plug_value("left_grey_white_output", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/segmentation/sub-rototo_ses-0_run-0_hemi-L_grey_white.nii.gz')
        self.nodes["import_fs"].set_plug_value("right_grey_white_output", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-R_grey_white.nii.gz')
        self.nodes["import_fs"].process.T1_output = '/tmp/input_data/sub-rototo/ses-0/run-0/sub-rototo_ses-0_run-0_T1w.nii.gz'
        self.nodes["import_fs"].process.talairach_transform = '/tmp/input_data/sub-rototo/ses-0/run-0/registration/sub-rototo_ses-0_run-0_T1w_TO_Talairach-ACPC.trm'
        self.nodes["import_fs"].process.split_brain_output = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/segmentation/sub-rototo_ses-0_run-0_voronoi.nii.gz'
        self.nodes["import_fs"].process.left_grey_white_output = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/segmentation/sub-rototo_ses-0_run-0_hemi-L_grey_white.nii.gz'
        self.nodes["import_fs"].process.right_grey_white_output = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-R_grey_white.nii.gz'
        self.add_process("HeadMesh", "morphologist.capsul.axon.scalpmesh.ScalpMesh")
        self.add_process("GreyWhiteTopology", "morphologist.capsul.axon.greywhitetopology.GreyWhiteTopology")
        self.nodes["GreyWhiteTopology"].set_plug_value("grey_white", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/segmentation/sub-rototo_ses-0_run-0_hemi-L_grey_white.nii.gz')
        self.nodes["GreyWhiteTopology"].process.grey_white = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/segmentation/sub-rototo_ses-0_run-0_hemi-L_grey_white.nii.gz'
        self.add_process("GreyWhiteTopology_1", "morphologist.capsul.axon.greywhitetopology.GreyWhiteTopology")
        self.nodes["GreyWhiteTopology_1"].set_plug_value("grey_white", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-R_grey_white.nii.gz')
        self.nodes["GreyWhiteTopology_1"].process.grey_white = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-R_grey_white.nii.gz'
        self.add_process("SulciSkeleton", "morphologist.capsul.axon.sulciskeleton.SulciSkeleton")
        self.nodes["SulciSkeleton"].set_plug_value("grey_white", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/segmentation/sub-rototo_ses-0_run-0_hemi-L_grey_white.nii.gz')
        self.nodes["SulciSkeleton"].process.grey_white = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/segmentation/sub-rototo_ses-0_run-0_hemi-L_grey_white.nii.gz'
        self.add_process("SulciSkeleton_1", "morphologist.capsul.axon.sulciskeleton.SulciSkeleton")
        self.nodes["SulciSkeleton_1"].set_plug_value("grey_white", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-R_grey_white.nii.gz')
        self.nodes["SulciSkeleton_1"].process.grey_white = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-R_grey_white.nii.gz'
        self.add_process("GreyWhiteMesh", "morphologist.capsul.axon.greywhitemesh.GreyWhiteMesh")
        self.nodes["GreyWhiteMesh"].set_plug_value("white_mesh", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-L_white.surf.gii')
        self.nodes["GreyWhiteMesh"].process.white_mesh = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-L_white.surf.gii'
        self.add_process("GreyWhiteMesh_1", "morphologist.capsul.axon.greywhitemesh.GreyWhiteMesh")
        self.nodes["GreyWhiteMesh_1"].set_plug_value("white_mesh", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-R_white.surf.gii')
        self.nodes["GreyWhiteMesh_1"].process.white_mesh = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-R_white.surf.gii'
        self.add_process("PialMesh¨", "morphologist.capsul.axon.pialmesh.PialMesh")
        self.nodes["PialMesh¨"].set_plug_value("grey_white", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/segmentation/sub-rototo_ses-0_run-0_hemi-L_grey_white.nii.gz')
        self.nodes["PialMesh¨"].set_plug_value("pial_mesh", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-L_pial.surf.gii')
        self.nodes["PialMesh¨"].process.grey_white = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/segmentation/sub-rototo_ses-0_run-0_hemi-L_grey_white.nii.gz'
        self.nodes["PialMesh¨"].process.pial_mesh = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-L_pial.surf.gii'
        self.add_process("PialMesh_1", "morphologist.capsul.axon.pialmesh.PialMesh")
        self.nodes["PialMesh_1"].set_plug_value("grey_white", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-R_grey_white.nii.gz')
        self.nodes["PialMesh_1"].set_plug_value("pial_mesh", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-R_pial.surf.gii')
        self.nodes["PialMesh_1"].process.grey_white = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-R_grey_white.nii.gz'
        self.nodes["PialMesh_1"].process.pial_mesh = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-R_pial.surf.gii'
        self.add_process("CorticalFoldsGraph", "morphologist.capsul.axon.sulcigraph.SulciGraph")
        self.nodes["CorticalFoldsGraph"].set_plug_value("grey_white", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/segmentation/sub-rototo_ses-0_run-0_hemi-L_grey_white.nii.gz')
        self.nodes["CorticalFoldsGraph"].set_plug_value("split_brain", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/segmentation/sub-rototo_ses-0_run-0_voronoi.nii.gz')
        self.nodes["CorticalFoldsGraph"].set_plug_value("white_mesh", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-L_white.surf.gii')
        self.nodes["CorticalFoldsGraph"].set_plug_value("pial_mesh", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-L_pial.surf.gii')
        self.nodes["CorticalFoldsGraph"].set_plug_value("talairach_transform", '/tmp/input_data/sub-rototo/ses-0/run-0/registration/sub-rototo_ses-0_run-0_T1w_TO_Talairach-ACPC.trm')
        self.nodes["CorticalFoldsGraph"].process.grey_white = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/segmentation/sub-rototo_ses-0_run-0_hemi-L_grey_white.nii.gz'
        self.nodes["CorticalFoldsGraph"].process.split_brain = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/segmentation/sub-rototo_ses-0_run-0_voronoi.nii.gz'
        self.nodes["CorticalFoldsGraph"].process.white_mesh = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-L_white.surf.gii'
        self.nodes["CorticalFoldsGraph"].process.pial_mesh = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-L_pial.surf.gii'
        self.nodes["CorticalFoldsGraph"].process.talairach_transform = '/tmp/input_data/sub-rototo/ses-0/run-0/registration/sub-rototo_ses-0_run-0_T1w_TO_Talairach-ACPC.trm'
        self.add_process("CorticalFoldsGraph_1", "morphologist.capsul.axon.sulcigraph.SulciGraph")
        self.nodes["CorticalFoldsGraph_1"].set_plug_value("grey_white", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-R_grey_white.nii.gz')
        self.nodes["CorticalFoldsGraph_1"].set_plug_value("split_brain", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/segmentation/sub-rototo_ses-0_run-0_voronoi.nii.gz')
        self.nodes["CorticalFoldsGraph_1"].set_plug_value("white_mesh", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-R_white.surf.gii')
        self.nodes["CorticalFoldsGraph_1"].set_plug_value("pial_mesh", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-R_pial.surf.gii')
        self.nodes["CorticalFoldsGraph_1"].set_plug_value("talairach_transform", '/tmp/input_data/sub-rototo/ses-0/run-0/registration/sub-rototo_ses-0_run-0_T1w_TO_Talairach-ACPC.trm')
        self.nodes["CorticalFoldsGraph_1"].process.grey_white = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-R_grey_white.nii.gz'
        self.nodes["CorticalFoldsGraph_1"].process.split_brain = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/segmentation/sub-rototo_ses-0_run-0_voronoi.nii.gz'
        self.nodes["CorticalFoldsGraph_1"].process.white_mesh = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-R_white.surf.gii'
        self.nodes["CorticalFoldsGraph_1"].process.pial_mesh = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-R_pial.surf.gii'
        self.nodes["CorticalFoldsGraph_1"].process.talairach_transform = '/tmp/input_data/sub-rototo/ses-0/run-0/registration/sub-rototo_ses-0_run-0_T1w_TO_Talairach-ACPC.trm'
        self.add_process("SulciRecognition", "morphologist.capsul.axon.sulcilabelling.SulciLabelling")
        self.nodes["SulciRecognition"].set_plug_value("output_graph", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-L_auto.arg')
        self.nodes["SulciRecognition"].set_plug_value("CNN_recognition19_grey_white", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/segmentation/sub-rototo_ses-0_run-0_hemi-L_grey_white.nii.gz')
        self.nodes["SulciRecognition"].set_plug_value("CNN_recognition19_white_mesh", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-L_white.surf.gii')
        self.nodes["SulciRecognition"].set_plug_value("CNN_recognition19_pial_mesh", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-L_pial.surf.gii')
        self.nodes["SulciRecognition"].process.nodes["recognition2000"].set_plug_value("output_graph", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-L_auto.arg')
        self.nodes["SulciRecognition"].process.nodes["SPAM_recognition09"].set_plug_value("output_graph", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-L_auto.arg')
        self.nodes["SulciRecognition"].process.nodes["CNN_recognition19"].set_plug_value("grey_white", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/segmentation/sub-rototo_ses-0_run-0_hemi-L_grey_white.nii.gz')
        self.nodes["SulciRecognition"].process.nodes["CNN_recognition19"].set_plug_value("white_mesh", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-L_white.surf.gii')
        self.nodes["SulciRecognition"].process.nodes["CNN_recognition19"].set_plug_value("pial_mesh", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-L_pial.surf.gii')
        self.nodes["SulciRecognition"].process.nodes["CNN_recognition19"].set_plug_value("labelled_graph", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-L_auto.arg')
        self.nodes["SulciRecognition"].process.nodes["select_Sulci_Recognition"].set_plug_value("recognition2000_switch_output_graph", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-L_auto.arg')
        self.nodes["SulciRecognition"].process.nodes["select_Sulci_Recognition"].set_plug_value("SPAM_recognition09_switch_output_graph", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-L_auto.arg')
        self.nodes["SulciRecognition"].process.nodes["select_Sulci_Recognition"].set_plug_value("CNN_recognition19_switch_output_graph", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-L_auto.arg')
        self.nodes["SulciRecognition"].process.nodes["select_Sulci_Recognition"].set_plug_value("output_graph", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-L_auto.arg')
        self.nodes["SulciRecognition"].process.nodes["SPAM_recognition09"].process.nodes["global_recognition"].set_plug_value("output_graph", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-L_auto.arg')
        self.nodes["SulciRecognition"].process.nodes["SPAM_recognition09"].process.nodes["local_recognition"].set_plug_value("data_graph", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-L_auto.arg')
        self.nodes["SulciRecognition"].process.nodes["SPAM_recognition09"].process.nodes["local_recognition"].set_plug_value("output_graph", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-L_auto.arg')
        self.nodes["SulciRecognition"].process.nodes["SPAM_recognition09"].process.nodes["markovian_recognition"].set_plug_value("data_graph", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-L_auto.arg')
        self.nodes["SulciRecognition"].process.nodes["SPAM_recognition09"].process.nodes["markovian_recognition"].set_plug_value("output_graph", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-L_auto.arg')
        self.nodes["SulciRecognition"].process.nodes["SPAM_recognition09"].process.nodes["local_or_markovian"].set_plug_value("local_recognition_switch_output_graph", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-L_auto.arg')
        self.nodes["SulciRecognition"].process.nodes["SPAM_recognition09"].process.nodes["local_or_markovian"].set_plug_value("markovian_recognition_switch_output_graph", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-L_auto.arg')
        self.nodes["SulciRecognition"].process.nodes["SPAM_recognition09"].process.nodes["local_or_markovian"].set_plug_value("output_graph", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-L_auto.arg')
        self.nodes["SulciRecognition"].process.nodes_activation = {'recognition2000': True, 'SPAM_recognition09': True, 'CNN_recognition19': True}
        self.nodes["SulciRecognition"].process.output_graph = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-L_auto.arg'
        self.nodes["SulciRecognition"].process.CNN_recognition19_grey_white = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/segmentation/sub-rototo_ses-0_run-0_hemi-L_grey_white.nii.gz'
        self.nodes["SulciRecognition"].process.CNN_recognition19_white_mesh = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-L_white.surf.gii'
        self.nodes["SulciRecognition"].process.CNN_recognition19_pial_mesh = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-L_pial.surf.gii'
        self.add_process("SulciRecognition_1", "morphologist.capsul.axon.sulcilabelling.SulciLabelling")
        self.nodes["SulciRecognition_1"].set_plug_value("output_graph", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-R_auto.arg')
        self.nodes["SulciRecognition_1"].set_plug_value("CNN_recognition19_grey_white", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-R_grey_white.nii.gz')
        self.nodes["SulciRecognition_1"].set_plug_value("CNN_recognition19_white_mesh", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-R_white.surf.gii')
        self.nodes["SulciRecognition_1"].set_plug_value("CNN_recognition19_pial_mesh", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-R_pial.surf.gii')
        self.nodes["SulciRecognition_1"].process.nodes["recognition2000"].set_plug_value("output_graph", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-R_auto.arg')
        self.nodes["SulciRecognition_1"].process.nodes["SPAM_recognition09"].set_plug_value("output_graph", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-R_auto.arg')
        self.nodes["SulciRecognition_1"].process.nodes["CNN_recognition19"].set_plug_value("grey_white", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-R_grey_white.nii.gz')
        self.nodes["SulciRecognition_1"].process.nodes["CNN_recognition19"].set_plug_value("white_mesh", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-R_white.surf.gii')
        self.nodes["SulciRecognition_1"].process.nodes["CNN_recognition19"].set_plug_value("pial_mesh", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-R_pial.surf.gii')
        self.nodes["SulciRecognition_1"].process.nodes["CNN_recognition19"].set_plug_value("labelled_graph", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-R_auto.arg')
        self.nodes["SulciRecognition_1"].process.nodes["select_Sulci_Recognition"].set_plug_value("recognition2000_switch_output_graph", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-R_auto.arg')
        self.nodes["SulciRecognition_1"].process.nodes["select_Sulci_Recognition"].set_plug_value("SPAM_recognition09_switch_output_graph", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-R_auto.arg')
        self.nodes["SulciRecognition_1"].process.nodes["select_Sulci_Recognition"].set_plug_value("CNN_recognition19_switch_output_graph", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-R_auto.arg')
        self.nodes["SulciRecognition_1"].process.nodes["select_Sulci_Recognition"].set_plug_value("output_graph", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-R_auto.arg')
        self.nodes["SulciRecognition_1"].process.nodes["SPAM_recognition09"].process.nodes["global_recognition"].set_plug_value("output_graph", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-R_auto.arg')
        self.nodes["SulciRecognition_1"].process.nodes["SPAM_recognition09"].process.nodes["local_recognition"].set_plug_value("data_graph", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-R_auto.arg')
        self.nodes["SulciRecognition_1"].process.nodes["SPAM_recognition09"].process.nodes["local_recognition"].set_plug_value("output_graph", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-R_auto.arg')
        self.nodes["SulciRecognition_1"].process.nodes["SPAM_recognition09"].process.nodes["markovian_recognition"].set_plug_value("data_graph", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-R_auto.arg')
        self.nodes["SulciRecognition_1"].process.nodes["SPAM_recognition09"].process.nodes["markovian_recognition"].set_plug_value("output_graph", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-R_auto.arg')
        self.nodes["SulciRecognition_1"].process.nodes["SPAM_recognition09"].process.nodes["local_or_markovian"].set_plug_value("local_recognition_switch_output_graph", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-R_auto.arg')
        self.nodes["SulciRecognition_1"].process.nodes["SPAM_recognition09"].process.nodes["local_or_markovian"].set_plug_value("markovian_recognition_switch_output_graph", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-R_auto.arg')
        self.nodes["SulciRecognition_1"].process.nodes["SPAM_recognition09"].process.nodes["local_or_markovian"].set_plug_value("output_graph", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-R_auto.arg')
        self.nodes["SulciRecognition_1"].process.nodes_activation = {'recognition2000': True, 'SPAM_recognition09': True, 'CNN_recognition19': True}
        self.nodes["SulciRecognition_1"].process.output_graph = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-R_auto.arg'
        self.nodes["SulciRecognition_1"].process.CNN_recognition19_grey_white = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-R_grey_white.nii.gz'
        self.nodes["SulciRecognition_1"].process.CNN_recognition19_white_mesh = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-R_white.surf.gii'
        self.nodes["SulciRecognition_1"].process.CNN_recognition19_pial_mesh = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-R_pial.surf.gii'
        self.add_process("SulcalMorphometry", "morphologist.capsul.axon.sulcigraphmorphometrybysubject.sulcigraphmorphometrybysubject")
        self.nodes["SulcalMorphometry"].set_plug_value("left_sulci_graph", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-L_auto.arg')
        self.nodes["SulcalMorphometry"].set_plug_value("right_sulci_graph", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-R_auto.arg')
        self.nodes["SulcalMorphometry"].process.left_sulci_graph = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-L_auto.arg'
        self.nodes["SulcalMorphometry"].process.right_sulci_graph = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-R_auto.arg'
        self.add_process("GlobalMorphometry", "morphologist.capsul.axon.brainvolumes.brainvolumes")
        self.nodes["GlobalMorphometry"].set_plug_value("split_brain", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/segmentation/sub-rototo_ses-0_run-0_voronoi.nii.gz')
        self.nodes["GlobalMorphometry"].set_plug_value("left_grey_white", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/segmentation/sub-rototo_ses-0_run-0_hemi-L_grey_white.nii.gz')
        self.nodes["GlobalMorphometry"].set_plug_value("right_grey_white", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-R_grey_white.nii.gz')
        self.nodes["GlobalMorphometry"].set_plug_value("left_labelled_graph", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-L_auto.arg')
        self.nodes["GlobalMorphometry"].set_plug_value("right_labelled_graph", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-R_auto.arg')
        self.nodes["GlobalMorphometry"].set_plug_value("left_gm_mesh", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-L_pial.surf.gii')
        self.nodes["GlobalMorphometry"].set_plug_value("right_gm_mesh", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-R_pial.surf.gii')
        self.nodes["GlobalMorphometry"].set_plug_value("left_wm_mesh", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-L_white.surf.gii')
        self.nodes["GlobalMorphometry"].set_plug_value("right_wm_mesh", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-R_white.surf.gii')
        self.nodes["GlobalMorphometry"].set_plug_value("subject", 'rototo')
        self.nodes["GlobalMorphometry"].set_plug_value("left_csf", '/tmp/output_data/sub-rototo/ses-0/run-0/ana-tutu/segmentation/sub-rototo_ses-0_run-0_hemi-L_csf.nii.gz')
        self.nodes["GlobalMorphometry"].set_plug_value("right_csf", '/tmp/output_data/sub-rototo/ses-0/run-0/ana-tutu/segmentation/sub-rototo_ses-0_run-0_hemi-R_csf.nii.gz')
        self.nodes["GlobalMorphometry"].set_plug_value("brain_volumes_file", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/segmentation/sub-rototo_ses-0_run-0_brain_volumes.csv')
        self.nodes["GlobalMorphometry"].process.split_brain = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/segmentation/sub-rototo_ses-0_run-0_voronoi.nii.gz'
        self.nodes["GlobalMorphometry"].process.left_grey_white = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/segmentation/sub-rototo_ses-0_run-0_hemi-L_grey_white.nii.gz'
        self.nodes["GlobalMorphometry"].process.right_grey_white = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-R_grey_white.nii.gz'
        self.nodes["GlobalMorphometry"].process.left_csf = '/tmp/output_data/sub-rototo/ses-0/run-0/ana-tutu/segmentation/sub-rototo_ses-0_run-0_hemi-L_csf.nii.gz'
        self.nodes["GlobalMorphometry"].process.right_csf = '/tmp/output_data/sub-rototo/ses-0/run-0/ana-tutu/segmentation/sub-rototo_ses-0_run-0_hemi-R_csf.nii.gz'
        self.nodes["GlobalMorphometry"].process.left_labelled_graph = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-L_auto.arg'
        self.nodes["GlobalMorphometry"].process.right_labelled_graph = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-R_auto.arg'
        self.nodes["GlobalMorphometry"].process.left_gm_mesh = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-L_pial.surf.gii'
        self.nodes["GlobalMorphometry"].process.right_gm_mesh = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-R_pial.surf.gii'
        self.nodes["GlobalMorphometry"].process.left_wm_mesh = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-L_white.surf.gii'
        self.nodes["GlobalMorphometry"].process.right_wm_mesh = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-R_white.surf.gii'
        self.nodes["GlobalMorphometry"].process.subject = 'rototo'
        self.nodes["GlobalMorphometry"].process.brain_volumes_file = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/segmentation/sub-rototo_ses-0_run-0_brain_volumes.csv'
        self.add_process("Report", "morphologist.capsul.axon.morpho_report.morpho_report")
        self.nodes["Report"].set_plug_value("t1mri", '/tmp/input_data/sub-rototo/ses-0/run-0/sub-rototo_ses-0_run-0_T1w.nii.gz')
        self.nodes["Report"].set_plug_value("left_grey_white", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/segmentation/sub-rototo_ses-0_run-0_hemi-L_grey_white.nii.gz')
        self.nodes["Report"].set_plug_value("right_grey_white", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-R_grey_white.nii.gz')
        self.nodes["Report"].set_plug_value("left_gm_mesh", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-L_pial.surf.gii')
        self.nodes["Report"].set_plug_value("right_gm_mesh", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-R_pial.surf.gii')
        self.nodes["Report"].set_plug_value("left_wm_mesh", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-L_white.surf.gii')
        self.nodes["Report"].set_plug_value("right_wm_mesh", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-R_white.surf.gii')
        self.nodes["Report"].set_plug_value("left_labelled_graph", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-L_auto.arg')
        self.nodes["Report"].set_plug_value("right_labelled_graph", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-R_auto.arg')
        self.nodes["Report"].set_plug_value("talairach_transform", '/tmp/input_data/sub-rototo/ses-0/run-0/registration/sub-rototo_ses-0_run-0_T1w_TO_Talairach-ACPC.trm')
        self.nodes["Report"].set_plug_value("brain_volumes_file", '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/segmentation/sub-rototo_ses-0_run-0_brain_volumes.csv')
        self.nodes["Report"].set_plug_value("normative_brain_stats", '/volatile/home/dr144257/brainvisa-6.0/build/share/brainvisa-share-6.0/normative_tables/morphologist/ukb_hcp/morphologist_normative_brain_volumes_stats.json')
        self.nodes["Report"].set_plug_value("subject", 'rototo')
        self.nodes["Report"].set_plug_value("report", '/tmp/output_data/sub-rototo/ses-0/run-0/ana-tutu/sub-rototo_ses-0_run-0_morphologist_report.pdf')
        self.nodes["Report"].set_plug_value("report_json", '/tmp/output_data/sub-rototo/ses-0/run-0/ana-tutu/sub-rototo_ses-0_run-0_morphologist_report.json')
        self.nodes["Report"].set_plug_value("inter_subject_qc_table", '/tmp/output_data/qc/qc.tsv')
        self.nodes["Report"].process.t1mri = '/tmp/input_data/sub-rototo/ses-0/run-0/sub-rototo_ses-0_run-0_T1w.nii.gz'
        self.nodes["Report"].process.left_grey_white = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/segmentation/sub-rototo_ses-0_run-0_hemi-L_grey_white.nii.gz'
        self.nodes["Report"].process.right_grey_white = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-R_grey_white.nii.gz'
        self.nodes["Report"].process.left_gm_mesh = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-L_pial.surf.gii'
        self.nodes["Report"].process.right_gm_mesh = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-R_pial.surf.gii'
        self.nodes["Report"].process.left_wm_mesh = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-L_white.surf.gii'
        self.nodes["Report"].process.right_wm_mesh = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-R_white.surf.gii'
        self.nodes["Report"].process.left_labelled_graph = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-L_auto.arg'
        self.nodes["Report"].process.right_labelled_graph = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-R_auto.arg'
        self.nodes["Report"].process.talairach_transform = '/tmp/input_data/sub-rototo/ses-0/run-0/registration/sub-rototo_ses-0_run-0_T1w_TO_Talairach-ACPC.trm'
        self.nodes["Report"].process.brain_volumes_file = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/segmentation/sub-rototo_ses-0_run-0_brain_volumes.csv'
        self.nodes["Report"].process.normative_brain_stats = '/volatile/home/dr144257/brainvisa-6.0/build/share/brainvisa-share-6.0/normative_tables/morphologist/ukb_hcp/morphologist_normative_brain_volumes_stats.json'
        self.nodes["Report"].process.report = '/tmp/output_data/sub-rototo/ses-0/run-0/ana-tutu/sub-rototo_ses-0_run-0_morphologist_report.pdf'
        self.nodes["Report"].process.report_json = '/tmp/output_data/sub-rototo/ses-0/run-0/ana-tutu/sub-rototo_ses-0_run-0_morphologist_report.json'
        self.nodes["Report"].process.inter_subject_qc_table = '/tmp/output_data/qc/qc.tsv'
        self.nodes["Report"].process.subject = 'rototo'

        # links
        self.export_parameter("import_fs", "T1_orig", is_optional=False)
        self.export_parameter("import_fs", "ribbon_image", is_optional=False)
        self.export_parameter("import_fs", "scanner_based_referential", is_optional=True)
        self.export_parameter("import_fs", "Talairach_Auto", is_optional=False)
        self.export_parameter("import_fs", "mni_referential", is_optional=False)
        self.export_parameter("import_fs", "transform_chain_ACPC_to_Normalized", is_optional=False)
        self.export_parameter("import_fs", "acpc_referential", is_optional=False)
        self.export_parameter("SulciRecognition", "CNN_recognition19_allow_multithreading", "allow_multithreading", is_optional=False)
        self.add_link("allow_multithreading->CorticalFoldsGraph.allow_multithreading")
        self.add_link("allow_multithreading->CorticalFoldsGraph_1.allow_multithreading")
        self.add_link("allow_multithreading->SulciRecognition_1.CNN_recognition19_allow_multithreading")
        self.export_parameter("HeadMesh", "remove_mask", "HeadMesh_remove_mask", is_optional=True)
        self.export_parameter("HeadMesh", "first_slice", "HeadMesh_first_slice", is_optional=True)
        self.export_parameter("HeadMesh", "threshold", "HeadMesh_threshold", is_optional=True)
        self.export_parameter("HeadMesh", "closing", "HeadMesh_closing", is_optional=True)
        self.export_parameter("HeadMesh", "threshold_mode", "HeadMesh_threshold_mode", is_optional=False)
        self.export_parameter("HeadMesh", "keep_head_mask", "HeadMesh_keep_head_mask", is_optional=False)
        self.export_parameter("GreyWhiteTopology_1", "version", "GreyWhiteTopology_version", is_optional=False)
        self.add_link("GreyWhiteTopology_version->GreyWhiteTopology.version")
        self.export_parameter("SulciSkeleton_1", "fix_random_seed", is_optional=False)
        self.add_link("fix_random_seed->PialMesh_1.fix_random_seed")
        self.add_link("fix_random_seed->SulciRecognition_1.fix_random_seed")
        self.add_link("fix_random_seed->PialMesh¨.fix_random_seed")
        self.add_link("fix_random_seed->SulciSkeleton.fix_random_seed")
        self.add_link("fix_random_seed->GreyWhiteTopology.fix_random_seed")
        self.add_link("fix_random_seed->SulciRecognition.fix_random_seed")
        self.add_link("fix_random_seed->GreyWhiteTopology_1.fix_random_seed")
        self.export_parameter("SulciSkeleton_1", "version", "SulciSkeleton_version", is_optional=False)
        self.add_link("SulciSkeleton_version->SulciSkeleton.version")
        self.export_parameter("PialMesh¨", "version", "PialMesh_version", is_optional=False)
        self.add_link("PialMesh_version->PialMesh_1.version")
        self.export_parameter("CorticalFoldsGraph_1", "compute_fold_meshes", is_optional=False)
        self.add_link("compute_fold_meshes->CorticalFoldsGraph.compute_fold_meshes")
        self.export_parameter("CorticalFoldsGraph", "graph_version", "CorticalFoldsGraph_graph_version", is_optional=False)
        self.add_link("CorticalFoldsGraph_graph_version->CorticalFoldsGraph_1.graph_version")
        self.export_parameter("CorticalFoldsGraph", "write_cortex_mid_interface", "CorticalFoldsGraph_write_cortex_mid_interface", is_optional=False)
        self.add_link("CorticalFoldsGraph_write_cortex_mid_interface->CorticalFoldsGraph_1.write_cortex_mid_interface")
        self.export_parameter("SulciRecognition", "select_Sulci_Recognition", is_optional=False)
        self.add_link("select_Sulci_Recognition->SulciRecognition_1.select_Sulci_Recognition")
        self.export_parameter("SulciRecognition", "recognition2000_model", "SulciRecognition_recognition2000_model", is_optional=True)
        self.export_parameter("SulciRecognition_1", "recognition2000_model_hint", "sulci_recognition2000_model_hint", is_optional=True)
        self.add_link("sulci_recognition2000_model_hint->SulciRecognition.recognition2000_model_hint")
        self.export_parameter("SulciRecognition", "recognition2000_rate", "sulci_recognition2000_rate", is_optional=True)
        self.add_link("sulci_recognition2000_rate->SulciRecognition_1.recognition2000_rate")
        self.export_parameter("SulciRecognition_1", "recognition2000_stopRate", "sulci_recognition2000_stop_rate", is_optional=True)
        self.add_link("sulci_recognition2000_stop_rate->SulciRecognition.recognition2000_stopRate")
        self.export_parameter("SulciRecognition", "recognition2000_niterBelowStopProp", "sulci_recognition2000_niter_below_stop_prop", is_optional=True)
        self.add_link("sulci_recognition2000_niter_below_stop_prop->SulciRecognition_1.recognition2000_niterBelowStopProp")
        self.export_parameter("SulciRecognition_1", "recognition2000_forbid_unknown_label", "sulci_recognition2000_forbid_unknown_label", is_optional=True)
        self.add_link("sulci_recognition2000_forbid_unknown_label->SulciRecognition.recognition2000_forbid_unknown_label")
        self.export_parameter("SulciRecognition", "SPAM_recognition09_local_or_markovian", "sulci_recognition_spam_local_or_markovian", is_optional=True)
        self.add_link("sulci_recognition_spam_local_or_markovian->SulciRecognition_1.SPAM_recognition09_local_or_markovian")
        self.export_parameter("SulciRecognition", "SPAM_recognition09_global_recognition_labels_translation_map", "SPAM_recognition_labels_translation_map", is_optional=True)
        self.add_link("SPAM_recognition_labels_translation_map->SulciRecognition_1.SPAM_recognition09_global_recognition_labels_translation_map")
        self.export_parameter("SulciRecognition", "SPAM_recognition09_global_recognition_labels_priors", "SulciRecognition_SPAM_recognition09_global_recognition_labels_priors", is_optional=True)
        self.export_parameter("SulciRecognition", "SPAM_recognition09_global_recognition_initial_transformation", "SulcalRecognition_SPAM_recognition09_global_recognition_initial_transformation", is_optional=True)
        self.export_parameter("SulciRecognition_1", "SPAM_recognition09_global_recognition_model_type", "sulci_recognition_spam_global_model_type", is_optional=True)
        self.add_link("sulci_recognition_spam_global_model_type->SulciRecognition.SPAM_recognition09_global_recognition_model_type")
        self.export_parameter("SulciRecognition", "SPAM_recognition09_global_recognition_model", "SulciRecognition_SPAM_recognition09_global_recognition_model", is_optional=True)
        self.export_parameter("SulciRecognition", "SPAM_recognition09_local_recognition_model", "SulciRecognition_SPAM_recognition09_local_recognition_model", is_optional=True)
        self.export_parameter("SulciRecognition", "SPAM_recognition09_local_recognition_local_referentials", "SulciRecognition_SPAM_recognition09_local_recognition_local_referentials", is_optional=True)
        self.export_parameter("SulciRecognition", "SPAM_recognition09_local_recognition_direction_priors", "SulciRecognition_SPAM_recognition09_local_recognition_direction_priors", is_optional=True)
        self.export_parameter("SulciRecognition", "SPAM_recognition09_local_recognition_angle_priors", "SulciRecognition_SPAM_recognition09_local_recognition_angle_priors", is_optional=True)
        self.export_parameter("SulciRecognition", "SPAM_recognition09_local_recognition_translation_priors", "SulciRecognition_SPAM_recognition09_local_recognition_translation_priors", is_optional=True)
        self.export_parameter("SulciRecognition", "SPAM_recognition09_markovian_recognition_model", "SulciRecognition_SPAM_recognition09_markovian_recognition_model", is_optional=True)
        self.export_parameter("SulciRecognition", "SPAM_recognition09_markovian_recognition_segments_relations_model", "SulciRecognition_SPAM_recognition09_markovian_recognition_segments_relations_model", is_optional=True)
        self.export_parameter("SulciRecognition", "CNN_recognition19_model_file", "SulciRecognition_CNN_recognition19_model_file", is_optional=True)
        self.export_parameter("SulciRecognition", "CNN_recognition19_param_file", "SulciRecognition_CNN_recognition19_param_file", is_optional=True)
        self.export_parameter("SulciRecognition", "CNN_recognition19_cuda", "SulciRecognition_CNN_recognition19_cuda", is_optional=True)
        self.add_link("SulciRecognition_CNN_recognition19_cuda->SulciRecognition_1.CNN_recognition19_cuda")
        self.export_parameter("SulciRecognition_1", "SPAM_recognition09_global_recognition_labels_priors", "SulciRecognition_1_SPAM_recognition09_global_recognition_labels_priors", is_optional=True)
        self.export_parameter("SulciRecognition_1", "SPAM_recognition09_global_recognition_initial_transformation", "SulciRecognition_1_SPAM_recognition09_global_recognition_initial_transformation", is_optional=True)
        self.export_parameter("SulciRecognition_1", "SPAM_recognition09_global_recognition_model", "SulciRecognition_1_SPAM_recognition09_global_recognition_model", is_optional=True)
        self.export_parameter("SulciRecognition_1", "SPAM_recognition09_local_recognition_model", "SulciRecognition_1_SPAM_recognition09_local_recognition_model", is_optional=True)
        self.export_parameter("SulciRecognition_1", "SPAM_recognition09_local_recognition_local_referentials", "SulciRecognition_1_SPAM_recognition09_local_recognition_local_referentials", is_optional=True)
        self.export_parameter("SulciRecognition_1", "SPAM_recognition09_local_recognition_direction_priors", "SulciRecognition_1_SPAM_recognition09_local_recognition_direction_priors", is_optional=True)
        self.export_parameter("SulciRecognition_1", "SPAM_recognition09_local_recognition_angle_priors", "SulciRecognition_1_SPAM_recognition09_local_recognition_angle_priors", is_optional=True)
        self.export_parameter("SulciRecognition_1", "SPAM_recognition09_local_recognition_translation_priors", "SulciRecognition_1_SPAM_recognition09_local_recognition_translation_priors", is_optional=True)
        self.export_parameter("SulciRecognition_1", "SPAM_recognition09_markovian_recognition_model", "SulciRecognition_1_SPAM_recognition09_markovian_recognition_model", is_optional=True)
        self.export_parameter("SulciRecognition_1", "SPAM_recognition09_markovian_recognition_segments_relations_model", "SulciRecognition_1_SPAM_recognition09_markovian_recognition_segments_relations_model", is_optional=True)
        self.export_parameter("SulciRecognition_1", "recognition2000_model", "SulciRecognition_1_recognition2000_model", is_optional=True)
        self.export_parameter("SulciRecognition_1", "CNN_recognition19_model_file", "SulciRecognition_1_CNN_recognition19_model_file", is_optional=True)
        self.export_parameter("SulciRecognition_1", "CNN_recognition19_param_file", "SulciRecognition_1_CNN_recognition19_param_file", is_optional=True)
        self.export_parameter("GlobalMorphometry", "subject", "GlobalMorphometry_subject", is_optional=False)
        self.add_link("GlobalMorphometry_subject->Report.subject")
        self.export_parameter("GlobalMorphometry", "sulci_label_attribute", "GlobalMorphometry_sulci_label_attribute", is_optional=False)
        self.add_link("GlobalMorphometry_sulci_label_attribute->SulcalMorphometry.use_attribute")
        self.export_parameter("GlobalMorphometry", "table_format", "GlobalMorphometry_table_format", is_optional=False)
        self.export_parameter("SulcalMorphometry", "sulci_file", "sulcal_morphometry_sulci_file", is_optional=False)
        self.export_parameter("Report", "normative_brain_stats", "Report_normative_brain_stats", is_optional=True)
        self.export_parameter("Report", "bids", "Report_bids", is_optional=False)
        self.export_parameter("Report", "covariables_file", "Report_covariables_file", is_optional=True)
        self.export_parameter("Report", "covariables", "Report_covariables", is_optional=True)
        self.export_parameter("import_fs", "T1_output", "imported_t1mri", is_optional=False)
        self.add_link("import_fs.T1_output->Report.t1mri")
        self.export_parameter("import_fs", "T1_referential", "t1mri_referential", is_optional=False)
        self.export_parameter("import_fs", "transform_to_scanner_based", is_optional=True)
        self.add_link("import_fs.bias_corrected_output->GreyWhiteTopology_1.t1mri_nobias")
        self.add_link("import_fs.bias_corrected_output->GreyWhiteTopology.t1mri_nobias")
        self.export_parameter("import_fs", "bias_corrected_output", "t1mri_nobias", is_optional=False)
        self.add_link("import_fs.bias_corrected_output->SulciSkeleton_1.t1mri_nobias")
        self.add_link("import_fs.bias_corrected_output->PialMesh_1.t1mri_nobias")
        self.add_link("import_fs.bias_corrected_output->PialMesh¨.t1mri_nobias")
        self.add_link("import_fs.bias_corrected_output->SulciSkeleton.t1mri_nobias")
        self.add_link("import_fs.bias_corrected_output->HeadMesh.t1mri_nobias")
        self.export_parameter("import_fs", "normalization_transformation", "MNI_transform", is_optional=False)
        self.export_parameter("import_fs", "talairach_transform", is_optional=False)
        self.add_link("import_fs.talairach_transform->Report.talairach_transform")
        self.add_link("import_fs.talairach_transform->CorticalFoldsGraph.talairach_transform")
        self.add_link("import_fs.talairach_transform->CorticalFoldsGraph_1.talairach_transform")
        self.add_link("import_fs.commissure_coordinates->CorticalFoldsGraph_1.commissure_coordinates")
        self.export_parameter("import_fs", "commissure_coordinates", is_optional=False)
        self.add_link("import_fs.commissure_coordinates->CorticalFoldsGraph.commissure_coordinates")
        self.export_parameter("import_fs", "histo_analysis", is_optional=False)
        self.add_link("import_fs.histo_analysis->HeadMesh.histo_analysis")
        self.add_link("import_fs.histo_analysis->GreyWhiteTopology_1.histo_analysis")
        self.add_link("import_fs.histo_analysis->GreyWhiteTopology.histo_analysis")
        self.export_parameter("import_fs", "brain_mask_output", "brain_mask_outputBrainSegmentation_brain_mask", is_optional=False)
        self.add_link("import_fs.split_brain_output->GlobalMorphometry.split_brain")
        self.export_parameter("import_fs", "split_brain_output", "split_brain", is_optional=False)
        self.add_link("import_fs.split_brain_output->CorticalFoldsGraph.split_brain")
        self.add_link("import_fs.split_brain_output->CorticalFoldsGraph_1.split_brain")
        self.add_link("import_fs.left_grey_white_output->SulciRecognition.CNN_recognition19_grey_white")
        self.add_link("import_fs.left_grey_white_output->SulciSkeleton.grey_white")
        self.add_link("import_fs.left_grey_white_output->PialMesh¨.grey_white")
        self.add_link("import_fs.left_grey_white_output->GreyWhiteTopology.grey_white")
        self.add_link("import_fs.left_grey_white_output->CorticalFoldsGraph.grey_white")
        self.add_link("import_fs.left_grey_white_output->GlobalMorphometry.left_grey_white")
        self.add_link("import_fs.left_grey_white_output->Report.left_grey_white")
        self.export_parameter("import_fs", "left_grey_white_output", "GreyWhiteClassification_grey_white", is_optional=False)
        self.export_parameter("import_fs", "right_grey_white_output", "GreyWhiteClassification_1_grey_white", is_optional=False)
        self.add_link("import_fs.right_grey_white_output->CorticalFoldsGraph_1.grey_white")
        self.add_link("import_fs.right_grey_white_output->GreyWhiteTopology_1.grey_white")
        self.add_link("import_fs.right_grey_white_output->PialMesh_1.grey_white")
        self.add_link("import_fs.right_grey_white_output->GlobalMorphometry.right_grey_white")
        self.add_link("import_fs.right_grey_white_output->SulciSkeleton_1.grey_white")
        self.add_link("import_fs.right_grey_white_output->Report.right_grey_white")
        self.add_link("import_fs.right_grey_white_output->SulciRecognition_1.CNN_recognition19_grey_white")
        self.export_parameter("HeadMesh", "head_mesh", "HeadMesh_head_mesh", is_optional=False)
        self.export_parameter("HeadMesh", "head_mask", "HeadMesh_head_mask", is_optional=True)
        self.add_link("GreyWhiteTopology.hemi_cortex->CorticalFoldsGraph.hemi_cortex")
        self.add_link("GreyWhiteTopology.hemi_cortex->SulciRecognition.CNN_recognition19_hemi_cortex")
        self.add_link("GreyWhiteTopology.hemi_cortex->SulciSkeleton.hemi_cortex")
        self.add_link("GreyWhiteTopology.hemi_cortex->PialMesh¨.hemi_cortex")
        self.add_link("GreyWhiteTopology.hemi_cortex->GreyWhiteMesh.hemi_cortex")
        self.export_parameter("GreyWhiteTopology", "hemi_cortex", "GreyWhiteTopology_hemi_cortex", is_optional=False)
        self.add_link("GreyWhiteTopology_1.hemi_cortex->SulciRecognition_1.CNN_recognition19_hemi_cortex")
        self.export_parameter("GreyWhiteTopology_1", "hemi_cortex", "GreyWhiteTopology_1_hemi_cortex", is_optional=False)
        self.add_link("GreyWhiteTopology_1.hemi_cortex->GreyWhiteMesh_1.hemi_cortex")
        self.add_link("GreyWhiteTopology_1.hemi_cortex->SulciSkeleton_1.hemi_cortex")
        self.add_link("GreyWhiteTopology_1.hemi_cortex->PialMesh_1.hemi_cortex")
        self.add_link("GreyWhiteTopology_1.hemi_cortex->CorticalFoldsGraph_1.hemi_cortex")
        self.add_link("SulciSkeleton.skeleton->CorticalFoldsGraph.skeleton")
        self.export_parameter("SulciSkeleton", "skeleton", "SulciSkeleton_skeleton", is_optional=False)
        self.add_link("SulciSkeleton.skeleton->SulciRecognition.CNN_recognition19_skeleton")
        self.add_link("SulciSkeleton.skeleton->PialMesh¨.skeleton")
        self.export_parameter("SulciSkeleton", "roots", "SulciSkeleton_roots", is_optional=False)
        self.add_link("SulciSkeleton.roots->SulciRecognition.CNN_recognition19_roots")
        self.add_link("SulciSkeleton.roots->CorticalFoldsGraph.roots")
        self.add_link("SulciSkeleton_1.skeleton->CorticalFoldsGraph_1.skeleton")
        self.add_link("SulciSkeleton_1.skeleton->SulciRecognition_1.CNN_recognition19_skeleton")
        self.add_link("SulciSkeleton_1.skeleton->PialMesh_1.skeleton")
        self.export_parameter("SulciSkeleton_1", "skeleton", "SulciSkeleton_1_skeleton", is_optional=False)
        self.export_parameter("SulciSkeleton_1", "roots", "sulciSkeleton_1_roots", is_optional=False)
        self.add_link("SulciSkeleton_1.roots->CorticalFoldsGraph_1.roots")
        self.add_link("SulciSkeleton_1.roots->SulciRecognition_1.CNN_recognition19_roots")
        self.add_link("GreyWhiteMesh.white_mesh->GlobalMorphometry.left_wm_mesh")
        self.add_link("GreyWhiteMesh.white_mesh->Report.left_wm_mesh")
        self.add_link("GreyWhiteMesh.white_mesh->SulciRecognition.CNN_recognition19_white_mesh")
        self.export_parameter("GreyWhiteMesh", "white_mesh", "GreyWhiteMesh_white_mesh", is_optional=False)
        self.add_link("GreyWhiteMesh.white_mesh->CorticalFoldsGraph.white_mesh")
        self.export_parameter("GreyWhiteMesh_1", "white_mesh", "GreyWhiteMesh_1_white_mesh", is_optional=False)
        self.add_link("GreyWhiteMesh_1.white_mesh->CorticalFoldsGraph_1.white_mesh")
        self.add_link("GreyWhiteMesh_1.white_mesh->GlobalMorphometry.right_wm_mesh")
        self.add_link("GreyWhiteMesh_1.white_mesh->Report.right_wm_mesh")
        self.add_link("GreyWhiteMesh_1.white_mesh->SulciRecognition_1.CNN_recognition19_white_mesh")
        self.add_link("PialMesh¨.pial_mesh->CorticalFoldsGraph.pial_mesh")
        self.add_link("PialMesh¨.pial_mesh->GlobalMorphometry.left_gm_mesh")
        self.export_parameter("PialMesh¨", "pial_mesh", "PialMesh_pial_mesh", is_optional=False)
        self.add_link("PialMesh¨.pial_mesh->Report.left_gm_mesh")
        self.add_link("PialMesh¨.pial_mesh->SulciRecognition.CNN_recognition19_pial_mesh")
        self.add_link("PialMesh_1.pial_mesh->CorticalFoldsGraph_1.pial_mesh")
        self.add_link("PialMesh_1.pial_mesh->SulciRecognition_1.CNN_recognition19_pial_mesh")
        self.add_link("PialMesh_1.pial_mesh->GlobalMorphometry.right_gm_mesh")
        self.add_link("PialMesh_1.pial_mesh->Report.right_gm_mesh")
        self.export_parameter("PialMesh_1", "pial_mesh", "PialMesh_1_pial_mesh", is_optional=False)
        self.add_link("CorticalFoldsGraph.graph->SulciRecognition.data_graph")
        self.export_parameter("CorticalFoldsGraph", "graph", "left_graph", is_optional=False)
        self.export_parameter("CorticalFoldsGraph", "sulci_voronoi", "CorticalFoldsGraph_sulci_voronoi", is_optional=False)
        self.export_parameter("CorticalFoldsGraph", "cortex_mid_interface", "CorticalFoldsGraph_cortex_mid_interface", is_optional=True)
        self.add_link("CorticalFoldsGraph_1.graph->SulciRecognition_1.data_graph")
        self.export_parameter("CorticalFoldsGraph_1", "graph", "right_graph", is_optional=False)
        self.export_parameter("CorticalFoldsGraph_1", "sulci_voronoi", "CorticalFoldsGraph_1_sulci_voronoi", is_optional=False)
        self.export_parameter("CorticalFoldsGraph_1", "cortex_mid_interface", "CorticalFoldsGraph_1_cortex_mid_interface", is_optional=True)
        self.add_link("SulciRecognition.output_graph->SulcalMorphometry.left_sulci_graph")
        self.export_parameter("SulciRecognition", "output_graph", "left_labelled_graph", is_optional=False)
        self.add_link("SulciRecognition.output_graph->Report.left_labelled_graph")
        self.add_link("SulciRecognition.output_graph->GlobalMorphometry.left_labelled_graph")
        self.export_parameter("SulciRecognition", "recognition2000_energy_plot_file", "SulciRecognition_recognition2000_energy_plot_file", is_optional=True)
        self.export_parameter("SulciRecognition", "SPAM_recognition09_global_recognition_posterior_probabilities", "SulciRecognition_SPAM_recognition09_global_recognition_posterior_probabilities", is_optional=True)
        self.export_parameter("SulciRecognition", "SPAM_recognition09_global_recognition_output_transformation", "SulciRecognition_SPAM_recognition09_global_recognition_output_transformation", is_optional=True)
        self.export_parameter("SulciRecognition", "SPAM_recognition09_global_recognition_output_t1_to_global_transformation", "SulciRecognition_SPAM_recognition09_global_recognition_output_t1_to_global_transformation", is_optional=True)
        self.export_parameter("SulciRecognition", "SPAM_recognition09_local_recognition_posterior_probabilities", "SulciRecognition_SPAM_recognition09_local_recognition_posterior_probabilities", is_optional=True)
        self.export_parameter("SulciRecognition", "SPAM_recognition09_local_recognition_output_local_transformations", "SulciRecognition_SPAM_recognition09_local_recognition_output_local_transformations", is_optional=True)
        self.export_parameter("SulciRecognition", "SPAM_recognition09_markovian_recognition_posterior_probabilities", "SulciRecognition_SPAM_recognition09_markovian_recognition_posterior_probabilities", is_optional=True)
        self.export_parameter("SulciRecognition_1", "output_graph", "right_labelled_graph", is_optional=False)
        self.add_link("SulciRecognition_1.output_graph->Report.right_labelled_graph")
        self.add_link("SulciRecognition_1.output_graph->SulcalMorphometry.right_sulci_graph")
        self.add_link("SulciRecognition_1.output_graph->GlobalMorphometry.right_labelled_graph")
        self.export_parameter("SulciRecognition_1", "recognition2000_energy_plot_file", "SulciRecognition_1_recognition2000_energy_plot_file", is_optional=True)
        self.export_parameter("SulciRecognition_1", "SPAM_recognition09_global_recognition_posterior_probabilities", "SulciRecognition_1_SPAM_recognition09_global_recognition_posterior_probabilities", is_optional=True)
        self.export_parameter("SulciRecognition_1", "SPAM_recognition09_global_recognition_output_transformation", "SulciRecognition_1_SPAM_recognition09_global_recognition_output_transformation", is_optional=True)
        self.export_parameter("SulciRecognition_1", "SPAM_recognition09_global_recognition_output_t1_to_global_transformation", "SulciRecognition_1_SPAM_recognition09_global_recognition_output_t1_to_global_transformation", is_optional=True)
        self.export_parameter("SulciRecognition_1", "SPAM_recognition09_local_recognition_posterior_probabilities", "SulciRecognition_1_SPAM_recognition09_local_recognition_posterior_probabilities", is_optional=True)
        self.export_parameter("SulciRecognition_1", "SPAM_recognition09_local_recognition_output_local_transformations", "SulciRecognition_1_SPAM_recognition09_local_recognition_output_local_transformations", is_optional=True)
        self.export_parameter("SulciRecognition_1", "SPAM_recognition09_markovian_recognition_posterior_probabilities", "SulciRecognition_1_SPAM_recognition09_markovian_recognition_posterior_probabilities", is_optional=True)
        self.export_parameter("SulcalMorphometry", "sulcal_morpho_measures", is_optional=False)
        self.export_parameter("GlobalMorphometry", "left_csf", "GlobalMorphometry_left_csf", is_optional=False)
        self.export_parameter("GlobalMorphometry", "right_csf", "GlobalMorphometry_right_csf", is_optional=False)
        self.add_link("GlobalMorphometry.brain_volumes_file->Report.brain_volumes_file")
        self.export_parameter("GlobalMorphometry", "brain_volumes_file", "GlobalMorphometry_brain_volumes_file", is_optional=False)
        self.export_parameter("Report", "report", "Report_report", is_optional=False)
        self.export_parameter("Report", "report_json", "Report_report_json", is_optional=True)
        self.export_parameter("Report", "inter_subject_qc_table", "Report_inter_subject_qc_table", is_optional=True)

        # parameters order

        self.reorder_traits(("T1_orig", "ribbon_image", "scanner_based_referential", "Talairach_Auto", "mni_referential", "transform_chain_ACPC_to_Normalized", "acpc_referential", "allow_multithreading", "imported_t1mri", "commissure_coordinates", "talairach_transform", "t1mri_nobias", "histo_analysis", "brain_mask_outputBrainSegmentation_brain_mask", "split_brain", "HeadMesh_head_mesh", "GreyWhiteClassification_grey_white", "GreyWhiteClassification_1_grey_white", "GreyWhiteTopology_hemi_cortex", "GreyWhiteTopology_1_hemi_cortex", "GreyWhiteMesh_white_mesh", "GreyWhiteMesh_1_white_mesh", "SulciSkeleton_skeleton", "SulciSkeleton_1_skeleton", "PialMesh_pial_mesh", "PialMesh_1_pial_mesh", "left_graph", "right_graph", "left_labelled_graph", "right_labelled_graph", "sulcal_morpho_measures", "t1mri_referential", "MNI_transform", "HeadMesh_head_mask", "HeadMesh_remove_mask", "HeadMesh_first_slice", "HeadMesh_threshold", "HeadMesh_closing", "HeadMesh_threshold_mode", "HeadMesh_keep_head_mask", "GreyWhiteTopology_version", "fix_random_seed", "SulciSkeleton_version", "PialMesh_version", "GlobalMorphometry_left_csf", "GlobalMorphometry_right_csf", "GlobalMorphometry_brain_volumes_file", "Report_report", "Report_report_json", "Report_inter_subject_qc_table", "SulciSkeleton_roots", "sulciSkeleton_1_roots", "compute_fold_meshes", "CorticalFoldsGraph_graph_version", "CorticalFoldsGraph_write_cortex_mid_interface", "CorticalFoldsGraph_sulci_voronoi", "CorticalFoldsGraph_cortex_mid_interface", "CorticalFoldsGraph_1_sulci_voronoi", "CorticalFoldsGraph_1_cortex_mid_interface", "select_Sulci_Recognition", "SulciRecognition_recognition2000_model", "sulci_recognition2000_model_hint", "sulci_recognition2000_rate", "sulci_recognition2000_stop_rate", "sulci_recognition2000_niter_below_stop_prop", "sulci_recognition2000_forbid_unknown_label", "sulci_recognition_spam_local_or_markovian", "SPAM_recognition_labels_translation_map", "SulciRecognition_SPAM_recognition09_global_recognition_labels_priors", "SulcalRecognition_SPAM_recognition09_global_recognition_initial_transformation", "sulci_recognition_spam_global_model_type", "SulciRecognition_SPAM_recognition09_global_recognition_model", "SulciRecognition_SPAM_recognition09_local_recognition_model", "SulciRecognition_SPAM_recognition09_local_recognition_local_referentials", "SulciRecognition_SPAM_recognition09_local_recognition_direction_priors", "SulciRecognition_SPAM_recognition09_local_recognition_angle_priors", "SulciRecognition_SPAM_recognition09_local_recognition_translation_priors", "SulciRecognition_SPAM_recognition09_markovian_recognition_model", "SulciRecognition_SPAM_recognition09_markovian_recognition_segments_relations_model", "SulciRecognition_CNN_recognition19_model_file", "SulciRecognition_CNN_recognition19_param_file", "SulciRecognition_CNN_recognition19_cuda", "SulciRecognition_recognition2000_energy_plot_file", "SulciRecognition_SPAM_recognition09_global_recognition_posterior_probabilities", "SulciRecognition_SPAM_recognition09_global_recognition_output_transformation", "SulciRecognition_SPAM_recognition09_global_recognition_output_t1_to_global_transformation", "SulciRecognition_SPAM_recognition09_local_recognition_posterior_probabilities", "SulciRecognition_SPAM_recognition09_local_recognition_output_local_transformations", "SulciRecognition_SPAM_recognition09_markovian_recognition_posterior_probabilities", "SulciRecognition_1_SPAM_recognition09_global_recognition_labels_priors", "SulciRecognition_1_SPAM_recognition09_global_recognition_initial_transformation", "SulciRecognition_1_SPAM_recognition09_global_recognition_model", "SulciRecognition_1_SPAM_recognition09_local_recognition_model", "SulciRecognition_1_SPAM_recognition09_local_recognition_local_referentials", "SulciRecognition_1_SPAM_recognition09_local_recognition_direction_priors", "SulciRecognition_1_SPAM_recognition09_local_recognition_angle_priors", "SulciRecognition_1_SPAM_recognition09_local_recognition_translation_priors", "SulciRecognition_1_SPAM_recognition09_markovian_recognition_model", "SulciRecognition_1_SPAM_recognition09_markovian_recognition_segments_relations_model", "SulciRecognition_1_recognition2000_model", "SulciRecognition_1_CNN_recognition19_model_file", "SulciRecognition_1_CNN_recognition19_param_file", "SulciRecognition_1_recognition2000_energy_plot_file", "SulciRecognition_1_SPAM_recognition09_global_recognition_posterior_probabilities", "SulciRecognition_1_SPAM_recognition09_global_recognition_output_transformation", "SulciRecognition_1_SPAM_recognition09_global_recognition_output_t1_to_global_transformation", "SulciRecognition_1_SPAM_recognition09_local_recognition_posterior_probabilities", "SulciRecognition_1_SPAM_recognition09_local_recognition_output_local_transformations", "SulciRecognition_1_SPAM_recognition09_markovian_recognition_posterior_probabilities", "GlobalMorphometry_subject", "GlobalMorphometry_sulci_label_attribute", "GlobalMorphometry_table_format", "sulcal_morphometry_sulci_file", "Report_normative_brain_stats", "Report_bids", "Report_covariables_file", "Report_covariables", "transform_to_scanner_based"))

        # default and initial values
        self.allow_multithreading = True
        self.imported_t1mri = '/tmp/input_data/sub-rototo/ses-0/run-0/sub-rototo_ses-0_run-0_T1w.nii.gz'
        self.talairach_transform = '/tmp/input_data/sub-rototo/ses-0/run-0/registration/sub-rototo_ses-0_run-0_T1w_TO_Talairach-ACPC.trm'
        self.split_brain = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/segmentation/sub-rototo_ses-0_run-0_voronoi.nii.gz'
        self.GreyWhiteClassification_grey_white = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/segmentation/sub-rototo_ses-0_run-0_hemi-L_grey_white.nii.gz'
        self.GreyWhiteClassification_1_grey_white = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-R_grey_white.nii.gz'
        self.GreyWhiteMesh_white_mesh = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-L_white.surf.gii'
        self.GreyWhiteMesh_1_white_mesh = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-R_white.surf.gii'
        self.PialMesh_pial_mesh = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-L_pial.surf.gii'
        self.PialMesh_1_pial_mesh = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/mesh/sub-rototo_ses-0_run-0_hemi-R_pial.surf.gii'
        self.left_labelled_graph = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-L_auto.arg'
        self.right_labelled_graph = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/folds/3.1/sul-0_auto/sub-rototo_ses-0_run-0_sul-0_hemi-R_auto.arg'
        self.GreyWhiteTopology_version = '2'
        self.SulciSkeleton_version = '2'
        self.PialMesh_version = '2'
        self.GlobalMorphometry_left_csf = '/tmp/output_data/sub-rototo/ses-0/run-0/ana-tutu/segmentation/sub-rototo_ses-0_run-0_hemi-L_csf.nii.gz'
        self.GlobalMorphometry_right_csf = '/tmp/output_data/sub-rototo/ses-0/run-0/ana-tutu/segmentation/sub-rototo_ses-0_run-0_hemi-R_csf.nii.gz'
        self.GlobalMorphometry_brain_volumes_file = '/tmp/input_data/sub-rototo/ses-0/run-0/ana-tutu/segmentation/sub-rototo_ses-0_run-0_brain_volumes.csv'
        self.Report_report = '/tmp/output_data/sub-rototo/ses-0/run-0/ana-tutu/sub-rototo_ses-0_run-0_morphologist_report.pdf'
        self.Report_report_json = '/tmp/output_data/sub-rototo/ses-0/run-0/ana-tutu/sub-rototo_ses-0_run-0_morphologist_report.json'
        self.Report_inter_subject_qc_table = '/tmp/output_data/qc/qc.tsv'
        self.compute_fold_meshes = True
        self.CorticalFoldsGraph_graph_version = '3.1'
        self.select_Sulci_Recognition = 'CNN_recognition19'
        self.SulciRecognition_recognition2000_model = '/volatile/home/dr144257/brainvisa-sf-master/build/share/brainvisa-share-5.2/models/models_2008/discriminative_models/3.0/Rfolds_noroots/Rfolds_noroots.arg'
        self.sulci_recognition2000_rate = 0.98
        self.sulci_recognition2000_stop_rate = 0.05
        self.sulci_recognition2000_niter_below_stop_prop = 1
        self.SPAM_recognition_labels_translation_map = '/volatile/home/dr144257/brainvisa-sf-master/build/share/brainvisa-share-5.2/nomenclature/translation/sulci_model_2008.trl'
        self.sulci_recognition_spam_global_model_type = 'Global registration'
        self.SulciRecognition_1_recognition2000_model = '/volatile/home/dr144257/brainvisa-sf-master/build/share/brainvisa-share-5.2/models/models_2008/discriminative_models/3.0/Rfolds_noroots/Rfolds_noroots.arg'
        self.GlobalMorphometry_subject = 'rototo'
        self.sulcal_morphometry_sulci_file = '/volatile/home/dr144257/brainvisa-sf-master/build/share/brainvisa-share-5.2/nomenclature/translation/sulci_default_list.json'
        self.Report_normative_brain_stats = '/volatile/home/dr144257/brainvisa-6.0/build/share/brainvisa-share-6.0/normative_tables/morphologist/ukb_hcp/morphologist_normative_brain_volumes_stats.json'

        # nodes positions
        self.node_position = {
            "import_fs": (-622.4744914375725, -52.8320541854967),
            "inputs": (-1327.5253390024586, 7.14015322191085),
            "HeadMesh": (-119.0, 696.0),
            "GreyWhiteTopology": (297.8, 357.6),
            "GreyWhiteTopology_1": (249.80000000000007, 710.3999999999999),
            "SulciSkeleton": (621.3999999999999, -264.12991999999997),
            "SulciSkeleton_1": (593.0, 954.0),
            "GreyWhiteMesh": (626.9999999999999, 57.0),
            "GreyWhiteMesh_1": (596.6, 662.5999999999998),
            "PialMesh¨": (927.8666666666666, 339.33333333333326),
            "PialMesh_1": (946.2, 753.8000000000001),
            "CorticalFoldsGraph": (1271.2400000000005, -547.0000000000001),
            "CorticalFoldsGraph_1": (1289.0960000000002, 937.856),
            "SulciRecognition": (1773.2689208888887, -277.7103111111104),
            "SulciRecognition_1": (1748.0213119999999, 1441.949248),
            "SulcalMorphometry": (2903.439168, 1094.5779839999998),
            "GlobalMorphometry": (2940.098222222223, 124.7693333333334),
            "Report": (3357.4592711111127, 473.6364088888881),
            "outputs": (3780.6555179185593, 114.65120000000002),
        }

        # nodes dimensions
        self.node_dimension = {
            "import_fs": (428.640625, 460.0),
            "inputs": (549.671875, 2315.0),
            "HeadMesh": (197.640625, 320.0),
            "GreyWhiteTopology": (200.78125, 215.0),
            "GreyWhiteTopology_1": (200.78125, 215.0),
            "SulciSkeleton": (179.1875, 215.0),
            "SulciSkeleton_1": (179.1875, 215.0),
            "GreyWhiteMesh": (172.59375, 75.0),
            "GreyWhiteMesh_1": (172.59375, 75.0),
            "PialMesh¨": (190.625, 250.0),
            "PialMesh_1": (190.625, 250.0),
            "CorticalFoldsGraph": (311.171875, 495.0),
            "CorticalFoldsGraph_1": (311.171875, 495.0),
            "SulciRecognition": (867.53125, 1160.0),
            "SulciRecognition_1": (867.53125, 1160.0),
            "SulcalMorphometry": (274.953125, 180.0),
            "GlobalMorphometry": (264.671875, 460.0),
            "Report": (296.5, 600.0),
            "outputs": (565.578125, 1895.0),
        }

        self.do_autoexport_nodes_parameters = False
