from DFA import DFA


def build_combined_dfa(dfa1: DFA, dfa2: DFA):  # returns DFA without finals
    start = f"{dfa1.start},{dfa2.start}"

    alphabet = dfa1.alphabet

    states = []
    for state1 in dfa1.states:
        for state2 in dfa2.states:
            states.append(f"{state1},{state2}")

    transitions = {}
    for state1 in dfa1.states:
        for state2 in dfa2.states:
            for symbol in alphabet:
                des1 = dfa1.transitions[(state1, symbol)]
                des2 = dfa2.transitions[(state2, symbol)]
                transitions[(f"{state1},{state2}", symbol)] = f"{des1},{des2}"

    return DFA(states, alphabet, start, [], transitions)


def intersection_dfa(dfa1: DFA, dfa2: DFA):
    combined_dfa = build_combined_dfa(dfa1, dfa2)

    finals = []
    for state1 in dfa1.states:
        for state2 in dfa2.states:
            if state1 in dfa1.finals and state2 in dfa2.finals:
                finals.append(f"{state1},{state2}")

    return DFA(combined_dfa.states, combined_dfa.alphabet, combined_dfa.start, finals, combined_dfa.transitions)


def union_dfa(dfa1: DFA, dfa2: DFA):
    combined_dfa = build_combined_dfa(dfa1, dfa2)

    finals = []
    for state1 in dfa1.states:
        for state2 in dfa2.states:
            if state1 in dfa1.finals or state2 in dfa2.finals:
                finals.append(f"{state1},{state2}")

    return DFA(combined_dfa.states, combined_dfa.alphabet, combined_dfa.start, finals, combined_dfa.transitions)


def difference_dfa(dfa1: DFA, dfa2: DFA):
    dfa3 = dfa2.compliment()
    return intersection_dfa(dfa1, dfa3)


def are_equivalent(dfa1: DFA, dfa2: DFA):
    diff1 = difference_dfa(dfa1, dfa2)
    diff2 = difference_dfa(dfa2, dfa1)
    return diff1.is_empty() and diff2.is_empty()


def are_separate(dfa1: DFA, dfa2: DFA):
    return intersection_dfa(dfa1, dfa2).is_empty()
