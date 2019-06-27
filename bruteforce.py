#!/usr/bin/python
# *-* coding: utf8 *-*

class Bruteforce:
    """
    Bruteforce:
        C'est une classe qui permet la génération de caractères
        à partir d'une liste donnée pendant l'initialisation, de
        taille comprise entre deux extremums
    """
    def __init__(self, list_of_term, extremum):
        self._list_of_term = list_of_term

        self._min = extremum[0]
        self._max = extremum[1]
        
        self._word_index = [0] * self._max

        self._word = list_of_term[0] * self._min
    
    def set_term(self, list_of_term):
        self._list_of_term = list_of_term

    def go_next(self):
        if self._word == None:
            return None

        word_tmp = self._word
        
        for i in range(0, len(self._word)):
            self._word_index[i] += 1
            
            if i == (len(self._word) - 1):
                if self._check_last_term(i):
                    if self._is_finish():
                        self._word = None
                        break
                    else:
                        self._word_index = [0] * self._max
                        self._word = self._list_of_term[0] * (len(self._word) + 1)
                        break
                else:
                    self._word = self._word[:-1] + self._list_of_term[self._word_index[i]] 
                    break

            elif i == 0:
                if self._check_last_term(i):
                    self._word_index[i] = 0
                    self._word = self._list_of_term[0] + self._word[1:]
                else:
                    self._word = self._list_of_term[self._word_index[i]] + self._word[1:]
                    break
            else:
                if self._check_last_term(i):
                    self._word_index[i] = 0
                    self._word = self._word[:i] + self._list_of_term[self._word_index[i]] + self._word[i + 1:]
                else:
                    self._word = self._word[:i] + self._list_of_term[self._word_index[i]] + self._word[i + 1:]
                    break

        return word_tmp


    def _check_last_term(self, i):
        return self._word[i] == self._list_of_term[-1]

    def _is_finish(self):
        len(self._word) == self._max and self._list_of_term[-1] * self._max == self._word 


