# app/resume_parser/parser_model.py
import os
import paddle
import paddle.nn as nn
from paddlenlp.transformers import ErnieForTokenClassification, ErnieTokenizer
from app.resume_parser.schema_map import label_map

model_path = os.path.join(os.path.dirname(__file__), 'checkpoints', 'best_model.pdparams')
tokenizer = ErnieTokenizer.from_pretrained('ernie-1.0')
model = ErnieForTokenClassification.from_pretrained('ernie-1.0', num_classes=len(label_map))
model.load_dict(paddle.load(model_path))
model.eval()

def predict(text: str) -> dict:
    words = list(text)
    input_ids = tokenizer(words, return_length=True, is_split_into_words=True, max_seq_len=512, return_tensors="pd")["input_ids"]
    logits = model(input_ids)[0]
    preds = paddle.argmax(logits, axis=-1).numpy()[0]

    # 标签映射回字段名
    result = {}
    for token, label_id in zip(words, preds[1:len(words)+1]):
        label = label_map[label_id]
        if label.startswith("B-") or label.startswith("I-"):
            key = label[2:]
            result.setdefault(key, "")
            result[key] += token
    return result
