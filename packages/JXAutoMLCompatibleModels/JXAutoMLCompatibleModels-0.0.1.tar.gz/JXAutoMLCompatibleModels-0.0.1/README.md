# JXAutoMLCompatibleModels

```
Author GitHub: https://github.com/TGChenZP
```

*Please cite when using this package for research and other machine learning purposes*

# Introduction
This package wraps various model classes in an Sklearn style API, enabling its compatability with JXAutoML tuners.

# Installation
```bash
pip install JXAutoMLCompatibleModels
```

# Models
## JXAutoMLCompatibleModels.Stacking.StackingClassifier_Pro [[source]]()
```python
class JXAutoMLCompatibleModels.Stacking.StackingClassifier_Pro(estimators_list, num_estimators, cv, n_jobs, passthrough, stack_method, verbose, final_estimator, **kwargs)
```

### Parameters
| **Parameter & Type**                              | **Description**                                                                                                                                                        |
|---------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `estimators` (`list of (str, estimator)`)         | Base estimators to be stacked together. Each element is a tuple consisting of a string (name) and an estimator instance. An estimator can be set to ‘drop’ using `set_params`. Typically, these are classifiers, though regressors can be used for specific cases (e.g., ordinal regression).                                          |
| `final_estimator` (`estimator`, default=`None`)   | Classifier used to combine the base estimators. Defaults to `LogisticRegression`.                                                                                       |
| `cv` (`int`, `cross-validation generator`, `iterable`, or “prefit”, default=`None`) | Determines the cross-validation splitting strategy used in `cross_val_predict` to train `final_estimator`. Possible values include: <br>- `None`: Default 5-fold cross-validation. <br>- `int`: Specifies the number of folds in a (Stratified) KFold. <br>- `cross-validation generator`: Object used as a cross-validation generator. <br>- `iterable`: Yields train, test splits. <br>- `prefit`: Assumes the estimators are prefit, and they will not be refitted. <br><br>For integer/None inputs, `StratifiedKFold` is used for binary or multiclass classifiers; otherwise, `KFold` is used. Note that these splitters are instantiated with `shuffle=False` to ensure the same splits across calls. The ‘prefit’ option was added in version 1.1, assuming that all estimators are pre-fitted. The `final_estimator_` is trained on the full training set predictions rather than cross-validated predictions, which risks overfitting if models are trained on the same data.| 
| `stack_method` (`{‘auto’, ‘predict_proba’, ‘decision_function’, ‘predict’}`, default=`auto`) | Method called for each base estimator. Options include: <br>- `auto`: Invokes, in order, `predict_proba`, `decision_function`, or `predict`. <br>- `predict_proba`, `decision_function`, or `predict`: Specific method to be called. An error is raised if the method is not implemented by the estimator. |
| `n_jobs` (`int`, default=`None`)                  | The number of jobs to run in parallel during the fit of all estimators. `None` means 1, unless in a `joblib.parallel_backend` context. `-1` means using all processors. |
| `passthrough` (`bool`, default=`False`)           | When `False`, only the predictions of estimators will be used as training data for `final_estimator`. When `True`, the `final_estimator` is trained on the predictions as well as the original training data. |
| `verbose` (`int`, default=`0`)                    | Verbosity level.                                                                                                                                                       |
| `**kwargs`                                        | Parameters of `final_estimator` can be defined through `**kwargs` and will be picked up during the call, allowing further customization of the `final_estimator`.       |


## ## JXAutoMLCompatibleModels.Stacking.StackingRegressor_Pro [[source]]()
```python
class JXAutoMLCompatibleModels.Stacking.StackingRegressor_Pro(estimators_list, num_estimators, cv, n_jobs, passthrough, verbose, final_estimator, **kwargs)
```

### Parameters
| **Parameter & Type**                              | **Description**                                                                                                                                                        |
|---------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `estimators` (`list of (str, estimator)`)         | Base estimators to be stacked together. Each element is a tuple consisting of a string (name) and an estimator instance. An estimator can be set to ‘drop’ using `set_params`.                                          |
| `final_estimator` (`estimator`, default=`None`)   | Regressor used to combine the base estimators. Defaults to `RidgeCV`.                                                                                                   |
| `cv` (`int`, `cross-validation generator`, `iterable`, or “prefit”, default=`None`) | Determines the cross-validation splitting strategy used in `cross_val_predict` to train `final_estimator`. Possible values include: <br>- `None`: Default 5-fold cross-validation. <br>- `int`: Specifies the number of folds in a (Stratified) KFold. <br>- `cross-validation generator`: Object used as a cross-validation generator. <br>- `iterable`: Yields train, test splits. <br>- `prefit`: Assumes the estimators are prefit, and they will not be refitted. <br><br>For integer/None inputs, `StratifiedKFold` is used for binary or multiclass classifiers; otherwise, `KFold` is used. Note that these splitters are instantiated with `shuffle=False` to ensure the same splits across calls. The ‘prefit’ option was added in version 1.1, assuming that all estimators are pre-fitted. The `final_estimator_` is trained on the full training set predictions rather than cross-validated predictions, which risks overfitting if models are trained on the same data.| 
| `n_jobs` (`int`, default=`None`)                  | The number of jobs to run in parallel during the fit of all estimators. `None` means 1, unless in a `joblib.parallel_backend` context. `-1` means using all processors. |
| `passthrough` (`bool`, default=`False`)           | When `False`, only the predictions of estimators will be used as training data for `final_estimator`. When `True`, the `final_estimator` is trained on the predictions as well as the original training data. |
| `verbose` (`int`, default=`0`)                    | Verbosity level.                                                                                                                                                       |
| `**kwargs`                                        | Parameters of `final_estimator` can be defined through `**kwargs` and will be picked up during the call, allowing further customization of the `final_estimator`.       |

# *Usage Examples*
## *StackingRegressor_Pro*
```python
from JXAutoMLCompatibleModels.Stacking import StackingRegressor_Pro
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.metrics import r2_score


X_reg, y_reg = make_regression(
        n_samples=100, n_features=5, noise=0.1, random_state=42)
X = pd.DataFrame(
    X_reg, columns=[f'feature_{i+1}' for i in range(X_reg.shape[1])])
y = pd.Series(y_reg, name='target')

model = StackingRegressor_Pro(
        estimators_list=[('gbr', GradientBoostingRegressor()), ('svr', SVR())],
        num_estimators=2,
        final_estimator_class=RandomForestRegressor,
        verbose=False,
        passthrough=True,
        n_jobs=-1,
        cv=3,
        n_estimators=50,
    )

model.fit(X, y)

print(r2_score(y, model.predict(X)))
```

## *StackingClassifier_Pro*
```python
from JXAutoMLCompatibleModels.Stacking import StackingClassifier_Pro
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

X_reg, y_reg = make_regression(
        n_samples=100, n_features=5, noise=0.1, random_state=42)
X = pd.DataFrame(
    X_reg, columns=[f'feature_{i+1}' for i in range(X_reg.shape[1])])
y = pd.Series(y_reg, name='target')

model = StackingClassifier_Pro(
        estimators_list=[
            ('gbr', GradientBoostingClassifier()), ('svc', SVC())],
        num_estimators=2,
        final_estimator_class=RandomForestClassifier,
        verbose=False,
        passthrough=True,
        stack_method='auto',
        n_jobs=-1,
        cv=3,
        n_estimators=50,
    )
    print("===Initialise Classifier complete===")

model.fit(X, y)

print(r2_score(y, model.predict(X)))
```