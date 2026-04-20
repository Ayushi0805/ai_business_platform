import os
import numpy as np

_model = None

def _load_model():
    global _model
    try:
        import joblib
        model_path = os.path.join('ml_models', 'fraud_model.pkl')
        if os.path.exists(model_path):
            _model = joblib.load(model_path)
            print('[fraud] sklearn model loaded.')
            return
        else:
            print('[fraud] No trained model found — using rule-based fallback.')
            return
    except ImportError:
        print('[fraud] joblib not installed — using rule-based fallback.')
        return

_load_model()

def detect_fraud(total_price: float, quantity: int, user_id: int) -> bool:
    if _model is not None:
        features = np.array([[total_price, quantity, user_id]])
        prediction = _model.predict(features)
        return bool(prediction[0])
    
    # Rule-based fallback
    if total_price > 10000:
        return True
    if quantity > 100:
        return True
    return False
