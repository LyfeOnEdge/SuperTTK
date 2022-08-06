import json
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
from ..widgets.Tabs import Tab
from ..widgets.EntryWidgets import LabeledEntry
from ..widgets.ComboboxWidgets import LabeledCombobox
from ..widgets.TextWidgets import CopyBox
from ..widgets.WidgetsCore import (
    default_pack,
    force_aspect,
    get_generated_font_images_lookup,
    get_asset,
)
from ..widgets.ScrolledCanvas import ScrolledCanvas

CANVAS_SIZE = 750
BOARD_COLOR = "#000000"
LINE_COLOR = "#ffffff"
WIN_LINE_WIDTH = 20
WIN_LINE_COLOR = "#aa00cc"
PIECE_COLOR = "white"  # Can be white or black
# Must be a valid generated char size
# 8,10,12,14,16,18,20,22,24,26,28,30,32,36,40,48,64,128,256
PIECE_SIZE = 256
PREVIEW_PIECE_SIZE = 128
ROUND_END_TEXT_COLOR = "#00aaff"
ROUND_END_TEXT_SIZE = 140
ROUND_END_DROP_SHADOW_COLOR = "#999999"
ROUND_END_DROP_SHADOW_OFFSET = (-5, 12)
TURNLABEL_TEXT_SIZE = 40
WIN_COUNT_TEXT_SIZE = 50


class TicTacToe:
    def __init__(self):
        self.players = {
            "X": 0,
            "O": 0,
        }
        self.round_number = 0  # Used to keep track of who goes first
        self.new_game()

    def new_game(self):
        self.round_number += 1
        self.game_over = False
        self.winner = None
        self.turn_number = 1
        self.board = [[None for _ in range(3)] for __ in range(3)]

    def get_current_player(self):
        return list(self.players.keys())[(self.turn_number + self.round_number) % 2]

    def place_piece(self, row, col):
        """Place a piece at a given location"""
        if self.board[row][col]:
            return  # Just do nothing
        self.board[row][col] = self.get_current_player()
        self.turn_number += 1
        return self.check_board()

    def check_row(self, row):
        """Returns the piece type if a solid row is found, otherwise returns None"""
        firstpiece = self.board[row][0]
        return [None, firstpiece][all((p == firstpiece for p in self.board[row]))]

    def check_col(self, col):
        """Returns the piece type if a solid row is found, otherwise returns None."""
        firstpiece = self.board[0][col]
        for r in range(3):
            if not self.board[r][col] == firstpiece:
                return None
        return firstpiece

    def check_board(self):
        """Check if game is won. A list of tuples containing start and end win locations"""
        win_coords = []

        # Check Columns
        for row in range(3):
            piece = self.check_row(row)
            if piece:
                self.set_winner(piece)
                win_coords.append((row, 0, row, 2))
        # Check rows
        for col in range(3):
            piece = self.check_col(col)
            if piece:
                self.set_winner(piece)
                win_coords.append((0, col, 2, col))
        # Check diagonal
        if all((self.board[0][0], self.board[1][1], self.board[2][2])):
            if (
                self.board[0][0] == self.board[1][1]
                and self.board[1][1] == self.board[2][2]
            ):
                self.set_winner(self.board[1][1])
                win_coords.append((0, 0, 2, 2))

        # Check other diagonal
        if all((self.board[0][2], self.board[1][1], self.board[2][0])):
            if (
                self.board[0][2] == self.board[1][1]
                and self.board[1][1] == self.board[2][0]
            ):
                self.set_winner(self.board[1][1])
                win_coords.append((0, 2, 2, 0))

        # Check that the board isn't full
        if not (9 - sum(sum(bool(v) for v in col) for col in self.board)):
            # Don't set winner for cat's game
            self.game_over = True

        return win_coords

    def set_winner(self, player):
        """Sets the winner and a flag to indicate the game is done."""
        if not self.winner:
            self.game_over = True
            self.winner = player
            self.players[player] = self.players[player] + 1


class TicTacToeTab(Tab):
    def __init__(self, notebook: ttk.Notebook):
        Tab.__init__(self, notebook, "TicTacToe")
        TicTacToeWidget(self).pack(fill=tk.BOTH, expand="True")


