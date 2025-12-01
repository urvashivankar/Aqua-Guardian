try:
    import os
    from .predict import PollutionPredictor
    
    # Initialize predictor
    print("⏳ Initializing ML Predictor...")
    predictor = PollutionPredictor()
    
    ML_AVAILABLE = True
    print("✅ ML Predictor initialized successfully.")
except Exception as e:
    print(f"⚠️  ML dependencies not available or model failed to load: {e}")
    print("   Image classification will be disabled.")
    ML_AVAILABLE = False

def predict_image(image_bytes, demo_mode=False):
    """
    Predict pollution type from image.
    
    Args:
        image_bytes: Image data as bytes
        demo_mode: If True, simulates high-confidence predictions for testing
    
    Returns:
        dict: {"class": str, "confidence": float}
    """
    # Demo mode: Force high confidence for testing notifications
    if demo_mode or os.getenv("ML_DEMO_MODE", "false").lower() == "true":
        import random
        predicted_class = random.choice(["plastic", "sewage", "oil_spill"])
        confidence = random.uniform(0.91, 0.99)
        print(f"🔬 DEMO MODE: Simulated {predicted_class} at {confidence:.1%} confidence")
        return {
            "class": predicted_class,
            "confidence": confidence
        }

    if not ML_AVAILABLE:
        return {"class": "unknown", "confidence": 0.0}
    
    try:
        result, error = predictor.predict_bytes(image_bytes)
        if error:
            print(f"Inference error: {error}")
            return {"class": "unknown", "confidence": 0.0}
        
        return {
            "class": result["class"],
            "confidence": result["confidence"]
        }
    except Exception as e:
        print(f"Inference error: {e}")
        return {"class": "unknown", "confidence": 0.0}
