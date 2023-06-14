class Tournament:
    def __init__(self, name, subject_name: str, perma_id: str):
        self.name = name
        self.perma_id = perma_id
        self.subject_name = subject_name


class GrandSlam(Tournament):
    pass
