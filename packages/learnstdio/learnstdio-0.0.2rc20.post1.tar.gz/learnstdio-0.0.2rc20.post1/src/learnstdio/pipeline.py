#   ---------------------------------------------------------------------------------
#   Copyright (c) Learnstdio. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
"""This is Pipeline module."""


from __future__ import annotations
import json
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LinearRegression

def read_parameters(path: str) -> dict:
    """This is to read parameters from a file."""
    if not path:
        raise ValueError('Path not provided')
    if not path.endswith('.json'):
        raise ValueError('File format not supported')
    with open(path, 'r') as file:
        data = json.load(file)
    return data

def load_model(model: dict) -> LoadableModel:
    """This is to load a model from parameters."""
    # Read model parameters information
    parameters = model['parameters']
    if not parameters:
        raise ValueError('Model parameters not found')
    # Create a model object
    new_model = None
    if 'K-Nearest Neighbors' in model['name']:
        new_model = LoadableKNN(parameters)
    elif 'Multivariate Linear Regression' in model['name']:
        new_model = LoadableMultivariableLinearRegression(parameters)
    else:
        raise ValueError('Model not supported')
    #
    return new_model

def load_pipeline(path: str) -> LoadableModel:
    """This is to load a pipeline from a file."""
    # Read file
    data = read_parameters(path)
    # Read model information
    model = data['model']
    if not model:
        raise ValueError('Model not found')
    # Read model parameters information
    new_model = load_model(model)
    #
    return new_model

class LoadableModel:
    """Loadable model from parameters."""

    def __init__(self):
        """Initialize the model."""
        self.model = None

    def predict(self, *args):
        """Predict the output from the model."""
        # Convert args to a 2D array
        input_features = np.array(args).reshape(1, -1)
        # Make prediction
        prediction = self.model.predict(input_features)
        # Return the first (and only) prediction
        return prediction.item() if prediction.size == 1 else prediction

class LoadableKNN(LoadableModel):
    """Loadable KNN model from parameters."""

    def __init__(self, parameters):
        """Initialize the model."""
        super().__init__()
        self.model = KNeighborsClassifier(
            n_neighbors=parameters['n_neighbors'],
        )
        self.model.fit(
            parameters['X'],
            parameters['y'],
        )


class LoadableMultivariableLinearRegression(LoadableModel):
    """Loadable Linear Regression model from parameters."""

    def __init__(self, parameters):
        """Initialize the model."""
        super().__init__()
        self.model = LinearRegression()
        self.model.coef_ = np.array(parameters['weights'][:-1]).reshape(1, -1)
        self.model.intercept_ = np.array(parameters['weights'][-1])
