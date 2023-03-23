# import libraries/modules
import pygame
import os
import sys
import random
import time
from pygame import mixer
from anagrams import wordlist
import csv
from leaderboard import leaderboard

# function for checking if user inputted word is real
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

# initialize game window
WIN.fill("white")
pygame.display.update()

# Menu variables
FPS = 60
MAIN_MENU = 0
INSTRUCTION = 1
PLAY = 2
END = 3
NAME_MENU = 4
LEADERBOARD_MENU = 5
MENU = 0
play_check = 0 
main_menu_check = 0

# set current level
level = 1 

end_option = 0

# word objects
current_guess = []  # list of letters that make up the current guess
current_guess_string = ""   # string format that makes up current guess
current_letter_bg_x = 110   # initialize current letter position

# player username variables
username = []
username_string = ""
current_letter_username_x = 110

game_result = ""    # initialize game without result
current_guess_max_letters = 3 # set the max letters user can guess to 3

user_correct_words = []     # list of correct words user has entered
user_score = 0      # score of user

# letter sizing specifications
LETTER_X_SPACING = 85
LETTER_Y_SPACING = 265
LETTER_SIZE = 75

# positioning of user-guessed words
user_guessed_words_y = 15

# set fonts
GUESSED_LETTER_FONT = pygame.font.Font("assets/FreeSansBold.otf", 50)
AVAILABLE_LETTER_FONT = pygame.font.Font("assets/FreeSansBold.otf", 25)
MENU_FONT = pygame.font.Font("assets/FreeSansBold.otf", 50)
TITLE_FONT = pygame.font.Font("assets/FreeSansBold.otf", 75)
BODY_FONT = pygame.font.Font("assets/FreeSansBold.otf", 35)
WORDS_FONT = pygame.font.Font("assets/FreeSansBold.otf", 15) #30?
LEADERBOARD_FONT = pygame.font.Font("assets/FreeSansBold.otf", 25) #30?
LEVEL_FONT = pygame.font.Font("assets/FreeSansBold.otf", 50)

# main menu text

title_surface = TITLE_FONT.render("ANAGRAMS", 1, "black")
play_surface = MENU_FONT.render("PLAY", 1, "black")
instructions_surface = MENU_FONT.render("INSTRUCTIONS", 1, "black")
quit_surface = MENU_FONT.render("QUIT", 1, "black") 
arrow_surface = MENU_FONT.render(">", 1, "black")
ending_surface = MENU_FONT.render("WELL DONE!", 1, "black")
return_surface = BODY_FONT.render("Click Escape to leave, or R to return to menu,", 1, "black")
return1_surface = BODY_FONT.render("and play again", 1, "black")
name_surface = MENU_FONT.render("Enter a name: ", 1, "black")
name1_surface = MENU_FONT.render("Click Space to continue", 1, "black")
leaderboard_surface = MENU_FONT.render("LEADERBOARD", 1, "black")
leaderboard1_surface = BODY_FONT.render("Click Space to return to menu", 1, "black")

#set music
UI_SOUND = mixer.Sound("assets/uiSE.wav")
WIN_SOUND = mixer.Sound("assets/win sound.wav")
END_SOUND = mixer.Sound("assets/end sound.wav")
LEVEL_UP_SOUND = mixer.Sound("assets/new level.wav")
END_SOUND = mixer.Sound("assets/end sound.wav")
WRONG_SOUND = mixer.Sound("assets/wrong word.wav")
MUSIC = mixer.music.load("assets/Background Music.wav")
mixer.music.play(-1)

