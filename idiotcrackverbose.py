#!/usr/bin/python
# *-* coding: utf8 *-*

import curses
import signal

class IdiotCrackVerbose:
    

    def __init__(self, title, version, description):
        self._stdscr = curses.initscr()
        signal.signal(signal.SIGWINCH, signal.SIG_IGN) 

        curses.noecho()
        self._stdscr.keypad(True)
        curses.cbreak()

        self.settitle(title)
        self.setversion(version)
        self.setdescription(description)

    def settitle(self, title):
        self._title = title

    def setversion(self, version):
        self._version = version

    def setdescription(self, description):
        self._description = description

    def displayresume(self, number_of_combination):
        self._stdscr.clear()
        
        _, x = self._stdscr.getmaxyx()
        
        self._stdscr.addstr(0, 0, self._version)
        self._stdscr.addstr(2, x // 2  - len(self._title) // 2, self._title)
        self._stdscr.addstr(4, x // 2 - len(self._description) // 2, self._description)
        self._stdscr.refresh()
        self._stdscr.addstr(5 + 1 + len(self._description) // x, 0, str(number_of_combination) + " combinaisons possibles trouvees") 
        

        #curses.echo()
        #while self._stdscr.getstr(8, 0, 1) != 'y':
         #   pass
        self._stdscr.addstr(5 + 2 + len(self._description) // x, 0, "Pressez Enter pour continuer ou Ctrl+C pour annuler...")
        inp = self._stdscr.getch()
        
        while inp not in [curses.KEY_ENTER, 10, 13]:
            # TODO: gerer le redimmenssionnement
            inp = self._stdscr.getch()

        self._stdscr.refresh()
        
        return True

    def displayonerun(self, request_left, request_speed):
        self._stdscr.clear()
        self._stdscr.addstr(0, 0, "Requetes restantes  " + str(request_left))
        self._stdscr.addstr(1, 0, "Requete / seconde   " + str(request_speed))
        tmp = str(request_left // request_speed) if request_speed != 0 else '?' 
        self._stdscr.addstr(2, 0, "Temps restants      " + tmp)

        self._stdscr.refresh()

    def waitkey(self):
        self._stdscr.getch()

    def refresh(self):
        pass
    
    def _insertline(self, y, x, line):
        pass

    def __del__(self):
        self.close()

    def close(self):
        curses.echo()
        self._stdscr.keypad(True)
        curses.nocbreak()

        curses.endwin()


if __name__ == "__main__":
    a = IdiotCrackVerbose("Idiot Crack 1.0", "version 1.0", """\
IdiotCrack a ete concu pour tester la robustesse d'une application \
web. Presser sur Enter si vous voulez continuer ou Ctrl+C pour arreter \
le programme.
            """)
    def test():
        for i in xrange(10**7):
            pass
        return 5

    a.displayresume(test())
    a.displayonerun(45, 40)


    a.waitkey()
