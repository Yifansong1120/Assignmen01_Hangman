import unittest
from hangman import Hangman
import string

class HangmanInitialSettingTestCase(unittest.TestCase):
    #To test initial value of players before the game starts
    def setUp(self):
        #create an instance  of object "Hangman", named hangman_player1
        self.hangman_player1 = Hangman()
    
    def test_initial_life(self):
        #Test case: to test life remaining before the game starts
        self.assertEqual(self.hangman_player1.life, 7, msg="Initial Life is invalid")

    def test_initial_word(self):
        #Test case: to test word that haven't been chosen randomly, which is empty, before the game starts
        self.assertEqual(self.hangman_player1.word, [], msg="Initial word is not empty")
        
    def test_initial_attempt(self):
        #Test case: to test the number of attempt before the game starts
        self.assertEqual(self.hangman_player1.attempt, 0, msg="Initial attempt is invalid")
    
    def test_initial_guessed_list(self):
        #Test case: to test the guess before the game starts 
        self.assertEqual(self.hangman_player1.guessed, [], msg="Initial guessed list is invalid")

    def test_initial_score(self):
        #Test case: to test the guess before the game starts 
        self.assertEqual(self.hangman_player1.score, 0, msg="Initial score is invalid")

    def test_get_word(self):
        #Test case: to test the word that is randomly selected from word_list when the game starts
        self.hangman_player1.get_word()
        self.assertNotEqual(self.hangman_player1.word, [], msg="Getting word unsuccessfully")
        
    def test_guessed_list(self):
        #Test case: to test the guess when the game starts before user inputs anything
        self.hangman_player1.get_word()
        self.assertNotEqual(self.hangman_player1.guessed, [], msg="Guessed list setup is invalid")

class HangmanWordCompletionTestCase(unittest.TestCase):
    
    def setUp(self):
        #create an instance  of object "Hangman", named hangman_player1
        self.hangman_player2 = Hangman()
        self.hangman_player2.get_word()
    
    def test_all_attributes_if_guessed(self):
        #assume that the player guessed the first letter of word correctly, then the letter should be added to 'guessed' list
        guessed_letter = self.hangman_player2.word[0]
        self.hangman_player2.word_completion(guessed_letter)
        self.assertTrue(guessed_letter in self.hangman_player2.guessed, msg="The guessed letter cannot be added to guessed list if guessed correct letter")
        self.assertEqual(self.hangman_player2.life, 7, msg="The life is changed incorrectly if guessed correct letter")
        self.assertEqual(self.hangman_player2.attempt, 1, msg="The attempt is changed incorrectly if guessed correct letter")
        self.assertTrue(guessed_letter in self.hangman_player2.letter_input, msg="The guessed letter cannot be added to letter_input list if satisfied all rules")      

    def test_all_attributes_if_guessed_all(self):
        #assume that the player guessed the first letter of word correctly, then the letter should be added to 'guessed' list
        print(self.hangman_player2.word)
        option_list = []
        for guessed_letter in self.hangman_player2.word:
            if guessed_letter not in option_list:
                option_list.append(guessed_letter)
        print(option_list)
        for letter in option_list:
            self.hangman_player2.word_completion(letter)
        self.assertEqual(self.hangman_player2.word, self.hangman_player2.guessed, msg="The guessed letter cannot be added to guessed list correctly if guessed all letter")
        self.assertEqual(self.hangman_player2.life, 7, msg="The life is changed incorrectly if guessed correct letter")
        self.assertEqual(self.hangman_player2.attempt, len(option_list), msg="The attempt is changed incorrectly if guessed correct letter")
       
    def test_all_attributes_if_not_guessed(self):
        #assume that the player guessed the first letter of word correctly, then the letter should be added to 'guessed' list
        for guessed_letter in string.ascii_uppercase:
            if guessed_letter not in self.hangman_player2.word:
                break
        self.hangman_player2.word_completion(guessed_letter)
        self.assertFalse(guessed_letter in self.hangman_player2.guessed, msg="The guessed letter is added to guessed list incorrectly if not guessed the correct letter")
        self.assertEqual(self.hangman_player2.life, 6, msg="The life is changed incorrectly if not guessed the correct letter.")
        self.assertEqual(self.hangman_player2.attempt, 1, msg="The attempt is changed incorrectly if not guessed the correct letter")
        self.assertTrue(guessed_letter in self.hangman_player2.letter_input, msg="The guessed letter cannot be added to letter_input list if satisfied all rules")        

    def test_all_attributes_if_guessed_nothing(self):
        #assume that the player guessed the first letter of word correctly, then the letter should be added to 'guessed' list
        option_list = []
        for guessed_letter in string.ascii_uppercase:
            if guessed_letter not in self.hangman_player2.word and guessed_letter not in option_list:
                option_list.append(guessed_letter)
        for opti in option_list:
            self.hangman_player2.word_completion(opti)
            if self.hangman_player2.result:
                break
        self.assertNotEqual(self.hangman_player2.letter_input,self.hangman_player2.guessed, msg="The guessed letter is added to guessed list incorrectly if not guessed the correct letter")
        self.assertEqual(self.hangman_player2.life, 0, msg="The life is changed incorrectly if not guessed the correct letter.")
        
    
