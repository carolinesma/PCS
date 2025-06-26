import math
import numpy as np
from typing import List
import copy
from itertools import tee

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

    def print(self):   
        print(f"Upper Bound: {self.upperBound}")
        print(f"Lower Bound: {self.lowerBound}")
        print(f"Probability: {self.probability}")
        print(f"Symbols: {self.symbols}")

class SourceInterval:
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


def update_src_interval(src_interval, src_probability, src_symbols):
    """
    Updates the source interval based on the symbol and probability model.
    """
    newborder = np.uint32(src_interval.lowerBound + (np.uint32(src_interval.upperBound - src_interval.lowerBound) * src_probability[0]))
    if src_symbols == 0:
        src_interval.upperBound = np.uint32(newborder)
    else:
        src_interval.lowerBound = np.uint32(newborder)   

def find_identified_code_candidate_index(src_interval, cc_list, n_i):
    """
    Returns the index of the code candidate identified by the current source interval.
    """
    for i, cc in enumerate(cc_list.list):
        if src_interval.lowerBound <= cc.lowerBound and cc.lowerBound < src_interval.upperBound and n_i[i] != 0:
            return i
    return -1

def update_n_i(n_i, symbol_list):
    """
    Updates the frequency vector n_i by decreasing the count for each symbol in symbol_list.
    """
    for symbol in symbol_list:
        n_i[symbol-1] -= 1

def update_code_candidates(cc_list, n_i):
    """
    Recomputes the list of code candidates based on the current symbol frequencies.
    """
    cc_list.list.clear()
    n = 0
    sum_n_i = np.uint32(0)
    sum_p_i = np.uint32(0)
    n = np.uint32(sum(n_i))
        
    for i in range(0, cc_list.k):
        cc_push = CodeCandidate()
        cc_push.lowerBound = np.uint32(sum_p_i)
        sum_n_i += np.uint32(n_i[i])

        sum_p_i = np.uint64(sum_n_i << 31)//n
        if sum_p_i > 1<<31:
            sum_p_i = np.uint32(1<<31)
        if i == cc_list.k - 1:
            cc_push.upperBound = np.uint32(1<<31)
        else:
            cc_push.upperBound = np.uint32(sum_p_i)
        cc_push.probability = cc_push.upperBound - cc_push.lowerBound
        cc_push.symbols = [i+1]
        cc_list.list.append(cc_push)

def find_code_interval_from_candidates(cc_list, searchList):
    """
    Finds the interval corresponding to a given sequence of symbols.
    """
    code_interval = SourceInterval()
    for cc in cc_list.list:
        if cc.symbols == searchList:
            code_interval.lowerBound = cc.lowerBound
            code_interval.upperBound = cc.upperBound
            searchList.clear()     
    return code_interval

def finalize_code_symbols(src_interval, cc_list, n_i):
    """
    Finalizes symbol decoding by finding the last valid code candidate.
    """
    cc_index = find_identified_code_candidate_index(src_interval, cc_list, n_i)
    if cc_index == -1:
        return []
    cc = cc_list.list[cc_index]
    symbols_new = cc.symbols
    update_n_i(n_i, cc.symbols)
    for i in range(0, cc_list.k):
        for j in range(0, n_i[i]):
          symbols_new.append(i+1)
    return symbols_new

