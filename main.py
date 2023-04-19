
####### Problem 3 #######

test_cases = [('book', 'back'), ('kookaburra', 'kookybird'), ('elephant', 'relevant'), ('AAAGAATTCA', 'AAATCA')]

alignments = [('book', 'back'), ('kookaburra', 'kookybird-'), ('relev-ant','-elephant'), ('AAAGAATTCA', 'AAA---T-CA')]

def MED(S, T):
    # TO DO - modify to account for insertions, deletions and substitutions
    # If the last characters of S and T are the same, no edit is needed
    if (S == ""):
        return(len(T))
    elif (T == ""):
        return(len(S))
    else:
        if (S[0] == T[0]):
            return(MED(S[1:], T[1:]))
        else:
            return(1 + min(MED(S, T[1:]), MED(S[1:], T)))

def fast_MED(S, T, MED={}):
    # TODO -  implement memoization
    if (S, T) in MED:
        return MED[(S, T)]

    if (S == ""):
        result = len(T)
    elif (T == ""):
        result = len(S)
    else:
        if (S[0] == T[0]):
            result = fast_MED(S[1:], T[1:], MED)
        else:
            result = 1 + min(fast_MED(S, T[1:], MED), fast_MED(S[1:], T, MED))
    
    MED[(S, T)] = result
    return result
    pass

def fast_align_MED(S, T, MED={}):
    # TODO - keep track of alignment
    if (S, T) in MED:
        return MED[(S, T)]

    if (S == ""):
        result = ("-" * len(T), T)
    elif (T == ""):
        result = (S, "-" * len(S))
    else:
        if (S[0] == T[0]):
            aligned_S, aligned_T = fast_align_MED(S[1:], T[1:], MED)
            result = (S[0] + aligned_S, T[0] + aligned_T)
        else:
            aligned_S_insert, aligned_T_insert = fast_align_MED(S, T[1:], MED)
            aligned_S_delete, aligned_T_delete = fast_align_MED(S[1:], T, MED)
            aligned_S_substitute, aligned_T_substitute = fast_align_MED(S[1:], T[1:], MED)

            insert_cost = fast_MED(S, T[1:])
            delete_cost = fast_MED(S[1:], T)
            substitute_cost = fast_MED(S[1:], T[1:])

            min_cost = min(insert_cost, delete_cost, substitute_cost)

            if min_cost == insert_cost:
                result = ("-" + aligned_S_insert, T[0] + aligned_T_insert)
            elif min_cost == delete_cost:
                result = (S[0] + aligned_S_delete, "-" + aligned_T_delete)
            else:
                result = (S[0] + aligned_S_substitute, T[0] + aligned_T_substitute)

    MED[(S, T)] = result
    return result
    pass

def test_MED():
    for S, T in test_cases:
        assert fast_MED(S, T) == MED(S, T)
                                 
def test_align():
    for i in range(len(test_cases)):
        S, T = test_cases[i]
        align_S, align_T = fast_align_MED(S, T)
        assert (align_S == alignments[i][0] and align_T == alignments[i][1])


test_MED()
test_align()

