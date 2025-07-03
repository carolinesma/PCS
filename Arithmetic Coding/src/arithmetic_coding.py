import numpy as np
import numpy as np
import itertools
import copy
from typing import List

class CodeCandidate:
    """
    Represents a candidate for arithmetic coding with associated probability interval and symbol sequence.

    Attributes
    ----------
    lowerBound : np.uint32
        Lower bound of the probability interval.
    upperBound : np.uint32
        Upper bound of the probability interval.
    probability : np.uint32
        Width of the probability interval.
    symbols : List[int]
        Symbol sequence associated with this candidate.
    """
    def __init__(self, lowerBound: np.uint32 = np.uint32(0), 
                 upperBound: np.uint32= np.uint32(0), 
                 probability: np.uint32 = np.uint32(0), 
                 symbols: List[int] = []):
        self.lowerBound = lowerBound
        self.upperBound = upperBound
        self.probability = probability
        self.symbols = symbols

    def print_interval(self):   
        print(f"Upper Bound: {self.upperBound}")
        print(f"Lower Bound: {self.lowerBound}")

    def print_all(self):   
        print(f"Upper Bound: {self.upperBound}")
        print(f"Lower Bound: {self.lowerBound}")
        print(f"Probability: {self.probability}")
        print(f"Symbol: {self.symbols}")

class Interval:
    """
    Represents the current encoding or decoding interval for the source.

    Attributes
    ----------
    lowerBound : np.uint32
        Lower bound of the interval.
    upperBound : np.uint32
        Upper bound of the interval.
    """
    def __init__(self, lowerBound: np.uint32 = np.uint32(0), 
                 upperBound: np.uint32 = np.uint32(0)):
        self.lowerBound = lowerBound
        self.upperBound = upperBound

    def print(self):
        print(f"Upper Bound: {self.upperBound}")
        print(f"Lower Bound: {self.lowerBound}")

class CodeCandidateList:
    """
    Maintains a list of code candidates used during encoding or decoding.

    Attributes
    ----------
    list : List[CodeCandidate]
        The list of code candidates.
    k : int
        Alphabet size.
    """
    def __init__(self, k: int):
        self.list = []
        self.k = k

    def print(self):
        print(f"k: {self.k}")
        print(f"List of Candidates:")
        for i, candidate in enumerate(self.list):
            print(f"Candidate {i + 1}:")
            candidate.print(candidate)