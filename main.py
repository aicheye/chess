import pygame

# dictionaries - used for functions
pieceDict = {"P" : 1, "N" : 2, "B" : 3, "R" : 4, "Q" : 5, "K" : 6}
reversePieceDict = {0 : ".", 1 : "P", 2 : "N", 3 : "B", 4 : "R", 5 : "Q", 6 : "K", 7 : ".",
                    "0" : ".", "1" : "P", "2" : "N", "3" : "B", "4" : "R", "5" : "Q", "6" : "K", "7" : "."}
fileDict = {"a" : 0, "b" : 1, "c" : 2, "d" : 3, "e" : 4, "f" : 5, "g" : 6, "h" : 7}

# images of the pieces
images = {}


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
def parseFen(fen, posOnly=False) :
    # these are variables for all the FEN fields
    position = clearBoard()
    indexed = fen.split()
    placements = indexed[0].split("/")
    canCastle = [False, False, False, False]
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
    # canCastle[0]: white king side, [1]: white queen side, [2]: black king side, [3]: black queen side
    if "K" in indexed[2] :
        canCastle[0] = True
    if "Q" in indexed[2] :
        canCastle[1] = True
    if "k" in indexed[2] :
        canCastle[2] = True
    if "q" in indexed[2] :
        canCastle[3] = True
    if indexed[3] != "-" :
        position[int(indexed[3][1])][fileDict[indexed[3][0]]] = colour + 7
    if not posOnly :
        return position, colour, canCastle, halfmove, fullmove
    else :
        return position


# returns a list of all legal moves in a given position
def findMoves(position, colour) :
    moves = []
    return moves


# checks if a move ends the game
def doesGameEnd(position, colour, repetitionCount) :
    if len(findMoves(position, colour)) == 0 :
        if isCheck(position, colour) :
            return "checkmate"
        else :
            return "stalemate"
    else :
        if repetitionCount == 3 :
            return "stalemate"
        return False


