# dictionaries - used for functions
pieceDict = {"P": 1, "N": 2, "B": 3, "R": 4, "Q": 5, "K": 6}
reversePieceDict = {0: ".", 1: "P", 2: "N", 3: "B", 4: "R", 5: "Q", 6: "K",
                    "0": ".", "1": "P", "2": "N", "3": "B", "4": "R", "5": "Q", "6": "K"}
fileDict = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}


# clears board to empty - used for FEN
def clearBoard():
    return [[30, 30, 30, 30, 30, 30, 30, 30],
            [30, 30, 30, 30, 30, 30, 30, 30],
            [30, 30, 30, 30, 30, 30, 30, 30],
            [30, 30, 30, 30, 30, 30, 30, 30],
            [30, 30, 30, 30, 30, 30, 30, 30],
            [30, 30, 30, 30, 30, 30, 30, 30],
            [30, 30, 30, 30, 30, 30, 30, 30],
            [30, 30, 30, 30, 30, 30, 30, 30]]


# resets board to starting position
def startBoard():
    return [[14, 12, 13, 15, 16, 13, 12, 14],
            [11, 11, 11, 11, 11, 11, 11, 11],
            [30, 30, 30, 30, 30, 30, 30, 30],
            [30, 30, 30, 30, 30, 30, 30, 30],
            [30, 30, 30, 30, 30, 30, 30, 30],
            [30, 30, 30, 30, 30, 30, 30, 30],
            [21, 21, 21, 21, 21, 21, 21, 21],
            [24, 22, 23, 25, 26, 23, 22, 24]]


# function to parse fen codes - used to load positions
def parseFen(fen) :
    # these are variables for all the FEN fields
    position = clearBoard()
    indexed = fen.split()
    placements = indexed[0].split("/")
    canCastle = [False, False, False, False]
    halfmove = int(indexed[4])
    fullmove = int(indexed[5])
    scrolling = True
    rank = 7
    # iterates through the FEN placement notation to construct a board
    while scrolling :
        file = 0
        increment = 0
        placing = True
        while placing :
            if placements[rank][increment].upper() not in pieceDict :
                file += int(placements[rank][increment])
            elif placements[rank][increment].isupper() :
                position[rank][file] = pieceDict[placements[rank][increment]] + 20
                file += 1
            else :
                position[rank][file] = pieceDict[placements[rank][increment].upper()] + 10
                file += 1
            if file == 8 :
                placing = False
            else :
                increment += 1
        if rank == 0 :
            scrolling = False
        else :
            rank -= 1
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
    if indexed[3] == "-" :
        enPassant = [None, None]
    else :
        enPassant = [int(indexed[3][1]), fileDict[indexed[3][0]]]
    return position, colour, canCastle, enPassant, halfmove, fullmove


# checks if a move is legal - placeholder for now
def isLegal(piece, start, destination, special):
    return True


# checks if a move causes checkmate
def isCheckmate(position):
    return True


# confirm move on board - this is separate from sendMove to (hopefully) make implementing chess bots easier
def move(position, piece, start, destination, special="-1"):
    # first checks if move is legal
    if isLegal(piece, start, destination, special):
        # default state, no special moves
        if special == "-1":
            position[start[0]][start[1]] = 30  # starting square of that piece is reset to empty
            position[destination[0]][destination[1]] = piece  # destination square is set to the piece
            return position
        # castling
        elif special == "short":
            position[start[0]][start[1]] = 30  # starting square of the king is cleared
            position[destination[0]][destination[1]] = piece  # destination square of the king is set
            position[destination[0]][destination[1] + 1] = 30
            position[destination[0]][destination[1] - 1] = 10 * int(str(piece)[0]) + pieceDict["R"]  # castles
            return position
        elif special == "long":
            position[start[0]][start[1]] = 30  # starting square of the king is cleared
            position[destination[0]][destination[1]] = piece  # destination square of the king is set
            position[destination[0]][destination[1] - 2] = 30
            position[destination[0]][destination[1] + 1] = 10 * int(str(piece)[0]) + pieceDict["R"]  # castles
            return position
        # promotion
        elif str(special)[1] in reversePieceDict:
            position[start[0]][start[1]] = 30  # starting square of the pawn is set to empty
            position[destination[0]][destination[1]] = special  # destination square is set to the piece
            return position
        # handles en passant
        elif special == "en passant":
            position[start[0]][start[1]] = 30  # starting square of the pawn  is reset to empty
            position[destination[0]][destination[1]] = piece  # destination square is set to the piece
            if str(piece)[0] == "1":
                position[destination[0] - 1][destination[1]] = 30  # pawn is captured
            if str(piece)[0] == "2":
                position[destination[0] + 1][destination[1]] = 30  # pawn is captured
            return position


