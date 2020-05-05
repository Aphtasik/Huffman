__license__ = 'Junior (c) EPITA'
__docformat__ = 'reStructuredText'
__revision__ = '$Id: huffman.py 2019-04-01'

"""
Huffman homework
2019
@author: alexandre.gautier
"""

from algopy import bintree
from algopy import heap


###############################################################################
# Do not change anything above this line, except your login!
# Do not add any import

###############################################################################
## COMPRESSION


def __binToIntWithoutIndex(s):
    """
    FOnction qui prend une string faite de 0 et 1 et converti le tout
    en son equivalent en nombre et enfin sa correspondance dans la table ASCII
    :param s: string : la chaine de 0 et 1
    :return: char
    """
    lS = len(s)
    somme = 0
    powTwo = 1
    i = lS -1

    while i >= 0:
        if s[i] == '1':
            somme += powTwo
        powTwo *= 2
        i-=1
    return chr(somme)


def __binToInt(s, i):
    """
    FOnction qui prend une string faite de 0 et 1 et converti le tout
    en son equivalent en nombre et enfin sa correspondance dans la table ASCII
    :param s: string : la chaine de 0 et 1
    :return: char
    """
    if len(s)>=8:
        somme = 0
        powTwo = 1
        imax = i + 7

        while imax >= i:
            if s[imax] == '1':
                somme += powTwo
            powTwo *= 2
            imax -= 1
        return chr(somme), i+8


def __intToBin(x):
    """
    Converti un entier en un nombre binaire sur 8 bit sous forme de string
    :param x: int : l'entier a convertir
    :return: string : le code 8 bit de l'entier
    """
    l = []
    while x > 1:
        if x % 2 == 0:
            l.append(0)
        else:
            l.append(1)
        x //=2
    l.append(1)
    lL = len(l)

    binString = ""
    fillWithZero = 8 - lL
    while fillWithZero != 0:
        binString += '0'
        fillWithZero -= 1

    lL -= 1
    while lL >= 0:
        binString += str(l[lL])
        lL -= 1

    return binString


def buildfrequencylist(dataIN):
    """
    Builds a tuple list of the character frequencies in the input.
    """
    histo = []

    for elt in dataIN:
        found = False
        i = 0
        while i < len(histo) and not found:
            if histo[i][1] == elt:
                found = True
                histo[i][0] += 1
            i += 1
        if not found:
            histo.append([1, elt])

    histoChar = []
    for liste in histo:
        histoChar.append((liste[0], liste[1]))

    return histoChar


def __buildHuffmantree(H, lH):
    """
    Fonction récursive qui grâce à un heap, fusionne petit à petit
    les éléments en arbre de Huffman.
    :param H: Heap (val, elt)
    :param lH: int : Longueur du Heap
    :return: Bintree : L'arbre de Huffman correspondant
    """
    if lH < 3:
        lastTuple = H.pop()
        return lastTuple[1] #On retourne l'abre restant
    else:
        min1 = H.pop()
        min2 = H.pop()

        addMinVal = min1[0] + min2[0]
        B = bintree.BinTree(None, min2[1], min1[1]) #min1 à droite car c'est le plus petit des deux min

        H.push((addMinVal, B)) #on push la nouvelle comb

        return __buildHuffmantree(H, lH-1)


def buildHuffmantree(inputList):
    """
    Processes the frequency list into a Huffman tree according to the algorithm.
    """
    H = heap.Heap()
    lL = len(inputList)
    for i in range(lL): #creation du Heap qui va servir comme outil
        B = bintree.BinTree(inputList[i][1], None, None)
        H.push((inputList[i][0], B))
    if H.isempty():
        return bintree.BinTree(None, None, None)
    else:
        return __buildHuffmantree(H, lL + 1)


def __encodedata(huffmanTree, c, occ = ""):
    """
    Fonction recursive qui prend un caractere et renvoie son equivalent binaire dans l'arbre
    :param huffmanTree: BinTree
    :param c: char : caractere dont on cherche l'ecriture binaire
    :param occ: string : ecriture binaire de c
    :return: string
    """
    if huffmanTree.left == None and huffmanTree.right == None:
        if huffmanTree.key == c:
            return occ
        else:
            return ""
    else:
        if huffmanTree.left == None:
            left = ""
        else:
            left = __encodedata(huffmanTree.left, c, occ + '0')

        if huffmanTree.right == None:
            right = ""
        else:
            right = __encodedata(huffmanTree.right, c, occ + '1')

        return left+right


