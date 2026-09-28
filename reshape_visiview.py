# /// script
# requires-python = ">=3.11"
# dependencies = []
#
# [tool.pixi.dependencies]
# cyclopts = "*"
# ome-types = "*"
# ///

from pathlib import Path

import cyclopts
from ome_types import from_xml, to_xml
from ome_types.model import Image

app = cyclopts.App()

@app.default
def main(
    companion: Path,
    /,
    *,
    size_t: int | None = None,
    size_z: int | None = None,
    suffix: str = "_reshaped",
    dry_run: bool = False
):
    """Rewrite metadata of a Visiview companion.ome file.
    
    You can set new sizes in z and t.

    Parameters
    ----------
    companion : Path
        The path to the Visiview companion.ome file.
    size_t : int | None, optional
        The new size for the t dimension, by default None.
    size_z : int | None, optional
        The new size for the z dimension, by default None.
    suffix : str, optional
        The suffix to add to the reshaped file, by default "_reshaped".
    dry_run : bool, optional
        If True, only print the changes without modifying the file, by default False.
    """
    assert companion.exists(), "The specified companion file does not exist."
    ome = from_xml(companion.read_text())

    for image_index, image in enumerate(ome.images):
        image_dict = image.model_dump()
        if size_t is not None:
            image_dict["pixels"]["size_t"] = size_t
        if size_z is not None:
            image_dict["pixels"]["size_z"] = size_z
        print(f"Updating image {image_index} with: {image_dict['pixels']['size_t']=}, {image_dict['pixels']['size_z']=}")
        ome.images[image_index] = Image(**image_dict)

    if not dry_run:
        new_file = companion.with_name(companion.stem + suffix + companion.suffix)
        new_file.write_text(to_xml(ome))
    else:
        print(f"Dry run enabled. Would write updated OME file to: {companion.with_name(companion.stem + suffix + companion.suffix)}")


if __name__ == "__main__":
    app()
