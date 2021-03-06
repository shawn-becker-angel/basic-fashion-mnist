#!/usr/bin/env python
# coding: utf-8

epochs = 2
plot_figures = True

# create and activate your virtual environment

# per https://www.tensorflow.org/install/pip#macos
# install tensorflow with pip on macos
# python3 -m pip install tensorflow
# python3 -c "import tensorflow as tf; print(tf.reduce_sum(tf.random.normal([1000, 1000])))"

# per https://scikit-learn.org/stable/install.html
# install sklearn with pip on macos
# pip install scikit-learn
# python -c "import sklearn; sklearn.show_versions()"

# pip install opencv-python


import os
os.system('cls||clear')

print("basic-fashion-mnist image classification")

print("importing tensorflow")
import tensorflow as tf
print("TensorFlow version:", tf.__version__)
print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
print("Num CPUs Available: ", len(tf.config.experimental.list_physical_devices('CPU')))

# Adapted from jupyter notebook at
# https://github.com/tensorflow/docs/blob/master/site/en/tutorials/keras/classification.ipynb
# provided in this online tutorial
# https://www.tensorflow.org/tutorials/keras/classification

#@title Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#@title MIT License
#
# Copyright (c) 2017 François Chollet
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

# <table class="tfo-notebook-buttons" align="left">
#   <td>
#     <a target="_blank" href="https://www.tensorflow.org/tutorials/k
# eras/classification"><img src="https://www.tensorflow.org/images/tf_
# logo_32px.png" />View on TensorFlow.org</a>
#   </td>
#   <td>
#     <a target="_blank" href="https://colab.research.google.com/git
# hub/tensorflow/docs/blob/master/site/en/tutorials/keras/classificat
# ion.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32
# px.png" />Run in Google Colab</a>
#   </td>
#   <td>
#     <a target="_blank" href="https://github.com/tensorflow/doc
# s/blob/master/site/en/tutorials/keras/classification.ipynb"><img
# src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" />View 
# source on GitHub</a>
#   </td>
#   <td>
#     <a href="https://storage.googleapis.com/tensorflow_docs/doc
# s/site/en/tutorials/keras/classification.ipynb"><img src="https
# ://www.tensorflow.org/images/download_logo_32px.png" />Download 
# notebook</a>
#   </td>
# </table>

# This guide trains a neural network model to classify images of 
# clothing, like sneakers and shirts. It's okay if you don't understand all the details; this is a fast-paced overview of a complete TensorFlow program with the details explained as you go.
# 
# This guide uses [tf.keras](https://www.tensorflow.org/guide/keras), 
# a high-level API to build and train models in TensorFlow.

print("Loading the packages")

from matplotlib_utils import plot_model_fit_history, show_and_wait_for_click
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import numpy as np
import matplotlib.pyplot as plt

# verify availability of GPU
tf.config.list_physical_devices()
with tf.device('/GPU'):
    a = tf.random.normal(shape=(2,), dtype=tf.float64)
    b = tf.nn.relu(a)
    print(f"a:{a}")
    print(f"b:{b}")

print("Importing the Fashion MNIST dataset")

# This guide uses the [Fashion MNIST](https://github.com/zalan
# oresearch/fashion-mnist) dataset which contains 70,000 grayscale 
# images in 10 categories. The images show individual articles 
# of clothing at low resolution (28 by 28 pixels), as seen here:
# 
# <table>
#   <tr><td>
#     <img src="https://tensorflow.org/images/fashion-mnist-sprite.png"
#          alt="Fashion MNIST sprite"  width="600">
#   </td></tr>
#   <tr><td align="center">
#     <b>Figure 1.</b> <a href="https://github.com/zalandoresea
# rch/fashion-mnist">Fashion-MNIST samples</a> (by Zalando, MIT License).<br/>&nbsp;
#   </td></tr>
# </table>
# 
# Fashion MNIST is intended as a drop-in replacement for the 
# classic [MNIST](http://yann.lecun.com/exdb/mnist/) dataset—
# often used as the "Hello, World" of machine learning programs 
# for computer vision. The MNIST dataset contains images of 
# handwritten digits (0, 1, 2, etc.) in a format identical to 
# that of the articles of clothing you'll use here.
# 
# This guide uses Fashion MNIST for variety, and because it's a 
# slightly more challenging problem than regular MNIST. Both 
# datasets are relatively small and are used to verify that an 
# algorithm works as expected. They're good starting points to 
# est and debug code.
# 
# Here, 60,000 images are used to train the network and 10,000 
# images to evaluate how accurately the network learned to classify 
# images. You can access the Fashion MNIST directly from TensorFlow. 
# Import and [load the Fashion MNIST 
# data](https://www.tensorflow.org/api_docs/python/tf/keras/datasets/
# fashion_mnist/load_data) directly from TensorFlow:

