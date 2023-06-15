## CLI Commands

```shell
poetry run go leaderboard --tournament USOpen2023

poetry run go leaderboard-scrap --leaderboard-file _temp/results.py

poetry run go plot --file _temp/totals.png --tournament USOpen2023 --accum-totals-plot --to-discord
poetry run go plot --file _temp/rank.png --tournament USOpen2023 --ranking-plot --to-discord 
```