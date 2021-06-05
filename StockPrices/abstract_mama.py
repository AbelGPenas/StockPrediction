# abstract_mama.py

from abc import ABCMeta, abstractmethod


class Strategy:
# take a list of candle bars as input (Open-High-Low-Close-Volume) and produce movement 
# recommendations i.e. positions going long, hold or short {1, 0, -1} for Portfolio class to take
# decision on the position """    
    
    @abstractmethod
    def generate_signs(self):
        """ implementation required to return the DataFrame of signs {1, 0, -1} """
    

    @abstractmethod
    def get_close_prices(self):

        """ implementation required to retrieve data """
