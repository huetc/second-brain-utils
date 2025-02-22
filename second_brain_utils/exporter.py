import os.path
import re
from pathlib import Path

import yaml

from second_brain_utils.obsidian_constants import PROPERTY_SECTION_DELIMITER

TMP_LINE_DELIMITER = "<DELIMITER>"


def export_notes(
    notes: list, target_dir: str, render_md_links: bool = False, pop_properties: list[str] | None = None
) -> None:
    # Create the target directory if not existing
    Path(os.path.join(target_dir)).mkdir(parents=True, exist_ok=True)

    if render_md_links:
        # Prepare a pattern to transform all references to notes as Markdown links
        # Example: "[[my-other-note]]" shall be exported as "[my-other-note](my-other-note)"
        note_ref_pattern = r"\[\[([^\]]+)\]\]"
        replace_pattern = r"[\1](\1)"
    # Dump all notes
    for note in notes:
        with open(os.path.join(target_dir, note["filename"]), mode="w") as note_file:
            # Dumping the properties first, correctly delimited
            note_file.write(PROPERTY_SECTION_DELIMITER)
            # Optionally removing some properties for the export
            export_properties = (
                {prop: value for prop, value in note["properties"].items() if prop not in pop_properties}
                if pop_properties
                else note["properties"]
            )
            yaml.dump(data=export_properties, stream=note_file, sort_keys=False, indent=2, allow_unicode=True)
            note_file.write(PROPERTY_SECTION_DELIMITER)
            if render_md_links:
                joined_content_lines = TMP_LINE_DELIMITER.join(note["content"])
                content_with_links = re.sub(pattern=note_ref_pattern, repl=replace_pattern, string=joined_content_lines)
                note_file.writelines(content_with_links.split(TMP_LINE_DELIMITER))
            else:
                note_file.writelines(note["content"])


def export_unique_tags(
    notes: list,
    target_path: str,
) -> None:
    all_tags = []

    for note in notes:
        all_tags.extend(note["properties"].get("tags") or [])

    with open(target_path, mode="w") as out_f:
        out_f.writelines("\n".join(sorted(set(all_tags))))
