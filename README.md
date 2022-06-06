# Basic classification: Classify images of clothing 

The python code in this repo was adapted from jupyter notebook at:
https://github.com/tensorflow/docs/blob/master/site/en/tutorials/keras/classification.ipynb

and described in this online tutorial:
https://www.tensorflow.org/tutorials/keras/classification

This guide trains a neural network model to classify images of clothing, like sneakers and shirts. It's okay if you don't understand all the details; this is a fast-paced overview of a complete TensorFlow program with the details explained as you go.

### Packages and utilities  
This guide uses `tf.keras`, a high-level API to build and train models in `TensorFlow`. The `matplotlib` package is used to display images and graphs, and the `nbconvert` utility is used to help convert the `jupyter notebook` into a python script.

### sklearn not working in Jupyter
Note that the original jupyter notebook file,   `classification.ipynb` is included in this repo, but it is not used because it fails to recognize the required `sklearn` module when running from `jupyter notebook`. 

After much effort, this problem persists even when `sklearn` and `skikit-learn` packages have been installed into the active virtual environment and they have been included the `PATH` and `PYTHONPATH` env vars.