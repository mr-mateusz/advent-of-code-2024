from __future__ import annotations

from typing import Mapping


class Instruction:

    @property
    def has_combo_operand(self) -> bool:
        raise NotImplementedError

    def execute(self, operand: int, computer: Computer):
        operand = self.get_operand_value(operand, computer)
        self._execute(operand, computer)
        self.move_pointer(computer)

    def _execute(self, resolved_operand: int, computer: Computer):
        raise NotImplementedError()

    def get_operand_value(self, operand: int, computer: Computer) -> int:
        if not self.has_combo_operand:
            return operand
        return self._get_combo_operand_value(operand, computer)

    def _get_combo_operand_value(self, operand: int, computer: Computer) -> int:
        if operand <= 3:
            return operand
        if operand == 4:
            return computer.register_a
        if operand == 5:
            return computer.register_b
        if operand == 6:
            return computer.register_c
        raise ValueError('Combo operand cannot be > 6')

    def move_pointer(self, computer: Computer) -> None:
        computer.pointer += 2


class Adv(Instruction):

    @property
    def has_combo_operand(self) -> bool:
        return True

    def _execute(self, resolved_operand: int, computer: Computer):
        numerator = computer.register_a
        denominator = 2 ** resolved_operand
        result = numerator // denominator
        computer.register_a = result


class Bxl(Instruction):

    @property
    def has_combo_operand(self) -> bool:
        return False

    def _execute(self, resolved_operand: int, computer: Computer):
        computer.register_b = computer.register_b ^ resolved_operand


class Bst(Instruction):

    @property
    def has_combo_operand(self) -> bool:
        return True

    def _execute(self, resolved_operand: int, computer: Computer):
        computer.register_b = resolved_operand % 8


class Jnz(Instruction):

    def __init__(self):
        self.move_pointer_to = None

    @property
    def has_combo_operand(self) -> bool:
        return False

    def _execute(self, resolved_operand: int, computer: Computer):
        if computer.register_a == 0:
            return
        self.move_pointer_to = resolved_operand

    def move_pointer(self, computer: Computer) -> None:
        if self.move_pointer_to is not None:
            computer.pointer = self.move_pointer_to
            self.move_pointer_to = None
        else:
            super().move_pointer(computer)


class Bxc(Instruction):

    @property
    def has_combo_operand(self) -> bool:
        return False

    def _execute(self, resolved_operand: int, computer: Computer):
        computer.register_b = computer.register_b ^ computer.register_c


class Out(Instruction):

    @property
    def has_combo_operand(self) -> bool:
        return True

    def _execute(self, resolved_operand: int, computer: Computer):
        computer.stdout.append(resolved_operand % 8)


class Bdv(Instruction):

    @property
    def has_combo_operand(self) -> bool:
        return True

    def _execute(self, resolved_operand: int, computer: Computer):
        numerator = computer.register_a
        denominator = 2 ** resolved_operand
        result = numerator // denominator
        computer.register_b = result


class Cdv(Instruction):

    @property
    def has_combo_operand(self) -> bool:
        return True

    def _execute(self, resolved_operand: int, computer: Computer):
        numerator = computer.register_a
        denominator = 2 ** resolved_operand
        result = numerator // denominator
        computer.register_c = result


class Computer:
    def __init__(self, register_states: list[int], instructions: list[int],
                 instruction_map: Mapping[int, Instruction]) -> None:
        self.register_a = register_states[0]
        self.register_b = register_states[1]
        self.register_c = register_states[2]

        self.instructions = instructions

        self.instruction_map = instruction_map

        self.pointer = 0

        self.stdout = []

    def interpret(self) -> bool:
        try:
            opcode = self.instructions[self.pointer]
            operand = self.instructions[self.pointer + 1]
        except IndexError:
            return False

        self.instruction_map[opcode].execute(operand, self)
        return True


if __name__ == '__main__':
    path = 'input.txt'

    with open(path, 'r') as f:
        data = f.read()

    register_states, instructions = data.split('\n\n')

    register_states = [int(l.split()[-1]) for l in register_states.split('\n')]
    instructions = [int(i) for i in instructions.replace('Program: ', '').strip().split(',')]

    instruction_mapping = {index: instr for index, instr in enumerate([Adv(), Bxl(), Bst(), Jnz(),
                                                                       Bxc(), Out(), Bdv(), Cdv()])}

    computer = Computer(register_states, instructions, instruction_mapping)

    while True:
        instruction_performed = computer.interpret()
        if not instruction_performed:
            break

    # Part 1
    print(','.join(str(val) for val in computer.stdout))
