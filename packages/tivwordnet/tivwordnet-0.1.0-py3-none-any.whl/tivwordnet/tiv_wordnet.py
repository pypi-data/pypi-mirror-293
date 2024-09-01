import os

class Word:
    def __init__(self, lemma, definition):
        self.lemma = lemma
        self.definition = definition

    def get_lemma(self):
        return self.lemma

    def get_definition(self):
        return self.definition


class TivWordNet:
    def __init__(self):
        self.synsets = {}
        self.load_data()

    def load_data(self):
        if os.path.exists('tivwordnet/data/tiv_synsets.txt'):
            with open('tivwordnet/data/tiv_synsets.txt', 'r') as file:
                for line in file:
                    parts = line.strip().split(' ', 2)
                    if len(parts) < 3:
                        continue
                    word, sense_number, definition = parts
                    self.add_synset(word, int(sense_number), definition)
        else:
            print("Data files not found. Starting with an empty database.")

    def add_synset(self, word, sense_number, definition, hypernyms=None, hyponyms=None):
        if word not in self.synsets:
            self.synsets[word] = []
        self.synsets[word].append({
            'sense_number': sense_number,
            'definition': definition,
            'hypernyms': hypernyms if hypernyms else [],
            'hyponyms': hyponyms if hyponyms else []
        })
        self.save_synsets()

    def save_synsets(self):
        with open('tivwordnet/data/tiv_synsets.txt', 'w') as file:
            for word, senses in self.synsets.items():
                for sense in senses:
                    file.write(f"{word} {sense['sense_number']} {sense['definition']}\n")

    def add_hypernym(self, word, sense_number, hypernym_word):
        if word in self.synsets:
            for sense in self.synsets[word]:
                if sense['sense_number'] == sense_number:
                    if hypernym_word not in sense['hypernyms']:
                        sense['hypernyms'].append(hypernym_word)
                        self.save_synsets()
                    return True
        return False

    def add_hyponym(self, word, sense_number, hyponym_word):
        if word in self.synsets:
            for sense in self.synsets[word]:
                if sense['sense_number'] == sense_number:
                    if hyponym_word not in sense['hyponyms']:
                        sense['hyponyms'].append(hyponym_word)
                        self.save_synsets()
                    return True
        return False

    def get_synsets(self, word):
        return [Word(word, sense['definition']) for sense in self.synsets.get(word, [])]

    def get_hypernyms(self, synset):
        return [self.get_synsets(hypernym) for hypernym in synset.get('hypernyms', [])]

    def get_hyponyms(self, synset):
        return [self.get_synsets(hyponym) for hyponym in synset.get('hyponyms', [])]

    def get_common_hypernyms(self, synset1, synset2):
        hypernyms1 = set(synset1.get('hypernyms', []))
        hypernyms2 = set(synset2.get('hypernyms', []))
        common = hypernyms1.intersection(hypernyms2)
        return common

    def get_common_hyponyms(self, synset1, synset2):
        hyponyms1 = set(synset1.get('hyponyms', []))
        hyponyms2 = set(synset2.get('hyponyms', []))
        common = hyponyms1.intersection(hyponyms2)
        return common
