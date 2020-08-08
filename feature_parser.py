# Devin Johnson
# Feature grammar parser with NTLK

import nltk
import sys

# Load in text files
sentences = open(sys.argv[2], "r")

# Load in the CFG to a variable
grammar = nltk.data.load(sys.argv[1])

# Load in parser to variable
parser = nltk.parse.FeatureEarleyChartParser(grammar)

# Tokenize each sentence and send it to the parser and output
total_num_parses = 0.0
total_num_sentences = 0.0
output = open(sys.argv[3],"w")

for sentence in sentences:
    total_num_sentences = total_num_sentences + 1
    i = 0
    tokenized_sent = nltk.word_tokenize(sentence)
    parses = parser.parse(tokenized_sent)
    tree_count = 0
    for x in parses:
        tree_count += 1
    if tree_count == 0:
        output.write("\n")
    else:
        x = False
        for tree in parser.parse(tokenized_sent):
            if not x:
                output.write(tree._pformat_flat("", "()", False))
                output.write("\n")
                i = i + 1
                x = True
                total_num_parses = total_num_parses + 1

# Add a newline at end so diff doesn't throw error 
output.write("\n")