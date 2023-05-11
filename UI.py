from DFA import DFA


def input_dfa():
    states = input("Enter the states:\n> ").split(" ")
    alphabet = input("Enter the alphabet(default is {a, b}):\n> ").split(" ")
    if alphabet[0] == "":
        alphabet = ["a", "b"]
    start = input("Enter the starting state:\n> ")
    while start not in states:
        start = input("Not a state. Try again:\n> ")
    finals = input("Enter the final states:\n> ").split(" ")
    if finals[0] == "":
        finals = []
    for i, state in enumerate(finals):
        while state not in states:
            state = input(f"{state} is not a state. Try again:\n> ")
            finals[i] = state
    transitions = {}
    for state in states:
        for symbol in alphabet:
            next_state = input(f"Enter δ({state}, {symbol}):\n> ")
            while next_state not in states:
                next_state = input("Not a state. Try again:\n> ")
            transitions[(state, symbol)] = next_state

    return DFA(states, alphabet, start, finals, transitions)


def output_dfa(dfa):
    res = ""
    res += "States:\n\t"
    res += " ".join(dfa.states) + "\n"
    res += "Alphabet:\n\t"
    res += " ".join(dfa.alphabet) + "\n"
    res += "The starting state:\n\t"
    res += dfa.start + "\n"
    res += "The final states:\n\t"
    res += " ".join(dfa.finals) + "\n"
    res += "The transitions:\n"
    for state in dfa.states:
        for symbol in dfa.alphabet:
            res += f"\tδ({state}, {symbol}) = {dfa.transitions[(state, symbol)]}\n"
    return res
