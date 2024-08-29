import grpc
from pryvx import pryvx_pb2
from pryvx import pryvx_pb2_grpc
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import IsolationForest
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix
import requests
import pickle
import json
import base64

class Client:

    @staticmethod
    def preprocess_data(df, input_columns, target_column):

        X = df[input_columns]
        y = df[target_column]

        categorical_columns = X.select_dtypes(include=['object', 'category']).columns
        numerical_columns = X.select_dtypes(include=['int64', 'float64']).columns

        numerical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='mean')),
            ('scaler', StandardScaler())
        ])

        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('encoder', OneHotEncoder(handle_unknown='ignore'))
        ])

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numerical_transformer, numerical_columns),
                ('cat', categorical_transformer, categorical_columns)
            ])

        pipeline = Pipeline(steps=[('preprocessor', preprocessor)])

        X_preprocessed = pipeline.fit_transform(X)

        return X_preprocessed, y

        
    @staticmethod
    def train_logistic_regression(X, y, test_sample_size=0.2):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_sample_size)
        model = LogisticRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        conf_matrix = confusion_matrix(y_test, y_pred)
        return model, classification_report(y_test, y_pred, output_dict=True)
    

    @staticmethod
    def train_linear_regression(X, y, test_sample_size=0.2):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_sample_size)
        model = LinearRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        return model
    

    @staticmethod
    def train_iosolation_forest(X, test_sample_size=0.2):
        X_train, X_test = train_test_split(X, test_size=test_sample_size)
        model = IsolationForest()
        model.fit(X_train)
        y_pred = model.predict(X_test)
        return model
    

    @staticmethod
    def train_ensemble_model(X, y, test_sample_size=0.2, random_state=42):

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_sample_size, random_state=random_state)

        logistic_model = LogisticRegression()
        xgb_model = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
        rf_model = RandomForestClassifier()

        stacked_model = StackingClassifier(
            estimators=[
                ('logistic', logistic_model),
                ('xgb', xgb_model),
                ('rf', rf_model)
            ],
            final_estimator=LogisticRegression()
        )
        stacked_model.fit(X_train, y_train)
        y_pred = stacked_model.predict(X_test)

        return stacked_model, classification_report(y_test, y_pred, output_dict=True)
    
    
    @staticmethod
    def send_model_to_server(trained_model, metrics_dict, PROJECT_ID, COLLABORATOR_ID, CLIENT_SECRET_KEY):

        serialized_params = pickle.dumps(trained_model)
        encoded_params = base64.b64encode(serialized_params).decode('utf-8')
    
        payload = {
            "model_params": encoded_params,
            "metrics": json.dumps(metrics_dict),
        }

        headers = {
            "projectId": PROJECT_ID,
            "collaboratorId": COLLABORATOR_ID,
            "clientSecretKey": CLIENT_SECRET_KEY,
            "Content-Type": "application/json"
        }

        url = "https://api.pryvx.com/send-params"

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return "Error:", response.text


def train(features, labels):
    model = LogisticRegression()
    model.fit(features, labels)

    serialized_model = pickle.dumps(model)

    return serialized_model


def send_params(serialized_model, connection_url):

    with grpc.insecure_channel(connection_url) as channel:
        stub = pryvx_pb2_grpc.ModelServiceStub(channel)

        model_params = pryvx_pb2.ModelParams(params=serialized_model)

        response = stub.SendModelParams(model_params)

        return "Model Params sent to server"
    
