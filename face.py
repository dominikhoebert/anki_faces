from dataclasses import dataclass


@dataclass
class Face:
    firstname: str
    lastname: str
    group: str
    filename: str

    @staticmethod
    def read_in(filename: str):
        parts = filename.split('_')
        group = parts[2].split('.')[0]
        return Face(parts[1], parts[0], group, filename)

    def __str__(self):
        return f'{self.firstname} {self.lastname} ({self.group})'

    def __repr__(self):
        return self.__str__()
