from googletrans import Translator
from transformers import pipeline

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

class AI:
    def __init__(self) -> None:
        self.question_answer = pipeline('question-answering', model="timpal0l/mdeberta-v3-base-squad2")
        self.translator = Translator()
        self.summary_conf = {'l': "russian", 
                             'c': 1,
                             's': Stemmer("russian"),
                             'w': get_stop_words("russian")}
        
        self.SUMMARING = "summaring"
        self.QA = "question_answering"

    def summaring(self, text, sentences_count=1):
        parser = PlaintextParser.from_string(text, Tokenizer(self.summary_conf['l'])) 
        summarizer = LsaSummarizer(self.summary_conf['s']) 
        summarizer.stop_words = self.summary_conf['w'] 
        print(sentences_count)
        summary_sentences = []
        for sentence in summarizer(parser.document, sentences_count): 
            summary_sentences.append(str(sentence))
        
        return " ".join(summary_sentences)
    
    def classification(self, text):
        pass
    
    def question_answering(self, quest, context):
        quest = {
            "question": quest,
            "context": context
        }
        out = self.question_answer(quest)
        return out['answer']