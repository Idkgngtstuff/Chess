import tkinter as tk
board = [
    ["♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜"],
    ["♟", "♟", "♟", "♟", "♟", "♟", "♟", "♟"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["♙", "♙", "♙", "♙", "♙", "♙", "♙", "♙"],
    ["♖", "♘", "♗", "♕", "♔", "♗", "♘", "♖"],
]
W_PIECES = {"♙", "♖", "♘", "♗", "♕", "♔"}
B_PIECES = {"♟", "♜", "♞", "♝", "♛", "♚"}
pieces = {
    "white": {
        "pawn": "♙",
        "rook": "♖",
        "knight": "♘",
        "bishop": "♗",
        "queen": "♕",
        "king": "♔",
    },
    "black": {
        "pawn": "♟",
        "rook": "♜",
        "knight": "♞",
        "bishop": "♝",
        "queen": "♛",
        "king": "♚",
    }
}
PIECE_TYPES = {
    symbol: kind
    for color_pieces in pieces.values()
    for kind, symbol in color_pieces.items()
}
def new_board():
          return [
              ["♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜"],
              ["♟"] * 8,
              [""] * 8, [""] * 8, [""] * 8, [""] * 8,
              ["♙"] * 8,
              ["♖", "♘", "♗", "♕", "♔", "♗", "♘", "♖"],
          ]


class ChessApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Chess App")
        self.master.geometry("400x400")
        self.master.resizable(False, False)

        self.canvas = tk.Canvas(self.master, width=400, height=400)
        self.canvas.pack()
        self.master.bind("<Button-1>", self.on_click)
        self.selected_square = None
        self.turn = "white"
        self.game_over = False

        self.draw_board()

    def draw_board(self):
        square_size = 50
        for row in range(8):
            for col in range(8):
                x1 = col * square_size
                y1 = row * square_size
                x2 = x1 + square_size
                y2 = y1 + square_size
                color = "#f0d9b5" if (row + col) % 2 == 0 else "#b58863"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
                piece = board[row][col]
                if piece:
                    self.canvas.create_text(
                        x1 + square_size / 2,
                        y1 + square_size / 2,
                        text=piece,
                        fill="black" if piece in W_PIECES else "white",
                        font=("Arial", 24),
                    )
    def update_board(self, new_board):
        global board
        board = new_board
        self.canvas.delete("all")
        self.draw_board()
        
    def on_click(self, event):
        if self.game_over:
            return
        col = event.x // 50
        row = event.y // 50
        if not (0 <= row < 8 and 0 <= col < 8):
            return

        if self.selected_square is None:
            piece = self.get_piece_at(row, col)
            if piece and self.get_piece_color(piece) == self.turn:
                self.selected_square = (row, col)
                self.highlight_square(row, col, "yellow")
                for r, c in self.get_valid_moves(row, col):
                    self.highlight_square(r, c, "green")
        else:
            from_row, from_col = self.selected_square
            self.selected_square = None
            if self.is_legal_move(from_row, from_col, row, col):
                self.move_piece(from_row, from_col, row, col)
                self.turn = "black" if self.turn == "white" else "white"
                self.update_game_status()
            else:
                self.update_board(board)

    def reset_board(self):
        global board
        board = [
            ["♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜"],
            ["♟", "♟", "♟", "♟", "♟", "♟", "♟", "♟"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["♙", "♙", "♙", "♙", "♙", "♙", "♙", "♙"],
            ["♖", "♘", "♗", "♕", "♔", "♗", "♘", "♖"],
        ]
        self.update_board(board)


    def get_piece_at(self, row, col):
        if 0 <= row < 8 and 0 <= col < 8:
            return board[row][col]
        return None

    def is_valid_move(self, from_row, from_col, to_row, to_col):
        if not (0 <= from_row < 8 and 0 <= from_col < 8 and 0 <= to_row < 8 and 0 <= to_col < 8):
            return False
        piece = board[from_row][from_col]
        if piece == "":
            return False
        target_piece = board[to_row][to_col]
        if piece in W_PIECES and target_piece in W_PIECES:
            return False
        if piece in B_PIECES and target_piece in B_PIECES:
            return False
        dr = to_row - from_row
        dc = to_col - from_col
        if dr == 0 and dc == 0:
            return False

        kind = PIECE_TYPES[piece]
        if kind == "knight":
            return (abs(dr), abs(dc)) in {(1, 2), (2, 1)}
        if kind == "king":
            return max(abs(dr), abs(dc)) == 1
        if kind == "rook":
            return (dr == 0 or dc == 0) and self.path_clear(from_row, from_col, to_row, to_col)
        if kind == "bishop":
            return abs(dr) == abs(dc) and self.path_clear(from_row, from_col, to_row, to_col)
        if kind == "queen":
            straight_or_diagonal = dr == 0 or dc == 0 or abs(dr) == abs(dc)
            return straight_or_diagonal and self.path_clear(from_row, from_col, to_row, to_col)
        if kind == "pawn":
            direction = -1 if piece in W_PIECES else 1
            start_row = 6 if piece in W_PIECES else 1


    # one square forward, onto an empty square
            if dc == 0 and dr == direction and target_piece == "":
                return True

    # two squares forward from the starting row, if both squares are empty
            if (dc == 0 and dr == 2 * direction and from_row == start_row
            and target_piece == ""
            and board[from_row + direction][from_col] == ""):
                return True

    # diagonal capture, only if there's a piece to capture
            if abs(dc) == 1 and dr == direction and target_piece != "":
                return True

            return False   
    
    def get_valid_moves(self, row, col):
        if not (0 <= row < 8 and 0 <= col < 8):
            return []
        piece = board[row][col]
        if piece == "":
            return []
        valid_moves = []
        for r in range(8):
            for c in range(8):
                if self.is_legal_move(row, col, r, c):
                    valid_moves.append((r, c))
        return valid_moves
       
    def highlight_square(self, row, col, color):
        if 0 <= row < 8 and 0 <= col < 8:
            square_size = 50
            x1 = col * square_size
            y1 = row * square_size
            x2 = x1 + square_size
            y2 = y1 + square_size
            self.canvas.create_rectangle(x1, y1, x2, y2, outline=color, width=3, tags="highlight")
        
                

    def move_piece(self, from_row, from_col, to_row, to_col):
            if 0 <= from_row < 8 and 0 <= from_col < 8 and 0 <= to_row < 8 and 0 <= to_col < 8:
                piece = board[from_row][from_col]
                board[to_row][to_col] = piece
                board[from_row][from_col] = ""
                self.update_board(board)

    def get_piece_color(self, piece):
        if piece in W_PIECES:
            return "white"
        elif piece in B_PIECES:
            return "black"
        return None
    
    
    def path_clear(self, from_row, from_col, to_row, to_col):
        if from_row == to_row:
            step = 1 if to_col > from_col else -1
            for col in range(from_col + step, to_col, step):
                if board[from_row][col] != "":
                    return False
        elif from_col == to_col:
            step = 1 if to_row > from_row else -1
            for row in range(from_row + step, to_row, step):
                if board[row][from_col] != "":
                    return False
        elif abs(to_row - from_row) == abs(to_col - from_col):
            row_step = 1 if to_row > from_row else -1
            col_step = 1 if to_col > from_col else -1
            row, col = from_row + row_step, from_col + col_step
            while row != to_row and col != to_col:
                if board[row][col] != "":
                    return False
                row += row_step
                col += col_step
        return True

    def find_king(self, color):
        king_symbol = pieces[color]["king"]
        for row in range(8):
            for col in range(8):
                if board[row][col] == king_symbol:
                    return (row, col)
        return None

    def is_in_check(self, color):
        king_pos = self.find_king(color)
        if not king_pos:
            return False
        king_row, king_col = king_pos
        opponent_color = "black" if color == "white" else "white"
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece and self.get_piece_color(piece) == opponent_color:
                    if self.is_valid_move(row, col, king_row, king_col):
                        return True
        return False

    def leaves_king_in_check(self, from_row, from_col, to_row, to_col):
        piece = board[from_row][from_col]
        captured = board[to_row][to_col]
        color = self.get_piece_color(piece)
        
        board[to_row][to_col] = piece
        board[from_row][from_col] = ""
        in_check = self.is_in_check(color)
        board[from_row][from_col] = piece
        board[to_row][to_col] = captured
        return in_check
        
    def is_legal_move(self, from_row, from_col, to_row, to_col):
            return (self.is_valid_move(from_row, from_col, to_row, to_col)
            and not self.leaves_king_in_check(from_row, from_col, to_row, to_col))

    def has_legal_moves(self, color):
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece and self.get_piece_color(piece) == color:
                    for r in range(8):
                        for c in range(8):
                            if self.is_legal_move(row, col, r, c):
                                return True
        return False


    def update_game_status(self):
        if not self.has_legal_moves(self.turn):
            self.game_over = True
            if self.is_in_check(self.turn):
                self.master.title(f"Checkmate! {self.turn.capitalize()} loses")
            else:
                self.master.title("Stalemate - draw")
        elif self.is_in_check(self.turn):
            self.master.title(f"Chess App - {self.turn.capitalize()} is in check")
        else:
            self.master.title("Chess App")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChessApp(root)
    root.mainloop()