# draw main menu
def main_menu():
    WIN.fill("white")

    WIN.blit(title_surface, ((WIDTH -  title_surface.get_width())/2, 5)) 
    WIN.blit(play_surface, ((WIDTH -  play_surface.get_width())/2 , 150)) 
    WIN.blit(instructions_surface, ((WIDTH -  instructions_surface.get_width())/2 , 210))
    WIN.blit(leaderboard_surface, ((WIDTH - leaderboard_surface.get_width())/2, 270)) 
    WIN.blit(quit_surface, ((WIDTH -  quit_surface.get_width())/2 , 350)) 

    # draw option chooser
    if main_menu_check == 0: 
                    WIN.blit(arrow_surface, (((WIDTH -  play_surface.get_width())/2)-30, 145))
    if main_menu_check == 1:
                    WIN.blit(arrow_surface, (((WIDTH -  instructions_surface.get_width())/2)-30, 205))
    if main_menu_check == 3:
                    WIN.blit(arrow_surface, (((WIDTH -  quit_surface.get_width())/2)-30, 345))
    if main_menu_check == 2:
                    WIN.blit(arrow_surface,(((WIDTH - leaderboard_surface.get_width())/2)-30, 265))
    

# draw instruction menu
def instruction_menu():
    WIN.fill("white")
    WIN.blit(INSTRUCTION_IMAGE, ((WIDTH - INSTRUCTION_IMAGE.get_width())/2, (HEIGHT - INSTRUCTION_IMAGE.get_height())/2))

# draw icons and start game
def start_game():
    WIN.fill("white")

    # set background and icons
    pygame.display.set_icon(ICON)
    WIN.blit(BACKGROUND, BACKGROUND_RECT)
    # initialize game
    initalize_clock()
    initialize_possible_letters()

# end screen menu
def end_menu():
     global end_option
     WIN.fill("white")
     WIN.blit(ending_surface, ((WIDTH - ending_surface.get_width())/2, 5))
     WIN.blit(score_surface, ((WIDTH - score_surface.get_width())/2, 200))
     WIN.blit(return_surface, ((WIDTH - return_surface.get_width())/2, 300))
     WIN.blit(return1_surface, ((WIDTH - return1_surface.get_width())/2, 330))
     if end_option == 1:
          end_option = 0
          play_again()

# prompt name input screen
def name_menu():
     WIN.blit(name_surface, ((WIDTH - name_surface.get_width())/2, 5))
     WIN.blit(name1_surface, ((WIDTH - name1_surface.get_width())/2, 350))

# leaderboard screen
def leaderboard_menu():
    global leaderboard
    WIN.fill("white")
    WIN.blit(leaderboard_surface, ((WIDTH - leaderboard_surface.get_width())/2,5))
    WIN.blit(leaderboard1_surface, ((WIDTH- leaderboard1_surface.get_width())/2, 350))

    # sort leadeboard from highest to lowest
    leaderboard.sort(key=lambda x:x[1])
    leaderboard.reverse()

    # get first five people
    leaderboard = leaderboard[:5]
    current_y = 100

    # show people on leaderboard
    for person in leaderboard:
        text = LEADERBOARD_FONT.render(str(person[0] + " - " + str(person[1])), True, (0, 0, 0))
        text_rect = text.get_rect(center = (450, current_y))
        current_y+=25
        WIN.blit(text, text_rect)


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
    
    def drawRed(self):
        pygame.draw.rect(WIN, "red", self.bg_rect)
        pygame.draw.rect(WIN, "#878a8c", self.bg_rect, 3)
        pygame.display.update()

# play again dialogue after game ends
def play_again():
    global MAIN_MENU, INSTRUCTION, PLAY, MENU, user_score, user_guessed_words_y, play_check, main_menu_check, NAME_MENU, username_string, username, current_letter_username_x, game_result
    # Puts the play again text on the screen.
    pygame.draw.rect(WIN, "white", (10, 600, 1000, 600))
    WIN.fill("white")
    MAIN_MENU = 0
    INSTRUCTION = 1
    PLAY = 2
    NAME_MENU = 4
    MENU = 0
    game_result = ""
    username = []
    username_string = ""
    current_letter_username_x = 110
    user_guessed_words_y = 15
    play_check = 0 
    main_menu_check = 0
    user_score = 0
    pygame.display.update()

# resets window and game state
def reset():
    # Resets all global variables to their default states.
    global seconds, current_guess, current_letter_username_x, current_guess_string, game_result, user_correct_words, user_score, current_letter_bg_x, user_guessed_words_y, current_guess_max_letters, level, username, username_string
    WIN.fill("white")
    WIN.blit(BACKGROUND, BACKGROUND_RECT)
    current_guess = []
    current_guess_string = ""
    game_result = ""
    user_correct_words = []
    user_score = 0
    current_letter_bg_x = 110
    user_guessed_words_y = 15
    current_guess_max_letters = 3
    level = 1
    username = []
    username_string = ""
    seconds = 0
    initalize_clock()
    initialize_possible_letters()
    
    pygame.display.update()

