from face.SmileExtractor import SmileExtractor
import logging
logging.basicConfig(
    level=logging.INFO,
    #format="%(asctime)s | [%(levelname)s] | %(message)s | function: %(funcName)s",
    format="%(asctime)s [%(levelname)s]: %(message)s",
    force=True
)


if __name__ == '__main__':
    #----extract smile 
    logging.info("-------------Temporal Face Feature Extraction-------------")
    # for happy face
    smile_extractor = SmileExtractor("./face/AU_data/happy_fed.csv")
    smile_extractor.mean_activation_per_window()

    # for neutral face
    smile_extractor = SmileExtractor("./face/AU_data/neutral_fed.csv.csv")
    smile_extractor.mean_activation_per_window()