def check_for_output_and_rescale(src_interval, cc_list, n_i):
    """
    Checks whether the current interval falls within a candidate and rescales if needed.
    """
    cc = CodeCandidate()
    code_symbols_new = []
    success = False  
    
    for cc in cc_list.list:
        if src_interval.lowerBound >= cc.lowerBound and src_interval.upperBound <= cc.upperBound:
            success = True
            break

    while success:
        src_interval.lowerBound = np.uint32(np.uint64((src_interval.lowerBound - cc.lowerBound) << 31) // (cc.upperBound - cc.lowerBound))
        src_interval.upperBound = np.uint32(np.uint64((src_interval.upperBound - cc.lowerBound) << 31) // (cc.upperBound - cc.lowerBound))
        if src_interval.upperBound > 1<<31:  
            src_interval.upperBound = 1<<31

        update_n_i(n_i, cc.symbols)

        code_symbols_new.extend(cc.symbols)

        update_code_candidates(cc_list, n_i)
        success = False
        for cc in cc_list.list:
            if src_interval.lowerBound >= cc.lowerBound and src_interval.upperBound <= cc.upperBound:
                success = True
                break

    return code_symbols_new

def encode(src_symbols, n_i_vect):
    """
    Encodes a sequence using constant composition arithmetic coding (CCDM).

    Parameters
    ----------
    src_symbols : list
        Source symbols to be encoded.
    n_i_vect : list
        Target symbol distribution (absolute counts).

    Returns
    -------
    list
        Encoded symbol sequence.
    """
    k = len(n_i_vect)    
    n_i = [0] * k
    psrc = np.array([0.5, 0.5])
    code_symbols = []

    src_interval = SourceInterval(np.uint32(0), np.uint32(1<<31))
    cc_list = CodeCandidateList(k)

    for i in range(0, k):
      n_i[i] =n_i_vect[i]
	
    n_i[k-1] = n_i_vect[k-1]

    update_code_candidates(cc_list, n_i)
    
    for src_symbol in src_symbols:
        update_src_interval(src_interval, psrc, src_symbol)
        new_sym = check_for_output_and_rescale(src_interval, cc_list, n_i)
        if new_sym:
            code_symbols.extend(new_sym)

    fin_symbols = finalize_code_symbols(src_interval, cc_list, n_i)
    code_symbols.extend(fin_symbols)

    return code_symbols

def decode(code_symbols, n_i_vect, m):
    """
    Decodes a sequence encoded with constant composition arithmetic coding.

    Parameters
    ----------
    code_symbols : list
        Encoded symbol sequence.
    n_i_vect : list
        Target symbol distribution.
    m : int
        Length of the original source message.

    Returns
    -------
    list
        Decoded source symbols.
    """
    n = len(code_symbols)
    k = len(n_i_vect)
    n_i = [0] * k
    n_i_future = [0] * k
    n_i_future[:] = n_i_vect[:]
    n_future = n
    
    sum_n_i = np.uint32(0)
    new_border = np.uint32(0)
    
    src_interval = SourceInterval(np.uint32(0), np.uint32(1<<31))
    code_interval = SourceInterval()
    cc_list = CodeCandidateList(k)

    for i in range(0, k):
        n_i[i] = n_i_vect[i]
    
    n_i[k-1] = n_i_vect[k-1]
    update_code_candidates(cc_list, n_i)

    src_symbols = [0] * m
    src_symbol_index = 0
    code_symbols_unprocessed = []

    index_code_symbol_iterator = 0
    index_code_interval_symbol_iterator = 0

    while index_code_symbol_iterator <= len(code_symbols):
        current_symbol = code_symbols[index_code_symbol_iterator]
        code_symbols_unprocessed.append(current_symbol)    
        code_interval = find_code_interval_from_candidates(cc_list, code_symbols_unprocessed)
        index_code_interval_symbol_iterator = index_code_symbol_iterator + 1
        n_future = n
        for i in range(0, k):
            n_i_future[i] = n_i[i]
        
        if n_i_future[current_symbol - 1] > 0:
            n_i_future[current_symbol - 1] -= 1
        n_future -= 1

        scaling_performed = False
        while not scaling_performed:
            new_border = np.uint32(src_interval.lowerBound + (np.uint32(src_interval.upperBound - src_interval.lowerBound) * 0.5))
            
            while code_interval.lowerBound >= new_border or code_interval.upperBound < new_border:
                if code_interval.lowerBound >= new_border:
                    src_symbols[src_symbol_index] = 1
                    src_symbol_index += 1
                    src_interval.lowerBound = new_border

                elif code_interval.upperBound < new_border:
                    src_symbols[src_symbol_index] = 0
                    src_symbol_index += 1
                    src_interval.upperBound = new_border

                if src_symbol_index >= m:
                    return src_symbols

                new_border = np.uint32(src_interval.lowerBound + (np.uint32(src_interval.upperBound - src_interval.lowerBound) * 0.5))

                checksrc_interval = copy.copy(src_interval)
                checkcode = check_for_output_and_rescale(checksrc_interval, cc_list, n_i)
                if checksrc_interval.lowerBound != src_interval.lowerBound or checksrc_interval.upperBound != src_interval.upperBound:
                    index_code_symbol_iterator = index_code_symbol_iterator + len(checkcode)
                    src_interval = checksrc_interval
                    scaling_performed = True
                    break
            
            if index_code_interval_symbol_iterator >= len(code_symbols):
                code_interval.upperBound = np.uint32(code_interval.lowerBound + (np.uint64(code_interval.upperBound - code_interval.lowerBound) * 0.5))
            else:
                code_interval_symbol = code_symbols[index_code_interval_symbol_iterator]
                buffer = SourceInterval()
                
                n = np.uint32(sum(n_i_future))
                sum_n_i = np.uint32(sum(n_i_future[:code_interval_symbol - 1]))
                lbound = np.uint64(np.uint64(sum_n_i << 31) // n)
                sum_n_i += np.uint32(n_i_future[code_interval_symbol - 1])
                ubound = np.uint64(np.uint64(sum_n_i << 31) // n)
                if (ubound < lbound):
                    ubound = 1 << 31
                
                buffer.lowerBound = np.uint32(code_interval.lowerBound  + ((np.uint64(code_interval.upperBound  - code_interval.lowerBound)* lbound) >> np.uint64(31)))
                buffer.upperBound = np.uint32(code_interval.lowerBound  + ((np.uint64(code_interval.upperBound  - code_interval.lowerBound)* ubound) >> np.uint64(31)))
                code_interval = buffer

                if n_i_future[code_interval_symbol - 1] > 0:
                    n_i_future[code_interval_symbol - 1] -= 1
                n_future -= 1
                
                index_code_interval_symbol_iterator+=1