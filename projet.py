import math
from random import randint

#---Fonctions auxiliaires---

def binomial(n,k):
    """
    Fonction auxiliaire pour calculer un coefficient binomial.
    On peut voir le coefficient binomial comme :
    - au numérateur, n-k termes : n!/k! = (k+1) x (k+2) x ... x n
    - au dénominateur, n-k termes : (n-k)! = 1 x 2 x .... x (n - k)!   
    """
    
    if k == 0 or k == n:
        return 1
    elif 0 < k < n:
        num = 1
        den = 1
        for i in range(1,n-k+1):
            num = num * (k+i)
            den *= i
    
        return num//den
    else:
        return 0


def permutations(elements):
    """
    Fonction auxiliaire pour générer les permutations d'une liste d'éléments
    """
    if len(elements)<=1:
        yield elements
    else:
        for perm in permutations(elements[1:]):
            for i in range(len(elements)):
                yield perm[:i] + elements[0:1] + perm[i:]


#---Corps du sujet---
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
    
    def unrank(self, S, i):
        if (i >= self.count(len(S))):
            raise ValueError
            
    def random(self, S):
        i = randint(0, self.count(len(S)))
        return self.unrank(S, i)

        

class ConstantRule(AbstractRule):
    """
    Représente un ensemble composé d'un objet unique dont la taille
    est spécifié par la méthode degree
    """

    def degree(self):
        raise NonImplementedError
    
    def unrank(self, S, i):
        AbstractRule.unrank(self, S, i)
        return S

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
    
    def valuation(self):
        return 1
    
    def count(self, n):
        if (n == 1):
            return 1
        else:
            return 0
            
    def list(self, l):
        if len(l) != 1:
            return []
        else:
            return [self.fun(l[0])]
        
        

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
    
    def valuation(self):
        return 0
    
    def count(self, n):
        if (n == 0):
            return 1
        else:
            return 0
    
    def list(self,l):
        if len(l) != 0:
            return []
        else:
            return [self.obj()]

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

    def _calc_valuation(self):
        fst, snd = self.parameters()
        return min(self._gram[fst].valuation(), self._gram[snd].valuation())
    
    def count(self, n):
        fst,snd = self.parameters()
        return self._gram[fst].count(n) + self._gram[snd].count(n)
    
    def unrank(self, S, i):
        AbstractRule.unrank(self, S, i)
        fst,snd = self.parameters()
        a = self._gram[fst]
        b = self._gram[snd]
        if (i < a.count(len(S))):
            return a.unrank(S, i)
        else:
            return b.unrank(S, i - a.count(len(S)))

    def list(self, l):
        fst, snd = self.parameters()
        l1 = self._gram[fst].list(l)    #Liste des objets étiquetés par l dans N1
        l2 = self._gram[snd].list(l)    #Liste des objets étiquetés par l dans N2
        return l1 + l2


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
        self._valProd = 0

    def _calc_valuation(self):
        fst, snd = self.parameters()
        return self._gram[fst].valuation() + self._gram[snd].valuation()

    def construct(self, obj1, obj2):
        return self._cons(*(obj1,obj2))
    
    def iter_label(self,l,k):
        yield [],[]
        
    def list(self,l):
        objects = []
        fst, snd = self.parameters()
        fstVal = self._gram[fst].valuation()
        sndVal = self._gram[snd].valuation()
        n = len(l)
        for k in range(fstVal,n-sndVal+1):
            for left,right in self.iter_label(l,k):
                for e1 in self._gram[fst].list(left):
                    for e2 in self._gram[snd].list(right):
                        objects.append(self.construct(e1,e2))
        return objects
        
    def valProd(self, n, k):
        return 1
        
    def unrank(self, S, i):
        AbstractRule.unrank(self, S, i)
        fst,snd = self.parameters()
        s_min = 0
        s_max = 0
        r = 0
        n = len(S)
        cachingFst = [-1 for i in range(n+1)]
        cachingSnd = [-1 for i in range(n+1)]
        """
        Calcul de l'indice i tel que S_i <= r < S_i+1
        """
        while(True):
            if (s_min <= i and i < s_max):
                break
            else:
                r += 1
                S_r = 0
                for j in range(r):
                    if (cachingFst[j] == -1):
                        cachingFst[j] = self._gram[fst].count(j)
                    if (cachingSnd[n-j] == -1):
                        cachingSnd[n-j] = self._gram[snd].count(n-j)
                    S_r += self.valProd(n, j) * cachingFst[j] * cachingSnd[n-j]
                s_min = s_max
                s_max = S_r
        r = r - 1
        """
        Calcul de la répartition des étiquettes entre A et B
        """
        r2 = i - s_min
        nbSol = cachingFst[r] * cachingSnd[n-r]
        qE = r2 // nbSol
        rE = r2 % nbSol
        nG = cachingSnd[n-r]
        F,G = list(self.iter_label(S, r))[qE]
        Q = rE // nG
        R = rE % nG
        return self._cons(self._gram[fst].unrank(F, Q), self._gram[snd].unrank(G, R))