def encodedata(huffmanTree, dataIN):
    """
    Encodes the input string to its binary string representation.
    """
    fullString = "" #sinon on créé une string qu'on rempli pr chaque char
    for c in dataIN:
        fullString += __encodedata(huffmanTree, c)

    return fullString


def encodetree(huffmanTree):
    """
    Encodes a huffman tree to its binary representation using a preOrder traversal:
        * each leaf key is encoded into its binary representation on 8 bits preceded by '1'
        * each time we go left we add a '0' to the result
    """
    if huffmanTree.left == None and huffmanTree.right == None:
        return '1' + __intToBin(ord(huffmanTree.key))
    else:
        if huffmanTree.left == None:
            left = ""
        else:
            left = encodetree(huffmanTree.left)

        if huffmanTree.right == None:
            right = ""
        else:
            right = encodetree(huffmanTree.right)

        return '0' + left + right


def tobinary(dataIN):
    """
    Compresses a string containing binary code to its real binary value.
    """
    encodedString = ""
    stringPart = ""
    lD = len(dataIN)
    count = 0

    for i in range(lD):
        if count == 8:
            encodedString += __binToIntWithoutIndex(stringPart)
            stringPart = ""
            count = 0
        stringPart += dataIN[i]
        count += 1

    encodedString += __binToIntWithoutIndex(stringPart)

    return encodedString, 8-count


def compress(dataIn):
    """
    The main function that makes the whole compression process.
    """
    tree = buildHuffmantree(buildfrequencylist(dataIn))

    return tobinary(encodedata(tree, dataIn)), tobinary(encodetree(tree))

    
################################################################################
## DECOMPRESSION


def __decodedata(huffmanTree, dataIN, i):
    """
    Fonction recursive qui a partir de la string binaire trouve
    le chemin vers la feuille contenant le caratere a ecrire
    :param huffmanTree: BinTree
    :param dataIN: String : La string de binaire
    :param i: int
    :return: charF
    """
    if huffmanTree.left == None and huffmanTree.right == None:
        return huffmanTree.key, i
    elif dataIN[i] == '0':
        return __decodedata(huffmanTree.left, dataIN, i+1)
    else:
        return  __decodedata(huffmanTree.right, dataIN, i+1)


def decodedata(huffmanTree, dataIN):
    """
    Decode a string using the corresponding huffman tree into something more readable.
    """
    lD = len(dataIN)
    totalString = ""
    i = 0

    while i < lD:
        c, i = __decodedata(huffmanTree, dataIN, i)
        totalString += c

    return totalString

    
def __decodetree(dataIN, i, lD):
    """
    Fonction recursive qui créé l'abre a partir de la string de départ.
    :param dataIN: string : string de départ
    :param i: int : l'indexe
    :param lD: int : longueur de dataIN
    :return: BinTree, int : le bintree entrain d'être créé et l'indexe courant
    """
    B = None
    if i < lD:
        if dataIN[i] == '1':
            c, newi = __binToInt(dataIN, i+1)
            B = bintree.BinTree(c , None, None) #feuille dont la clef est le char
            i = newi
        else:
            i+=1
            Bl, il = __decodetree(dataIN, i, lD)
            Br, i = __decodetree(dataIN, il, lD)

            B = bintree.BinTree(None, Bl, Br)

    return B, i


def decodetree(dataIN):
    """
    Decodes a huffman tree from its binary representation:
        * a '0' means we add a new internal node and go to its left node
        * a '1' means the next 8 values are the encoded character of the current leaf
    """
    tree, i = __decodetree(dataIN, 0, len(dataIN))
    return tree


def frombinary(dataIN, align):
    """
    Retrieve a string containing binary code from its real binary value (inverse of :func:`toBinary`).
    """
    lD = len(dataIN)
    binString = ""

    for i in range(lD - 1):
        binString += __intToBin(ord(dataIN[i]))

    if ord(dataIN[lD - 1]) != 0:
        last = __intToBin(ord(dataIN[lD - 1]))
        lastStr = ""

        for j in range(align, 8):
            lastStr += last[j]

        binString += lastStr
    else:
        binString += '0'

    return binString


def decompress(data, dataAlign, tree, treeAlign):
    """
    The whole decompression process.
    """
    fromBinData = frombinary(data, dataAlign)
    fromBinTree = frombinary(tree, treeAlign)

    return decodedata(decodetree(fromBinTree), fromBinData)
