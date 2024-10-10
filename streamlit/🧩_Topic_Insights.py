import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import streamlit as st
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_json(
    "customer_data/processed_sample_reviews.json", orient="records", lines=False
)
df_negative = pd.read_json(
    "customer_data/processed_negative_reviews.json", orient="records", lines=False
)


def IDA(
    df: pd.DataFrame,
    n_topics: int,
):
    vectorizer = CountVectorizer(max_df=0.85, min_df=100, ngram_range=(2, 3))
    text_matrix = vectorizer.fit_transform(df["cleaned_text"])
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    lda.fit(text_matrix)
    return lda, vectorizer


def print_coherent_topics(model, vectorizer, top_n):
    words = vectorizer.get_feature_names_out()
    topics = {}

    for idx, topic in enumerate(model.components_):
        top_words_indices = topic.argsort()[: -top_n - 1 : -1]
        top_words = [words[i] for i in top_words_indices]
        topic = " ".join(top_words)
        key_phrase = " ".join(topic.split()[: top_n - 1])
        topics[f"Key Word {idx + 1}"] = key_phrase

    return topics


def extract_key_phrases_tfidf(
    df, column, ngram_range=(2, 3), max_features=100, ranking=10
):
    vectorizer = TfidfVectorizer(
        max_df=0.85,
        max_features=max_features,
        stop_words="english",
        ngram_range=ngram_range,
    )

    tfidf_matrix = vectorizer.fit_transform(df[column])

    feature_names = vectorizer.get_feature_names_out()

    tfidf_scores = tfidf_matrix.sum(axis=0).A1
    tfidf_ranking = Counter(dict(zip(feature_names, tfidf_scores)))

    top_phrases = tfidf_ranking.most_common(ranking)

    return top_phrases


def combine_similar_phrases(key_phrases, threshold=0.4):
    phrases, scores = zip(*key_phrases)
    vectorizer = TfidfVectorizer().fit_transform(phrases)
    vectors = vectorizer.toarray()

    cosine_sim = cosine_similarity(vectors)
    combined_phrases = {}

    combined_indices = set()

    for i, phrase in enumerate(phrases):
        if i in combined_indices:
            continue

        total_score = scores[i]
        combined_phrases[phrase] = total_score
        for j in range(i + 1, len(phrases)):
            if cosine_sim[i][j] > threshold:
                combined_phrases.pop(phrase)
                total_score += scores[j]
                combined_phrases[phrase] = total_score
                combined_indices.add(j)

    return combined_phrases


def generate_word_cloud(phrase_frequencies, title):
    wordcloud = WordCloud(
        width=800, height=400, background_color="white"
    ).generate_from_frequencies(phrase_frequencies)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(title)
    st.pyplot(plt)


def main():
    st.title("Key Phrase of All Customer Reviews")

    key_phrases = extract_key_phrases_tfidf(
        df, "cleaned_text", ngram_range=(2, 3), max_features=500, ranking=12
    )

    combined_phrases = combine_similar_phrases(key_phrases)
    header = "Word Cloud of Key Phrases"
    st.subheader(header)
    generate_word_cloud(combined_phrases, header)
    st.title("Key Phrase of Low Rating Reviews")

    key_phrases_negative = extract_key_phrases_tfidf(
        df_negative,
        "cleaned_text",
        ngram_range=(2, 3),
        max_features=100,
        ranking=5,
    )
    combined_neg_phrases = combine_similar_phrases(key_phrases_negative)
    header = "Word Cloud of Key Phrases for Rating < 3"
    st.subheader(header)
    generate_word_cloud(combined_neg_phrases, header)

    st.title("Key Phrase of Top 100 Low Rating Products Reviews")
    low_rating_counts = (
        df_negative.groupby("asin")
        .agg(
            total_count=("rating", "count"),
        )
        .reset_index()
    )
    lowest_rated_products = low_rating_counts.sort_values(
        by="total_count", ascending=False
    ).head(100)
    df_lowest_rated = df_negative[df_negative["asin"].isin(lowest_rated_products.asin)]
    key_phrases_low_rated = extract_key_phrases_tfidf(
        df_lowest_rated,
        "cleaned_text",
        ngram_range=(2, 3),
        max_features=100,
        ranking=5,
    )
    combined_low_rated_phrases = combine_similar_phrases(key_phrases_low_rated)
    header = "Word Cloud of Key Phrases for Top 100 Lower Rated Products"
    st.subheader(header)
    generate_word_cloud(combined_low_rated_phrases, header)


if __name__ == "__main__":
    main()