class OrdProdRule(AbstractProductRule):
    """
    Représente un ensemble produit de deux autres ensembles avec labels ordonnés
    """
    def __repr__(self):
        return "Ordered Product of " + str(self.parameters())
    
    def count(self, n):
        result = 0
        fst,snd = self.parameters()
        fstVal = self._gram[fst].valuation()    #V(N1)
        sndVal = self._gram[snd].valuation()    #V(N2)

        #On ne considère que les termes où k >= V(N1) et n-k >= V(N2) (ie k <= V(N2)-k)
        for k in range(fstVal, n-sndVal+1):
            result += self._gram[fst].count(k) * self._gram[snd].count(n-k)
        return result
    
    def valProd(self, n, k):
        return 1
    
    def iter_label(self, l, k):
        """
        Renvoie les découpages de la liste l en k éléments d'un côté et n - k de l'autre
        Pour un produit ordonné, un seul découpage pour un k donné.
        """
        if k > len(l):
            raise ValueError
        yield l[:k],l[k:]
        
class ProductRule(AbstractProductRule):
    """
    Représente un ensemble produit de deux autres ensembles
    """

    def __repr__(self):
        return "Product of " + str(self.parameters())
    
    def count(self, n):
        result = 0
        fst,snd = self.parameters()
        fstVal = self._gram[fst].valuation()    #V(N1)
        sndVal = self._gram[snd].valuation()    #V(N2)
        
        #On ne considère que les termes où k >= V(N1) et n-k >= V(N2) (ie k <= n-V(N2))
        for k in range(fstVal, n-sndVal+1):
            result += self.valProd(n,k) * self._gram[fst].count(k) * self._gram[snd].count(n-k)
        return result
    
    def valProd(self, n, k):
        return binomial(n,k)
        
    def iter_label(self,l, k):
        """
        Renvoie les découpages de la liste l en k éléments d'un côté et n - k de l'autre.
        On utilise la fonction qui génère toutes les permutations ci-dessus, on produit ensuite
        toutes les permutations d'indices possibles, on réordonne la liste initiale
        selon les indices donnés et on coupe à k.
        """
       
        #Si k est plus grand que n, on ne produit rien
        n = len(l)
        
        if k > n:
            return
        
        #On génère toutes les permutations des indices jusqu'à n
        for indices in permutations(list(range(n))):
            #On filtre les permutations non ordonnées afin d'éviter les répétitions 
            if sorted(indices[:k]) == indices[:k] and sorted(indices[k:]) == indices[k:]:
                left = indices[:k]
                right = indices[k:]
                yield [l[x] for x in left], [l[x] for x in right]
        

        
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
        fstVal = max(1, self._gram[fst].valuation())
        sndVal = self._gram[snd].valuation()
        for k in range(fstVal, n-sndVal+1):
            result += self.valProd(n,k) * self._gram[fst].count(k) * self._gram[snd].count(n-k)
        return result
        
    def iter_label(self,l,k):
        n = len(l)
        if k > n or l == [] or k == 0:
            return
    
        #On récupère l'indice de l'élément le plus petit
        mini = l.index(min(l))
    
        #On génère toutes les permutations des indices jusqu'à n privé de l'indice
        listeInit = list(range(n))
        listeInit.remove(mini)
        for indices in permutations(listeInit):
            
            #On filtre les permutations non ordonnées afin d'éviter les répétitions
            #On fait attention au k qui devient k-1 (premier élément fixé) 
            if sorted(indices[:k-1]) == indices[:k-1] and sorted(indices[k-1:]) == indices[k-1:]:
                left = indices[:k-1]
                right = indices[k-1:]
                #On n'oublie pas d'ajouter le plus petit élément à gauche
                yield [l[mini]]+[l[x] for x in left], [l[x] for x in right]
        
    def valProd(self, n, k):
        return binomial(n-1, k-1)

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

def calc_valuation(gram):
    """
    Fonction auxiliaire à init_grammar.
    
     * Prend en argument la grammaire dont on veut calculer la valuation,
     * Applique ensuite le calcul de la valuation de manière récursive en 3.1. 
     * L'algorithme termine dès que le calcul renvoie les mêmes valeurs que
       l'appel précédent.
    """
    flag = False            #Levé dès que la nouvelle val. diffère de la précédente
    
    for key in gram:        #Parcours des éléments de la grammaire
        
        #Si non-terminal :
        if isinstance(gram[key], ConstructorRule):
            val = gram[key]._calc_valuation()
            
            #Si la nouvelle valuation diffère, on lève le drapeau et on actualise
            if val != gram[key].valuation():
                flag = True
                gram[key]._valuation = val
    
    if flag:
        calc_valuation(gram)
    
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
  
        #Évaluation de V0
        for key in gram:                                
            if isinstance(gram[key], ConstructorRule):
                gram[key]._valuation = math.inf
            
        #Évaluation de V1
        for key in gram:
            if isinstance(gram[key], ConstructorRule):
                gram[key]._valuation = gram[key]._calc_valuation()
        
        #Évaluation récursive
        calc_valuation(gram)
        
        
        #Vérification que chaque non-terminal a une valuation != inf
        for key in gram:
            if (gram[key].valuation() == math.inf):
                raise NotImplementedError
        

    else:
        raise NotImplementedError