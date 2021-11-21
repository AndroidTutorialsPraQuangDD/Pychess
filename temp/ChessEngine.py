class Gamestate():
    def __init__(self):
        # tạo bàn cờ với b* là quân đen và w* là quân trắng
        self.board = [
            ['bR', 'bN', 'bB', 'bQ',
                'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP',
                'bP', 'bP', 'bP', 'bP'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['wP', 'wP', 'wP', 'wP',
                'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ',
                'wK', 'wB', 'wN', 'wR']
        ]
        self.wturn = True
        self.moveLog = []

    def makeMove(self, move):
        self.board[move.start_hang][move.start_cot] = '-'
        self.board[move.end_hang][move.end_cot] = move.piece_moved
        self.moveLog.append(move)  # danh sách các bước đã đi
        self.wturn = not self.wturn  # đổi lượt

    def undoMove(self):
        if len(self.moveLog) != 0:  # cần có bước đi để thực hiện undo
            move = self.moveLog.pop()  # lấy ra bước đi gần nhất
            self.board[move.start_hang][move.start_cot] = move.piece_moved
            self.board[move.end_hang][move.end_cot] = move.piece_captured
            self.wturn = not self.wturn  # đổi lượt về thời điểm trước đó

    def getValidmoves(self):  # nước đi hợp lệ
        return self.possibleMoves()  # tạm thời chưa cân nhắc đến

    def possibleMoves(self):  # nước có thể đi
        moves = []
        for h in range(8):  # số hàng
            # for h in range(len(self.board)):
            for c in range(8):  # số cột
                # for c in range(len(self.board[r])):
                turn = self.board[h][c][0]
                if(turn == 'w' and self.wturn) or (turn == 'b' and not self.wturn):
                    # nếu quân cờ là màu trắng và đang ở trong lượt bên trắng hoặc ngược lại
                    piece = self.board[h][c][1]  # tên quân cờ
                    if piece == 'P':
                        if self.wturn:
                            if self.board[h - 1][c] == '-':
                                moves.append(
                                    Move((h, c), (h - 1, c), self.board))
                            if h == 6 and self.board[h - 2][c] == '-':
                                moves.append(
                                    Move((h, c), (h - 2, c), self.board))
                    elif piece == 'R':
                        self.R_possibleMoves(h, c, moves)
                    elif piece == 'N':
                        self.N_possibleMoves(h, c, moves)
                    elif piece == 'B':
                        self.B_possibleMoves(h, c, moves)
                    elif piece == 'Q':
                        self.Q_possibleMoves(h, c, moves)
                    elif piece == 'K':
                        self.K_possibleMoves(h, c, moves)
        return moves

    # tìm tất cả các nước có thể đi của quân tốt có vị trí h, c

    # tìm tất cả các nước có thể đi của quân xe có vị trí h, c

    def R_possibleMoves(self, h, c, moves):
        pass

    # tìm tất cả các nước có thể đi của quân mã có vị trí h, c
    def N_possibleMoves(self, h, c, moves):
        pass

    # tìm tất cả các nước có thể đi của quân tượng có vị trí h, c
    def B_possibleMoves(self, h, c, moves):
        pass

    # tìm tất cả các nước có thể đi của quân hậu có vị trí h, c
    def Q_possibleMoves(self, h, c, moves):
        pass

    # tìm tất cả các nước có thể đi của quân vua có vị trí h, c
    def K_possibleMoves(self, h, c, moves):
        pass


class Move():

    ranksToRows = {
        '1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0
    }
    rowsToRanks = {
        v: k for k, v in ranksToRows.items()
    }
    filesToCols = {
        'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7
    }
    colsTofiles = {
        v: k for k, v in filesToCols.items()
    }

    def __init__(self, start_square, end_square, board):
        self.start_hang = start_square[0]
        self.start_cot = start_square[1]
        self.end_hang = end_square[0]
        self.end_cot = end_square[1]
        # lưu lại quân đã di chuyển
        self.piece_moved = board[self.start_hang][self.start_cot]
        # lưu lại quân đã bị ăn
        self.piece_captured = board[self.end_hang][self.end_cot]
        self.moveID = self.start_hang * 1000 + self.start_cot * \
            100 + self.end_hang * 10 + self.end_cot  # moveid
        print(self.moveID)

        # overriding ?????????????????????
        def __eq__(self, other):
            if isinstance(other, Move):
                return self.moveID == other.moveID
            return False

    def getChessNotation(self):
        return self.getRankFile(self.start_hang, self.start_cot) + self.getRankFile(self.end_hang, self.end_cot)

    def getRankFile(self, hang, cot):
        return self.colsTofiles[cot] + self.rowsToRanks[hang]