# create new letter on screen
def create_new_letter():
    global current_guess_string, current_letter_bg_x, username_string, current_letter_username_x, username
    # if in name screen
    if MENU == NAME_MENU:
        username_string += key_pressed
        new_letter = Letter(key_pressed, (current_letter_username_x, LETTER_Y_SPACING))
        current_letter_username_x += LETTER_X_SPACING
        username.append(new_letter)
        for letter in username:
             letter.draw()
    # if in play screen
    else:
        if len(current_guess) >= current_guess_max_letters:
            pass
        else:
            current_guess_string += key_pressed
            new_letter = Letter(key_pressed, (current_letter_bg_x, LETTER_Y_SPACING))
            current_letter_bg_x += LETTER_X_SPACING
            current_guess.append(new_letter)
            for letter in current_guess:    
                letter.draw()

# delete letter from screen
def delete_letter():
    global current_guess_string, current_letter_bg_x, current_letter_username_x, username_string, username
    # if in name screen
    if NAME_MENU == MENU:
         username[-1].delete()
         username_string = username_string[:-1]
         username.pop()
         current_letter_username_x-=LETTER_X_SPACING
    # if in play screen
    else:
        current_guess[-1].delete()
        current_guess_string = current_guess_string[:-1]
        current_guess.pop()
        current_letter_bg_x -= LETTER_X_SPACING

# initialize clock for game
def initalize_clock():
    global clock, start_ticks
    # initalize clock
    clock = pygame.time.Clock()

    start_ticks=pygame.time.get_ticks()

# initialize possible letters that user can use on a given round
def initialize_possible_letters():
    global possible_letters, possible_letters_objects
    possible_letters = []

    # get random combo of letters
    word_index = random.randint(0, len(wordlist)-1)
    word = wordlist[word_index]
    
    # add chars to possible_letters list
    for char in range(0, len(word)):
        possible_letters.append(word[char].upper())

    # randomize order of letters
    random.shuffle(possible_letters)

    # show possible letters on screen
    possible_letters_x = current_letter_bg_x
    possible_letters_objects = []
    for letter in possible_letters:
        new_letter = Letter(letter, (possible_letters_x, 0))
        possible_letters_objects.append(new_letter)
        new_letter.draw()
        possible_letters_x+=85

