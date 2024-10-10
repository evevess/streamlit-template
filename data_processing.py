import gzip
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import langid
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from googletrans import Translator

# Download necessary NLTK resources
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("omw-1.4")

lemmatizer = WordNetLemmatizer()
english_stopwords = set(stopwords.words("english"))
english_stopwords = {word.replace("'", "") for word in english_stopwords}
custom_stopwords = english_stopwords.union(
    {"dont", "doesnt", "arent", "cant", "wont", "isnt", "havent", "hasnt", "didnt"}
)


def load_json_data() -> pd.DataFrame:
    with gzip.open(
        "customer_data/Health_and_Personal_Care.jsonl.gz", "rt", encoding="utf-8"
    ) as file:
        df = pd.read_json(file, lines=True)
    return df


def data_exploration(df: pd.DataFrame, verbose: bool = True) -> None:
    if verbose:
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

    stopword_count = sum(1 for word in words if word in custom_stopwords)
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
    text = re.sub(r"[^\w\s]", "", text).replace("'", "")
    text = text.lower()
    # Filter out stopwords
    text = " ".join([word for word in text.split() if word not in custom_stopwords])
    return text


def lemmatize_words(text):
    words = text.split()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    return " ".join(lemmatized_words)


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


def data_processing(df: pd.DataFrame, file_name: str) -> None:
    df = df.sample(50000).reset_index(drop=True)
    df = detect_language_parallel(df)
    df = data_preprocessing(df)
    df["translated_text"] = df.loc[df["languages"] != "en", "text"].apply(
        translate_to_english
    )
    df["cleaned_text"] = df["translated_text"].fillna(df["text"]).apply(clean_text)
    df["lemmatized_text"] = df["cleaned_text"].apply(lemmatize_words)
    df.to_json(f"customer_data/{file_name}.json", orient="records", lines=False)


def main():
    df = load_json_data()
    data_exploration(df)
    df_negative = df[df["rating"] < 3]
    data_processing(df, "processed_sample_reviews")
    data_processing(df_negative, "processed_negative_reviews")


if __name__ == "__main__":
    main()
