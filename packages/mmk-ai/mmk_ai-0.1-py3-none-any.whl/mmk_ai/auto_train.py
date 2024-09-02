from MK_ML.data_preprocessing import preprocess_data
from MK_ML.visualization import univariate_visualization, bivariate_visualization, multivariate_visualization, correlation_heatmap, interactive_heatmap
from MK_ML.model_training import optimize_hyperparameters, train_model_threaded, save_model
from MK_ML.evaluation import evaluate_model
from MK_ML.scoring import calculate_scores, plot_roc_curve
import concurrent.futures
import csv
import os

def auto_train(data, target_column, model_names, save_model_paths=None, csv_export_paths=None, visualization_theme="Viridis", n_trials=50):
    """
    Tüm modelleri aynı anda eğitir, Optuna ile en iyi parametreleri bulur ve sonuçları döndürür.
    
    :param data: DataFrame, işlenecek veri seti
    :param target_column: str, hedef sütun adı
    :param model_names: list, eğitilecek modellerin isimleri
    :param save_model_paths: dict, model isimlerini anahtar olarak alan ve modellerin kaydedileceği dosya yollarını içeren sözlük
    :param csv_export_paths: dict, model isimlerini anahtar olarak alan ve sonuçların kaydedileceği CSV dosya yollarını içeren sözlük
    :param visualization_theme: str, görselleştirme için kullanılacak renk teması (varsayılan: 'Viridis')
    :param n_trials: int, Optuna ile yapılacak deneme sayısı (varsayılan: 50)
    :return: dict, eğitilen modeller ve metrik sonuçları
    """
    
    # 1. Adım: Veri Görselleştirme
    print("Performing Univariate Visualization...")
    univariate_visualization(data, theme=visualization_theme)
    
    print("Performing Bivariate Visualization...")
    bivariate_visualization(data, target_column, theme=visualization_theme)
    
    print("Performing Multivariate Visualization...")
    multivariate_visualization(data, theme=visualization_theme)
    
    print("Generating Correlation Heatmap...")
    correlation_heatmap(data)
    
    print("Generating Interactive Heatmap...")
    interactive_heatmap(data)
    
    # 2. Adım: Veri Ön İşleme
    print("Preprocessing Data...")
    X_train, X_test, y_train, y_test = preprocess_data(data, target_column)
    
    # 3. Adım: Optuna ile Hiperparametre Optimizasyonu
    print("Optimizing Hyperparameters with Optuna...")
    best_params = optimize_hyperparameters(X_train, y_train, n_trials=n_trials)
    
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
                
                # 5. Adım: Model Değerlendirme
                print(f"Evaluating Model: {model_name}...")
                evaluate_model(model, X_test, y_test)
                
                # 6. Adım: Değerlendirme Metrikleri ve ROC Eğrisi
                print(f"Calculating Scores for {model_name}...")
                scores = calculate_scores(y_test, model.predict(X_test))
                results[model_name]["scores"] = scores
                print(f"Scores for {model_name}: {scores}")
                
                if model_name.endswith('Classifier'):
                    print(f"Plotting ROC Curve for {model_name}...")
                    plot_roc_curve(model, X_test, y_test)
                
                # 7. Adım: Model Kaydetme
                if save_model_paths and model_name in save_model_paths:
                    print(f"Saving {model_name} to {save_model_paths[model_name]}...")
                    save_model(model, save_model_paths[model_name])
                
                # 8. Adım: Sonuçları CSV'ye Aktarma
                if csv_export_paths and model_name in csv_export_paths:
                    print(f"Exporting Results for {model_name} to {csv_export_paths[model_name]}...")
                    with open(csv_export_paths[model_name], mode='w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(['Metric', 'Score'])
                        for metric, value in scores.items():
                            writer.writerow([metric, value])
            
            except Exception as exc:
                print(f"{model_name} generated an exception: {exc}")
    
    return results
