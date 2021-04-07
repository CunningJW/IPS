import re
from pymorphy2 import MorphAnalyzer
from nltk.corpus import stopwords
from tinydb import TinyDB
import pyLDAvis.gensim_models
import matplotlib.pyplot as plt
import gensim

from gensim.models.ldamulticore import LdaMulticore
import matplotlib.pyplot as plt
from multiprocessing import Process, freeze_support

def lemmatize(paragraph):
    paragraph = re.sub(patterns,' ', str(paragraph))
    tokens = []
    for token in paragraph.split():
        if token:
            token = token.strip()
            token = morph.normal_forms(token)[0]
            if token not in stopwords_en:
                tokens.append(token)
    if len(tokens) > 2:
        return tokens
    return None

def compute_coherence_values(dictionary, corpus, texts, limit, start=2, step=3):
    coherence_values = []
    model_list = []
    for num_topics in range(start, limit, step):
        model=LdaMulticore(corpus=corpus,id2word=dictionary, num_topics=num_topics)
        model_list.append(model)
        coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())
    return model_list, coherence_values


if __name__ == '__main__':
    freeze_support()
    db = TinyDB('paragraphs.json')

    patterns = "[0-9!#$%&';()*+,./:;<=>?@[\]«»^_`{|}~—\";\-·©]"
    stopwords_en = stopwords.words('english')
    morph = MorphAnalyzer()
    data_ready = []

    for item in db.all():
        data_ready.append(lemmatize([item['text']]))

    data_ready = list(filter(None, data_ready))


    id2word = gensim.corpora.Dictionary(data_ready)
    corpus = [id2word.doc2bow(text) for text in data_ready]

    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                id2word=id2word,
                                                num_topics=20,
                                                random_state=100,
                                                update_every=1,
                                                chunksize=10,
                                                passes=1,
                                                alpha='symmetric',
                                                per_word_topics=True)


    data = pyLDAvis.gensim_models.prepare(lda_model, corpus, id2word, mds='mmds')
    pyLDAvis.save_html(data, 'lda.html')

    model_list, coherence_values = compute_coherence_values(dictionary=id2word, corpus=corpus, texts=data_ready, start=2, limit=20, step=2)
    limit=20
    start=2
    step=2

    x = range(start, limit, step)
    plt.plot(x, coherence_values)
    plt.xlabel("Количество тем")
    plt.ylabel("Согласованность")
    plt.legend(("coherence_values"), loc='best')
    plt.show()
