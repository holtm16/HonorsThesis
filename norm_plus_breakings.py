"""
Author: Michael Holt
Program: norm_plus_breakings.py
Date: 2015_8_4
Purpose: To find any requested level norm and the corresponding breakings that
         give us this norm value.
"""
import itertools

S1_N = []


"""---------------- Interface of Functions -----------------------"""
# Arguments: None
# Takes user input and returns the associated norms
def main():
    while True:  #We want to keep asking the user for input
        print()  
        str_seq = input("Give me a sequence of numbers (without []'s and with \n\
each number separated by a single space without commas): ")
        while str_seq == "":
            str_seq = input("\nSorry, you didn't enter a valid sequence. Give me another sequence of numbers (without []'s and with \n\
each number separated by a single space without commas): ")
        n = int(input("\nGive me a non-negative integer to indicate which level \n\
norm you want me to return: "))
        while n < 0:
            n = int(input("Sorry, your integer must be non-negative. Give \
me another integer: "))
        seq = str_seq.split()
        new_seq = [float(x) for x in seq]
        norm_tuple = find_nth_level_norm(new_seq, n)

        print("\nThe level %i norm is %.2f \ndue to the following sequences \
resulting in this value: " % (n, norm_tuple[0]))
        for element in norm_tuple[1]:
            print(element)
                  
    

# Arguments: input sequence of numbers seq; level n of desired Schreier norm
# Returns: a tuple containing the max summation of the ||Iix||_(n-1)'s
#           and all elements of the Schreier family that give that value
def find_nth_schreier_norm(seq, n):
    global S1_N
    if n == 1:
        return find_schreier_norm(seq)
    N = len(seq)
    S1_N = find_schreier_sets(N)
    max_value = 0
    elements_that_give_max_value = []
    for element_of_S1_N in S1_N:
        total_sum = 0
        list_of_lists_giving_max = []
        lyst_of_sequences = make_interval_sequences(seq, element_of_S1_N)
        for new_seq in lyst_of_sequences:
            temp_tuple = find_nth_level_norm(new_seq, n-1)
            total_sum += temp_tuple[0]
            list_of_lists_giving_max.append(temp_tuple[1])
        if total_sum == max_value:
            temp_lyst = get_all_combos_from_interval_lists(list_of_lists_giving_max)
            # Add these elements to list of elements giving max value
            for elem in temp_lyst:
                # Do not want to add duplicates
                if not (elem in elements_that_give_max_value):
                    elements_that_give_max_value.append(elem)
        elif total_sum > max_value:
            temp_lyst = get_all_combos_from_interval_lists(list_of_lists_giving_max)
            # Update the max value
            max_value = total_sum
            # Reset the list of elements that give the max value
            elements_that_give_max_value = temp_lyst          
    return (max_value, elements_that_give_max_value)

# Arguments: input sequence of numbers seq; level n of desired norm
# Returns: a tuple containing the n-th level norm and all elements
#           of the Schreier family that give that value
def find_nth_level_norm(seq, n):
    if seq == []:
        return (0, [])
    elif n == 0:
        return find_zero_norm(seq)
    elif n == 1:
        return find_first_level_norm(seq)
    else:               #For n >= 2
        nth_norm_tuple = find_nth_level_norm(seq, n-1)
        nth_norm_tuple_value = nth_norm_tuple[0]
        schreier_norm_tuple = find_nth_schreier_norm(seq, n)
        half_schreier_norm_value = 0.5*schreier_norm_tuple[0]
        if nth_norm_tuple_value > half_schreier_norm_value:
            return nth_norm_tuple
        elif half_schreier_norm_value > nth_norm_tuple_value:
            return (half_schreier_norm_value, schreier_norm_tuple[1])
        else:           #This case is reached only if the values are equal
            temp_lyst_of_elements = nth_norm_tuple[1]
            for element in schreier_norm_tuple[1]:
                if element not in temp_lyst_of_elements:
                    temp_lyst_of_elements.append(element)
            return (nth_norm_tuple_value, temp_lyst_of_elements)


"""---------------- Helper Functions -----------------------"""
    
# Arguments: input list of lists where each list is a list of indices of
#            a particular interval subsequence of a vector (like elements 3-5)
#            that norms that individual part of the intervalled sequence
# Returns: a distinguished representation of the indices to shows how it
#          breaks a sequence into intervals
def get_all_combos_from_interval_lists(list_of_tuple_lists):
    # product returns all ways to pick one element from each of the lists
    # in list_of_lists
    list_of_tuples = list(itertools.product(*list_of_tuple_lists))
    
    # Now we must remove elements with redundant indices
    new_list_of_tuples = []
    for i in range(len(list_of_tuples)):
        boolean = True
        temp_tuple = list_of_tuples[i]
        for j in range(len(temp_tuple)-1):
            first_int = strip_to_int(temp_tuple[j])
            first_int_2 = strip_to_int(temp_tuple[j+1])
            if first_int_2 <= first_int:
                boolean = False
        if strip_to_int(temp_tuple[0]) < len(temp_tuple):
            boolean = False
        if boolean == True:
            new_list_of_tuples.append(temp_tuple)
    return new_list_of_tuples
    """I do not think we need to check if we have tuples like (1, 5) and (2,4)
    within a temp_tuple since we only call this function on an input
    list of lists, with each list representing the ways to norm an intervalled
    subsequence of a given sequence. I make these intervalled subsequences
    using the function make_interval_sequences, which will truncate trailing
    zeroes. Therefore, there should be no way for the last index in one list
    of tuples to surpass the list index from another later tuple."""

