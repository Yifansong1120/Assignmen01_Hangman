'''
This documnt is to create a hangman object with GUI which allows players to enter a letter / select a letter from the keyboard provided. [if you want to run this program, please run player.py (an instance of hangman object)]
The shape of hangman is built using tkinder.Canvas, and the widget of GUI is developed using tkinder.
Assignment: Hangman (Assignment01)
Coding Author: Yifan Song
Student ID: s330809
Please enjoy this game! Thank you!
'''
import random
from words import word_list
import tkinter
from tkinter import messagebox
from tkinter import *

class Hangman(object):
    def __init__(self, life = 7, word =[], attempt = 0, guessed =[], letter_input=[], score=0, result=False):
        #initialize the player's setup: Default life: 7, Attempt #: start from 0, Won't randomly pick up a word before player is ready to play, Any letters are not been guessed, player hasn't input anything before game start.
        self.life = life
        self.word = word
        self.attempt = attempt
        self.guessed =guessed
        self.letter_input = letter_input
        self.score = score
        self.result = result

        #initialize window
        self.root=tkinter.Tk()

        #initialize text widget
        self.text = tkinter.Text(self.root, height = 10, width = 30)
        self.text.place(x=300,y=150)

        #create canvas object to draw hangman
        self.canvas= tkinter.Canvas(self.root)

        #showing the initial player's status on screen
        self.label_life=tkinter.Label(text='The Remaining Life is: %d'%self.life)
        self.label_life.place(x=10, y=0)
        self.label_attempt=tkinter.Label(text='Number of attempts: %d'%self.attempt)
        self.label_attempt.place(relx=0.75, y=0)
        #self.label_word=tkinter.Label(text='The Word is: %s'%self.word)
        #self.label_word.pack()
        self.label_guessed=tkinter.Label(text='Guessing word: %s'%' '.join([str(v) for v in self.guessed]),font=("Helvetica", 18))
        self.label_guessed.place(relx = 0.5, rely = 0.1, anchor = CENTER)
        self.label_letter_input=tkinter.Label(text='You have input: %s'%' '.join([str(v) for v in self.letter_input]))
        self.label_letter_input.pack()
        self.label_score=tkinter.Label(text='Score: %d'%self.score)
        self.label_score.place(relx = 0.9, rely = 0.95)
        
    def get_word(self):
        # function get_word is to randomly select a word from the given word list
        # And convert it to same length of _ based on the word selected
        self.word = list(random.choice(word_list).upper())
        self.guessed = list("_" * len(self.word))

    def player_input_rule(self, guess):
        #This function is to make sure player inputs a valid letter: player only can input 1 letter once; the letter must be alphbet; the letter shouldn't be duplicated from the letters that player input before
        if len(guess)!=1 :
            self.text.insert(tkinter.END,'Sorry, wrong number of letter is input. \n\nPlease input only ONE Letter. ')
            return 'NumberError'
        
        elif guess.isalpha()==False:
            self.text.insert(tkinter.END,'Sorry, wrong character input.\n\nPlease input an alphabet letter.')
            return 'SymbolError'

        elif guess in self.guessed:
            self.text.insert(tkinter.END,'The letter %s is correct. \n\nBut you have already input the letter: %s. \n\nPlease input another letter.'%(guess,guess))
            return 'DuplicationError(correct)'

        elif guess in self.letter_input:
            self.text.insert(tkinter.END,'The letter %s is NOT correct. \n\nAnd you have already input the letter: %s.\n\nPlease input another letter'%(guess,guess))
            return 'DuplicationError(incorrect)'
        else:
            #And it will be sent to word_completion function to check if the letter is correct
            self.word_completion(guess)
            return 'Successful'

    def guess_word_submit_btn(self,event=None) :
        #guess_word_submit_btn will be called when player clicks the submit button
        if self.result != True:
        #if player hasn't completed the word...
            print('Submit button is clicked.')
            self.text.delete("1.0",tkinter.END)

            #read user's input from input bar
            guess=self.entry_player.get().upper()

            #check input is valid or not
            self.player_input_rule(guess)
            
            #automatically clear entry when clicking submit button
            self.entry_player.delete(0,tkinter.END)

            #refactoring implementation: Duplicated code
            self.update_player_attribute()
        else:
        #if player has completed the word...
            #refactoring implementation: Duplicated code and nested loop
            self.restart_widget()

    def guess_word_keyboard(self, guess) :
        #guess_word_keyboard function is to check the letter that player selected is valided or not
        #it will be called when player selected a letter button from keyboard provided on screen
        if self.result != True:
            self.text.delete("1.0",tkinter.END)
            self.player_input_rule(guess)

            #automatically clear entry when clicking submit button
            self.entry_player.delete(0,tkinter.END)
            #refactoring implementation: Duplicated code
            self.update_player_attribute()
        else:
            #refactoring implementation: Duplicated code and nested loop
            self.restart_widget()

    def on_click(self, i):
        # this function is to return the text on the keyboard buttons
        print ("This is Button:", str(i))
        self.guess_word_keyboard(str(i))
        return str(i)

    def word_completion(self, letter):
        #word_completion function is to check the valid letter that player inputs is correct or not. 

        #whatever the letter is correct or incorrect, the number of attempt will increase by 1.
        self.attempt = self.attempt+1

        #if the letter that player input satifisfied all above rules, it will be added to the letter_input list
        self.letter_input.append(letter)
        
        self.text.delete("1.0",tkinter.END)
        if letter in self.word:
        #if it is correct... update to guessed list, and replace _ showing on screen
            for index in range(len(self.word)):
                if self.word[index] == letter:
                    self.guessed[index] = letter
            self.text.insert(tkinter.END,'Congradulations!\n\n You guessed a letter of the word: %s'%letter)
        else:
            #if it is incorrect...
            self.life-=1
            self.draw_hangman()
            self.text.insert(tkinter.END,"Sorry!\n You didn't guessed a letter of the word.")
        
        #call check_result function to see if the word is guessed or player runs out of life
        self.check_result()

    def check_result(self):
        #this function is to check if player wins/loses the game
        self.text.delete("1.0",tkinter.END)
        if(self.word == self.guessed):
            #print(self.score)
            self.text.insert(tkinter.END,'You Win the Game!\nYou guessed the word: %s\nDo you want to restart the game?'%''.join([str(v) for v in self.word]))
            self.result=True
            self.score+=1
            return
        elif self.life==0:
            self.text.insert(tkinter.END,'You Lose the Game\nYou did not guessed the word: %s\nDo you want to restart the game?'%''.join([str(v) for v in self.word]))
            self.result=True
            return
    
    def draw_hangman(self):
        #draw_hangman function is to draw a hangman based on the life remaining
        if self.life ==6:
            #If player select a wrong letter once
            #    ___ 
            #   |   |
            #   |
            #   |
            #   |
            #   |________  draw this shape
            self.canvas.create_line(10,220,200,220, width=3)
            self.canvas.create_line(10,10,10,220, width=3)
            self.canvas.create_line(10,10, 100, 10, width=3)
            self.canvas.create_line(100,10, 100, 50,fill='BROWN',width=2)
        elif self.life ==5:
            #If player select a wrong letter twice
            #    ___ 
            #   |   |
            #   |  {-.- }
            #   |
            #   |
            #   |________  draw a head of man
            self.canvas.create_oval(85, 50, 115, 80, outline = "black", fill = "white", width = 2) 
            self.canvas.create_oval(93, 60, 95, 62, outline = "black", fill = "black", width = 2) 
            self.canvas.create_oval(103, 60, 105, 62, outline = "black", fill = "black",  width = 2) 
            self.canvas.create_line(93,70,105,70, width=3)    
        elif self.life ==4:
            #If player select a wrong letter three times
            #    ___ 
            #   |   |
            #   |  {-.- }
            #   |     |
            #   |
            #   |________  draw a body of man
            self.canvas.create_line(100,80, 100, 145,width=3)
        elif self.life ==3:
            #If player select a wrong letter four times
            #    ___ 
            #   |   |
            #   |  {-.- }
            #   |    /|
            #   |
            #   |________  draw an arm of man
            self.canvas.create_line(100,90, 80, 120,width=3)
        elif self.life ==2:
            #If player select a wrong five times
            #    ___ 
            #   |   |
            #   |  {-.- }
            #   |    /|\
            #   |
            #   |________  draw another arm of man
            self.canvas.create_line(100,90, 120, 120,width=3)
        elif self.life ==1:
            #If player select a wrong six times
            #    ___ 
            #   |   |
            #   |  {-.- }
            #   |    /|\
            #   |     /
            #   |________  draw a leg of man
            self.canvas.create_line(100,145, 80, 185 ,width=3)
        elif self.life ==0:
            #If player select a wrong seven times
            #    ___ 
            #   |   |
            #   |  {-.- }
            #   |    /|\
            #   |     /\
            #   |________  draw another leg of man --- die!
            self.canvas.create_line(100,145, 120, 185 ,width=3)
        self.canvas.place(x=10, y=100)
        #refactoring implementation: Duplicated code
        self.update_player_attribute()

   #refactoring: Duplicated code and nested loop
    def restart_widget(self):
        #this function is to create a restart window and get user repsonses
        if tkinter.messagebox.askyesno('To be Continue...','Do you want to restart the game? '):
            self.restart_game()
        else:
            self.root.destroy()
           
    def restart_game(self):
        #this function is to reset all attributes of player, except score
        self.text.delete("1.0",tkinter.END)
        self.canvas.delete('all')
        self.life = 7
        self.word = []
        self.attempt = 0
        self.guessed =[]
        self.letter_input = []
        self.result = False
        self.get_word()
        #refactoring implementation: Duplicated code
        self.update_player_attribute()
    
    #refactoring: Duplicated code
    def update_player_attribute(self):
        #player attributes update
        self.label_life.config(text='The Remaining Life is: %d' %self.life)
        self.label_attempt.config(text='Number of attempts:%d' %self.attempt)
        #self.label_word.config(text='The Word is: %s' %self.word)
        self.label_guessed.config(text='Guessing word: %s' %' '.join([str(v) for v in self.guessed]))
        self.label_letter_input.config(text='You have input: %s'%' '.join([str(v) for v in self.letter_input]))
        self.label_score.config(text="Score: %d"%self.score)

    def main(self):
        #function create_widget is to create a window (or GUI) showing all information, including life, attemps, question word, word completion, and tips.
       
        self.get_word()

        #create a widget/window
        self.root.title("HANGMAN")
        self.root.geometry("600x600+0+0")
        self.root.maxsize(600,600)
        self.root.minsize(600,600)

        #refactoring implementation: Duplicated code
        self.update_player_attribute()

        #restart button
        self.button_restart = tkinter.Button(self.root, text="Restart",command = self.restart_game)
        self.button_restart.config(width=20, height=1)
        self.button_restart.place(x=400, y=380)

        #hint widget/windows will prompt users with the appropriate feedback
        self.text = tkinter.Text(self.root, height = 10, width = 30)
        self.text.place(x=300,y=150)

        #instruction hint 1
        hint1= tkinter.Label(self.root, text="Please enter a letter (press 'Enter' or click 'Submit')")
        hint1.place(x=50, y=350)
        
        #create a input bar to allow user to input letter
        self.entry_player=tkinter.Entry()
        #user can submit a letter by pressing enter button
        self.entry_player.bind('<Return>', self.guess_word_submit_btn)
        self.entry_player.place(x=50, y=380)
        
        #create a submit button to allow user to submit the guess letter and call function submitFunction
        self.button_submit = tkinter.Button(self.root, text ="Submit",command=self.guess_word_submit_btn)
        self.button_submit.config(width=20, height=1)
        self.button_submit.place(x=200, y=380)
        

        #instruction hint 2
        hint2= tkinter.Label(self.root, text="Or you can select a letter from below keyboard")
        hint2.place(x=50, y=420)
        
        #create keyboard
        self.buttons = []
        item = ['Q','W','E','R','T','Y','U','I','O','P',
                'A','S','D','F','G','H','J','K','L',
                'Z','X','C','V','B','N','M']
        for i in range(len(item)):
            if i<10:
                b = tkinter.Button(self.root, height=2, width=5,text=item[i], command = lambda i=i: self.on_click(item[i]))
                b.place(x =50*i+50, y =450) 
                self.buttons.append(b)
            elif 10<=i<20:
                b = tkinter.Button(self.root, height=2, width=5,text=item[i], command = lambda i=i: self.on_click(item[i]))
                b.place(x =50*(i-10)+50, y =500) 
                self.buttons.append(b)
            else:
                b = tkinter.Button(self.root, height=2, width=5,text=item[i], command = lambda i=i: self.on_click(item[i]))
                b.place(x =50*(i-20)+150, y =550)
                self.buttons.append(b)
        
        
        #running this loop all the time
        self.root.mainloop()


