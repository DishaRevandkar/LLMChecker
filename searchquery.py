def generate_dynamic_search_query(keywords):
    # Selects the top N important keywords
    important_keywords = sorted(keywords, key=lambda k: keywords.count(k), reverse=True)[:5]

    # Constructs query segments based on important keywords
    important_segments = [f'"{k}"' for k in important_keywords]

    final_query = ' AND '.join(important_segments)

    return final_query
