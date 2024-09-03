import time
import unicodedata

from langdetect import detect_langs, DetectorFactory
from tqdm import tqdm

from .model import NERModel

DetectorFactory.seed = 0


class MetaCleaner:
    def __init__(self, model_name_or_path, max_length=4096):
        self.model = NERModel(model_name_or_path)
        self.max_length = max_length

    def clean(self, texts, confidence_threshold=0.80, batch_size=16):
        start_time = time.time()

        total_meta_tags, total_tokens, non_english_docs = 0, 0, 0

        texts = self.normalize_texts(texts)
        texts_to_process = []

        for text in texts:
            if not self.is_english(text):
                non_english_docs += 1
                continue
            texts_to_process.append(text)

        cleaned_texts = []
        for i in tqdm(range(0, len(texts_to_process), batch_size), desc="Processing", mininterval=0.5):
            batch_texts = texts_to_process[i:i + batch_size]

            for text in batch_texts:
                if len(self.model.tokenizer.tokenize(text)) <= self.max_length:
                    batch_cleaned, meta_tags, tokens = self._clean_batch([text], confidence_threshold)
                    cleaned_texts.extend(batch_cleaned)
                else:
                    cleaned_long_text, meta_tags, tokens = self._clean_long_text(text, confidence_threshold)
                    cleaned_texts.append(cleaned_long_text)

                total_meta_tags += meta_tags
                total_tokens += tokens

        meta_tag_percentage = (total_meta_tags / total_tokens) * 100 if total_tokens > 0 else 0
        non_english_percentage = (non_english_docs / len(texts)) * 100 if len(texts) > 0 else 0
        end_time = time.time()
        runtime = end_time - start_time

        self.print_report(runtime, meta_tag_percentage, non_english_percentage)

        return cleaned_texts

    def _clean_batch(self, texts, confidence_threshold):
        predictions_batch = self.model.predict(texts)
        batch_cleaned_texts = []

        meta_tags_detected = 0
        total_tokens = 0

        for predictions in predictions_batch:
            cleaned_tokens = []

            for token, pred, conf in predictions:
                total_tokens += 1
                if token in ["<pad>", "<s>", "</s>"]:
                    continue
                if pred in [1, 2] and conf >= confidence_threshold:
                    meta_tags_detected += 1
                    continue

                if token == "Ċ":
                    cleaned_tokens.append("\n")
                elif token.startswith("Ġ"):
                    cleaned_tokens.append(" " + token[1:])
                else:
                    cleaned_tokens.append(token)

            cleaned_text = "".join(cleaned_tokens)

            cleaned_text = cleaned_text.replace(" \n", "\n").replace("\n ", "\n").strip()
            batch_cleaned_texts.append(cleaned_text)

        return batch_cleaned_texts, meta_tags_detected, total_tokens

    def _clean_long_text(self, text, confidence_threshold):
        full_tokens = self.model.tokenizer.tokenize(text)
        cleaned_text_parts = []
        meta_tags_detected = 0
        total_tokens = 0

        for i in range(0, len(full_tokens), self.max_length):
            chunk_tokens = full_tokens[i:i + self.max_length]
            chunk_text = self.model.tokenizer.convert_tokens_to_string(chunk_tokens)
            batch_cleaned, meta_tags, tokens = self._clean_batch([chunk_text], confidence_threshold)
            cleaned_text_parts.extend(batch_cleaned)
            meta_tags_detected += meta_tags
            total_tokens += tokens

        final_cleaned_text = "".join(cleaned_text_parts).replace(" \n", "\n").replace("\n ", "\n").strip()
        return final_cleaned_text, meta_tags_detected, total_tokens

    @staticmethod
    def normalize_texts(texts):
        return [unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII') for text in texts]

    @staticmethod
    def is_english(text):
        try:
            detected_langs = detect_langs(text)
            return any(lang.lang == 'en' and lang.prob > 0.5 for lang in detected_langs)
        except Exception as e:
            print(f"Language detection failed: {e}")
            return False

    @staticmethod
    def print_report(runtime, meta_tag_percentage, non_english_percentage):
        print("\n" + "=" * 50)
        print("Processing Complete!")
        print(f"Runtime: {runtime:.2f} seconds")
        print(f"Percentage of META tags detected: {meta_tag_percentage:.2f}%")
        print(f"Percentage of non-English documents: {non_english_percentage:.2f}%")
        print("=" * 50)
