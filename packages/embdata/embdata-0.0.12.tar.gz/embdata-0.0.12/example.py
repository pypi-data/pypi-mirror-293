from datasets import get_dataset_config_names, load_dataset
import pandas as pd
from embdata import describe
from embdata import Episode

def get_oxe_metadata(dataset_name: str = "utokyo_xarm_pick_and_place_converted_externally_to_rlds") -> dict:
    path = "oxe.csv"
    oxe_dataset_metadata = pd.read_csv(path)

    if dataset_name not in oxe_dataset_metadata["Registered Dataset Name"].values:  # noqa: PD011
        raise ValueError(f"Dataset {dataset_name} not found in OXE Overview metadata.")  # noqa

    return oxe_dataset_metadata[oxe_dataset_metadata["Registered Dataset Name"] == dataset_name].to_dict(
        orient="records",
    )[0]


# e.trajectory().plot().show()

repo = "jxu124/OpenX-Embodiment"
config_names = get_dataset_config_names(repo)

for m in config_names:
    metadata = get_oxe_metadata(m)
for name in ["taco_play"]:
    m = get_oxe_metadata(name)
    ds = load_dataset(repo, "taco_play", split="train[:2]")

    describe(ds, show=True)
    e = Episode(ds)
    describe(e, show=True)
    e.dataset().push_to_hub(
        "mbodiai/OpenX-Embodiment", name,
        private=True,
        token="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",
    )

    try:
        e.trajectory().plot().save(f"{name}.png")
    except Exception as e:


    input("Press Enter to continue...")
