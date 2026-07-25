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

```
/data        sample inputs + generated outputs
/notebooks   exploration notebook (optional, for analysis narrative)
/src         fetch_nasa_power.py, pv_yield_model.py
/powerbi     .pbix dashboard (build after generating CSVs)
```

## Quickstart

```bash
pip install -r requirements.txt

# 1. Fetch real data for your location (example: Bahawalpur, Pakistan)
python src/fetch_nasa_power.py --lat 29.4 --lon 71.68 \
    --start 20230101 --end 20231231 --out data/bahawalpur_2023.csv

# 2. Estimate yield for a 5kW system
python src/pv_yield_model.py --input data/bahawalpur_2023.csv \
    --capacity_kw 5 --tilt 25 --out data/monthly_yield.csv
```

Try other cities relevant to Gulf hiring by changing lat/lon:
- Dubai, UAE: 25.20, 55.27
- Riyadh, KSA: 24.71, 46.68
- Doha, Qatar: 25.29, 51.53

## Power BI Dashboard

Import `data/monthly_yield.csv` and `data/daily_yield.csv` into Power BI Desktop.
Suggested visuals:
- Line chart: monthly yield (kWh) across the year
- KPI card: total annual yield
- Scatter: temperature vs. yield (shows derating effect)
- Map: yield by location if comparing multiple cities

Export the finished dashboard as `powerbi/solar_pv_dashboard.pbix`.

## Data source

NASA POWER: https://power.larc.nasa.gov — free, no registration, no API key.

## Tooling note — this vs. industry-standard software

This project uses **pvlib-style open-source modeling** in Python. Real Solar
Analyst roles in the industry commonly use **PVsyst**, a commercial tool that
remains the standard for professional feasibility studies. This project
demonstrates the underlying physics and modeling logic transparently in code —
a strong complement to, not a replacement for, PVsyst experience. Familiarity
with both is the honest goal.

## Notes / honesty disclaimer

This uses a simplified irradiance-to-power model for a fast, defensible v1.
A production-grade version would use `pvlib.modelchain` with real panel and
inverter specs from the CEC/SAM database. That upgrade is a natural "v2" to
mention in interviews — it shows you know the difference between a quick
estimate and an engineering-grade simulation.

---
Contact: [LinkedIn] • Open to Remote / UAE / KSA
