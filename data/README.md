# data/ – three small reference files

Static files the notebooks read. No flight data – that you collect yourself. These files are third-party data and
are **not** covered by the MIT licence of the code; their sources and terms are listed here.

| File | Used in | Source | Terms |
|---|---|---|---|
| `mobitool_factors.csv` | 11 Plane or train | mobitool factors v3.1 (2025-04-08), EnergieSchweiz / PSI – file `mobitool-Faktoren-v3.1-20250408.xlsx`, linked as data basis on <https://www.energieschweiz.ch/programme/umweltrechner-verkehr/>. Extracted 2026-10-20; the comment lines at the top of the file name the sheet and columns. | No licence stated in the source file. Cite as "mobitool v3.1, EnergieSchweiz/PSI". |
| `rail_times_zurich.csv` | 11 Plane or train | Fastest rail connection Zürich HB → city, queried **once** on 2026-10-20 (departures from 07:00 on Thu 2026-10-22) from the ÖBB timetable (HAFAS endpoint behind fahrplan.oebb.at – unofficial, not a documented public API). Only the derived travel times and number of changes are stored. | Timetable data of the railways, no licence stated. No code in this project calls the endpoint – please do not automate queries against it. |
| `statpop_2025_municipalities.csv` | 12 Who is overflown | Swiss Federal Statistical Office (BFS), STATPOP: permanent resident population per municipality on 31.12.2025, PXWeb table `px-x-0102010000_101` (municipalities as of 6.4.2025), fetched 2026-10-20. | BFS open data: free use, the source must be given (BFS, STATPOP). |

The other data the notebooks use is downloaded at run time into `cache/` (not part of the repository) – see the
section "Data sources and their terms" in the main [README](../README.md).
