import spacy

# Load the medium-sized language model
nlp = spacy.load("en_core_web_md")

# Example sentences to compare
doc1 = nlp("Cat sits on the mat")
doc2 = nlp("Monkey eats banana")
doc3 = nlp("Banana is a fruit")

# Similarity between "cat" and "monkey"
print("Similarity between 'cat' and 'monkey':", doc1[0].similarity(doc2[0]))

# Similarity between "monkey" and "banana"
print("Similarity between 'monkey' and 'banana':", doc2[0].similarity(doc3[0]))

# Similarity between "cat" and "banana"
print("Similarity between 'cat' and 'banana':", doc1[0].similarity(doc3[0]))

# Similarity between entire documents
print("Similarity between doc1 and doc2:", doc1.similarity(doc2))
print("Similarity between doc2 and doc3:", doc2.similarity(doc3))
print("Similarity between doc1 and doc3:", doc1.similarity(doc3))
