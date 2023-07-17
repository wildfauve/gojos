from .rdf_prefix import *

name = foaf.name
notation = skos.notation


# Players
hasAlternateName = clo_go_plr.hasAltName
hasKlassName = clo_go_plr.hasKlassName

# Fantasy
hasTeamMembers = clo_fan.hasTeamMembers
hasFeature = clo_fan.hasFeature
isSelectionForTeam = clo_fan.isSelectionForTeam
isForTeam = clo_fan.isForTeam
isFantasyForEvent = clo_fan.isFantasyForEvent


# Tournaments
isInYear = clo_go.isInYear
hasSubjectName = clo_go.hasSubjectName
hasPermId = clo_go.hasPermId
isEventOf = clo_go.isEventOf
isEntryForPlayer = clo_go.isEntryForPlayer
hasFantasyPointsStrategy = clo_go.hasFantasyPointsStrategy
hasCutStrategy = clo_go.hasCutStrategy
