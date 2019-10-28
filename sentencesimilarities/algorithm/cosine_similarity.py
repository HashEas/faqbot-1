# Scikit Learn
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


def calculate_symmetric_score(sentence1, sentence2):

    sentences = [sentence1, sentence2]

    # Create the Document Term Matrix
    count_vectorizer = CountVectorizer(stop_words='english')
    sparse_matrix = count_vectorizer.fit_transform(sentences)

    # OPTIONAL: Convert Sparse Matrix to Pandas Dataframe if you want to see the word frequencies.
    doc_term_matrix = sparse_matrix.todense()
    df = pd.DataFrame(doc_term_matrix,
                      columns=count_vectorizer.get_feature_names(),
                      index=['sentence1', 'sentence2'])

    # Compute Cosine Similarity
    cosine_similar_val = cosine_similarity(df, df)
    sim_score  = cosine_similar_val[0][1]

    return sim_score
