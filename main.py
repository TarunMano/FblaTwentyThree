import pygame
import os
import sys
import random
import time
from pygame import mixer

# References: https://www.youtube.com/watch?v=mJ2hPj3kURg, https://github.com/baraltech/Wordle-PyGame/blob/main/youtubemain.py

# check if given word is real
with open("assets/words_alpha.txt") as word_file:
    english_words = set(word.strip().lower() for word in word_file)
def is_english_word(word):
    return word.lower() in english_words

# initialize pygame
pygame.init()
pygame.font.init()

# initalize game window
WIDTH, HEIGHT = 900, 500 # alternative: 633, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption("FBLA 2023")

# set instruction image
INSTRUCTION_IMAGE = pygame.transform.scale(pygame.image.load("assets/Instructions Image.png"), (900,500))
BACKGROUND = pygame.image.load("assets/Starting Tiles.png")
BACKGROUND_RECT = BACKGROUND.get_rect(center=(317,300))
ICON = pygame.image.load("assets/Icon.png")


WIN.fill("white")

pygame.display.update()

FPS = 60
MAIN_MENU = 0
INSTRUCTION = 1
PLAY = 2
MENU = 0
play_check = 0 
main_menu_check = 0

# word objects
current_guess = []  # list of letters that make up the current guess
current_guess_string = ""   # string format that makes up current guess
current_letter_bg_x = 110   # initialize current letter position

game_result = ""    # initialize game without result

user_correct_words = []     # list of correct words user has entered
user_score = 0      # score of user

# letter sizing specifications
LETTER_X_SPACING = 85
LETTER_Y_SPACING = 265
LETTER_SIZE = 75

# set fonts
GUESSED_LETTER_FONT = pygame.font.Font("assets/FreeSansBold.otf", 50)
AVAILABLE_LETTER_FONT = pygame.font.Font("assets/FreeSansBold.otf", 25)
MAIN_MENU_FONT = pygame.font.SysFont('comicsans', 50)
TITLE_FONT = pygame.font.SysFont('comicsans', 75)

# main menu text
title_surface = TITLE_FONT.render("ANAGRAMS", 1, "black")
play_surface = MAIN_MENU_FONT.render("PLAY", 1, "black")
instructions_surface = MAIN_MENU_FONT.render("INSTRUCTIONS", 1, "black")
quit_surface = MAIN_MENU_FONT.render("QUIT", 1, "black") 
arrow_surface = MAIN_MENU_FONT.render(">", 1, "black")

#set music
UI_SOUND = mixer.Sound("assets/uiSE.wav")
MUSIC = mixer.music.load("assets/Background Music.wav")
mixer.music.play(-1)

# draw main menu
def main_menu():
    WIN.fill("white")

    WIN.blit(title_surface, ((WIDTH -  title_surface.get_width())/2, 5)) #-  title_surface.get_width()
    WIN.blit(play_surface, ((WIDTH -  play_surface.get_width())/2 , 160)) #
    WIN.blit(instructions_surface, ((WIDTH -  instructions_surface.get_width())/2 , 210)) #
    WIN.blit(quit_surface, ((WIDTH -  quit_surface.get_width())/2 , 260)) #

    # draw option chooser
    if main_menu_check == 1:
                    WIN.blit(arrow_surface, (((WIDTH -  instructions_surface.get_width())/2)-20, 210))
    if main_menu_check == 2:
                    WIN.blit(arrow_surface, (((WIDTH -  quit_surface.get_width())/2)-20, 260))
    if main_menu_check == 0: 
                    WIN.blit(arrow_surface, (((WIDTH -  play_surface.get_width())/2)-20, 160))

# draw instruction menu
def instruction_menu():
    WIN.fill("white")
    WIN.blit(INSTRUCTION_IMAGE, ((WIDTH - INSTRUCTION_IMAGE.get_width())/2, (HEIGHT - INSTRUCTION_IMAGE.get_height())/2))

# draw icons and start game
def start_game():
    WIN.fill("white")
    # set background sprite & icon
    
    pygame.display.set_icon(ICON)
    WIN.blit(BACKGROUND, BACKGROUND_RECT)
    # initialize game
    initalize_clock()
    initialize_possible_letters()

# Letter class
class Letter:
    def __init__(self, text, bg_position):
        self.bg_color = "white"
        self.text_color = "black"
        self.bg_position = bg_position
        self.bg_x = bg_position[0]
        self.bg_y = bg_position[1]
        self.bg_rect = (bg_position[0], self.bg_y, LETTER_SIZE, LETTER_SIZE)
        self.text = text
        self.text_position = (self.bg_x+36, self.bg_position[1]+34)
        self.text_surface = GUESSED_LETTER_FONT.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.text_position)

    def draw(self):
        pygame.draw.rect(WIN, self.bg_color, self.bg_rect)
        if self.bg_color == 'white':
            pygame.draw.rect(WIN, "#878a8c", self.bg_rect, 3)
        WIN.blit(self.text_surface, self.text_rect)
        pygame.display.update()

    def delete(self):
        pygame.draw.rect(WIN, "white", self.bg_rect)
        pygame.draw.rect(WIN, "#d3d6da", self.bg_rect, 3)
        pygame.display.update()

# play again dialogue after certain time
def play_again():
    # Puts the play again text on the screen.
    pygame.draw.rect(WIN, "white", (10, 600, 1000, 600))
    WIN.fill("white")
    play_again_font = pygame.font.Font("assets/FreeSansBold.otf", 40)
    play_again_text = play_again_font.render("Press ENTER to Play Again!", True, "black")
    play_again_rect = play_again_text.get_rect(center=(WIDTH/2, 700))
    word_was_text = play_again_font.render(f"The word was TARUN!", True, "black")
    word_was_rect = word_was_text.get_rect(center=(WIDTH/2, 650))
    WIN.blit(play_again_text, play_again_rect)
    WIN.blit(play_again_text, play_again_rect)
    pygame.display.update()

