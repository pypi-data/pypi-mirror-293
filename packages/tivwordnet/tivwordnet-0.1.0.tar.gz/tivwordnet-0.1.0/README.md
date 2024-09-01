# TivWordNet

**TivWordNet** is a semantic network for the Tiv language, modeled after WordNet. It provides functionality to manage synsets, retrieve hypernyms and hyponyms, and work with definitions and lemmas. The package uses text files for data storage and supports basic operations for lexical semantic processing.

## Installation

To install TivWordNet, you can use `pip`:

```bash
pip install tivwordnet

Usage

Importing the Package
First, import the TivWordNet class from the package:


from tivwordnet import TivWordNet
Initialize TivWordNet

Create an instance of TivWordNet:
wn = TivWordNet()


Adding a Synset
To add a new synset, use the add_synset method:
wn.add_synset('tiv', 1, 'A language spoken by the Tiv people.')


Retrieving Synsets
To retrieve synsets for a word:
synsets = wn.get_synsets('tiv')

for synset in synsets:
    print(f"Lemma: {synset.get_lemma()}")
    print(f"Definition: {synset.get_definition()}")


Adding Hypernyms and Hyponyms
You can add hypernyms and hyponyms to a synset:

wn.add_hypernym('tiv', 1, 'language')
wn.add_hyponym('tiv', 1, 'Tiv language')


Retrieving Hypernyms and Hyponyms
To get hypernyms and hyponyms for a synset:

synsets = wn.get_synsets('tiv')
synset = synsets[0] if synsets else None

if synset:
    hypernyms = wn.get_hypernyms(synset)
    hyponyms = wn.get_hyponyms(synset)
    
    print("Hypernyms:")
    for hypernym_set in hypernyms:
        for word in hypernym_set:
            print(word.get_lemma())
    
    print("Hyponyms:")
    for hyponym_set in hyponyms:
        for word in hyponym_set:
            print(word.get_lemma())


Getting Common Hypernyms and Hyponyms
To find common hypernyms or hyponyms between two synsets:

synset1 = wn.get_synsets('tiv')[0] if wn.get_synsets('tiv') else None
synset2 = wn.get_synsets('language')[0] if wn.get_synsets('language') else None

if synset1 and synset2:
    common_hypernyms = wn.get_common_hypernyms(synset1, synset2)
    common_hyponyms = wn.get_common_hyponyms(synset1, synset2)
    
    print("Common Hypernyms:")
    for hypernym in common_hypernyms:
        for word in hypernym:
            print(word.get_lemma())
    
    print("Common Hyponyms:")
    for hyponym in common_hyponyms:
        for word in hyponym:
            print(word.get_lemma())

Data Files
The package uses the following text files to store data:

tivwordnet/data/tiv_synsets.txt: Contains synsets, definitions, and relations (e.g., hypernyms and hyponyms).
tivwordnet/data/tiv_definitions.txt: Contains definitions for individual words (if required for further expansion).

License
TivWordNet is distributed under the MIT License. See LICENSE for more information.

Support
For questions or issues, please open an issue on GitHub or contact support at danterkum16@gmail.com.

Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

Acknowledgements
This project is inspired by WordNet and similar lexical databases.

### Explanation

1. **Installation**: Instructions for installing the package with `pip`.
2. **Usage**: Detailed examples of how to use the package to add synsets, retrieve synsets, and get hypernyms and hyponyms.
3. **Data Files**: Information on the data files used by the package.
4. **License**: Details about the license under which the package is distributed.
5. **Support**: Information on how to get help or report issues.
6. **Contributing**: Guidelines for contributing to the project.
7. **Acknowledgements**: Credits for inspiration and sources.
