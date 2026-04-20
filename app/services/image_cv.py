"""
Phase 3 — Computer Vision (YOLO) image analysis service.

Install: pip install ultralytics torch torchvision

YOLOv8n weights are downloaded automatically on first use (~6 MB).
"""
from ultralytics import YOLO

_model = YOLO('yolov8n.pt')

def analyze_image(image_path: str) -> dict:
    results = _model(image_path)
    labels = [_model.names[int(c)] for c in results[0].boxes.cls]
    
    if results[0].boxes.conf.numel() > 0:
        conf = float(results[0].boxes.conf.mean())
    else:
        conf = 0.0
        
    return {
        'detected_objects': labels,
        'confidence': conf,
        'raw_count': len(labels)
    }
