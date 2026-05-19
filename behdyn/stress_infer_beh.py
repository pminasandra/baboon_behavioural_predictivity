# Pranav Minasandra
# pminasandra.github.io
# 19 May 2026

import accutils as au
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

import config
import utilities

if not config.SUPPRESS_INFORMATIVE_PRINT:
    old_print = print
    print = utilities.sprint

RECOLLARED_INDS_DATA = config.DATA / "collar_replacement_data.csv"
RECOLLARED_INDS_DATA = pd.read_csv(RECOLLARED_INDS_DATA)
RECOLLARED_INDS_DATA.event_time = pd.to_datetime(RECOLLARED_INDS_DATA.event_time)
RECOLLARED_INDS_DATA.event_time -= pd.to_timedelta("3h")#timezone correction

DIR_BEFORE_ACC = config.DATA/"Stress_Acc/Before"
DIR_AFTER_ACC = config.DATA/"Stress_Acc/After"
DIR_BEH_SEQ = config.DATA/"Stress_Beh"

def infer_beh_sequences(accdf, figtitle=None):
    accdf = accdf.copy()
    accdf = au.filters.smudge_acc_data(accdf)

    accdf["vedba"] = au.feature_ext.dbas.vedba_vals(accdf)
    g = accdf.groupby(by="burst_timestamp").vedba.mean()

    df = pd.DataFrame()
    df["Timestamp"] = g.index
    g = g.reset_index()
    df["vedba_mean"] = g["vedba"]
    df["log_vedba_mean"] = np.log(df["vedba_mean"] + 1e-8)

    x = df["log_vedba_mean"].dropna()

    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.22)

    ax.hist(x, bins=100, alpha=0.6)
    ax.set_xlabel("log(VeDBA mean)")
    ax.set_ylabel("Count")

    init_threshold = float(x.median())

    vline = ax.axvline(init_threshold, color="red", linewidth=2)
    if figtitle is not None:
        ax.set_title(figtitle)

    slider_ax = fig.add_axes([0.15, 0.07, 0.7, 0.03])
    slider = Slider(
        ax=slider_ax,
        label="Threshold",
        valmin=float(x.min()),
        valmax=float(x.max()),
        valinit=init_threshold,
    )

    def update_threshold(val):
        vline.set_xdata([val, val])
        fig.canvas.draw_idle()

    slider.on_changed(update_threshold)

    plt.show()

    user_threshold = float(slider.val)

    # Keep final chosen threshold visible on returned figure
    vline.set_xdata([user_threshold, user_threshold])

    out = pd.DataFrame({
        "datetime": df["Timestamp"],
        "state": np.where(
            df["log_vedba_mean"] < user_threshold,
            "Inactive",
            "Active",
        ),
    })

    return out, user_threshold, fig, ax

def baboon_beh_seq_infer(masterdf=RECOLLARED_INDS_DATA):
    DIR_BEH_SEQ.mkdir(exist_ok=True)
    def apply_to_row(row):
        indname = row["individual_local_identifier"]
        fname = indname + ".parquet"

        before_acc = pd.read_parquet(DIR_BEFORE_ACC/fname)
        if before_acc.empty:
            return
        before_beh, _, fig, ax = infer_beh_sequences(before_acc,
                                figtitle=f"{indname}_before")
        utilities.saveimg(fig, f"histogram_logvedba_before_{indname}")

        after_acc = pd.read_parquet(DIR_AFTER_ACC/fname)
        if after_acc.empty:
            return
        after_beh, _, fig, ax = infer_beh_sequences(after_acc,
                                figtitle=f"{indname}_after")
        utilities.saveimg(fig, f"histogram_logvedba_after_{indname}")

        total_beh = pd.concat((before_beh, after_beh))
        total_beh = total_beh.reset_index()
        total_beh.to_parquet(DIR_BEH_SEQ/fname)
        return total_beh
    behdfs = masterdf.apply(apply_to_row, axis=1)

if __name__ == "__main__":
    baboon_beh_seq_infer()


