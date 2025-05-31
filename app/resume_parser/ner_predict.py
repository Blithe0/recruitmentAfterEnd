import paddle
from paddlenlp.transformers import ErnieForTokenClassification, ErnieTokenizer
from schema_map import label_map

tokenizer = ErnieTokenizer.from_pretrained('ernie-1.0')
model = ErnieForTokenClassification.from_pretrained('ernie-1.0', num_classes=len(label_map))
model.load_dict(paddle.load('./checkpoints/best_model.pdparams'))
model.eval()

def predict_entities(text: str) -> dict:
    tokens = tokenizer(list(text), return_tensors='pd', is_split_into_words=True, max_length=512, truncation=True)
    logits = model(tokens['input_ids'])[0]
    preds = paddle.argmax(logits, axis=-1).numpy()[0]

    entities, current_label = {}, ''
    for token, pred in zip(text, preds[1:len(text)+1]):
        label = label_map[pred]
        if label.startswith('B-'):
            current_label = label[2:]
            entities[current_label] = token
        elif label.startswith('I-') and current_label:
            entities[current_label] += token
        else:
            current_label = ''

    return entities
