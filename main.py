import genanki
import os
from face import Face
from random import sample, randrange

from model import my_model
from PIL import Image, ImageOps
import shutil

TARGET_HEIGHT = 400  # desired max height in pixels


def ensure_resized(src_path: str, dest_path: str, target_height: int = TARGET_HEIGHT):
    """Create a resized copy of image with given max height while preserving aspect ratio.
    Only downsizes images taller than target_height. If already <= target_height, it just copies.
    Returns destination path.
    """
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    if os.path.exists(dest_path):
        return dest_path  # already processed
    try:
        with Image.open(src_path) as im:
            im = ImageOps.exif_transpose(im)
            width, height = im.size
            if height > target_height and height > 0:
                new_width = int(width * target_height / height)
                im = im.resize((new_width, target_height), Image.LANCZOS)
                save_kwargs = {}
                ext = os.path.splitext(dest_path)[1].lower()
                if ext in {'.jpg', '.jpeg'}:
                    save_kwargs = {"quality": 85, "optimize": True}
                elif ext == '.png':
                    save_kwargs = {"optimize": True}
                im.save(dest_path, **save_kwargs)
            else:
                # Height already small enough – copy original
                shutil.copy2(src_path, dest_path)
    except Exception as e:
        # Fallback: copy original if Pillow fails
        try:
            shutil.copy2(src_path, dest_path)
        except Exception:
            print(f"⚠️ Failed to process image {src_path}: {e}")
    return dest_path

# Root folder containing all group subdirectories
folder = 'Klassenfotos_cropped'


def build_decks(root_folder: str):
    os.makedirs('decks', exist_ok=True)
    os.makedirs('resized_media', exist_ok=True)

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
        resized_media_files = []
        processed = set()
        resized_group_dir = os.path.join('resized_media', group)

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

            # Ensure resized image exists for this face
            if face.filename and face.filename not in processed:
                original_path = os.path.join(group_path, face.filename)
                dest_path = os.path.join(resized_group_dir, face.filename)
                resized_path = ensure_resized(original_path, dest_path)
                resized_media_files.append(resized_path)
                processed.add(face.filename)

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
        package.media_files = resized_media_files

        out_file = f'decks/{group}.apkg'
        package.write_to_file(out_file)
        print(f'🎉 Created deck: {out_file} ({len(faces)} faces)')


def main():
    build_decks(folder)


if __name__ == '__main__':
    main()
