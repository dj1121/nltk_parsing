# Author: Devin Johnson
# Description: Converts a given CFG in NLTK to CNF form

import nltk
import sys

# Global to keep track of new nonterms (Xn -> ...)
x_counter = 0

# Input: nltk cfg
# Output: nltk with mixed (term/nonterm) rules replaced 
def fix_hybrid_productions(cfg):
    global x_counter

    non_hybrid = []
    hybrid = []

    # Go through all productions, decide which need to be fixed
    for production in cfg.productions():
        if production.is_nonlexical():
            non_hybrid.append(production)
        else:
            if len(production) > 1:
                hybrid.append(production)
            else:
                non_hybrid.append(production)

    while len(hybrid) > 0:
        # Go through all symbols on RHS of bad production
        bad_prod = hybrid.pop(0)
        # Incrementally build new RHS without non-terms
        new_rhs = []
        for symbol in bad_prod.rhs():
            if type(symbol) == unicode:                
                # Create new rule where new non term goes to term (_Xn_ -> term)
                nt_to_term = nltk.Production(nltk.Nonterminal("_X" + str(x_counter) + "_"), [symbol])
                new_rhs.append(nltk.Nonterminal("_X" + str(x_counter) + "_"))
                non_hybrid.append(nt_to_term)
                x_counter += 1
            else:
                new_rhs.append(symbol)

        # Replace old rhs with new and improved non-hybrid one
        to_add = nltk.Production(bad_prod.lhs(), tuple(new_rhs))
        non_hybrid.append(to_add)
    
    # Return modified cfg
    return nltk.CFG(cfg.start(), non_hybrid)
    
# Input: nltk cfg
# Output: nltk with non-cnf unit productions replaced  
def fix_unit_productions(cfg):
    # Good production doesn't mean fully CNF, it just means its not a bad unit production
    good_productions = []
    bad_productions = []
    # Go through all productions
    for i in range(0, len(cfg.productions())):
        # Check if right side is only nonterminals
        non_terms_only = True
        for symbol in cfg.productions()[i].rhs():
            if type(symbol) == unicode:
                non_terms_only = False
                break

        # If rhs is length 1 it MUST be terminal
        if len(cfg.productions()[i].rhs()) == 1 and non_terms_only:
            bad_productions.append(cfg.productions()[i])
        else:
            good_productions.append(cfg.productions()[i])

    # Follow RHS of bad productions till reaching a stable RHS (and make new rule)
    while True:
        if len(bad_productions) == 0:
            break
        # Get current bad production
        bad_prod = bad_productions.pop(0)
        # Find all productions where LHS is the first RHS symbol of our bad production
        for possible in cfg.productions():
            if possible.lhs() == bad_prod.rhs()[0]:
                # Try to make rule with bad prod LHS and find nonterm RHS
                new = nltk.Production(bad_prod.lhs(), possible.rhs())
                if type(new.rhs()[0]) == unicode or len(new) > 1:
                    good_productions.append(new)
                else:
                    bad_productions.append(new)
            
    # Return modified cfg
    return nltk.CFG(cfg.start(), good_productions)


# Input: nltk cfg
# Output: nltk with long productions replaced 
def fix_long_productions(cfg):
    global x_counter

    good_prods = []
    long_prods = []

    # Go through all productions, decide which need to be fixed
    for production in cfg.productions():
        if len(production) > 2 and production.is_nonlexical:
            long_prods.append(production)
        else:
            good_prods.append(production)
    
    
    while len(long_prods) > 0:
        long_prod = long_prods.pop(0)
        new_rhs = []
        # Iterate right to left over RHS (in groups of two)
        for i in range(len(long_prod.rhs()) - 1, -1, -2):
            # Check if you can form group of two
            if i - 2 >= -1:
                # If you have A -> ABC..., makes new rule Xn -> BC (still need to modify A->ABC... though)
                new_x = nltk.Production(nltk.Nonterminal("_X" + str(x_counter) + "_"), [long_prod.rhs()[i-1], long_prod.rhs()[i]])
                good_prods.append(new_x)
                new_rhs.insert(0, nltk.Nonterminal("_X" + str(x_counter) + "_"))
                x_counter += 1
            else:
                new_rhs.insert(0, long_prod.rhs()[i])
        
        # Add modified production to long or good accordingly
        modified_production = nltk.Production(long_prod.lhs(), tuple(new_rhs))
        if len(modified_production) > 2:
            long_prods.append(modified_production)
        else:
            good_prods.append(modified_production)

    # Return modified cfg
    return nltk.CFG(cfg.start(), good_prods)




# Input: nltk cfg (any valid form)
# Output: weakly equivalent nltk cfg in cnf form
def to_cnf(cfg):

    # CASE 1: Remove mixed rules (hybrid)
    cfg = fix_hybrid_productions(cfg)
    
    #CASE 2: If RHS length is one, it should be a terminal (unit)
    cfg = fix_unit_productions(cfg)
    
    # CASE 3: Replace long rules (more than 2 nonterms on RHS)
    cfg = fix_long_productions(cfg)

    return cfg



##### MAIN #####
# Load in CFG
cfg = nltk.data.load(sys.argv[1])

# Open output
cnf_output = open(sys.argv[2],"w") 

# Start conversion/writing to output
cnf_output.write("%start " + str(cfg.start()) + "\n")
for production in to_cnf(cfg).productions():
    cnf_output.write(str(production) + "\n")