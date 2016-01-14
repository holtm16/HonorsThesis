"""
Author: Michael Holt
Program: breaking_possibilities.py
Date: 2015_11_1
Purpose: To return a list of all functionals that are useful.
"""
import itertools
import math

S1_N = []


"""---------------- Interface of Functions -----------------------"""
# Arguments: integer n >= 7
# Takes an input integer n (>= 7) and returns all possible ways to break the
# vectors of length n
def main():
    while True:  #We want to keep asking the user for input
        print()  
        vec_length = input("Give me a vector length: ")
        while vec_length == "" or vec_length == "1":
            vec_length = input("\nSorry, you didn't enter a valid length. Give me a length: ")
        vec_length = int(vec_length)
        for elem in make_all_breakings(1, vec_length, math.ceil((vec_length - 3) / 2)):
            print(elem)
 
                                


                  
# Arguments: integer n
# Returns the union of the set of all sets F with #F = minF and maxF <= n AND the set
# of all sets {k, ..., n} : k >= ceiling((n+1)/2) 
def S_maxn(n):
    # First we build the set of all sets F with #F = minF and maxF <= n; call it set_1
    set_1 = []
    """Base Cases"""
    if n == 0:
        set_1 = []
    else:
        set_1 = [tuple([1])]
        #for n = 1 or 2, (1,) will be the only element
        temp_lyst = []
        for j in range(1, n + 1):
            temp_lyst.append(j)
        for i in range(2, int((n+3)/2)):
            #We use the built-in function combinations() below to give us i-1 length
            #subsequences of temp_lyst[i-1:]
            lyst_of_tuples = list(itertools.combinations(temp_lyst[i:], i-1))
            for a_tuple in lyst_of_tuples:
                temp_elem = tuple([tuple([i])])
                for num in a_tuple:
                    temp_elem += tuple([tuple([num])])
                if len(temp_elem) > 2: 
                    set_1.append(temp_elem)
    # Now we build all sets {k, ..., n} : k >= ceiling((n+1)/2); call it set_2
    set_2 = []
    # Note that we are not looping for n below, because that would give a singleton
    begin_index = math.ceil((n+1)/2)
    for k in range(begin_index, n):
        temp_set = tuple([tuple([k])])
        for m in range(k+1, n+1):
            temp_set += tuple([tuple([m])])
        if not temp_set in set_1 and len(temp_set) > 2:
            set_2.append(temp_set)
    return set_1 + set_2


# Arguments: integer n, smaller integer m
# Returns the set of all sets F within S_maxn(n) such that minF = m
def S_maxn_minm(n, m):
    return_set = []
    set_of_S_maxn = S_maxn(n)
    for F in set_of_S_maxn:
        if min(F) == (m,):
            return_set.append(F)
    return return_set


# Arguments: integer n, smaller integer m
# Returns the set of all sets F within S_maxn(n) such that minF >= m
def S_maxn_minm_and_up(n, m):
    return_set = []
    set_of_S_maxn = S_maxn(n)
    for F in set_of_S_maxn:
        if strip_to_int(min(F)) >= m:
            return_set.append(F)
    return return_set


# Arguments: a tuple of length greater than one; an index end to indicate where to stop
# Returns a list of all tuples that can be created by breaking up this tuple
# once
def break_up_a_tuple(temp_tuple, end):
    lyst_for_breaking_all_parts = []
    for i in range(len(temp_tuple)):
        first_elem = temp_tuple[i]
        len_of_elem = len(first_elem)
        # If the length is 1, we are dealing with just an integer
        if len_of_elem == 1:
            # First we handle if we are not at the last index
            if i < len(temp_tuple)-1:
                second_elem = temp_tuple[i+1]
                temp_lyst = S_maxn_minm(strip_to_int(second_elem)-1, strip_to_int(first_elem))
                # Must add the singleton to this list of options
                temp_lyst.append(first_elem)
                lyst_for_breaking_all_parts.append(temp_lyst)
            # Now we handle the last case (from last index to end)
            else:
                temp_lyst = S_maxn_minm(end, strip_to_int(first_elem))
                # Must add the singleton to this list of options
                temp_lyst.append(first_elem)
                lyst_for_breaking_all_parts.append(temp_lyst)
        else:  #Should be a longer tuple in this case
            # First we handle if we are not at the last index
            if i < len(temp_tuple)-1:
                second_elem = temp_tuple[i+1]
                lyst_for_breaking_all_parts.append(break_up_a_tuple(first_elem,strip_to_int(second_elem)-1))
            # Now we handle the last case (from last index to end)
            else:
                lyst_for_breaking_all_parts.append(break_up_a_tuple(first_elem,end))
    # product returns all ways to pick one element from each of the lists
    # in lyst_for_breaking_all_parts
    return list(itertools.product(*lyst_for_breaking_all_parts))


# Arguments: tuple or integer
# Returns: the integer if input is an integer; the first integer in the tuple
def strip_to_int(tuple_or_int):
    if type(tuple_or_int) is int:
        return tuple_or_int
    return strip_to_int(tuple_or_int[0])    #The input is a tuple in this case


# Arguments: integer start, bigger integer end, positive integer level
# Returns the set of all sets F within the given level that could potentially
# norm a vector of length n that starts at index start and ends at index end
def make_all_breakings(start, end, level):
    return_lyst = []
    if level == 0:
        # We add all the 0 norm options
        for i in range(start,end+1):
            return_lyst.append(tuple([i]))
        return return_lyst
    elif level == 1:
        return_lyst = make_all_breakings(start, end, 0)
        for elem in S_maxn_minm_and_up(end, start):
            # We avoid adding (1,) twice
            if elem not in return_lyst:
                return_lyst.append(elem)
        return return_lyst
    else:
        lower_level = make_all_breakings(start, end, level-1)
        for temp_tuple in lower_level:
            len_of_tup = len(temp_tuple)
            if len_of_tup > 1:
                lyst_of_tuples = break_up_a_tuple(temp_tuple, end)
                for a_tuple in lyst_of_tuples:
                    # We look to avoid duplicates
                    if not a_tuple in lower_level:
                        return_lyst.append(a_tuple)
        return lower_level + return_lyst


main()
             
            
        
            
        
        
        
    
