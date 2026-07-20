include('base')
#include('anatomy')

insert('{center}/{subject}',
    "synthSeg", SetWeakAttr("modality", "synthSeg"), SetContent(
        "{acquisition}",
        SetType("Acquisition"),
        SetDefaultAttributeValue("acquisition", default_acquisition),
        SetContent(
            "<subject>_segmentation", SetType("SynthSeg segmentation"),
            "<subject>_parcellation", SetType("SynthSeg parcellation"),
            "<subject>_volumes", SetType("SynthSeg volumes"),
            "<subject>_qc", SetType("QC Table"),
            "<subject>_posterior", SetType("Tissue probability map"),
            "<subject>_resampled", SetType("SynthSeg resampled"),
            "<subject>_report", SetType("Analysis Report"),
            "<subject>_execution", SetType("SynthSeg execution log"),
        ),
    ),
)