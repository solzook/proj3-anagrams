# proj3-anagrams
Vocabularly anagrams game for primary school English language learners (ELL)


## Overview

A simple anagram game designed for English-language learning students in 
elementary and middle school.  
Students are presented with a list of vocabulary words (taken from a text file) 
and an anagram.  The anagram is a jumble of some number of vocabulary words, randomly chosen.  Students attempt to type vocabularly words that can be created from the  
jumble.  When a matching word is typed, it is added to a list of solved words. 

The vocabulary word list is fixed for one invocation of the server, so multiple
students connected to the same server will see the same vocabulary list but may 
have different anagrams.

## Authors 

Initial version by M Young;
AJAX implementation by Solomon Zook; 

## Status

flask_vocab.py and the template vocab.html are a 'skeleton' version 
of the anagram game for a CIS 322 project.  They uses conventional  
interaction through a form, interacting only when the user submits the form. 
Your assignment is to replace the interaction with AJAX interaction on each 
keystroke. 

## Testing

'make test' runs nosetests: tests are currently implemented for vocab.py, letterbag.py, and jumble.py
