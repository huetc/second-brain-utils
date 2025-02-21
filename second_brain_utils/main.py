import sys

from second_brain_utils.config import JobConfig
from second_brain_utils.dispatcher import dispatch_notes_by_branch, split_notes_by_branch
from second_brain_utils.exporter import export_notes
from second_brain_utils.parser import retrieve_source_notes
from second_brain_utils.privacy_checker import get_obfuscated_notes


def main():
    print("""
        This project contains tools to dispatch, export and mask the notes from the second brain.

        Available commands are:
          - dispatch-notes
          - export-notes
    """)


def run_dispatch_notes():
    config = JobConfig()

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


def run_export_notes():
    config = JobConfig()

    source_directory = config.source_directory
    target_dump_dir = config.target_directory

    # Parse and retrieve all source notes
    all_notes = retrieve_source_notes(source_directory=source_directory)

    # Filter the private notes and mask the private sections in the public ones
    public_notes_with_mask = get_obfuscated_notes(
        notes=all_notes,
        private_ref_filler=config.private_ref_filler,
        private_section_start=config.private_section_start,
        private_section_end=config.private_section_end,
        private_section_filler=config.private_ref_filler,
    )

    # Export the notes
    export_notes(
        notes=public_notes_with_mask,
        target_dir=target_dump_dir,
        render_md_links=config.export_render_md_links,
        pop_properties=config.export_pop_properties,
    )


if __name__ == "__main__":
    main()