# resets window and game state
def reset():
    # Resets all global variables to their default states.
    global current_guess, current_guess_string, game_result, user_correct_words, user_score, current_letter_bg_x
    WIN.fill("white")
    WIN.blit(BACKGROUND, BACKGROUND_RECT)
    current_guess = []
    current_guess_string = ""
    game_result = ""
    user_correct_words = []
    user_score = 0
    initalize_clock()
    initialize_possible_letters()
    current_letter_bg_x = 110
    
    pygame.display.update()

# create new letter on screen
def create_new_letter():
    global current_guess_string, current_letter_bg_x
    current_guess_string += key_pressed
    new_letter = Letter(key_pressed, (current_letter_bg_x, LETTER_Y_SPACING))
    current_letter_bg_x += LETTER_X_SPACING
    current_guess.append(new_letter)
    for letter in current_guess:
        letter.draw()

# delete letter from screen
def delete_letter():
    global current_guess_string, current_letter_bg_x
    current_guess[-1].delete()
    current_guess_string = current_guess_string[:-1]
    current_guess.pop()
    current_letter_bg_x -= LETTER_X_SPACING

# draw window class


# initialize clock for game
def initalize_clock():
    global clock, start_ticks
    # initalize clock
    clock = pygame.time.Clock()

    start_ticks=pygame.time.get_ticks()

# initialize possible letters that user can use on a given round
def initialize_possible_letters():
    global possible_letters, possible_letters_objects
    # identify consonants/vowels
    consonant = ['B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z']
    vowels = ['A', 'E', 'I', 'O', 'U']
    possible_letters = []

    # retrieves three random consonants
    for i in range(3):
        index = random.randint(0, 20)
        while(consonant[index] in possible_letters):
            index = random.randint(0, 20)
        possible_letters.append(consonant[index])

    # retrieves two random vowels
    for i in range(2):
        index = random.randint(0, 4)
        while(vowels[index] in possible_letters):
            index = random.randint(0, 4)
        possible_letters.append(vowels[index])

    # show possible letters on screen
    possible_letters_x = current_letter_bg_x
    possible_letters_objects = []
    for letter in possible_letters:
        new_letter = Letter(letter, (possible_letters_x, 0))
        possible_letters_objects.append(new_letter)
        new_letter.draw()
        possible_letters_x+=85

#initalize_clock()
#initialize_possible_letters()

def draw_window():
     if MENU == INSTRUCTION:
         instruction_menu()
     elif MENU == MAIN_MENU:
         main_menu()
     pygame.display.update()

# main class
run = True
while run:
    # start game
    if play_check == 1:       
        start_game()
        play_check = 2

        # run game 
    if play_check == 2:
        clock.tick(FPS)
        seconds=(pygame.time.get_ticks()-start_ticks)/1000
        
        if game_result != "":
         play_again()

        if seconds >= 5 and game_result == "":    # end game timer
         current_guess = []
         current_guess_string = ""
         current_letter_bg_x = 110
         game_result = "L"
         for letter in possible_letters_objects:
             letter.delete()
         play_again()

    # on event
    
    for event in pygame.event.get():
      # quit game
      if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()
      # on key press
      if event.type == pygame.KEYDOWN:
           
           # on escape key
           if event.key == pygame.K_ESCAPE:
                run = False
                pygame.quit()
                sys.exit()
      # while in main menu
      if MENU == MAIN_MENU:
          if event.type == pygame.KEYDOWN:
            # move through options
            if event.key == pygame.K_DOWN: # move down
                
                main_menu_check += 1
                if main_menu_check == 3:
                    main_menu_check = 0
                UI_SOUND.play()
                    
                
            if event.key == pygame.K_UP: # move up
                main_menu_check -= 1
                if main_menu_check == -1:
                    main_menu_check = 2
                UI_SOUND.play()
            if event.key == pygame.K_RETURN: # select option
                if main_menu_check == 0:
                     MENU = 2
                     play_check = 1
                     draw_window
                if main_menu_check == 1:
                    MENU = 1
                    draw_window()
                if main_menu_check == 2:
                    run = False
                    pygame.quit()
                    sys.exit()
                UI_SOUND.play()
      # while in instruction menu
      if MENU == INSTRUCTION:
          if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_r:
                  main_menu_check = 0
                  UI_SOUND.play()
                  MENU = MAIN_MENU
        # while playing game
      if MENU == PLAY:

        # on key press
        if event.type == pygame.KEYDOWN:
            # if escape key pressed
           
            # if return key pressed
            if event.key == pygame.K_RETURN:
                if game_result != "":
                    reset()
                else:
                    # if valid word
                    if len(current_guess_string) <= 5 and is_english_word(current_guess_string.lower()) and current_guess_string not in user_correct_words:
                        user_correct_words.append(current_guess_string)
                        user_score+=100
                        print(user_correct_words)
                        print(user_score)

                        # clear screen
                        for i in range(len(current_guess_string)):
                            delete_letter()

            # if backspace key pressed
            elif event.key == pygame.K_BACKSPACE:
                if len(current_guess_string) > 0:
                    delete_letter()                
            
            # if alphabetic key pressed
            else:
                key_pressed = event.unicode.upper()
                if key_pressed in "QWERTYUIOPASDFGHJKLZXCVBNM" and key_pressed != "" and key_pressed in possible_letters:
                    if len(current_guess_string) < 5 and key_pressed not in current_guess_string:
                        create_new_letter()
            
            
    draw_window()

pygame.quit() 

