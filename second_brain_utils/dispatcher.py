import os.path
from pathlib import Path

import yaml

from second_brain_utils.obsidian_constants import PROPERTY_SECTION_DELIMITER


def split_notes_by_branch(notes: list) -> dict[str, list]:
    # Accross all notes, retrieve the list of uniques branches, knowing each note can have multiple branches
    all_branches = {branch for note in notes for branch in note["properties"].get("branches")}

    notes_by_branch = {}

    for branch in all_branches:
        notes_by_branch[branch] = [note for note in notes if branch in note["properties"].get("branches")]
    return notes_by_branch


def dispatch_notes_by_branch(notes_by_branch: dict[str, list], target_dispatch_dir: str) -> None:
    # Create the target directory if it does not exist
    Path(target_dispatch_dir).mkdir(parents=True, exist_ok=True)

    # Dispatch and transfer the notes in the branch directories
    for branch, notes in notes_by_branch.items():
        # Create the branch directory
        Path(os.path.join(target_dispatch_dir, branch)).mkdir(parents=True, exist_ok=True)

        # Dump all notes associated to this branch
        for note in notes:
            with open(os.path.join(target_dispatch_dir, branch, note["filename"]), mode="w") as note_file:
                # Dumping the properties first, correctly delimited
                note_file.write(PROPERTY_SECTION_DELIMITER)
                yaml.dump(data=note["properties"], stream=note_file, sort_keys=False, indent=2, allow_unicode=True)
                note_file.write(PROPERTY_SECTION_DELIMITER)
                note_file.writelines(note["content"])
