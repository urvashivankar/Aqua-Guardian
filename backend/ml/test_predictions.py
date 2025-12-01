import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from predict import PollutionPredictor

# Test the predictor
predictor = PollutionPredictor()

# Test with a plastic image
plastic_img = r"C:\Users\Urvashi\OneDrive\Desktop\AQUA_guardian_project\data\dataset\plastic\IMG_0037_JPG.rf.f4a6ef575499373cf6cc6dc4b0a1abec.jpg"
print("\n=== Testing with Plastic Image ===")
result, error = predictor.predict(plastic_img)
if error:
    print(f"Error: {error}")
else:
    print(f"Predicted Class: {result['class']}")
    print(f"Confidence: {result['confidence']:.2%}")
    print(f"All Probabilities:")
    for cls, prob in result['all_probabilities'].items():
        print(f"  {cls}: {prob:.2%}")

# Test with a clean image
clean_img = r"C:\Users\Urvashi\OneDrive\Desktop\AQUA_guardian_project\data\dataset\clean"
clean_files = [f for f in os.listdir(clean_img) if f.endswith('.jpg')]
if clean_files:
    clean_img_path = os.path.join(clean_img, clean_files[0])
    print("\n=== Testing with Clean Image ===")
    result, error = predictor.predict(clean_img_path)
    if error:
        print(f"Error: {error}")
    else:
        print(f"Predicted Class: {result['class']}")
        print(f"Confidence: {result['confidence']:.2%}")
        print(f"All Probabilities:")
        for cls, prob in result['all_probabilities'].items():
            print(f"  {cls}: {prob:.2%}")

# Test with oil spill image
oil_img = r"C:\Users\Urvashi\OneDrive\Desktop\AQUA_guardian_project\data\dataset\oil_spill"
oil_files = [f for f in os.listdir(oil_img) if f.endswith('.jpg')]
if oil_files:
    oil_img_path = os.path.join(oil_img, oil_files[0])
    print("\n=== Testing with Oil Spill Image ===")
    result, error = predictor.predict(oil_img_path)
    if error:
        print(f"Error: {error}")
    else:
        print(f"Predicted Class: {result['class']}")
        print(f"Confidence: {result['confidence']:.2%}")
        print(f"All Probabilities:")
        for cls, prob in result['all_probabilities'].items():
            print(f"  {cls}: {prob:.2%}")

# Test with sewage image
sewage_img = r"C:\Users\Urvashi\OneDrive\Desktop\AQUA_guardian_project\data\dataset\sewage"
sewage_files = [f for f in os.listdir(sewage_img) if f.endswith('.jpg')]
if sewage_files:
    sewage_img_path = os.path.join(sewage_img, sewage_files[0])
    print("\n=== Testing with Sewage Image ===")
    result, error = predictor.predict(sewage_img_path)
    if error:
        print(f"Error: {error}")
    else:
        print(f"Predicted Class: {result['class']}")
        print(f"Confidence: {result['confidence']:.2%}")
        print(f"All Probabilities:")
        for cls, prob in result['all_probabilities'].items():
            print(f"  {cls}: {prob:.2%}")
