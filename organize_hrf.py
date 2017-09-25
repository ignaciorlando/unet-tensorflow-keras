
import urllib.request # for downloading files
from os import path, makedirs, listdir
import zipfile
from shutil import copyfile
from numpy import invert
from scipy import misc
import re


# URLs to download images
URLs = ['https://www5.cs.fau.de/fileadmin/research/datasets/fundus-images/healthy.zip', 
        'https://www5.cs.fau.de/fileadmin/research/datasets/fundus-images/glaucoma.zip',
        'https://www5.cs.fau.de/fileadmin/research/datasets/fundus-images/diabetic_retinopathy.zip',
        'https://www5.cs.fau.de/fileadmin/research/datasets/fundus-images/healthy_manualsegm.zip',
        'https://www5.cs.fau.de/fileadmin/research/datasets/fundus-images/glaucoma_manualsegm.zip',
        'https://www5.cs.fau.de/fileadmin/research/datasets/fundus-images/diabetic_retinopathy_manualsegm.zip']

# URL filenames
URL_FILENAMES_IMAGES = ['healthy.zip', 'glaucoma.zip', 'diabetic_retinopathy.zip']
URL_FILENAMES_LABELS = ['healthy_manualsegm.zip', 'glaucoma_manualsegm.zip', 'diabetic_retinopathy_manualsegm.zip']
ALL_URL_FILENAMES = URL_FILENAMES_IMAGES + URL_FILENAMES_LABELS

# Training data paths
TRAINING_IMAGES_DATA_PATH = 'HRF/training/images'
TRAINING_GT_DATA_PATH = 'HRF/training/gt'
# Test data paths
TEST_IMAGES_DATA_PATH = 'HRF/test/images'
TEST_GT_DATA_PATH = 'HRF/test/gt'






def unzip_files(root_path, zip_filenames, data_path):
    # Unzip files    
    for i in range(0, len(zip_filenames)):
        zip_ref = zipfile.ZipFile(path.join(root_path, zip_filenames[i]), 'r')
        zip_ref.extractall(data_path)
        zip_ref.close()


def copy_images(root_folder, filenames, data_path):
    # Create the folder if it doesnt exist
    if not path.exists(data_path):
        makedirs(data_path)
    # Copy images in filenames to data_path
    for i in range(0, len(filenames)):
        current_file = filenames[i]
        if current_file[-3:]=='JPG':
            target_filename = current_file[:-3] + 'jpg'
        else:
            target_filename = current_file
        copyfile(path.join(root_folder, current_file), path.join(data_path, target_filename))            


def copy_labels(root_folder, filenames, data_path):
    # Initialize folders
    false_class_folder = path.join(data_path, '0')
    true_class_folder = path.join(data_path, '1')
    # Create folders
    if not path.exists(false_class_folder):
        makedirs(false_class_folder)
    if not path.exists(true_class_folder):
        makedirs(true_class_folder)
    # Copy the images
    for i in range(0, len(filenames)):
        current_filename = filenames[i]
        # Open the image
        labels = misc.imread(path.join(root_folder, current_filename))
        # Save the image as a .png file
        misc.imsave(path.join(true_class_folder, current_filename[:-3] + 'png'), labels)
        misc.imsave(path.join(false_class_folder, current_filename[:-3] + 'png'), invert(labels))

def natural_key(string_):
    """See http://www.codinghorror.com/blog/archives/001018.html"""
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]


# Check if tmp exists
if not path.exists('tmp'):
    makedirs('tmp')

# Download images from the known links to tmp
for i in range(0, len(URLs)):
    data_path = path.join('tmp', ALL_URL_FILENAMES[i])
    if not path.exists(data_path):
        print('Downloading data from ' + URLs[i])
        urllib.request.urlretrieve(URLs[i], data_path)
    else:
        print(ALL_URL_FILENAMES[i] + ' already exists. Skipping download.')

# Check if HRF folders exist
if not path.exists('tmp/HRF/images'):
    makedirs('tmp/HRF/images')
if not path.exists('tmp/HRF/gt'):
    makedirs('tmp/HRF/gt')

# Unzip images in tmp/images
print('Unzipping images...')
unzip_files('tmp', URL_FILENAMES_IMAGES, 'tmp/HRF/images')
# Unzip images in tmp/gt
print('Unzipping labels...')
unzip_files('tmp', URL_FILENAMES_LABELS, 'tmp/HRF/gt')

# Generate training/test images ----------
print('Copying images...')
# 1. Get image names
image_filenames = sorted(listdir('tmp/HRF/images'), key=natural_key)
# 2. Copy training images
copy_images('tmp/HRF/images', image_filenames[:15], 'datasets/HRF/training/images')
# 2. Copy test images
copy_images('tmp/HRF/images', image_filenames[-30:], 'datasets/HRF/test/images')
# ----------------------------------------

# Generate training/test labels ----------
print('Copying labels...')
# 1. Get labels names
gt_filenames = sorted(listdir('tmp/HRF/gt'), key=natural_key)
# 2. Copy training labels
copy_labels('tmp/HRF/gt', gt_filenames[:15], 'datasets/HRF/training/gt')
# 2. Copy test labels
copy_labels('tmp/HRF/gt', gt_filenames[-30:], 'datasets/HRF/test/gt')
# ----------------------------------------
