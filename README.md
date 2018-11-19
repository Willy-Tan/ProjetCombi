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
On peut considérer qu'une séquence cyclique correspond à une permutation dont le premier élément est fixé. Connaissant ceci, on construit donc la 
grammaire des séquences cycliques en s'inspirant de la grammaire des permutations, et en faisant bien attention à ce que le premier élément soit
fixé dans un produit cartésien boxé.

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
Pour définir la grammaire des arbres binaires dont les feuilles sont étiquetées de gauche à droite, on exploite la relation d'ordre définie sur les noeuds. Il suffit ainsi d'utiliser le produit cartésien ordonné à la règle des noeuds dans la grammaire des arbres binaires aux feuilles étiquetées pour classer les feuilles de gauche à droite.
```python
SortedBinaryTree = {
    "Tree": UnionRule("Node","Leaf"),
    "Node": OrdProdRule("Tree","Tree",Node),
    "Leaf":SingletonRule(Leaf)
}
```
### Grammaire des arbres binaires croissants
De même pour ici, on reprend la grammaire des arbres binaires croissants aux noeuds étiquetés et on applique simplement un produit cartésien ordonné sur la règle des noeuds pour obtenir le résultat voulu.
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

Chaque règle décrite précédemment est encapsulée dans une classe (par exemple EpsilonRule). Ces classes contiennent également un attribut pour la grammaire utilisée.

On va implémenter les méthodes suivantes :
- **calcul de valuation** d'une grammaire (permettant de verifier celle-ci)
- une méthode **count(self, n)** pour calculer le nombre d'objet de poids n
- une méthode **list(self, S)** qui calcule la liste des objets étiquetés par S
- une méthode **unrank(self, S, i)** qui calcule le i-ème élément de la liste des objets étiquetés par S (sans calculer celle-ci)
- une méthode **random(self, S)** qui choisit de manière aléatoire un élément de la liste des objets étiquetés par S.

### Calcul de la valuation 
Rappelons les règles de l'algorithme :
- La valuation d'un `SingletonRule` est 1 ;
- La valuation d'un `EpsilonRule` est 0 ;
- La valuation de l'union `UnionRule` des non-terminaux N1 et N2 est le minimum des valuations de N1 et de N2 ;
- La valuation d'un produit des non-terminaux N1 et N2 est la somme des valuations de N1 et de N1.
Pour calculer la valuation de la grammaire, on associe d'abord la valeur infinie à chaque non-terminal (valuation V0). Ensuite, à partir de ces valeurs initiales, on calcule une première fois en suivant les règles (valuation V1), et on réitère jusqu'à ce que la valuation VN soit égale à la valuation V(N-1). L'algorithme finit dès que cette condition est remplie.

Appliquons l'algorithme de calcul de la valuation à chaque grammaire définie, afin de calculer leur valuation.
On déroulera l'algorithme en entier pour les premières grammaires afin de montrer en extension son fonctionnement.

#### Grammaire singleton
```python
GSingl = {
    "Singl": SingletonRule(lambda x:x)
}
```

```
#Initalisation :
V("Singl") = +inf

#Première itération :
V("Singl") = 1

#Deuxième itération :
V("Singl") = 1

#V1 = V2, on s'arrête.
```

#### Grammaire Epsilon
```python
GMotVide = {
    "Empty": EpsilonRule("")
}
```

```
#Initialisation : 
V("Empty") = +inf

#Première itération :
V("Empty") = 0

#Deuxième itération :
V("Empty") = 0

#V1 = V2, on s'arrête.
```

#### Permutations de taille 2

```python
Perm2 = {
    "Perms": ProductRule("Letter","Letter", lambda a,b: [a,b]),
    "Letter": SingletonRule(lambda x:x)
}
```

```
#Initialisation :
V("Perms") = +inf
V("Letter") = +inf

#Première itération : 
V("Perms") = V("Letter") + V("Letter") = +inf
V("Letter") = 1

#Deuxième itération :
V("Perms") = V("Letter") + V("Letter") = 1 + 1 = 2
V("Letter") = 1

#Troisième itération :
V("Perms") = V("Letter") + V("Letter") = 1 + 1 = 2
V("Letter") = 1

#V2 = V3, on s'arrête.
```

#### Permutations de toute taille

```python
Perms = {
    "Perms": UnionRule("Empty","NonEmpty"),
    "NonEmpty": ProductRule("Letter","Perms",lambda l1,l2:l1+l2),
    "Letter": SingletonRule(lambda x:[x]),
    "Empty": EpsilonRule([])
}
```

```
#Initialisation :
V("Perms") = +inf
V("NonEmpty") = +inf
V("Letter") = +inf
V("Empty") = +inf

#Première itération :
V("Perms") = min(V("Empty"),V("NonEmpty")) = min(+inf,+inf) = +inf
V("NonEmpty") = V("Letter") + V("Perms") = +inf + +inf = +inf
V("Letter") = 1
V("Empty") = 0

#Deuxième itération :
V("Perms") = min(V("Empty"),V("NonEmpty")) = min(0,+inf) = 0
V("NonEmpty") = V("Letter") + V("Perms") = 1 + 0 = 1
V("Letter") = 1
V("Empty") = 0


#Troisième itération :
V("Perms") = min(V("Empty"),V("NonEmpty")) = min(0,1) = 0
V("NonEmpty") = V("Letter") + V("Perms") = 1 + 0 = 1
V("Letter") = 1
V("Empty") = 0

#V2 = V3, on s'arrête.
```