# draw window function
def draw_window():
     # show different windows based on MENU variable
     if MENU == INSTRUCTION:
         instruction_menu()
     elif MENU == MAIN_MENU:
         main_menu()
     elif MENU == END:
          end_menu()
     elif MENU == NAME_MENU:
          name_menu()
     elif MENU == LEADERBOARD_MENU:
          leaderboard_menu()
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

        # update seconds variable (timer)
        seconds=(pygame.time.get_ticks()-start_ticks)/1000

        # if game is ends, show end screen
        if game_result != "":
            MENU = 3

        # if timer exceeds 45 seconds
        if seconds >= 45 and game_result == "":
            # reset guesses
            current_guess = []
            current_guess_string = ""
            current_letter_bg_x = 110

            # set game result
            game_result = "L"

            # delete letters on screen
            for letter in possible_letters_objects:
                letter.delete()
            
            # if game just ended
            if(MENU != 3):

                # write to leaderboard file
                with open("leaderboard.py", "w") as f:
                    if [username_string, user_score] not in leaderboard:
                        print("leaderboard = " + (str(leaderboard)))
                        leaderboard.append([username_string, user_score])
                        f.write("leaderboard = " + (str(leaderboard)))
                    else:
                        pass
            
            # set menu to end screen
            if MENU == 2:
                 END_SOUND.play()
            MENU = 3

            # reset timer
            seconds = 0
        
        # update timer on screen if it increments by 1
        if abs(seconds - int(seconds)) < 0.12 and MENU != END:
            pygame.draw.rect(WIN, "white",(800, 0, 500, 80))
            text = GUESSED_LETTER_FONT.render(str(int(seconds)), True, (0, 128, 0))
            text_rect = text.get_rect(center = (850, 50))
            WIN.blit(text, text_rect)
            
            pygame.draw.rect(WIN, "white",(0, 350, 350, 400) )
            level_text = LEVEL_FONT.render("Level: " + str(level), 1, "black")
            level_text_rect = level_text.get_rect(center = (100, 450))
            WIN.blit(level_text, level_text_rect)

            pygame.display.flip()
        else:
            pass

        # if timer exceeds 30
        if seconds>=30:
            # increment level to 3
            if level == 2:
                LEVEL_UP_SOUND.play()
            level = 3
            # update the max letters allowed
            current_guess_max_letters = 5

        # if timer exceeds 15
        elif seconds>=15:
            # increment level to 2
            if level == 1:
                LEVEL_UP_SOUND.play()
            level = 2
            # update the max letters allowed
            current_guess_max_letters = 4
        else:
            pass
        

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
                if main_menu_check == 4:
                    main_menu_check = 0
                UI_SOUND.play()
                    
            if event.key == pygame.K_UP: # move up
                main_menu_check -= 1
                if main_menu_check == -1:
                    main_menu_check = 3
                UI_SOUND.play()

            if event.key == pygame.K_RETURN: # select option
                if main_menu_check == 0: # play
                     MENU = 4
                     WIN.fill("white")
                     draw_window()
                if main_menu_check == 1: # instructions
                    MENU = 1
                    draw_window()
                if main_menu_check == 2: # leaderboard
                     MENU = 5
                     draw_window()
                if main_menu_check == 3: # quit
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
        score_surface = MENU_FONT.render("Your final score was: " + str(user_score), 1, "black")

        # on key press
        if event.type == pygame.KEYDOWN:
            # if escape key pressed
           
            # if return key pressed
            if event.key == pygame.K_RETURN:
                if game_result != "":
                    reset()
                else:
                    # if valid word
                    if len(current_guess_string) <= current_guess_max_letters and is_english_word(current_guess_string.lower()) and current_guess_string not in user_correct_words:
                        user_correct_words.append(current_guess_string)
                        user_score+=(100 + (len(current_guess_string) - 3)*100)
                        print(user_correct_words)
                        print(user_score)
                        
                        score_surface = MENU_FONT.render("Your final score was: " + str(user_score), 1, "black")

                        text = WORDS_FONT.render(current_guess_string, True, (51, 51, 0))
                        text_rect = text.get_rect(center = (600, user_guessed_words_y))
                        WIN.blit(text, text_rect)
                        user_guessed_words_y+=15

                        pygame.draw.rect(WIN, "white",(700, 400, 700, 500))
                        text = GUESSED_LETTER_FONT.render(str(user_score), True, (0, 128, 0))
                        text_rect = text.get_rect(center = (825, 450))
                        WIN.blit(text, text_rect)
                        WIN_SOUND.play()
                        # clear screen
                        for i in range(len(current_guess_string)):
                            delete_letter()
                    else:
                         WRONG_SOUND.play()

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

      # if current menu is leaderboard screen
      if MENU == LEADERBOARD_MENU:
           if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                     main_menu_check = 0
                     UI_SOUND.play()
                     MENU = MAIN_MENU

      # if current menu is name screen
      if MENU == NAME_MENU:
           # if return key pressed
           if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                MENU = 2
                play_check = 1
                
            # if backspace key pressed
            elif event.key == pygame.K_BACKSPACE:
                if len(username_string) > 0 and len(username_string) >= 1:
                    delete_letter()                
            
            # if alphabetic key pressed
            else:
                key_pressed = event.unicode.upper()
                if key_pressed in "QWERTYUIOPASDFGHJKLZXCVBNM" and key_pressed != "":
                    create_new_letter()

      # if current menu is end screen
      if MENU == END:
             if event.type == pygame.KEYDOWN:
                  if event.key == pygame.K_r:
                       UI_SOUND.play()
                       end_option = 1
    draw_window()
    

pygame.quit() 

