# nltk_parsing

**cfg_parser.py**
- Parser created using NLTK which parses sentences using a [context-free grammar](https://en.wikipedia.org/wiki/Context-free_grammar)
- Context-free grammar (CFG) grammar file must be in proper NTLK format (one rule per line). An example:
```
TOP -> MD _X_9
TOP -> PP _X_10
TOP -> NP PUNC
TOP -> NP VP
TOP -> NP _X_6
...
```
- Sentences must also be one per line. An example:
```
Scientists rescued a mouse immune system.
Will this work in humans?
They published their research today online.
```



**feature_parser.py**
- Parser created using NLTK which parses sentences using a [feature grammar](https://www.nltk.org/book/ch09.html)
- To invoke: ```python feature_parser.py [.fcfg grammar file] [.txt sentences file] [output path]```
- Features encode for attributes other than part of speech such as: singular, plural, etc. Features are added to CFG rules as so:
```
PropN[NUM=sg, GEND=m]-> 'John'
PropN[NUM=sg, GEND=f] -> 'Mary'
PropN[NUM=sg] -> 'Tuesday'
```
- An example parse of the sentence "The dogs bark" is below. Exact parse depends on features you define in .fcfg file:
```
(S[] (NP[NUM='pl'] (DET[] the) (N[NUM='pl'] dogs)) (VP[NUM='pl', TENSE='pres'] (IV[NUM='pl', TENSE='pres'] bark)) (PUNC[] .))
```


**cky_scratch.py**
- A from-scratch implementation of the CKY parsing algorithm
- To invoke: ```python cky_scratch.py [.cfg grammar file] [.txt sentences file] [output path]```

**cnf_converter.py**
- Takes a CFG file (as specified above in for cky_scratch.py) and converts it to [Chomsky Normal Form](https://en.wikipedia.org/wiki/Chomsky_normal_form)
- To invoke: ```python cnf_converter.py [.cfg grammar file] [output path]```
