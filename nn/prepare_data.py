import os
import shutil
import numpy as np

DATA_HOME_DIR = "../datasets/data/"


def create_directories():
    # %cd $DATA_HOME_DIR
    # %mkdir valid
    # %mkdir results
    # %mkdir -p sample/train
    # %mkdir -p sample/test
    # %mkdir -p sample/valid
    # %mkdir -p sample/results
    # %mkdir -p test/unknown
    pass


# def create_valid_dataset():
#     g = glob('*.jpg')
#     shuf = np.random.permutation(g)
#     for i in range(2000):
#         os.rename(shuf[i], DATA_HOME_DIR+'/valid/' + shuf[i])


def split_dataset_into_test_and_train_sets(all_data_dir, training_data_dir, testing_data_dir, testing_data_pct=0.1):
    # Recreate testing and training directories
    if testing_data_dir.count('/') > 1:
        shutil.rmtree(testing_data_dir, ignore_errors=False)
        os.makedirs(testing_data_dir)
        print("Successfully cleaned directory {0}".format(testing_data_dir))
    else:
        print(
            "Refusing to delete testing data directory {0} as we prevent you from doing stupid things!".format(
                testing_data_dir
            ))

    if training_data_dir.count('/') > 1:
        shutil.rmtree(training_data_dir, ignore_errors=False)
        os.makedirs(training_data_dir)
        print("Successfully cleaned directory {0}".format(training_data_dir))
    else:
        print(
            "Refusing to delete testing data directory {0} as we prevent you from doing stupid things!".format(
                testing_data_dir
            ))

    num_training_files = 0
    num_testing_files = 0

    for subdir, dirs, files in os.walk(all_data_dir):
        category_name = os.path.basename(subdir)

        # Don't create a subdirectory for the root directory
        print(category_name + " vs " + os.path.basename(all_data_dir))
        if category_name == os.path.basename(all_data_dir):
            continue

        training_data_category_dir = os.path.join(
            training_data_dir, category_name)
        testing_data_category_dir = os.path.join(
            testing_data_dir, category_name)

        if not os.path.exists(training_data_category_dir):
            os.mkdir(training_data_category_dir)

        if not os.path.exists(testing_data_category_dir):
            os.mkdir(testing_data_category_dir)

        for file in files:
            input_file = os.path.join(subdir, file)
            if np.random.rand(1) < testing_data_pct:
                shutil.copy(input_file,
                            os.path.join(testing_data_dir, category_name, file))
                num_testing_files += 1
            else:
                shutil.copy(input_file,
                            os.path.join(training_data_dir, category_name, file))
                num_training_files += 1

    print("Processed {0} training files.".format(num_training_files))
    print("Processed {0} testing files.".format(num_testing_files))


ALL_DATA_HOME_DIR = "../datasets/downloads/"
DATA_TRAIN_DIR = "../data/train"
DATA_TEST_DIR = "../data/test"


split_dataset_into_test_and_train_sets(ALL_DATA_HOME_DIR,DATA_TRAIN_DIR,DATA_TEST_DIR)