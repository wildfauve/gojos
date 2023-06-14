from typing import Dict
import csv

from gojos.util import echo

sp = f"{'':>4}"


def fantasy_score_template(result_fn_calls: Dict):
    for fn_draw_symbol, fn_calls_for_draw in result_fn_calls.items():
        for result in fn_calls_for_draw:
            echo.echo(result)


def format_as_csv(draw_name, round_number, results):
    with open(f"{draw_name}-{round_number}.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['draw', 'match', 'winner', 'sets', 'match up'])
        for row in results:
            writer.writerow(row)
