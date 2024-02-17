from abc import ABC, abstractmethod 
import pandas as pd

class SmileExtractor(ABC):
    """
    Abstract class FacialFeaturesExtractor which holds the preprocessing steps for the extraction of facial features.
    In this stage of the development, Action Units (AUs) and angles of the mouth are developed as inheriting classes 
    to recognize if the player is smiling and act accordingly.
    """

    def __init__(self, file):
        self.df = pd.read_csv(file)

    def remove_whitespaces(self):
        self.df.columns = [col.strip() for col in self.df.columns]

    @abstractmethod
    def get_required_cols(self):
        pass
    
    def cleanup_data(self):
        self.remove_whitespaces()
        self.get_required_cols()