fashion_mnist = tf.keras.datasets.fashion_mnist
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

# Loading the dataset returns four NumPy arrays:
# 
# * The `train_images` and `train_labels` arrays are the *training set*—the data the model uses to learn.
# * The model is tested against the *test set*, the `test_images`, and `test_labels` arrays.
# 
# The images are 28x28 NumPy arrays, with pixel values ranging from 0 to 255. The *labels* are an array of integers, ranging from 0 to 9. These correspond 
# to the *class* of clothing the image represents:
# 
# Each image is mapped to a single label. Since the *class names* are not included with the dataset, store them here to use later when plotting the images:

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

# Let's explore the format of the dataset before training the model. The following shows there are 60,000 images in the training set, with each image represented as 28 x 28 pixels:

train_images.shape

# Likewise, there are 60,000 labels in the training set:

len(train_labels)

# Each label is an integer between 0 and 9:

train_labels

# There are 10,000 images in the test set. Again, 
# each image is represented as 28 x 28 pixels:

test_images.shape

# And the test set contains 10,000 images labels:

len(test_labels)

# ## Preprocess the data
# 
# The data must be preprocessed before training the network.
# If you inspect the first image in the training set, you will see that the pixel values fall in the range of 0 to 255:

# plt.figure()
# plt.imshow(train_images[0])
# plt.colorbar()
# plt.grid(False)
# plt.show()
# show_and_wait_for_click(plt,"inspecting image 0")


# Scale these values to a range of 0 to 1 before feeding 
# them to the neural network model. To do so, divide the values by 255. It's important that the *training set* and the *testing set* be preprocessed in the same way:

train_images = train_images / 255.0
test_images = test_images / 255.0

# To verify that the data is in the correct format and that you're ready to build and train the network, let's 
# display the first 25 images from the *training set* and display the class name below each image.

if plot_figures:
    fig = plt.figure(figsize=(10,10))
    for i in range(25):
        plt.subplot(5,5,i+1)
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        plt.imshow(train_images[i], cmap=plt.cm.binary)
        plt.xlabel(class_names[train_labels[i]])
    show_and_wait_for_click(plt,"5x5 grid of the first 25 images and their classes")


print("Building the model")
# 
# Building the neural network requires configuring the layers of the model, then compiling the model.

# ### Set up the layers
# 
# The basic building block of a neural network is the [*layer*](https://www.tensorflow.org/api_docs/python/tf/keras/layers). Layers extract representations from the data fed into them. Hopefully, these representations are meaningful for the problem at hand.
# 
# Most of deep learning consists of chaining together simple layers. Most layers, such as `tf.keras.layers.Dense`, have parameters that are learned during training.

model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10)
])

