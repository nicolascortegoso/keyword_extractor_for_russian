from tagger import POStagger, Keywords

tagger = POStagger()
keywords = Keywords()

filename = '#путь в текстовой файл (txt)'

tagged_text, token_count = tagger.parse(filename)
results = keywords.extract(tagged_text,
									 token_count,
									  0.01, #порог (отфильтровывает ключевые слова с более низким оценками)
									  0.5)  #вес для повышения оценк длинных ключевых слов. Экспериментируйте с этим!
print(filename, results)
