""" Analyze

This file contains functions related to the analasyis of play-
by-play data from basketball-reference.com, including a shot
probability predictor,  


This file requires that `pandas` and 'bs4' be installed within the 
Python environment you are running this script in.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import util
import sys


def predict_proba(model, features):
	""" Uses the logistic regression model to predict the 
	probability that a shot is made given the features
	
	Parameters
	----------
	pid : str
		The player ID assigned by basketball-reference.com

	yid : str (optional)
		The year ID for a specific season
		Example: yid for 2019/20 season is '2020'
	
	features: list
		List of feature names (str) from the schema to include
		in the regression model.

	Returns
	-------
	float
		A number in range [0, 1] that represents the percentage
		chance that the shot is made
	"""

def build_model(data):
	dmatrix = design_matrix()


def design_matrix(pid, yid='', features):




def evaluate(model, x_test, y_test):
	""" Prints model evaluation statistics

	Parameters
    ----------
    y_test : list
        A list of integers representing the
        actual labels for the test_data

	y_pred : list
		A list of integers representing the
		predicted labels for the test_data
    """

    # Build y_pred from x_test
    

	# Calculate accuracy, precision, recall
	tp = sum([1 for pred, test in zip(y_pred, y_test) if 1 == pred == test])
	fp = sum([1 for pred, test in zip(y_pred, y_test) if 1 == pred != test])
	tn = sum([1 for pred, test in zip(y_pred, y_test) if 0 == pred == test])
	fn = sum([1 for pred, test in zip(y_pred, y_test) if 0 == pred != test])

	accuracy = float((tp + tn)) / (tp + fp + tn + fn)
	precision = float(tp + fp) and float(tp) / (tp + fp)
	recall = float((tp + fn) and float(tp) / (tp + fn))

	# Weird print formatting stuff
	print('True Positives | False Positives | True Negatives | False Negatives')
	print(str(tp)+' '*(14-len(str(tp)))+' | '+str(fp)+' '*(15-len(str(fp)))+' | '+str(tn)+' '*(14-len(str(tn)))+' | '+str(fn)+'\n')

	print('Accuracy: ' + str(accuracy))
	print('Precision: ' + str(precision))
	print('Recall: ' + str(recall) + '\n')


