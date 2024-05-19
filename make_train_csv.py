import pandas as pd
import re
from kss import split_sentences
from kakao_text_preprocessing import *

"""카톡 ai로 생성한 user, formal, gentle txt파일을 데이터 프레임으로 변환"""
def txt_to_train_df(txt_path):
    with open(txt_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    df = pd.DataFrame(columns=['text'])
    for line in lines:
        if line is not None:
            df.loc[len(df)] = line.strip()
    # user, formal, gentle 분리
    df['user'] = df[df['text'].str.startswith('[user]')]['text']
    df['formal'] = df[df['text'].str.startswith('[formal]')]['text']
    df['gentle'] = df[df['text'].str.startswith('[gentle]')]['text']
    origin = df['user'].dropna().to_frame().reset_index(drop=True)
    sangnyang=df['formal'].dropna().to_frame().reset_index(drop=True)
    jungjoong=df['gentle'].dropna().to_frame().reset_index(drop=True)

    origin['user']=origin['user'].apply(remove_some)
    sangnyang['formal']=sangnyang['formal'].apply(remove_some)
    jungjoong['gentle']=jungjoong['gentle'].apply(remove_some)
    total_df=pd.concat([origin, sangnyang, jungjoong], axis=1)
    total_df = total_df[total_df['user'].str.len() > 5]
    return total_df

import os
def make_total_train_df(folder_path):
    file_list=os.listdir(folder_path)
    total_formal=pd.DataFrame(columns=["formal", "random"])
    total_gentle=pd.DataFrame(columns=["gentle", "random"])
    
    for file in file_list:
        if(file[-4:]==".txt"):
            df=txt_to_train_df(os.path.join(folder_path, file))
            formal = text_pairing(df, "formal")
            gentle = text_pairing(df, "gentle")
            total_formal=pd.concat([total_formal, formal], axis=0)
            total_gentle=pd.concat([total_gentle, gentle], axis=0)

    total_formal.to_csv("formal_df.csv", index=False)
    total_formal.to_csv("gentle_df.csv", index=False)
    
    return 0

if __name__ == "__main__":
    folder_path = input("매크로로 완성한 원본, 상냥체, 정중체 txt이 들어있는 폴더 경로:")
    make_total_train_df(folder_path)