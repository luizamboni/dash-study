import fasttext
import unidecode
import pandas as pd
import os

UPLOAD_DIRECTORY = f"{os.path.dirname(os.path.realpath(__file__))}/models/"

def normalize(text):
    text = ' '.join(text.lower().split()[0:4])
    text = unidecode.unidecode(text)
    return text

def train_fasttext(train_data_df):

    to_file_df = pd.DataFrame()
    to_file_df["line"] = train_data_df["label"] + " " + train_data_df["text"].apply(normalize)
    
    train_filename = f"{UPLOAD_DIRECTORY}/train.train"
    to_file_df.to_csv(train_filename, header=False, index=False)
    
    model = fasttext.train_supervised(input=train_filename, epoch=3, lr=0.3, wordNgrams=2)


    precision, recall, f1_score = model.test(train_filename)
    model_filename = "model.bin"
    model.save_model(f"{UPLOAD_DIRECTORY}/{model_filename}")

    return model, model_filename, precision, recall, f1_score

def load_model(path):
    return fasttext.load_model(path)
