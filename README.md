# anki_faces

Generate per-class Anki decks for learning student names from face photos.

## What it does
For every subfolder inside `Klassenfotos_cropped/` (e.g. `1AHIT`, `2AHIT`, ...), the script:
1. Parses each image filename to extract last & first name(s).
2. Resizes images to a max height of 400px (keeps aspect ratio) into `resized_media/<GROUP>/` (only if not already processed).
3. Builds a single‑choice (SC) multiple choice note for each face with 1 correct + up to 3 distractor names from the same group.
4. Exports an Anki package `<GROUP>.apkg` into the `decks/` folder including the resized images as media.
5. Anki Addon 1566095810 needed.

## Quick start
```bash
# (Optional) create & activate a virtual environment
python -m venv .venv
# Windows PowerShell
. .venv/Scripts/Activate.ps1

pip install -r requirements.txt
python main.py
```
Result: one `.apkg` per class under `decks/`.

## Input folder structure
```
Klassenfotos_cropped/
  1AHIT/
    01_Surname_Firstname.jpg
    02_Surname_Firstname-PartTwo.jpg
  2AHIT/
    ...
```
Each **subdirectory name = class/group name**. Only image files ending in `.jpg`, `.jpeg`, `.png` are processed.

## Filename convention
Pattern: `NN_Lastname_Firstname[ _MoreParts].ext`
- `NN` (numeric prefix) is ignored except for ordering.
- Parts are split on `_`.
- `parts[1]` = last name.
- `parts[2:]` joined with space = first name (supports hyphens & multi-part first names).
- Group is not encoded in the filename; it's taken from the containing folder name.

Examples:
- `14_Gül_Gökalp_Kaan.jpg` → Last name: `Gül`, First name: `Gökalp Kaan`.
- `18_Kayali-Leopold_Laurenz.jpg` → Last name: `Kayali-Leopold`, First name: `Laurenz`.

## Generated note fields (model: AllInOne (kprim, mc, sc))
The script always sets `QType` = `2` (single choice). Fields used:
1. Question: `<img src="<filename>">`
2. Title: group (e.g. `1AHIT`)
3. QType: `2`
4. Q_1: Correct full name ("Firstname Lastname")
5. Q_2..Q_4: Distractor names (may be empty if not enough classmates)
6. Q_5: (unused)
7. Answers: hard-coded string `1 0 0 0` (marks first option as correct for sc)

If a class has fewer than 4 students, empty placeholder names are added so the template still renders four rows.

## Image resizing
`ensure_resized()` downsizes only if height > 400px; otherwise it copies the original. JPEGs saved with quality 85 & optimize, PNGs with optimize. Already processed images are skipped on re-runs (idempotent).

## Output
```
decks/
  1AHIT.apkg
  2AHIT.apkg
resized_media/
  1AHIT/<images>
  2AHIT/<images>
```
Each deck gets a randomly generated numeric ID (via `randrange`). Re-running will create *new* decks (Anki treats them as different note types/decks) — if you want stable imports, replace the random with a fixed integer per group & a fixed model ID.

## Customization ideas
- Change `TARGET_HEIGHT` in `main.py`.
- Adjust the number of distractors (currently fixed at 3) and update the `Answers` pattern accordingly.
- Provide different `QType` values (0 = kprim, 1 = multi-select, 2 = single-choice) and adapt field population.
- Add deterministic deck/model IDs to enable deck updates instead of duplicates.
- Include reverse cards (show name → pick photo) by adding another note model or template.

## Potential improvements (future work)
- Validate filenames & warn on malformed patterns.
- CLI arguments (root folder, target height, number of distractors, output path).
- Logging with verbosity levels instead of plain prints.
- Hash-based cache to avoid re-resizing if original changes.
- Unit tests for `Face.read_in` and image resizing.

## Troubleshooting
- Missing `.apkg`: ensure the group folder contains at least one supported image file.
- Garbled names: verify underscores & ordering in filenames.
- Duplicate cards after re-import: switch to stable IDs.

## License
Add a license file (e.g. MIT) to clarify usage/distribution rights.

## Disclaimer
The embedded card template JavaScript (in `model.py`) derives from third-party code segments (notably "anki-persistence" & Cloze Overlapper-inspired blocks). Ensure compliance with their respective licenses if distributing.

---
Happy studying! Generate, import into Anki, and start memorizing faces fast.

