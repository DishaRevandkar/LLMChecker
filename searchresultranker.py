from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import requests
from urllib.parse import urlparse

distilbert_model = SentenceTransformer('distilbert-base-nli-mean-tokens')


def calculate_semantic_similarity(snippet, original_prompt, ai_answer):
    snippet_embedding = distilbert_model.encode(snippet)
    prompt_embedding = distilbert_model.encode(original_prompt)
    answer_embedding = distilbert_model.encode(ai_answer)

    snippet_prompt_similarity = cosine_similarity([snippet_embedding], [prompt_embedding])[0][0]

    snippet_answer_similarity = cosine_similarity([snippet_embedding], [answer_embedding])[0][0]

    semantic_similarity_score = (snippet_prompt_similarity + snippet_answer_similarity) / 2

    return semantic_similarity_score


def get_page_rank(domain):
    API_KEY = ''
    api_url = 'https://openpagerank.com/api/v1.0/getPageRank'
    headers = {'API-OPR': API_KEY}
    params = {'domains[]': domain}

    try:
        response = requests.get(api_url, headers=headers, params=params)
        data = response.json()
        if 'response' in data and len(data['response']) > 0:
            return data['response'][0]['rank']
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def rank_search_results(search_results, original_prompt, ai_answer):
    ranked_results = []
    page_ranks = []

    for item in search_results['items']:
        snippet = item.get('snippet', '')
        relevance_score = calculate_semantic_similarity(snippet, original_prompt, ai_answer)
        url = item.get('link', '')
        domain = urlparse(url).netloc
        page_rank = get_page_rank(domain)


        if page_rank is not None:
            page_ranks.append(float(page_rank))

        ranked_results.append((item, relevance_score, page_rank))

    if page_ranks:
        min_page_rank = min(page_ranks)
        max_page_rank = max(page_ranks)
    else:
        min_page_rank = 0.0
        max_page_rank = 0.0

    for i, (item, relevance_score, page_rank) in enumerate(ranked_results):
        if page_rank is not None:
            try:
                normalized_page_rank = (float(page_rank) - min_page_rank) / (max_page_rank - min_page_rank) if max_page_rank != min_page_rank else 0.0
            except (TypeError, ValueError):
                normalized_page_rank = 0.0
        else:
            normalized_page_rank = 0.0

        combined_score = (0.8 * relevance_score) + (0.2 * normalized_page_rank)
        ranked_results[i] = (item, relevance_score, page_rank, combined_score)

    ranked_results.sort(key=lambda x: x[3], reverse=True)

    return ranked_results
