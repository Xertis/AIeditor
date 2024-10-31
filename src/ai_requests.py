from googletrans import Translator
from transformers import pipeline

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

class AI:
    def __init__(self) -> None:
        self.summary = pipeline("summarization")
        self.question_answer = pipeline('question-answering', model="deepset/roberta-base-squad2", tokenizer="deepset/roberta-base-squad2")
        self.translator = Translator()
        self.summary_conf = {'l': "russian", 
                             'c': 3,
                             's': Stemmer("russian"),
                             'w': get_stop_words("russian")}


    def __translate__(self, text, tlang):
        translated = self.translator.translate(text=text, dest=tlang)
        return translated.text

    def summaring(self, text):
        parser = PlaintextParser.from_string(text, Tokenizer(self.summary_conf['l'])) 
        summarizer = LsaSummarizer(self.summary_conf['s']) 
        summarizer.stop_words = self.summary_conf['w'] 
        
        summary_sentences = []
        for sentence in summarizer(parser.document, self.summary_conf['c']): 
            summary_sentences.append(str(sentence))
        
        return " ".join(summary_sentences)
    
    def classification(self, text):
        pass
    
    def question_answering(self, quest, context):
        print(context)
        quest = {
            "question": self.__translate__(quest, 'en'),
            "context": self.__translate__(context, 'en')
        }
        out = self.question_answer(quest)
        return self.__translate__(out['answer'], 'ru')