# vinayaga/__init__.py

import pandas as pd
import numpy as np

def load_data(filepath):
    """Load data from a CSV file."""
    data = pd.read_csv(filepath)
    attributes = np.array(data)[:, :-1]
    target = np.array(data)[:, -1]
    return attributes, target

def train(c, t):
    """Train the model to find the specific hypothesis."""
    specific_hypothesis = None

    for i, val in enumerate(t):
        if val == "Yes":
            specific_hypothesis = c[i].copy()
            break

    for i, val in enumerate(c):
        if t[i] == "Yes":
            for x in range(len(specific_hypothesis)):
                if val[x] != specific_hypothesis[x]:
                    specific_hypothesis[x] = '?'
    
    return specific_hypothesis
