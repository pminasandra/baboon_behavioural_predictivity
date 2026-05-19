# Pranav Minasandra
# pminasandra.github.io
# Dec 24, 2022

import json
import multiprocessing as mp
from pathlib import Path

import pandas as pd

#Directories
PROJECTROOT = Path("/home/pranav/Projects/Bout_Duration_Distributions/").absolute()
EAS_SHARED_MOUNT_POINT = Path("/media/pranav/MPI_Dirs/EAS_shared/")
if Path('./dirs.json').exists():
    with open("./dirs.json") as ddata:
        dirdata = json.load(ddata)
        PROJECTROOT = Path(dirdata["cwd"])
        EAS_SHARED_MOUNT_POINT = Path(dirdata["servermount"])
DATA = PROJECTROOT / "Data"
FIGURES = PROJECTROOT / "Figures"


BABOON_ACC_DIR = "baboon/working/data/processed/2025/acc/acc_v1"
BABOON_BEH_SEQ_DIR ="baboon/working/data/processed/2025/acc/inactivity"
BABOON_ACC_DIR = EAS_SHARED_MOUNT_POINT / BABOON_ACC_DIR
BABOON_BEH_SEQ_DIR = EAS_SHARED_MOUNT_POINT / BABOON_BEH_SEQ_DIR


# Species
species = ['baboon']
for spec in species:
    (DATA / spec).mkdir(parents=True, exist_ok=True)
    (DATA / 'FitResults' / spec).mkdir(parents=True, exist_ok=True)

# Image saving
formats = ['png', 'svg', 'pdf']

# Night
ONLY_NIGHT = True
KENYA_NIGHT_BEGIN = pd.to_datetime("16:00").time()
KENYA_NIGHT_END = pd.to_datetime("03:00").time()

# General
MIN_DATA_POINTS = 60 * 24 * 20#at least 20 days
TOLERABLE_TIMESTAMP_OFFSET = 29#seconds either way

# Distribution fitting
def all_distributions(fit):
    return {'Exponential': fit.exponential,
            'Lognormal': fit.lognormal,
            'Power_Law': fit.power_law,
            'Truncated_Power_Law': fit.truncated_power_law#,
#            'Stretched_Exponential': fit.stretched_exponential
        }

discrete = True
xmin = 2.0

distributions_to_numbers = {
    'Exponential': 0,
    'Lognormal': 1,
    'Power_Law': 2,
    'Truncated_Power_Law': 3#,
#    'Stretched_Exponential': 4
}


# Distribution plotting
colors = {
    'Exponential': 'cyan',
    'Lognormal': 'blue',
    'Power_Law': 'red',
    'Truncated_Power_Law': 'maroon'#,
#    'Stretched_Exponential': 'pink'
}
fit_line_style = 'dotted'
error_bars_rlim = 25

# Mutual information analyses
NUM_REPS_PER_SUB_SIZE = 5

# markovised sequence analysis and plotting
ADD_MARKOV=False
NUM_MARKOVISED_SEQUENCES = 30
markovised_plot_color = "darkgreen"


# Survival analysis and plots
survival_plot_color = "darkblue"
survival_randomization_plot_color = "darkgreen"
survival_xscale = "log" #Use "linear" 
survival_yscale = "linear" #for typical

survival_exclude_last_few_points = True
survival_num_points_to_exclude = 100

# Fitting specific
minimum_bouts_for_fitting = 250
insufficient_data_flag = 'insufficient_data'

# Bootstrapping
ADD_BOOTSTRAPPING=False
NUM_BOOTSTRAP_REPS = 100

# Miscellaneous
SUPPRESS_INFORMATIVE_PRINT = False
NUM_CORES = 8

COLLAGE_IMAGES = True # Set to false to get normal images
# Collage images increases font size

if __name__=="__main__":
    import utilities
    utilities.sprint(f"config.py speaking. current projectroot is {PROJECTROOT}")

