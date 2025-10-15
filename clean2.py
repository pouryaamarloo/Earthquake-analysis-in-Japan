
import os
import argparse
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def parse_args():
    p = argparse.ArgumentParser(description="Visualize earthquake CSV (Japan Geofon) — creates 4 plots.")
    p.add_argument(
        "--csv", "-c",
        default="/mnt/data/JAPAN_GEOFON_cleaned.csv",
        help="Path to CSV file (default: /mnt/data/JAPAN_GEOFON_cleaned.csv)"
    )
    p.add_argument(
        "--outdir", "-o",
        default="plots",
        help="Output folder for saved figures (default: plots/)"
    )
    p.add_argument(
        "--show", action="store_true",
        help="If set, display the figures interactively in addition to saving them."
    )
    return p.parse_args()

def load_and_prepare(csv_path):
    df = pd.read_csv(csv_path)
    # ترکیب date و time در صورت وجود و ساخت ستون datetime
    if "time" in df.columns and "date" in df.columns:
        # بعضی فایل‌ها time شامل میلی‌ثانیه با نقطه است؛ concat و parse
        combined = df["date"].astype(str).str.strip() + " " + df["time"].astype(str).str.strip()
        df["datetime"] = pd.to_datetime(combined, errors="coerce")
    else:
        # اگر فقط date موجود است
        if "date" in df.columns:
            df["datetime"] = pd.to_datetime(df["date"], errors="coerce")
        else:
            df["datetime"] = pd.NaT

    # تبدیل تایپ‌ها و حذف ردیف‌هایی که مقادیر مورد نیاز را ندارند
    numeric_cols = ["mag", "longitude", "latitude", "depth"]
    for c in numeric_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    df = df.dropna(subset=["mag", "longitude", "latitude"])  # ردیف‌های بدون مختصات یا بزرگی را کنار می‌گذاریم
    return df


# نمودارها
def plot_scatter_map(df, outpath, show=False):
    """نقشه پراکندگی: longitude vs latitude، اندازه بر اساس mag."""
    plt.figure(figsize=(9,7))
    # اندازه نقاط: تابعی از بزرگی (اسکیل را قابل‌فهم انتخاب کردم)
    sizes = (df["mag"] ** 3) * 8  # توان 3 برای تمایز بهتر، سپس مقیاس‌دهی
    sc = plt.scatter(df["longitude"], df["latitude"],
                     s=sizes,
                     alpha=0.6,
                     edgecolor="black",
                     linewidth=0.4)
    plt.title("Earthquake Locations in Japan (marker size ~ magnitude)")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True, linestyle=":", alpha=0.5)
    plt.tight_layout()
    plt.savefig(outpath, dpi=300)
    if show:
        plt.show()
    plt.close()

def plot_magnitude_time(df, outpath, show=False):
    """نمودار زمانی بزرگی‌ها (datetime vs mag)."""
    plt.figure(figsize=(10,4.5))
    # اگر datetime موجود نباشد، از index یا date استفاده می‌کنیم
    x = df["datetime"] if "datetime" in df.columns and not df["datetime"].isna().all() else pd.to_datetime(df["date"], errors="coerce")
    plt.plot(x, df["mag"], marker='o', linestyle='-', linewidth=1)
    plt.title("Earthquake Magnitudes Over Time")
    plt.xlabel("Date")
    plt.ylabel("Magnitude")
    plt.grid(True, linestyle=":", alpha=0.5)
    # فرمت تاریخ برای خوانایی بهتر
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.gca().xaxis.set_major_formatter(mdates.ConciseDateFormatter(mdates.AutoDateLocator()))
    plt.tight_layout()
    plt.savefig(outpath, dpi=300)
    if show:
        plt.show()
    plt.close()

def plot_hist_magnitude(df, outpath, show=False):
    """هیستوگرام توزیع بزرگی‌ها."""
    plt.figure(figsize=(7,5))

bins = max(6, int((df["mag"].max() - df["mag"].min()) / 0.2))  # تعیین خودکار تعداد بین‌ها
    plt.hist(df["mag"], bins=bins, edgecolor='black', alpha=0.8)
    plt.title("Distribution of Earthquake Magnitudes")
    plt.xlabel("Magnitude")
    plt.ylabel("Frequency")
    plt.grid(axis='y', linestyle=":", alpha=0.5)
    plt.tight_layout()
    plt.savefig(outpath, dpi=300)
    if show:
        plt.show()
    plt.close()

def plot_depth_vs_magnitude(df, outpath, show=False):
    """نمودار عمق در برابر بزرگی."""
    plt.figure(figsize=(7,5))
    plt.scatter(df["mag"], df["depth"], alpha=0.75, edgecolor="black", linewidth=0.4)
    plt.gca().invert_yaxis()  # گاهی جا افتاده: عمق بیشتر پایین‌تر نشان داده می‌شود (اختیاری)
    plt.title("Depth vs Magnitude")
    plt.xlabel("Magnitude")
    plt.ylabel("Depth (km)")
    plt.grid(True, linestyle=":", alpha=0.5)
    plt.tight_layout()
    plt.savefig(outpath, dpi=300)
    if show:
        plt.show()
    plt.close()

# اجرای اصلی
def main():
    args = parse_args()
    csv_path = Path(args.csv)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    df = load_and_prepare(csv_path)

    # مسیرهای ذخیره
    p1 = outdir / "map_scatter_locations.png"
    p2 = outdir / "magnitude_over_time.png"
    p3 = outdir / "hist_magnitude.png"
    p4 = outdir / "depth_vs_magnitude.png"

    # تولید نمودارها
    plot_scatter_map(df, p1, show=args.show)
    plot_magnitude_time(df, p2, show=args.show)
    plot_hist_magnitude(df, p3, show=args.show)
    plot_depth_vs_magnitude(df, p4, show=args.show)

    print("Plots saved to:", outdir.resolve())
    print(f" - {p1.name}")
    print(f" - {p2.name}")
    print(f" - {p3.name}")
    print(f" - {p4.name}")

if name == "__main__":
    main()