#### Séquences ordonnées 
```python
SortedSeq = {
    "Sorted": UnionRule("Empty","NonEmpty"),
    "NonEmpty": OrdProdRule("Letter","Sorted",lambda l1,l2:l1+l2),
    "Letter": SingletonRule(lambda x:[x]),
    "Empty": EpsilonRule([])
}
```

```
#[...]

V("Sorted") = 0
V("NonEmpty") = 1
V("Letter") = 1
V("Empty") = 0
```

#### Exemple Boxed product

```python
ExBoxProduct = {
    "BoxProduct": BoxProdRule("Sorted", "Sorted", lambda a,b: (a,b)),
    "Sorted": UnionRule("Empty","NonEmpty"),
    "NonEmpty": OrdProdRule("Letter","Sorted",lambda l1,l2:l1+l2),
    "Letter": SingletonRule(lambda x:[x]),
    "Empty": EpsilonRule([])
}
```

```
#[...]

V("BoxProduct") = 1 #Un BoxProdRule a une valuation d'au moins 1
V("Sorted") = 0
V("NonEmpty") = 1
V("Letter") = 1
V("Empty") = 0
```

#### Arbres binaires avec labels feuilles

```python
TreeLabelLeaves = {
    "Tree": UnionRule("Node", "Leaf"),
    "Node" : ProductRule("Tree", "Tree", Node),
    "Leaf" : SingletonRule(Leaf)
}
```

```
#[...]

V("Tree") = 1
V("Node") = 2
V("Leaf") = 1
```

#### Arbres binaires avec labels noeuds

```python
TreeLabelNodes = {
    "Tree" : UnionRule("Node", "Leaf"),
    "Node" : ProductRule("Label","Subtrees", lambda l,t: Node(t[0],t[1],l)),
    "Label" : SingletonRule(lambda x:x),
    "Subtrees" : ProductRule("Tree","Tree", lambda t1,t2: (t1,t2)),
    "Leaf" : EpsilonRule(Leaf())
}
```

```
#[...]

V("Tree") = 0
V("Node") = 1
V("Label") = 1
V("Subtree") = 0
V("Leaf") = 0
```

#### Séquences cycliques 

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

```
#[...]

V("Cycle") = 0
V("NonEmptyCycle") = 1
V("Perms") = 0
V("NonEmptyPerms") = 1
V("Letter") = 1
V("Empty") = 0
```

#### Arbres binaires dont les feuilles sont rangées de gauche à droite

```python
SortedBinaryTree = {
    "Tree": UnionRule("Node","Leaf"),
    "Node": OrdProdRule("Tree","Tree",Node),
    "Leaf":SingletonRule(Leaf)
}
```

```
#[...]

V("Tree") = 1
V("Node") = 2
V("Leaf") = 1
```

#### Arbres binaires croissants

```python
IncreasingBinaryTree = {
    "Tree" : UnionRule("Node", "Leaf"),
    "Node" : OrdProdRule("Label","Subtrees", lambda l,t: Node(t[0],t[1],l)),
    "Label" : SingletonRule(lambda x:x),
    "Subtrees" : ProductRule("Tree","Tree", lambda t1,t2: (t1,t2)),
    "Leaf" : EpsilonRule(Leaf())
}
```

```
#[...]

V("Tree") = 0
V("Node") = 1
V("Label") = 1
V("Subtree") = 0
V("Leaf") = 0
```

#### Arbres binaires de recherche

```python
BinarySearchTree = {
    "Tree" : UnionRule("Node", "Leaf"),
    "Node" : OrdProdRule("Tree","RightTree", lambda left,right: Node(left,right[1],right[0])),
    "RightTree": OrdProdRule("Label", "Tree", lambda l, t: (l,t)),
    "Label" : SingletonRule(lambda x:x),
    "Leaf" : EpsilonRule(Leaf())
}
```

```
#[...]

V("Tree") = 0
V("Node") = 1
V("RightTree") = 1
V("Label") = 1
V("Leaf") = 0
```

#### Partitions d'ensemble

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

```
#[...]
V("Partition") = 0
V("Seq") = 1			#BoxProdRule est au minimum de 1, la valeur après l'algo étant 0.
V("Element") = 0
V("Elt") = 1
V("Atom") = 1
V("Empty") = 0
```

## Pour rendre le programme plus sûr, efficace et utilisable
### Tests de cohérence génériques
Les méthodes des classes combinatoires doivent vérifier un certain nombre de propriété :
- len(self.list(S)) == self.count(len(S))
- self.unrank(S, i) appartient à self.list(S) si i appartient à [0, self.count(len(S)) - 1]
- self.random(S) appartient à self.list(S)

### Caching
Un moyen d'économiser de la compléxité est d'utiliser des tableaux où on stocke les calculs déjà effectués afin de ne pas le faire plusieurs fois. Ce phénomène de caching est présent dans :
- la méthode **unrank(self, S, i)** dans les classes dérivant AbstractProductRule
