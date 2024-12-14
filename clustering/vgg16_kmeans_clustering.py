import keras.utils as image
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
import numpy as np
from sklearn.cluster import KMeans
import shutil, glob, os.path

image.LOAD_TRUNCATED_IMAGES = True
model = VGG16(weights='imagenet', include_top=False, pooling='avg')

base_dir = os.path.dirname(os.path.abspath(__file__))
imdir = os.path.join(base_dir, "input_images")
targetdir = os.path.join(base_dir, "result_images")
os.makedirs(targetdir, exist_ok=True)
number_clusters = 3

filelist = glob.glob(os.path.join(imdir, '*.jpg'))
filelist.sort()
featurelist = []
for i, imagepath in enumerate(filelist):
    img = image.load_img(imagepath, target_size=(224, 224))
    img_data = image.img_to_array(img)
    img_data = np.expand_dims(img_data, axis=0)
    img_data = preprocess_input(img_data)
    features = np.array(model.predict(img_data))
    featurelist.append(features.flatten())

kmeans = KMeans(n_clusters=number_clusters, init='k-means++', n_init=10, random_state=0).fit(np.array(featurelist))

print("\n")
for i, m in enumerate(kmeans.labels_):
    original_filename = os.path.basename(filelist[i])
    new_filename = f"{m}_{i}_{original_filename}"
    shutil.copy(filelist[i], os.path.join(targetdir, new_filename))
