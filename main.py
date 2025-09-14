import genanki
import os
from face import Face
from random import sample, randrange

from model import my_model

# Root folder containing all group subdirectories
folder = 'Klassenfotos_cropped'


def build_decks(root_folder: str):
    os.makedirs('decks', exist_ok=True)

    # Iterate over every subdirectory (group) inside the root folder
    for group in sorted(os.listdir(root_folder)):
        group_path = os.path.join(root_folder, group)
        if not os.path.isdir(group_path):
            continue  # skip non-directories

        # Collect image files (basic extensions)
        image_files = [f for f in os.listdir(group_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        if not image_files:
            continue  # nothing to do for empty group folders

        # Read in faces for this group
        faces = []
        for filename in image_files:
            face = Face.read_in(filename)
            # store group info (Face.read_in currently sets group=None)
            face.group = group
            faces.append(face)

        # Create a deck for this group
        deck = genanki.Deck(randrange(1 << 30, 1 << 31), group)

        for face in faces:
            others = [f for f in faces if f is not face]
            # Select up to 3 false options (ensure they don't include the correct face)
            if len(others) >= 3:
                false_selection = sample(others, 3)
            else:
                false_selection = others[:]

            # Pad with placeholder empty names if fewer than 3 distractors are available
            while len(false_selection) < 3:
                false_selection.append(Face('', '', group, ''))

            wrong_names = [f'{f.firstname} {f.lastname}'.strip() for f in false_selection]

            # Answers field currently hard-coded as in original script
            deck.add_note(genanki.Note(
                model=my_model,
                fields=[
                    f'<img src="{face.filename}">',  # Question (image)
                    f'{group}',  # Title
                    '2',  # QType (keep original value)
                    f'{face.firstname} {face.lastname}',  # Correct answer shown among options
                    wrong_names[0],
                    wrong_names[1],
                    wrong_names[2],
                    '',  # Q_5 (unused)
                    '1 0 0 0',  # Answers pattern (original)
                    '',  # Sources
                    ''  # Extra 1
                ]
            ))

        # Package with media files
        package = genanki.Package(deck)
        package.media_files = [os.path.join(group_path, face.filename) for face in faces if face.filename]

        out_file = f'decks/{group}.apkg'
        package.write_to_file(out_file)
        print(f'🎉 Created deck: {out_file} ({len(faces)} faces)')


def main():
    build_decks(folder)


if __name__ == '__main__':
    main()
