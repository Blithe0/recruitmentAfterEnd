# app/resume_parser/ner_predict.py
import os
import paddle
from paddlenlp.transformers import ErnieForTokenClassification, ErnieTokenizer

from app.resume_parser.schema_map import label_map

# 加载模型和分词器，只初始化一次
# MODEL_PATH = os.path.join(os.path.dirname(__file__), 'checkpoints', 'best_model.pdparams')
tokenizer = ErnieTokenizer.from_pretrained('ernie-1.0')
model = ErnieForTokenClassification.from_pretrained('ernie-1.0', num_classes=len(label_map))
# model.load_dict(paddle.load(MODEL_PATH))
model.eval()

def predict_entities(text: str) -> dict:
    # 不要手动切分成字符数组，直接传入原始字符串
    encoding = tokenizer(
        text,
        return_tensors="pd",
        max_length=512,
        truncation=True,
        padding=True
    )

    input_ids = encoding["input_ids"]  # shape: [1, seq_len]
    logits = model(input_ids)[0]       # shape: [1, seq_len, num_classes]
    preds = paddle.argmax(logits, axis=-1).numpy()[0]  # shape: [seq_len]

    tokens = tokenizer.tokenize(text)  # 获取 tokenizer 对应的 token
    result = {}
    for token, label_id in zip(tokens, preds[1:len(tokens)+1]):  # 忽略 [CLS]
        # label = label_map[label_id]
        label = label_map[int(label_id)]
        print(f"label_id type: {type(label_id)}, value: {label_id}")

        if label.startswith("B-") or label.startswith("I-"):
            key = label[2:]
            result.setdefault(key, "")
            result[key] += token.replace("##", "")  # 去掉子词前缀（若有）
    return result