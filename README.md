# proj3-anagrams
Vocabularly anagrams game for primary school English language learners (ELL)


## Overview

A simple anagram game designed for English-language learning students in 
elementary and middle school.
Students are presented with a list of vocabulary words (taken from a text file) and an anagram.  The anagram is a jumble of some number of vocabulary words, randomly chosen.  Students attempt to type vocabularly words that can be created from the jumble.  When a matching word is typed, it is added to a list of solved words. 

The vocabulary word list is fixed for one invocation of the server, so multiple students connected to the same server will see the same vocabulary list but may have different anagrams.


## Authors 

Initial version by M Young;
AJAX implementation by Solomon Zook; 


## Setup
	Clone the repository from http://github.com/solzook/proj3-anagrams

	Navigate into the newly created 'proj3-anagrams' directory

	Use 'bash ./configure' to configure the environment

	Use 'make test' to run nosetests, this isn't a required step
	
	Use 'make run' to start the server (Ctrl + C to quit) using flask's default framework

	Use 'make service' to start the server using gunicorn


## Settings
A CONFIG.py file is created during configuration, the number of words that get searched for and vocab list can be changed by editing this file
	
	Edit vocab list: change the vocab variable which starts as "data/first_grade.txt" to the filepath of the desired vocab list
		
		"third_grade.txt" and "vocab.txt" are also included in the data file
	
	Edit number of words: change the success_at_count variable, which defaults to 3, to the desired number


## Testing

'make test' runs nosetests: tests are currently implemented for vocab.py, letterbag.py, and jumble.py
