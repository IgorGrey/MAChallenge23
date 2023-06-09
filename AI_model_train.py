import cv2
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
import glob
import json

# Gather all images
with open("config.json", "r") as config_file:
    config = config_file.read()
    config = json.loads(config)

img_dir = r"C:\Users\Dom\MAChallenge23\imgs"

img_files = glob.glob(img_dir + r"\*.jpg")

print(img_files)
