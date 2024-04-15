import spacy

nlp = spacy.load("en_core_web_sm")


def extract_keywords(prompt, answer):
    prompt_doc = nlp(prompt)
    answer_doc = nlp(answer)

    prompt_entities = {ent.text.lower() for ent in prompt_doc.ents}
    response_entities = {ent.text.lower() for ent in answer_doc.ents}

    prompt_nouns_adj = {token.text.lower() for token in prompt_doc if token.pos_ in ['NOUN', 'ADJ']}
    response_nouns_adj = {token.text.lower() for token in answer_doc if token.pos_ in ['NOUN', 'ADJ']}

    combined_keywords = list(prompt_entities.union(response_entities, prompt_nouns_adj, response_nouns_adj))

    return combined_keywords
