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
        H.push((inputList[i][0], inputList[i][1]))
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
    if huffmanTree.left == None:
        if huffmanTree.Key == c:
            return occ
        else:
            res = __encodedata(huffmanTree.left, c, occ + '0')
            if res != None:
                return res
            else:
                return __encodedata(huffmanTree.righ, c, occ + '1')


def encodedata(huffmanTree, dataIN):
    """
    Encodes the input string to its binary string representation.
    """
    if huffmanTree == None:
        return None
    else:
        fullString = ""
        for c in dataIN:
            fullString += __encodedata(huffmanTree, c)

    return fullString


def encodetree(huffmanTree):
    """
    Encodes a huffman tree to its binary representation using a preOrder traversal:
        * each leaf key is encoded into its binary representation on 8 bits preceded by '1'
        * each time we go left we add a '0' to the result
    """
    # FIXME
    pass


def tobinary(dataIN):
    """
    Compresses a string containing binary code to its real binary value.
    """
    # FIXME
    pass


def compress(dataIn):
    """
    The main function that makes the whole compression process.
    """
    
    # FIXME
    pass

    
################################################################################
## DECOMPRESSION

def decodedata(huffmanTree, dataIN):
    """
    Decode a string using the corresponding huffman tree into something more readable.
    """
    # FIXME
    pass

    
def decodetree(dataIN):
    """
    Decodes a huffman tree from its binary representation:
        * a '0' means we add a new internal node and go to its left node
        * a '1' means the next 8 values are the encoded character of the current leaf         
    """
    # FIXME
    pass


def frombinary(dataIN, align):
    """
    Retrieve a string containing binary code from its real binary value (inverse of :func:`toBinary`).
    """
    # FIXME
    pass


def decompress(data, dataAlign, tree, treeAlign):
    """
    The whole decompression process.
    """
    # FIXME
    pass
