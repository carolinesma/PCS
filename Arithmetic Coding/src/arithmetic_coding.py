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

def cumulative_prob(P):
    """Cria os limites cumulativos para cada símbolo"""
    cum = {}
    total = 0.0
    for symbol, prob in sorted(P.items()):
        cum[symbol] = (total, total + prob)
        total += prob
    return cum

def update_code_interval(code_intervals, P):
    code_interval_list = CodeCandidateList(2 * code_intervals.k)
    probability = P[0]
    for cc in code_intervals.list:
        range_ = cc.upperBound - cc.lowerBound

        if cc.symbols[0] == 0:
            l2 = cc.upperBound - (1 - probability) * range_
            
            # Novo objeto para símbolo 0
            c0 = CodeCandidate()
            c0.symbols = cc.symbols + [0]
            c0.upperBound = l2
            c0.lowerBound = cc.lowerBound
            c0.probability = c0.upperBound - c0.lowerBound
            code_interval_list.list.append(c0)

            # Novo objeto para símbolo 1
            c1 = CodeCandidate()
            c1.symbols = cc.symbols + [1]
            c1.upperBound = cc.upperBound
            c1.lowerBound = l2
            c1.probability = c1.upperBound - c1.lowerBound
            code_interval_list.list.append(c1)
        
        elif cc.symbols[0] == 1:
            u2 = cc.lowerBound + (probability) * range_
            
            # Novo objeto para símbolo 0
            c0 = CodeCandidate()
            c0.symbols = cc.symbols + [0]
            c0.upperBound = u2
            c0.lowerBound = cc.lowerBound
            c0.probability = c0.upperBound - c0.lowerBound
            code_interval_list.list.append(c0)

            # Novo objeto para símbolo 1
            c1 = CodeCandidate()
            c1.symbols = cc.symbols + [1]
            c1.upperBound = cc.upperBound
            c1.lowerBound = u2
            c1.probability = c1.upperBound - c1.lowerBound
            code_interval_list.list.append(c1)

    return code_interval_list

def matching_canditade_intervals(source_interval, code_interval_list):
    """Encontra os intervalos de símbolos que coincidem com os da fonte"""
    
    for cc in code_interval_list.list:
        if source_interval.lowerBound >= cc.lowerBound and source_interval.upperBound <= cc.upperBound:
            return True, cc
    return False, None

def find_code_interval_from_candidates(cc_list, searchList):
    """
    Finds the interval corresponding to a given sequence of symbols.
    """
    code_interval = Interval()
    for cc in cc_list.list:
        if cc.symbols == searchList:
            code_interval.lowerBound = cc.lowerBound
            code_interval.upperBound = cc.upperBound
            searchList.clear()     
    return code_interval

def output_and_rescale(source_interval, code_intervals, P_code):

    code_symbols = []
    cc = CodeCandidate()
    
    success, cc = matching_canditade_intervals(source_interval, code_intervals)
    
    while success:
        range_ = cc.upperBound - cc.lowerBound
        source_interval.lowerBound = (source_interval.lowerBound  - cc.lowerBound)/ range_
        source_interval.upperBound = (source_interval.upperBound- cc.lowerBound)/ range_
        #source_interval = rescale_source_interval(source_interval, new_low, new_high)
        print("\nIntervalo encontrado")
        print("Intervalo Fonte:")
        source_interval.print()
        print("Intervalo Candidato:") 
        cc.print_interval()
        code_symbols.extend(cc.symbols)
        
    
        code_intervals = update_code_interval(code_intervals, P_code)
        
        success, cc = matching_canditade_intervals(source_interval, code_intervals)

    return code_symbols, source_interval, code_intervals

def matching_canditade_intervals_finalize(source_interval, code_interval_list, P_code):
    """Encontra os intervalos de símbolos que coincidem com os da fonte"""
    new_code_interval_list = CodeCandidateList(code_interval_list.k)
    fin_intervals = {}
    fin_symbols = []
 
    for cc in code_interval_list.list:
        if (source_interval.lowerBound < cc.upperBound) and (source_interval.upperBound > cc.lowerBound):
            new_code_interval_list.list.append(cc)
    new_code_interval_list.k = len(new_code_interval_list.list)
    new_code_interval_list = update_code_interval(new_code_interval_list, P_code)

    for cc in new_code_interval_list.list:
        if (source_interval.lowerBound < cc.lowerBound) and (source_interval.upperBound > cc.upperBound):
            fin_intervals[cc.probability] = cc.symbols
    fin_symbols = fin_intervals[max(fin_intervals)]
    return fin_symbols