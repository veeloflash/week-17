"""
AI Question Classifier v1 - Interactive Mode
Classifies user questions into: Math, Coding, English, General
"""
import json
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from src.ai.text_features import TextFeatureExtractor
from src.ai.knn_classifier import KNNTextClassifier
from src.security.input_guard import InputGuard

ROOT = Path(__file__).resolve().parent
DATASET_PATH = ROOT / "src" / "data" / "dataset.json"

def main():
    """Main interactive classifier"""
    print("="*60)
    print("AI Question Classifier v1")
    print("="*60)
    
    # Load data
    with DATASET_PATH.open("r", encoding="utf-8") as d:
        data = json.load(d)
    
    texts = [item["text"] for item in data]
    labels = [item["label"] for item in data]
    
    print(f"\nLoaded {len(texts)} training samples")
    
    # Ask user for K value
    print("\nSelect K value for KNN:")
    print("  1 - K=1   (high accuracy, risk of overfitting)")
    print("  2 - K=3   (recommended, balanced)")
    print("  3 - K=5   (robust, good generalization)")
    print("  4 - K=15  (smooth, risk of underfitting)")
    print("  5 - Auto  (use K=5)")
    
    choice = input("\nEnter choice (1-5): ").strip()
    
    k_values = {
        '1': 1,
        '2': 3,
        '3': 5,
        '4': 15,
        '5': 5
    }
    
    k = k_values.get(choice, 5)
    print(f"\nUsing K={k}")
    
    # Feature extraction
    extractor = TextFeatureExtractor()
    X = extractor.fit_transform(texts)
    
    # Train-test split for evaluation
    X_train, X_test, y_train, y_test = train_test_split(
        X, labels, test_size=0.3, random_state=42, stratify=labels
    )
    
    # Train classifier
    classifier = KNNTextClassifier(k=k)
    classifier.train(X_train, y_train)
    
    # Evaluate on test set
    predictions = classifier.predict_batch(X_test)
    accuracy = accuracy_score(y_test, predictions)
    
    print(f"\n--- Model Evaluation (30% test set) ---")
    print(f"Test Accuracy: {accuracy:.4f} ({accuracy*100:.1f}%)")
    print(f"Test Samples: {len(y_test)}")
    print(f"Correct Predictions: {sum(predictions == y_test)}/{len(y_test)}")
    
    # Initialize security guard
    guard = InputGuard()
    
    # Interactive prediction loop
    print("\n" + "="*60)
    print("Enter questions to classify (type 'quit' to exit)")
    print("="*60)
    
    while True:
        try:
            user_input = input("\nEnter your question: ").strip()
            
            if user_input.lower() == 'quit':
                print("Thank you for using AI Question Classifier!")
                break
            
            # Security validation
            ok, msg = guard.validate(user_input)
            if not ok:
                print(f"⚠️ Input validation failed: {msg}")
                continue
            
            # Make prediction
            X_test_input = extractor.transform([user_input])
            prediction = classifier.predict(X_test_input)
            
            print(f"✓ Classification: {prediction}")
            
        except KeyboardInterrupt:
            print("\n\nProgram interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()

