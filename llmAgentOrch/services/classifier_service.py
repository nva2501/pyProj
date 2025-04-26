from transformers import pipeline


class ClassifierService:
    def __init__(self):
        self.base_labels = ["support", "sales", "billing", "technical issue", "feedback"]
        self.additional_examples = []  # New (text, label) pairs
        self.classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

    def predict(self, text: str) -> str:
        all_labels = self.base_labels + [label for _, label in self.additional_examples]
        all_labels = list(set(all_labels))  # remove duplicates
        result = self.classifier(text, all_labels)
        return result['labels'][0]

    def add_training_example(self, text: str, label: str):
        """Add a new (text, label) pair for live training"""
        self.additional_examples.append((text, label))
        self._retrain()

    def _retrain(self):
        # Simulate retraining by refreshing labels set
        # Full fine-tuning requires actual model re-training (out of scope for live)
        all_labels = self.base_labels + [label for _, label in self.additional_examples]
        self.labels = list(set(all_labels))
        print(f"[Retrain] Updated labels for classification: {self.labels}")
