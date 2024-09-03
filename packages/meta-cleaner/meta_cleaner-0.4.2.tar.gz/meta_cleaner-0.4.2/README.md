# meta_cleaner

`meta_cleaner` is a Python package designed to clean text from META tags using XLM-RoBERTa (large-sized model).

`trainer.ipynb` is a notebook that creates a dataset and a NER model.

## Installation

```bash
pip install meta-cleaner
```

or

```bash
pip install git+https://github.com/pirr-me/meta_cleaner.git
```

### Install Locally

To install locally in editable mode (for development):

```
pip install -e .
```

## Usage

```python
from meta_cleaner.cleaner import MetaCleaner

# Initialize the MetaCleaner
meta_cleaner = MetaCleaner(model_name_or_path='Pirr/longformer-4096-large-ner')

# List of texts to clean
texts = ['[Genre: Fiction, Consensual Sex, Oral Sex, Romance, Teen Male/Teen Female]\nCHAPTER 15\nWe walked together into the school office to turn in our early dismissal note. Mrs. Roscoe laughed when she saw it. "Don\'t trust him to go on his own, eh Cinda? I can\'t say that I blame you. I never let my husband go on his own either. He can never remember what the doctor said. Okay, here\'s your pass." She handed Cinda the blue excuse slip and we walked out into the hallway. One of the first people I saw was Mitch. He didn\'t look very happy.\n"Surely you\'re still not pissed about New Year\'s Eve?"\n"Yeah, but not your part. We got stopped by the cops not even five minutes after leaving your place.']

# Clean the texts with batch inference
cleaned_texts = meta_cleaner.clean(texts, batch_size=8, confidence_threshold=0.8)

# Display the cleaned texts
for i, cleaned_text in enumerate(cleaned_texts):
    print(f"Cleaned Text {i + 1}:\n{cleaned_text}\n")
```

## Clean data from GCP

```python
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from google.cloud import storage
from tqdm import tqdm
from datasets import Dataset
from meta_cleaner.cleaner import MetaCleaner

storage_client = storage.Client()

bucket_name = 'pirr-training-data'
prefix = 'Processed_data/cleaned-venus'

bucket = storage_client.bucket(bucket_name)
blobs = list(storage_client.list_blobs(bucket_name, prefix=prefix))

txt_blobs = [blob for blob in blobs if blob.name.endswith('.txt')]

def download_blob(blob):
    return blob.download_as_text()

texts = []
with ThreadPoolExecutor(max_workers=16) as executor:
    future_to_blob = {executor.submit(download_blob, blob): blob for blob in txt_blobs}
    
    for future in tqdm(as_completed(future_to_blob), total=len(txt_blobs), desc="Downloading files"):
        blob = future_to_blob[future]
        try:
            content = future.result()
            texts.append(content)
        except Exception as e:
            print(f"Error downloading {blob.name}: {e}")


meta_cleaner = MetaCleaner(model_name_or_path='Pirr/longformer-4096-large-ner')
cleaned_texts = meta_cleaner.clean(texts, batch_size=16, confidence_threshold=0.8)
dataset = Dataset.from_dict({"text": cleaned_texts})

#dataset.push_to_hub("...")
```
