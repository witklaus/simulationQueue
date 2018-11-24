import abc
import random
from uuid import uuid4

class NameGeneratorABC(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_name(self, wordcount):
        pass
    
class NameGenerator(NameGeneratorABC):
    def __init__(self):
        try:
            self.wordlist = open("/usr/share/dict/words").read().splitlines()
            self.unix_wordlist_exists = True
        except FileNotFoundError:
            self.unix_wordlist_exists = False

    def get_word(self):
        return random.choice(self.wordlist).upper()
        
    def get_name(self, wordcount=3):
        if self.unix_wordlist_exists:
            return "_".join([self.get_word() for w in range(wordcount)])
        return str(uuid4())[0:wordcount]    

name_generator = NameGenerator()         