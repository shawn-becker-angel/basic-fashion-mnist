# pip install matplotlib
# pip install opencv-python

import cv2
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from typing import List
import random
import sys

from numpy.random import default_rng

def show_and_wait_for_click(plt, msg=None):
    print()
    if msg is not None:
        print(msg)
    print("click the window's close button to continue")
    sys.stdout.flush()

    # blocks until close button is clicked
    plt.show()
    plt.close()

def plot_grid_of_NxN_labeled_images(N, X_data, y_data):
    assert len(X_data) == len(y_data)
    assert N*N <= len(X_data)
    shape_rows = N
    shape_cols = N
    width_px = shape_cols * 200
    height_px = shape_rows * 200
    plt.figure(figsize=(width_px/100,height_px/100))
    for i in range(N*N): # i'th frame
        plt.subplot(shape_rows,shape_cols, i+1)
        plt.xticks([])
        plt.yticks([])
        plt.imshow(np.array(X_data.iloc[i, :]).reshape(28,28), cmap=plt.cm.binary)
        plt.xlabel(y_data.iloc[i])
    

# def get_unique_random_ints(minVal: int, maxVal: int, N: int):
#     R = maxVal-minVal
#     if N > R:
#         raise Exception("not possible to create N unique integers over range of {R} integers")
#     rint = list(range(minVal,maxVal))
#     np.random.shuffle(rint)
#     return rint

# def generate_random_plot_idx(generator):
#     N = generator.n
#     if N < 1:
#         msg = "ERROR: generator.n is not > zero"
#         raise Exception(msg)
    
#     rints = get_unique_random_ints(0, N, N)
#     if len(rints) != N:
#         msg = f"ERROR: rints:{len(rints)} != N:{N}"
#         raise Exception(msg)
    
#     return rints

def plot_idxed_image_files_with_labels(name, image_files, labels, plot_idx):
    assert len(image_files) == len(labels) == len(plot_idx), "ERROR: length failures"
    N = min(len(image_files),12) # number of images
    fig = plt.figure(figsize=(12,8))
    for n in range(N):
        i = plot_idx[n]
        plt.subplot(3,4,n+1)
        image = cv2.imread(image_files[i])
        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        plt.imshow(image)   
        plt.axis('off')
        title = f"{name}[{i}]: {labels[i]}" if name is not None else labels[i]
        plt.title(title)
    plt.tight_layout()
    name_cnt =  f"{N} {name}" if name is not None else f"{N}"
    show_and_wait_for_click(plt, "{name_cnt} images and labels")

def plot_idxed_generator_images(name, generator, plot_idx, idx_to_label_map=None):
    assert len(plot_idx) > 0, "ERROR: empty plot_idx"
    if idx_to_label_map is not None:
        X, y = generator.next()
    else:
        X = generator.next()
        y = None

    fig = plt.figure(figsize=(12,8))
    
    # trim plot_idx to not exceed the new N
    N = min(len(X),12) # number of images
    plot_idx = [plot_idx[n] for n in plot_idx if plot_idx[n] < N] 
    
    for n in range(N):
        i = plot_idx[n]
        plt.subplot(3,4,n+1)
        plt.imshow(X[i,:,:,:])   
        plt.axis('off')
        label = "unknown" if y is None else idx_to_label_map[y[i]]
        plt.title(f"{name}[{i}]: {label}")
    plt.tight_layout()
    legend = "images only" if y is None else "images and labels"        
    show_and_wait_for_click(plt, f"Showing {N} {name} {legend}")

def plot_histogram(title: str='Title', data: List[float]=[], with_normal: bool=True):
    import matplotlib.pyplot as plt

    plt.hist(data, 50, density=True)
    plt.ylabel('Probability')
    plt.xlabel('Data');

    if with_normal:
        from scipy.stats import norm
        mu, std = norm.fit(data) 
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = norm.pdf(x, mu, std)
        plt.plot(x, p, 'k', linewidth=2)
        title = f"{title} mu:{mu:.2f} std:{std:.2f}"
    plt.tight_layout()
    plt.title(title)
    show_and_wait_for_click(plt, "Histogram with normal pdf")

def plot_model_fit_history(
    history, 
    accuracy_metrics=['accuracy', 'val_accuracy'], 
    loss_metrics=['loss', 'val_loss']):
    # see https://machinelearningmastery.com/display-deep-learning-model-training-history-in-keras/
        
    # list all metrics in history

    for metric in [*accuracy_metrics, *loss_metrics]:
        if metric not in history.history.keys(): 
            print(f"ERROR: matric:{metric} not found in keys")
            return
        
        if len(history.history[metric]) < 2:
            print("ERROR: pmatric:{metric} has < 2 epochs")
            return
    
    # plot accuracy metrics per epoch 
    for accuracy_metric in accuracy_metrics:
        plt.plot(history.history[accuracy_metric])
        # plt.plot(history.history["val_" + accuracy_metric])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.tight_layout()
    show_and_wait_for_click(plt, "accuracy metrics per epoch")
    
    # plot loss metrics per epoch
    for loss_metric in loss_metrics:
        plt.plot(history.history[loss_metric])
        # plt.plot(history.history["val_" + loss_metric])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.tight_layout()
    show_and_wait_for_click(plt, "loss metrics per epoch")


#==============================================
# TESTS
#==============================================

def test_plot_gamma_histogram():
    shape = 1.5
    N = 100_000
    s = np.random.standard_gamma(shape, N)
    assert len(s) == N
    plot_histogram(title="gamma distribution", data=s )

def test_plot_rand_int_histogram():
    s = []
    minVal = 0
    maxVal = 100
    N = 100_000
    for i in range(N):
        s.append(np.random.randint(minVal,maxVal))
    assert len(s) == N
    assert np.min(s) >= minVal
    maxS = np.max(s)
    if not maxS < maxVal:
        print(f"ERROR: maxS:{maxS} not < maxVal:{maxVal}")
    plot_histogram(title="randint distribution", data=s )

#==============================================
# MAIN
#==============================================

if __name__ == "__main__":
    test_plot_gamma_histogram()
    test_plot_rand_int_histogram()
    print("done")