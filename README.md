# Basic classification: Classify images of clothing 

The python code in this repo was adapted from jupyter notebook at:
https://github.com/tensorflow/docs/blob/master/site/en/tutorials/keras/classification.ipynb

and described in this online tutorial:
https://www.tensorflow.org/tutorials/keras/classification

This guide trains a neural network model to classify images of clothing, like sneakers and shirts. It's okay if you don't understand all the details; this is a fast-paced overview of a complete TensorFlow program with the details explained as you go.

### Packages and utilities  
This guide uses `tf.keras`, a high-level API to build and train models in `TensorFlow`. The `matplotlib` package is used to display images and graphs, and the `nbconvert` utility is used to help convert the `jupyter notebook` into a python script.

### Python `sklearn` package not working in Jupyter
Note that the original jupyter notebook file,   `classification.ipynb` is included in this repo, but it is not used because it fails to recognize the required `sklearn` module when running from `jupyter notebook`. 

After much effort, this problem persists even when `sklearn` and `skikit-learn` packages have been installed into the active virtual environment and they have been included the `PATH` and `PYTHONPATH` env vars.


### ACTIVATING APPLE's M1 onboard GPU chip  
Follow the detailed instructions here:
[https://developer.apple.com/metal/tensorflow-plugin](https://developer.apple.com/metal/tensorflow-plugin)

This installation updates the `base` conda environment, which is by default activated on each shell startup.

If you'd prefer that conda's base environment not be activated on shell startup, set the `auto_activate_base` parameter to `false`:

	conda config --set auto_activate_base false

To verify that tensorflow has been installed, open a python shell and run the following:

	print("importing tensorflow")  
	import tensorflow as tf  
	print("TensorFlow version:", tf.__version__)  

To verify that the GPU is now available run the following in the python shell:

	print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
	print("Num CPUs Available: ", len(tf.config.experimental.list_physical_devices('CPU')))

If everything has been installed properly, you should see: 

	Num GUPs Available: 1
	Num CPUs Available: 1


