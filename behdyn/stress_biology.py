# Pranav Minasandra
# pminasandra.github.io
# 19 May 2026

import matplotlib.pyplot as plt
import seaborn as sns#FIXME
import numpy as np
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

def _is_night(dtcol):
    mask1 = dtcol.dt.time.between(config.KENYA_NIGHT_BEGIN,
                        pd.to_datetime("23:59:59.999").time())
    mask2 = dtcol.dt.time.between(pd.to_datetime("00:00").time(),
                        config.KENYA_NIGHT_END)
    mask = mask1 | mask2
    return mask


DAILY_ANALYSES = {}


def daily_data_generator():
    for f in DIR_BEH_SEQ.glob("*.parquet"):
        df = pd.read_parquet(f)

        for date, chunk in df.groupby(df["datetime"].dt.to_period("D")):
            size = chunk.shape[0]

            if size <= 86400/60*0.3:
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

if (config.DATA / "stress_raw_MI_vals.parquet").exists():
    stress_beh_dyn = pd.read_parquet(config.DATA / "stress_raw_MI_vals.parquet")
    stress_beh_dyn.loc[:, "date"] = pd.to_datetime(stress_beh_dyn.timechunk).dt.date
    stress_beh_dyn.loc[:, "mi_vals_np"] = stress_beh_dyn.mi_vals.map(np.array)

def metric_to_track(f):
    DAILY_ANALYSES[f.__name__] = f
    return f

@metric_to_track
def prop_active(df, date, ind):
    p = (df.state=="Active").sum()/df.shape[0]
    return p

@metric_to_track
def prop_active_night(df, date, ind):
    df = df.copy()
    df = df.loc[_is_night(df.datetime), :]
    return prop_active(df, date, ind)

@metric_to_track
def log_pred_dec_curve(df, date, ind):
    mask1 = stress_beh_dyn["date"] == date
    mask2 = stress_beh_dyn["id"] == ind
    mask = mask1 & mask2
    arr = stress_beh_dyn.loc[mask, "mi_vals_np"]
    if arr.empty:
        print(f"Got an empty pred decay curve: {date} for {ind}")
        return np.nan
    arr = arr.item()
    arr = np.log(arr + 1e-8)
    return arr


def do_biological_analyses(bdg):
    METRIC_CHARTS = {"date": [], "id": []}
    for metric in DAILY_ANALYSES:
        METRIC_CHARTS[metric] = []

    for databundle in bdg:
        df = databundle["data"]
        df = df.copy()
        if df.empty:
            continue
        date = pd.to_datetime(databundle["timechunk"]).date()
        id_ = databundle["id"]

        METRIC_CHARTS["date"].append(date)
        METRIC_CHARTS["id"].append(id_)

        for metric in DAILY_ANALYSES:
            METRIC_CHARTS[metric].append(DAILY_ANALYSES[metric](df, date, id_))

    METRIC_CHARTS = pd.DataFrame(METRIC_CHARTS)

    METRIC_CHARTS.loc[:, "delta_days"] = 0
    rid = RECOLLARED_INDS_DATA
    for ind in METRIC_CHARTS["id"].unique():
        event_date = rid.loc[rid.individual_local_identifier == ind,
                                "event_time"].item()
        indmask = METRIC_CHARTS["id"] == ind
        METRIC_CHARTS["datetime"] = pd.to_datetime(METRIC_CHARTS["date"])
        METRIC_CHARTS.loc[indmask, "delta_days"] =\
            -(event_date - METRIC_CHARTS.loc[indmask, "datetime"]).dt.days

    fig, (ax1, ax2) = plt.subplots(1,2)
    sns.lineplot(data=METRIC_CHARTS, x="delta_days",
                        y="prop_active", hue="id", ax=ax1, linewidth=0.5)
    sns.lineplot(data=METRIC_CHARTS, x="delta_days",
                        y="prop_active_night", hue="id", ax=ax2, linewidth=0.5)
    utilities.saveimg(fig, "inital_analyses_stress")

if __name__ == "__main__":
    #compute_pred_decay_curves() 
    bdg = daily_data_generator()
    do_biological_analyses(bdg)
