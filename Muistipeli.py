# TIE-02100 Johdatus ohjelmointiin
# Ville-Valtteri Litmanen, litmanen@student.tut.fi, opiskelijanumero: 272102
# Skaalautuvan Graafisen käyttöliittymän suunnitteleminen ja toteuttaminen
# Status: READY

""" Ohjelman on tarkoitus olla muistipeli, jossa käyttäjä klikkaa hiirellä
kortteja kääntääkseen ne ja perinteisesti yrittää löytää jokaiselle kuvalle
parin. Pyrin toteuttamaan skaalautuvan käyttöliittymän. """

from tkinter import *
from random import shuffle
import time


CARDPICS = ["gif01.gif", "gif02.gif", "gif03.gif", "gif04.gif",
            "gif05.gif", "gif06.gif", "gif07.gif", "gif08.gif"]

TEMPLATE = "template.gif"

CARD_NUMBER = 16


class CardGame:
    def __init__(self):
        self.__window = Tk()
        self.__window.title("Muistipeli")

        self.__button_1_status = False
        self.__button_2_status = False

        self.__previous_index = None
        self.__randicards = {}

        self.__cardpics = []
        for picfile in CARDPICS:
            pic = PhotoImage(file=picfile)
            self.__cardpics.append(pic)

        self.__template = PhotoImage(file=TEMPLATE)

        self.__cardpiclabels = []

        for i in range(CARD_NUMBER):
            # Sijoittaa kortit paikoilleen
            uusi_nappi = Button(self.__window)
            if i in range(4):
                uusi_nappi.grid(row=0, column=2 + i)
            elif i in range(8):
                uusi_nappi.grid(row=1, column=2 + i - 4)
            elif i in range(12):
                uusi_nappi.grid(row=2, column=2 + i - 8)
            elif i in range(16):
                uusi_nappi.grid(row=3, column=2 + i - 12)
            self.__cardpiclabels.append(uusi_nappi)

        self.__game_over_text = Label(self.__window,
                               text="Congratulations! You found all the pairs.")

        self.__quit_game = Button(self.__window, text="Quit", command=self.exit)
        self.__quit_game.grid(row=7, column=4)

        self.__new_game = Button(self.__window, text="New Game",
                              command=self.start_new_game)
        self.__new_game.grid(row=7, column=2)

        self.__turns = 0   # Laskee käytettyjen vuorojen/käännettyjen korttien määrää
        self.__turns_text= Label(text="Turns: {:}".format(self.__turns))
        self.__turns_text.grid(row=4, column=2)

        self.__found_pairs = 0  # Pelaajan löytämät parit
        self.__best_score = None  # Kaikkien yritysten kesken pienin vuoromäärä

        self.randomize_pics()

    def start_new_game(self):
        # Asettaa kortit takaisin selkäpuoli ylöspäin ja randomisoi kortit.
        self.__game_over_text.grid_remove()
        self.__turns = 0
        self.__turns_text.configure(text="Turns: {:}".format(self.__turns))
        self.__found_pairs = 0
        for i in range(len(self.__cardpiclabels)):
            self.__cardpiclabels[i].configure(state=NORMAL ,image=self.__template)

        self.__button_1_status = False
        self.__button_2_status = False
        self.__previous_index = None
        self.__randicards = {}

        self.randomize_pics()

    def randomize_pics(self):
        """Arpoo satunnaiset indeksit jokaiselle buttonille, jotka tallennetaan
        dictiin randicards. Dictin avulla voidaan myöhemmin buttonia painaessa
        saada esiin oikea kuva. Samalla asetetaan nappulaan komento press_button """
        nro = [0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,7]
        # Mikäli pelissä esitettävien korttien(kuvien) määrää halutaan muuttaa
        # tulee tätä listaa muokata sen mukaan
        shuffle(nro)
        i = 0
        for button in self.__cardpiclabels:
            button.configure(image=self.__template, command=lambda x=self.
                __cardpiclabels.index(button): self.press_button(x))
            self.__randicards[i] = nro[i]
            i = i + 1

    def press_button(self, index):
        """ Metodi, jolla määritellään mitä tapahtuu kun nappia painetaan eli
        kun ns. "käännetään" kortti """
        if self.__button_1_status is False:
            self.__cardpiclabels[index].configure(state=DISABLED,
                                                  image=self.__cardpics[self.__randicards[index]])
            self.__button_1_status = True
            self.__previous_index = index
        elif self.__button_2_status is False:
            self.__turns += 1
            self.__turns_text.configure(text="Turns: {:}".format(self.__turns))

            self.__cardpiclabels[index].configure(state=DISABLED,
                                                  image=self.__cardpics
                                                  [self.__randicards[index]])
            self.__button_1_status = False

            if self.__randicards[index] == self.__randicards[self.__previous_index]:
                self.__cardpiclabels[index].configure(state=DISABLED)

                self.__found_pairs += 1
                self.is_game_over()

            else:
                self.__window.update_idletasks()
                self.__cardpiclabels[index].configure(state=NORMAL, image=self.__template)
                time.sleep(0.5) # Näyttää molemmat avatut kortit hetken ajan
                self.__cardpiclabels[self.__previous_index].configure(state=NORMAL, image=self.__template)

    def is_game_over(self):
        """ Metodi tarkastaa, onko kaikki kortit käännetty, ja lisää pistemäärän
         HI-scoreksi, mikäli se on matalampi kuin edellinen pistemäärä.
         Kutsuu metodeja exit() ja start_new_game() napin painalluksesta. """
        if self.__found_pairs == len(CARDPICS):
            if self.__best_score is None or self.__turns < self.__best_score:
                self.__best_score = self.__turns

            score = Label(self.__window, text="HI-score: {:}"
                          .format(self.__best_score))

            self.__game_over_text.grid(row=5, column=2, columnspan=2)
            score.grid(row=6, column=2)



    def exit(self):
        self.__window.destroy()

    def start(self):
        self.__window.mainloop()


def main():
    ui = CardGame()
    ui.start()

main()
