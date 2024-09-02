import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder

def load_csv(file_path):
    return pd.read_csv(file_path)

def preprocess_data(df, target_column):
    numeric_features = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_features = df.select_dtypes(include=['object']).columns.tolist()
    
    X = df.drop(columns=[target_column])
    y = df[target_column]
    
    X_numeric = X[numeric_features]
    X_categorical = X[categorical_features]
    
    scaler = StandardScaler()
    X_numeric_scaled = scaler.fit_transform(X_numeric)
    
    encoder = OneHotEncoder(sparse=False)
    X_categorical_encoded = encoder.fit_transform(X_categorical)
    
    X_preprocessed = pd.DataFrame(X_numeric_scaled, columns=numeric_features)
    X_preprocessed = pd.concat([X_preprocessed, pd.DataFrame(X_categorical_encoded)], axis=1)
    
    return train_test_split(X_preprocessed, y, test_size=0.2, random_state=42)
