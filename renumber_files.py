# /// script
# requires-python = ">=3.11"
# dependencies = []
#
# [tool.pixi.dependencies]
# cyclopts = "*"
# ///

# Renumber a list of files, given a pattern and an offset number.

import re
from pathlib import Path

import cyclopts

app = cyclopts.App()

@app.default
def main(
    folder: Path,
    /,
    *,
    offset: int,
    pattern: str = r".*_t(\d+)\.[a-zA-Z0-9]{3}",
    dry_run: bool = False,
):
    """Renumber a list of files, adding an offset to a number group in the filename.
    Parameters
    ----------
    folder : Path
        The folder containing the files to renumber.
    offset : int
        The offset to add to the number group in the filename.
    pattern : str, optional
        The pattern to identify the number group in the filename"
    dry_run : bool, optional
        If True, only print the changes without renaming the files, by default False.
    
    """
    files = sorted(folder.glob("*"))
    matches = []
    for file in files:
        match = re.match(pattern, file.name)
        if match:
            number = int(match.group(1))
            start, end = match.span(1)
            matches.append((number, start, end, file))

    # process in an order that never lets a renamed file collide with an unrenamed one
    matches.sort(key=lambda m: m[0], reverse=offset > 0)

    for number, start, end, file in matches:
        new_number = number + offset
        new_name = file.name[:start] + str(new_number) + file.name[end:]
        if dry_run:
            print(f"{file.name} -> {new_name}")
        else:
            file.rename(file.with_name(new_name))

if __name__ == "__main__":
    app()
