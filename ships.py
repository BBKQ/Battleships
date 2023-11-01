class Ship:

    def __init__(self, name, size, owner):
        self.name = name
        self.size = size
        self.owner = owner
        self.coordinates = []
        self.afloat = True