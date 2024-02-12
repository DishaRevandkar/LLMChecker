import spacy

nlp = spacy.load("en_core_web_sm")


def is_meaningful(token):
    return token.pos_ not in ['PUNCT', 'SPACE']


def extract_sentences_from_snippet(snippet):
    # Tokenizing the snippet into sentences.
    doc = nlp(snippet)

    # Extracting meaningful sentences and add missing periods
    meaningful_sentences = []
    for sent in doc.sents:
        meaningful_tokens = [token.text for token in sent if is_meaningful(token)]
        cleaned_sentence = ' '.join(meaningful_tokens).strip()

        if len(cleaned_sentence) > 10:
            meaningful_sentences.append(cleaned_sentence + '.')

    return meaningful_sentences
