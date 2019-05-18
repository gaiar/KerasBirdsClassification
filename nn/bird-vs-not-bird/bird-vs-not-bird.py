#!/usr/bin/env python
# coding: utf-8

# In[8]:


from comet_ml import Experiment


# In[1]:


DATA_DIR = "data"


# In[10]:


get_ipython().run_line_magic('matplotlib', 'inline')

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import random
from keras.preprocessing.image import (
    ImageDataGenerator,
    load_img,
    img_to_array,
    array_to_img,
)


# In[2]:


import keras
from keras import backend as K
from keras.layers.core import Dense, Activation
from keras.optimizers import Adam
from keras.metrics import categorical_crossentropy
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
from keras.models import Model
from keras.applications import imagenet_utils
from keras.layers import Dense, GlobalAveragePooling2D
from keras.applications import MobileNet
from keras.applications.mobilenet import preprocess_input
from keras import callbacks
from keras.callbacks import EarlyStopping
import numpy as np
from IPython.display import Image
from keras.optimizers import Adam


# # Review the images

# In[12]:


get_ipython().run_line_magic('matplotlib', 'inline')

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import random
from keras.preprocessing.image import (
    ImageDataGenerator,
    load_img,
    img_to_array,
    array_to_img,
)


# In[13]:


import os
import warnings
import glob


# In[14]:


img_list = glob.glob(os.path.join(DATA_DIR,"*/*.jpg"))
print(len(img_list))


# In[28]:


fig = plt.gcf()
fig.set_size_inches(15,10)
for i, img_path in enumerate(random.sample(img_list, 15)):
    img = image.load_img(img_path, target_size=(224, 224))
    img = image.img_to_array(img, dtype=np.uint8)

    plt.subplot(3, 5, i + 1)
    plt.imshow(img.squeeze())


# In[ ]:





# In[ ]:





# In[18]:


# experiment.display()


# In[19]:


train_generator = train_datagen.flow_from_directory(
    DATA_DIR + "/train",
    target_size=(224, 224),
    color_mode="rgb",
    batch_size=params["batch_size"],
    class_mode="categorical",
    shuffle=True,
)


# In[20]:


validation_generator = valid_datagen.flow_from_directory(
    DATA_DIR + "/valid",
    target_size=(224, 224),
    color_mode="rgb",
    batch_size=params["batch_size"],
    class_mode="categorical",
    shuffle=True,
)


# In[21]:


labels = train_generator.class_indices
labels = dict((v, k) for k, v in labels.items())


# In[23]:


model.save_weights(os.path.join(MODELS_DIR, "mobilenet.bird-vs-not-bird.overfit.h5"))


# In[22]:


model.compile(
    optimizer=params["optimizer"], loss="categorical_crossentropy", metrics=["accuracy"]
)


# In[26]:


# log parameters in Comet.ml
experiment.log_parameters(params)


# In[11]:


import keras
from keras import backend as K
from keras.layers.core import Dense, Activation
from keras.optimizers import Adam
from keras.metrics import categorical_crossentropy
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
from keras.models import Model
from keras.applications import imagenet_utils
from keras.layers import Dense, GlobalAveragePooling2D
from keras.applications import MobileNet
from keras.applications.mobilenet import preprocess_input
from keras import callbacks
from keras.callbacks import EarlyStopping
import numpy as np
from IPython.display import Image
from keras.optimizers import Adam


# In[ ]:





# In[12]:


model = get_model(params)


# In[13]:


model.summary()


# In[14]:


# experiment.display()


# In[15]:


params = {}


params["batch_size"] = 96
params["num_classes"] = 2
params["epochs"] = 100
params["optimizer"] = "adam"
params["activation"] = "relu"
params["validation_split"] = 0.2
params["lr"] = 1e-3
params["kernel_initializer"] = "he_uniform"


# In[16]:


def prepare_image(file):
    img_path = ""
    img = keras.preprocessing.image.load_img(img_path + file, target_size=(224, 224))
    img_array = keras.preprocessing.image.img_to_array(img)
    img_array_expanded_dims = np.expand_dims(img_array, axis=0)
    return keras.applications.mobilenet.preprocess_input(img_array_expanded_dims)


# In[17]:


train_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input,
    rescale=1.0 / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    width_shift_range=0.1,
    height_shift_range=0.1,
)  # included in our dependencies


# In[12]:


model = get_model(params)


# In[13]:


model.summary()


# In[17]:


train_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input,
    rescale=1.0 / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    width_shift_range=0.1,
    height_shift_range=0.1,
)  # included in our dependencies


# In[18]:


valid_datagen = ImageDataGenerator(
    rescale=1.0 / 255, preprocessing_function=preprocess_input
)


# In[19]:


train_generator = train_datagen.flow_from_directory(
    DATA_DIR + "/train",
    target_size=(224, 224),
    color_mode="rgb",
    batch_size=params["batch_size"],
    class_mode="categorical",
    shuffle=True,
)


# In[20]:


validation_generator = valid_datagen.flow_from_directory(
    DATA_DIR + "/valid",
    target_size=(224, 224),
    color_mode="rgb",
    batch_size=params["batch_size"],
    class_mode="categorical",
    shuffle=True,
)


# In[21]:


labels = train_generator.class_indices
labels = dict((v, k) for k, v in labels.items())


# In[22]:


