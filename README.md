## CLI Commands

```shell
poetry run go leaderboard --tournament USOpen2023

poetry run go cut-danger --tournament USOpen2023

poetry run go leaderboard-scrap --leaderboard-file gojos/majors/year_2023/us_open/leaderboard/round2.py --for-round 2

poetry run go plot --file _temp/totals.png --tournament USOpen2023 --accum-totals-plot --to-discord
poetry run go plot --file _temp/rank.png --tournament USOpen2023 --ranking-plot --to-discord 
```