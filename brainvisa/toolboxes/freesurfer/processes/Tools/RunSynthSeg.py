import os
import shutil

from brainvisa.processes import Boolean, Integer, ReadDiskItem, Signature, String, WriteDiskItem
from freesurfer.brainvisaFreesurfer import testFreesurferCommand

name = "Run SynthSeg"
userLevel = 1

synthseg_options = "SynthSeg options"
optional_outputs = "Optional outputs"

default_format = ["gz compressed NIFTI-1 image", "NIFTI-1 image"]

# fmt: off
signature = Signature(
    # Input
    "t1mri", ReadDiskItem("Raw T1 MRI", default_format),

    # Output folder
    "output_folder", WriteDiskItem("Acquisition", "Directory", requiredAttributes={"modality": "synthSeg"}),

    # Main output
    "segmentation", WriteDiskItem("SynthSeg segmentation", default_format,
                                  requiredAttributes={"modality": "synthSeg"}),

    # Optional outputs
    "volumes_csv", WriteDiskItem("SynthSeg volumes", "CSV file", section=optional_outputs,
                                 requiredAttributes={"modality": "synthSeg"}),
    "qc_csv", WriteDiskItem("QC Table", "CSV file", section=optional_outputs,
                            requiredAttributes={"modality": "synthSeg"}),
    "posterior", WriteDiskItem("Tissue probability map", default_format,
                               section=optional_outputs, requiredAttributes={"modality": "synthSeg"}),
    "resampled", WriteDiskItem("SynthSeg resampled", default_format,
                               section=optional_outputs, requiredAttributes={"modality": "synthSeg"}),
    "execution_log", WriteDiskItem("SynthSeg execution log", "JSON file", section=optional_outputs,
                                   requiredAttributes={"modality": "synthSeg"}),

    # SynthSeg options
    "parc", Boolean(section=synthseg_options),
    "robust", Boolean(section=synthseg_options),
    "fast", Boolean(section=synthseg_options),
    "crop", String(section=synthseg_options),
    "threads", Integer(section=synthseg_options),
    "cpu", Boolean(section=synthseg_options),
    "v1", Boolean(section=synthseg_options),
    "overwrite", Boolean(section=synthseg_options)
)
# fmt: on


def validation():
    testFreesurferCommand()


def initialization(self):
    # Set defaults matching SynthSeg
    self.threads = 1
    self.cpu = False
    self.robust = False
    self.fast = False
    self.parc = False
    self.v1 = False
    self.overwrite = False

    # Make optional outputs optional
    self.setOptional("volumes_csv", "qc_csv", "posterior", "resampled", "crop")

    # Link outputs to folder
    self.addLink("output_folder", "t1mri")
    self.addLink("segmentation", "output_folder", self.update_output)
    self.addLink("volumes_csv", "output_folder")
    self.addLink("qc_csv", "output_folder")
    self.addLink("posterior", "output_folder")
    self.addLink("resampled", "output_folder")
    self.addLink("execution_log", "output_folder")

    self.addLink(None, "parc", self.update_output_type)

    # Set user levels for advanced options
    self.setUserLevel(2, "parc", "robust", "fast", "crop", "threads", "cpu", "v1", "overwrite")


def update_output_type(self, parc):
    seg_type = self.signature["segmentation"].type

    if parc and str(seg_type) != "SynthSeg parcellation":
        self.signature["segmentation"].type = WriteDiskItem("SynthSeg parcellation", default_format).type
    elif not parc and str(seg_type) != "SynthSeg segmentation":
        self.signature["segmentation"].type = WriteDiskItem("SynthSeg segmentation", default_format).type
    else:
        return

    self.changeSignature(self.signature)
    self.update_output()


def update_output(self, *_):
    if self.output_folder:
        return self.signature["segmentation"].findValue(self.output_folder.hierarchyAttributes())
    return


def execution(self, context):
    # Check if output folder is empty
    output_dir = self.output_folder.fullPath()
    os.makedirs(output_dir, exist_ok=True)

    # Check if directory is empty
    if os.listdir(output_dir):
        if self.overwrite:
            shutil.rmtree(output_dir)
            os.makedirs(output_dir, exist_ok=True)
        else:
            context.error(
                f"Output directory '{output_dir}' is not empty. SynthSeg has already been launched for this subject and timepoint. "
                "Please remove these results or choose the overwrite option to do so."
            )
            raise RuntimeError(f"Output directory '{output_dir}' is not empty.")

    context.runProcess(
        "RunSynthSeg_generic",
        t1mri=self.t1mri,
        output_folder=self.output_folder,
        segmentation=self.segmentation,
        volumes_csv=self.volumes_csv,
        qc_csv=self.qc_csv,
        posterior=self.posterior,
        resampled=self.resampled,
        execution_log=self.execution_log,
        parc=self.parc,
        robust=self.robust,
        fast=self.fast,
        crop=self.crop,
        threads=self.threads,
        cpu=self.cpu,
        v1=self.v1,
        overwrite=self.overwrite,
    )
