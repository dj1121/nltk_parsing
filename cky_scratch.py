# Author: Devin Johnson
# From-scratch implementation of CKY parsing algorithm using NLTK

import nltk
import sys

class entry:
    def __init__(self, value, left, right):
        # List of parse table entries
        self.value = value
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

    def get_value(self):
        return self.value
    
    def get_left(self):
        return self.left

    def get_right(self):
        return self.right
    
class parse_table_box:
    def __init__(self, nonterms):
        # List of parse table entries
        self.nonterms = nonterms
    
    def add_nonterm(self, nonterm):
        self.nonterms.append(nonterm)

    def get_nonterms(self):
        return self.nonterms

    def __str__(self):
        return str(self.nonterms)
    

# Defines a cky parser to be used to parse sentences
class cky_parser:
    # Pass in the grammar that the parser will be defined upon
    def __init__(self, grammar):
        self.grammar = grammar
        self.table = []
        
    # Fill parse table
    def parse(self, sentence):
        # Represent parse table with 2d array (NxN)
        n = len(sentence)
        self.table = [[parse_table_box([]) for j in range(n+1)] for i in range(n+1)]

        # First fill in terminals
        for j in range (1, n+1):
            for production in self.grammar.productions():
                if sentence[j-1] == production.rhs()[0]:
                    terminal_entry = entry(production.rhs()[0], None, None)
                    self.table[j-1][j].add_nonterm(entry(production.lhs(), terminal_entry, None))

        # Fill in rest
        for j in range (1, n+1):
            for i in range(j-1, -1, -1):
                for k in range(i, j+1):
                    # Table [i,j] <- {A|A->BC} U {B in table[i,k]} U {C in table [k,j]}
                    left = self.table[i][k]
                    right = self.table[k][j]
                    # Try to make a production
                    for production in grammar.productions():
                        for left_nt in left.get_nonterms():
                            for right_nt in right.get_nonterms():
                                if production.rhs()[0] == left_nt.get_value() and production.rhs()[1] == right_nt.get_value():
                                    new_entry = entry(production.lhs(), left_nt, right_nt)
                                    self.table[i][j].add_nonterm(new_entry)
        
        return self.table
        
# Given a 2d array table, print parses            
def produce_tree(start):

    if start.get_left() == None and start.get_right() == None:
        return start.get_value()
    
    elif start.get_left() is not None and start.get_right() == None:
        return "(" + str(start.get_value()) + " " + produce_tree(start.get_left()) + ")"
    
    return "(" + str(start.get_value()) + " " + produce_tree(start.get_left()) + " " + produce_tree(start.get_right()) + ")"     


### MAIN PROGRAM ###
# Load in text files
sentences = open(sys.argv[2], "r")

# Load in the CFG to a variable
grammar = nltk.load(sys.argv[1])

# Load in parser to variable
parser = cky_parser(grammar)

# Tokenize each sentence and send it to the parser and output
output = open(sys.argv[3],"w") 
for sentence in sentences:
    i = 0
    # Tokenize the sentence
    tokenized_sent = nltk.word_tokenize(sentence)
    output.write(sentence)

    # Get the parse table
    parse_table = parser.parse(tokenized_sent)
    returned_string = ""

    # Get the parse tree for each S
    for j in range(0, len(parse_table[0][len(parse_table[0])-1].get_nonterms())):
        curr_entry = parse_table[0][len(parse_table[0])-1].get_nonterms()[j]

        # Make sure the entry is a start symbol
        if str(curr_entry.get_value()) == str(grammar.start()):
            # Generate tree
            returned_string += produce_tree(curr_entry)
            returned_string += "\n"
            i = i + 1
            
    # Write parse tree to output
    output.write(returned_string)
    output.write("Number of parses: " + str(i) + "\n\n")

# Add a newline at end so diff doesn't throw error 
output.write("\n")
sentences.close()
output.close()