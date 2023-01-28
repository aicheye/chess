import pygame
import random
import time

# dictionaries - used for functions
pieceDict = {"P" : 1, "N" : 2, "B" : 3, "R" : 4, "Q" : 5, "K" : 6}
reversePieceDict = {0 : ".", 1 : "P", 2 : "N", 3 : "B", 4 : "R", 5 : "Q", 6 : "K", 7 : ".",
                    "0" : ".", "1" : "P", "2" : "N", "3" : "B", "4" : "R", "5" : "Q", "6" : "K", "7" : "."}
fileDict = {"a" : 0, "b" : 1, "c" : 2, "d" : 3, "e" : 4, "f" : 5, "g" : 6, "h" : 7}
reverseFileDict = ["a", "b", "c", "d", "e", "f", "g", "h"]


# clears board to empty - used for some functions
def clearBoard() :
    return [[30, 30, 30, 30, 30, 30, 30, 30],
            [30, 30, 30, 30, 30, 30, 30, 30],
            [30, 30, 30, 30, 30, 30, 30, 30],
            [30, 30, 30, 30, 30, 30, 30, 30],
            [30, 30, 30, 30, 30, 30, 30, 30],
            [30, 30, 30, 30, 30, 30, 30, 30],
            [30, 30, 30, 30, 30, 30, 30, 30],
            [30, 30, 30, 30, 30, 30, 30, 30]]


# resets board to starting position
def startBoard() :
    return [[14, 12, 13, 15, 16, 13, 12, 14],
            [11, 11, 11, 11, 11, 11, 11, 11],
            [30, 30, 30, 30, 30, 30, 30, 30],
            [30, 30, 30, 30, 30, 30, 30, 30],
            [30, 30, 30, 30, 30, 30, 30, 30],
            [30, 30, 30, 30, 30, 30, 30, 30],
            [21, 21, 21, 21, 21, 21, 21, 21],
            [24, 22, 23, 25, 26, 23, 22, 24]]


# function to parse fen codes - used to load positions
def parseFEN(fenString, posOnly=True) :
    # these are variables for all the FEN fields
    position = clearBoard()
    indexed = fenString.split()
    placements = indexed[0].split("/")
    canCastle = [[False, False], [False, False]]
    halfmove = int(indexed[4])
    fullmove = int(indexed[5])
    scrolling = True
    rankFen = 7
    rank = 0
    # iterates through the FEN placement notation to construct a board
    while scrolling :
        file = 0
        increment = 0
        placing = True
        while placing :
            if placements[rankFen][increment].upper() not in pieceDict :
                file += int(placements[rankFen][increment])
            elif placements[rankFen][increment].isupper() :
                position[rank][file] = pieceDict[placements[rankFen][increment]] + 10
                file += 1
            else :
                position[rank][file] = pieceDict[placements[rankFen][increment].upper()] + 20
                file += 1
            if file == 8 :
                placing = False
            else :
                increment += 1
        if rank == 7 :
            scrolling = False
        else :
            rankFen -= 1
            rank += 1
    if indexed[1] == "w" :
        colour = 10
    else :
        colour = 20
    # canCastle[0][1]: white king side, [0][1]: white queen side, [1][0]: black king side, [1][1]: black queen side
    if "K" in indexed[2] :
        canCastle[0][0] = True
    if "Q" in indexed[2] :
        canCastle[0][1] = True
    if "k" in indexed[2] :
        canCastle[1][0] = True
    if "q" in indexed[2] :
        canCastle[1][1] = True
    if indexed[3] != "-" :
        if int(indexed[3][1]) - 1 == 5 :
            position[int(indexed[3][1]) - 1][fileDict[indexed[3][0]]] = 27
        else :
            position[int(indexed[3][1]) - 1][fileDict[indexed[3][0]]] = 17
    if posOnly :
        return position
    else :
        return {"position" : position, "colour" : colour, "canCastle" : canCastle, "halfmove" : halfmove,
                "fullmove" : fullmove}


def encodeFEN(position, colour, canCastle, halfmove, fullmove) :
    fenString = ""
    enPassant = " -"
    blanks = 0
    for rank in reversed(range(8)) :
        for file in range(8) :
            if position[rank][file] == 30 :
                blanks += 1
            elif str(position[rank][file])[0] == "1" :
                if position[rank][file] != 17 :
                    if blanks > 0 :
                        fenString += str(blanks)
                        fenString += reversePieceDict[str(position[rank][file])[1]]
                    else :
                        fenString += reversePieceDict[str(position[rank][file])[1]]
                else :
                    enPassant = " " + reverseFileDict[file] + str(rank + 1)
                blanks = 0
            elif str(position[rank][file])[0] == "2" :
                if position[rank][file] != 27 :
                    if blanks > 0 :
                        fenString += str(blanks)
                        fenString += reversePieceDict[str(position[rank][file])[1]].lower()
                    else :
                        fenString += reversePieceDict[str(position[rank][file])[1]].lower()
                else :
                    enPassant = " " + reverseFileDict[file] + str(rank + 1)
                blanks = 0
        fenString += str(blanks)
        blanks = 0
        if rank != 0 :
            fenString += "/"
    if colour == 10 :
        fenString += " w "
    else :
        fenString += " b "
    if canCastle == [[False, False], [False, False]] :
        fenString += "-"
    else :
        if canCastle[0][0] :
            fenString += "K"
        if canCastle[0][1] :
            fenString += "Q"
        if canCastle[1][0] :
            fenString += "k"
        if canCastle[1][1] :
            fenString += "q"
    fenString += enPassant
    fenString += " " + str(halfmove)
    fenString += " " + str(fullmove)
    return fenString


