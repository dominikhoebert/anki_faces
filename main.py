import genanki
import os
from face import Face
from random import sample, randrange

from model import my_model

folder = 'klassenfotos_cropped'
group = '3CHIT'

files = os.listdir(folder + "/" + group)
faces = [Face.read_in(file) for file in files]


def get_random_faces(faces: list, n: int):
    selection = sample(faces, n)
    return selection

deck = genanki.Deck(randrange(1 << 30, 1 << 31), group)

for face in faces:
    while True:
        false_selection = get_random_faces(faces, 3)
        if face not in false_selection:
            break

    deck.add_note(genanki.Note(
        model=my_model,
        fields=[f'<img src="{face.filename}">', f'{group}', '2',
                f'{face.firstname} {face.lastname}', f'{false_selection[0].firstname} {false_selection[0].lastname}',
                f'{false_selection[1].firstname} {false_selection[1].lastname}',
                f'{false_selection[2].firstname} {false_selection[2].lastname}', '', '1 0 0 0', '', '']))

package = genanki.Package(deck)
package.media_files = [folder + "/" + group + "/" + face.filename for face in faces]

package.write_to_file(f'decks/{group}.apkg')

