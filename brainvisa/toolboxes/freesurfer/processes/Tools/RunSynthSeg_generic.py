import os
import shutil
import json
from pathlib import Path

from brainvisa.processes import Boolean, Integer, ReadDiskItem, Signature, String, WriteDiskItem
from freesurfer.brainvisaFreesurfer import launchFreesurferCommand, testFreesurferCommand

name = "Run SynthSeg generic"
userLevel = 1

synthseg_options = "SynthSeg options"
optional_outputs = "Optional outputs"

default_format = ["gz compressed NIFTI-1 image", "NIFTI-1 image"]

# fmt: off
signature = Signature(
    # Input
    "t1mri", ReadDiskItem("4D Volume", default_format),

    # Output folder
    "output_folder", WriteDiskItem("Directory", "Directory"),

    # Main output
    "segmentation", WriteDiskItem("4D Volume", default_format),

    # Optional outputs
    "volumes_csv", WriteDiskItem("CSV file", "CSV file", section=optional_outputs),
    "qc_csv", WriteDiskItem("CSV file", "CSV file", section=optional_outputs),
    "posterior", WriteDiskItem("4D Volume", default_format,
                               section=optional_outputs),
    "resampled", WriteDiskItem("4D Volume", default_format,
                               section=optional_outputs),
    "execution_log", WriteDiskItem("Any Type", "JSON file", section=optional_outputs),

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

    # Set user levels for advanced options
    self.setUserLevel(2, "parc", "robust", "fast", "crop", "threads", "cpu", "v1", "overwrite")


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
                f"Output directory '{output_dir}' is not empty. SynthSeg has already been launched for this subjet and timepoint. "
                "Please remove these results or choose overwrtie option to do so."
            )
            raise AttributeError()

    # Build command
    cmd = ["mri_synthseg", "--i", self.t1mri, "--o", self.segmentation]

    # Add optional flags
    if self.parc:
        cmd.append("--parc")
    if self.robust:
        cmd.append("--robust")
    if self.fast:
        cmd.append("--fast")
    if self.cpu:
        cmd.append("--cpu")
    if self.v1:
        cmd.append("--v1")
    if self.threads:
        cmd.extend(["--threads", str(self.threads)])
    if self.crop:
        cmd.extend(["--crop"] + self.crop.split())
    if self.volumes_csv:
        cmd.extend(["--vol", self.volumes_csv])
    if self.qc_csv:
        cmd.extend(["--qc", self.qc_csv])
    if self.posterior:
        cmd.extend(["--post", self.posterior])
    if self.resampled:
        cmd.extend(["--resample", self.resampled])

    if self.execution_log:
        exec_json = {
            "process": "synthSeg",
            "parameters": {
                "inputs": {
                    "t1mri": self.t1mri.fullPath()
                },
                "outputs": {
                    "segmentation": self.segmentation.fullPath(),
                    "volumes_csv": self.volumes_csv.fullPath() if self.volumes_csv else None,
                    "qc_csv": self.qc_csv.fullPath() if self.qc_csv else None,
                    "posterior": self.posterior.fullPath() if self.posterior else None,
                    "resampled": self.resampled.fullPath() if self.resampled else None,
                },
                "robust": self.robust,
                "parc": self.parc,
                "fast": self.fast,
                "crop": self.crop,
                "v1": self.v1,
                "threads": self.threads,
                "cpu": self.cpu,
                "command": " ".join(str(c) for c in cmd)
            }
        }

        with open(self.execution_log.fullPath(), "w") as json_file:
            json.dump(exec_json, json_file)
    
    launchFreesurferCommand(context, None, *cmd)
