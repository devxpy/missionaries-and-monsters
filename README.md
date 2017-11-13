# missionaries and monsters

A solution to [this](https://en.wikipedia.org/wiki/Missionaries_and_cannibals_problem) game   
Supports python > 3.6

It has a `State` object representing the current state of the game. 

`get_next_possible_states` method figures out the possible sub-states (by figuring out the possible combinations for a boat, given a state). Conveniently returns empty set in case the required state is achieved

`check_and_transport` method is for checking if a boat combination is valid, and updates the state accordingly

the main loop successively calls the `get_next_possible_states` on each sub-state, which it receives from `get_next_possible_states` until the required state is achieved.
