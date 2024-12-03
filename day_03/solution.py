from __future__ import annotations


class State:
    def __init__(self) -> None:
        pass

    def make_transition(self, _input: str) -> State:
        return StateStart()

    def make_action(self, _input: str, fsm: FSM) -> None:
        pass


class StateStart(State):
    def make_transition(self, _input: str) -> State:
        if _input == 'm':
            return StateM()
        return StateStart()

    def make_action(self, _input: str, fsm: FSM) -> None:
        fsm.reset()


class StateM(State):
    def make_transition(self, _input: str) -> State:
        if _input == 'u':
            return StateMU()
        return StateStart()


class StateMU(State):
    def make_transition(self, _input: str) -> State:
        if _input == 'l':
            return StateMUL()
        return StateStart()


class StateMUL(State):
    def make_transition(self, _input: str) -> State:
        if _input == '(':
            return StateLB()
        return StateStart()


class StateLB(State):
    def make_transition(self, _input: str) -> State:
        if _input.isdigit():
            return StateD1()
        return StateStart()


class StateD1(State):
    def make_transition(self, _input: str) -> State:
        if _input.isdigit():
            return StateD2()
        if _input == ',':
            return StateComma()
        return StateStart()

    def make_action(self, _input: str, fsm: FSM) -> None:
        fsm.push_x(_input)


class StateD2(State):
    def make_transition(self, _input: str) -> State:
        if _input.isdigit():
            return StateD3()
        if _input == ',':
            return StateComma()
        return StateStart()

    def make_action(self, _input: str, fsm: FSM) -> None:
        fsm.push_x(_input)


class StateD3(State):
    def make_transition(self, _input: str) -> State:
        if _input == ',':
            return StateComma()
        return StateStart()

    def make_action(self, _input: str, fsm: FSM) -> None:
        fsm.push_x(_input)


class StateComma(State):
    def make_transition(self, _input: str) -> State:
        if _input.isdigit():
            return State2D1()
        return StateStart()


class State2D1(State):
    def make_transition(self, _input: str) -> State:
        if _input.isdigit():
            return State2D2()
        if _input == ')':
            return StateRB()
        return StateStart()

    def make_action(self, _input: str, fsm: FSM) -> None:
        fsm.push_y(_input)


class State2D2(State):
    def make_transition(self, _input: str) -> State:
        if _input.isdigit():
            return State2D3()
        if _input == ')':
            return StateRB()
        return StateStart()

    def make_action(self, _input: str, fsm: FSM) -> None:
        fsm.push_y(_input)


class State2D3(State):
    def make_transition(self, _input: str) -> State:
        if _input == ')':
            return StateRB()
        return StateStart()

    def make_action(self, _input: str, fsm: FSM) -> None:
        fsm.push_y(_input)


class StateRB(State):
    def make_action(self, _input: str, fsm: FSM) -> None:
        fsm.multiply()
        # This is the final state. After action is performed, the state of the FSM must be reset and its state restored
        fsm.reset()
        fsm.state = StateStart()


class FSM:
    def __init__(self, initial_state: State, verbose: bool = False) -> None:
        self.state = initial_state

        self.x_buffer = None
        self.y_buffer = None
        self.total = 0

        self.__verbose = verbose

    def push_x(self, _input: str) -> None:
        if not self.x_buffer:
            self.x_buffer = _input
        else:
            self.x_buffer += _input

    def push_y(self, _input: str) -> None:
        if not self.y_buffer:
            self.y_buffer = _input
        else:
            self.y_buffer += _input

    def multiply(self) -> None:
        if self.__verbose:
            print(f'multiplying: {self.x_buffer}, {self.y_buffer}')
        self.total += int(self.x_buffer) * int(self.y_buffer)

    def reset(self) -> None:
        self.x_buffer = None
        self.y_buffer = None

    def step(self, _input: str) -> None:
        # if self.__verbose:
        #     print(f'State: {self.state}, input: {_input}')
        self.state = self.state.make_transition(_input)
        self.state.make_action(_input, self)


if __name__ == "__main__":
    path = "input.txt"

    with open(path, "r") as f:
        data = f.read()

    fsm = FSM(StateStart(), verbose=False)

    for char in data:
        fsm.step(char)

    print(fsm.total)
