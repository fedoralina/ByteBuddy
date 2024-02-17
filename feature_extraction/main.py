from face.AUExtractor import AUSmileExtractor
from face.AngleSmileExtractor import AngleSmileExtractor
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    force=True
)


if __name__ == '__main__':
    #----extract smile 
    logging.info("-------------Temporal Face Feature Extraction-------------")
    # for happy face
    #au_smile_extractor = AUSmileExtractor("./face/AU_data/happy_fed.csv")
    #au_smile_extractor.mean_activation_per_window()
    
    # for neutral face
    #au_smile_extractor = AUSmileExtractor("./face/AU_data/neutral_fed.csv")
    #au_smile_extractor.mean_activation_per_window()

    # smile was held too shortly
    #au_smile_extractor = AUSmileExtractor("./face/AU_data/happy_fed_short_smile.csv")
    #au_smile_extractor.mean_activation_per_window(step_size=15)


    logging.info("-------------Angle Face Feature Extraction-------------")
    # for happy face
    #angle_smile_extractor = AngleSmileExtractor("./face/AU_data/happy_fed.csv")
    angle_smile_extractor = AngleSmileExtractor("./face/AU_data/happy_c.csv")
    angle_smile_extractor.mean_activation_per_window()

    # for neutral face
    #angle_smile_extractor = AngleSmileExtractor("./face/AU_data/neutral_c.csv")
    #angle_smile_extractor.mean_activation_per_window()
