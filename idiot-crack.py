#!/usr/bin/python
# *-* coding: utf8 *-*

import sys
import getopt
import re
from bruteforce import *
from sendform import * 
from idiotcrackverbose import IdiotCrackVerbose
from time import time
from random import shuffle

class IdiotCrack:
    """
    IdiotCrack:
        C'est la classe principale du programme qui permet de configurer
        les différentes étapes du bruteforce telles ques la liste de 
        caractères à tester ou bien la verbosité lors du lancement.

        Ceci est simplement à titre de test de sécurité d'une
        application web sur laquelle vous êtes autorisé à auditer
        dessus ou qu'elle vous appartienne.
        En aucun cas vous n'êtes autorisé à tester ce programme
        sur une application propriétaire dont vous ne possèdez pas
        les autorisations requises pour ce type d'audit.
    """

    alpha_numeric = [
str(i) for i in xrange(10)] + [chr(65 + i) for i in xrange(26)] + \
        [chr(97 + i) for i in xrange(26)]
    
    def __init__(self, target="http://127.0.0.1", symbol=alpha_numeric, extremum=(5, 6)):
        self.settarget(target)
        self.setsymbol(symbol)
        self.setextremum(extremum)
        
        self.setdico(None)
        self.stopwhen("")

        self._post_data = ""
        
        self.setverbose(False)
        
    def settarget(self, target):
        self._target = target

    def setdico(self, dico):
        self._dico = dico

    def setsymbol(self, symbol):
        self._symbol = symbol

    def setextremum(self, extremum):
        self._extremum = extremum

    def setverbose(self, verbose):
        self._verbose = verbose

    def stopwhen(self, expr):
        self._stop_when = expr

    def setpostdata(self, data):
        self._post_data = data

    def shuffle(self):
        shuffle(self._dico) if self._dico is not None else shuffle(self._symbol)

    def _run(self):
        send_data = Sendform(self._target)

        if self._dico is None:
             b = Bruteforce(self._symbol, self._extremum) 
        
        total_combination = len(self._dico) if self._dico is not None else b.numberofpossibilities()
        total_combination_fixed = total_combination
            
        if self._verbose:
            speed = 0

            idc_verbose = IdiotCrackVerbose("Idiot Crack", "version 1.0 alpha", "Programme de penetration de systemes d'authentification basiques")        
            idc_verbose.displayresume(total_combination)
            idc_verbose.initrun()       
        
        start_test_list = time()

        tmp = b.go_next() if self._dico is None else self._dico[0]
        while total_combination > 0:
            total_combination -= 1
            if self._verbose: 
                if (time() - start_test_list) > 5.0:
                    speed = int((total_combination_fixed - total_combination) / (time() - start_test_list))
                idc_verbose.displayonerun(total_combination, total_combination_fixed, speed)

            send_data.send_data(self._post_data + tmp, True)

            if re.search(self._stop_when, send_data.get_response()):
                if self._verbose:
                    idc_verbose.close()
                return tmp  
            
            tmp = b.go_next() if self._dico is None else self._dico[total_combination_fixed - total_combination]
        
        return None

    def run(self):
        return self._run() 

def help():
    """
    help:
        Fournit une liste d'arguments accompagnée 
        d'explications.
    """
    print "Liste des commandes\n"
    
    print "-h\tAffiche la liste des commandes."
    
    print "-v\tActive la verbosité du programme."
    
    print ("-t\tPermet de spécifier la cible respectant l'uri HTTP \
(pas de gestion de HTTPS).")

    print "-s\tPar défaut, le programme teste toutes les possibilités \
alpha-numériques.Pour spécifier votre propre liste de symboles, vous \
pouvez l'indiquer par cette commande."

    print "-d\tVous pouvez indiquer une liste de mots à tester \
directement sans passer par la génération de mots par liste de \
symboles."

    print "-e\tPar défaut, le programme teste toutes les possiblités \
de la liste des symboles d'une taille de 5 à 6. Pour changer cette taille \
il suffit d'écire 'min,max' en argument, avec min et max deux entiers."

    print "-r\tPar défaut, le programme s'arrête tout de suite. L'arrêt \
s'effectue par une condition regex qui est testé sur la page de \
l'application web reçue après l'envoi d'une requête."
    
    print "-g\tGénère une liste de possibilités alpha-numériques \
d'une taille comprise entre 1 et 8 inclue."
    print "--data\tSpécifie une liste de données à envoyer par la \
methode POST sous format 'token1=data1&token2='. Le dernier token \
dans l'exemple est celui dont la valeur sera généré par le programme."
    print "--rand\tMélange la liste de symboles ou le dictionnaire \
utilisé pour le bruteforce."
def main():
    """ Script """
    list_argv = dict(getopt.getopt(sys.argv[1:], "hgvt:d:s:e:r:", ["data=", "rand"])[0])
    
    # Demande de la liste des commandes
    if '-h' in list_argv or list_argv == {}:
        help()
        sys.exit()
    
    # Demande de génération des possibilités alpha-numériques

    if '-g' in list_argv:
        b = Bruteforce(IdiotCrack.alpha_numeric, (1, 8))
    
        tmp = b.go_next()
        while tmp != None:
            print tmp
            tmp = b.go_next()

        sys.exit()

    # Début du programme

    idc = IdiotCrack()

    if '-t' in list_argv:
        idc.settarget(list_argv["-t"])

    if '-v' in list_argv:
        idc.setverbose(True)

    if '-d' in list_argv:
        with open(list_argv["-d"], 'r') as dico_read_only:
            idc.setdico(dico_read_only.read().split('\n'))

    if '-s' in list_argv:
        with open(list_argv["-s"], 'r') as dico_read_only:
            idc.setsymbol(list(set(dico_read_only.read())))

    if "-e" in list_argv:
        extremum = list_argv["-e"].split(',')
        idc.setextremum((int(extremum[0]), int(extremum[1])))

    if '-r' in list_argv:
        idc.stopwhen(list_argv["-r"])

    if "--data" in list_argv:
        idc.setpostdata(list_argv["--data"])

    if "--rand" in list_argv:
        idc.shuffle()


    ## Execution du programme ##
    word_found = idc._run()
    
    if word_found is None:
        print "Aucun resultat trouve dans la liste des mots testes"
    else:
        print "Mot trouve:" + word_found

if __name__ == "__main__":
    main()