def isAmbiguous(position, piecePos, endPos, canCastle) :
    colour = int(str(position[piecePos[0]][piecePos[1]])[0]) * 10
    pieceID = position[piecePos[0]][piecePos[1]]
    sameRank = False
    sameFile = False
    for rank in range(8) :
        for file in range(8) :
            if position[rank][file] == pieceID and piecePos != (rank, file) and endPos in findPiecesLegalMoves(position,
                                                                                                               (rank, file),
                                                                                                               canCastle) :
                if rank == piecePos[0] :
                    sameRank = True
                if file == piecePos[1] :
                    sameFile = True
    if not sameRank and not sameFile :
        return tuple([False, False])
    elif sameRank and not sameFile :
        return tuple([True, False])
    elif sameFile and not sameRank :
        return tuple([False, True])
    else :
        return tuple([True, True])


def encodePGN(position, piecePos, endPos, canCastle, promoteTo=None) :
    colour = int(str(position[piecePos[0]][piecePos[1]])[0]) * 10
    pieceID = position[piecePos[0]][piecePos[1]]
    if colour == 10 :
        oppositeColour = 20
    else :
        oppositeColour = 10
    pgn = ""
    if pieceID - colour == 1 :
        if position[endPos[0]][endPos[1]] == 30 :
            pgn += reverseFileDict[endPos[1]] + str(endPos[0] + 1)
            if endPos[0] == 7 or endPos[0] == 0 :
                pgn += reversePieceDict[promoteTo - colour]
                newPosition = [i[:] for i in position]
                newPosition[piecePos[0]][piecePos[1]] = 30
                newPosition[endPos[0]][endPos[1]] = promoteTo
                if doesGameEnd(newPosition, oppositeColour, False, canCastle) == "checkmate" :
                    pgn += "#"
                elif inCheck(newPosition, oppositeColour) :
                    pgn += "+"
                if doesGameEnd(newPosition, oppositeColour, False, canCastle) == "checkmate" :
                    pgn += "#"
                elif inCheck(newPosition, oppositeColour) :
                    pgn += "+"
            else :
                newPosition = [i[:] for i in position]
                newPosition[piecePos[0]][piecePos[1]] = 30
                newPosition[endPos[0]][endPos[1]] = pieceID
                if doesGameEnd(newPosition, oppositeColour, False, canCastle) == "checkmate" :
                    pgn += "#"
                elif inCheck(newPosition, oppositeColour) :
                    pgn += "+"
        else :
            pgn += reverseFileDict[piecePos[1]] + "x"
            pgn += reverseFileDict[endPos[1]] + str(endPos[0] + 1)
            if endPos[0] == 7 or endPos[0] == 0 :
                pgn += reversePieceDict[promoteTo - colour]
                newPosition = [i[:] for i in position]
                newPosition[piecePos[0]][piecePos[1]] = 30
                newPosition[endPos[0]][endPos[1]] = promoteTo
                if doesGameEnd(newPosition, oppositeColour, False, canCastle) == "checkmate" :
                    pgn += "#"
                elif inCheck(newPosition, oppositeColour) :
                    pgn += "+"
            else :
                newPosition = [i[:] for i in position]
                if str(position[endPos[0]][endPos[1]])[1] == "7" :
                    newPosition[piecePos[0]][piecePos[1]] = 30
                    newPosition[endPos[0]][endPos[1]] = pieceID
                    if colour == 10 :
                        newPosition[endPos[0] - 1][endPos[1]] = 30
                    else :
                        newPosition[endPos[0] + 1][endPos[1]] = 30
                else :
                    newPosition[piecePos[0]][piecePos[1]] = 30
                    newPosition[endPos[0]][endPos[1]] = pieceID
                if doesGameEnd(newPosition, oppositeColour, False, canCastle) == "checkmate" :
                    pgn += "#"
                elif inCheck(newPosition, oppositeColour) :
                    pgn += "+"
    elif pieceID - colour != 6 or (pieceID - colour == 6 and abs(piecePos[1] - endPos[1]) != 2) :
        if pieceID - colour == 2 :
            pgn += "N"
        if pieceID - colour == 3 :
            pgn += "B"
        if pieceID - colour == 4 :
            pgn += "R"
        if pieceID - colour == 5 :
            pgn += "Q"
        if pieceID - colour == 6 :
            pgn += "K"
        ambiguous = isAmbiguous(position, piecePos, endPos, canCastle)
        if ambiguous[0] :
            pgn += reverseFileDict[piecePos[1]]
        if ambiguous[1] :
            pgn += str(piecePos[0] + 1)
        if position[endPos[0]][endPos[1]] == 30 or position[endPos[0]][endPos[1]] - oppositeColour == 7 :
            pgn += reverseFileDict[endPos[1]] + str(endPos[0] + 1)
        else :
            pgn += "x"
            pgn += reverseFileDict[endPos[1]] + str(endPos[0] + 1)
        newPosition = [i[:] for i in position]
        newPosition[piecePos[0]][piecePos[1]] = 30
        newPosition[endPos[0]][endPos[1]] = pieceID
        if doesGameEnd(newPosition, oppositeColour, False, canCastle) == "checkmate" :
            pgn += "#"
        elif inCheck(newPosition, oppositeColour) :
            pgn += "+"
    elif pieceID - colour == 6 and abs(piecePos[1] - endPos[1]) == 2 :
        if piecePos[1] - endPos[1] == -2 :
            pgn += "O-O"
            newPosition = [i[:] for i in position]
            newPosition[piecePos[0]][piecePos[1]] = 30
            newPosition[endPos[0]][endPos[1]] = pieceID
            newPosition[endPos[0]][endPos[1] - 1] = colour + 4
            if doesGameEnd(newPosition, oppositeColour, False, canCastle) == "checkmate" :
                pgn += "#"
            elif inCheck(newPosition, oppositeColour) :
                pgn += "+"
        elif piecePos[1] - endPos[1] == 2 :
            pgn += "O-O-O"
            newPosition = [i[:] for i in position]
            newPosition[piecePos[0]][piecePos[1]] = 30
            newPosition[endPos[0]][endPos[1]] = pieceID
            newPosition[endPos[0]][endPos[1] + 1] = colour + 4
            if doesGameEnd(newPosition, oppositeColour, False, canCastle) == "checkmate" :
                pgn += "#"
            elif inCheck(newPosition, oppositeColour) :
                pgn += "+"
    return pgn


