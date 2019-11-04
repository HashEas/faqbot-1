from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
import re

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
        return None

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
    print(sentence1)
    sentence2 = pos_tag(word_tokenize(sentence2))
    print(sentence2)
    # Get the synsets for the tagged words
    syn_sets_1 = [tagged_to_syn_set(*tagged_word) for tagged_word in sentence1]
    syn_sets_2 = [tagged_to_syn_set(*tagged_word) for tagged_word in sentence2]
    # Filter out the Nones
    syn_sets_1 = [ss for ss in syn_sets_1 if ss]
    syn_sets_2 = [ss for ss in syn_sets_2 if ss]
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

def read_content_from_file(file_name):
    file = open(file_name, "r")
    doc_list = [line for line in file]
    doc_str = ''.join(doc_list)
    faq_sentences = re.split(r'[\n\r.!?]', doc_str)
    return faq_sentences

def calculate_similarity(print_possible_matches, question):
    best_score = 0.0
    best_sentence = ""
    score_array = []
    if print_possible_matches:
        print("----Possible Matches ---")
        print("Matched Sentence , Matched Score")
    for sentence in sentences:
        if sentence:
            score = symmetric_sentence_similarity(sentence, question)
            score_class = myClass(score, sentence)
            score_array.append(score_class)
            if print_possible_matches:
                print("%s , %s  " % (sentence, score))
            if score > best_score:
                best_score = score
                best_sentence = sentence
    if print_possible_matches:
        print_match_results(question, best_sentence, best_score)
    return best_sentence, best_score

def print_match_results(question, best_sentence, best_score):
    print("************************************************")
    print("Best match")
    print("Asked Question, Matched Sentence , Matched Score")
    print("%s, %s , %s  " % (question, best_sentence, best_score))
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
            best_sentence, best_score = calculate_similarity(detailed_logging, question)
            answer = get_the_answer(detailed_logging, best_sentence, best_score, question)
            if not answer:
                print("Please ask questions related to DevOps")
            else:
                print(answer)
    pass

def get_the_answer(print_answers, best_sentence, best_score, question):
    import csv
    answers = ""
    with open('resources/FaqQuestionsAndAnswers.csv') as csvfile:
        csv_content = csv.reader(csvfile, delimiter=',')
        for row in csv_content:
            if row[0] == best_sentence:
                answers = row[1]
    if print_answers:
        print_question_answer(question, answers, best_score)
    return answers

if __name__ == '__main__':
    # sentences = read_content_from_file("resources/FaqQuestions.txt")
    # get_questions_from_user(True)