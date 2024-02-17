from face.SmileExtractor import SmileExtractor
import logging
import math

WINDOW_SIZE = 30

class AngleSmileExtractor(SmileExtractor):

    def __init__(self, file):
        super().__init__(file)

    def get_required_cols(self):
        self.df = self.df[['frame', 'timestamp', 'x_30', 'y_30', 'x_48', 'y_48', 'x_54', 'y_54']]
    
    def __calculate_angles(self, x1, y1, x2, y2, x3, y3):
        # calc distances between points
        a = math.sqrt((x2 - x3)**2 + (y2 - y3)**2)
        b = math.sqrt((x1 - x3)**2 + (y1 - y3)**2)
        c = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

        # calc angles
        angle_A = math.degrees(math.acos((b**2 + c**2 - a**2) / (2 * b * c)))
        angle_B = math.degrees(math.acos((a**2 + c**2 - b**2) / (2 * a * c)))
        angle_C = 180 - angle_A - angle_B

        return angle_A, angle_B, angle_C

    def __check_exceed_threshold(self, LM_angles_start, LM_angles):
        # requirement 1: angle at LM30 increases (min +16°)
        req_1 = (LM_angles[0] - LM_angles_start[0]) >= 16.0
        # requirement 2: angle at LM48 decreases (min -6°)
        req_2 = (LM_angles[1] - LM_angles_start[1]) <= 6.0
        # requirement 3: angle at LM54 decreases (min -6°)
        req_3 = (LM_angles[2] - LM_angles_start[2]) <= 6.0

        if (req_1 and req_2 and req_3):
            return True
        else:
            return False
    
    def mean_activation_per_window(self, num_seconds = 2, step_size = 10):
        """
        Parameters:
            - num_seconds: int
                number of seconds required to "hold" the emotion
            - step_size: int
                amount of frames to slide within a window to 
        """

        # cleanup dataset and extract columns of interest
        self.cleanup_data()

        # extract start and end frame number
        start_frame = self.df['frame'].iloc[0]
        end_frame = self.df['frame'].iloc[-1] + 1
        current_frame = start_frame
        LM_angles_start = self.__calculate_angles(*list(self.df.loc[0, ['x_30', 'y_30', 'x_48', 'y_48', 'x_54', 'y_54']].values))

        num_exceeded = 0
        while current_frame < end_frame:
            if num_exceeded >= num_seconds:
                break
            remaining_frames = end_frame - current_frame
            ## drop the last frames as they cannot be taken into account as a "whole" second
            if remaining_frames < WINDOW_SIZE:
                logging.info(f"#frames = {remaining_frames} is smaller than 1 second (={WINDOW_SIZE} frames). The remaining frame amount will be dropped.")
                break
            window_start = current_frame
            # Ensure not to exceed end_frame
            window_end = min(current_frame + WINDOW_SIZE + 1, end_frame)
            window_data = self.df[(self.df['frame'] >= window_start) & (self.df['frame'] < window_end)]
            
            mean_LM_positions = list(window_data[['x_30', 'y_30', 'x_48', 'y_48', 'x_54', 'y_54']].mean())
            LM_angles = self.__calculate_angles(*mean_LM_positions)

            logging.info(f"Frame(s) {window_data['frame'].iloc[0]} to {window_data['frame'].iloc[-1]} | Mean values of LM angles [LM30, LM48, LM54]: {[round(num, 2) for num in LM_angles]} ")

            if self.__check_exceed_threshold(LM_angles_start, LM_angles):
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
