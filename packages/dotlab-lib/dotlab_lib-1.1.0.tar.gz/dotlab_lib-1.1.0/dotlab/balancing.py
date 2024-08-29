import pandas as pd
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler

def hybrid_sampling(X_train, y_train, hybrid_size:int=2, seed:int=42):
    '''
    Apply hybrid sampling technique combining SMOTE oversampling and random undersampling.

    Parameters
    ----------
    X_train : pandas.DataFrame or numpy.ndarray
      Training feature data.
    y_train : pandas.Series or numpy.ndarray
      Training target data.
    hybrid_size : int, optional
      Multiplication factor to determine the desired number of minority class examples after SMOTE oversampling. 
      Default is 2.
    seed : int, optional
      Random seed for reproducibility. Default is 42.

    Returns
    -------
    X_train_resampled : pandas.DataFrame or numpy.ndarray
      Resampled training feature data.
    y_train_resampled : pandas.Series or numpy.ndarray
      Resampled training target data.

    Description
    -----------
    The function performs a hybrid sampling technique to balance the class distribution in the training data by:
    1. Calculating the number of minority class examples in the original training data.
    2. Using SMOTE (Synthetic Minority Over-sampling Technique) to oversample the minority class to a specified size.
    3. Applying random undersampling to the majority class to further balance the class distribution.

    The desired number of minority class examples after oversampling is determined by multiplying the original number
    of minority class examples by `hybrid_size`, ensuring it does not exceed the total number of examples available 
    minus the number of majority class examples. The function then combines the oversampled minority class with the
    randomly undersampled majority class to create a balanced dataset.

    Notes
    -----
    - The `SMOTE` class is used for oversampling, and the `RandomUnderSampler` class is used for undersampling.
    - Both oversampling and undersampling steps use the provided random seed for reproducibility.
    - The function returns the resampled feature and target data, which can be used for training machine learning models.
    '''
    # Contando a quantidade de exemplos na classe minoritária
    minority_class_count = sum(y_train == 1)
    
    # Calculando a quantidade desejada após o oversampling
    desired_minority_count = min(int(hybrid_size * minority_class_count), len(y_train) - minority_class_count)
    
    # Aplicando oversampling na classe minoritária usando SMOTE com a quantidade desejada
    smote = SMOTE(sampling_strategy={1: desired_minority_count}, random_state=seed)
    X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)
    
    # Aplicando undersampling na classe majoritária
    rus = RandomUnderSampler(random_state=seed)
    X_train_resampled, y_train_resampled = rus.fit_resample(X_train_resampled, y_train_resampled)
    
    return X_train_resampled, y_train_resampled   