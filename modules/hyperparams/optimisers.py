import concurrent
import warnings

import optuna
from optuna.samplers import TPESampler
from sklearn.exceptions import ConvergenceWarning

from modules.config import hyperparameter_rounds
from modules.hyperparams.objectives import objective, objective_xgb, objective_rf, objective_stacking, \
    objective_reg_stacking
from modules.hyperparams.save_and_load import load_hyperparameters, save_hyperparameters
from modules.utilities import logging, run_with_timeout


def create_study(name, objective):
    """
    Create or load an Optuna study.

    Args:
        name (str): The name of the study.
        objective (callable): The objective function for optimization.

    Returns:
        tuple: A tuple containing the study object and the objective function.
    """
    saved_params = load_hyperparameters(name)
    if saved_params is None:
        return optuna.create_study(direction='minimize', sampler=TPESampler()), objective
    return None, None


def optimize_model(name, objective, X_train_groups, y_train_groups, X_train_padded, y_train_padded, base_models,
                   timeout):
    """
    Optimize hyperparameters for a specific model using Optuna.

    Args:
        name (str): The name of the model.
        objective (callable): The objective function for optimization.
        X_train_groups (list): List of training data groups.
        y_train_groups (list): List of training target groups.
        X_train_padded (array-like): Padded training data.
        y_train_padded (array-like): Padded training target values.
        base_models (list): List of base models for stacking.
        timeout (int): Timeout for optimization in seconds.

    Returns:
        tuple: The model name and the best hyperparameters.
    """
    study, func = create_study(name, objective)
    if study is not None and func is not None:
        try:
            def optimize_with_timeout():
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore", category=ConvergenceWarning)
                    study.optimize(func, n_trials=hyperparameter_rounds, timeout=timeout, n_jobs=-1,
                                   show_progress_bar=True)

            run_with_timeout(optimize_with_timeout, timeout_duration=timeout)
            return name, study.best_params
        except TimeoutError:
            logging.error(f"Optimization for {name} timed out")
            return name, None
        except Exception as exc:
            logging.error(f'{name} generated an exception: {exc}')
            return name, None
    else:
        return name, load_hyperparameters(name)


def optimize_hyperparameters(X_train_groups, y_train_groups, X_train_padded, y_train_padded, base_models, timeout=3600):
    """
    Optimize hyperparameters for multiple models in parallel.

    Args:
        X_train_groups (list): List of training data groups.
        y_train_groups (list): List of training target groups.
        X_train_padded (array-like): Padded training data.
        y_train_padded (array-like): Padded training target values.
        base_models (list): List of base models for stacking.
        timeout (int): Timeout for optimization in seconds.

    Returns:
        dict: Best hyperparameters for each model.
    """
    models_to_optimize = [
        ('xgb', lambda trial: objective_xgb(trial, X_train_groups, y_train_groups)),
        ('rf', lambda trial: objective_rf(trial, X_train_groups, y_train_groups)),
        ('stacking', lambda trial: objective_stacking(trial, X_train_padded, y_train_padded, base_models)),
        ('reg_stacking', lambda trial: objective_reg_stacking(trial, X_train_padded, y_train_padded, base_models))
    ]

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(
            lambda x: optimize_model(*x, X_train_groups, y_train_groups, X_train_padded, y_train_padded, base_models,
                                     timeout), models_to_optimize))

    params = {}
    for name, best_params in results:
        if best_params is not None and isinstance(best_params, dict):
            params[name] = best_params
            save_hyperparameters(best_params, name)
        else:
            params[name] = load_hyperparameters(name)

        # Ensure params[name] is a dictionary
        if not isinstance(params[name], dict):
            raise ValueError(f"Invalid parameters for {name}.")

    # Ensure all parameters are loaded
    for name in ['xgb', 'rf', 'stacking', 'reg_stacking']:
        if name not in params or params[name] is None:
            params[name] = load_hyperparameters(name)
        if params[name] is None:
            logging.warning(f"No parameters found for {name}. Using default parameters.")
            params[name] = {}
    xgb = params['xgb']
    rf = params['rf']
    stacking = params['stacking']
    reg_stacking = params['reg_stacking']
    return xgb, rf, stacking, reg_stacking


def optimize_hyperparameters_base(X_train, y_train, X_val, y_val, timeout=3600):
    """
    Optimize hyperparameters for the base LSTM model using Optuna.

    Args:
        X_train (array-like): Training data.
        y_train (array-like): Training target values.
        X_val (array-like): Validation data.
        y_val (array-like): Validation target values.
        timeout (int): Timeout for optimization in seconds.

    Returns:
        dict: Best hyperparameters.
    """
    logging.info("Starting hyperparameter optimization")

    study = optuna.create_study(direction='minimize', sampler=TPESampler())

    try:
        study.optimize(lambda trial: objective(trial, X_train, y_train, X_val, y_val),
                       n_trials=hyperparameter_rounds,
                       timeout=timeout,
                       n_jobs=-1,
                       show_progress_bar=True)
    except KeyboardInterrupt:
        logging.info("Optimization interrupted by user.")

    logging.info(f"Best trial: {study.best_trial.number}")
    logging.info(f"Best value: {study.best_value}")
    logging.info(f"Best hyperparameters: {study.best_params}")

    return study.best_params