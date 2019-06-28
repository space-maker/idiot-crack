#!/usr/bin/python
# *-* coding: utf8 *-*

import sys
import os
import getopt
import re
from bruteforce import *
from sendform import * 

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

    alpha_numeric = [str(i) for i in xrange(10)] + [chr(65 + i) for i in xrange(26)] + \
        [chr(97 + i) for i in xrange(26)]
    
    def __init__(self, target="http://127.0.0.1", dico=alpha_numeric, extremum=(5, 6)):
        self.settarget(target)
        self.setdico(dico)
        self.setextremum(extremum)
        
        self.stopwhen("")

        self._post_data = ""
        
    def settarget(self, target):
        self._target = target

    def setdico(self, dico):
        self._dico = dico

    def setextremum(self, extremum):
        self._extremum = extremum

    def setverbose(self, verbose):
        self._verbose = verbose

    def stopwhen(self, expr):
        self._stop_when = expr

    def setpostdata(self, data):
        self._post_data = data

    def run(self):
        
        # Initialisation des instances
        b = Bruteforce(self._dico, self._extremum)
        send_data = Sendform(self._target)

        tmp = b.go_next()
        while tmp != None:
            print '\033c'
            os.system("clear")
            print tmp
            send_data.send_data(self._post_data + tmp, True)
            if re.search(self._stop_when, send_data.get_response()):
                print("Success with", tmp)  
                break
            tmp = b.go_next()

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

    print "-d\tPar défaut, le programme teste toutes les possibilités \
alpha-numériques.Pour spécifier votre propre liste de symboles, vous \
pouvez l'indiquer par cette commande."

    print "-e\tPar défaut, le programme teste toutes les possiblités \
de la liste des symboles d'une taille de 5 à 6. Pour changer cette taille \
il suffit d'écire 'min,max' en argument, avec min et max deux entiers."

    print "-r\tPar défaut, le programme s'arrête tout de suite. L'arrêt \
s'effectue par une condition regex qui est testé sur la page de \
l'application web reçue après l'envoi d'une requête."

def main():
    """ Script """
    list_argv = dict(getopt.getopt(sys.argv[1:], "hvt:d:e:r:", ["data="])[0])
    
    # Demande de la liste des commandes
    if '-h' in list_argv:
        help()
        sys.exit()
    
    # Début du programme

    idc = IdiotCrack()

    if '-t' in list_argv:
        idc.settarget(list_argv["-t"])

    if '-v' in list_argv:
        idc.setverbose(True)

    if '-d' in list_argv:
        with open(list_argv["-d"], 'r') as dico_read_only:
            idc.setdico(sorted(list(set(dico_read_only.read()))))

    if "-e" in list_argv:
        extremum = list_argv["-e"].split(',')
        idc.setextremum((int(extremum[0]), int(extremum[1])))

    if '-r' in list_argv:
        idc.stopwhen(list_argv["-r"])

    idc.run()

if __name__ == "__main__":
    main()

