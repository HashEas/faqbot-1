from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
import nltk
import re
import DataLoader as dl

stem_obj = SnowballStemmer('english')
word_net_lemma = WordNetLemmatizer()


class myClass():
    def __init__(self, sentence_score, value):
        self.score = sentence_score
        self.value = value

    def __eq__(self, other):
        return self.score == other.score and self.value == other.value

    def __lt__(self, other):
        return self.score < other.score


def penn_to_wn(tag):
    """ Convert between a Penn Treebank tag to a simplified Wordnet tag """
    if tag.startswith('N'):
        return 'n'
    if tag.startswith('V'):
        return 'v'
    if tag.startswith('J'):
        return 'a'
    if tag.startswith('R'):
        return 'r'
    return None


def tagged_to_syn_set(word, tag):
    wn_tag = penn_to_wn(tag)
    if wn_tag is None:
        return None
    try:
        return wn.synsets(word_net_lemma.lemmatize(word), wn_tag)[0]
    except:
        # print(word,wn_tag)
        return word, wn_tag


def symmetric_sentence_similarity(sentence1, sentence2):
    # """ compute the symmetric sentence similarity using Wordnet """
    sentence_similar_score = 0.0
    primary_sim = sentence_similarity(sentence1, sentence2)
    secondary_sim = sentence_similarity(sentence2, sentence1)

    if primary_sim is not None and secondary_sim is not None:
        sentence_similar_score = (primary_sim + secondary_sim) / 2
    elif primary_sim is not None and secondary_sim is None:
        sentence_similar_score = primary_sim
    elif primary_sim is None and secondary_sim is not None:
        sentence_similar_score = secondary_sim
    return sentence_similar_score


def sentence_similarity(sentence1, sentence2):
    """ compute the sentence similarity using Wordnet """
    # Tokenize and tag
    sentence1 = pos_tag(word_tokenize(sentence1))
    # print(sentence1)
    sentence2 = pos_tag(word_tokenize(sentence2))
    # print(sentence2)
    # Get the synsets for the tagged words
    # syn_sets_1 = [tagged_to_syn_set(*tagged_word) for tagged_word in sentence1]
    # syn_sets_2 = [tagged_to_syn_set(*tagged_word) for tagged_word in sentence2]

    syn_sets_1 = []
    syn_sets_2 = []
    non_dict_set_sets_1 = []
    non_dict_set_sets_2 = []

    for tagged_word in sentence1:
        result_returned = tagged_to_syn_set(*tagged_word)
        if result_returned is not None:
            if type(result_returned) is tuple:
                non_dict_set_sets_1.append(result_returned)
            else:
                syn_sets_1.append(result_returned)

    for tagged_word in sentence2:
        result_returned = tagged_to_syn_set(*tagged_word)
        if result_returned is not None:
            if type(result_returned) is tuple:
                non_dict_set_sets_2.append(result_returned)
            else:
                syn_sets_2.append(result_returned)

    # Filter out the Nones
    syn_sets_1 = [ss for ss in syn_sets_1 if ss]
    syn_sets_2 = [ss for ss in syn_sets_2 if ss]
    synset_score, count = 0.0, 0
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
            synset_score += new_score
            count += 1
    # Average the values
    non_dict_score, sum_non_dict_score = 0.0, 0.0
    for non_dict_word_sent1, non_dict_word_pos_sent1 in non_dict_set_sets_1:
        non_dict_score_array = []
        for non_dict_word_sent2, non_dict_word_pos_sent2 in non_dict_set_sets_2:
            if non_dict_word_sent1 == non_dict_word_sent2:
                if non_dict_word_pos_sent1 == non_dict_word_pos_sent2:
                    non_dict_score_array.append(1.0)
                else:
                    non_dict_score_array.append(0.5)
        sum_non_dict_score = sum(non_dict_score_array)
        if sum_non_dict_score is not None:
            non_dict_score += sum_non_dict_score
            count += 1
    final_score = synset_score + non_dict_score
    if count > 0:
        final_score /= count
    return final_score


