import getopt
import sys

import image_preprocess


def main(argv):
    dire = ''
    prop = ''
    try:
        opts, args = getopt.getopt(argv, "d:p:", ["directory=", "proportion="])
    except getopt.GetoptError:
        print('main.py -d <directory> -p <proportion>')
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -d <directory> -p <proportion>')
            sys.exit(1)
        elif opt in ("-d", "--directory"):
            dire = arg
        elif opt in ("-p", "--proportion"):
            prop = arg
    if dire == "":
        print('data directory undefined')
        sys.exit(1)
    if prop == '':
        prop = 8  # by default, the proportion that train : test is 8
    print('data directory: ' + dire)
    print('train/test: ' + str(prop))
    nested_path = "cotton-seed labels/"  # Hardcode

    image_processor = image_preprocess.ImageProcessor(dire, nested_path)
    image_processor.preprocess(int(prop))


if __name__ == "__main__":
    main(sys.argv[1:])
