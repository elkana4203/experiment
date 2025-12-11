import sys
from board import Board


def parse_move(text):
    text = text.strip()
    text = text.replace('-', '').replace(' ', '')
    if len(text) == 4:
        return text[0:2], text[2:4]
    return None


def demo_game():
    b = Board()
    moves = ['e2e4','e7e5','g1f3','b8c6','f1c4','g8f6']
    color = 'white'
    for m in moves:
        parsed = parse_move(m)
        if not parsed:
            continue
        s, d = parsed
        src = b.algebraic_to_coord(s)
        dst = b.algebraic_to_coord(d)
        ok, msg = b.move(src, dst, color)
        print(color, m, ok, msg)
        b.print()
        color = 'black' if color == 'white' else 'white'


def repl():
    b = Board()
    color = 'white'
    while True:
        b.print()
        inp = input(f"{color}> ").strip()
        if inp == 'quit' or inp == 'exit' or inp == 'resign':
            print('Bye')
            break
        if inp == 'board':
            continue
        parsed = parse_move(inp)
        if not parsed:
            print('Use move format like e2e4')
            continue
        s, d = parsed
        src = b.algebraic_to_coord(s)
        dst = b.algebraic_to_coord(d)
        if not src or not dst:
            print('Invalid squares')
            continue
        ok, msg = b.move(src, dst, color)
        print(msg)
        if ok:
            color = 'black' if color == 'white' else 'white'


if __name__ == '__main__':
    if '--demo' in sys.argv:
        demo_game()
    else:
        repl()