# The first layer in this network, `tf.keras.layers.Flatten`, transforms the format of the images from a two-dimensional array (of 28 by 28 pixels) to a one-dimensional array (of 28 * 28 = 784 pixels). Think of this layer as unstacking rows of pixels in the image and lining them up. This layer has no parameters to learn; it only reformats the data.
# 
# After the pixels are flattened, the network consists of a sequence of two `tf.keras.layers.Dense` layers. These are densely connected, or fully connected, neural layers. The first `Dense` layer has 128 nodes (or neurons). The second (and last) layer returns a logits array with length of 10. Each node contains a score that indicates the current image belongs to one of the 10 classes.
# 
print("Compiling the model")
# 
# Before the model is ready for training, it needs a few more settings. These are added during the model's [*compile*](https://www.tensorflow.org/api_docs/python/tf/keras/Model#compile) step:
# 
# * [*Loss function*](https://www.tensorflow.org/api_docs/python/tf/keras/losses) —This measures how accurate the model is during training. You want to minimize this function to "steer" the model in the right direction.
# * [*Optimizer*](https://www.tensorflow.org/api_docs/python/tf/keras/optimizers) —This is how the model is updated based on the data it sees and its loss function.
# * [*Metrics*](https://www.tensorflow.org/api_docs/python/tf/keras/metrics) —Used to monitor the training and testing steps. The following example uses *accuracy*, the fraction of the images that are correctly classified.

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

print("Training the model")
# 
# Training the neural network model requires the following steps:
# 
# 1. Feed the training data to the model. In this example, the training data is in the `train_images` and `train_labels` arrays.
# 2. The model learns to associate images and labels.
# 3. You ask the model to make predictions about a test set—in this example, the `test_images` array.
# 4. Verify that the predictions match the labels from the `test_labels` array.

# ### Feed the model
# 
# To start training,  call the
# `model.fit`](https://www.tensorflow.org/api_docs/python/tf/keras/Model#fit) method—so called because it "fits" the model to the training data:

history = model.fit(train_images, train_labels, epochs=epochs)

if plot_figures:
    plot_model_fit_history(
    history, 
    accuracy_metrics=['accuracy'], 
    loss_metrics=['loss'])

# As the model trains, the loss and accuracy metrics are displayed. This model reaches an accuracy of about 0.91 (or 91%) on the training data.

print("Evaluating accuracy")
# 
# Next, compare how the model performs on the test dataset:

test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)

print('\nTest accuracy:', test_acc)

# It turns out that the accuracy on the test dataset is a little less than the accuracy on the training dataset. This gap between training accuracy and test accuracy represents *overfitting*. Overfitting happens when a machine learning model performs worse on new, previously unseen inputs than it does on the training data. An overfitted model "memorizes" the noise and details in the training dataset to a point where it negatively impacts the performance of the model on the new data. For more information, see the following:
# *   [Demonstrate overfitting](https://www.tensorflow.org/tutorials/keras/overfit_and_underfit#demonstrate_overfitting)
# *   [Strategies to prevent overfitting](https://www.tensorflow.org/tutorials/keras/overfit_and_underfit#strategies_to_prevent_overfitting)

# 
# With the model trained, you can use it to make predictions about some images.
# Attach a softmax layer to convert the model's linear outputs—[logits](https://developers.google.com/machine-learning/glossary#logits)—to probabilities, which should be easier to interpret.

probability_model = tf.keras.Sequential(
  [model, tf.keras.layers.Softmax()])

predictions = probability_model.predict(test_images)


def plot_image(i, predictions_array, true_label, img):
  true_label, img = true_label[i], img[i]
  plt.grid(False)
  plt.xticks([])
  plt.yticks([])
  plt.imshow(img, cmap=plt.cm.binary)

  predicted_label = np.argmax(predictions_array)
  if predicted_label == true_label:
    color = 'blue'
  else:
    color = 'red'

  plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label],
                                100*np.max(predictions_array),
                                class_names[true_label]),
                                color=color)

def plot_value_array(i, predictions_array, true_label):
  true_label = true_label[i]
  plt.grid(False)
  plt.xticks(range(10))
  plt.yticks([])
  thisplot = plt.bar(range(10), predictions_array, color="#777777")
  plt.ylim([0, 1])
  predicted_label = np.argmax(predictions_array)

  thisplot[predicted_label].set_color('red')
  thisplot[true_label].set_color('blue')

# 
# With the model trained, you can use it to make pedictions 
# about some images.

# Let's look at the 0th image, predictions, and prediction 
# rray. Correct prediction labels are blue and incorrect 
# prediction labels are red. The number gives the percentage 
# (out of 100) for the predicted label.

