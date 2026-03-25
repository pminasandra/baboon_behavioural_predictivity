# Pranav Minasandra
# pminasandra.github.io
# Dec 24, 2022

import multiprocessing as mp
import os
import os.path


#Directories
PROJECTROOT = os.path.abspath("/home/pranav/Projects/Bout_Duration_Distributions/")
if os.path.exists('./cwd.txt'):
    with open("./cwd.txt") as cwd:
        PROJECTROOT = cwd.read().rstrip()
DATA = os.path.join(PROJECTROOT, "Data")
FIGURES = os.path.join(PROJECTROOT, "Figures")
EAS_SHARED_MOUNT_POINT="/media/pranav/MPI_Dirs/EAS_shared/"


BABOON_BEH_SEQ_DIR ="baboon/working/data/processed/2025/acc/inactivity"
BABOON_BEH_SEQ_DIR = os.path.join(*BABOON_BEH_SEQ_DIR.split('/'))
BABOON_BEH_SEQ_DIR = os.path.join(EAS_SHARED_MOUNT_POINT, BABOON_BEH_SEQ_DIR)


# Species
species = ['baboon']
os.makedirs(os.path.join(DATA, 'FitResults'), exist_ok=True)
for spec in species:
    os.makedirs(os.path.join(DATA, spec), exist_ok=True)
    os.makedirs(os.path.join(DATA, 'FitResults', spec), exist_ok=True)

# Image saving
formats = ['png', 'svg', 'pdf']


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

