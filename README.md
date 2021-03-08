Алгоритм поиска ключевых слов для русского языка

1. Алгоритм ищет ключевые слова в тексте.
2. Он построен на основе pymorphy2 и алгоритма для получения наиболее вероятной последовательности POS тегов в каждом предложении.
3. Алгоритм наивно полагает, что цепочки существительных - хорошие кандидаты на ключевые слова. 
4. Самым основным ключевым словом является изолированное существительное (NOUN) в именительном падеже. Пример: «издание». Это ключевое слово, состоящее из одного элемента.
5. Если за существительным в именительном падеже сразу же следуют другие слова в родительном падеже, они добавляются к существительному в именительном падеже, чтобы сформировать ключевое слово, состоящего более чем из одного элемента.
6. Все извлеченные ключевые слова взвешиваются и ранжируются в соответствии со следующими критериями:
		a. сколько раз каждый элемент ключевых слов встречается в теле текста
		b. длина ключевого слова (количество элементов)
7. Как правило, ключевые слова с высокой оценкой являются ключевыми словами 1+ елементов. Ключевые слова, состоящие из одного элемента, который редко встречается в тексте, получают более низкие оценки

Keyword search algorithm for the Russian language

1. The algorithm searches for keywords in a text.
2. It is build on top of pymorphy2 and an algorithm to get the most probable POS tag sequence in each sentence.
3. The algorithm naively presuppose that chain of nouns are good candidates for keywords.
3. It naively suppose that a chain of nouns is a good candidate for a keyword in text.
3. The most basic keyword is defined to be an isolated NOUN in the nominative case. Example: 'издание'. This is a keyword with just one element.
4. If a NOUN in nominative case is immediately followed by other words in the genitive case, they are appended to the nominative NOUN to form a chunk. Example: 'издание евангелия'. This is a keyword with n elements. 
5. All extracted keywords are weighted and ranked according to the following criteria:
		a. the number of times the elements of the keywords appear in the text body
		b. length of the keyword (number of elements)
6. High-ranked keywords tend to be a keywords consisting of 1+ elements. Lower-ranked keywords tend to be keywords of one single element that does not appear many times in the text.
