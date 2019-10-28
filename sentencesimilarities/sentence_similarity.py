import sys
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
import sentencesimilarities.util.sentence_util as SentenceUtil
import sentencesimilarities.util.file_util as FileUtil
import sentencesimilarities.algorithm.symmetric_similarity as Symmetric_Similarity
import sentencesimilarities.algorithm.cosine_similarity as Cosine_Similarity

stem_obj = SnowballStemmer('english')
word_net_lemma = WordNetLemmatizer()
algo_type = "SS"


def get_best_suitable_question(user_question):
    best_score = 0.0
    best_sentence = ""
    for db_question in input_question_set:
        score = calculate_best_score(db_question, user_question)
        if score > best_score:
            best_score = score
            best_sentence = db_question
    print("### Best Score the algo :")
    print(best_score)
    return best_sentence, best_score


def calculate_best_score(db_question, user_question):
    symmetric_similarity_score = 0.0
    primary_sim = 0
    secondary_sim = 0
    if algo_type == "SS":
        primary_sim = Symmetric_Similarity.calculate_symmetric_score(db_question, user_question)
        secondary_sim = Symmetric_Similarity.calculate_symmetric_score(user_question, db_question)
    elif algo_type == "CS":
        primary_sim = Cosine_Similarity.calculate_symmetric_score(db_question, user_question)
        secondary_sim = Cosine_Similarity.calculate_symmetric_score(user_question, db_question)

    if primary_sim is not None and secondary_sim is not None:
        symmetric_similarity_score = (primary_sim + secondary_sim) / 2
    elif primary_sim is not None and secondary_sim is None:
        symmetric_similarity_score = primary_sim
    elif primary_sim is None and secondary_sim is not None:
        symmetric_similarity_score = secondary_sim
    return symmetric_similarity_score


def bot_start_chat():
    print("Hi Welcome to FAQ BOT !!!!\n")

    while True:
        question = input("Please ask your Question? \n")
        if question.split(" ").__len__().__le__(1):
            print("Can you please give some more details, so that i can try to answer ?")
        else:
            best_sentence, best_score = get_best_suitable_question(question)
            answer = SentenceUtil.get_the_answer(best_sentence, 'resources/FaqQuestionsAndAnswers.csv')
            if not answer:
                print("Please ask questions related to DevOps")
            else:
                print(answer)
    pass


if __name__ == '__main__':
    algo_type = sys.argv[1]
    input_question_set = FileUtil.read_questions_from_input_file("resources/FaqQuestions.txt")
    bot_start_chat()
