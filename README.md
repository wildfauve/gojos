## CLI Commands

```shell
poetry run go plot --file _temp/totals.png --tournament USOpen2023 --accum-totals-plot --to-discord
poetry run go plot --file _temp/rank.png --tournament USOpen2023 --ranking-plot --to-discord 
```

## Creating a new Tournament

```shell
poetry run to new-tournament -t themasters -p mas -s TheMasters

poetry run to new-event -t TheMasters -y 2024

poetry run to add-entries -t TheMasters -y 2024
```

## Running the Tournament

```shell
poetry run to add-round-results -t TheMasters -y 2024 -r 1

poetry run to tournament-leaderboard -t TheMasters -y 2024 -r 1

poetry run fan leaderboard --tournament TheMasters -y 2024

poetry run fan cut-danger --tournament TheMasters -y 2024

```
