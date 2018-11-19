# Génération d’objets combinatoires décrit par une grammaire

Par Araye Anthony et Tan Willy

Le but de ce projet est de compter et d’engendrer l’ensemble des objets combinatoires étiqueté décrits par une grammaire. Il est ainsi possible d’engendrer une grande variété d’objets comme des ensembles, des arbres ou des mots.

## 1. Grammaires étiquetées : Introduction et quelques exemples
Dans ce projet, nous allons construire et implémenter des grammaires pour décrire des objets étiquetés.

Une grammaire décrit récursivement un ensemble d'objet, constituée d'un ensemble de règles.

Une règle de grammaire décrit un ensemble qui peut être :
- un singleton (élément atomique) (noté SingletonRule)
- un ensemble constitué d'un objet vide (noté EpsilonRule)
- l'union de deux ensembles de non-terminaux (noté UnionRule)
- une variante de produit cartésien (qui peut être ProductRule, OrdProdRule ou BoxProdRule).

On va voir ici différents exemples de grammaires. L'ensemble des grammaires est implémenté dans le fichier tests.py.

### Grammaire des séquences cycliques
```python
CycleSeq = {
    "Cycle": UnionRule("Empty","NonEmptyCycle"),
    "NonEmptyCycle": BoxProdRule("Letter","Perms", lambda l1,l2: l1+l2),
    "Perms": UnionRule("Empty","NonEmptyPerms"),
    "NonEmptyPerms": ProductRule("Letter","Perms",lambda l1,l2: l1+l2),
    "Letter": SingletonRule(lambda x:[x]),
    "Empty": EpsilonRule([])
}
```
### Grammaire des arbres binaires dont les feuilles sont étiquetées de gauche à droite
```python
SortedBinaryTree = {
    "Tree": UnionRule("Node","Leaf"),
    "Node": OrdProdRule("Tree","Tree",Node),
    "Leaf":SingletonRule(Leaf)
}
```
### Grammaire des arbres binaires croissants
```python
IncreasingBinaryTree = {
    "Tree" : UnionRule("Node", "Leaf"),
    "Node" : OrdProdRule("Label","Subtrees", lambda l,t: Node(t[0],t[1],l)),
    "Label" : SingletonRule(lambda x:x),
    "Subtrees" : ProductRule("Tree","Tree", lambda t1,t2: (t1,t2)),
    "Leaf" : EpsilonRule(Leaf())
}
```
### Grammaire des arbres binaires de recherche
```python
BinarySearchTree = {
    "Tree" : UnionRule("Node", "Leaf"),
    "Node" : OrdProdRule("Tree","RightTree", lambda left,right: Node(left,right[1],right[0])),
    "RightTree": OrdProdRule("Label", "Tree", lambda l, t: (l,t)),
    "Label" : SingletonRule(lambda x:x),
    "Leaf" : EpsilonRule(Leaf())
}
```
### Grammaire des partitions d'un ensemble
```python
Partition = {
    "Partition" : UnionRule("Empty", "Seq"),
    "Seq" : BoxProdRule("Element", "Partition", lambda l1,l2:[l1]+l2),
    "Element": UnionRule("Elt", "Empty"),
    "Elt" : BoxProdRule("Atom", "Element", lambda l1,l2:l1+l2),
    "Atom" : SingletonRule(lambda x:[x]),
    "Empty" : EpsilonRule([])
}
```
### Grammaire des séquences zig-zag
Non implémenté 

## 2. Implémentation du projet
Ce projet a été implémenté en Python (et compilé en Python3.7) et utilise au mieux l'avantage de la conception objet.

Chaque règle décrite précédemment est encapsulé dans une classe (par exemple EpsilonRule). Ces classes contiennent également un attribut pour la grammaire utilisée.

On va implémenter les méthodes suivantes :
- **calcul de valuation** d'une grammaire (permettant de verifier celle-ci)
- une méthode **count(self, n)** pour calculer le nombre d'objet de poids n
- une méthode **list(self, S)** qui calcule la liste des objets étiquetés par S
- une méthode **unrank(self, S, i)** qui calcule le i-ème élément de la liste des objets étiquetés par S (sans calculer celle-ci)
- une méthode **random(self, S)** qui choisit de manière aléatoire un élément de la liste des objets étiquetés par S.

### Calcul de la valuation 
@todo: A faire

## Pour rendre le programme plus sûr, efficace et utilisable
### Tests de cohérence génériques
Les méthodes des classes combinatoires doivent vérifier un certain nombre de propriété :
- len(self.list(S)) == self.count(len(S))
- self.unrank(S, i) appartient à self.list(S) si i appartient à [0, self.count(len(S)) - 1]
- self.random(S) appartient à self.list(S)