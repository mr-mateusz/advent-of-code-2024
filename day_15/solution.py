from __future__ import annotations

direction_map = {
    '^': (-1, 0),
    'v': (1, 0),
    '<': (0, -1),
    '>': (0, 1)
}


class Warehouse:
    def __init__(self, grid: list[list[str]]) -> None:
        self.grid = grid

        self.robot_pos = None
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] == '@':
                    self.robot_pos = (i, j)

        if not self.robot_pos:
            raise AttributeError('Incorrect input')

    @classmethod
    def from_str(cls, input: str) -> Warehouse:
        input = [list(l.strip()) for l in input.split('\n')]
        return cls(input)

    def print(self):
        print('--------')
        for l in self.grid:
            print(''.join(l))
        print('--------')

    def find_objects_to_move(self, direction: str) -> list[tuple]:
        """Returned structure should be interpreted as a stack and objects should be moved from the end."""
        direction_vector = direction_map[direction]

        to_move_stack = [self.robot_pos]
        next_pos = self.robot_pos[0] + direction_vector[0], self.robot_pos[1] + direction_vector[1]
        while True:
            if self.grid[next_pos[0]][next_pos[1]] == 'O':
                to_move_stack.append(next_pos)
            if self.grid[next_pos[0]][next_pos[1]] == '.':
                to_move_stack.append(next_pos)
                return to_move_stack
            if self.grid[next_pos[0]][next_pos[1]] == '#':
                return []
            next_pos = next_pos[0] + direction_vector[0], next_pos[1] + direction_vector[1]

    def swap(self, first: tuple, second: tuple) -> None:
        self.grid[first[0]][first[1]], self.grid[second[0]][second[1]] = \
            self.grid[second[0]][second[1]], self.grid[first[0]][first[1]]

    def move_robot(self, direction: str) -> None:
        to_move_stack = self.find_objects_to_move(direction)

        if not to_move_stack:
            return
        if len(to_move_stack) == 1:
            raise AttributeError('Something is not right in find_objects_to_move')

        first = to_move_stack.pop()
        while to_move_stack:
            second = to_move_stack.pop()
            self.swap(first, second)
            _first = first
            first = second
        self.robot_pos = _first

    def sum_box_coords(self) -> int:
        total_sum = 0
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                if self.grid[r][c] == 'O':
                    total_sum += 100 * r + c
        return total_sum


if __name__ == '__main__':
    path = 'input.txt'

    with open(path, 'r') as f:
        data = f.read()

    grid, moves = data.split('\n\n')
    moves = moves.strip().replace('\n', '')

    warehouse = Warehouse.from_str(grid)

    for move in moves:
        warehouse.move_robot(move)

    # Part 1
    print(warehouse.sum_box_coords())
