from __future__ import annotations

direction_map = {
    '^': (-1, 0),
    'v': (1, 0),
    '<': (0, -1),
    '>': (0, 1)
}


class Warehouse:
    def __init__(self, grid_shape: tuple, robot: Robot, walls: list[Wall], boxes: list[Box]) -> None:
        self.grid_shape = grid_shape

        self.robot = robot
        self.walls = walls
        self.boxes = boxes

    @classmethod
    def from_str(cls, warehouse_map: str) -> Warehouse:
        warehouse_map = [list(l.strip()) for l in warehouse_map.split('\n')]

        n_rows = len(warehouse_map)
        n_cols = len(warehouse_map[0])
        grid_shape = (n_rows, n_cols)

        robot = None
        walls = []
        boxes = []
        for r, row in enumerate(warehouse_map):
            for c, value in enumerate(row):
                if value == '@':
                    robot = Robot((r, c))
                elif value == '[':
                    boxes.append(Box((r, c)))
                elif value == '#':
                    walls.append(Wall((r, c)))

        return cls(grid_shape, robot, walls, boxes)

    def print(self) -> None:
        grid_as_characters = [['.' for _ in range(self.grid_shape[0])] for _ in range(len(self.grid_shape[1]))]

        self.robot.update_str_map(grid_as_characters)
        for wall in self.walls:
            wall.update_str_map(grid_as_characters)
        for box in self.boxes:
            box.update_str_map(grid_as_characters)

        print('--------')
        for line in grid_as_characters:
            print(''.join(line))
        print('--------')

    def move_robot(self, direction: str) -> None:
        if self.robot.can_move(direction, self):
            self.robot.move(direction, self)

    def get_object_at(self, position: tuple) -> WarehouseObject | None:
        if self.robot.is_at(position):
            return self.robot
        for wall in self.walls:
            if wall.is_at(position):
                return wall
        for box in self.boxes:
            if box.is_at(position):
                return box
        return None

    def sum_box_coords(self) -> int:
        total_sum = 0
        for box in self.boxes:
            total_sum += box.coord_value
        return total_sum


class WarehouseObject:
    character = 'X'

    def __init__(self, position: tuple[int, int]) -> None:
        self.position = position

    def can_move(self, direction: str, environment: Warehouse) -> bool:
        neighbours = self.get_neighbours(direction, environment)

        if not neighbours:
            return True
        return all(n.can_move(direction, environment) for n in neighbours)

    def move(self, direction: str, environment: Warehouse) -> None:
        neighbours = self.get_neighbours(direction, environment)

        for n in neighbours:
            n.move(direction, environment)

        direction_vector = direction_map[direction]
        self.position = self.position[0] + direction_vector[0], self.position[1] + direction_vector[1]

    def get_neighbours(self, direction: str, environment: Warehouse) -> list[WarehouseObject]:
        direction_vector = direction_map[direction]
        neighbouring_position = self.position[0] + direction_vector[0], self.position[1] + direction_vector[1]
        neighbour = environment.get_object_at(neighbouring_position)
        return [neighbour] if neighbour else []

    def is_at(self, position: tuple) -> bool:
        return self.position == position

    def update_str_map(self, grid_as_characters: list[list[str]]) -> None:
        grid_as_characters[self.position[0]][self.position[1]] = self.character


class Robot(WarehouseObject):
    character = '@'


class Wall(WarehouseObject):
    character = '#'

    def can_move(self, direction: str, environment: Warehouse) -> bool:
        return False

    def move(self, direction: str, environment: Warehouse) -> None:
        raise RuntimeError('Trying to move a wall')


class Box(WarehouseObject):
    character = '['
    character_end = ']'

    def __init__(self, position: tuple[int, int]) -> None:
        self.positions = [position, (position[0], position[1] + 1)]
        super().__init__(self.positions[0])

    def update_str_map(self, grid_as_characters: list[list[str]]) -> None:
        grid_as_characters[self.positions[0][0]][self.positions[0][1]] = self.character
        grid_as_characters[self.positions[1][0]][self.positions[1][1]] = self.character_end

    def move(self, direction: str, environment: Warehouse) -> None:
        neighbours = self.get_neighbours(direction, environment)

        for n in neighbours:
            n.move(direction, environment)

        direction_vector = direction_map[direction]
        self.positions[0] = self.positions[0][0] + direction_vector[0], self.positions[0][1] + direction_vector[1]
        self.positions[1] = self.positions[1][0] + direction_vector[0], self.positions[1][1] + direction_vector[1]

        self.position = self.positions[0]

    def get_neighbours(self, direction: str, environment: Warehouse) -> list[WarehouseObject]:
        direction_vector = direction_map[direction]

        if direction == '<':
            neighbouring_position = (self.positions[0][0] + direction_vector[0],
                                     self.positions[0][1] + direction_vector[1])

            neighbour = environment.get_object_at(neighbouring_position)
            return [neighbour] if neighbour else []
        if direction == '>':
            neighbouring_position = (self.positions[1][0] + direction_vector[0],
                                     self.positions[1][1] + direction_vector[1])
            neighbour = environment.get_object_at(neighbouring_position)
            return [neighbour] if neighbour else []

        neighbouring_position_1 = (self.positions[0][0] + direction_vector[0],
                                   self.positions[0][1] + direction_vector[1])
        neighbouring_position_2 = (self.positions[1][0] + direction_vector[0],
                                   self.positions[1][1] + direction_vector[1])
        neighbour_1 = environment.get_object_at(neighbouring_position_1)
        neighbour_2 = environment.get_object_at(neighbouring_position_2)

        neighbours = [n for n in {neighbour_1, neighbour_2} if n is not None]
        return neighbours

    def is_at(self, position: tuple) -> bool:
        return self.positions[0] == position or self.positions[1] == position

    @property
    def coord_value(self) -> int:
        return 100 * self.position[0] + self.position[1]


if __name__ == '__main__':
    path = 'input.txt'

    with open(path, 'r') as f:
        data = f.read()

    grid, moves = data.split('\n\n')
    moves = moves.strip().replace('\n', '')

    grid = grid.replace('#', '##', ).replace('O', '[]').replace('.', '..').replace('@', '@.')

    warehouse = Warehouse.from_str(grid)

    for move in moves:
        warehouse.move_robot(move)

    # Part 2
    print(warehouse.sum_box_coords())
