import os
import shutil
import numpy as np



ALL_DATA_HOME_DIR = "data"
DATA_TRAIN_DIR = "dataset/train"
DATA_TEST_DIR = "dataset/valid"
def create_dirs ():
    pass

def split_dataset_into_test_and_train_sets(all_data_dir, training_data_dir, valid_data_dir, valid_data_pct=0.2):
    # Recreate testing and training directories
    if valid_data_dir.count('/') > 1:
        shutil.rmtree(valid_data_dir, ignore_errors=False)
        os.makedirs(valid_data_dir)
        print("Successfully cleaned directory {0}".format(valid_data_dir))
    else:
        print(
            "Refusing to delete testing data directory {0} as we prevent you from doing stupid things!".format(
                valid_data_dir
            ))

    if training_data_dir.count('/') > 1:
        shutil.rmtree(training_data_dir, ignore_errors=False)
        os.makedirs(training_data_dir)
        print("Successfully cleaned directory {0}".format(training_data_dir))
    else:
        print(
            "Refusing to delete testing data directory {0} as we prevent you from doing stupid things!".format(
                valid_data_dir
            ))

    num_training_files = 0
    num_testing_files = 0

    for subdir, _, files in os.walk(all_data_dir):
        category_name = os.path.basename(subdir)

        # Don't create a subdirectory for the root directory
        print(category_name + " vs " + os.path.basename(all_data_dir))
        if category_name == os.path.basename(all_data_dir):
            continue

        training_data_category_dir = os.path.join(
            training_data_dir, category_name)
        testing_data_category_dir = os.path.join(
            valid_data_dir, category_name)

        if not os.path.exists(training_data_category_dir):
            os.mkdir(training_data_category_dir)

        if not os.path.exists(testing_data_category_dir):
            os.mkdir(testing_data_category_dir)

        for file in files:
            input_file = os.path.join(subdir, file)
            if np.random.rand(1) < valid_data_pct:
                shutil.copy(input_file,
                            os.path.join(valid_data_dir, category_name, file))
                num_testing_files += 1
            else:
                shutil.copy(input_file,
                            os.path.join(training_data_dir, category_name, file))
                num_training_files += 1

    print("Processed {0} training files.".format(num_training_files))
    print("Processed {0} validation files.".format(num_testing_files))




split_dataset_into_test_and_train_sets(ALL_DATA_HOME_DIR,DATA_TRAIN_DIR,DATA_TEST_DIR)