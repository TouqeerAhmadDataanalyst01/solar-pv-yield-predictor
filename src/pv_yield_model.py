"""
Estimate monthly solar PV yield (kWh) from NASA POWER daily data using a
simplified pvlib-style model.

Usage:
    python pv_yield_model.py --input ../data/bahawalpur_2023.csv --capacity_kw 5 --tilt 25 --out ../data/monthly_yield.csv
"""

import argparse
import pandas as pd


def estimate_daily_yield(df: pd.DataFrame, capacity_kw: float, tilt: float,
                          system_efficiency: float = 0.80,
                          temp_coeff: float = -0.004) -> pd.DataFrame:
    """
    Simple PV yield estimate.
    kWh_day = GHI (kWh/m2/day) * capacity_kw * system_efficiency * temp_derate
    """
    df = df.copy()
    tilt_factor = 1.0 + (tilt / 90) * 0.05

    df["temp_derate"] = 1 + temp_coeff * (df["temp_c"] - 25)
    df["temp_derate"] = df["temp_derate"].clip(upper=1.0)

    df["yield_kwh"] = (
        df["ghi_kwh_m2_day"]
        * capacity_kw
        * system_efficiency
        * tilt_factor
        * df["temp_derate"]
    )
    return df


def monthly_summary(df: pd.DataFrame) -> pd.DataFrame:
    monthly = df.resample("MS")["yield_kwh"].sum().to_frame()
    monthly["avg_daily_ghi"] = df.resample("MS")["ghi_kwh_m2_day"].mean()
    monthly["avg_temp_c"] = df.resample("MS")["temp_c"].mean()
    monthly.index.name = "month"
    return monthly


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Estimate PV yield from NASA POWER data")
    parser.add_argument("--input", type=str, required=True)
    parser.add_argument("--capacity_kw", type=float, required=True)
    parser.add_argument("--tilt", type=float, default=25)
    parser.add_argument("--out", type=str, required=True)
    args = parser.parse_args()

    raw = pd.read_csv(args.input, index_col="date", parse_dates=True)
    daily = estimate_daily_yield(raw, args.capacity_kw, args.tilt)
    monthly = monthly_summary(daily)

    daily.to_csv(args.out.replace("monthly", "daily"))
    monthly.to_csv(args.out)

    print(monthly)
    print(f"\nTotal annual estimated yield: {daily['yield_kwh'].sum():.0f} kWh")
