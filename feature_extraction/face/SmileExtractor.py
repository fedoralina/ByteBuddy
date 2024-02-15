import numpy as np
import pandas as pd
import logging

WINDOW_SIZE = 30

class SmileExtractor():

    def __init__(self, file):
        self.df = pd.read_csv(file)

    def __remove_whitespaces(self):
        self.df.columns = [col.strip() for col in self.df.columns]

    def __get_required_cols(self):
        au = self.df.filter(like="AU")
        tmp = self.df[['frame', 'timestamp']]
        self.df = pd.concat([tmp, au], axis=1)

    def __check_exceed_threshold(self, mean_AU_value_list, threshold=0.6):
        return all(mean_val >= threshold for mean_val in mean_AU_value_list)

    def __cleanup_data(self):
        self.__remove_whitespaces()
        self.__get_required_cols()

    def mean_activation_per_window(self, num_seconds=2, step_size=30):
        """
        Parameters:
            - data: DataFrame
                the required columns, like AU activations and frames, needed for further processing
            - num_seconds: int
                number of seconds required to "hold" the emotion
            - step_size: int
                amount of frames to slide within a window to 
        """

        # cleanup dataset and extract columns of interest
        self.__cleanup_data()

        # extract start and end frame number
        start_frame = self.df['frame'].iloc[0]
        end_frame = self.df['frame'].iloc[-1] + 1
        current_frame = start_frame

        num_exceeded = 0
        while current_frame < end_frame:
            if num_exceeded >= num_seconds:
                break
            remaining_frames = end_frame - current_frame
            ## drop the last frames as they cannot be taken into account as a "whole" second
            if remaining_frames < WINDOW_SIZE:
                logging.info(f"#frames = {remaining_frames} is smaller than one second (={WINDOW_SIZE}). The remaining frame amount will be dropped.")
                break
            window_start = current_frame
            # Ensure not to exceed end_frame
            window_end = min(current_frame + WINDOW_SIZE + 1, end_frame)
            window_data = self.df[(self.df['frame'] >= window_start) & (self.df['frame'] < window_end)]
            mean_AU_value_list = list(window_data[["AU06_c", "AU12_c", "AU25_c"]].mean())
            print(window_data["frame"].iloc[0], window_data["frame"].iloc[-1], len(window_data))
            logging.info(f"Frame(s) {window_data['frame'].iloc[0]} to {window_data['frame'].iloc[-1]} | Mean values of AU activations [AU06, AU12, AU25]: {[round(num, 2) for num in mean_AU_value_list]} ")

            if self.__check_exceed_threshold(mean_AU_value_list):
                num_exceeded += 1
                logging.info(f"Smile is detected for n={num_exceeded}.")
            else:
                # reset window size of smiling
                num_exceeded = 0
                logging.info("No smile detected")

            current_frame += step_size


        if num_exceeded >= num_seconds:
            logging.info("Smile was held long enough. B will be reloaded now.")
        elif (num_exceeded < num_seconds) and (num_exceeded > 0):
            logging.info("Smile was held too short to reload B completely. It has to be done again.")
        else:
            logging.info("Smile task was not executed as required. Display details in the UI.")