if plot_figures:
    i = 0
    plt.figure(figsize=(6,3))
    plt.subplot(1,2,1)
    plot_image(i, predictions[i], test_labels, test_images)
    plt.subplot(1,2,2)
    plot_value_array(i, predictions[i],  test_labels)
    plt.tight_layout()
    show_and_wait_for_click(plt,f"image[{i}] and its predicted\nclass values: {predictions[i]}")

    i = 12
    plt.figure(figsize=(6,3))
    plt.subplot(1,2,1)
    plot_image(i, predictions[i], test_labels, test_images)
    plt.subplot(1,2,2)
    plot_value_array(i, predictions[i],  test_labels)
    plt.tight_layout()
    show_and_wait_for_click(plt, f"image[{i}] and its predicted\nclass values{predictions[i]}")


# Let's plot several images with their predictions. 
# Note that the model can be wrong even when very confident.

# Plot the first X test images, their predicted labels, 
# and the true labels. Color correct predictions in blue
# and incorrect predictions in red.
if plot_figures:
    num_rows = 5
    num_cols = 3
    num_images = num_rows*num_cols
    plt.figure(figsize=(2*2*num_cols, 2*num_rows))
    for i in range(num_images):
        plt.subplot(num_rows, 2*num_cols, 2*i+1)
        plot_image(i, predictions[i], test_labels, test_images)
        plt.subplot(num_rows, 2*num_cols, 2*i+2)
        plot_value_array(i, predictions[i], test_labels)
    plt.tight_layout()
    show_and_wait_for_click(plt,"showing the first 15 images with their predicted classes")


# print("Using he trained model to make a prediction about a single image")

# # Grab an image from the test dataset.
# img = test_images[1]

# print(img.shape)

# # `tf.keras` models are optimized to make predictions on a *batch*, 
# # or collection, of examples at once. Accordingly, even though you're 
# # using a single image, you need to add it to a list:

# # Add the image to a batch where it's the only member.
# img = (np.expand_dims(img,0))

# print(img.shape)

# # Now predict the correct label for this image:

# predictions_single = probability_model.predict(img)

# print(predictions_single)

# plot_value_array(1, predictions_single[0], test_labels)
# _ = plt.xticks(range(10), class_names, rotation=45)
# show_and_wait_for_click(plt,"prediction for image[0] with class names")


# `tf.keras.Model.predict` returns a list of lists—
# one list for each image in the batch of data. Grab 
# the predictions for our (only) image in the batch:

pred_labels = np.argmax(predictions, axis=1)
# pred_labels = [np.argmax(predictions[i]) for i in range(len(predictions))]
assert len(pred_labels) == len(test_labels)

cm = confusion_matrix(test_labels, pred_labels)

if plot_figures:
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot(cmap=plt.cm.Blues)
    show_and_wait_for_click(plt,"the confusion matrix of test vs pred labels")


print("done with tensorflow appraoch")

###########################################################################
# this section has been copied from 
# https://dataplatform.cloud.ibm.com/analytics/notebooks/v2/acd6bd85-dc27-4d09-8045-a16ac13b568e?projectid=a653439b-775c-4414-aaf1-c485df7d18a2&context=cpdaas

probability_model = tf.keras.Sequential(
  [model, tf.keras.layers.Softmax()])

test_input_data = test_images
predictions = probability_model.predict(test_input_data)


#### Review the Prediction Results

# Each row in this array contains a numeric score (ranging from 0 and 1) for each of
# the 10 classes that we trained the model on, indicating the likelihood that the 
# depicted clothing item belongs to the class. For the first image in the test data 
# set the predictions look as follows:

predictions[0]

# The higher the score, the more confident the model is that the depicted clothing 
# item belongs to the class. Calculate the maximum for each rows to determine what 
# the predicted label is:

label = test_labels
pred_label = [np.argmax(i) for i in predictions]

# Let's take a peek at the predicted label and the correct label for the first clothing 
# item in the test data set:

