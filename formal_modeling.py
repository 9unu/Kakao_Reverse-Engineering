import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from kakao_text_preprocessing import *
import torch
from transformers import (
    T5TokenizerFast,
    T5ForConditionalGeneration,
    Seq2SeqTrainingArguments,
    Seq2SeqTrainer,
    DataCollatorForSeq2Seq,
    EarlyStoppingCallback)
from tokenizers import Tokenizer
from torch.utils.data import Dataset
import pandas as pd
import shutil

def modeling(csv_path):
    print(torch.cuda.is_available())
    df=pd.read_csv(csv_path)

    model_name="paust/pko-t5-base" #'paust/pko-t5-small'
    # 모델 로드
    tokenizer = T5TokenizerFast.from_pretrained(model_name)
    df.dropna(inplace=True)
    # 말투 변환 맵
    style_map = {
        'formal': '상냥체',
        'random' : "무작위",
        'gentle' : "정중체"
    }
    
# 학습 데이터 만드는 class
    class TextStyleTransferDataset(Dataset):
        def __init__(self,
                    df: pd.DataFrame,
                    tokenizer: Tokenizer
                    ):
            self.df = df
            self.tokenizer = tokenizer

        def __len__(self):
            return len(self.df)

        def __getitem__(self, index):
            row = self.df.iloc[index, :].dropna().sample(2)
            text1 = row[0]
            text2 = row[1]
            target_style = row.index[1]
            target_style_name = style_map[target_style]

            encoder_text = f"{target_style_name} 말투로 변환: {text1}"
            decoder_text = f"{text2}{self.tokenizer.eos_token}"
            model_inputs = self.tokenizer(encoder_text, max_length=64, truncation=True)

            with self.tokenizer.as_target_tokenizer():
                labels = tokenizer(decoder_text, max_length=64, truncation=True)
                model_inputs['labels'] = labels['input_ids']

            return model_inputs
    
    
    # 데이터 분할
    from sklearn.model_selection import train_test_split

    # 문체 변환용으로 데이터 변환
    df_train, df_test = train_test_split(df, test_size=0.2, random_state=42)
    print(len(df_train), len(df_test))

    train_dataset = TextStyleTransferDataset(
        df_train,
        tokenizer
    )
    test_dataset = TextStyleTransferDataset(
        df_test,
        tokenizer
    )

    model =T5ForConditionalGeneration.from_pretrained(model_name)

    data_collator = DataCollatorForSeq2Seq(
        tokenizer=tokenizer, model=model
    )

    directory_to_delete = "saved_model"

    training_args = Seq2SeqTrainingArguments(
                    directory_to_delete,
                    evaluation_strategy = "epoch",
                    save_strategy = "epoch",
                    eval_steps = 10,
                    load_best_model_at_end = True,
                    per_device_train_batch_size=10,
                    per_device_eval_batch_size=10,
                    gradient_accumulation_steps=2,
                    weight_decay=0.01,
                    save_total_limit=1,
                    num_train_epochs=30,
                    predict_with_generate=True,
                    fp16=False,
            )

    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
        callbacks = [EarlyStoppingCallback(early_stopping_patience=5)]
    )

    # 모델 학습
    trainer.train()


    trainer.save_model("modeling\model.pth")
    if os.path.exists(directory_to_delete):
        shutil.rmtree(directory_to_delete)
        
"""함수 호출"""
if __name__ == "__main__":
    file_path=input("학습할 csv파일 경로:")
    modeling(file_path)