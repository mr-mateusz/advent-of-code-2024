from __future__ import annotations

CHECK_DO_INSTRUCTION = False


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
        if CHECK_DO_INSTRUCTION:
            if _input == 'd':
                return StateD()
        return StateStart()

    def make_action(self, _input: str, fsm: FSM) -> None:
        fsm.reset()
        # Start State needs to make the transition immediately:
        fsm.state = self.make_transition(_input)


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
    # Final State
    def make_action(self, _input: str, fsm: FSM) -> None:
        fsm.multiply()


class StateD(State):
    def make_transition(self, _input: str) -> State:
        if _input == 'o':
            return StateDO()
        return StateStart()


class StateDO(State):
    def make_transition(self, _input: str) -> State:
        if _input == '(':
            return StateDOLB()
        if _input == 'n':
            return StateDON()
        return StateStart()


class StateDOLB(State):
    def make_transition(self, _input: str) -> State:
        if _input == ')':
            return StateDORB()
        return StateStart()


class StateDORB(State):
    # Final state
    def make_action(self, _input: str, fsm: FSM) -> None:
        fsm.enable()


class StateDON(State):
    def make_transition(self, _input: str) -> State:
        if _input == '\'':
            return StateDONa()
        return StateStart()


class StateDONa(State):
    def make_transition(self, _input: str) -> State:
        if _input == 't':
            return StateDONaT()
        return StateStart()


class StateDONaT(State):
    def make_transition(self, _input: str) -> State:
        if _input == '(':
            return StateDONaTLB()
        return StateStart()


class StateDONaTLB(State):
    def make_transition(self, _input: str) -> State:
        if _input == ')':
            return StateDONaTRB()
        return StateStart()


class StateDONaTRB(State):
    # Final State
    def make_action(self, _input: str, fsm: FSM) -> None:
        fsm.disable()


class FSM:
    def __init__(self, initial_state: State, is_enabled: bool = True, verbosity_level: int = 0) -> None:
        self.state = initial_state

        self.is_enabled = is_enabled
        self.x_buffer = None
        self.y_buffer = None
        self.total = 0

        self.__verbosity_level = verbosity_level

    def enable(self) -> None:
        self.is_enabled = True

    def disable(self) -> None:
        self.is_enabled = False

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
        if self.is_enabled:
            if self.__verbosity_level:
                print(f'multiplying: {self.x_buffer}, {self.y_buffer}')
            self.total += int(self.x_buffer) * int(self.y_buffer)
        else:
            if self.__verbosity_level:
                print(f'not multiplying (disabled): {self.x_buffer}, {self.y_buffer}')

    def reset(self) -> None:
        self.x_buffer = None
        self.y_buffer = None

    def step(self, _input: str) -> None:
        if self.__verbosity_level >= 2:
            print(f'State: {self.state}, input: {_input}')
        self.state = self.state.make_transition(_input)
        self.state.make_action(_input, self)


if __name__ == "__main__":
    path = "input.txt"

    with open(path, "r") as f:
        data = f.read()

    fsm = FSM(StateStart(), verbosity_level=0)

    for char in data:
        fsm.step(char)

    # Part 1
    print(fsm.total)

    CHECK_DO_INSTRUCTION = True

    fsm = FSM(StateStart(), verbosity_level=0)

    for char in data:
        fsm.step(char)

    # Part 2
    print(fsm.total)
