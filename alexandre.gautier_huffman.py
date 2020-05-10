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
    Convert a string composed with 0 and 1 to int and then convert this int to char with the ASCII table.
    :param s: string: the string composed with 0 and 1
    :return: char
    """
    lS = len(s)
    sum = 0
    powTwo = 1
    i = lS - 1

    while i >= 0:
        if s[i] == '1':
            sum += powTwo
        powTwo *= 2
        i -= 1
    return chr(sum)


def __binToInt(s, i):
    """
    Convert the next 8 char of a string composed with 0 and 1 to an int
    and then convert this int to char with the ASCII table.
    :param s: string: the string composed with 0 and 1
    :param i: int: index
    :return: (char, int): the char and the index position
    """
    if len(s) >= 8:
        sum = 0
        powTwo = 1
        imax = i + 7

        while imax >= i:
            if s[imax] == '1':
                sum += powTwo
            powTwo *= 2
            imax -= 1
        return chr(sum), i + 8


def __intToBin(x):
    """
    Convert and int to a binary string of 8 char.
    :param x: int: the int to convert
    :return: string: 8 bit string
    """
    l = []
    if x != 0:  # convert the int and put each value in a list
        while x > 1:
            if x % 2 == 0:
                l.append(0)
            else:
                l.append(1)
            x //= 2
        l.append(1)

    lL = len(l)
    binString = ""  # put the right number of zeros in order to have a 8 string char at the end
    fillWithZero = 8 - lL
    while fillWithZero != 0:
        binString += '0'
        fillWithZero -= 1

    lL -= 1
    while lL >= 0:  # put each list's value in the string
        binString += str(l[lL])
        lL -= 1

    return binString  # return the final string


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
    Put all element in a heap and combine them in an huffman tree.
    :param H: (val, elt), the Heap
    :param lH: int: Heap length
    :return: bintree
    """
    if lH < 3:
        lastTuple = H.pop()
        return lastTuple[1]  # Return the last tree
    else:
        min1 = H.pop()  # pop the two tuples with min values
        min2 = H.pop()

        addMinVal = min1[0] + min2[0]
        B = bintree.BinTree(None, min2[1], min1[1])

        H.push((addMinVal, B))  # push in the heap the new combination (addMinVal, B)

        return __buildHuffmantree(H, lH-1)


def buildHuffmantree(inputList):
    """
    Processes the frequency list into a Huffman tree according to the algorithm.
    """
    H = heap.Heap()
    lL = len(inputList)
    for i in range(lL):
        B = bintree.BinTree(inputList[i][1], None, None)  # convert each char in a bintree
        H.push((inputList[i][0], B))  # push these char in a heap
    return __buildHuffmantree(H, lL + 1)


def __encodedata(huffmanTree, c, occ=""):
    """
    Take a char and return its binary value in the Huffman Tree
    :param huffmanTree: bintree
    :param c: char: char we need to convert in bin
    :param occ: string: binary string representative of c
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

        return left + right


def encodedata(huffmanTree, dataIN):
    """
    Encodes the input string to its binary string representation.
    """
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
        if count == 8:  # each time we have add 8 char to stringPart we convert them to a real char
            encodedString += __binToIntWithoutIndex(stringPart)
            stringPart = ""
            count = 0
        stringPart += dataIN[i]
        count += 1

    encodedString += __binToIntWithoutIndex(stringPart)  # add the last values

    return encodedString, 8 - count


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
    Use a binary string to find the path to a char.
    :param huffmanTree: bintree
    :param dataIN: string: binary string
    :param i: int
    :return: (char, int)
    """
    if huffmanTree.left == None and huffmanTree.right == None:
        return huffmanTree.key, i
    elif dataIN[i] == '0':
        return __decodedata(huffmanTree.left, dataIN, i+1)
    else:
        return __decodedata(huffmanTree.right, dataIN, i+1)


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
    Recreate the Huffman Tree used to decode.
    :param dataIN: string: initial string
    :param i: int: index
    :param lD: int: DataIN length
    :return: (bintree, int)
    """
    B = None
    if i < lD:
        if dataIN[i] == '1':
            c, newi = __binToInt(dataIN, i+1)
            B = bintree.BinTree(c, None, None)
            i = newi
        else:
            i+=1
            Bleft, il = __decodetree(dataIN, i, lD)
            Bright, i = __decodetree(dataIN, il, lD)

            B = bintree.BinTree(None, Bleft, Bright)

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


    last = __intToBin(ord(dataIN[lD - 1]))  # we need to take care of align for the last char
    lastStr = ""
    for j in range(align, 8):
        lastStr += last[j]

    binString += lastStr

    return binString


def decompress(data, dataAlign, tree, treeAlign):
    """
    The whole decompression process.
    """
    fromBinData = frombinary(data, dataAlign)
    fromBinTree = frombinary(tree, treeAlign)

    return decodedata(decodetree(fromBinTree), fromBinData)