def read_content_from_file(file_name):
    import csv
    faq_sentences = []
    with open(file_name) as file:
        csv_reader = csv.reader(file, delimiter='\t')
        for each_line in csv_reader:
            faq_sentences.append(each_line[1])
    return faq_sentences


def calculate_similarity(print_possible_matches, question):
    best_score = 0.0
    best_sentence = ""
    score_array = []
    cat = classifier.classify(loader.get_feature_set(question=question))
    sentences = loader.get_questions(category=cat)
    sentences = read_content_from_file("resources/Single_FaQ.csv")
    print(len(sentences))
    if print_possible_matches:
        print("----Possible Matches ---")
        print("Matched Sentence , Matched Score")
    matched_sentences = []
    for sentence in sentences:
        if sentence:
            score = symmetric_sentence_similarity(sentence, question)
            score_class = myClass(score, sentence)
            score_array.append(score_class)
            if print_possible_matches:
                print("%s , %s  " % (sentence, score))
            if score > 0.6:
                print(sentence, question, score)
                matched_sent_tuple = (sentence, question, score)
                matched_sentences.append(matched_sent_tuple)
    if print_possible_matches:
        print_match_results(matched_sentences)
    return matched_sentences


def print_match_results(matched_sentences):
    print("************************************************")
    print("Best match")
    print("Asked Question, Matched Sentence , Matched Score")
    for best_sentence, question, best_score in matched_sentences:
        print("%s, %s, %s  " % (question, best_sentence, best_score))
    print("************************************************")


def print_question_answer(question, answers, best_score):
    print("************************************************")
    print("Answer for your Question")
    print("Question, Answer , Matched Score")
    print("%s, %s , %s  " % (question, answers, best_score))
    print("************************************************")


def get_questions_from_user(detailed_logging):
    print("Hi Welcome to FAQ BOT !!!!  Ctrl+C to Exit from FAQ BOT \n")
    while True:
        question = input("Please ask your Questions? \n")
        if question.split(" ").__len__().__le__(1):
            print("Can you please give some more details, so that i can try to answer")
        else:
            possible_sentences = calculate_similarity(detailed_logging, question)
            for best_sentence, question, best_score in possible_sentences:
                answer = get_the_answer_unclassified(detailed_logging, best_sentence, best_score, question)
                if not answer:
                    print("Please ask questions related to DevOps")
                else:
                    print(answer)
            if not possible_sentences:
                print("Please ask questions related to DevOps")
    pass


def get_the_answer(print_answers, best_sentence, best_score, question):
    import csv
    answers = ""
    with open('resources/Single_FaQ.csv') as csvfile:
        csv_content = csv.reader(csvfile, delimiter='\t')
        for row in csv_content:
            if row[1] == best_sentence:
                answers = row[2]
    if print_answers:
        print_question_answer(question, answers, best_score)
    return answers


def get_the_answer_unclassified(print_answers, best_sentence, best_score, question):
    import csv
    answers = ""
    with open('resources/Single_FaQ.csv') as csvfile:
        csv_content = csv.reader(csvfile, delimiter='\t')
        for row in csv_content:
            if row[1] == best_sentence:
                answers = row[2]
    if print_answers:
        print_question_answer(question, answers, best_score)
    return answers

if __name__ == '__main__':
    print(dl)
    loader = dl.DataLoader('resources/Single_FaQ.csv')
    feature_set = loader.get_feature_set()
    train_set_length = round(len(feature_set) / 2)
    train_set = feature_set[:train_set_length]
    test_set = feature_set[train_set_length:]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print('Actual Value: ' + test_set[0][1])
    print('Predicted Value: ' + classifier.classify(test_set[0][0]))
    # print("Classifier accuracy percent:",(nltk.classify.accuracy(classifier, test_set))*100)
    # print(classifier.show_most_informative_features(15))
    get_questions_from_user(True)
