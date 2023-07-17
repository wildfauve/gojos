from gojos import model, adapter

def tournament_leaderboard(event: model.TournamentEvent, for_round: int):
    return _add_results(adapter.build_leaderboard(event, for_round)),


def _add_results(draws):
    results = [_round_result(draw, match_blocks) for draw, match_blocks in draws.items()]
    return results

def _round_result(entries, leaderboard_file, for_round):
    if not leaderboard_file:
        return entries
    py = _results_function()
    for rd, entries in reduce(partial(_leaderboard_def, for_round), entries, {1: [], 2: [], 3: [], 4: []}).items():
        if entries:
            py = py + f"\n\ndef scores(tournie):\n"
            for entry in entries:
                py = py + f"{'':>4}{entry}\n"
            py = py + f"{'':>4}tournie.leaderboard.for_round({rd}).done()\n"

    _write_file(leaderboard_file, py)
    return entries


