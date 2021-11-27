
import pygame as p
from pygame.time import Clock
import ChessEngine

width = height = 512
size = 8
square_size = width // size
max_fps = 15
images = {}

def loadImages():
    images['wP'] = p.transform.scale(p.image.load(
        'quan_co/wP.png'), (square_size, square_size))
    images['wR'] = p.transform.scale(p.image.load(
        'quan_co/wR.png'), (square_size, square_size))
    images['wN'] = p.transform.scale(p.image.load(
        'quan_co/wN.png'), (square_size, square_size))
    images['wB'] = p.transform.scale(p.image.load(
        'quan_co/wB.png'), (square_size, square_size))
    images['wQ'] = p.transform.scale(p.image.load(
        'quan_co/wQ.png'), (square_size, square_size))
    images['wK'] = p.transform.scale(p.image.load(
        'quan_co/wK.png'), (square_size, square_size))
    images['bP'] = p.transform.scale(p.image.load(
        'quan_co/bP.png'), (square_size, square_size))
    images['bR'] = p.transform.scale(p.image.load(
        'quan_co/bR.png'), (square_size, square_size))
    images['bN'] = p.transform.scale(p.image.load(
        'quan_co/bN.png'), (square_size, square_size))
    images['bB'] = p.transform.scale(p.image.load(
        'quan_co/bB.png'), (square_size, square_size))
    images['bQ'] = p.transform.scale(p.image.load(
        'quan_co/bQ.png'), (square_size, square_size))
    images['bK'] = p.transform.scale(p.image.load(
        'quan_co/bK.png'), (square_size, square_size))


def main():
    p.init()
    screen = p.display.set_mode((width, height))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    loadImages()
    running = True
    square_selected = ()
    clicks = []
    gameOver = False
    drawText(screen, 'here')

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos()
                    col = location[0] // square_size
                    row = location[1] // square_size
                    if square_selected == (row, col):
                        square_selected = ()
                        clicks = []
                    else:
                        square_selected = (row, col)
                        clicks.append(square_selected)
                    if len(clicks) == 2:  # sau 2 lần click chuột thì thực hiện nước đi
                        move = ChessEngine.Move(clicks[0], clicks[1], gs.board)
                        # print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                square_selected = ()
                                clicks = []
                        if not moveMade:
                            clicks = [square_selected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                if e.key == p.K_r:  # reset game khi nhấn r
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    square_selected = ()
                    clicks = []
                    moveMade = False

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs, validMoves, square_selected)

        if gs.checkMate:
            gameOver = True
            if gs.wturn:
                drawText(screen, 'Black wins')
            else:
                drawText(screen, 'White wins')
        elif gs.staleMate:
            gameOver = True
            drawText(screen, 'Draw')

        clock.tick(max_fps)
        p.display.flip()


def highlightSquares(screen, gs, validMoves, square_selected):
    if square_selected != ():
        r, c = square_selected
        # ô được chọn là 1 quân có thể di chuyển
        if gs.board[r][c][0] == ('w' if gs.wturn else 'b'):
            # highlight ô được chọn
            s = p.Surface((square_size, square_size))
            s.set_alpha(100)  # transparency value
            s.fill(p.Color('blue'))
            screen.blit(s, (c*square_size, r*square_size))
            # highlight các ô có thể đi
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (square_size*move.endCol,
                                square_size*move.endRow))


def drawGameState(screen, gs, validMoves, square_selected):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, square_selected)
    drawPieces(screen, gs.board)


def drawBoard(screen):
    colors = [p.Color('white'), p.Color('gray')]
    for r in range(size):
        for c in range(size):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*square_size, r *
                        square_size, square_size, square_size))


def drawPieces(screen, board):
    for r in range(size):
        for c in range(size):
            piece = board[r][c]
            if piece != '-':
                screen.blit(images[piece], p.Rect(
                    c*square_size, r*square_size, square_size, square_size))


def drawText(screen, text):
    font = p.font.SysFont('Helvitca', 32, True, False)
    textObject = font.render(text, 0, p.Color('black'))
    textLocation = p.Rect(0, 0, width, height).move(
        width/2 - textObject.get_width()//2, height/2 - textObject.get_height()//2)
    screen.blit(textObject, textLocation)


if __name__ == '__main__':
    main()
