import math

class AbstractRule():
    """
    Classe abstraite pour tous les ensembles engendrés par une grammaire.
    """


    def __init__(self):
        """
        Méthode d'initialisation pour tous les ensembles
        """

    def valuation(self):
        return self._valuation

    def set_grammar(self, gramm):
        self._gram = gramm

    def count(self, n):
        return 0

class ConstantRule(AbstractRule):
    """
    Représente un ensemble composé d'un objet unique dont la taille
    est spécifié par la méthode degree
    """

    def degree(self):
        raise NonImplementedError



class SingletonRule(ConstantRule):
    """
    Représente un ensemble composé d'un objet unique de taille 1
    """
    def __init__(self, fun):
        """
        Input :
            - fun, la fonction qui construit l'objet depuis l'etiquette
        """
        ConstantRule.__init__(self) # initialisation de la super classe
        self._fun = fun

    def __repr__(self):
        return "Singleton"

    def fun(self, x):
        """
        Retourne l'objet unique associé à l'ensemble
        Input :
            - x, une étiquette
        """
        return self._fun(x)
    
    def count(self, n):
        if (n == 1):
            return 1
        else:
            return 0

class EpsilonRule(ConstantRule):
    """
    Représente un ensemble composé d'un objet unique de taille 0
    """
    def __init__(self, obj):
        """
        Input :
            - obj, l'objet unique appartement à l'ensemble
        """
        AbstractRule.__init__(self) # initialisation de la super classe
        self._obj = obj

    def obj(self):
        """
        Retourne l'objet unique associé à l'ensemble
        """
        return self._obj

    def __repr__(self):
        return "Epsilon " + str(self.obj())
    
    def count(self, n):
        if (n == 0):
            return 1
        else:
            return 0

class ConstructorRule(AbstractRule):
    """
    Représente un ensemble d'objets construit à partir d'autres ensembles
    """

    def __init__(self, parameters):
        """
        Input :
            - parameters, un tuple contenant les clés identifiant les ensembles nécessaires à l'ensemble construit
        """
        AbstractRule.__init__(self)  # initialisation de la super classe
        self._parameters = parameters

    def parameters(self):
        """
        Retourne les paramètres du constructeurs : les clés des ensembles nécessaires à l'ensemble construit
        """
        return self._parameters



class UnionRule(ConstructorRule):
    """
    Représente un ensemble union de deux autres ensembles
    """

    def __init__(self, key1, key2):
        """
        Input :
            - key1, la clé du premier ensemble de l'union
            - key2, la clé du second ensemble de l'union
        """
        ConstructorRule.__init__(self,(key1,key2))

    def __repr__(self):
        return "Union of " + str(self._parameters)
    
    def count(self, n):
        fst,snd = self.parameters()
        return self._gram[fst].count(n) + self._gram[snd].count(n)

class AbstractProductRule(ConstructorRule):
    """
    Représente un ensemble produit de deux autres ensembles
    """

    def __init__(self, key1, key2, cons):
        """
        Input :
            - key1, la clé du premier ensemble du produit
            - key2, la clé du second ensemble du produit
            - cons une fonction prenant deux paramètres : ``òbj1`` un objet de l'ensemble ``key1``
            et ``obj2`` un objet de l'ensemble ``key2``, et renvoyant un objet de l'ensemble produit
        """
        ConstructorRule.__init__(self,(key1,key2))
        self._cons = cons

    def construct(self, obj1, obj2):
        return self._cons(*(obj1,obj2))



class OrdProdRule(AbstractProductRule):
    """
    Représente un ensemble produit de deux autres ensembles avec labels ordonnés
    """
    def __repr__(self):
        return "Ordered Product of " + str(self.parameters())
    
    def count(self, n):
        result = 0
        fst,snd = self.parameters()
        val = self.valuation()
        for k in range(val, n+1):
            result += self._gram[fst].count(k) * self._gram[snd].count(n-k)
        return result

class ProductRule(AbstractProductRule):
    """
    Représente un ensemble produit de deux autres ensembles
    """

    def __repr__(self):
        return "Product of " + str(self.parameters())
    
    def count(self, n):
        result = 0
        fst,snd = self.parameters()
        val = self.valuation()
        for k in range(val, n+1):
            nn = math.factorial(n)
            a = math.factorial(k)
            b = math.factorial(n-k)
            result += (nn // (a*b)) * self._gram[fst].count(k) * self._gram[snd].count(n-k)
        return result
        
class BoxProdRule(AbstractProductRule):
    """
    Représente un ensemble produit de deux autres ensembles avec plus petit
    label à gauche
    """

    def __repr__(self):
        return "Boxed Product of " + str(self.parameters())
    
    def count(self, n):
        result = 0
        fst,snd = self.parameters()
        val = self.valuation() if self.valuation() > 0 else 1
        for k in range(val, n+1):
            nn = math.factorial(n-1)
            a = math.factorial(k-1)
            b = math.factorial(n-k)
            result += (nn / (a*b)) * self._gram[fst].count(k) * self._gram[snd].count(n-k)
        return result
        
        
def save_grammar(gram):
    """
    Parcourt les ensembles de la grammaires et leur associe le dictionnaire (clé, ensemble)
    qui constitue la grammaire.
    Input :
        - gram, une grammaire donnée sous forme d'un dictionnaire
    """
    for key in gram:
        gram[key].set_grammar(gram)
    return gram




def check_grammar(gram):
    """
    Retourne vrai si toutes les clés utilisées dans les ConstructorRule
    appartiennent bien au dictionnaire de la grammaire.
    """
    result = True
    for key in gram:
        if isinstance(gram[key], ConstructorRule):
            for j in gram[key]._gram:
                if (not j in gram):
                    result = False
    return result

def init_grammar(gram):
    """
     * Utilise la fonction save_grammar pour enregistrer la grammaire au
       niveau des différents ensembles
     * Vérifie la cohérence de la grammaire avec la fonction check_grammar
       (lève une exception si la fonction renvoie faux)
     * Calcul la valuation sur les ensembles de la grammaire
    Input :
        - gram, une grammaire donnée sous forme d'un dictionnaire clé - ensembles
    """
    gram = save_grammar(gram)
    if (check_grammar(gram)):
        """
            Pour les tests, à enlever quand la valuation aura été implémenté
        """
        for key in gram:
            gram[key]._valuation = 1
    else:
        raise NotImplementedError