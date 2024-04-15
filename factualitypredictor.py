from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('distilbert-base-nli-mean-tokens')


def semantic_similarity(summary, answer):
    summary_embedding = model.encode(summary)
    answer_embedding = model.encode(answer)

    similarity_score = cosine_similarity([summary_embedding], [answer_embedding])[0][0]
    return similarity_score


def predict_factuality(summary, answer, threshold=0.5):
    similarity_score = semantic_similarity(summary, answer)
    if similarity_score >= threshold:
        return "Factually Accurate"
    else:
        return "Not Factually Accurate"
