import re

from second_brain_utils.obsidian_constants import NOTE_REFERENCE_MARKER

# Used only for easier work on the text
TMP_LINE_DELIMITER = "<DELIMITER>"


def get_obfuscated_notes(
    notes: list,
    private_ref_filler: str,
    private_section_start: str,
    private_section_end: str,
    private_section_filler: str,
) -> list:
    # In case of poor performances, check here first as multiple passes are performed on the same files and lines within files
    notes_by_privacy = {"private": [], "public": []}
    for note in notes:
        if (note.get("properties") or {}).get("privé", True):
            notes_by_privacy["private"].append(note)
        else:
            notes_by_privacy["public"].append(note)

    # Retrieve the names of the private notes
    # Notes are private by default
    private_note_patterns = map(
        re.escape, [f"[[{note["filename"].split(".md")[0]}]]" for note in notes_by_privacy["private"]]
    )

    obfuscated_notes = []
    private_pattern = re.compile("|".join(private_note_patterns))
    # Loop over all public notes to obfuscate anything private
    for note in notes_by_privacy["public"]:
        content_lines = note.get("content") or []
        # If note has no content, adding it as is
        if not content_lines:
            obfuscated_notes.append(note)
            continue

        # Processing the whole content as a single string for easier multi-line pattern matching
        joined_lines = TMP_LINE_DELIMITER.join(content_lines)

        # Checking if at least one of the "Privacy Markers" is in the notes:
        # - reference to a private note
        # - sections noted as private
        if NOTE_REFERENCE_MARKER in joined_lines or private_section_start in joined_lines:
            # Processing references to private notes
            censored_ref_lines = private_pattern.sub(private_ref_filler, joined_lines)
            # Processing private sections
            censored_section_lines = re.sub(
                f"{re.escape(private_section_start)}.*?{re.escape(private_section_end)}",
                private_section_filler,
                censored_ref_lines,
                flags=re.DOTALL,  # required to handle multiline sections
            )

            # Replacing the original content with the censored version, as a list of lines
            note["content"] = censored_section_lines.split(sep=TMP_LINE_DELIMITER)

        obfuscated_notes.append(note)
    return obfuscated_notes
