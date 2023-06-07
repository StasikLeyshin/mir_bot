# from spacy.lang.ru import Russian
# import spacy
# from spacy.symbols import ORTH, LEMMA


class text_analysis:

    def __init__(self, text):
        self.text = text.lower()
        self.score = 0

    def analysis(self):
        #nlp = spacy.load("ru_core_news_md")
        #doc = nlp(self.text)
        #print(doc)
        if len(self.text.split(' ')) == 1:
            self.score += 0.5
            #for token in doc:
                #if token.pos_ != "PART":
                    #self.score += 0.5
                #print(token.text, token.pos_, token.tag_, token.dep_, spacy.explain(token.dep_))
        return self.score
        # else:
        #     list_tokens = []
        #     for token in doc:
        #         if token.pos_ != "PART":
        #             self.score += 0.1
                #print(token.text, token.pos_, token.tag_, token.dep_, spacy.explain(token.dep_))


if __name__ == '__main__':
    text_analysis("хвхахахахпхах").analysis()

