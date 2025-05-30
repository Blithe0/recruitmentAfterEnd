import pdfplumber
from app.resume_parser.ner_predict import predict_entities

def parse_resume_pdf(pdf_path: str) -> dict:
    # 1. 提取PDF文本
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)

    # 2. 用你之前迁移的 predict/NER 代码进行结构化抽取
    entities = predict_entities(text)  # 返回字典

    # 3. 结构化字段适配（可根据实际标签调整）
    result = {
        'name': entities.get('姓名', ''),
        'gender': entities.get('性别', ''),
        'age': int(entities.get('年龄', 0)) if entities.get('年龄') else 0,
        'degree': entities.get('学历', ''),
        'skills': entities.get('技能', ''),
        'job_target': entities.get('意向岗位', ''),
        'phone': entities.get('手机', ''),
        'email': entities.get('邮箱', ''),
        # 其他字段
    }
    # 返回所有实体字典以便存储
    result.update({'parse_json': entities})
    return result
