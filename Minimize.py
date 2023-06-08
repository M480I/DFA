from DFA import DFA


def minimize_dfa(dfa):
    # Step 1: Split states into two sets - final and non-final
    final_states = set(dfa.finals)
    non_final_states = set(dfa.states) - final_states

    # Step 2: Initialize the partition with the final and non-final sets
    partition = [final_states, non_final_states]

    # Step 3: Initialize the split queue with the partition
    split_queue = [final_states, non_final_states]

    # Step 4: Process the split queue
    while split_queue:
        current_set = split_queue.pop(0)
        for symbol in dfa.alphabet:
            # Step 5: Split the set based on the transitions for each symbol
            split_set = set()
            for state in current_set:
                next_state = dfa.transitions[(state, symbol)]
                for subset in partition:
                    if next_state in subset:
                        split_set = subset
                        break

            if len(split_set) < len(current_set):
                # Remove the current set from the partition and add the split sets
                partition.remove(current_set)
                partition.extend([split_set, current_set - split_set])

                # Update the split queue
                if current_set in split_queue:
                    split_queue.remove(current_set)
                    split_queue.extend([split_set, current_set - split_set])
                else:
                    split_queue.extend([split_set, current_set - split_set])

                break

    # Step 6: Create the minimized DFA
    minimized_states = []
    minimized_transitions = {}

    for subset in partition:
        state_name = ",".join(sorted(subset))
        minimized_states.append(state_name)

        for symbol in dfa.alphabet:
            next_state = dfa.transitions[(next(iter(subset)), symbol)]
            for idx, sub in enumerate(partition):
                if next_state in sub:
                    minimized_transitions[(state_name, symbol)] = ",".join(sorted(sub))
                    break

    minimized_start = ",".join(sorted([subset for subset in partition if dfa.start in subset][0]))
    minimized_finals = [",".join(sorted(subset)) for subset in partition if subset & final_states]

    minimized_dfa = DFA(
        states=minimized_states,
        alphabet=dfa.alphabet,
        start=minimized_start,
        finals=minimized_finals,
        transitions=minimized_transitions
    )

    return minimized_dfa
