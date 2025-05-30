# app/resume_parser/ner_predict.py
import os
import paddle
from paddlenlp.transformers import ErnieForTokenClassification, ErnieTokenizer
from app.resume_parser.schema_map import label_map

# 模型路径
model_path = os.path.join(os.path.dirname(__file__), 'checkpoints', 'best_model.pdparams')

# 初始化 tokenizer & model
tokenizer = ErnieTokenizer.from_pretrained('ernie-1.0')
model = ErnieForTokenClassification.from_pretrained(
    'ernie-1.0',
    num_classes=len(label_map)
)
# 加载训练好的权重
state_dict = paddle.load(model_path)
model.set_dict(state_dict)
model.eval()

def predict_entities(text: str) -> dict:
    """
    对一整段简历文本做 NER 推理，返回结构化字段字典。
    这里只演示 “BIO” 拼接逻辑，按需要调整。
    """
    # 1. 输入切成字列表
    tokens = list(text)
    # 2. 构造模型输入：去掉 return_length
    inputs = tokenizer(
        tokens,
        is_split_into_words=True,
        max_length=512,
        truncation=True,
        return_attention_mask=True,
        return_token_type_ids=True,
        return_tensors="pd"
    )
    # 3. 模型前向，得到 logits
    logits = model(**inputs)[0]  # [batch_size, seq_len, num_classes]
    preds = paddle.argmax(logits, axis=-1).numpy()[0]  # [seq_len]

    # 4. BIO 拼接成字段
    info = {key: "" for key in ["name", "age", "education", "school", "work_time", "match_position"]}
    current = None
    # preds 包含 [CLS] token 预测在 preds[0]，我们从 preds[1] 开始对齐 tokens[0]
    for token, label_id in zip(tokens, preds[1: len(tokens) + 1]):
        label = label_map.get(int(label_id), "O")
        if label.startswith("B-"):
            current = label[2:]
            info.setdefault(current, "")
            info[current] += token
        elif label.startswith("I-") and current:
            info[current] += token
        else:
            current = None

    return info