# function to find pawn attacks
def findPawnAttacks(position, piecePos) :
    colour = int(str(position[piecePos[0]][piecePos[1]])[0]) * 10
    squares = []
    # runs if the colour is white
    if colour == 10 :
        # performs the left diagonal check if it is not beyond the board
        if 0 <= piecePos[0] + 1 <= 7 and 0 <= piecePos[1] - 1 <= 7 :
            leftID = position[piecePos[0] + 1][piecePos[1] - 1]
            leftPos = (piecePos[0] + 1, piecePos[1] - 1)
            # if the square is a black piece, it is marked
            if str(leftID)[0] == "2" :
                squares.append(leftPos)
        # performs the right diagonal check if it is not beyond the board
        if 0 <= piecePos[0] + 1 <= 7 and 0 <= piecePos[1] + 1 <= 7 :
            rightID = position[piecePos[0] + 1][piecePos[1] + 1]
            rightPos = (piecePos[0] + 1, piecePos[1] + 1)
            # if the square is a black piece, it is marked
            if str(rightID)[0] == "2" :
                squares.append(rightPos)
    # runs if the colour is black
    else :
        # performs the left diagonal check if it is not beyond the board
        if 0 <= piecePos[0] - 1 <= 7 and 0 <= piecePos[1] - 1 <= 7 :
            leftID = position[piecePos[0] - 1][piecePos[1] - 1]
            leftPos = (piecePos[0] - 1, piecePos[1] - 1)
            # if the square is a white piece, it is marked
            if str(leftID)[0] == "1" :
                squares.append(leftPos)
        # performs the right diagonal check if it is not beyond the board
        if 0 <= piecePos[0] - 1 <= 7 and 0 <= piecePos[1] + 1 <= 7 :
            rightID = position[piecePos[0] - 1][piecePos[1] + 1]
            rightPos = (piecePos[0] - 1, piecePos[1] + 1)
            # if the square is a white piece, it is marked
            if str(rightID)[0] == "1" :
                squares.append(rightPos)
    return squares


# function to find pawn moves (moving forward one square and two squares)
def findPawnMoves(position, piecePos) :
    colour = int(str(position[piecePos[0]][piecePos[1]])[0]) * 10
    squares = []
    if colour == 10 :
        if 0 <= piecePos[0] + 1 <= 7 :
            newSquareID = position[piecePos[0] + 1][piecePos[1]]
            newSquarePos = (piecePos[0] + 1, piecePos[1])
            if newSquareID == 30 :
                squares.append(newSquarePos)
            if 0 <= piecePos[0] + 2 <= 7 and piecePos[0] == 1 :
                newSquareID = position[piecePos[0] + 2][piecePos[1]]
                newSquarePos = (piecePos[0] + 2, piecePos[1])
                if newSquareID == 30 :
                    squares.append(newSquarePos)
    else :
        if 0 <= piecePos[0] - 1 <= 7 :
            newSquareID = position[piecePos[0] - 1][piecePos[1]]
            newSquarePos = (piecePos[0] - 1, piecePos[1])
            if newSquareID == 30 :
                squares.append(newSquarePos)
            if 0 <= piecePos[0] - 2 <= 7 and piecePos[0] == 6 :
                newSquareID = position[piecePos[0] - 2][piecePos[1]]
                newSquarePos = (piecePos[0] - 2, piecePos[1])
                if newSquareID == 30 :
                    squares.append(newSquarePos)
    attacks = findPawnAttacks(position, piecePos)
    if len(attacks) > 0 :
        for i in range(len(attacks)) :
            squares.append(attacks[i])
    return squares


# find all knight attacks
def findKnightMoves(position, piecePos) :
    colour = int(str(position[piecePos[0]][piecePos[1]])[0]) * 10
    if colour == 10 :
        oppositeColour = 20
    else :
        oppositeColour = 10
    squares = []
    # the direction of every possible knight move
    directions = [[2, 1], [1, 2], [-1, 2], [-2, 1], [-2, -1], [-1, -2], [1, -2], [2, -1]]
    for i in range(8) :
        # iterating through all possible moves
        # if the move is beyond the board, it is ignored
        if 0 <= piecePos[0] + directions[i][0] <= 7 and 0 <= piecePos[1] + directions[i][1] <= 7 :
            endID = position[piecePos[0] + directions[i][0]][piecePos[1] + directions[i][1]]
            endPos = (piecePos[0] + directions[i][0], piecePos[1] + directions[i][1])
            # if the square the knight targets is empty or has an enemy piece it is marked
            if endID == 30 or str(endID)[0] == str(oppositeColour)[0] :
                squares.append(endPos)
    return squares


