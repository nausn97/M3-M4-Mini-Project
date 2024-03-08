import sys
from pathlib import Path

from stroke_model.processing.features import OutlierHandler

file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))


from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier

from stroke_model.config.core import config

pipeline = Pipeline([
    ('label-encoder', LabelEncoder()),
    ('scaler', StandardScaler()),
    ('outlier_handler', OutlierHandler(threshold=3)),
    ('model_rf', RandomForestClassifier(
        n_estimators=150,
        max_depth=5,
        random_state=42
    ))
])

