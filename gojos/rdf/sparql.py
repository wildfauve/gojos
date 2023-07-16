from typing import Callable
from textwrap import dedent
from rdflib import Literal
from rdflib.plugins.sparql.processor import SPARQLResult

from gojos.util import logger



def sparql_prefixes():
    return dedent("""prefix clo-go: <https://clojos.io/ontology/FantasyGolf/>
    prefix clo-go-plr: <https://clojos.io/ontology/FantasyGolf/Player/>
    prefix clo-go-ind_plr: <https://clojos.io/ontology/FantasyGolf/Ind/Player/>
    prefix clo-go-tou: <https://clojos.io/ontology/FantasyTennis/Tournament/>
    prefix clo-fan: <https://clojos.io/ontology/Fantasy/>
    prefix clo-fan-ind: <https://clojos.io/ontology/Fantasy/Ind/>
    prefix foaf: <http://xmlns.com/foaf/0.1/>
    prefix skos: <http://www.w3.org/2004/02/skos/core#>
    prefix foaf: <http://xmlns.com/foaf/0.1/>
    """)

def query(g, query_exp: str, prefixes_fn: Callable = sparql_prefixes) -> SPARQLResult:
    logger.info(f"{prefixes_fn()}\n{query_exp}")
    return g.query(f"{prefixes_fn()}\n{query_exp}")


