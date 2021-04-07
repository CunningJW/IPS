import gensim
data_ready = [['cat','dog','cat'],['fox'],['goat']]
id2word = gensim.corpora.Dictionary(data_ready)
print(id2word)
