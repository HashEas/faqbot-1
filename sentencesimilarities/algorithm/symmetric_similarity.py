import sentencesimilarities.util.sentence_util as SentenceUtil


def calculate_symmetric_score(question1, question2):
    """ compute the sentence similarity using Wordnet """

    # Tokenize and tag
    sentence1 = SentenceUtil.pos_tagging(question1)
    sentence2 = SentenceUtil.pos_tagging(question2)

    # Get the synsets for the tagged words

    syn_sets_1 = [SentenceUtil.get_synsets_from_tags(*tagged_word) for tagged_word in sentence1]
    syn_sets_2 = [SentenceUtil.get_synsets_from_tags(*tagged_word) for tagged_word in sentence2]

    # Filter out the Nones
    syn_sets_1 = SentenceUtil.remove_empty_sets(syn_sets_1)
    syn_sets_2 = SentenceUtil.remove_empty_sets(syn_sets_2)

    sim_score, count = 0.0, 0
    # For each word in the first sentence
    for syn_set in syn_sets_1:
        # Get the similarity value of the most similar word in the other sentence
        best_score = [syn_set.path_similarity(ss) for ss in syn_sets_2]
        filtered_score = []

        for score_value in best_score:
            if score_value is not None:
                filtered_score.append(score_value)
                # Check that the similarity could have been computed
        new_score = 0.0
        if filtered_score:
            if filtered_score is not None:
                new_score = max(filtered_score)
        if new_score is not None:
            sim_score += new_score
            count += 1
    # Average the values
    if count > 0:
        sim_score /= count
    return sim_score
