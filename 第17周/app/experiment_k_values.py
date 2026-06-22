"""
K-Value Comparison Experiment
This script conducts K=1,3,5,15 experiments and records accuracy metrics
"""
import json
import sys
sys.path.insert(0, '/'.join(__file__.split('/')[:-3]))

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from src.ai.text_features import TextFeatureExtractor
from src.ai.knn_classifier import KNNTextClassifier

def load_data():
    """Load dataset from JSON"""
    with open("src/data/dataset.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    texts = [item["text"] for item in data]
    labels = [item["label"] for item in data]
    return texts, labels

def run_experiment():
    """Run K-value comparison experiment"""
    print("="*60)
    print("K-Value Comparison Experiment for KNN Text Classifier")
    print("="*60)
    
    # Load data
    texts, labels = load_data()
    print(f"\nDataset Info: {len(texts)} samples")
    
    # Feature extraction
    extractor = TextFeatureExtractor()
    X = extractor.fit_transform(texts)
    print(f"Feature dimension: {X.shape[1]}")
    
    # Train-test split (70-30)
    X_train, X_test, y_train, y_test = train_test_split(
        X, labels, test_size=0.3, random_state=42, stratify=labels
    )
    
    print(f"Training set: {X_train.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")
    
    # Test different K values
    k_values = [1, 3, 5, 15]
    results = {}
    
    print("\n" + "="*60)
    print("Experiment Results")
    print("="*60)
    
    for k in k_values:
        print(f"\n--- K = {k} ---")
        
        # Train classifier
        classifier = KNNTextClassifier(k=k)
        classifier.train(X_train, y_train)
        
        # Make predictions
        predictions = classifier.predict_batch(X_test)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, predictions)
        
        results[k] = {
            'accuracy': accuracy,
            'predictions': predictions,
            'y_test': y_test
        }
        
        print(f"Accuracy: {accuracy:.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, predictions))
        
        # Confusion matrix
        cm = confusion_matrix(y_test, predictions)
        print(f"Confusion Matrix:\n{cm}")
    
    # Summary comparison
    print("\n" + "="*60)
    print("Summary Comparison")
    print("="*60)
    print(f"{'K Value':<10} {'Accuracy':<15} {'Note'}")
    print("-"*60)
    
    for k in k_values:
        accuracy = results[k]['accuracy']
        note = ""
        if k == 1:
            note = "Overfitting risk: memorizes all training data"
        elif k == 15:
            note = "Underfitting risk: too many neighbors averaging"
        elif k == 3:
            note = "Usually best balance"
        elif k == 5:
            note = "More robust than K=3"
        
        print(f"{k:<10} {accuracy:.4f}        {note}")
    
    # Analysis
    print("\n" + "="*60)
    print("Analysis & Insights")
    print("="*60)
    
    acc_1 = results[1]['accuracy']
    acc_3 = results[3]['accuracy']
    acc_5 = results[5]['accuracy']
    acc_15 = results[15]['accuracy']
    
    print(f"\n1. Overfitting Analysis (K=1 vs K=3):")
    print(f"   K=1 accuracy: {acc_1:.4f}")
    print(f"   K=3 accuracy: {acc_3:.4f}")
    if acc_1 > acc_3:
        print(f"   → K=1 shows higher accuracy but OVERFITTING risk exists")
        print(f"   → K=1 memorizes training examples, poor generalization")
    else:
        print(f"   → Balanced results, good generalization")
    
    print(f"\n2. Underfitting Analysis (K=5 vs K=15):")
    print(f"   K=5 accuracy: {acc_5:.4f}")
    print(f"   K=15 accuracy: {acc_15:.4f}")
    if acc_15 < acc_5:
        print(f"   → K=15 shows lower accuracy (UNDERFITTING)")
        print(f"   → Too many neighbors cause over-smoothing")
    else:
        print(f"   → K=15 performs acceptably")
    
    print(f"\n3. Optimal K Selection:")
    best_k = max(k_values, key=lambda k: results[k]['accuracy'])
    print(f"   → Recommended K: {best_k}")
    print(f"   → Best accuracy: {results[best_k]['accuracy']:.4f}")
    
    return results

if __name__ == "__main__":
    results = run_experiment()
    print("\n" + "="*60)
    print("Experiment completed successfully!")
    print("="*60)
