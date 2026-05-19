# Pranav Minasandra
# pminasandra.github.io
# 19 May 2026

import pandas as pd

import config
import persistence
import utilities

if not config.SUPPRESS_INFORMATIVE_PRINT:
    old_print = print
    print = utilities.sprint

RECOLLARED_INDS_DATA = config.DATA / "collar_replacement_data.csv"
RECOLLARED_INDS_DATA = pd.read_csv(RECOLLARED_INDS_DATA)
RECOLLARED_INDS_DATA.event_time = pd.to_datetime(RECOLLARED_INDS_DATA.event_time)
RECOLLARED_INDS_DATA.event_time -= pd.to_timedelta("3h")#timezone correction

DIR_BEH_SEQ = config.DATA/"Stress_Beh"

def daily_data_generator():
    for f in DIR_BEH_SEQ.glob("*.parquet"):
        df = pd.read_parquet(f)

        for date, chunk in df.groupby(df["datetime"].dt.to_period("D")):
            size = chunk.shape[0]

            if size <= 86400/60*0.75:
                continue
            databundle = {}
            databundle["data"] = chunk
            databundle["species"] = "baboon"
            databundle["id"] = f.name[:-len(".parquet")]
            databundle["timechunk"] = str(date)

            yield databundle

def compute_pred_decay_curves():
    timelags = persistence._time_slots_for_sampling(1, 60, 25)
    bdg = daily_data_generator()
    persistence.complete_MI_analysis(
        bdg=bdg,
        add_markov=False,
        timelags=timelags,
        bialek_correction=False,
        fprefix="stress"
    )

if __name__ == "__main__":
    compute_pred_decay_curves() 
