# idiot-crack
Un petit programme dont le but est de tester la robustesse d'un site contre les attaques de type bruteforce. Le système utilise la librairie *curl* pour réaliser des requêtes HTTP, ce qui n'est pas optimisé pour le but recherché ici. L'objectif de ce programme est purement pédagogique.
## Prérequis
Les instructions suivantes présentes une liste de prérequis et de librairies utilisées lors de l'implémentation du programme.
### Librairies
Le projet entier a été codé sur Python 2.7.16. Il faut donc vous munis de cette version de Python.
L'installation de curses est **obligatoire**.
```bash
pip install curses
```

Il faut vous munir d'un système basé sur Unix (Windows a de fortes chances de ne pas éxecuter le programme).

## Utilisation
Vous pouvez faire un test sur votre machine en localhost pour tester si le programme est fonctionnel. Lancez un serveur sur le port 80 et lancez la commande sui suit.
```bash
./idiot-crack.py -t http://127.0.0.1 -v -r "hello world !"
```
Si il n'y a pas d'erreurs Python, le programme est à priori fonctionnel.

Pour avoir davantages d'informations sur les commandes disponibles, faites `./idiot-crack -h` pour avoir une liste avec des explications pour chaque argument disponible.
