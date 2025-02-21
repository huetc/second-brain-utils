import os.path
from pathlib import Path

from second_brain_utils.exporter import export_notes


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
        # Dump all notes associated to this branch
        export_notes(notes, os.path.join(target_dispatch_dir, branch))
