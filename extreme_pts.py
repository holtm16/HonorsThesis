"""
Author: Michael Holt
Program: extreme_pts.py
Date: 2015_9_11
Purpose: To find out whether or not a vector is an extreme point of B_T.
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
        norm_value = find_nth_level_norm(new_seq, n)
        list_of_unchanged_norm_seqs = vectors_still_same_norm(new_seq, n)
        print("\nThe level %i norm is %.2f. \nThe following vectors \
maintained that norm value of %.2f:" % (n, norm_value, norm_value))
        for element in list_of_unchanged_norm_seqs:
            print(element)
        
# Arguments: input sequence of numbers seq; desired norm_level
# Returns: a list of sequences that have been slightly altered
#          from the input sequence whose norm has remained unchanged
def vectors_still_same_norm(seq, norm_level):
    epsilon = (1/10)*find_smallest_value(seq)
    previous_norm_value = find_nth_level_norm(seq, norm_level)
    list_of_new_seqs = make_all_epsilon_combos(seq, epsilon)
    list_of_unchanged_norm_seqs = []
    for new_seq in list_of_new_seqs:
        temp_seq = list(new_seq)
        if find_nth_level_norm(temp_seq, norm_level) == previous_norm_value:
            if temp_seq != seq:         #Want to make sure we have altered seq
                                        #in some way
                list_of_unchanged_norm_seqs.append(new_seq)
    return list_of_unchanged_norm_seqs

# Arguments: input sequence of numbers seq; level n of desired Schreier norm
# Returns: the n-th Schreier norm
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
            total_sum += find_nth_level_norm(new_seq, n-1)
        if total_sum > max_value:
            # Update the max value
            max_value = total_sum         
    return max_value

# Arguments: input sequence of numbers seq; level n of desired norm
# Returns: the n-th level norm
def find_nth_level_norm(seq, n):
    if seq == []:
        return 0
    elif n == 0:
        return find_zero_norm(seq)
    elif n == 1:
        return find_first_level_norm(seq)
    else:               #For n >= 2
        nth_norm_value = find_nth_level_norm(seq, n-1)
        half_schreier_norm_value = 0.5*find_nth_schreier_norm(seq, n)
        if nth_norm_value >= half_schreier_norm_value:
            return nth_norm_value
        else:           #half_schreier_norm_value > nth_norm_value:
            return half_schreier_norm_value


"""---------------- Helper Functions -----------------------"""
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
# Returns: the zero norm
def find_zero_norm(seq):
    max_value = 0
    for i in range(len(seq)):
        abs_val_of_element = abs(seq[i])
        if abs_val_of_element > max_value:
            # Update the max value
            max_value = abs_val_of_element
    return max_value

# Arguments: input sequence seq of numbers
# Returns: the first level norm 
def find_first_level_norm(seq):
    zero_norm_value = find_zero_norm(seq)
    half_schreier_norm_value = 0.5*find_schreier_norm(seq)
    if zero_norm_value >= half_schreier_norm_value:
        return zero_norm_value
    else:      #half_schreier_norm_value > zero_norm_value:
        return half_schreier_norm_value


# Arguments: input sequence of numbers seq
# Returns: the Schreier norm 
def find_schreier_norm(seq):
    global S1_N
    max_value = 0
    S1_N = find_schreier_sets(len(seq))
    for element_of_S1_N in S1_N:
        total_sum = 0
        for i in element_of_S1_N:
            total_sum += abs(seq[i-1])
        if total_sum > max_value:
            # Update the max value
            max_value = total_sum
    return max_value

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

# Arguments: input sequence seq of numbers
# Returns: the smallest absolute value within the sequence
def find_smallest_value(seq):
    min_value = 10
    for i in range(len(seq)):
        abs_val_of_element = abs(seq[i])
        if abs_val_of_element < min_value:
            # Update the min value
            min_value = abs_val_of_element
    return min_value


# Arguments: input sequence seq of numbers, a small number epsilon
# Returns: list of all possible sequences (as tuples) gotten when having three options
#           for each coordinate (add epsilon to it, subtract epsilon from it,
#           or leave it unchanged)
def make_all_epsilon_combos(seq, epsilon):
    list_of_lists_of_3_options = []
    for element in seq:
        temp_list = []
        temp_list.append(element)
        temp_list.append(element+epsilon)
        temp_list.append(element-epsilon)
        list_of_lists_of_3_options.append(temp_list)
    # product returns all ways to pick one element from each of the lists
    # in list_of_lists_of_3_options
    return list(itertools.product(*list_of_lists_of_3_options))
    
    
    
        
        
    
        

"""---------------- Function Calls -----------------------"""

main()

