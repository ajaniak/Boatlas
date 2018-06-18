
# Boatlas
Gazetteer produit dans le cadre du cours Python de l'Ecole Nationales des Chartes
3 personnes maximum

Il s'agira de modifier l'application Gazetteer développée pendant le cours afin de

1. Ajouter des connexions entre les lieux et les gérer
2. Ajouter la capacité de lier des articles ou des ressources bibliographiques à des lieux
3. Ajouter des tests et une documentation

Compléter l'API :
- Avec les nouvelles données
- Ajouter à la fonction de navigation API places la capacité de rechercher sur un rectangle de coordonnées latmin, latmax,longmin, longmax

(Optionnel)
- Ajoutez la capacité de chercher X kilomètres autour d'une longitude / latitude (Lien et Article sur la question)
- Ajouter une page A propos où vous décrirez l'API

## Installation
Pré-requis: Python 3 et MySQL.

### OS X
#### python 3 et MySQL
Vous devez avoir installé Python et Mysql sur votre poste. Avant l’installation de Python, vous devez installer le gestionnaire de paquets HomeBrew (équivalent apt-get sous linux)

Installation de HomeBrew Pour installer Homebrew, ouvrez le Terminal et exécutez
```shell
 /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)
 ```

Pour installer Python 3: ```shell brew install python3```

Pour lancer un environnement virtuel:  virtualenv
```shell
pip install virtualenv
```

Installation Mysql ```shell brew install mysql```

####Première utilisation

Lancez le dossier dico-proso/ dans un terminal et tapez :
virtualenv ~/.dicoproso -p python3
Cela crée un environnement virtuel dans lequel pourront être installés les packages utilisés. Pour activer cet environnement virtuel, tapez :
source ~/.dicoproso/bin/activate
Cette commande sera nécessaire à chaque fois que vous voudrez activer l'environnement virtuel pour utiliser l'application.

Dans le même terminal, tapez :
pip install -r requirements.txt
Cela installe les packages requis pour faire fonctionner l'application.

Pour lancer l'application, tapez :
python3 run.py

Utilisations ultérieures :

Lancez le terminal depuis le dossier principal et entrez :
source ~/.dicoproso/bin/activate
puis
python3 run.py
