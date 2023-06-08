from DFA import DFA


class NFA:
    def __init__(self, states, alphabet, start, finals, transitions):
        self.lambda_closure = {}
        self.mark = []
        self.delta_star = {}

        self.states = states
        self.alphabet = alphabet
        self.start = start
        self.finals = finals
        self.transitions = transitions

    def build_delta_star(self):
        for state in self.states:  # building lambda closure
            self.mark.clear()
            self.lambda_closure[state] = {state}
            self.dfs_lambda(state, state)

        for state in self.states:
            for symbol in self.alphabet:
                self.delta_star[(state, symbol)] = set({})

                for n_state in self.lambda_closure[state]:
                    for n_n_state in self.transitions[(n_state, symbol)]:
                        self.delta_star[(state, symbol)] = self.delta_star[(state, symbol)].union(
                            self.lambda_closure[n_n_state])

    def to_dfa(self):
        self.build_delta_star()
        trapneeded = False

        dfa_states = [self.start]
        dfa_alphabet = self.alphabet
        dfa_start = self.start
        dfa_finals = []
        dfa_transitions = {}

        states_todo = [self.start]

        while len(states_todo):
            c_state = states_todo.pop(-1)
            states = c_state.split(",")

            for state in states:
                if state in self.finals:
                    dfa_finals.append(c_state)
                    break

            for symbol in self.alphabet:

                dist = set({})
                for state in states:
                    dist = dist.union(self.delta_star[(state, symbol)])

                if not len(dist):
                    dfa_transitions[(c_state, symbol)] = "Trap"
                    trapneeded = True
                    continue

                dist = list(dist)
                dist.sort()
                n_state = ",".join(dist)

                if n_state not in dfa_states:
                    dfa_states.append(n_state)
                    states_todo.append(n_state)

                dfa_transitions[(c_state, symbol)] = n_state

        if trapneeded:
            dfa_states.append("Trap")
            for symbol in self.alphabet:
                dfa_transitions[("Trap", symbol)] = "Trap"

        return DFA(dfa_states, dfa_alphabet, dfa_start, dfa_finals, dfa_transitions)

    def dfs_lambda(self, start, state):
        self.mark.append(state)

        for next_state in self.transitions[(state, "λ")]:
            if next_state not in self.mark:
                self.lambda_closure[start].add(next_state)
                self.dfs_lambda(start, next_state)
