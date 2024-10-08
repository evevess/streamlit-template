import gzip
import pandas as pd
import nltk
from nltk.corpus import stopwords
import langid
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from googletrans import Translator

nltk.download("stopwords")
english_stopwords = set(stopwords.words("english"))


def load_json_data() -> pd.DataFrame:
    with gzip.open(
        "customer_data/Health_and_Personal_Care.jsonl.gz", "rt", encoding="utf-8"
    ) as file:
        df = pd.read_json(file, lines=True)
    return df


def data_exploration(df: pd.DataFrame, verbose: bool = True) -> None:
    print(df.describe())
    print(f"number of null per column: {df.isnull().sum()}")
    print(f"Unique products (ASIN): {df['asin'].nunique()}")
    print(f"Verified purchases: {df['verified_purchase'].value_counts()}")


def detect_language(batch):
    return [langid.classify(text)[0] for text in batch]


def is_probably_english(text):
    words = text.lower().split()
    total_words = len(words)
    if total_words == 0:
        return False

    stopword_count = sum(1 for word in words if word in english_stopwords)
    return (stopword_count / total_words) >= 0.2 and stopword_count >= 2


def detect_language_parallel(df, batch_size=1000) -> pd.DataFrame:
    languages = ["en"] * len(df)
    futures = []
    indices_to_check = []

    with ThreadPoolExecutor() as executor:
        for start in range(0, len(df), batch_size):
            end = min(start + batch_size, len(df))
            batch_texts = df["text"].iloc[start:end].tolist()

            non_english_texts = []
            for index, text in enumerate(batch_texts):
                if not is_probably_english(text):
                    non_english_texts.append(text)
                    indices_to_check.append(start + index)

            if non_english_texts:
                futures.append(executor.submit(detect_language, non_english_texts))

        for future in as_completed(futures):
            result_languages = future.result()
            for lang, index in zip(result_languages, indices_to_check):
                languages[index] = lang
    df["languages"] = languages
    return df


def clean_text(text):
    text = re.sub(r"[^\w\s]", "", text)
    text = text.lower()
    text = " ".join([word for word in text.split() if word not in english_stopwords])
    return text


def translate_to_english(text):
    translator = Translator()
    try:
        translated = translator.translate(text, dest="en")
        return translated.text
    except Exception:
        return text


def data_preprocessing(df: pd.DataFrame) -> pd.DataFrame:
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.drop(columns=["images"])
    df = (
        df.drop_duplicates()
        .dropna(subset=["text"])
        .sort_values(by="timestamp")
        .reset_index(drop=True)
    )
    return df


def main():
    df = load_json_data()
    df = df.sample(10000).reset_index(drop=True)
    df = detect_language_parallel(df)
    df = data_preprocessing(df)
    df["translated_text"] = df.loc[df["languages"] != "en", "text"].apply(
        translate_to_english
    )
    df["cleaned_text"] = df["text"].apply(clean_text)
    df.to_csv("customer_data/processed_data.csv", index=False)


if __name__ == "__main__":
    main()
