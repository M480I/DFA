class DFA:

    def __init__(self, states, alphabet, start, finals, transitions):
        self.empty = True
        self.finite = True
        self.dfs_start = None
        self.length = None
        self.strings = []
        self.path = []
        self.reachable_to_finals = finals.copy()
        self.mark = []
        self.edge_mark = []

        self.states = states
        self.alphabet = alphabet
        self.start = start
        self.finals = finals
        self.transitions = transitions

    def is_empty(self):
        self.reset_dfs()
        self.dfs(self.start, self.check_mark, func=self.find_any_accept)
        if self.empty:
            return "This dfa's language is empty.\n"
        else:
            return "This dfa's language is not empty.\n"

    def is_finite(self):
        self.reset_dfs()
        self.dfs(self.start, self.check_mark, for_func=self.find_reachable_to_finals)
        for state in self.reachable_to_finals:
            self.reset_dfs()
            self.dfs_start = state
            self.dfs(state, self.check_mark, func=self.find_loop)
        if not self.finite:
            return "This dfa's language is not finite.\n"
        return "This dfa's language is finite.\n"

    def get_lang(self):
        self.reset_dfs()
        self.strings.clear()
        self.dfs(self.start, self.check_edge, func=self.find_lang, end_func=self.path_pop)

        self.is_finite()
        self.is_empty()
        if self.empty:
            return self.is_empty().removesuffix("\n") + failed("it's language")
        if not self.finite:
            return "This dfs's language is not finite." + failed("it's language")

        self.prep_lang()
        s = ""
        if len(self.strings) > 1:
            s = "s"

        return f"This language has {str(len(self.strings))} string{s} :\n\t" + " ".join(self.strings) + "\n"

    def get_lang_k(self, k):
        self.length = int(k)
        self.strings.clear()
        self.reset_dfs()
        self.dfs(self.start, self.check_path, func=self.find_lang_k, end_func=self.path_pop)
        s = ""
        if len(self.strings) > 1:
            s = "s"
        self.strings.sort()
        if len(self.strings) and self.strings[0] == "\"\"":
            self.strings[0] = "λ"
        return f"This language has {str(len(self.strings))} string{s} with length {self.length} :\n\t" + " ".join(
            self.strings)

    def check_string(self, string):
        state = self.start
        for symbol in string:
            if symbol not in self.alphabet:
                return f"\"{symbol}\" in \"{string}\" is not in alphabet.\n"
            state = self.transitions[(state, symbol)]
        if state in self.finals:
            return f"{string} is accepted.\n"
        return f"{string} is failed.\n"

    def get_min(self):
        self.is_empty()
        if self.empty:
            return self.is_empty().removesuffix("\n") + failed("the string with minimum length")
        self.get_lang()
        return f"{self.strings[0]} is the string with the minimum length.\n"

    def get_max(self):
        self.is_empty()
        if self.empty:
            return self.is_empty().removesuffix("\n") + failed("the string with maximum length")
        self.is_finite()
        if not self.finite:
            return "This DFA's language is not finite." + failed("the string with maximum length")
        self.get_lang()
        return f"{self.strings[-1]} is the string with the maximum length.\n"

    def get_sample_in(self):
        self.is_empty()
        self.is_finite()
        if self.empty:
            return self.is_empty().removesuffix("\n") + failed("two accepted strings")

        self.reset_dfs()
        self.strings.clear()
        self.dfs(self.start, self.check_lang_length, func=self.find_lang, end_func=self.path_pop)
        self.prep_lang()

        if len(self.strings) == 1:
            return f"{self.strings[0]} is the only accepted string.\n"

        string = " and ".join(self.strings[0:2])
        return f"{string} are two accepted strings.\n"

    def get_sample_out(self):
        comp = self.compliment()
        comp.is_empty()
        if comp.empty:
            return f"All possible strings with given alphabet are in this DFA." + failed("two failed strings")
        return comp.get_sample_in().replace("accepted", "failed")

    def prep_lang(self):
        self.strings.sort()
        if len(self.strings) and self.strings[0] == "\"\"":
            self.strings[0] = "λ"

    # dfs functions
    #   func
    def find_any_accept(self, state, symbol):
        if state in self.finals:
            self.empty = False

    #   for_func
    def find_reachable_to_finals(self, state, par_state, symbol):
        if par_state in self.reachable_to_finals:
            return
        if state in self.reachable_to_finals:
            self.reachable_to_finals.append(par_state)

    #   func
    def find_loop(self, state, symbol):
        for symbol in self.alphabet:
            next_state = self.transitions[(state, symbol)]
            if next_state == self.dfs_start:
                self.finite = False

    #   func
    def find_lang(self, state, symbol):
        if symbol is not None:
            self.path.append(symbol)
        if state in self.finals:
            self.strings.append("\"" + "".join(self.path) + "\"")

    #   func
    def find_lang_k(self, state, symbol):
        if symbol is not None:
            self.path.append(symbol)
        if state in self.finals and self.length == len(self.path):
            self.strings.append("\"" + "".join(self.path) + "\"")

    #   end_func
    def path_pop(self, state, symbol):
        if len(self.path):
            self.path.pop()

    #   dfs_con
    def check_mark(self, state, symbol):
        return state not in self.mark

    #   dfs_con
    def check_reachable(self, state, symbol):
        return state in self.reachable_to_finals

    #   dfs_con
    def check_path(self, state, symbol):
        return len(self.path) < self.length

    #   dfs_con
    def check_edge(self, state, symbol):
        return (symbol, state) not in self.edge_mark

    #   dfs_con
    def check_lang_length(self, state, symbol):
        return len(self.strings) < 2 and self.check_reachable(state, symbol)

    # reset
    def reset_dfs(self):
        self.mark.clear()
        self.edge_mark.clear()

    def dfs(self, state, dfs_con, symbol=None, func=None, for_func=None, end_func=None):
        self.mark.append(state)
        if symbol is not None:
            self.edge_mark.append((symbol, state))
        if func is not None:
            func(state, symbol)
        for next_symbol in self.alphabet:
            next_state = self.transitions[(state, next_symbol)]
            if dfs_con(next_state, next_symbol):
                self.dfs(next_state, dfs_con, next_symbol, func, for_func, end_func)
                if for_func is not None:
                    for_func(next_state, state, symbol)
        if end_func is not None:
            end_func(state, symbol)

    def compliment(self):
        compliment_finals = []
        for state in self.states:
            if state not in self.finals:
                compliment_finals.append(state)
        return DFA(self.states, self.alphabet, self.start, compliment_finals, self.transitions)

    
def failed(string):
    return f" Failed to print {string}.\n"
