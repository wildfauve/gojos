from rdflib import Namespace

__clo_fan_ns = "https://clojos.io/ontology/Fantasy/"
__clo_fan_ind_ns = "https://clojos.io/ontology/Fantasy/Ind/"
__clo_go_ns = "https://clojos.io/ontology/FantasyGolf/"
__clo_ind_ns = "https://clojos.io/ontology/FantasyGolf/Ind/"

owl = Namespace("http://www.w3.org/2002/07/owl#")
skos = Namespace('http://www.w3.org/2004/02/skos/core#')

clo_fan = Namespace(__clo_fan_ns)
clo_fan_ind = Namespace(__clo_fan_ind_ns)

clo_go = Namespace(__clo_go_ns)

clo_go_ind = Namespace(__clo_ind_ns)

clo_go_plr = Namespace(f"{__clo_go_ns}Player/")

clo_go_fan = Namespace(f"{__clo_go_ns}Fantasy/")

clo_go_ind_plr = Namespace(f"{__clo_ind_ns}Player/")

clo_go_ind_tou = Namespace(f"{__clo_ind_ns}Tournament/")

clo_go_ind_fan = Namespace(f"{__clo_ind_ns}Fantasy/")

foaf = Namespace("http://xmlns.com/foaf/0.1/")

dcterms = Namespace("http://purl.org/dc/terms/")
