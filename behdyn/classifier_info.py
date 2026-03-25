
class ClassifierInfo:
    def __init__(self, species:str, epoch:float):
        self.species = species
        self.epoch = epoch

classifiers_info = {
    "baboon": ClassifierInfo("baboon", 60.0),
}
