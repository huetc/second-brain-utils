import glob
import os.path
from datetime import datetime

import yaml

SOURCE_DIRECTORY = "../second-brain/second-brain-raw"
# SOURCE_DIRECTORY = "./tmp"

PROPERTY_SECTION_DELIMITER = "---\n"

REF_DATE = datetime(2025, 2, 18, 0)
DT_FORMAT = "%Y-%m-%dT%H:%M:%S"


def parse_note(source_path: str) -> dict[str, dict[str, str | list[str]] | list[str]]:
    # Parse the file and separate the properties from the content
    with open(source_path) as input_f:
        first_line = input_f.readline()
        property_lines = []
        if first_line == PROPERTY_SECTION_DELIMITER:
            next_line = input_f.readline()
            while next_line != PROPERTY_SECTION_DELIMITER:
                property_lines.append(next_line)
                next_line = input_f.readline()
        content_lines = input_f.readlines()

    # Load the properties as an object
    property_dict = yaml.safe_load("".join(property_lines)) if property_lines else {}

    # Ensure datetimes are loaded as such
    if (modification_date := property_dict.get("modifié")) and isinstance(modification_date, str):
        property_dict["modifié"] = datetime.strptime(property_dict["modifié"], DT_FORMAT)

    return {"properties": property_dict, "content": content_lines}


# Retrieve all notes in the source directory
source_note_paths = glob.glob(os.path.join(SOURCE_DIRECTORY, "*.md"))

recent_notes = [
    parse_note(path) for path in source_note_paths if datetime.fromtimestamp(os.path.getmtime(path)) > REF_DATE
]


# Accross all notes, retrieve the list of uniques branches, knowing each note can have multiple branches
all_branches = {branch for note in recent_notes for branch in note["properties"].get("branches")}

recent_notes_by_branch = {}

for branch in all_branches:
    recent_notes_by_branch[branch] = [note for note in recent_notes if branch in note["properties"].get("branches")]

print({branch: len(notes) for branch, notes in recent_notes_by_branch.items()})

print(recent_notes_by_branch)