# function to parse user inputs for the move function
def sendMove(board, string, player):
    indexed = [string[0], string[1:3], string[3:5]]  # creates an easier to parse list of the args
    sending = [-1, [-1, -1], [-1, -1], "-1"]  # empty placeholder list
    sending[0] = pieceDict[indexed[0].upper()] + player  # finds the correct piece that the player wants to move
    sending[1][0] = int(indexed[1][1]) - 1  # finds the rank of the start
    sending[1][1] = fileDict[indexed[1][0]]  # file of start
    sending[2][0] = int(indexed[2][1]) - 1  # rank of destination
    sending[2][1] = fileDict[indexed[2][0]]  # file of destination
    if sending[0] == 16 and sending[1] == [0, 4] and sending[2] == [0, 6]:
        sending[3] = "short"
    elif sending[0] == 26 and sending[1] == [7, 4] and sending[2] == [7, 6]:
        sending[3] = "short"
    elif sending[0] == 16 and sending[1] == [0, 4] and sending[2] == [0, 2]:
        sending[3] = "long"
    elif sending[0] == 26 and sending[1] == [7, 4] and sending[2] == [7, 2]:
        sending[3] = "long"
    elif str(sending[0])[1] == "1" and \
            abs(sending[2][0] - sending[1][0]) == 1 and \
            abs(sending[2][1] - sending[1][1]) == 1 and \
            board[sending[2][0]][sending[2][1]] == 30:
        sending[3] = "en passant"
    elif len(string) == 6:
        sending[3] = pieceDict[string[3]] + player
    return move(board, sending[0], sending[1], sending[2], sending[3])


# prints the current chess board (GUI stand-in), iterates through every board piece to print the correct symbol
def displayPosition(position):
    for i in range(8):
        print("    ", end="")
        print(i + 1, end=" ")
        for j in range(8):
            if str(position[i][j])[0] == "1":
                print("\033[1m" + reversePieceDict[int(str(position[i][j])[1])] + "\033[0m", end=" ")
            elif str(position[i][j])[0] == "2":
                print("\033[36m\033[1m" + reversePieceDict[int(str(position[i][j])[1])] + "\033[0m", end=" ")
            else:
                print(".", end=" ")
        print("")
    print("      a b c d e f g h")


# basic PVP mechanics - rules parameter can be used for implementing multiple game modes
def PvP(rules="default"):
    board = startBoard()
    playing = True
    turn = 1
    player = 10
    while playing:
        print("\n\n---------------------------\n\n   ", end="")
        if player == 10:
            print("\033[1mWHITE\033[0m to move " + "(turn " + str(turn) + ")", end="\n\n")
        else:
            print("\033[36m\033[1mBLACK\033[0m to move " + "(turn " + str(turn) + ")", end="\n\n")
        displayPosition(board)
        print("")
        board = sendMove(board, input("     Input move: "), player)
        if player == 10:
            player = 20
        else:
            player = 10
        turn += 1


# driver code
if __name__ == '__main__':
    displayPosition(parseFen("rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2")[0])
