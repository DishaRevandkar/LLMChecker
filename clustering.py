import requests
from sentence_transformers import SentenceTransformer
from sklearn.cluster import AgglomerativeClustering
import numpy as np


def cluster_search_results(search_results, n_clusters=3):
    texts = [result['title'] + ' ' + result['snippet'] for result in search_results]

    model = SentenceTransformer('distilbert-base-nli-mean-tokens')
    embeddings = model.encode(texts)

    similarity_matrix = np.inner(embeddings, embeddings)

    clustering = AgglomerativeClustering(n_clusters=n_clusters, linkage='average')
    cluster_labels = clustering.fit_predict(1 - similarity_matrix)

    clustered_results = {}
    for i, label in enumerate(cluster_labels):
        if label not in clustered_results:
            clustered_results[label] = []
        clustered_results[label].append(search_results[i])

    return clustered_results


def get_page_rank(domain):
    API_KEY = ''
    api_url = 'https://openpagerank.com/api/v1.0/getPageRank'
    headers = {'API-OPR': API_KEY}
    params = {'domains[]': domain}

    try:
        response = requests.get(api_url, headers=headers, params=params)
        data = response.json()
        if 'response' in data and len(data['response']) > 0:
            return int(data['response'][0]['rank'])
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None
