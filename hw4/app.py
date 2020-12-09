from hw4 import TicTacToe

def main():

    while True:
        chosen = int(input('Input 1 (start first) or 2 (start second): '))

        if chosen == 1:
            chosen = 'X'
            break
        elif chosen == 2:
            chosen = 'O'
            break

    g = TicTacToe(chosen)
    g.play()

if __name__ == "__main__":
    main()