、import spacy
from spacy.training.example import Example
import random

nlp = spacy.load("en_core_web_sm")  # 加载基础英语模型
ner = nlp.get_pipe("ner")

# 添加标签
ner.add_label("TECH")

train_data = [
    ("Looking for a skilled Java developer with expertise in Spring and Hibernate frameworks.", {"entities": [(22, 26, "TECH"), (55, 61, "TECH"), (66, 75, "TECH")]}),
    # 添加更多训练数据
]

# 训练 NER（命名实体识别）
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
with nlp.disable_pipes(*other_pipes):
    optimizer = nlp.begin_training()

    for itn in range(20):  # 迭代训练
        print(f"开始迭代 {itn}")
        random.shuffle(train_data)
        losses = {}

        # 分批训练
        for batch in spacy.util.minibatch(train_data, size=2):  
            examples = [Example.from_dict(nlp.make_doc(text), annotations) for text, annotations in batch]
            nlp.update(examples, drop=0.5, losses=losses)  

        print(losses)

# 保存模型
nlp.to_disk("model_upgrade")
