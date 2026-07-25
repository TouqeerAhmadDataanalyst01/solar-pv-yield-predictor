# Solar PV Yield Predictor — Pakistan / Gulf

BS Physics — Islamia University of Bahawalpur
Aspiring Energy Data Analyst | Python / SQL / Power BI

## What this does

Estimates monthly solar PV energy yield (kWh) for a given location using free
NASA POWER satellite irradiance and temperature data. Built to demonstrate the
exact skill Gulf solar operators (Masdar, ACWA Power, NEOM, Yellow Door Energy)
hire junior Energy Data Analysts for.

## How it works

1. **Fetch** — Pull daily solar irradiance (GHI) and temperature for any lat/lon
   from NASA's free POWER API (no API key required).
2. **Model** — Convert irradiance to estimated energy output, applying a
   temperature derating factor (panels lose efficiency above 25°C).
3. **Report** — Aggregate to monthly totals and visualize in Power BI.

## Folders
