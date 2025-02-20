import glob
import os
import os.path
from datetime import datetime

import yaml

PROPERTY_SECTION_DELIMITER = "---\n"

DT_FORMAT = "%Y-%m-%dT%H:%M:%S"
ALTERNATE_DT_FORMAT = "%Y-%m-%d %H:%M"


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


def retrieve_source_notes(source_directory: str, ref_dt: datetime) -> list:
    # Retrieve all notes in the source directory
    source_note_paths = glob.glob(os.path.join(source_directory, "*.md"))

    return [parse_note(path) for path in source_note_paths if datetime.fromtimestamp(os.path.getmtime(path)) > ref_dt]
