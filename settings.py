import numpy as np

class Settings():
    def __init__(self):

        self.plot_on = False # Visualize detection results
        self.save_fig = False # Save visualization to file
        self.debug = False # Prints output when debugging

        self.Fs = 600  # Sample rate of eye tracker

        # in mm, used to distinguish full from partial blinks
        # (only for visualization purposes)
        self.full_blink_max_opening = 2

        self.gap_dur = 40 # max gaps between period of data loss, interpolate smaller gaps
        self.min_amplitude = 0.1 # % of fully open eye (0.1 - 10%)
        self.min_separation = 100 # min separation between blinks

        self.filter_length = 25  # in ms
        self.width_of_blink = 15  # in ms width of peak to initially detect
        self.min_blink_dur = 30  # reject blinks shorter than 30 ms

        self.min_pupil_size = 2 # in mm
        self.window_len = np.nan # in ms window over which to exclude outliers (np.nan means whole trial)
        self.treshold_SD = 2.5 # remove values 2.5 * SD from the mean
