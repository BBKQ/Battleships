class Ship:

    def __init__(self, name, size, owner):
        self.name = name
        self.size = size
        self.owner = owner
        self.initial_coordinates = []
        self.afloat_coordinates = []
        self.afloat = True