# checks if position is in check for a colour
def isCheck(position, colour) :
    attacked = clearBoard()
    for rank in range(8) :
        for file in range(8) :
            if position[rank][file] != 30 and position[rank][file] != 17 and position[rank][file] != 27 and str(position[rank][file])[0] != str(colour // 10):
                pieceAttacks = findStaticAttacks(position, [rank, file])
                # for every square under attack, the corresponding square in the board "attacked" is also 99
                for i in range(len(pieceAttacks)) :
                    attacked[pieceAttacks[i][0]][pieceAttacks[i][1]] = 99
    for rank in range(8) :
        for file in range(8) :
            if position[rank][file] == colour + 6 and attacked[rank][file] == 99 :
                return True
    return False


# function to find pawn attacks
def findPawnAttacks(position, piecePos) :
    colour = int(str(position[piecePos[0]][piecePos[1]])[0]) * 10
    squares = []
    # runs if the colour is white
    if colour == 10 :
        # performs the left diagonal check if it is not beyond the board
        if 0 <= piecePos[0] + 1 <= 7 and 0 <= piecePos[1] - 1 <= 7 :
            leftID = position[piecePos[0] + 1][piecePos[1] - 1]
            leftPos = [piecePos[0] + 1, piecePos[1] - 1]
            # if the square is empty or a black piece, it is marked
            if leftID == 30 or str(leftID)[0] == "2" :
                squares.append(leftPos)
        # performs the right diagonal check if it is not beyond the board
        if 0 <= piecePos[0] + 1 <= 7 and 0 <= piecePos[1] + 1 <= 7 :
            rightID = position[piecePos[0] + 1][piecePos[1] + 1]
            rightPos = [piecePos[0] + 1, piecePos[1] + 1]
            # if the square is empty or a black piece, it is marked
            if rightID == 30 or str(rightID)[0] == "2" :
                squares.append(rightPos)
    # runs if the colour is black
    else :
        # performs the left diagonal check if it is not beyond the board
        if 0 <= piecePos[0] - 1 <= 7 and 0 <= piecePos[1] - 1 <= 7 :
            leftID = position[piecePos[0] - 1][piecePos[1] - 1]
            leftPos = [piecePos[0] - 1, piecePos[1] - 1]
            # if the square is empty or a white piece, it is marked
            if leftID == 30 or str(leftID)[0] == "1" :
                squares.append(leftPos)
        # performs the right diagonal check if it is not beyond the board
        if 0 <= piecePos[0] - 1 <= 7 and 0 <= piecePos[1] + 1 <= 7 :
            rightID = position[piecePos[0] - 1][piecePos[1] + 1]
            rightPos = [piecePos[0] - 1, piecePos[1] + 1]
            # if the square is empty or a white piece, it is marked
            if rightID == 30 or str(rightID)[0] == "1" :
                squares.append(rightPos)
    return squares


def findKnightAttacks(position, piecePos) :
    colour = int(str(position[piecePos[0]][piecePos[1]])[0]) * 10
    if colour == 10 :
        oppositeColour = 20
    else :
        oppositeColour = 10
    squares = []
    directions = [[2, 1], [1, 2], [-1, 2], [-2, 1], [-2, -1], [-1, -2], [1, -2], [2, -1]]
    for i in range(8) :
        if 0 <= piecePos[0] + directions[i][0] <= 7 and 0 <= piecePos[1] + directions[i][1] <= 7 :
            destinationID = position[piecePos[0] + directions[i][0]][piecePos[1] + directions[i][1]]
            destinationPos = [piecePos[0] + directions[i][0], piecePos[1] + directions[i][1]]
            if destinationID == 30 or str(destinationID)[0] == str(oppositeColour)[0] :
                squares.append(destinationPos)
    return squares


# recursive function to find diagonal attacks
def findBishopAttacks(position, piecePos, colour=None, square=None, direction=None, squares=None) :
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
        newSquarePos = [square[0] + direction[0], square[1] + direction[1]]
        # if the square in the direction of travel is empty, it "walks" to that square and recurses
        if newSquareID == 30 :
            if newSquarePos not in squares :
                squares.append(newSquarePos)
                return findBishopAttacks(position, piecePos, colour, newSquarePos, direction, squares)
            else :
                return squares
        # if the square in the direction of travel is its own, it resets to the original square and switches direction
        elif str(newSquareID)[0] == str(colour // 10) :
            if direction != [1, -1] :
                return findBishopAttacks(position, piecePos, colour, piecePos, nextDirection, squares)
            else :
                return squares
            # if the square in the direction of travel is not its own, it attacks that square, resets to the original square and switches direction
        else :
            if direction != [1, -1] :
                squares.append(newSquarePos)
                return findBishopAttacks(position, piecePos, colour, piecePos, nextDirection, squares)
            else :
                squares.append(newSquarePos)
                return squares
    else :
        if direction != [1, -1] :
            return findBishopAttacks(position, piecePos, colour, piecePos, nextDirection, squares)
        else :
            return squares


# recursive function to find horizontal and vertical attacks
def findRookAttacks(position, piecePos, colour=None, square=None, direction=None, squares=None) :
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
        newSquarePos = [square[0] + direction[0], square[1] + direction[1]]
        # if the square in the direction of travel is empty, it "walks" to that square and recurses
        if newSquareID == 30 :
            if newSquarePos not in squares :
                squares.append(newSquarePos)
                return findRookAttacks(position, piecePos, colour, newSquarePos, direction, squares)
            else :
                return squares
        # if the square in the direction of travel is its own, it resets to the original square and switches direction
        elif str(newSquareID)[0] == str(colour // 10) :
            if direction != [0, -1] :
                return findRookAttacks(position, piecePos, colour, piecePos, nextDirection, squares)
            else :
                return squares
            # if the square in the direction of travel is not its own, it attacks that square, resets to the original square and switches direction
        else :
            if direction != [0, -1] :
                squares.append(newSquarePos)
                return findRookAttacks(position, piecePos, colour, piecePos, nextDirection, squares)
            else :
                squares.append(newSquarePos)
                return squares
    else :
        if direction != [0, -1] :
            return findRookAttacks(position, piecePos, colour, piecePos, nextDirection, squares)
        else :
            return squares


# simple function to find queen attacks combining the rook and bishop
def findQueenAttacks(position, piecePos) :
    squares = []
    lines = findRookAttacks(position, piecePos)
    diagonals = findBishopAttacks(position, piecePos)
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
            destinationID = position[piecePos[0] + directions[i][0]][piecePos[1] + directions[i][1]]
            destinationPos = [piecePos[0] + directions[i][0], piecePos[1] + directions[i][1]]
            if destinationID == 30 or str(destinationID)[0] == str(oppositeColour)[0] :
                squares.append(destinationPos)
    return squares


def findStaticAttacks(position, piecePos) :
    pieceID = str(position[piecePos[0]][piecePos[1]])[1]
    if pieceID == "1" :
        return findPawnAttacks(position, piecePos)
    elif pieceID == "2" :
        return findKnightAttacks(position, piecePos)
    elif pieceID == "3" :
        return findBishopAttacks(position, piecePos)
    elif pieceID == "4" :
        return findRookAttacks(position, piecePos)
    elif pieceID == "5" :
        return findQueenAttacks(position, piecePos)
    elif pieceID == "6" :
        return findKingAttacks(position, piecePos)
    else :
        return []


# GUI is thx to Eddie Sharick (YouTube) https://www.youtube.com/watch?v=EnYui0e73Rs&list=PLBwF487qi8MGU81nDGaeNE1EnNEPYWKY_&ab_channel=EddieSharick
def GUI(board) :
    # pygame is initialized
    pygame.init()
    # window is initialized
    screen = pygame.display.set_mode(size=(800, 800))
    # system clock is initialized
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    running = True
    while running :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.display.quit()
                pygame.quit()
                exit()
        drawPosition(screen, board)
        clock.tick(60)
        pygame.display.flip()


# function to combine drawBoard and drawPieces
def drawPosition(screen, position) :
    drawBoard(screen)
    drawPieces(screen, position)


# function to draw a board
def drawBoard(screen) :
    colours = [pygame.Color("white"), pygame.Color("tan")]
    for rank in range(8) :
        for file in range(8) :
            colour = colours[(rank + file) % 2]
            pygame.draw.rect(screen, colour, pygame.Rect(file * 100, rank * 100, 100, 100))


def drawPieces(screen, position) :
    for rank in range(8) :
        for file in range(8) :
            piece = str(position[rank][file])
            if piece != "30" :
                screen.blit(pygame.transform.scale(pygame.image.load("images/" + piece + ".png"), (90, 90)),
                            pygame.Rect(file * 100 + 5, rank * 100 + 5, 100, 100))


# driver code
if __name__ == '__main__' :
    print(isCheck(parseFen("rnb1kbnr/pppppppp/8/4K3/8/2q5/PPPPPPPP/RNBQ1BNR w kq - 0 1", True), 10))
