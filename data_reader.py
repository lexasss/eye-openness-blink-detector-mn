# -*- coding: utf-8 -*-
"""
@author: Marcus
@edited: Oleg
"""

import numpy as np
import pandas as pd
import os

from pathlib import Path

def read(dataset_name):
    cwd = Path.cwd()
    dataset_path = cwd / 'data' / f'{dataset_name}'

    eyes = ['left', 'right']
    
    # All loaded data
    dfs = []
    Fs = 0
    
    if 'spectrum' in dataset_name:

        Fs = 600
        
        # list all folders (each folder is a participant) in trial
        pids = [f for f in dataset_path.iterdir() if f.is_dir()] #[4]

        for pid in pids:
            
            for eye in eyes:
                
                pid_name = str(pid).split(os.sep)[-1]
                files = pid.rglob('*.tsv')
                for file in files:

                    filename = str(file).split(os.sep)[-1][:-4]

                    # if 'Center' not in filename:
                    #     continue

                    print(f'pid: {pid_name}, eye: {eye}, condition: {filename}')
                    df = pd.read_csv(Path(file), sep='\t')
                    eye_openness_signal = np.c_[df[f'{eye}_eye_openness_value']]
                    eye_openness_signal = np.squeeze(eye_openness_signal)

                    pupil_signal = np.array(df[f'{eye}_pupil_diameter'])

                    t = np.array(df['system_time_stamp'])
                    t = (t - t[0]) / 1000

                    xy = np.c_[df[f'{eye}_gaze_point_on_display_area_x'],
                                df[f'{eye}_gaze_point_on_display_area_y']]
                    
                    dfs.append({'t': t, 'eo': eye_openness_signal, 'pupil': pupil_signal,
                                'gaze': xy,'pid': pid_name, 'file': filename, 'eye': eye})

    elif 'fusion' in dataset_name:

        Fs = 120
        for eye in eyes:

            files = dataset_path.rglob('*.tsv')
            for file in files:

                filename = str(file).split(os.sep)[-1][:-4]
                pid_name = filename.split('-')[0].strip()
                filename = filename.split('-')[1].strip()

                print(file)
                df = pd.read_csv(Path(file), sep='\t', decimal = ',')
                eye_openness_signal = np.c_[df[f'Eye openness {eye}']]
                eye_openness_signal = np.squeeze(eye_openness_signal)

                pupil_signal = np.array(df[f'Pupil diameter {eye}'])
                t = np.array(df['Recording timestamp'])
                t = (t - t[0]) / 1000

                xy = np.c_[df[f'Gaze direction {eye} X'],
                            df[f'Gaze direction {eye} Y']]

                dfs.append({'t': t, 'eo': eye_openness_signal, 'pupil': pupil_signal,
                            'gaze': xy,'pid': pid_name, 'file': filename, 'eye': eye})

    elif 'xr4' in dataset_name:

        Fs = 200
        for eye in eyes:

            files = dataset_path.rglob('*.csv')
            for file in files:

                filename = str(file).split(os.sep)[-1][:-4]
                pid_name = '0'

                print(f'filename [{eye}]')
                
                df = pd.read_csv(Path(file), sep=',', decimal = '.')
                eye_openness_signal = np.array(df[f'{eye}_eye_openness'])
                pupil_signal = np.array(df[f'{eye}_pupil_diameter_in_mm'])
                t = np.array(df['relative_to_unix_epoch_timestamp'])
                t = (t - t[0]) / 1_000_000

                xy = np.c_[df[f'{eye}_forward_x'],
                           df[f'{eye}_forward_y']]
                
                pupil_signal[pupil_signal < 0.1] = np.nan

                dfs.append({'t': t, 'eo': eye_openness_signal, 'pupil': pupil_signal,
                            'gaze': xy, 'pid': pid_name, 'file': filename, 'eye': eye})

    else:
        print(f'Type "{dataset_name}" is not supported')


    return dfs, Fs    