from rdflib import Graph

class GraphRepo:

    def __init__(self, graph: Graph):
        self.graph = graph


    def output(self):
        print(self.graph.serialize(format="ttl"))
        pass

    def write(self, file):
        with open(file, 'w') as f:
            f.write(self.graph.serialize(format="ttl"))