print('Predicted label for the first clothing item: {}'.format(pred_label[0]))
print('Correct label for the first clothing item:   {}'.format(label[0]))

# Ideally the prediction should be correct, but your results might vary. Let's tally up 
# the numbers for the entire test data.

# identify correctly and incorrectly classified clothing items

correctly_classified = []
incorrectly_classified = []
index = 0
for actual, predict in zip(label, pred_label):
    if actual == predict:
        correctly_classified.append(index)
    else:
        incorrectly_classified.append(index)
    index += 1

ccc = len(correctly_classified)
icc = len(incorrectly_classified)
print('Correctly classified clothing items  : {:5d} ({:=5.2f} %)'.format(ccc, ccc * 100 / (ccc + icc)))    
print('Incorrectly classified clothing items: {:5d} ({:=5.2f} %)'.format(icc, icc * 100 / (ccc + icc)))    

import seaborn as sns

label_map = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot'] 

conf_matrix = confusion_matrix(label, pred_label)

if plot_figures:
    # display confusion matrix as heatmap
    ax = sns.heatmap(conf_matrix, 
                cmap='Blues', 
                xticklabels=label_map, 
                yticklabels=label_map,
                annot=True,
                fmt='d')

    plt.xlabel('Predicted label') 
    plt.ylabel('Correct label') 
    print("click window close button to continue")
    plt.show()


# FIXED: "Incorrectly Classified Clothing" figure

# plot up to max_preview clothing items that were correctly identified
shape_cols = 5
shape_rows = 1
max_preview = shape_cols * shape_rows
width_px = 1500
height_px = 400
X_test = test_input_data * 255.0

fig = plt.figure(figsize=(width_px/100, height_px/100))
for index, fail_index in enumerate(incorrectly_classified[0:max_preview]):
    plt.xticks([])
    plt.yticks([])
    ax = plt.subplot(shape_rows, shape_cols, index + 1)
    plt.imshow(np.reshape(X_test[fail_index], (28,28)), cmap=plt.cm.binary)
    plt.title('Pred: {}, Actual: {}'.format(label_map[pred_label[fail_index]], label_map[label[fail_index]]), fontsize = 10)
    # ax.set_title("Plot Title") same as plt.title 
fig.canvas.manager.set_window_title('Incorrectly Classified Clothing') 

print("click window close button to continue")
plt.show()

    
# num_cols = 5
# num_rows = 1
# num_images = num_rows*num_cols
# fig = plt.figure(figsize=(2*num_cols, 2*num_rows)) # cols*100 x rows*100
# for index, fail_index in enumerate(incorrectly_classified[0:max_preview]):
#     plt.xticks([])
#     plt.yticks([])
#     plt.subplot(index+1, 1, index+1)
#     plt.imshow(np.reshape(X_test[fail_index], (28,28)), cmap=plt.cm.binary)
#     plt.title('Pred: {}, Actual: {}'.format(
#         label_map[pred_label[fail_index]],
#         label_map[label[fail_index]]), fontsize = 10)
# plt.tight_layout()
# print("click window close button to continue")
# plt.show()

from sklearn.metrics import precision_score

# Calculate precision scores
precision_scores = precision_score(label, pred_label, average=None)

y_pos = np.arange(len(precision_scores))

fig = plt.figure(figsize=(5,5))
plt.bar(y_pos, precision_scores, align='center', alpha=0.5)
plt.xticks(y_pos, label_map, rotation=90)
plt.ylabel('Precision ( --> better)')
plt.title('Precision scores per class')

print("click window close button to continue")
plt.show()

from sklearn.metrics import recall_score

# Calculate recall score for each class
recall_scores = recall_score(label, pred_label, average=None)

# Visualize recall scores

y_pos = np.arange(len(recall_scores))

fig = plt.figure(figsize=(5,5))
plt.bar(y_pos, recall_scores, align='center', alpha=0.5)
plt.xticks(y_pos, label_map, rotation=90)
plt.ylabel('Recall ( --> better)')
plt.title('Recall scores per class')

print("click window close button to continue")
plt.show()

print("done with ibm approach")




