import optuna
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import make_scorer, accuracy_score

def objective(trial, X_train, y_train):
    model_name = trial.suggest_categorical('model_name', [
        'RandomForestClassifier',
        'GradientBoostingClassifier',
        'SVC',
        'LogisticRegression',
        'KNeighborsClassifier',
        'DecisionTreeClassifier'
    ])

    if model_name == 'RandomForestClassifier':
        n_estimators = trial.suggest_int('n_estimators', 10, 200)
        max_depth = trial.suggest_int('max_depth', 2, 32)
        model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth)

    elif model_name == 'GradientBoostingClassifier':
        n_estimators = trial.suggest_int('n_estimators', 10, 200)
        learning_rate = trial.suggest_loguniform('learning_rate', 0.01, 0.3)
        model = GradientBoostingClassifier(n_estimators=n_estimators, learning_rate=learning_rate)

    elif model_name == 'SVC':
        C = trial.suggest_loguniform('C', 1e-10, 1e10)
        kernel = trial.suggest_categorical('kernel', ['linear', 'poly', 'rbf', 'sigmoid'])
        model = SVC(C=C, kernel=kernel)

    elif model_name == 'LogisticRegression':
        C = trial.suggest_loguniform('C', 1e-10, 1e10)
        solver = trial.suggest_categorical('solver', ['newton-cg', 'lbfgs', 'liblinear'])
        model = LogisticRegression(C=C, solver=solver)

    elif model_name == 'KNeighborsClassifier':
        n_neighbors = trial.suggest_int('n_neighbors', 2, 40)
        model = KNeighborsClassifier(n_neighbors=n_neighbors)

    elif model_name == 'DecisionTreeClassifier':
        max_depth = trial.suggest_int('max_depth', 2, 32)
        criterion = trial.suggest_categorical('criterion', ['gini', 'entropy'])
        model = DecisionTreeClassifier(max_depth=max_depth, criterion=criterion)

    score = cross_val_score(model, X_train, y_train, n_jobs=-1, cv=3)
    accuracy = score.mean()
    return accuracy

def optimize_hyperparameters(X_train, y_train, n_trials=50):
    study = optuna.create_study(direction='maximize')
    study.optimize(lambda trial: objective(trial, X_train, y_train), n_trials=n_trials)
    
    print("Best model:", study.best_trial.params)
    return study.best_trial.params
