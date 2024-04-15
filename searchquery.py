from sklearn.feature_extraction.text import TfidfVectorizer


def generate_dynamic_search_query(keywords):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([" ".join(keywords)])

    feature_names = vectorizer.get_feature_names_out()

    keyword_weights = dict(zip(feature_names, tfidf_matrix.toarray()[0]))

    sorted_keywords = sorted(keyword_weights, key=keyword_weights.get, reverse=True)

    query_segments = [f'"{k}"' for k in sorted_keywords]

    final_query = ' AND '.join(query_segments)

    return final_query

