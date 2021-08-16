# from helper import *
import warnings
import nltk
from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
import string
import pandas as pd
import gensim
from gensim import corpora
import pyLDAvis.gensim

nltk.download('stopwords')
nltk.download('wordnet')

a1 = "Nowadays, everyone is talking about GPT-3 — an AI tool that has been developed \
by San Francisco-based OpenAI. Although it does not have a mind of its own, GPT-3 can \
do almost anything. I am not a technology person. I know next to nothing about artificial\
intelligence." 

a2 = "Nevertheless, I have found myself obsessing over GPT-3 over the past few weeks. \
I read about 50 articles and blog posts on GPT-3. The more I learned, the more I became \
fascinated and terrified by this new AI paradigm and technology."

a3 = "The Verge has just called GPT-3 ‘an invention that could end up defining the decade to come.’ The \
New York Times has described it “by far the most powerful language mode ever created”.\
MIT Technology Review article by W. D. Heaven called it “shockingly good — \
and completely mindless.”"

a4 = "You know a breakthrough innovation has just happened when even philosophers \
jump into the topic: Regini Rini has stated: “GPT-3 is not a mind, but it is also not \
entirely a machine. It’s something else: a statistically abstracted representation of \
the contents of millions of minds, as expressed in their writing.” David Chalmers has\
commented GPT-3’s impressive dexterousness makes it one of the most interesting and \
important AI systems ever produced."

a5 = "Let me give you an example to describe my own anxiety: I have spent at least 7 \
hours to write this article (up to now), and I have spent 20 hours reading and learning \
about GPT-3. I worked my ass off and yet I am still not impressed by the quality of what \
I have written. To be fair to me, I am writing on a topic that I know very little about \
in a second language. Still, I feel like an idiot."


class Modelbuilder():

	def __init__(self):
		self.df = pd.DataFrame([a1,a2,a3,a4,a5], columns=['text'])
		self.stop_words = set(stopwords.words('english'))
		self.punctuation = set(string.punctuation)
		self.lemmatize = WordNetLemmatizer()  

	def cleaning(self, article):
	    one = " ".join([i for i in article.lower().split() if i not in self.stop_words])
	    two = "".join(i for i in one if i not in self.punctuation)
	    three = " ".join(self.lemmatize.lemmatize(i) for i in two.split())
	    return three

	def process(self):

		text = self.df.applymap(self.cleaning)['text']
		text_list = [i.split() for i in text]

		dictionary = corpora.Dictionary(text_list)
		doc_term_matrix = [dictionary.doc2bow(doc) for doc in text_list]

		Lda = gensim.models.ldamodel.LdaModel
		ldamodel = Lda(doc_term_matrix, num_topics=10, id2word = dictionary, passes=50)

		topicData = pyLDAvis.gensim.prepare(ldamodel, doc_term_matrix, dictionary, mds='mmds')

		div_id = "pyldavis-in-org-mode"
		html = pyLDAvis.prepared_data_to_html(topicData,
                                      		template_type="simple",
                                      		visid=div_id)
		return html	