class HangmanInputRuleTestCase(unittest.TestCase):
    def setUp(self):
        #create an instance  of object "Hangman", named hangman_player1
        self.hangman_player3 = Hangman()
        self.hangman_player3.get_word()

    def test_symbol_input(self):
        self.assertEqual(self.hangman_player3.player_input_rule('.'),'SymbolError')

    def test_multiple_char_input(self):
        self.assertEqual(self.hangman_player3.player_input_rule('AB'),'NumberError')
        self.assertEqual(self.hangman_player3.player_input_rule('A.'),'NumberError')

    def test_duplicate_char_input1(self):
        guessed_letter = self.hangman_player3.word[0]
        self.assertEqual(self.hangman_player3.player_input_rule(guessed_letter),'Successful')
        self.assertEqual(self.hangman_player3.player_input_rule(guessed_letter),'DuplicationError(correct)')         

    def test_duplicate_char_input2(self):
        for guessed_letter in string.ascii_uppercase:
            if guessed_letter not in self.hangman_player3.word:
                break
        self.assertEqual(self.hangman_player3.player_input_rule(guessed_letter),'Successful')
        self.assertEqual(self.hangman_player3.player_input_rule(guessed_letter),'DuplicationError(incorrect)')   

class HangmanResultTestCase(unittest.TestCase):
    def setUp(self):
        self.hangman_player = Hangman()
        self.hangman_player.get_word()

    def test_score_if_win(self):
        self.hangman_player.score=0
        for i in self.hangman_player.word:
            self.hangman_player.word_completion(i)
        self.assertEqual(self.hangman_player.score,1)

    def test_result_if_win(self):
        self.hangman_player7 = Hangman()
        self.hangman_player7.get_word()
        for i in self.hangman_player7.word:
            self.hangman_player7.word_completion(i)
        self.assertTrue(self.hangman_player7.result)

    def test_score_if_lose(self):
        self.hangman_player8 = Hangman()
        self.hangman_player8.get_word()
        option_list = []
        for guessed_letter in string.ascii_uppercase:
            if guessed_letter not in self.hangman_player8.word and guessed_letter not in option_list:
                option_list.append(guessed_letter)
        for opti in option_list:
            self.hangman_player8.word_completion(opti)
            if self.hangman_player8.result:
                break
        self.assertEqual(self.hangman_player8.score,0)

    def test_result_if_lose(self):
        self.hangman_player6 = Hangman()
        self.hangman_player6.get_word()
        self.assertFalse(self.hangman_player6.result)

class HangmanRestartTestCase(unittest.TestCase):
    def setUp(self):
    #create an instance  of object "Hangman", named hangman_player1
        self.hangman_player_re = Hangman()
        self.hangman_player_re.get_word()
        
    def test_all_attributes_if_restart(self):
        self.hangman_player_re.score=0
        for i in self.hangman_player_re.word:
            self.hangman_player_re.word_completion(i)
        self.hangman_player_re.restart_game()
        self.assertEqual(self.hangman_player_re.life, 7, msg="Initial Life is invalid")
        self.assertNotEqual(self.hangman_player_re.word, [], msg="Initial word is not empty")
        self.assertEqual(self.hangman_player_re.attempt, 0, msg="Initial attempt is invalid")
        self.assertEqual(self.hangman_player_re.letter_input, [], msg="Initial guessed list is invalid")
        self.assertNotEqual(self.hangman_player_re.guessed, [], msg="Guessed list setup is invalid")