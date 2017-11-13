class State(object):
    def __init__(self, left_mons: int, left_miss: int, right_mons: int, right_miss: int, parent_move=None,
                 boat_move_to_get_here=None):
        self.left_mons = left_mons
        self.left_miss = left_miss

        self.right_mons = right_mons
        self.right_miss = right_miss

        self.parent_move = parent_move
        self.boat_move_to_get_here = boat_move_to_get_here

    def check_and_transport(self, boat: tuple, return_journey=False) -> bool:
        """
        Checks if the transportation is possible and does it.
        :param boat: tuple representing the boat config -> (<no of monsters>, <no of missionaries>)
        :param return_journey: True if this is a return journey, else False
        :return: True if the transport operation was successful, else False
        """
        assert 1 <= sum(boat) <= 2, 'A boat may have 1 or 2 people at a time'

        # If the boat is impossible with the current state
        if return_journey:
            if self.right_mons < boat[0] or self.right_miss < boat[1]:
                return False

        elif self.left_mons < boat[0] or self.left_miss < boat[1]:
            return False

        # State after transportation
        if return_journey:
            left_mons_ = self.left_mons + boat[0]
            left_miss_ = self.left_miss + boat[1]

            right_mons_ = self.right_mons - boat[0]
            right_miss_ = self.right_miss - boat[1]

        else:
            left_mons_ = self.left_mons - boat[0]
            left_miss_ = self.left_miss - boat[1]

            right_mons_ = self.right_mons + boat[0]
            right_miss_ = self.right_miss + boat[1]

        # If no of monsters exceed the no of missionaries after performing the operation
        if 0 < left_miss_ < left_mons_ or 0 < right_miss_ < right_mons_:
            return False

        # Transport
        self.left_mons = left_mons_
        self.left_miss = left_miss_

        self.right_mons = right_mons_
        self.right_miss = right_miss_

        return True

    def get_next_possible_states(self, return_journey=False) -> set:
        """
        Get all the next possible states, given a state
        :param return_journey: True if this is a return journey, else False
        :return: a set of all possible states
        """
        result = set()
        for boat in ((0, 1), (1, 0), (1, 1), (0, 2), (2, 0)):
            state = State(self.left_mons, self.left_miss, self.right_mons, self.right_miss, self,
                          f'\ <monsters : {boat[0]}, missionaries: {boat[1]}> /')

            if state.check_and_transport(boat, return_journey):
                if state.left_miss + state.left_mons == 0:  # Check for success
                    parent = self
                    moves = [f'\ <monsters : {parent.left_mons}, missionaries: {parent.left_miss}> /']

                    while parent:
                        moves.append(parent.boat_move_to_get_here)
                        parent = parent.parent_move

                    rev = False
                    for move in reversed(moves):
                        if move:
                            if rev:
                                print(move, '<-')
                                rev = not rev

                            else:
                                print(move, '->')
                                rev = not rev

                    return set()

                else:
                    result.add(state)

        return result

    def __str__(self):
        return f'<monsters : {self.left_mons}, missionaries: {self.left_miss}> | ------ | <monsters : {self.right_mons}, missionaries: {self.right_miss}>'

    def __eq__(self, other):
        return (self.left_mons == other.left_mons and
                self.left_miss == other.left_miss and
                self.right_mons == other.right_mons and
                self.right_miss == other.right_miss)

    def __hash__(self):
        return hash((self.left_mons, self.left_miss, self.right_miss, self.right_mons))


def get_answer():
    states = State(monsters, missionaries, 0, 0).get_next_possible_states()

    return_journey = True
    while states:
        next_states = set()
        for state in states:
            next_state = state.get_next_possible_states(return_journey)
            if next_state:
                next_states.update(next_state)

            else:
                next_states = {}
                break
        states, return_journey = next_states, not return_journey


# Recursive Implementation, just in case someone needs it?
def get_ans_by_recursion():
    def x(states, return_journey):
        next_states = set()
        for state in states:
            next_state = state.get_next_possible_states(return_journey)

            if next_state:
                next_states.update(next_state)

            else:
                return None

        return x(next_states, not return_journey)

    states = State(monsters, missionaries, 0, 0).get_next_possible_states()

    x(states, True)


if __name__ == '__main__':
    monsters = int(input('Enter no of monsters: '))
    missionaries = int(input('Enter no of missionaries: '))

    get_answer()
