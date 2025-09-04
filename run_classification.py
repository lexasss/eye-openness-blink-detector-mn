# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 14:56:52 2022

@author: Marcus
@edited: Oleg
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
from pathlib import Path
from pick import pick

import data_reader
from blink_detector import BlinkDetector
from settings import Settings

# %% Initialization

# Import and change (optional) settings
settings = Settings()
settings.plot_on = False
remove_outliers = False     # Remove outliers (pupil size values < 2 mm) and > 2.5 SD from the mean of sample in a window

# Get the dataset name
menu_prompt = 'Please choose the dataset: '
datasets = ['spectrum', 'fusion', 'xr4']

dataset, dataset_index = pick(datasets, menu_prompt, indicator='=>', default_index=2)


# %% Data import

dfs, Fs = data_reader.read(dataset)
settings.Fs = Fs


# %% Classification

plt.close('all')

bd = BlinkDetector(settings)
out_eo = []
out_pupil = []

for df in dfs:
    df_out, eye_openness_signal_vel = bd.blink_detector_eo(df.t, df.eo, settings.Fs, filter_length=settings.filter_length,
                                                        gap_dur=settings.gap_dur,
                                                        width_of_blink=settings.width_of_blink,
                                                        min_separation=settings.min_separation)

    df_out_pupil = bd.blink_detector_pupil(df.t, df.pupil, settings.Fs,
                                                gap_dur=settings.gap_dur,
                                                min_dur=settings.min_blink_dur,
                                                remove_outliers=remove_outliers,
                                                min_separation=settings.min_separation)
    if settings.plot_on:
        bd.plot_blink_detection_results(df.t,
                                        df.eo,
                                        eye_openness_signal_vel,
                                        df_out,
                                        df.pid,
                                        df.file,
                                        df.eye,
                                        pupil_signal=df.pupil,
                                        df_blink_pupil = df_out_pupil,
                                        xy = df.gaze)

    # Add participant ID to data frame
    df_out['pid'] = df_out_pupil['pid'] = df.pid
    df_out['eye'] = df_out_pupil['eye'] = df.eye
    df_out['trial'] = df_out_pupil['trial'] = df.file
    df_out['trial_duration'] = df_out_pupil['trial_duration'] = len(df.eo) / settings.Fs
    df_out['blink_rate'] = len(df_out) / df_out['trial_duration']
    df_out_pupil['blink_rate'] = len(df_out_pupil) / df_out_pupil['trial_duration']

    out_eo.append(df_out)
    out_pupil.append(df_out_pupil)


# %% Exporting results 

cwd = Path.cwd()
results_path = cwd / 'results'
os.makedirs(results_path, exist_ok=True)

if len(out_eo) > 0:
    pd.concat(out_eo).to_csv(results_path / 'eo.csv')

if len(out_pupil) > 0:
    pd.concat(out_pupil).to_csv(results_path / 'pupil.csv')
