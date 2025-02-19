import glob
import os
import os.path
from datetime import datetime
from pathlib import Path

import yaml

PROPERTY_SECTION_DELIMITER = "---\n"

DT_FORMAT = "%Y-%m-%dT%H:%M:%S"
ALTERNATE_DT_FORMAT = "%Y-%m-%d %H:%M"

with open(os.getenv("SECOND_BRAIN_UTILS_PARSER_CONF", "config/example.yaml")) as config_file:
    config = yaml.safe_load(config_file)

source_directory = config["source_path"]
ref_dt = datetime.strptime(config["ref_dt"], DT_FORMAT)
target_dispatch_dir = config["dispatch_directory_path"]


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
        try:
            property_dict["modifié"] = datetime.strptime(property_dict["modifié"], DT_FORMAT)
        except ValueError:
            property_dict["modifié"] = datetime.strptime(property_dict["modifié"], ALTERNATE_DT_FORMAT)

    return {"filename": os.path.basename(source_path), "properties": property_dict, "content": content_lines}


# Retrieve all notes in the source directory
source_note_paths = glob.glob(os.path.join(source_directory, "*.md"))

recent_notes = [
    parse_note(path) for path in source_note_paths if datetime.fromtimestamp(os.path.getmtime(path)) > ref_dt
]


# Accross all notes, retrieve the list of uniques branches, knowing each note can have multiple branches
all_branches = {branch for note in recent_notes for branch in note["properties"].get("branches")}

recent_notes_by_branch = {}

for branch in all_branches:
    recent_notes_by_branch[branch] = [note for note in recent_notes if branch in note["properties"].get("branches")]

# Create the target directory if it does not exist
Path(target_dispatch_dir).mkdir(parents=True, exist_ok=True)

# Dispatch and transfer the notes in the branch directories
for branch, notes in recent_notes_by_branch.items():
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
