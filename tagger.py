from pymorphy2 import MorphAnalyzer
from hmmtrigram import MostProbableTagSequence
from nltk import word_tokenize



class POStagger:
	def __init__(self):
		self.morph = MorphAnalyzer()
		self.mps = MostProbableTagSequence('transition_probabilities.json')
		self.end_of_sentence_markers = ['.', '!', '?', '\n']

	def parse(self, file_name):
		with open(file_name, 'r', encoding='UTF-8') as reader:
			txt_file = reader.read()
		tokenized_text = word_tokenize(txt_file)
		sentences = self.__sentence_divider(tokenized_text)
		parsed_sentences = self.__morphoanalyzer(sentences)
		most_probable_tags_sequence = self.__get_most_probable_pos_tag_sequence(parsed_sentences)
		return most_probable_tags_sequence, len(tokenized_text)

	def __sentence_divider(self, tokenized_text):
		sentences = []
		current_sentence = []
		for token in tokenized_text:
			current_sentence.append(token)
			if token in self.end_of_sentence_markers:
				sentences.append(current_sentence)
				current_sentence = []
		return sentences

	def __morphoanalyzer(self, sentences):
		parsed_sentences = []
		for sentence in sentences:
			parsed_sentence = []
			for token in sentence:
				parsed = self.morph.parse(token)
				parsed_sentence.append(parsed)
			parsed_sentences.append(parsed_sentence)
		return parsed_sentences

	def __get_most_probable_pos_tag_sequence(self, parsed_sentences):
		most_probable_tags_sequences = []
		for sentence in parsed_sentences:
			most_probable_tags_seq = self.mps.get_sequence(sentence)
			most_probable_tags_sequences.append(most_probable_tags_seq)
		return most_probable_tags_sequences


class Keywords:
	def extract(self, tagged_text, token_count, threshold=0.01, weigth_for_chunks=0.5):
		lemmas_count = {}
		keywords_in_text = []
		keylemmas_in_text = []
		for sentence in tagged_text:
			keywords_in_sentence = []
			keylemmas_in_sentence = []
			last_nominative_case = False
			for i, token in enumerate(sentence):
				if token.tag.POS == 'NOUN':
					word = token.word
					lemma = token.normal_form
					if lemma not in lemmas_count.keys():
						lemmas_count[lemma] = 0
					lemmas_count[lemma] += 1

					if token.tag.case == 'nomn':
						chain_of_words = word + ' '
						chain_of_lemmas = lemma + ' '
						n = 1
						while (i+n) < (len(sentence)):
							next = sentence[i+n]
							if next.tag.case == 'gent':
								word = next.word
								lemma = next.normal_form
								chain_of_words += word + ' '
								chain_of_lemmas += lemma + ' '
								n += 1
							else:
								chain_of_words = chain_of_words.strip()
								chain_of_lemmas = chain_of_lemmas.strip()
								keywords_in_sentence.append(chain_of_words)
								keylemmas_in_sentence.append(chain_of_lemmas)
								break
			keywords_in_text.append(keywords_in_sentence)
			keylemmas_in_text.append(keylemmas_in_sentence)

		results = self.__set_weights(keywords_in_text, keylemmas_in_text, lemmas_count, token_count, threshold, weigth_for_chunks)
		return results

	def __set_weights(self, keywords_in_text, keylemmas_in_text, lemmas_count, token_count, threshold, weigth_for_chunks):
		weighted_chunks = {}
		for i, sentence in enumerate(keywords_in_text):
			for j, chunk in enumerate(sentence):
				weighted_chunks[keywords_in_text[i][j]] = 0
				chunk_elements = chunk.split(' ')
				for element in chunk_elements:
					if element in lemmas_count.keys():
						weighted_chunks[keywords_in_text[i][j]] += lemmas_count[element]
		for k,v in weighted_chunks.items():
			n_keywords_in_chunk = len(k.split(' '))
			weighted_chunks[k] = (v / token_count) * (n_keywords_in_chunk * weigth_for_chunks)

		new_dict = {}
		for k,v in weighted_chunks.items():
			if v > threshold:
				new_dict[k] = v
		sorted_dict = {r: new_dict[r] for r in sorted(new_dict, key=new_dict.get, reverse=True)}

		return sorted_dict