class TicTacToeWidget(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.title_font = tkfont.Font(size=ROUND_END_TEXT_SIZE, weight="bold")
        self.shadow_font = tkfont.Font(size=ROUND_END_TEXT_SIZE + 2, weight="bold")
        self.turnlabel_font = tkfont.Font(size=TURNLABEL_TEXT_SIZE)
        self.wincount_font = tkfont.Font(size=WIN_COUNT_TEXT_SIZE, weight="bold")
        self.game = TicTacToe()

        lookup = get_generated_font_images_lookup()
        big = lookup[PIECE_SIZE][PIECE_COLOR]
        small = lookup[PREVIEW_PIECE_SIZE][PIECE_COLOR]
        self.pieces = {
            "X": (tk.PhotoImage(file=big["X"]), tk.PhotoImage(file=small["X"])),
            "O": (tk.PhotoImage(file=big["O"]), tk.PhotoImage(file=small["O"])),
        }

        self.status_frame = ttk.Frame(self)
        self.status_frame.pack(expand=False, side=tk.TOP)

        self.turnvar = tk.StringVar(
            value=f"{self.game.get_current_player()}'s turn to pick."
        )
        ttk.Label(
            self.status_frame,
            textvariable=self.turnvar,
            anchor=tk.CENTER,
            style="Bold.TLabel",
            font=self.turnlabel_font,
        ).pack(fill="x", side=tk.BOTTOM)

        self.x_wins_var = tk.StringVar(value="X - 0")
        ttk.Label(
            self.status_frame,
            textvariable=self.x_wins_var,
            anchor=tk.CENTER,
            font=self.wincount_font,
        ).pack(fill="x", expand=True, side=tk.LEFT, padx=(0,100))

        self.o_wins_var = tk.StringVar(value="O - 0")
        ttk.Label(
            self.status_frame,
            textvariable=self.o_wins_var,
            anchor=tk.CENTER,
            font=self.wincount_font,
        ).pack(fill="x", expand=True, side=tk.RIGHT, padx=(100,0))

        self.frame = ttk.Frame(self)
        self.frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        self.canvas = tk.Canvas(
            self.frame, width=CANVAS_SIZE, height=CANVAS_SIZE, bg=BOARD_COLOR
        )
        self.canvas.pack(fill="y", expand=False)
        self.canvas.bind("<Motion>", self.on_move)
        self.canvas.bind("<Enter>", self.on_move)
        self.canvas.bind("<Leave>", self.on_move)
        self.canvas.bind("<Button-1>", self.on_click)

        self.draw_game()

    def draw_game(self):
        """Redraws the canvas"""

        self.canvas.delete("all")
        # Draw grid lines
        for i in range(4):
            siz = (i / 3) * CANVAS_SIZE + 2
            self.canvas.create_line(
                siz, -1, siz, CANVAS_SIZE + 1, fill=LINE_COLOR, width=4
            )
            self.canvas.create_line(
                -1, siz, CANVAS_SIZE + 1, siz, fill=LINE_COLOR, width=4
            )

        for row in range(3):
            for col in range(3):
                if self.game.board[row][col]:
                    piece_image = self.canvas.create_image(
                        ((row + 0.5) / 3) * CANVAS_SIZE,
                        ((col + 0.5) / 3) * CANVAS_SIZE,
                        image=self.pieces[self.game.board[row][col]][0],
                        anchor="center",
                    )

    def draw_game_over(self, coords):
        """Draws the game-over screen."""

        def draw_center_text(text):
            """Creates text with a drop-shadow"""
            self.canvas.create_text(
                CANVAS_SIZE / 2 + ROUND_END_DROP_SHADOW_OFFSET[0],
                CANVAS_SIZE / 2 + ROUND_END_DROP_SHADOW_OFFSET[1],
                text=text,
                fill=ROUND_END_DROP_SHADOW_COLOR,
                anchor=tk.CENTER,
                font=self.title_font,
                justify=tk.CENTER,
            )
            self.canvas.create_text(
                CANVAS_SIZE / 2,
                CANVAS_SIZE / 2,
                text=text,
                fill=ROUND_END_TEXT_COLOR,
                anchor=tk.CENTER,
                font=self.title_font,
                justify=tk.CENTER,
            )

        if coords:
            print(f"Drawing win lines - {coords}")
            for c in coords:
                c = (((v + 0.5) / 3) * CANVAS_SIZE for v in c)
                self.canvas.create_line(*c, fill=WIN_LINE_COLOR, width=WIN_LINE_WIDTH)
            draw_center_text(f"{self.game.winner}\nWins")
        else:
            print(f"Drawing tie game")
            draw_center_text("Tie\nGame")

    def on_move(self, event):
        """Handles drawing preview items when mouse moves"""
        if not self.game.game_over:
            self.draw_game()
            try:
                row = int(3 / (CANVAS_SIZE / event.x))
                col = int(3 / (CANVAS_SIZE / event.y))
                if not self.game.board[row][col]:
                    img = self.pieces[self.game.get_current_player()][1]
                    piece_image = self.canvas.create_image(
                        ((row + 0.5) / 3) * CANVAS_SIZE,
                        ((col + 0.5) / 3) * CANVAS_SIZE,
                        image=img,
                        anchor="center",
                    )
            except IndexError as e:
                pass
            except ZeroDivisionError as e:
                pass

    def on_click(self, event):
        """Handles left click"""
        if self.game.game_over:
            self.game.new_game()
            self.draw_game()
            self.turnvar.set(f"{self.game.get_current_player()}'s turn to pick.")
            return

        win_coords = self.game.place_piece(
            int(3 / (CANVAS_SIZE / event.x)), int(3 / (CANVAS_SIZE / event.y))
        )
        self.draw_game()
        if self.game.game_over:
            self.draw_game_over(win_coords)
            if self.game.winner:
                self.o_wins_var.set(f"O - {self.game.players['O']}")
                self.x_wins_var.set(f"X - {self.game.players['X']}")
            self.turnvar.set("Click for new match.")
        else:
            self.turnvar.set(f"{self.game.get_current_player()}'s turn to pick.")
