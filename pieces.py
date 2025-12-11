class Piece:
    def __init__(self, color):
        self.color = color

    def symbol(self):
        return "?"

    def moves(self, board, r, c):
        return []


class Pawn(Piece):
    def symbol(self):
        return 'P' if self.color == 'white' else 'p'

    def moves(self, board, r, c):
        dir = -1 if self.color == 'white' else 1
        moves = []
        # forward
        if board.is_empty(r + dir, c):
            moves.append((r + dir, c))
            start_row = 6 if self.color == 'white' else 1
            if r == start_row and board.is_empty(r + 2 * dir, c):
                moves.append((r + 2 * dir, c))
        # captures
        for dc in (-1, 1):
            nr, nc = r + dir, c + dc
            if board.in_bounds(nr, nc) and board.has_opponent(nr, nc, self.color):
                moves.append((nr, nc))
        return moves


class Knight(Piece):
    def symbol(self):
        return 'N' if self.color == 'white' else 'n'

    def moves(self, board, r, c):
        deltas = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
        res = []
        for dr, dc in deltas:
            nr, nc = r+dr, c+dc
            if board.in_bounds(nr, nc) and not board.has_friendly(nr, nc, self.color):
                res.append((nr, nc))
        return res


class Bishop(Piece):
    def symbol(self):
        return 'B' if self.color == 'white' else 'b'

    def moves(self, board, r, c):
        return board.slide_moves(r, c, self.color, [(1,1),(1,-1),(-1,1),(-1,-1)])


class Rook(Piece):
    def symbol(self):
        return 'R' if self.color == 'white' else 'r'

    def moves(self, board, r, c):
        return board.slide_moves(r, c, self.color, [(1,0),(-1,0),(0,1),(0,-1)])


class Queen(Piece):
    def symbol(self):
        return 'Q' if self.color == 'white' else 'q'

    def moves(self, board, r, c):
        return board.slide_moves(r, c, self.color, [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)])


class King(Piece):
    def symbol(self):
        return 'K' if self.color == 'white' else 'k'

    def moves(self, board, r, c):
        res = []
        for dr in (-1,0,1):
            for dc in (-1,0,1):
                if dr==0 and dc==0:
                    continue
                nr, nc = r+dr, c+dc
                if board.in_bounds(nr, nc) and not board.has_friendly(nr, nc, self.color):
                    res.append((nr, nc))
        return res
