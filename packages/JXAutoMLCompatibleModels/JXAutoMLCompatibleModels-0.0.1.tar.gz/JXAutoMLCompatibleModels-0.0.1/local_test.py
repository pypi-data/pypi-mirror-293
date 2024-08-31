def smoke_test():

    try:
        print("===Begin Smoke Test===\n")

        print("===Import Modules===")
        import JXAutoMLCompatibleModels

        print("===Import Successful===")

        print("===Import StackingClassifierPro===")

        from JXAutoMLCompatibleModels.Stacking import StackingClassifier_Pro

        print("===Import StackingClassifierPro Successful===")

        print("===Import StackingRegressorPro===")

        from JXAutoMLCompatibleModels.Stacking import StackingRegressor_Pro

        print("===Import StackingRegressorPro Successful===")

        print("======\n")
        print("===SMOKETEST PASSED===")

    except Exception as e:
        print("===SMOKETEST FAILED===")
        raise e


def test_functions():

    from sklearn.datasets import make_regression, make_classification
    import pandas as pd

    # Create a regression dataset
    X_reg, y_reg = make_regression(
        n_samples=100, n_features=5, noise=0.1, random_state=42
    )
    X_reg_df = pd.DataFrame(
        X_reg, columns=[f"feature_{i+1}" for i in range(X_reg.shape[1])]
    )
    y_reg_series = pd.Series(y_reg, name="target")

    # Create a classification dataset with 2 classes
    X_class_2, y_class_2 = make_classification(
        n_samples=100,
        n_features=5,
        n_classes=2,
        n_clusters_per_class=1,
        random_state=42,
    )
    X_class_2_df = pd.DataFrame(
        X_class_2, columns=[
            f"feature_{i+1}" for i in range(X_class_2.shape[1])]
    )
    y_class_2_series = pd.Series(y_class_2, name="target")

    try:
        test_regressor(X_reg_df, y_reg_series)
        test_classifier(X_class_2_df, y_class_2_series)

        print("""FUNCTIONALITY TEST PASSED""")
    except Exception as e:
        print("""FUNCTIONALITY TEST FAILED""")
        raise e


def test_classifier(X, y):

    from JXAutoMLCompatibleModels.Stacking import StackingClassifier_Pro
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.svm import SVC
    from sklearn.metrics import accuracy_score

    print(f"===Begin Classifier test===")

    print("===Initialise Classifier===")
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

    print("===Begin fitting Classifier===")
    model.fit(X, y)
    print("===Fitting Classifier complete===")

    print("===Begin Classifier evaluation===")

    print(accuracy_score(y, model.predict(X)))
    print(f"===Evaluate Classifier test Complete===")
    print()


def test_regressor(X, y):
    from JXAutoMLCompatibleModels.Stacking import StackingRegressor_Pro
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
    from sklearn.svm import SVR
    from sklearn.metrics import r2_score

    print(f"===Begin Regressor test===")

    print("===Initialise Regressor===")
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
    print(model.final_estimator)
    print("===Initialise Regressor complete===")

    print("===Begin fitting Regressor===")
    model.fit(X, y)
    print("===Fitting Regressor complete===")

    print("===Begin Regressor evaluation===")

    print(r2_score(y, model.predict(X)))
    print(f"===Evaluate Regressor test Complete===")
    print()


def local_test():
    smoke_test()
    test_functions()


if __name__ == "__main__":

    local_test()

    print("ALL TESTS PASSED!")
