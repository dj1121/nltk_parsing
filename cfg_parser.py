import nltk
import sys

# Load in text files
grammar_file_lines = open(sys.argv[1],"r").readlines()
sentences = open(sys.argv[2], "r")

# Load in the CFG to a variable
grammar = nltk.CFG.fromstring(grammar_file_lines)

# Load in parser to variable
parser = nltk.parse.EarleyChartParser(grammar)

# Tokenize each sentence and send it to the parser and output
total_num_parses = 0.0
total_num_sentences = 0.0
output = open(sys.argv[3],"w") 
for sentence in sentences:
    total_num_sentences = total_num_sentences + 1
    i = 0
    tokenized_sent = nltk.word_tokenize(sentence)
    output.write(sentence)
    for tree in parser.parse(tokenized_sent):
        output.write(str(tree))
        output.write("\n")
        i = i + 1
        total_num_parses = total_num_parses + 1
    output.write("Number of parses: " + str(i) + "\n\n")

# Output average parses
output.write("Average parses per sentence: " + str(round(total_num_parses/total_num_sentences, 3)))

# Add a newline at end so diff doesn't throw error 
output.write("\n")

sentences.close()
output.close()