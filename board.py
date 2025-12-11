from pieces import Pawn, Knight, Bishop, Rook, Queen, King


class Board:
    def __init__(self):
        self.squares = [[None for _ in range(8)] for _ in range(8)]
        self.reset()

    def reset(self):
        # setup pawns
        for c in range(8):
            self.squares[6][c] = Pawn('white')
            self.squares[1][c] = Pawn('black')
        back_white = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        back_black = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for c, cls in enumerate(back_white):
            self.squares[7][c] = cls('white')
            self.squares[0][c] = back_black[c]('black')

    def in_bounds(self, r, c):
        return 0 <= r < 8 and 0 <= c < 8

    def is_empty(self, r, c):
        return self.in_bounds(r, c) and self.squares[r][c] is None

    def has_opponent(self, r, c, color):
        return self.in_bounds(r, c) and self.squares[r][c] is not None and self.squares[r][c].color != color

    def has_friendly(self, r, c, color):
        return self.in_bounds(r, c) and self.squares[r][c] is not None and self.squares[r][c].color == color

    def slide_moves(self, r, c, color, directions):
        res = []
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            while self.in_bounds(nr, nc):
                if self.squares[nr][nc] is None:
                    res.append((nr, nc))
                else:
                    if self.squares[nr][nc].color != color:
                        res.append((nr, nc))
                    break
                nr += dr; nc += dc
        return res

    def find_king(self, color):
        for r in range(8):
            for c in range(8):
                p = self.squares[r][c]
                if p and isinstance(p, King) and p.color == color:
                    return (r, c)
        return None

    def is_square_attacked(self, r, c, by_color):
        # naive: iterate opponent pieces and see if any can move to r,c
        for rr in range(8):
            for cc in range(8):
                p = self.squares[rr][cc]
                if p and p.color == by_color:
                    # For pawn, only consider capture moves
                    if isinstance(p, Pawn):
                        dir = -1 if by_color == 'white' else 1
                        for dc in (-1, 1):
                            if (rr + dir, cc + dc) == (r, c):
                                return True
                    else:
                        for mv in p.moves(self, rr, cc):
                            if mv == (r, c):
                                return True
        return False

    def would_cause_check(self, src, dst):
        sr, sc = src; dr, dc = dst
        piece = self.squares[sr][sc]
        target = self.squares[dr][dc]
        self.squares[dr][dc] = piece
        self.squares[sr][sc] = None
        king_pos = self.find_king(piece.color)
        in_check = False
        if king_pos:
            in_check = self.is_square_attacked(king_pos[0], king_pos[1], 'white' if piece.color == 'black' else 'black')
        # undo
        self.squares[sr][sc] = piece
        self.squares[dr][dc] = target
        return in_check

    def move(self, src, dst, color):
        sr, sc = src; dr, dc = dst
        if not (self.in_bounds(sr, sc) and self.in_bounds(dr, dc)):
            return False, 'out of bounds'
        piece = self.squares[sr][sc]
        if piece is None:
            return False, 'no piece at source'
        if piece.color != color:
            return False, 'not your piece'
        legal = piece.moves(self, sr, sc)
        if (dr, dc) not in legal:
            return False, 'illegal move for piece'
        if self.would_cause_check((sr,sc),(dr,dc)):
            return False, 'move would leave king in check'
        # perform
        self.squares[dr][dc] = piece
        self.squares[sr][sc] = None
        # pawn promotion simple: promote to Queen
        if isinstance(piece, Pawn) and (dr == 0 or dr == 7):
            self.squares[dr][dc] = Queen(piece.color)
        return True, 'ok'

    def algebraic_to_coord(self, s):
        s = s.strip()
        if len(s) != 2:
            return None
        file = s[0]
        rank = s[1]
        c = ord(file) - ord('a')
        r = 8 - int(rank)
        if not self.in_bounds(r, c):
            return None
        return (r, c)

    def coord_to_algebraic(self, r, c):
        return f"{chr(ord('a')+c)}{8-r}"

    def print(self):
        print('  +-----------------+')
        for r in range(8):
            row = self.squares[r]
            print(8-r, end=' | ')
            for c in range(8):
                p = row[c]
                ch = p.symbol() if p else '.'
                print(ch, end=' ')
            print('|')
        print('  +-----------------+')
        print('    a b c d e f g h')
