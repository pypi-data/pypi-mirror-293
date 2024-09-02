from MK_ML.data_preprocessing import preprocess_data, load_csv
from MK_ML.model_training import train_model_threaded
from MK_ML.evaluation import evaluate_model
from MK_ML.scoring import calculate_scores, plot_roc_curve
import concurrent.futures

def easy_train(data_path):
    """
    Verilen veri setini yükler ve tüm modeller ile eş zamanlı eğitim yapar.
    
    :param data_path: str, eğitim için kullanılacak veri setinin dosya yolu
    """
    # 1. Adım: Veriyi Yükleme
    data = load_csv(data_path)
    
    # 2. Adım: Veri Ön İşleme
    target_column = data.columns[-1]  # Son sütun hedef olarak varsayılır
    X_train, X_test, y_train, y_test = preprocess_data(data, target_column)
    
    # 3. Adım: Eğitilecek Modellerin İsimleri
    model_names = [
        'RandomForestClassifier',
        'GradientBoostingClassifier',
        'SVC',
        'LogisticRegression',
        'KNeighborsClassifier',
        'DecisionTreeClassifier'
    ]
    
    # 4. Adım: Model Eğitimi için Thread Pool
    results = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_model = {executor.submit(train_model_threaded, X_train, X_test, y_train, y_test, model_name): model_name for model_name in model_names}
        for future in concurrent.futures.as_completed(future_to_model):
            model_name = future_to_model[future]
            try:
                model, score = future.result()
                results[model_name] = {
                    "model": model,
                    "score": score
                }
                print(f"{model_name} Training Completed. Score: {score}")
                
                # Model Değerlendirme
                evaluate_model(model, X_test, y_test)
                
                # Değerlendirme Metrikleri ve ROC Eğrisi
                scores = calculate_scores(y_test, model.predict(X_test))
                results[model_name]["scores"] = scores
                print(f"Scores for {model_name}: {scores}")
                
                if model_name.endswith('Classifier'):
                    plot_roc_curve(model, X_test, y_test)
            
            except Exception as exc:
                print(f"{model_name} generated an exception: {exc}")
    
    return results
