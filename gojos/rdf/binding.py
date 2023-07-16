from . import rdf_prefix


def bind(g):
    [add_binding(g, ns) for ns in ontology_namespaces()]
    return g

def add_binding(g, ns):
    g.bind(ns.replace('_', '-'), getattr(rdf_prefix, ns))

def ontology_namespaces():
    return list(filter(lambda attrs: ('__' not in attrs) and ("Namespace" not in attrs), dir(rdf_prefix)))
