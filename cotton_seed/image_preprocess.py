import os
import random
import shutil
import xml.dom.minidom
from zipfile import ZipFile

import cv2


class ImageProcessor(object):
    def __init__(self, image_path, nested_path):
        """ Pass zipped file path (both absolute and relative work), nested_path is the nested directory.
        e.g. for data cotton-seed labels-20230513T132534Z-001.zip  nested_path is 'cotton-seed labels/'"""
        self.imagePath = image_path
        self.nested_path = nested_path

    def preprocess(self, proportion):
        """ Preprocess will parse xml files to acquire pixel coordinates for image segmentation, as well as labels;
        segmented image will be labeled on the name. Segmented image data will be resized before output for further
        conduction. Preprocessed data will be stored under temp/Data into two parts : Test & Train, respectively.
        For parameters: proportion is training data: testing data"""
        temp_path = 'temp'
        if os.path.exists(temp_path):
            shutil.rmtree(temp_path)
        # JPG Path
        img_path = 'temp/JPEGImages/'
        # XML Path
        anno_path = 'temp/Annotations/'
        # Segmented & Labeled Images Path
        test_data_path = 'temp/Data/Test/'
        train_data_path = 'temp/Data/Train/'
        os.makedirs(test_data_path)
        os.makedirs(train_data_path)

        with ZipFile(self.imagePath, 'r') as zipObject:
            listOfFileNames = zipObject.namelist()
            for fileName in listOfFileNames:
                if fileName.endswith('.jpg'):
                    zipObject.extract(fileName, img_path)
                if fileName.endswith('.xml'):
                    zipObject.extract(fileName, anno_path)

        img_path += self.nested_path
        anno_path += self.nested_path
        imageList = os.listdir(img_path)
        # Shuffle images before label
        random.shuffle(imageList)

        cnt = 0

        for image in imageList:
            image_pre, ext = os.path.splitext(image)
            img_file = img_path + image
            img = cv2.imread(img_file)
            xml_file = anno_path + image_pre + '.xml'
            DOMTree = xml.dom.minidom.parse(xml_file)
            collection = DOMTree.documentElement
            objects = collection.getElementsByTagName("object")

            for object in objects:
                cnt += 1
                label = object.getElementsByTagName('name')[0].childNodes[0].data
                bndbox = object.getElementsByTagName('bndbox')[0]
                xmin = bndbox.getElementsByTagName('xmin')[0]
                xmin_data = xmin.childNodes[0].data
                ymin = bndbox.getElementsByTagName('ymin')[0]
                ymin_data = ymin.childNodes[0].data
                xmax = bndbox.getElementsByTagName('xmax')[0]
                xmax_data = xmax.childNodes[0].data
                ymax = bndbox.getElementsByTagName('ymax')[0]
                ymax_data = ymax.childNodes[0].data
                xmin = int(xmin_data)
                xmax = int(xmax_data)
                ymin = int(ymin_data)
                ymax = int(ymax_data)
                img_seg = img[ymin:ymax, xmin:xmax, :]
                # img_seg_resize = cv2.resize(img_seg, (new_size, new_size))
                res_path = (test_data_path if cnt % proportion == 0 else train_data_path) + label + "/"
                if not os.path.exists(res_path):
                    os.makedirs(res_path)
                cv2.imwrite(res_path + 'img_{}_{}.jpg'.format(label, cnt), img_seg)