# recursive function to find diagonal attacks
def findBishopMoves(position, piecePos, colour=None, square=None, direction=None, squares=None) :
    if colour is None :
        colour = int(str(position[piecePos[0]][piecePos[1]])[0]) * 10
    nextDirection = []
    if square is None :
        square = piecePos
    if direction is None or direction == [1, 1] :
        direction = [1, 1]
        nextDirection = [-1, 1]
    elif direction == [-1, 1] :
        nextDirection = [-1, -1]
    elif direction == [-1, -1] :
        nextDirection = [1, -1]
    if squares is None :
        # this list will be used to keep track of all squares that are being attacked
        squares = []
    # if the square that this function will travel to next is not on the board, the direction is switched and position is reset
    if 0 <= square[0] + direction[0] <= 7 and 0 <= square[1] + direction[1] <= 7 :
        newSquareID = position[square[0] + direction[0]][square[1] + direction[1]]
        newSquarePos = (square[0] + direction[0], square[1] + direction[1])
        # if the square in the direction of travel is empty, it "walks" to that square and recurses
        if newSquareID == 30 or str(newSquareID)[1] == "7" :
            if newSquarePos not in squares :
                squares.append(newSquarePos)
                return findBishopMoves(position, piecePos, colour, newSquarePos, direction, squares)
            else :
                return squares
        # if the square in the direction of travel is its own, it resets to the original square and switches direction
        elif str(newSquareID)[0] == str(colour // 10) :
            if direction != [1, -1] :
                return findBishopMoves(position, piecePos, colour, piecePos, nextDirection, squares)
            else :
                return squares
        # if the square in the direction of travel is not its own, it attacks that square, resets to the original square and switches direction
        else :
            if direction != [1, -1] :
                squares.append(newSquarePos)
                return findBishopMoves(position, piecePos, colour, piecePos, nextDirection, squares)
            else :
                squares.append(newSquarePos)
                return squares
    else :
        if direction != [1, -1] :
            return findBishopMoves(position, piecePos, colour, piecePos, nextDirection, squares)
        else :
            return squares


# recursive function to find horizontal and vertical attacks
def findRookMoves(position, piecePos, colour=None, square=None, direction=None, squares=None) :
    if colour is None :
        colour = int(str(position[piecePos[0]][piecePos[1]])[0]) * 10
    nextDirection = []
    if square is None :
        square = piecePos
    if direction is None or direction == [1, 0] :
        direction = [1, 0]
        nextDirection = [0, 1]
    elif direction == [0, 1] :
        nextDirection = [-1, 0]
    elif direction == [-1, 0] :
        nextDirection = [0, -1]
    if squares is None :
        squares = []
    if 0 <= square[0] + direction[0] <= 7 and 0 <= square[1] + direction[1] <= 7 :
        newSquareID = position[square[0] + direction[0]][square[1] + direction[1]]
        newSquarePos = (square[0] + direction[0], square[1] + direction[1])
        # if the square in the direction of travel is empty, it "walks" to that square and recurses
        if newSquareID == 30 or str(newSquareID)[1] == "7" :
            if newSquarePos not in squares :
                squares.append(newSquarePos)
                return findRookMoves(position, piecePos, colour, newSquarePos, direction, squares)
            else :
                return squares
        # if the square in the direction of travel is its own, it resets to the original square and switches direction
        elif str(newSquareID)[0] == str(colour // 10) :
            if direction != [0, -1] :
                return findRookMoves(position, piecePos, colour, piecePos, nextDirection, squares)
            else :
                return squares
            # if the square in the direction of travel is not its own, it attacks that square, resets to the original square and switches direction
        else :
            if direction != [0, -1] :
                squares.append(newSquarePos)
                return findRookMoves(position, piecePos, colour, piecePos, nextDirection, squares)
            else :
                squares.append(newSquarePos)
                return squares
    else :
        if direction != [0, -1] :
            return findRookMoves(position, piecePos, colour, piecePos, nextDirection, squares)
        else :
            return squares


# simple function to find queen attacks combining the rook and bishop
def findQueenMoves(position, piecePos) :
    squares = []
    lines = findRookMoves(position, piecePos)
    diagonals = findBishopMoves(position, piecePos)
    for i in range(len(lines)) :
        squares.append(lines[i])
    for i in range(len(diagonals)) :
        squares.append(diagonals[i])
    return squares


def findKingAttacks(position, piecePos) :
    colour = int(str(position[piecePos[0]][piecePos[1]])[0]) * 10
    if colour == 10 :
        oppositeColour = 20
    else :
        oppositeColour = 10
    squares = []
    directions = [[1, 0], [1, 1], [0, 1], [1, -1], [-1, 0], [-1, -1], [0, -1], [-1, 1]]
    for i in range(8) :
        if 0 <= piecePos[0] + directions[i][0] <= 7 and 0 <= piecePos[1] + directions[i][1] <= 7 :
            endID = position[piecePos[0] + directions[i][0]][piecePos[1] + directions[i][1]]
            endPos = (piecePos[0] + directions[i][0], piecePos[1] + directions[i][1])
            if endID == 30 or str(endID)[0] == str(oppositeColour)[0] :
                squares.append(endPos)
    return squares


def findKingMoves(position, piecePos, canCastle) :
    colour = int(str(position[piecePos[0]][piecePos[1]])[0]) * 10
    if colour == 10 :
        oppositeColour = 20
    else :
        oppositeColour = 10
    squares = []
    directions = [[1, 0], [1, 1], [0, 1], [1, -1], [-1, 0], [-1, -1], [0, -1], [-1, 1]]
    for i in range(8) :
        if 0 <= piecePos[0] + directions[i][0] <= 7 and 0 <= piecePos[1] + directions[i][1] <= 7 :
            endID = position[piecePos[0] + directions[i][0]][piecePos[1] + directions[i][1]]
            endPos = (piecePos[0] + directions[i][0], piecePos[1] + directions[i][1])
            if endID == 30 or str(endID)[0] == str(oppositeColour)[0] :
                squares.append(endPos)
    if canCastle[colour // 10 - 1][0] and str(position[piecePos[0]][piecePos[1] + 3])[1] == "4" and \
            position[piecePos[0]][piecePos[1] + 2] == 30 and position[piecePos[0]][piecePos[1] + 1] == 30 :
        squares.append((piecePos[0], piecePos[1] + 2))
    if canCastle[colour // 10 - 1][1] and str(position[piecePos[0]][piecePos[1] - 4])[1] == "4" and \
            position[piecePos[0]][piecePos[1] - 3] == 30 and position[piecePos[0]][piecePos[1] - 2] == 30 and \
            position[piecePos[0]][piecePos[1] - 1] == 30 :
        squares.append((piecePos[0], piecePos[1] - 2))
    return squares


# combines all piece attacks into one function
def findPieceAttacks(position, piecePos) :
    pieceID = str(position[piecePos[0]][piecePos[1]])[1]
    if pieceID == "1" :
        return findPawnAttacks(position, piecePos)
    elif pieceID == "2" :
        return findKnightMoves(position, piecePos)
    elif pieceID == "3" :
        return findBishopMoves(position, piecePos)
    elif pieceID == "4" :
        return findRookMoves(position, piecePos)
    elif pieceID == "5" :
        return findQueenMoves(position, piecePos)
    elif pieceID == "6" :
        return findKingAttacks(position, piecePos)
    else :
        return []


# combines all piece moves into one function
def findPieceMoves(position, piecePos, canCastle) :
    pieceID = str(position[piecePos[0]][piecePos[1]])[1]
    if pieceID == "1" :
        return findPawnMoves(position, piecePos)
    elif pieceID == "2" :
        return findKnightMoves(position, piecePos)
    elif pieceID == "3" :
        return findBishopMoves(position, piecePos)
    elif pieceID == "4" :
        return findRookMoves(position, piecePos)
    elif pieceID == "5" :
        return findQueenMoves(position, piecePos)
    elif pieceID == "6" :
        return findKingMoves(position, piecePos, canCastle)
    else :
        return []


# checks if position is in check for a colour
def inCheck(position, colour) :
    attacked = clearBoard()
    for rank in range(8) :
        for file in range(8) :
            if position[rank][file] != 30 and str(position[rank][file])[1] != "7" and str(position[rank][file])[
                    0] != str(colour // 10) :
                pieceAttacks = findPieceAttacks(position, (rank, file))
                # for every square under attack, the corresponding square in the board "attacked" is also 99
                for i in range(len(pieceAttacks)) :
                    attacked[pieceAttacks[i][0]][pieceAttacks[i][1]] = 99
    # if the king's square is under attack, return True
    for rank in range(8) :
        for file in range(8) :
            if position[rank][file] == colour + 6 :
                if attacked[rank][file] == 99 :
                    return True
                else :
                    return False


# finds if any given move is legal
def isLegal(position, piecePos, endPos, canCastle) :
    colour = int(str(position[piecePos[0]][piecePos[1]])[0]) * 10
    pieceID = position[piecePos[0]][piecePos[1]]
    endID = position[endPos[0]][endPos[1]]
    if endPos not in findPieceMoves(position, piecePos, canCastle) :
        return False
    if pieceID - colour != 6 or (pieceID - colour == 6 and abs(piecePos[1] - endPos[1]) != 2) :
        # handles generic case
        if pieceID - colour != 1 or (pieceID - colour == 1 and str(endID)[1] != "7") :
            newPosition = [i[:] for i in position]
            newPosition[piecePos[0]][piecePos[1]] = 30
            newPosition[endPos[0]][endPos[1]] = pieceID
            return not inCheck(newPosition, colour)
        # handles edge case: en passant
        elif pieceID - colour == 1 and str(endID)[1] == "7" :
            if colour == 10 :
                newPosition = [i[:] for i in position]
                newPosition[piecePos[0]][piecePos[1]] = 30
                newPosition[endPos[0]][endPos[1]] = pieceID
                newPosition[endPos[0] - 1][endPos[1]] = 30
                return not inCheck(newPosition, colour)
            else :
                newPosition = [i[:] for i in position]
                newPosition[piecePos[0]][piecePos[1]] = 30
                newPosition[endPos[0]][endPos[1]] = pieceID
                newPosition[endPos[0] + 1][endPos[1]] = 30
                return not inCheck(newPosition, colour)
    # handles edge case: castling
    elif pieceID - colour == 6 and abs(piecePos[1] - endPos[1]) == 2 :
        # handles short castling
        if piecePos[1] - endPos[1] == -2 :
            if not inCheck(position, colour) :
                newPosition = [i[:] for i in position]
                newPosition[piecePos[0]][piecePos[1]] = 30
                newPosition[piecePos[0]][piecePos[1] + 1] = pieceID
                if not inCheck(newPosition, colour) :
                    newPosition = [i[:] for i in position]
                    newPosition[piecePos[0]][piecePos[1]] = 30
                    newPosition[piecePos[0]][piecePos[1] + 2] = pieceID
                    if not inCheck(newPosition, colour) :
                        newPosition = [i[:] for i in position]
                        newPosition[piecePos[0]][piecePos[1]] = 30
                        newPosition[piecePos[0]][piecePos[1] + 2] = pieceID
                        newPosition[piecePos[0]][piecePos[1] + 3] = 30
                        newPosition[endPos[0]][endPos[1] - 1] = colour + 4
                        return not inCheck(newPosition, colour)
                    else :
                        return False
                else :
                    return False
            else :
                return False
        # handles long castling
        elif piecePos[1] - endPos[1] == 2 :
            if not inCheck(position, colour) :
                newPosition = [i[:] for i in position]
                newPosition[piecePos[0]][piecePos[1]] = 30
                newPosition[piecePos[0]][piecePos[1] - 1] = pieceID
                if not inCheck(newPosition, colour) :
                    newPosition = [i[:] for i in position]
                    newPosition[piecePos[0]][piecePos[1]] = 30
                    newPosition[piecePos[0]][piecePos[1] - 2] = pieceID
                    if not inCheck(newPosition, colour) :
                        newPosition = [i[:] for i in position]
                        newPosition[piecePos[0]][piecePos[1]] = 30
                        newPosition[piecePos[0]][piecePos[1] - 2] = pieceID
                        newPosition[piecePos[0]][piecePos[1] - 4] = 30
                        newPosition[endPos[0]][endPos[1] + 1] = colour + 4
                        return not inCheck(newPosition, colour)
                    else :
                        return False
                else :
                    return False
            else :
                return False


def findPiecesLegalMoves(position, piecePos, canCastle) :
    legalMoves = findPieceMoves(position, piecePos, canCastle)
    incrementing = True
    i = 0
    while incrementing :
        if i < len(legalMoves) :
            if not isLegal(position, piecePos, legalMoves[i], canCastle) :
                legalMoves.pop(i)
            else :
                i += 1
        else :
            break
    return legalMoves


# returns a list of all legal moves in a given position
def findAllMoves(position, colour, canCastle) :
    moves = {}
    for rank in range(8) :
        for file in range(8) :
            if str(position[rank][file])[0] == str(colour // 10) and position[rank][file] != colour + 7 :
                moves[(rank, file)] = []
                possibleMoves = findPieceMoves(position, (rank, file), canCastle)
                # checks if every possible move a piece causes or ignores a check
                for i in range(len(possibleMoves)) :
                    if isLegal(position, (rank, file), possibleMoves[i], canCastle) :
                        moves[(rank, file)].append(possibleMoves[i])
                if not moves[(rank, file)] :
                    moves.pop((rank, file))
    return moves


# checks if a move ends the game
def doesGameEnd(position, colour, moveDraw, canCastle) :
    if len(findAllMoves(position, colour, canCastle)) == 0 :
        if inCheck(position, colour) :
            return "checkmate"
        else :
            return "stalemate"
    else :
        if moveDraw :
            return "stalemate"
        return False


def deleteEnPassant(position) :
    for rank in range(8) :
        for file in range(8) :
            if str(position[rank][file])[1] == "7" :
                position[rank][file] = 30
    return position


def makeMove(position, piecePos, endPos, canCastle, promoteTo=None) :
    if isLegal(position, piecePos, endPos, canCastle) :
        colour = int(str(position[piecePos[0]][piecePos[1]])[0]) * 10
        pieceID = position[piecePos[0]][piecePos[1]]
        endID = position[endPos[0]][endPos[1]]
        if pieceID - colour != 6 or (pieceID - colour == 6 and abs(piecePos[1] - endPos[1]) != 2) :
            if pieceID - colour != 1 or (pieceID - colour == 1 and str(endID)[1] != "7") :
                # generic case
                position[piecePos[0]][piecePos[1]] = 30
                position[endPos[0]][endPos[1]] = pieceID
                deleteEnPassant(position)
                # handles promotion
                if promoteTo is not None :
                    position[endPos[0]][endPos[1]] = promoteTo
                # create en passant target squares if pawn is pushed 2 squares
                elif pieceID - colour == 1 and abs(piecePos[0] - endPos[0]) == 2 :
                    if colour == 10 :
                        position[endPos[0] - 1][endPos[1]] = 17
                    elif colour == 20 :
                        position[endPos[0] + 1][endPos[1]] = 27
                # handle castling rules
                if pieceID == 16 :
                    canCastle[0] = [False, False]
                elif pieceID == 26 :
                    canCastle[1] = [False, False]
                elif pieceID == 14 and piecePos == (0, 7) :
                    canCastle[0][0] = False
                elif pieceID == 14 and piecePos == (0, 0) :
                    canCastle[0][1] = False
                elif pieceID == 24 and piecePos == (7, 7) :
                    canCastle[1][0] = False
                elif pieceID == 24 and piecePos == (7, 0) :
                    canCastle[1][1] = False
                return position, canCastle
            # handle special case: en passant
            elif pieceID - colour == 1 and str(endID)[1] == "7" :
                position[piecePos[0]][piecePos[1]] = 30
                position[endPos[0]][endPos[1]] = pieceID
                position[endPos[0] - 1][endPos[1]] = 30
                deleteEnPassant(position)
                return position, canCastle
        # handle special case: short side castling
        elif pieceID - colour == 6 and piecePos[1] - endPos[1] == - 2 :
            position[piecePos[0]][piecePos[1]] = 30
            position[piecePos[0]][piecePos[1] + 2] = pieceID
            position[piecePos[0]][piecePos[1] + 3] = 30
            position[endPos[0]][endPos[1] - 1] = colour + 4
            deleteEnPassant(position)
            if colour == 10 :
                canCastle[0][0] = False
            else :
                canCastle[1][0] = False
            return position, canCastle
        # handle special case: long side castling
        elif pieceID - colour == 6 and piecePos[1] - endPos[1] == 2 :
            position[piecePos[0]][piecePos[1]] = 30
            position[piecePos[0]][piecePos[1] - 2] = pieceID
            position[piecePos[0]][piecePos[1] - 4] = 30
            position[endPos[0]][endPos[1] + 1] = colour + 4
            deleteEnPassant(position)
            if colour == 10 :
                canCastle[0][1] = False
            else :
                canCastle[1][1] = False
            return position, canCastle
    return False


# GUI is thx to Eddie Sharick (YouTube) https://www.youtube.com/watch?v=EnYui0e73Rs&list=PLBwF487qi8MGU81nDGaeNE1EnNEPYWKY_&ab_channel=EddieSharick
# function to combine drawBoard and drawPieces
def drawPosition(screen, position, highlighted, moves, captures) :
    drawBoard(screen, highlighted)
    drawPieces(screen, position)
    drawDots(screen, moves, captures)


# function to draw a board
def drawBoard(screen, highlighted) :
    colours = [pygame.Color("white"), pygame.Color("tan")]
    for rank in range(8) :
        for file in range(8) :
            colour = colours[(rank + file) % 2]
            pygame.draw.rect(screen, colour, pygame.Rect(file * 100, rank * 100, 100, 100))
    if highlighted is not None :
        pygame.draw.rect(screen, "yellow", pygame.Rect(highlighted[1] * 100, (7 - highlighted[0]) * 100, 100, 100))


def drawPieces(screen, position) :
    visualRank = 7
    for rank in range(8) :
        for file in range(8) :
            piece = str(position[rank][file])
            if piece != "30" :
                screen.blit(pygame.transform.scale(pygame.image.load("images/" + piece + ".png"), (100, 100)),
                            pygame.Rect(file * 100, visualRank * 100, 100, 100))
        visualRank -= 1


def drawDots(screen, moves, captures) :
    if len(moves) > 0 :
        for i in range(len(moves)) :
            screen.blit(pygame.transform.scale(pygame.image.load("images/dot.png"), (100, 100)),
                        pygame.Rect(moves[i][1] * 100, (7 - moves[i][0]) * 100, 100, 100))
    if len(captures) > 0 :
        for i in range(len(captures)) :
            screen.blit(pygame.transform.scale(pygame.image.load("images/bracket.png"), (100, 100)),
                        pygame.Rect(captures[i][1] * 100, (7 - captures[i][0]) * 100, 100, 100))


def drawPGN(screen, pgn) :
    pygame.draw.rect(screen, "black", pygame.Rect(800, 0, 400, 800))
    font = pygame.font.Font("fonts/fff-forward.ttf", 13)
    pgnString = [""]
    for i in range(len(pgn)) :
        if font.render(pgnString[len(pgnString) - 1], True, "white").get_rect()[2] > 320 :
            pgnString.append("")
        if len(pgnString[len(pgnString) - 1]) > 0 :
            pgnString[len(pgnString) - 1] += "  "
        pgnString[len(pgnString) - 1] += str(i + 1) + ". "
        pgnString[len(pgnString) - 1] += str(pgn[i][0]) + " "
        if len(pgn[i]) > 1 :
            pgnString[len(pgnString) - 1] += str(pgn[i][1]) + " "
    for i in range(len(pgnString)) :
        if pgnString[i] != "" :
            screen.blit(font.render(pgnString[i], True, "white"), (810, 10 + i * 25))


def switchTurns(screen, pgn, move, playerClicks, capture, colour, halfmove, fullmove) :
    moveSound = [pygame.mixer.Sound("sounds/move_1.wav"), pygame.mixer.Sound("sounds/move_2.wav"),
                 pygame.mixer.Sound("sounds/move_3.wav")]
    captureSound = [pygame.mixer.Sound("sounds/capture_1.wav"), pygame.mixer.Sound("sounds/capture_2.wav"),
                    pygame.mixer.Sound("sounds/capture_3.wav")]
    if move is not False :
        if not capture :
            pygame.mixer.Sound.play(moveSound[random.randint(0, 2)])
        else :
            pygame.mixer.Sound.play(captureSound[random.randint(0, 2)])
        board = [i[:] for i in move[0]]
        canCastle = move[1]
        if str(board[playerClicks[0][0]][playerClicks[0][1]])[0] != "1" and \
                board[playerClicks[1][0]][playerClicks[1][1]] == 30 :
            halfmove += 1
        if colour == "2" :
            colour = "1"
            fullmove += 1
            if len(pgn) >= 4 and pgn[len(pgn) - 1] == pgn[len(pgn) - 3] and pgn[len(pgn) - 2] == pgn[len(pgn) - 4] :
                if doesGameEnd(board, int(colour) * 10, True, canCastle) :
                    print("GAME OVER by " + doesGameEnd(board, int(colour) * 10, True, canCastle) + "!")
                    print("FEN String of final position: ")
                    print(encodeFEN(board, 10, canCastle, halfmove, fullmove))
                    print("PGN of game: ")
                    for i in range(len(pgn) - 1) :
                        print(str(i + 1) + ".", end=" ")
                        print(pgn[i][0], end=" ")
                        print(pgn[i][1], end=" ")
                    if len(pgn[len(pgn) - 1]) == 2 :
                        print(str(len(pgn) + 1) + ".", end=" ")
                        print(pgn[len(pgn) - 1][0], end=" ")
                        print(pgn[len(pgn) - 1][1], end=" ")
                    else :
                        print(str(len(pgn) + 1) + ".", end=" ")
                        print(pgn[len(pgn) - 1][0], end=" ")
                    print("1/2-1/2")
            elif halfmove == 50 :
                if doesGameEnd(board, int(colour) * 10, True, canCastle) :
                    print("GAME OVER by " + doesGameEnd(board, int(colour) * 10, True, canCastle) + "!")
                    print("FEN String of final position: ")
                    print(encodeFEN(board, 10, canCastle, halfmove, fullmove))
                    print("PGN of game: ")
                    for i in range(len(pgn) - 1) :
                        print(str(i + 1) + ".", end=" ")
                        print(pgn[i][0], end=" ")
                        print(pgn[i][1], end=" ")
                    if len(pgn[len(pgn) - 1]) == 2 :
                        print(str(len(pgn) + 1) + ".", end=" ")
                        print(pgn[len(pgn) - 1][0], end=" ")
                        print(pgn[len(pgn) - 1][1], end=" ")
                    else :
                        print(str(len(pgn) + 1) + ".", end=" ")
                        print(pgn[len(pgn) - 1][0], end=" ")
                    print("1/2-1/2")
            elif doesGameEnd(board, int(colour) * 10, False, canCastle) :
                print("GAME OVER by " + doesGameEnd(board, int(colour) * 10, False,
                                                    canCastle) + "!")
                print("FEN String of final position: ")
                print(encodeFEN(board, 10, canCastle, halfmove, fullmove))
                print("PGN of game: ")
                for i in range(len(pgn) - 1) :
                    print(str(i + 1) + ".", end=" ")
                    print(pgn[i][0], end=" ")
                    print(pgn[i][1], end=" ")
                if len(pgn[len(pgn) - 1]) == 2 :
                    print(str(len(pgn) + 1) + ".", end=" ")
                    print(pgn[len(pgn) - 1][0], end=" ")
                    print(pgn[len(pgn) - 1][1], end=" ")
                else :
                    print(str(len(pgn) + 1) + ".", end=" ")
                    print(pgn[len(pgn) - 1][0], end=" ")
                print("0-1")
            else :
                return halfmove, fullmove, colour
        else :
            colour = "2"
            if halfmove == 50 :
                if doesGameEnd(board, int(colour) * 10, True, canCastle) :
                    print("GAME OVER by " + doesGameEnd(board, int(colour) * 10, True,
                                                        canCastle) + "!")
                    print("FEN String of final position: ")
                    print(encodeFEN(board, 10, canCastle, halfmove, fullmove))
                    print("PGN of game: ")
                    for i in range(len(pgn) - 1) :
                        print(str(i + 1) + ".", end=" ")
                        print(pgn[i][0], end=" ")
                        print(pgn[i][1], end=" ")
                    if len(pgn[len(pgn) - 1]) == 2 :
                        print(str(len(pgn) + 1) + ".", end=" ")
                        print(pgn[len(pgn) - 1][0], end=" ")
                        print(pgn[len(pgn) - 1][1], end=" ")
                    else :
                        print(str(len(pgn) + 1) + ".", end=" ")
                        print(pgn[len(pgn) - 1][0], end=" ")
                    print("1/2-1/2")
            elif doesGameEnd(board, int(colour) * 10, False, canCastle) :
                print(
                    "GAME OVER by " + doesGameEnd(board, int(colour) * 10, False, canCastle) + "!")
                print("FEN String of final position: ")
                print(encodeFEN(board, 10, canCastle, halfmove, fullmove))
                print("PGN of game: ")
                for i in range(len(pgn) - 1) :
                    print(str(i + 1) + ".", end=" ")
                    print(pgn[i][0], end=" ")
                    print(pgn[i][1], end=" ")
                if len(pgn[len(pgn) - 1]) == 2 :
                    print(str(len(pgn) + 1) + ".", end=" ")
                    print(pgn[len(pgn) - 1][0], end=" ")
                    print(pgn[len(pgn) - 1][1], end=" ")
                else :
                    print(str(len(pgn) + 1) + ".", end=" ")
                    print(pgn[len(pgn) - 1][0], end=" ")
                print("1-0")
            else :
                return halfmove, fullmove, colour


# main driver for the GUI and handling moves
def main(fenString=None) :
    if fenString is None :
        board = startBoard()
        colour = "1"
        canCastle = [[True, True], [True, True]]
        fullmove = 0
        halfmove = 0
    else :
        parsed = parseFEN(fenString, False)
        board = parsed["position"]
        colour = str(parsed["colour"] // 10)
        canCastle = parsed["canCastle"]
        fullmove = parsed["fullmove"]
        halfmove = parsed["halfmove"]
    pgn = []
    # pygame is initialized
    pygame.init()
    # window is initialized
    screen = pygame.display.set_mode(size=(1200, 800))
    # system clock is initialized
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("black"))
    # sounds are loaded
    running = True
    sqSelected = ()  # keep track of the last click in a tuple
    playerClicks = []  # keep track of the last two player clicks in two tuples
    while running :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.display.quit()
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pos()[0] <= 800 :
                location = pygame.mouse.get_pos()  # x,y location of mouse
                col = location[0] // 100
                row = (800 - location[1]) // 100
                if event.button == 3 :
                    sqSelected = ()  # deselect
                    playerClicks = []  # reset player clicks
                if sqSelected == (row, col) :
                    sqSelected = ()  # deselect
                    playerClicks = []  # reset player clicks
                elif event.button == 1 :
                    sqSelected = (row, col)
                    if len(playerClicks) == 0 and str(board[sqSelected[0]][sqSelected[1]])[0] == colour :
                        playerClicks.append(sqSelected)
                    elif len(playerClicks) == 1 :
                        if str(board[sqSelected[0]][sqSelected[1]])[0] == colour :
                            playerClicks = [sqSelected]
                        else :
                            playerClicks.append(sqSelected)
                    else :
                        playerClicks = []
                if len(playerClicks) == 2 :
                    if str(board[playerClicks[0][0]][playerClicks[0][1]])[0] == colour :
                        capture = False
                        if (board[playerClicks[1][0]][playerClicks[1][1]] != 30 and str(board[playerClicks[1][0]][playerClicks[1][1]])[1] != "7") or (str(board[playerClicks[0][0]][playerClicks[0][1]])[1] == "1" and (playerClicks[1][0] == 7 or playerClicks[1][0] == 0)) or (str(board[playerClicks[0][0]][playerClicks[0][1]])[1] == "1" and str(board[playerClicks[1][0]][playerClicks[1][1]])[1] == "7"):
                            capture = True
                        if isLegal(board, playerClicks[0], playerClicks[1], canCastle) :
                            promoteTo = None
                            if board[playerClicks[0][0]][playerClicks[0][1]] - (int(colour) * 10) == 1 and \
                                    (playerClicks[1][0] == 7 or playerClicks[1][0] == 0) :
                                promoting = True
                                while promoting :
                                    promoteTo = input("What piece would you like to promote to (N/B/R/Q)? ").upper()
                                    if promoteTo == "N" or promoteTo == "B" or promoteTo == "R" or promoteTo == "Q" :
                                        promoteTo = pieceDict[promoteTo] + (int(colour) * 10)
                                        promoting = False
                                    else :
                                        print("Please enter N for knight, B for bishop, R for rook, or Q for queen.")
                            if colour == "1" :
                                pgn.append([encodePGN(board, playerClicks[0], playerClicks[1], canCastle, promoteTo)])
                            else :
                                pgn[len(pgn) - 1].append(encodePGN(board, playerClicks[0], playerClicks[1], canCastle, promoteTo))
                            move = makeMove(board, playerClicks[0], playerClicks[1], canCastle, promoteTo)
                            variables = switchTurns(screen, pgn, move, playerClicks, capture, colour, halfmove, fullmove)
                            if variables is not None :
                                halfmove = variables[0]
                                fullmove = variables[1]
                                colour = variables[2]
                        else :
                            pygame.mixer.Sound.play(pygame.mixer.Sound("sounds/error.wav"))
                    playerClicks = []
        if len(playerClicks) > 0 and str(board[playerClicks[0][0]][playerClicks[0][1]])[0] == colour and \
                board[playerClicks[0][0]][playerClicks[0][1]] != int(colour * 10) + 7 :
            highlighted = playerClicks[0]
        else :
            highlighted = None
        moves = []
        captures = []
        if highlighted is not None :
            moves = findPiecesLegalMoves(board, highlighted, canCastle)
            incrementing = True
            i = 0
            while incrementing :
                if i < len(moves) :
                    if (board[moves[i][0]][moves[i][1]] != 30 and str(board[moves[i][0]][moves[i][1]])[1] != "7") or \
                            (str(board[moves[i][0]][moves[i][1]])[1] == "7" and str(board[highlighted[0]][highlighted[1]])[1] == "1"):
                        captures.append(moves.pop(i))
                    else :
                        i += 1
                else :
                    break
        drawPosition(screen, board, highlighted, moves, captures)
        drawPGN(screen, pgn)
        clock.tick(500)
        pygame.display.flip()


# driver code
if __name__ == '__main__' :
    main()
