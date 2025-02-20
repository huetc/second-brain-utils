import os
from datetime import datetime

import yaml

from second_brain_utils.dispatcher import dispatch_notes_by_branch, split_notes_by_branch
from second_brain_utils.parser import retrieve_source_notes

DT_FORMAT = "%Y-%m-%dT%H:%M:%S"


def main():
    with open(os.getenv("SECOND_BRAIN_UTILS_PARSER_CONF", "config/example.yaml")) as config_file:
        config = yaml.safe_load(config_file)

    source_directory = config["source_path"]
    ref_dt = datetime.strptime(config["ref_dt"], DT_FORMAT)
    target_dispatch_dir = config["dispatch_directory_path"]

    # Parse and retrieve all source notes
    recent_notes = retrieve_source_notes(source_directory=source_directory, ref_dt=ref_dt)

    # Split and dispatch the notes by directory depending on the branches they are associated to
    dispatch_notes_by_branch(
        notes_by_branch=split_notes_by_branch(recent_notes), target_dispatch_dir=target_dispatch_dir
    )


if __name__ == "__main__":
    main()
