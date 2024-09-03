import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification


class NERModel:
    def __init__(self, model_name_or_path, device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
        self.model = AutoModelForTokenClassification.from_pretrained(model_name_or_path)
        self.model.to(self.device)
        self.model.eval()

    def predict(self, texts):
        tokens = self.tokenizer(
            texts,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=4096
        ).to(self.device)

        with torch.no_grad():
            output = self.model(**tokens)

        logits = output.logits
        probabilities = torch.softmax(logits, dim=-1)
        confidence, predictions = torch.max(probabilities, dim=-1)

        token_ids = tokens['input_ids']
        tokens_converted = [self.tokenizer.convert_ids_to_tokens(ids) for ids in token_ids]

        return [
            list(zip(tokens, preds.tolist(), confs.tolist()))
            for tokens, preds, confs in zip(tokens_converted, predictions, confidence)
        ]