model.compile(
    optimizer=params["optimizer"], loss="categorical_crossentropy", metrics=["accuracy"]
)


# In[18]:


# experiment.display()


# In[25]:


get_ipython().run_line_magic('matplotlib', 'inline')

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
get_ipython().run_line_magic('matplotlib', 'inline')


from keras.models import load_model
import scipy
import os


# In[18]:


# experiment.display()


# In[26]:


# log parameters in Comet.ml
experiment.log_parameters(params)


# ## Setup callbacks 

# In[27]:


MODELS_DIR = "models"


# In[29]:


model.load_weights(os.path.join(MODELS_DIR, "bird-vs-not-bird-weights-30.h5"))


# ## Train the model

# In[30]:


with experiment.train():
    step_size_train = train_generator.samples // params["batch_size"]
    history = model.fit_generator(
        generator=train_generator,
        validation_data=validation_generator,
        validation_steps=validation_generator.samples // params["batch_size"],
        steps_per_epoch=step_size_train,
        epochs=params["epochs"],
        verbose=1,
        callbacks=[log, checkpoint, lr_decay],
        use_multiprocessing=True,
        workers=7,
    )


# In[23]:


model.save_weights(os.path.join(MODELS_DIR, "mobilenet.bird-vs-not-bird.overfit.h5"))


# In[24]:


experiment.end()


# # Testing predictions

# In[25]:


get_ipython().run_line_magic('matplotlib', 'inline')

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from keras.models import load_model
import scipy
import os


# Connecting Google Drive with saved model

# In[69]:


IMAGES_DIR = "/home/gaiar/developer/birds-of-berlin/datasets/data"


# In[70]:


MODELS_DIR = "models"


# In[28]:


model = get_model(params)


# In[29]:


model.load_weights(os.path.join(MODELS_DIR, "bird-vs-not-bird-weights-30.h5"))


# In[ ]:





# In[42]:


def load_image(img_path, show=False):
    img = keras.preprocessing.image.load_img(img_path, target_size=(150, 150))
    img_tensor = keras.preprocessing.image.img_to_array(
        img
    )  # (height, width, channels)
    img_tensor = np.expand_dims(
        img_tensor, axis=0
    )  # (1, height, width, channels), add a dimension because the model expects this shape: (batch_size, height, width, channels)
    img_tensor /= 255.0  # imshow expects values in the range [0, 1]
    if show:
        plt.imshow(img_tensor[0])
        plt.axis("off")
        plt.show()
    return img_tensor


# In[31]:


labels = validation_generator.class_indices
labels


# In[32]:


import os


# In[89]:


test_batches = ImageDataGenerator(
    preprocessing_function=preprocess_input
).flow_from_directory(
    IMAGES_DIR, target_size=(224, 224), batch_size=params["batch_size"]
)


# In[91]:


import math

steps = test_batches.samples / params["batch_size"]


# In[129]:


predictions = model.predict_generator(
    test_batches,
    max_queue_size=params["batch_size"] * 2,
    verbose=1,
    workers=7,
    steps=steps,
    use_multiprocessing=True,
)


# In[149]:


images = []
i = 0
for root, dirs, files in os.walk(IMAGES_DIR):
    for filename in files:
        if i <= 199999:
            try:
                img = os.path.join(root, filename)
                new_image = prepare_image(img)
                y_prob = model.predict(new_image)
                y_classes = y_prob.argmax(axis=-1)
                if y_classes[0] == 1:
                    images.append(img)
                    i += 1
            except Exception as e:
                print("Error reading image {0} {1}".format(filename, e))
                pass
        else:
            break


# In[ ]:





# In[ ]:


plt.figure(figsize=(300, 300))
columns = 4
for i, img in enumerate(images):
    plt.subplot(len(images) / columns + 1, columns, i + 1)
    plt.imshow(mpimg.imread((img)))


# In[ ]:


from IPython.display import Image
from IPython.display import display

# x = Image(filename='1.png')
imgs = []
imgs = [Image(filename=img) for img in images]

display(*imgs)


# In[ ]:


#So first of all the test images should be placed inside a separate folder inside the test folder. So in my case I made another folder inside test folder and named it all_classes. Then ran the following code:

test_generator = test_datagen.flow_from_directory(
    directory=pred_dir,
    target_size=(28, 28),
    color_mode="rgb",
    batch_size=32,
    class_mode=None,
    shuffle=False
)

#The above code gives me an output:
#Found 306 images belonging to 1 class

#And most importantly you've to write the following code:

test_generator.reset()

#else weird outputs will come. Then using the .predict_generator() function:

pred=cnn.predict_generator(test_generator,verbose=1,steps=306/batch_size)

#Running the above code will give output in probabilities so at first I need to convert them to class number. In my case it was 4 classes, so class numbers were 0,1,2 and 3.

#Code written:

predicted_class_indices=np.argmax(pred,axis=1)

#Next step is I want the name of the classes:

labels = (train_generator.class_indices)
labels = dict((v,k) for k,v in labels.items())
predictions = [labels[k] for k in predicted_class_indices]

#Where by class numbers will be replaced by the class names. One final step if you want to save it to a csv file, arrange it in a dataframe with the image names appended with the class predicted.

filenames=test_generator.filenames
results=pd.DataFrame({"Filename":filenames,
                      "Predictions":predictions})

#Display your dataframe. Everything is done now. You get all the predicted class for your images.

