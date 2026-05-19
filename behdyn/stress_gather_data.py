# Pranav Minasandra
# 19 May 2026
# pminasandra.github.io

from pathlib import Path

import pandas as pd

import config
import utilities

if not config.SUPPRESS_INFORMATIVE_PRINT:
    old_print = print
    print = utilities.sprint

RECOLLARED_INDS_DATA = config.DATA / "collar_replacement_data.csv"
RECOLLARED_INDS_DATA = pd.read_csv(RECOLLARED_INDS_DATA)
RECOLLARED_INDS_DATA.event_time = pd.to_datetime(RECOLLARED_INDS_DATA.event_time)
RECOLLARED_INDS_DATA.event_time -= pd.to_timedelta("3h")#timezone correction

def gather_data(bigdf=RECOLLARED_INDS_DATA):
    """
    brings together all required acc data under one roof.
    """

    output_dir = config.DATA / "Stress_Acc"
    bdir, adir = output_dir/"Before", output_dir/"After"
    bdir.mkdir(parents=True, exist_ok=True)
    adir.mkdir(parents=True, exist_ok=True)

    def apply_to_row(row):
        fname = row["individual_local_identifier"] + ".parquet"
        fpath = config.BABOON_ACC_DIR / fname
        event = row["event_time"]
        start = event - pd.to_timedelta("100d")
        end   = event + pd.to_timedelta("100d")

# let's leave out around 6h around the event
        before = lambda t: (start < t) & (t < event - pd.to_timedelta("3h"))
        after = lambda t: (end > t) & (t > event + pd.to_timedelta("3h"))

        df = pd.read_parquet(fpath)
#        df["timestamp"] = (
#            df["timestamp"]
#            .dt.tz_convert("UTC")
#            .dt.tz_localize(None)
#        )

        df_b = df.loc[before(df.timestamp)].copy()
        df_a = df.loc[after(df.timestamp)].copy()

        for df in (df_a, df_b):
            df = df.sort_values(by="timestamp")
            df = df.reset_index()

        df_b.to_parquet(bdir / fname, index=False)
        df_a.to_parquet(adir / fname, index=False)

    bigdf.apply(apply_to_row, axis=1)

if __name__ == "__main__":
    gather_data()