# Arguments: tuple or integer
# Returns: the integer if input is an integer; the first integer in the tuple
def strip_to_int(tuple_or_int):
    if type(tuple_or_int) is int:
        return tuple_or_int
    return strip_to_int(tuple_or_int[0])    #The input is a tuple in this case

# Arguments: input sequence seq of numbers; element is
#            an element of the Schreier set
# Returns: a tuple containing the list of the I_ix's
def make_interval_sequences(seq, element):
    lyst_of_new_seq = []
    N = len(seq) + 1
    last = len(element)-1
    for i in range(last):
        temp_1 = element[i]
        temp_2 = element[i+1]
        # We now create sequences whose trailing zeroes are truncated
        new_seq = [0]*(temp_1 - 1) + seq[temp_1 - 1:temp_2 - 1]
        lyst_of_new_seq.append(new_seq)
    # Must still add the sequence where all values in seq are zeroed
    # out other than from the last index in element on
    last_new_seq = [0]*(element[last]-1) + seq[element[last]-1:]
    lyst_of_new_seq.append(last_new_seq)
    return lyst_of_new_seq
    
# Arguments: input sequence seq of numbers
# Returns: a tuple containing the maximum absolute value of an element
#           within the sequence and all indices of elements in seq of
#            that value
def find_zero_norm(seq):
    max_value = 0
    indices_that_give_max_value = []
    for i in range(len(seq)):
        abs_val_of_element = abs(seq[i])
        if abs_val_of_element == max_value:
            # Add this index to list of elements giving max value
            indices_that_give_max_value.append((i+1,))
        elif abs_val_of_element > max_value:
            # Update the max value
            max_value = abs_val_of_element
            # Reset the list of elements that give the max value
            indices_that_give_max_value = [(i+1,)]
    return (max_value, indices_that_give_max_value)

# Arguments: input sequence seq of numbers
# Returns: the tuple containing the first level norm of the input seq
#           and all elements of the Schreier family that give that value
def find_first_level_norm(seq):
    zero_norm_tuple = find_zero_norm(seq)
    zero_norm_tuple_value = zero_norm_tuple[0]
    schreier_norm_tuple = find_schreier_norm(seq)
    half_schreier_norm_value = 0.5*schreier_norm_tuple[0]
    if zero_norm_tuple_value > half_schreier_norm_value:
        return zero_norm_tuple
    elif half_schreier_norm_value > zero_norm_tuple_value:
        return (half_schreier_norm_value, schreier_norm_tuple[1])
    else:           #This case is reached only if the values are equal
        temp_lyst_of_elements = zero_norm_tuple[1]
        for element in schreier_norm_tuple[1]:
                if element not in temp_lyst_of_elements:
                    temp_lyst_of_elements.append(element)
        return (zero_norm_tuple_value, temp_lyst_of_elements)

# Arguments: input sequence of numbers seq
# Returns: a tuple containing the Schreier norm and all elements of
#           the Schreier family that give that value
def find_schreier_norm(seq):
    global S1_N
    max_value = 0
    elements_that_give_max_value = []
    S1_N = find_schreier_sets(len(seq))
    for element_of_S1_N in S1_N:
        total_sum = 0
        for i in element_of_S1_N:
            total_sum += abs(seq[i-1])
        if total_sum == max_value:
            elements_that_give_max_value.append(element_of_S1_N)
        elif total_sum > max_value:
            # Update the max value
            max_value = total_sum
            # Reset the list of elements that yield the max
            elements_that_give_max_value = [element_of_S1_N]
    return (max_value, elements_that_give_max_value)

# Arguments: a non-negative integer N
# Returns: a list of the significant Schreier sets in determining a Schreier
#           norm of a given sequence of size N
def find_schreier_sets(N):
    """Base Cases"""
    if N == 0:
        return []
    elif N == 1:
        return [tuple([1])]
    elif N == 2:
        return [tuple([1]), tuple([2])]

    S1_N = [tuple([1])]
    temp_lyst = []
    for j in range(1, N + 1):
        temp_lyst.append(j)             #Now temp_lyst contains all numbers
                                        #from 1 to N
    """Adding the necessary elements of the Schreier Set to S1_N"""
    for i in range(2, int(N/2 + 1)):
        #We use the built-in function combinations() below to give us i length
        #subsequences of temp_lyst[i-1:]
        lyst_of_tuples = list(itertools.combinations(temp_lyst[i-1:], i))
        for a_tuple in lyst_of_tuples:
            S1_N.append(a_tuple)
    #For any natural number greater than or equal to the floor M of N/2 + 1,
    #we just consider the subset [M, M+1, M+2, ..., N].
    #This subset is in the Schreier family, and we do NOT need to consider
    #proper subsets of this subset since we only consider absolute values of
    #elements in a given sequence x, making F =[M, M+1, M+2, ..., N] the
    #subset of itself for which the summation of |seq[i]|'s for i in F is
    #the greatest
    M = int(N/2 + 1)
    temp_subset = (M,)
    for j in range(M + 1, N + 1):
        temp_subset += (j,)
    if not(temp_subset in S1_N):
        S1_N.append(temp_subset)
    return S1_N
        

"""---------------- Function Calls -----------------------"""

main()

