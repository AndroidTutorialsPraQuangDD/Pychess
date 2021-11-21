import ChessEngine
from pygame.time import Clock
from pygame import color
import pygame

width = height = 512
size = 8  # bàn cờ 8x8
square_size = width // size
images = {}
max_fps = 15


# load ảnh từ file quân cờ vào thư viện images
def loadImages():
    images['wP'] = pygame.transform.scale(pygame.image.load(
        'quan_co/wP.png'), (square_size, square_size))
    images['wR'] = pygame.transform.scale(pygame.image.load(
        'quan_co/wR.png'), (square_size, square_size))
    images['wN'] = pygame.transform.scale(pygame.image.load(
        'quan_co/wN.png'), (square_size, square_size))
    images['wB'] = pygame.transform.scale(pygame.image.load(
        'quan_co/wB.png'), (square_size, square_size))
    images['wQ'] = pygame.transform.scale(pygame.image.load(
        'quan_co/wQ.png'), (square_size, square_size))
    images['wK'] = pygame.transform.scale(pygame.image.load(
        'quan_co/wK.png'), (square_size, square_size))
    images['bP'] = pygame.transform.scale(pygame.image.load(
        'quan_co/bP.png'), (square_size, square_size))
    images['bR'] = pygame.transform.scale(pygame.image.load(
        'quan_co/bR.png'), (square_size, square_size))
    images['bN'] = pygame.transform.scale(pygame.image.load(
        'quan_co/bN.png'), (square_size, square_size))
    images['bB'] = pygame.transform.scale(pygame.image.load(
        'quan_co/bB.png'), (square_size, square_size))
    images['bQ'] = pygame.transform.scale(pygame.image.load(
        'quan_co/bQ.png'), (square_size, square_size))
    images['bK'] = pygame.transform.scale(pygame.image.load(
        'quan_co/bK.png'), (square_size, square_size))


def main():
    screen = pygame.display.set_mode((height, width))  # kích thước cửa sổ
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    gstate = ChessEngine.Gamestate()
    validMoves = gstate.getValidmoves()
    moveMade = False
    loadImages()
    running = True
    # chưa có ô nào được chọn khi khởi tạo, theo dõi vị trí click chuột cuối cùng và có dạng tuple(hàng, cột)
    square_selected = ()
    # tập vị trí click chuột có dạng 2 tuple ((hàng, cột), (hàng, cột))
    clicks = []
    while running:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                running = False
            elif i.type == pygame.MOUSEBUTTONDOWN:  # kiểm soát con trỏ
                location = pygame.mouse.get_pos()  # tọa độ vị trí bấm của con trỏ
                cot = location[0] // square_size
                hang = location[1] // square_size
                # nếu người chơi click vào một ô 2
                if square_selected == (hang, cot):
                    square_selected = ()           # thì sẽ bỏ chọn ô đó
                    clicks = []                    # và reset tập vị trí click chuột
                else:
                    square_selected = (hang, cot)
                    # append cả lần click thứ 1 và thứ 2
                    clicks.append(square_selected)
                # nếu đã có 2 lần click chuột được lưu trong tập vị trí
                if len(clicks) == 2:
                    move = ChessEngine.Move(clicks[0], clicks[1], gstate.board)
                    print(move.getChessNotation())
                    if move in validMoves:  # nếu nước đi thực hiện nằm trong những nước đi hợp lệ thì thực hiện nước đi đó
                        gstate.makeMove(move)
                        moveMade = True
                    square_selected = ()  # reset lại ô đã chọn
                    clicks = []  # reset tập 2 vị trí di chuyển
            elif i.type == pygame.KEYDOWN:  # kiểm soát bàn phím
                if i.key == pygame.K_z:  # undo khi nhấn z
                    gstate.undoMove()
                    moveMade = True  # undo có thể coi như một nước đi vì nó thay đổi vị trí quân cờ nên cần tìm những nước đi hợp lệ sau khi undo

        if moveMade:  # nếu nước đi đã được thực hiện, tiếp tục tìm những nước đi hợp lệ mới sau nước vừa thực hiện
            validMoves = gstate.getValidmoves()
            moveMade = False

        drawGstate(screen, gstate)
        clock.tick(max_fps)
        pygame.display.flip()


def drawGstate(screen, gstate):
    drawBoard(screen)
    drawPieces(screen, gstate.board)


def drawBoard(screen):  # vẽ ra bàn cờ
    colors = [pygame.Color('white'), pygame.Color('grey')]
    for h in range(size):
        for c in range(size):
            # ô trên cùng bên trái của cả 2 bên đều là trắng
            color = colors[(h+c) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(
                c * square_size, h * square_size, square_size, square_size))


def drawPieces(screen, board):  # vẽ các quân lên trên các ô
    for h in range(size):
        for c in range(size):
            piece = board[h][c]
            if piece != '-':  # quân không phải là ô trống
                screen.blit(images[piece], pygame.Rect(
                    c * square_size, h * square_size, square_size, square_size))


if __name__ == '__main__':  # nó là main, không có tác dụng gì hơn
    main()
