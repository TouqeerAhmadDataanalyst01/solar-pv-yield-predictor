"""
Fetch solar irradiance + temperature data from NASA POWER API (free, no key needed).
Docs: https://power.larc.nasa.gov/docs/services/api/

Usage:
    python fetch_nasa_power.py --lat 29.4 --lon 71.68 --start 20230101 --end 20231231 --out ../data/bahawalpur_2023.csv
"""

import argparse
import requests
import pandas as pd


def fetch_power_data(lat: float, lon: float, start: str, end: str) -> pd.DataFrame:
    """
    Fetch daily GHI, temperature, and wind speed from NASA POWER.
    Parameters:
        lat, lon: coordinates
        start, end: dates as YYYYMMDD strings
    Returns:
        DataFrame indexed by date
    """
    url = "https://power.larc.nasa.gov/api/temporal/daily/point"
    params = {
        "parameters": "ALLSKY_SFC_SW_DWN,T2M,WS10M",  # irradiance, temp at 2m, wind at 10m
        "community": "RE",
        "longitude": lon,
        "latitude": lat,
        "start": start,
        "end": end,
        "format": "JSON",
    }

    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    props = data["properties"]["parameter"]
    df = pd.DataFrame({
        "ghi_kwh_m2_day": props["ALLSKY_SFC_SW_DWN"],
        "temp_c": props["T2M"],
        "wind_ms": props["WS10M"],
    })
    df.index = pd.to_datetime(df.index, format="%Y%m%d")
    df.index.name = "date"
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch NASA POWER solar/weather data")
    parser.add_argument("--lat", type=float, required=True, help="Latitude")
    parser.add_argument("--lon", type=float, required=True, help="Longitude")
    parser.add_argument("--start", type=str, required=True, help="Start date YYYYMMDD")
    parser.add_argument("--end", type=str, required=True, help="End date YYYYMMDD")
    parser.add_argument("--out", type=str, required=True, help="Output CSV path")
    args = parser.parse_args()

    df = fetch_power_data(args.lat, args.lon, args.start, args.end)
    df.to_csv(args.out)
    print(f"Saved {len(df)} rows to {args.out}")
    print(df.head())
