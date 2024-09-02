# v_ml_program

A package for performing classification on Iris dataset and 20 Newsgroups dataset.

## Usage

```python
from v_ml_program import train_and_evaluate_iris, train_and_evaluate_text_classifier

# Iris Classification
accuracy = train_and_evaluate_iris()
print(f"Iris Classification Accuracy: {accuracy:.2f}%")

# Text Classification
new_docs_predictions, accuracy, report, confusion_matrix = train_and_evaluate_text_classifier()
print("New Documents Predictions:")
for doc, category in new_docs_predictions:
    print(f"{doc} => {category}")

print(f"Text Classification Accuracy: {accuracy:.2f}")
print("Classification Report:")
print(report)
print("Confusion Matrix:")
print(confusion_matrix)



### **6. Install and Test the Package**

1. **Install Locally**

Navigate to the `v_ml_program` directory and install the package:

```bash
pip install .
