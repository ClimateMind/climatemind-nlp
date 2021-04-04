# Load your usual SpaCy model (one of SpaCy English models)
import spacy
nlp = spacy.load('en_core_web_sm')

# load NeuralCoref and add it to the pipe of SpaCy's model
import neuralcoref
coref = neuralcoref.NeuralCoref(nlp.vocab)
nlp.add_pipe(coref, name='neuralcoref')

# You're done. You can now use NeuralCoref the same way you usually manipulate a SpaCy document and it's annotations.
doc = nlp(u'My sister has a dog. She loves him.')

print(f"doc._.has_coref: {doc._.has_coref}")
print(f"doc._.coref_clusters: {doc._.coref_clusters}")
print(f"doc._.coref_resolved: {doc._.coref_resolved}") # For the basic example, this prints: My sister has a dog. My sister loves a dog.