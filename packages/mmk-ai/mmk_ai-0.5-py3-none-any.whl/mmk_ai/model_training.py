from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
import optuna
import joblib

def train_model_threaded(X_train, X_test, y_train, y_test, model_name):
    """
    Verilen modeli eğitir ve test seti üzerindeki başarı puanını döndürür.
    
    :param X_train: DataFrame, eğitim verisinin özellikleri
    :param X_test: DataFrame, test verisinin özellikleri
    :param y_train: Series, eğitim verisinin hedef değişkeni
    :param y_test: Series, eğitim verisinin hedef değişkeni
    :param model_name: str, eğitilecek modelin adı
    :return: model, score
    """
    models = {
        "RandomForestClassifier": RandomForestClassifier(),
        "GradientBoostingClassifier": GradientBoostingClassifier(),
        "SVC": SVC(probability=True),
        "LogisticRegression": LogisticRegression(),
        "KNeighborsClassifier": KNeighborsClassifier(),
        "DecisionTreeClassifier": DecisionTreeClassifier()
    }

    model = models.get(model_name)
    if model:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        if model_name.endswith('Classifier'):
            score = accuracy_score(y_test, y_pred)
        else:
            score = model.score(X_test, y_test)
        
        return model, score
    else:
        raise ValueError(f"Model {model_name} is not supported.")

def save_model(model, file_path):
    """
    Modeli verilen dosya yoluna kaydeder.

    :param model: Eğitimli model
    :param file_path: str, modeli kaydetmek için dosya yolu
    """
    joblib.dump(model, file_path)

def load_model(file_path):
    """
    Verilen dosya yolundan modeli yükler.

    :param file_path: str, model dosya yolu
    :return: Yüklü model
    """
    return joblib.load(file_path)

def objective(trial, X_train, y_train):
    """
    Optuna kullanarak modelin hiperparametrelerini optimize etmek için hedef fonksiyon.

    :param trial: Optuna trial objesi
    :param X_train: DataFrame, eğitim verisinin özellikleri
    :param y_train: Series, eğitim verisinin hedef değişkeni
    :return: accuracy, doğruluk puanı
    """
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
    """
    Optuna ile model hiperparametrelerini optimize eder.

    :param X_train: DataFrame, eğitim verisinin özellikleri
    :param y_train: Series, eğitim verisinin hedef değişkeni
    :param n_trials: int, deneme sayısı (varsayılan: 50)
    :return: dict, en iyi hiperparametre kombinasyonu
    """
    study = optuna.create_study(direction='maximize')
    study.optimize(lambda trial: objective(trial, X_train, y_train), n_trials=n_trials)
    
    print("Best model:", study.best_trial.params)
    return study.best_trial.params
