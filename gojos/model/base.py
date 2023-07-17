from gojos import repo


class GraphModel:

    @classmethod
    def fantasy_graph(cls):
        return repo.fantasy_graph()

    @classmethod
    def player_graph(cls):
        return repo.players_graph()

    @classmethod
    def tournament_graph(cls):
        return repo.tournament_graph()

    def __init__(self, repository, graph_fn):
        self.repository = repository
        self.graph_fn = graph_fn
        self.repo_instance = None

    def gr(self):
        print(list(self.graph_fn().subjects()))
        if self.repo_instance:
            print(list(self.repo_instance.graph.subjects()))

    def __call__(self):
        if self.repo_instance:
            return self.repo_instance
        self.repo_instance = self.repository(self.graph_fn())
        return self.repo_instance
