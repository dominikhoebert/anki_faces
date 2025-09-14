from dataclasses import dataclass


@dataclass
class Face:
    firstname: str
    lastname: str
    group: str
    filename: str

    @staticmethod
    def read_in(filename: str):
        #remove file extension
        croped = filename.split('.')[0]
        parts = croped.split('_')
        group = None
        firstname = " ".join(parts[2:])
        return Face(firstname, parts[1], group, filename)

    def __str__(self):
        return f'{self.firstname} {self.lastname} ({self.group})'

    def __repr__(self):
        return self.__str__()
