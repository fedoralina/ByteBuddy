import logging
import argparse

from face.AUExtractor import AUSmileExtractor
from face.AngleSmileExtractor import AngleSmileExtractor
from gesture.DirectionRecognizer import DirectionRecognizer


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    force=True
)

def option_angle():
    logging.info("-------------Angle Face Feature Extraction-------------")
    # for happy face
    angle_smile_extractor = AngleSmileExtractor("./face/AU_data/happy_fed.csv")
    angle_smile_extractor = AngleSmileExtractor("./face/AU_data/happy_c.csv")
    angle_smile_extractor.mean_activation_per_window()

    # for neutral face
    # angle_smile_extractor = AngleSmileExtractor("./face/AU_data/neutral_c.csv")
    # angle_smile_extractor.mean_activation_per_window()

def option_au():
    logging.info("-------------Temporal Face Feature Extraction-------------")
    # for happy face
    au_smile_extractor = AUSmileExtractor("./face/AU_data/happy_fed.csv")
    au_smile_extractor.mean_activation_per_window()
    
    # for neutral face
    #au_smile_extractor = AUSmileExtractor("./face/AU_data/neutral_fed.csv")
    #au_smile_extractor.mean_activation_per_window()

    # smile was held too shortly
    #au_smile_extractor = AUSmileExtractor("./face/AU_data/happy_fed_short_smile.csv")
    #au_smile_extractor.mean_activation_per_window(step_size=15)

def option_gesture():
    logging.info("-------------Gesture Feature Extraction-------------")
    direction_recognizer = DirectionRecognizer()
    direction_recognizer.read_templates()
    direction_recognizer.draw_GUI()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Feature extraction selector")
    parser.add_argument("--angle", action="store_true", help="Extraction of face angle feature")
    parser.add_argument("--au", action="store_true", help="Extraction of face AU feature")
    parser.add_argument("--gesture", action="store_true", help="Extraction of gesture feature")
    args = parser.parse_args()
    if args.angle:
        option_angle()
    elif args.au:
        option_au()
    elif args.gesture:
        option_gesture()
    else:
        print("Please specify one of the following options: --angle / --au / --gesture")
    
    