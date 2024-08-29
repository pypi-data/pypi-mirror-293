# Source YouTube

- Source YouTube à consulter : [https://www.youtube.com/watch?v=Kz6IlDCyOUY](https://www.youtube.com/watch?v=Kz6IlDCyOUY)

# Installation des Dépendences (Requirements)
> **> pip install setuptools wheel twine**

pip : **"Pip Installs Packages"** est un gestionnaire de packages pour Python. Il permet d'installer, de mettre à jour, et de désinstaller des packages Python.

Il est anoter que pip donne la possibilité d'accéder automatiquement au Python Package Index (PyPI) qui est un dépôt de logiciels Python open-source, pour trouver et installer les packages dont on a besoin.

# Construire une distribution python
> **> python setup.py sdist bdist_wheel**

Une distribution avec l'extention .whl sera générée dans le répértoire dist. L'extension .whl est utilisée pour désigner les fichiers Wheel, qui sont un format de distribution pour les packages Python. Les fichiers Wheel sont des archives compressées qui contiennent tout le nécessaire pour installer un package Python, y compris le code source et les métadonnées (comme les informations de version, les dépendances, etc.).

Le format Wheel est un standard PEP 427 dans l'écosystème Python, ce qui garantit sa compatibilité et son interopérabilité.

Il est à noter que PEP signifie **Python Enhancement Proposal** (Proposition d'Amélioration de Python). C'est un document de conception fournissant des informations ou des propositions sur les nouvelles fonctionnalités, les améliorations, ou les pratiques recommandées dans le langage Python. Les PEPs servent de moyen de communication au sein de la communauté Python et entre les développeurs principaux de Python.

Exemples de PEPs Connus :

- PEP 8 : Guide de style pour le code Python.
- PEP 20 : Les 20 principes du "Zen de Python".
- PEP 484 : Annotations de type.
- PEP 572 : Opérateur d'assignation :=.

# Installer la distribution
> **> pip install dist/pijoris-1.0-py3-none-any.whl** [--force-reinstall]

> *> pip list*


