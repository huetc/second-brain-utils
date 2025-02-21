import sys

from second_brain_utils.config import JobConfig
from second_brain_utils.dispatcher import dispatch_notes_by_branch, split_notes_by_branch
from second_brain_utils.parser import retrieve_source_notes


def main():
    config = JobConfig()
    print(config)

    source_directory = config.source_directory
    if not config.ref_dt:
        sys.exit("ref_dt setting was not found but is required for the dispatch command.")
    ref_dt = config.ref_dt
    target_dispatch_dir = config.target_directory

    # Parse and retrieve all source notes
    recent_notes = retrieve_source_notes(source_directory=source_directory, ref_dt=ref_dt)

    # Split and dispatch the notes by directory depending on the branches they are associated to
    dispatch_notes_by_branch(
        notes_by_branch=split_notes_by_branch(recent_notes), target_dispatch_dir=target_dispatch_dir
    )


if __name__ == "__main__":
    main()
