"""
Isaiah Banta
bantaib@whitman.edu

A simple implementation of a Whitman focused Factoid Question 
Answering program.
"""

import string
import stanfordnlp as snlp
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm


# POS tagger declared here as it has a print statement that can't be stopped
nlp_pos = snlp.Pipeline(processors='tokenize,mwt,pos')

# named entity recognition loaded here
nlp_entity_recog = spacy.load("en_core_web_sm")

# list of stop words provided by nltk
stop_words = set(stopwords.words('english'))

# list of wh- words
question_signifiers = ['who', 'what', 'when', 'where', 'why', 'how', 'whose']

# list of question classifications in a hierarchy
database = {'PERSON': [],
                'NORP': [],
                'FAC': [],
                'ORG': [],
                'GPE': [],
                'LOC': [],
                'PRODUCT': [],
                'EVENT': [],
                'WORK_OF_ART': [],
                'LAW': [],
                'LANGUAGE': [],
                'DATE': [],
                'TIME': [],
                'PERCENT': [],
                'MONEY': [],
                'QUANTITY': [],
                'ORDINAL': [],
                'CARDINAL': [],
                'OTHER': []}


def find_key_words(question):
    """
    Returns a list strings of key words in the param question
    """

    # initiate word lemmatizer
    WNL = WordNetLemmatizer()

    # remove punctuation, lower caps, and tokenize
    question = question.translate(str.maketrans('', '', string.punctuation)).lower()
    
    # apply pos and tokenization
    doc = nlp_pos(question)

    # filter based on noun phrases and stop words
    key_words = []
    for sent in doc.sentences:
        for word in sent.words:
            if word.xpos == 'NNP':
                key_words.append(word.text)
                continue
            if word.text not in stop_words:
                key_words.append(word.text)
                if word.text != WNL.lemmatize(word.text):
                    key_words.append(word.text)

    return key_words


def question_classification(question):
    """
    Returns the answer type of the question as a list of strings
        I checked the course syllabus to make sure this was allowed:
        I built upon github.com/timotito/NLP-Question-Answer-System 's implementation
        of their question classification code in their processquestion() function.
    """
    
    question = question.lower()
    qtokens = word_tokenize(question)

    question_signifier = ""
    qindx = -1

    answer_type = ""

    for (indx, word) in enumerate(qtokens):
        if word in question_signifiers:
            question_signifier = word
            qindx = indx
            break

    # if no question signifiers found
    if qindx < 0:
        return 'OTHER'
    
    # if multiple question signifiers found
    if qindx > len(qtokens) - 3:
        rest = qtokens[:qindx]
    else:
        rest = qtokens[qindx+1:]
    
    answer_type = 'OTHER'
    
    # if just one then match subsets of question_signifiers list
    if question_signifier in ['who', 'whose']:
        answer_type = ['PERSON', 'NORP', 'ORG']
    if question_signifier == 'what':
        answer_type = ['NORP', 'FAC', 'ORG', 'LOC', 'PRODUCT', 'EVENT', 'WORK_OF_ART', 'LAW', 'LANGUAGE', 'DATE', 'TIME', 'QUANTITY']
    elif question_signifier == 'where':
        answer_type = ['LOC', 'GPE']
    elif question_signifier == 'when':
        answer_type = ['TIME', 'EVENT', 'DATE']
    elif question_signifier == 'how':
        if rest[0] in ["few", "little", "much", "many", "large", "big"]:
            answer_type = ['PRODUCT', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL']
        elif rest[0] in ["young", "old"]:
            answer_type = 'TIME'
        elif rest[0] == 'do':
            answer_type = ['LAW', 'PERSON']
        elif rest[0] == "long":
            if rest[1] in ["until", "till", "before"]:
                answer_type = ['TIME', 'DATE', 'QUANTITY', 'ORDINAL', 'CARDINAL']
            elif rest[1] == 'is':
                answer_type = ['NUMERIC', 'TIME', 'QUANTITY', 'ORDINAL', 'CARDINAL']
    
    return answer_type


def populate_database(raw_db):
    """
    Populates the database with sentences from raw_db txt file
    that it labels with scapy
    """

    with open(raw_db, 'r') as file:
        data = file.readlines()

    for sentence in data:
        
        entry = nlp_entity_recog(sentence)
        for ent in entry.ents:
            database[ent.label_].append(sentence)

    return


def database_lookup(question, keywords, answer_types):
    """
    Looks up sentences in our database with labels given by answer_types
    and then gives each of those sentences a score.
    """

    possible_sentences = []
    
    # doing an initial filter of the database
    for answer_type in answer_types:
        for sentence in database[answer_type]:
            for keyword in keywords:
                if keyword in sentence:
                    possible_sentences.append(sentence)
    
    # now doing a simple max keyword hueristic
    rankings = []
    kw_score = 0
    if len(possible_sentences) > 0:
        for sentence in possible_sentences:
            for keyword in keywords:
                if keyword in sentence:
                    kw_score += 1
            
            rankings.append([kw_score, sentence])
            kw_score = 0

        max_rank = max(rankings)[0]    
        # removing lower scores
        for sentence in rankings:
            if sentence[0] < max_rank:
                rankings.remove(sentence)

        # computing keyword proximity heuristic
        proximity = 0
        proximity_total = 0
        for sentence in rankings:
            tokens = nltk.word_tokenize(sentence[1])
            for word in tokens:
                if word in keywords and proximity == 0:
                    proximity += 1
                if word in keywords and proximity > 0:
                    proximity_total += proximity
                    proximity = 0
                if word not in keywords:
                    proximity += 1
                
            proximity_total /= len(keywords)
            sentence[0] = proximity_total

        min_rank = min(rankings)[0]    
        # removing higher scores (since lower is better for this heuristic)
        for sentence in rankings:
            if sentence[0] > min_rank:
                rankings.remove(sentence)
        
        answer = min(rankings)


        return answer[1]

    return ""


def get_answer(question, sentence, answer_type):
    """
    Returns the answer to the question given by sentence. 
    Prints "Could not find an answer." if database lookup returns -1
    """
    if sentence == "":
        print("Answer could not be found!")
        return
    else:
        print("The answer to question: %s is: " % question)
        answer_sent = nlp_entity_recog(sentence)
        for ans in answer_sent.ents:
            if ans.label_ in answer_type:
                print(ans.text)
    return


def main():

    populate_database("whitman.txt")

    question1 = "Who is the President of Whitman College?"
    question2 = "Where is Whitman College located?"

    # question 1
    keywords = find_key_words(question2)
    answer_type = question_classification(question2)
    sentence = database_lookup(question2, keywords, answer_type)
    get_answer(question2, sentence, answer_type)

    # question 2
    keywords = find_key_words(question1)
    answer_type = question_classification(question1)
    sentence = database_lookup(question1, keywords, answer_type)
    get_answer(question1, sentence, answer_type)
    
    return



if __name__ == '__main__':
    main()
