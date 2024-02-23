import json

import torch
import nltk
import numpy as np
from scipy.io.wavfile import write as write_wav
from transformers import VitsTokenizer, VitsModel, set_seed

nltk.download("punkt", quiet=True)

tokenizer = VitsTokenizer.from_pretrained("facebook/mms-tts-eng")
model = VitsModel.from_pretrained("facebook/mms-tts-eng")

with open("data/epub.json") as f:
    content = json.load(f)


def tts(text):

    inputs = tokenizer(text=text, normalize=True, return_tensors="pt")
    set_seed(555)  # make deterministic

    with torch.no_grad():
        outputs = model(**inputs)

    return outputs.waveform[0].numpy()


for d in content[1:4]:
    print("PAGE NUMBER", d["page_number"])

    texts = nltk.sent_tokenize(d["text"].strip())
    out_path = "data/audios/epub_page{}.wav".format(d["page_number"])

    waveforms = []

    for text in texts:
        waveforms.append(
            tts(
                text=text,
            )
        )

    waveform = np.concatenate(waveforms)

    write_wav(out_path, rate=model.config.sampling_rate, data=waveform)
