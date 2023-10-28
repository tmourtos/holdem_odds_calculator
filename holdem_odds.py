from tkinter import Tk, Button, Frame
from tkinter.ttk import Style, Label, Separator
from PIL import ImageTk, Image
from pprint import pprint, pformat

from holdem_calculator import calculate_odds


class DeckCard:
    def __init__(self, name, grid_row, grid_column):
        self.name = name
        self.image = None
        self.button = None
        self.grid_row = grid_row
        self.grid_column = grid_column
        self.slot = None

    def __str__(self):
        return self.name

    def __repr__(self):
        return pformat(vars(self))


class CardSlot:
    def __init__(self, index, slot_grid_row, slot_grid_column):
        self.index = index
        self.slot_grid_row = slot_grid_row
        self.slot_grid_column = slot_grid_column
        self.deck_card = None
        self.card_grid_row = None
        self.card_grid_column = None

    def __str__(self):
        return 'Slot {}'.format(self.index)

    def __repr__(self):
        return pformat(vars(self))


class HoldemUI(Frame):
    def __init__(self):
        super().__init__()

        self._init_ui()

    def _reset(self):
        """
            Reset the application
        :return:
        """
        # Reset slots
        for _index, _card_slot in enumerate(self.card_slots):
            if _card_slot.deck_card is None:
                continue
            # Reposition card
            _card_slot.deck_card.slot = None
            _card_slot.deck_card.button.grid(row=_card_slot.card_grid_row, column=_card_slot.card_grid_column)

            # Empty slot
            _card_slot.deck_card = None
            _card_slot.card_grid_row = None
            _card_slot.card_grid_column = None
        # Reset odds
        self.win_odds_label.configure(text='')
        self.lose_odds_label.configure(text='')
        self.tie_odds_label.configure(text='')

        self.player_hand_odds_content_label.configure(text='')
        self.opponent_hand_odds_content_label.configure(text='')

    def _get_available_slot(self):
        """
            Get the next available card slot
        :return: The index of the next available card slot
        """
        for _index, _slot in enumerate(self.card_slots):
            if not _slot.deck_card:
                return _index
        else:
            return None

    def _get_hand_details(self):
        """
            Enumerate the card slots and return pocket and board cards
        :return: The pocket and board cards
        """
        _pocket = list()
        _board = list()
        for _index, _card_slot in enumerate(self.card_slots):
            if _card_slot.deck_card is None:
                continue
            if _index < 2:
                _pocket.append(_card_slot.deck_card.name)
            else:
                _board.append(_card_slot.deck_card.name)

        return _pocket, _board

    def _calculate(self, _pocket, _board):
        """
            If parameters are valid, calculate hand odds
        :param _pocket: The player pocket
        :param _board: The hand board
        :return: The odds response
        """
        if _pocket and len(_pocket) == 2:
            _pocket.extend(['?', '?'])
            if not _board or len(_board) < 3:
                _board = list()
            return calculate_odds(_pocket, _board)

    def _card_click(self, picked_card):
        """
            Hide the given object
        :param picked_card: The given object
        """
        # Return card to original position
        if picked_card.slot is not None:
            # Get original slot position
            original_card_row = self.card_slots[picked_card.slot].card_grid_row
            original_card_column = self.card_slots[picked_card.slot].card_grid_column

            # Empty slot
            self.card_slots[picked_card.slot].deck_card = None
            self.card_slots[picked_card.slot].card_grid_row = None
            self.card_slots[picked_card.slot].card_grid_column = None

            # Reposition card
            picked_card.slot = None
            picked_card.button.grid(row=original_card_row, column=original_card_column)
        else:
            available_slot = self._get_available_slot()
            if available_slot is not None:
                # Get available slot position
                available_slot_row = self.card_slots[available_slot].slot_grid_row
                available_slot_column = self.card_slots[available_slot].slot_grid_column

                # Store card in slot
                self.card_slots[available_slot].deck_card = picked_card
                self.card_slots[available_slot].card_grid_row = picked_card.grid_row
                self.card_slots[available_slot].card_grid_column = picked_card.grid_column

                # Reposition card
                picked_card.slot = available_slot
                picked_card.button.grid(row=available_slot_row, column=available_slot_column)

        # Check if calculation can be called
        _pocket, _board = self._get_hand_details()

        calculation_response = self._calculate(_pocket, _board)
        pprint(calculation_response)
        if calculation_response:
            self.win_odds_label.configure(text='{}%'.format(calculation_response['game_odds']['win']))
            self.lose_odds_label.configure(text='{}%'.format(calculation_response['game_odds']['lose']))
            self.tie_odds_label.configure(text='{}%'.format(calculation_response['game_odds']['tie']))

            _player_hand_odds = ''
            for _hand, _odds in calculation_response['hand_odds']['player']:
                _player_hand_odds += '{}: {}%\n'.format(_hand, _odds)
            self.player_hand_odds_content_label.configure(text=_player_hand_odds)

            _opponent_hand_odds = ''
            for _hand, _odds in calculation_response['hand_odds']['opponent']:
                _opponent_hand_odds += '{}: {}%\n'.format(_hand, _odds)
            self.opponent_hand_odds_content_label.configure(text=_opponent_hand_odds)

    def _init_ui(self):
        self.master.title('Texas Holdem Heads Up Calculator')

        Style().configure('TLabel', padding=(5, 5, 5, 5), font='calibri')

        self.columnconfigure(0, pad=5)
        self.columnconfigure(1, pad=5)
        self.columnconfigure(2, pad=5)
        self.columnconfigure(3, pad=5)
        self.columnconfigure(4, pad=5)
        self.columnconfigure(5, pad=5)
        self.columnconfigure(6, pad=5)
        self.columnconfigure(7, pad=5)
        self.columnconfigure(8, pad=5)
        self.columnconfigure(9, pad=5)
        self.columnconfigure(10, pad=5)
        self.columnconfigure(11, pad=5)
        self.columnconfigure(12, pad=5)
        self.columnconfigure(13, pad=5)
        self.columnconfigure(14, pad=5)
        self.columnconfigure(15, pad=5)
        self.columnconfigure(16, pad=5)
        self.columnconfigure(17, pad=5)
        self.columnconfigure(18, pad=5)
        self.columnconfigure(19, pad=5)

        self.rowconfigure(0, pad=5)
        self.rowconfigure(1, pad=5)
        self.rowconfigure(2, pad=5)
        self.rowconfigure(3, pad=5)
        self.rowconfigure(4, pad=5)

        #
        # Cards
        #

        # Spades
        self.two_s_card = DeckCard(name='2s', grid_row=0, grid_column=0)
        self.two_s_image = ImageTk.PhotoImage(Image.open('resources/2s.png').resize((63, 90), Image.LANCZOS))
        self.two_s_button = Button(self, image=self.two_s_image, borderwidth=1,
                                   command=lambda: self._card_click(self.two_s_card))
        self.two_s_card.button = self.two_s_button
        self.two_s_button.grid(row=0, column=0)

        self.three_s_card = DeckCard(name='3s', grid_row=0, grid_column=1)
        self.three_s_image = ImageTk.PhotoImage(Image.open('resources/3s.png').resize((63, 90), Image.LANCZOS))
        self.three_s_button = Button(self, image=self.three_s_image, borderwidth=1,
                                     command=lambda: self._card_click(self.three_s_card))
        self.three_s_card.button = self.three_s_button
        self.three_s_button.grid(row=0, column=1)

        self.four_s_card = DeckCard(name='4s', grid_row=0, grid_column=2)
        self.four_s_image = ImageTk.PhotoImage(Image.open('resources/4s.png').resize((63, 90), Image.LANCZOS))
        self.four_s_button = Button(self, image=self.four_s_image, borderwidth=1,
                                    command=lambda: self._card_click(self.four_s_card))
        self.four_s_card.button = self.four_s_button
        self.four_s_button.grid(row=0, column=2)

        self.five_s_card = DeckCard(name='5s', grid_row=0, grid_column=3)
        self.five_s_image = ImageTk.PhotoImage(Image.open('resources/5s.png').resize((63, 90), Image.LANCZOS))
        self.five_s_button = Button(self, image=self.five_s_image, borderwidth=1,
                                    command=lambda: self._card_click(self.five_s_card))
        self.five_s_card.button = self.five_s_button
        self.five_s_button.grid(row=0, column=3)

        self.six_s_card = DeckCard(name='6s', grid_row=0, grid_column=4)
        self.six_s_image = ImageTk.PhotoImage(Image.open('resources/6s.png').resize((63, 90), Image.LANCZOS))
        self.six_s_button = Button(self, image=self.six_s_image, borderwidth=1,
                                   command=lambda: self._card_click(self.six_s_card))
        self.six_s_card.button = self.six_s_button
        self.six_s_button.grid(row=0, column=4)

        self.seven_s_card = DeckCard(name='7s', grid_row=0, grid_column=5)
        self.seven_s_image = ImageTk.PhotoImage(Image.open('resources/7s.png').resize((63, 90), Image.LANCZOS))
        self.seven_s_button = Button(self, image=self.seven_s_image, borderwidth=1,
                                     command=lambda: self._card_click(self.seven_s_card))
        self.seven_s_card.button = self.seven_s_button
        self.seven_s_button.grid(row=0, column=5)

        self.eight_s_card = DeckCard(name='8s', grid_row=0, grid_column=6)
        self.eight_s_image = ImageTk.PhotoImage(Image.open('resources/8s.png').resize((63, 90), Image.LANCZOS))
        self.eight_s_button = Button(self, image=self.eight_s_image, borderwidth=1,
                                     command=lambda: self._card_click(self.eight_s_card))
        self.eight_s_card.button = self.eight_s_button
        self.eight_s_button.grid(row=0, column=6)

        self.nine_s_card = DeckCard(name='9s', grid_row=0, grid_column=7)
        self.nine_s_image = ImageTk.PhotoImage(Image.open('resources/9s.png').resize((63, 90), Image.LANCZOS))
        self.nine_s_button = Button(self, image=self.nine_s_image, borderwidth=1,
                                    command=lambda: self._card_click(self.nine_s_card))
        self.nine_s_card.button = self.nine_s_button
        self.nine_s_button.grid(row=0, column=7)

        self.ten_s_card = DeckCard(name='Ts', grid_row=0, grid_column=8)
        self.ten_s_image = ImageTk.PhotoImage(Image.open('resources/10s.png').resize((63, 90), Image.LANCZOS))
        self.ten_s_button = Button(self, image=self.ten_s_image, borderwidth=1,
                                   command=lambda: self._card_click(self.ten_s_card))
        self.ten_s_card.button = self.ten_s_button
        self.ten_s_button.grid(row=0, column=8)

        self.jack_s_card = DeckCard(name='Js', grid_row=0, grid_column=9)
        self.jack_s_image = ImageTk.PhotoImage(Image.open('resources/Js.png').resize((63, 90), Image.LANCZOS))
        self.jack_s_button = Button(self, image=self.jack_s_image, borderwidth=1,
                                    command=lambda: self._card_click(self.jack_s_card))
        self.jack_s_card.button = self.jack_s_button
        self.jack_s_button.grid(row=0, column=9)

        self.queen_s_card = DeckCard(name='Qs', grid_row=0, grid_column=10)
        self.queen_s_image = ImageTk.PhotoImage(Image.open('resources/Qs.png').resize((63, 90), Image.LANCZOS))
        self.queen_s_button = Button(self, image=self.queen_s_image, borderwidth=1,
                                     command=lambda: self._card_click(self.queen_s_card))
        self.queen_s_card.button = self.queen_s_button
        self.queen_s_button.grid(row=0, column=10)

        self.king_s_card = DeckCard(name='Ks', grid_row=0, grid_column=11)
        self.king_s_image = ImageTk.PhotoImage(Image.open('resources/Ks.png').resize((63, 90), Image.LANCZOS))
        self.king_s_button = Button(self, image=self.king_s_image, borderwidth=1,
                                    command=lambda: self._card_click(self.king_s_card))
        self.king_s_card.button = self.king_s_button
        self.king_s_button.grid(row=0, column=11)

        self.ace_s_card = DeckCard(name='As', grid_row=0, grid_column=12)
        self.ace_s_image = ImageTk.PhotoImage(Image.open('resources/As.png').resize((63, 90), Image.LANCZOS))
        self.ace_s_button = Button(self, image=self.ace_s_image, borderwidth=1,
                                   command=lambda: self._card_click(self.ace_s_card))
        self.ace_s_card.button = self.ace_s_button
        self.ace_s_button.grid(row=0, column=12)

        # Diamonds
        self.two_d_card = DeckCard(name='2d', grid_row=1, grid_column=0)
        self.two_d_image = ImageTk.PhotoImage(Image.open('resources/2d.png').resize((63, 90), Image.LANCZOS))
        self.two_d_button = Button(self, image=self.two_d_image, borderwidth=1,
                                   command=lambda: self._card_click(self.two_d_card))
        self.two_d_card.button = self.two_d_button
        self.two_d_button.grid(row=1, column=0)

        self.three_d_card = DeckCard(name='3d', grid_row=1, grid_column=1)
        self.three_d_image = ImageTk.PhotoImage(Image.open('resources/3d.png').resize((63, 90), Image.LANCZOS))
        self.three_d_button = Button(self, image=self.three_d_image, borderwidth=1,
                                     command=lambda: self._card_click(self.three_d_card))
        self.three_d_card.button = self.three_d_button
        self.three_d_button.grid(row=1, column=1)

        self.four_d_card = DeckCard(name='4d', grid_row=1, grid_column=2)
        self.four_d_image = ImageTk.PhotoImage(Image.open('resources/4d.png').resize((63, 90), Image.LANCZOS))
        self.four_d_button = Button(self, image=self.four_d_image, borderwidth=1,
                                    command=lambda: self._card_click(self.four_d_card))
        self.four_d_card.button = self.four_d_button
        self.four_d_button.grid(row=1, column=2)

        self.five_d_card = DeckCard(name='5d', grid_row=1, grid_column=3)
        self.five_d_image = ImageTk.PhotoImage(Image.open('resources/5d.png').resize((63, 90), Image.LANCZOS))
        self.five_d_button = Button(self, image=self.five_d_image, borderwidth=1,
                                    command=lambda: self._card_click(self.five_d_card))
        self.five_d_card.button = self.five_d_button
        self.five_d_button.grid(row=1, column=3)

        self.six_d_card = DeckCard(name='6d', grid_row=1, grid_column=4)
        self.six_d_image = ImageTk.PhotoImage(Image.open('resources/6d.png').resize((63, 90), Image.LANCZOS))
        self.six_d_button = Button(self, image=self.six_d_image, borderwidth=1,
                                   command=lambda: self._card_click(self.six_d_card))
        self.six_d_card.button = self.six_d_button
        self.six_d_button.grid(row=1, column=4)

        self.seven_d_card = DeckCard(name='7d', grid_row=1, grid_column=5)
        self.seven_d_image = ImageTk.PhotoImage(Image.open('resources/7d.png').resize((63, 90), Image.LANCZOS))
        self.seven_d_button = Button(self, image=self.seven_d_image, borderwidth=1,
                                     command=lambda: self._card_click(self.seven_d_card))
        self.seven_d_card.button = self.two_s_button
        self.seven_d_button.grid(row=1, column=5)

        self.eight_d_card = DeckCard(name='8d', grid_row=1, grid_column=6)
        self.eight_d_image = ImageTk.PhotoImage(Image.open('resources/8d.png').resize((63, 90), Image.LANCZOS))
        self.eight_d_button = Button(self, image=self.eight_d_image, borderwidth=1,
                                     command=lambda: self._card_click(self.eight_d_card))
        self.eight_d_card.button = self.eight_d_button
        self.eight_d_button.grid(row=1, column=6)

        self.nine_d_card = DeckCard(name='9d', grid_row=1, grid_column=7)
        self.nine_d_image = ImageTk.PhotoImage(Image.open('resources/9d.png').resize((63, 90), Image.LANCZOS))
        self.nine_d_button = Button(self, image=self.nine_d_image, borderwidth=1,
                                    command=lambda: self._card_click(self.nine_d_card))
        self.nine_d_card.button = self.nine_d_button
        self.nine_d_button.grid(row=1, column=7)

        self.ten_d_card = DeckCard(name='Td', grid_row=1, grid_column=8)
        self.ten_d_image = ImageTk.PhotoImage(Image.open('resources/10d.png').resize((63, 90), Image.LANCZOS))
        self.ten_d_button = Button(self, image=self.ten_d_image, borderwidth=1,
                                   command=lambda: self._card_click(self.ten_d_card))
        self.ten_d_card.button = self.ten_d_button
        self.ten_d_button.grid(row=1, column=8)

        self.jack_d_card = DeckCard(name='Jd', grid_row=1, grid_column=9)
        self.jack_d_image = ImageTk.PhotoImage(Image.open('resources/Jd.png').resize((63, 90), Image.LANCZOS))
        self.jack_d_button = Button(self, image=self.jack_d_image, borderwidth=1,
                                    command=lambda: self._card_click(self.jack_d_card))
        self.jack_d_card.button = self.jack_d_button
        self.jack_d_button.grid(row=1, column=9)

        self.queen_d_card = DeckCard(name='Qd', grid_row=1, grid_column=10)
        self.queen_d_image = ImageTk.PhotoImage(Image.open('resources/Qd.png').resize((63, 90), Image.LANCZOS))
        self.queen_d_button = Button(self, image=self.queen_d_image, borderwidth=1,
                                     command=lambda: self._card_click(self.queen_d_card))
        self.queen_d_card.button = self.queen_d_button
        self.queen_d_button.grid(row=1, column=10)

        self.king_d_card = DeckCard(name='Kd', grid_row=1, grid_column=11)
        self.king_d_image = ImageTk.PhotoImage(Image.open('resources/Kd.png').resize((63, 90), Image.LANCZOS))
        self.king_d_button = Button(self, image=self.king_d_image, borderwidth=1,
                                    command=lambda: self._card_click(self.king_d_card))
        self.king_d_card.button = self.king_d_button
        self.king_d_button.grid(row=1, column=11)

        self.ace_d_card = DeckCard(name='Ad', grid_row=1, grid_column=12)
        self.ace_d_image = ImageTk.PhotoImage(Image.open('resources/Ad.png').resize((63, 90), Image.LANCZOS))
        self.ace_d_button = Button(self, image=self.ace_d_image, borderwidth=1,
                                   command=lambda: self._card_click(self.ace_d_card))
        self.ace_d_card.button = self.ace_d_button
        self.ace_d_button.grid(row=1, column=12)

        # Clubs
        self.two_c_card = DeckCard(name='2c', grid_row=2, grid_column=0)
        self.two_c_image = ImageTk.PhotoImage(Image.open('resources/2c.png').resize((63, 90), Image.LANCZOS))
        self.two_c_button = Button(self, image=self.two_c_image, borderwidth=1,
                                   command=lambda: self._card_click(self.two_c_card))
        self.two_c_card.button = self.two_c_button
        self.two_c_button.grid(row=2, column=0)

        self.three_c_card = DeckCard(name='3c', grid_row=2, grid_column=1)
        self.three_c_image = ImageTk.PhotoImage(Image.open('resources/3c.png').resize((63, 90), Image.LANCZOS))
        self.three_c_button = Button(self, image=self.three_c_image, borderwidth=1,
                                     command=lambda: self._card_click(self.three_c_card))
        self.three_c_card.button = self.three_c_button
        self.three_c_button.grid(row=2, column=1)

        self.four_c_card = DeckCard(name='4c', grid_row=2, grid_column=2)
        self.four_c_image = ImageTk.PhotoImage(Image.open('resources/4c.png').resize((63, 90), Image.LANCZOS))
        self.four_c_button = Button(self, image=self.four_c_image, borderwidth=1,
                                    command=lambda: self._card_click(self.four_c_card))
        self.four_c_card.button = self.four_c_button
        self.four_c_button.grid(row=2, column=2)

        self.five_c_card = DeckCard(name='5c', grid_row=2, grid_column=3)
        self.five_c_image = ImageTk.PhotoImage(Image.open('resources/5c.png').resize((63, 90), Image.LANCZOS))
        self.five_c_button = Button(self, image=self.five_c_image, borderwidth=1,
                                    command=lambda: self._card_click(self.five_c_card))
        self.five_c_card.button = self.five_c_button
        self.five_c_button.grid(row=2, column=3)

        self.six_c_card = DeckCard(name='6c', grid_row=2, grid_column=4)
        self.six_c_image = ImageTk.PhotoImage(Image.open('resources/6c.png').resize((63, 90), Image.LANCZOS))
        self.six_c_button = Button(self, image=self.six_c_image, borderwidth=1,
                                   command=lambda: self._card_click(self.six_c_card))
        self.six_c_card.button = self.six_c_button
        self.six_c_button.grid(row=2, column=4)

        self.seven_c_card = DeckCard(name='7c', grid_row=2, grid_column=5)
        self.seven_c_image = ImageTk.PhotoImage(Image.open('resources/7c.png').resize((63, 90), Image.LANCZOS))
        self.seven_c_button = Button(self, image=self.seven_c_image, borderwidth=1,
                                     command=lambda: self._card_click(self.seven_c_card))
        self.seven_c_card.button = self.seven_c_button
        self.seven_c_button.grid(row=2, column=5)

        self.eight_c_card = DeckCard(name='8c', grid_row=2, grid_column=6)
        self.eight_c_image = ImageTk.PhotoImage(Image.open('resources/8c.png').resize((63, 90), Image.LANCZOS))
        self.eight_c_button = Button(self, image=self.eight_c_image, borderwidth=1,
                                     command=lambda: self._card_click(self.eight_c_card))
        self.eight_c_card.button = self.eight_c_button
        self.eight_c_button.grid(row=2, column=6)

        self.nine_c_card = DeckCard(name='9c', grid_row=2, grid_column=7)
        self.nine_c_image = ImageTk.PhotoImage(Image.open('resources/9c.png').resize((63, 90), Image.LANCZOS))
        self.nine_c_button = Button(self, image=self.nine_c_image, borderwidth=1,
                                    command=lambda: self._card_click(self.nine_c_card))
        self.nine_c_card.button = self.nine_c_button
        self.nine_c_button.grid(row=2, column=7)

        self.ten_c_card = DeckCard(name='Tc', grid_row=2, grid_column=8)
        self.ten_c_image = ImageTk.PhotoImage(Image.open('resources/10c.png').resize((63, 90), Image.LANCZOS))
        self.ten_c_button = Button(self, image=self.ten_c_image, borderwidth=1,
                                   command=lambda: self._card_click(self.ten_c_card))
        self.ten_c_card.button = self.ten_c_button
        self.ten_c_button.grid(row=2, column=8)

        self.jack_c_card = DeckCard(name='Jc', grid_row=2, grid_column=9)
        self.jack_c_image = ImageTk.PhotoImage(Image.open('resources/Jc.png').resize((63, 90), Image.LANCZOS))
        self.jack_c_button = Button(self, image=self.jack_c_image, borderwidth=1,
                                    command=lambda: self._card_click(self.jack_c_card))
        self.jack_c_card.button = self.jack_c_button
        self.jack_c_button.grid(row=2, column=9)

        self.queen_c_card = DeckCard(name='Qc', grid_row=2, grid_column=10)
        self.queen_c_image = ImageTk.PhotoImage(Image.open('resources/Qc.png').resize((63, 90), Image.LANCZOS))
        self.queen_c_button = Button(self, image=self.queen_c_image, borderwidth=1,
                                     command=lambda: self._card_click(self.queen_c_card))
        self.queen_c_card.button = self.queen_c_button
        self.queen_c_button.grid(row=2, column=10)

        self.king_c_card = DeckCard(name='Kc', grid_row=2, grid_column=11)
        self.king_c_image = ImageTk.PhotoImage(Image.open('resources/Kc.png').resize((63, 90), Image.LANCZOS))
        self.king_c_button = Button(self, image=self.king_c_image, borderwidth=1,
                                    command=lambda: self._card_click(self.king_c_card))
        self.king_c_card.button = self.king_c_button
        self.king_c_button.grid(row=2, column=11)

        self.ace_c_card = DeckCard(name='Ac', grid_row=2, grid_column=12)
        self.ace_c_image = ImageTk.PhotoImage(Image.open('resources/Ac.png').resize((63, 90), Image.LANCZOS))
        self.ace_c_button = Button(self, image=self.ace_c_image, borderwidth=1,
                                   command=lambda: self._card_click(self.ace_c_card))
        self.ace_c_card.button = self.ace_c_button
        self.ace_c_button.grid(row=2, column=12)

        # Hearts
        self.two_h_card = DeckCard(name='2h', grid_row=3, grid_column=0)
        self.two_h_image = ImageTk.PhotoImage(Image.open('resources/2h.png').resize((63, 90), Image.LANCZOS))
        self.two_h_button = Button(self, image=self.two_h_image, borderwidth=1,
                                   command=lambda: self._card_click(self.two_h_card))
        self.two_h_card.button = self.two_h_button
        self.two_h_button.grid(row=3, column=0)

        self.three_h_card = DeckCard(name='3h', grid_row=3, grid_column=1)
        self.three_h_image = ImageTk.PhotoImage(Image.open('resources/3h.png').resize((63, 90), Image.LANCZOS))
        self.three_h_button = Button(self, image=self.three_h_image, borderwidth=1,
                                     command=lambda: self._card_click(self.three_h_card))
        self.three_h_card.button = self.three_h_button
        self.three_h_button.grid(row=3, column=1)

        self.four_h_card = DeckCard(name='4h', grid_row=3, grid_column=2)
        self.four_h_image = ImageTk.PhotoImage(Image.open('resources/4h.png').resize((63, 90), Image.LANCZOS))
        self.four_h_button = Button(self, image=self.four_h_image, borderwidth=1,
                                    command=lambda: self._card_click(self.four_h_card))
        self.four_h_card.button = self.four_h_button
        self.four_h_button.grid(row=3, column=2)

        self.five_h_card = DeckCard(name='5h', grid_row=3, grid_column=3)
        self.five_h_image = ImageTk.PhotoImage(Image.open('resources/5h.png').resize((63, 90), Image.LANCZOS))
        self.five_h_button = Button(self, image=self.five_h_image, borderwidth=1,
                                    command=lambda: self._card_click(self.five_h_card))
        self.five_h_card.button = self.five_h_button
        self.five_h_button.grid(row=3, column=3)

        self.six_h_card = DeckCard(name='6h', grid_row=3, grid_column=4)
        self.six_h_image = ImageTk.PhotoImage(Image.open('resources/6h.png').resize((63, 90), Image.LANCZOS))
        self.six_h_button = Button(self, image=self.six_h_image, borderwidth=1,
                                   command=lambda: self._card_click(self.six_h_card))
        self.six_h_card.button = self.six_h_button
        self.six_h_button.grid(row=3, column=4)

        self.seven_h_card = DeckCard(name='7h', grid_row=3, grid_column=5)
        self.seven_h_image = ImageTk.PhotoImage(Image.open('resources/7h.png').resize((63, 90), Image.LANCZOS))
        self.seven_h_button = Button(self, image=self.seven_h_image, borderwidth=1,
                                     command=lambda: self._card_click(self.seven_h_card))
        self.seven_h_card.button = self.seven_h_button
        self.seven_h_button.grid(row=3, column=5)

        self.eight_h_card = DeckCard(name='8h', grid_row=3, grid_column=6)
        self.eight_h_image = ImageTk.PhotoImage(Image.open('resources/8h.png').resize((63, 90), Image.LANCZOS))
        self.eight_h_button = Button(self, image=self.eight_h_image, borderwidth=1,
                                     command=lambda: self._card_click(self.eight_h_card))
        self.eight_h_card.button = self.eight_h_button
        self.eight_h_button.grid(row=3, column=6)

        self.nine_h_card = DeckCard(name='9h', grid_row=3, grid_column=7)
        self.nine_h_image = ImageTk.PhotoImage(Image.open('resources/9h.png').resize((63, 90), Image.LANCZOS))
        self.nine_h_button = Button(self, image=self.nine_h_image, borderwidth=1,
                                    command=lambda: self._card_click(self.nine_h_card))
        self.nine_h_card.button = self.nine_h_button
        self.nine_h_button.grid(row=3, column=7)

        self.ten_h_card = DeckCard(name='Th', grid_row=3, grid_column=8)
        self.ten_h_image = ImageTk.PhotoImage(Image.open('resources/10h.png').resize((63, 90), Image.LANCZOS))
        self.ten_h_button = Button(self, image=self.ten_h_image, borderwidth=1,
                                   command=lambda: self._card_click(self.ten_h_card))
        self.ten_h_card.button = self.ten_h_button
        self.ten_h_button.grid(row=3, column=8)

        self.jack_h_card = DeckCard(name='Jh', grid_row=3, grid_column=9)
        self.jack_h_image = ImageTk.PhotoImage(Image.open('resources/Jh.png').resize((63, 90), Image.LANCZOS))
        self.jack_h_button = Button(self, image=self.jack_h_image, borderwidth=1,
                                    command=lambda: self._card_click(self.jack_h_card))
        self.jack_h_card.button = self.jack_h_button
        self.jack_h_button.grid(row=3, column=9)

        self.queen_h_card = DeckCard(name='Qh', grid_row=3, grid_column=10)
        self.queen_h_image = ImageTk.PhotoImage(Image.open('resources/Qh.png').resize((63, 90), Image.LANCZOS))
        self.queen_h_button = Button(self, image=self.queen_h_image, borderwidth=1,
                                     command=lambda: self._card_click(self.queen_h_card))
        self.queen_h_card.button = self.queen_h_button
        self.queen_h_button.grid(row=3, column=10)

        self.king_h_card = DeckCard(name='Kh', grid_row=3, grid_column=11)
        self.king_h_image = ImageTk.PhotoImage(Image.open('resources/Kh.png').resize((63, 90), Image.LANCZOS))
        self.king_h_button = Button(self, image=self.king_h_image, borderwidth=1,
                                    command=lambda: self._card_click(self.king_h_card))
        self.king_h_card.button = self.king_h_button
        self.king_h_button.grid(row=3, column=11)

        self.ace_h_card = DeckCard(name='Ah', grid_row=3, grid_column=12)
        self.ace_h_image = ImageTk.PhotoImage(Image.open('resources/Ah.png').resize((63, 90), Image.LANCZOS))
        self.ace_h_button = Button(self, image=self.ace_h_image, borderwidth=1,
                                   command=lambda: self._card_click(self.ace_h_card))
        self.ace_h_card.button = self.ace_h_button
        self.ace_h_button.grid(row=3, column=12)

        #
        # Controls & reporting
        #

        # Add visual separators
        self.horizontal_saperator = Separator(self, orient='horizontal').grid(row=4, columnspan=13, sticky='we')
        self.vertical_saperator = Separator(self, orient='vertical').grid(column=13, row=0, rowspan=5, sticky='ns')

        # Hand Controls

        # Pocket and board labels
        self.hand_controls_spacing_frame = Frame(self, height=95)
        self.hand_controls_spacing_frame.grid(row=5, column=10, sticky='we')
        self.pocket_label = Label(self, text='Pocket:', anchor='center', justify='center')
        self.pocket_label.grid(row=5, column=0, sticky='we')
        self.board_label = Label(self, text='Board:', anchor='center', justify='center')
        self.board_label.grid(row=5, column=3, sticky='we')

        # Pocket and board slots
        self.card_slots = list()
        self.card_slots.append(CardSlot(index=0, slot_grid_row=5, slot_grid_column=1))
        self.card_slots.append(CardSlot(index=1, slot_grid_row=5, slot_grid_column=2))
        self.card_slots.append(CardSlot(index=1, slot_grid_row=5, slot_grid_column=4))
        self.card_slots.append(CardSlot(index=1, slot_grid_row=5, slot_grid_column=5))
        self.card_slots.append(CardSlot(index=1, slot_grid_row=5, slot_grid_column=6))
        self.card_slots.append(CardSlot(index=1, slot_grid_row=5, slot_grid_column=7))
        self.card_slots.append(CardSlot(index=1, slot_grid_row=5, slot_grid_column=8))

        # Reporting
        # Game odds
        self.win_label = Label(self, text='Win:', anchor='n', justify='center')
        self.win_label.grid(row=5, column=10, sticky='n', pady=15)
        self.win_odds_label = Label(self, text='', justify='center')
        self.win_odds_label.grid(row=5, column=10, sticky='s', pady=25)
        self.lose_label = Label(self, text='Lose:', anchor='w', justify='center')
        self.lose_label.grid(row=5, column=11, sticky='n', pady=15)
        self.lose_odds_label = Label(self, text='', justify='center')
        self.lose_odds_label.grid(row=5, column=11, sticky='s', pady=25)
        self.tie_label = Label(self, text='Tie:', anchor='w', justify='center')
        self.tie_label.grid(row=5, column=12, sticky='n', pady=15)
        self.tie_odds_label = Label(self, text='', justify='center')
        self.tie_odds_label.grid(row=5, column=12, sticky='s', pady=25)

        # Hand Odds
        self.player_hand_odds_title_label = Label(self, text='Player Hand Odds', anchor='center', justify='center',
                                                  width=20)
        self.player_hand_odds_title_label.grid(row=0, column=14, sticky='s', padx=10)
        self.opponent_hand_odds_title_label = Label(self, text='Opponent Hand Odds', anchor='center', justify='center',
                                                    width=20)
        self.opponent_hand_odds_title_label.grid(row=0, column=15, sticky='s', padx=10)

        self.player_hand_odds_content_label = Label(self, text='', anchor='n', justify='left')
        self.player_hand_odds_content_label.grid(row=1, column=14, sticky='we', padx=10, rowspan=3)
        self.opponent_hand_odds_content_label = Label(self, text='', anchor='n', justify='left')
        self.opponent_hand_odds_content_label.grid(row=1, column=15, sticky='we', padx=10, rowspan=3)

        self.reset = Button(self, text='Reset', command=self._reset)
        self.reset.grid(row=5, column=15, sticky='we', padx=10)

        self.pack_propagate(False)
        self.pack()


if __name__ == '__main__':
    root = Tk()
    app = HoldemUI()
    root.mainloop()
