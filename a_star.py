import pygame
import sys
import numpy as np

# options
CELL_WIDTH = 16
CELL_HEIGHT = 16
MENU_WIDTH = 250


class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0.0
        self.h = 0.0
        self.f = 0.0

    def __eq__(self, other):
        return self.position == other.position


class PathFinder:
    def __init__(self, matrix, win):
        self.matrix = matrix
        self.win = win

    def create_path(self, start, end):
        self.start = start
        self.end = end
        start_node = Node(None, start)
        end_node = Node(None, end)
        open_list = []
        closed_list = []

        open_list.append(start_node)

        while len(open_list) > 0:
            current_node = min(open_list, key=lambda node: node.f)
            current_index = open_list.index(current_node)

            open_list.pop(current_index)
            closed_list.append(current_node)
            self.visualize_lists(open_list, closed_list)

            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    self.visualize_path(path)
                    current = current.parent
                return path[::-1]

            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                node_position = (
                    current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                if node_position[0] > (len(self.matrix) - 1) or node_position[0] < 0 or node_position[1] > (len(self.matrix[0]) - 1) or node_position[1] < 0:
                    continue

                if self.matrix[node_position[0]][node_position[1]] != 1:
                    continue

                if node_position in [node.position for node in closed_list]:
                    continue

                new_node = Node(current_node, node_position)
                new_node.g = new_node.parent.g + np.sqrt(((new_node.position[0] - new_node.parent.position[0])**2) + (
                    (new_node.position[1] - new_node.parent.position[1]))**2)
                new_node.h = np.sqrt(((new_node.position[0] - end_node.position[0]) ** 2) + (
                    (new_node.position[1] - end_node.position[1]) ** 2))

                new_node.f = new_node.g + new_node.h

                if new_node.position not in [node.position for node in open_list]:
                    open_list.append(new_node)
                    self.visualize_lists(open_list, closed_list)
                else:
                    node_in = [
                        node for node in open_list if node.position == new_node.position]
                    if node_in[0].f > new_node.f:
                        open_list.remove(node_in[0])
                        open_list.append(new_node)
                        self.visualize_lists(open_list, closed_list)

    def visualize_path(self, path):
        if path:
            color = (255, 80, 255)
            for path in path[1:-1]:
                x_pos = MENU_WIDTH + path[1] * CELL_WIDTH + 1
                y_pos = path[0] * CELL_HEIGHT + 1

                pygame.draw.rect(self.win, color, (x_pos, y_pos,
                                 CELL_WIDTH - 2, CELL_HEIGHT - 2))

            pygame.display.update()
            pygame.time.delay(100)

    def visualize_lists(self, open_list, closed_list):
        if open_list:
            color = (0, 120, 255)
            for item in open_list:
                if item.position != self.start and item.position != self.end:
                    x_pos = MENU_WIDTH + item.position[1] * CELL_WIDTH + 1
                    y_pos = item.position[0] * CELL_HEIGHT + 1

                    pygame.draw.rect(
                        self.win, color, (x_pos, y_pos, CELL_WIDTH - 2, CELL_HEIGHT - 2))

        if closed_list:
            color = (0, 255, 50)
            for item in closed_list:
                if item.position != self.start and item.position != self.end:
                    x_pos = MENU_WIDTH + item.position[1] * CELL_WIDTH + 1
                    y_pos = item.position[0] * CELL_HEIGHT + 1

                    pygame.draw.rect(
                        self.win, color, (x_pos, y_pos, CELL_WIDTH - 2, CELL_HEIGHT - 2))

        pygame.display.update()
        # pygame.time.delay(100)


class Game:
    def __init__(self):
        # game options
        self.rows = 40
        self.cols = 40

        self.matrix = np.ones((self.rows, self.cols), dtype=int)

        # win dimensions
        self.WIDTH = MENU_WIDTH + CELL_WIDTH * self.cols
        self.HEIGHT = CELL_HEIGHT * self.rows

        # buttons dimensions
        self.buttons_x = 25
        self.button_width = MENU_WIDTH - 2 * self.buttons_x
        self.button_height = 60
        self.first_button_y = 25
        self.button_space = self.HEIGHT // 6

        self.set_start = False
        self.set_end = False
        self.set_walls = False
        self.del_walls = False
        self.set_search = False

        self.start = None
        self.end = None
        self.walls = []
        self.path = []

    def reset(self):
        self.matrix = np.ones((self.rows, self.cols), dtype=int)

        self.set_start = False
        self.set_end = False
        self.set_walls = False
        self.del_walls = False
        self.set_search = False

        self.start = None
        self.end = None
        self.walls = []
        self.path = []

    # DRAWING
    def draw_items(self, win):
        win.fill((0, 200, 150))
        self.draw_buttons(win)
        self.draw_board(win)
        self.draw_start(win)
        self.draw_end(win)
        self.draw_walls(win)
        self.draw_path(win)

    def draw_buttons(self, win):

        self.draw_button(win, self.first_button_y, self.set_start, 'START')
        self.draw_button(win, self.first_button_y +
                         self.button_space, self.set_end, 'END')
        self.draw_button(win, self.first_button_y + 2 * self.button_space,
                         self.set_walls, 'DRAW WALLS')
        self.draw_button(win, self.first_button_y + 3 * self.button_space,
                         self.del_walls, 'ERASE WALLS')
        self.draw_button(win, self.first_button_y + 4 * self.button_space,
                         self.set_search, 'SEARCH')
        self.draw_button(win, self.first_button_y + 5 * self.button_space,
                         self.set_search, 'RESET')

    def draw_button(self, win, y_pos, cond, text):
        color = (120, 120, 120)
        bg_color = (0, 0, 0)

        fnt = pygame.font.SysFont('comicsans', 25)

        if cond:
            color = (60, 60, 60)

        pygame.draw.rect(
            win, bg_color, (self.buttons_x, y_pos, self.button_width, self.button_height))
        pygame.draw.rect(
            win, color, (self.buttons_x + 1, y_pos + 1, self.button_width - 2, self.button_height - 2))

        text = fnt.render(text, True, bg_color)
        text_x = self.buttons_x + (self.button_width - text.get_width()) // 2
        text_y = y_pos + (self.button_height - text.get_height()) // 2
        win.blit(text, (text_x, text_y))

    def draw_board(self, win):
        color = (120, 120, 120)
        bg_color = (0, 0, 0)

        pygame.draw.rect(win, bg_color, (MENU_WIDTH, 0,
                         CELL_WIDTH*self.cols, CELL_HEIGHT * self.rows))

        for row in range(self.rows):
            for col in range(self.cols):
                x_pos = MENU_WIDTH + col * CELL_WIDTH + 1
                y_pos = row * CELL_HEIGHT + 1

                pygame.draw.rect(
                    win, color, (x_pos, y_pos, CELL_WIDTH - 2, CELL_HEIGHT - 2))

    def draw_start(self, win):
        if self.start:
            color = (0, 0, 255)
            x_pos = MENU_WIDTH + self.start[1] * CELL_WIDTH + 1
            y_pos = self.start[0] * CELL_HEIGHT + 1

            pygame.draw.rect(
                win, color, (x_pos, y_pos, CELL_WIDTH - 2, CELL_HEIGHT - 2))

    def draw_end(self, win):
        if self.end:
            color = (200, 0, 0)
            x_pos = MENU_WIDTH + self.end[1] * CELL_WIDTH + 1
            y_pos = self.end[0] * CELL_HEIGHT + 1

            pygame.draw.rect(
                win, color, (x_pos, y_pos, CELL_WIDTH - 2, CELL_HEIGHT - 2))

    def draw_walls(self, win):
        if self.walls:
            color = (255, 255, 80)
            for wall in self.walls:
                x_pos = MENU_WIDTH + wall[1] * CELL_WIDTH + 1
                y_pos = wall[0] * CELL_HEIGHT + 1

                pygame.draw.rect(
                    win, color, (x_pos, y_pos, CELL_WIDTH - 2, CELL_HEIGHT - 2))

    def draw_path(self, win):
        if self.path:
            color = (255, 80, 255)
            for path in self.path[1:-1]:
                x_pos = MENU_WIDTH + path[1] * CELL_WIDTH + 1
                y_pos = path[0] * CELL_HEIGHT + 1

                pygame.draw.rect(
                    win, color, (x_pos, y_pos, CELL_WIDTH - 2, CELL_HEIGHT - 2))

    def draw_message(self, win, text):
        fnt = pygame.font.SysFont('comicsans', 30)
        text = fnt.render(text, True, (255, 255, 255))
        text_x = self.WIDTH // 2
        text_y = (self.HEIGHT - text.get_height()) // 2
        win.blit(text, (text_x, text_y))

        pygame.display.update()
        pygame.time.delay(1500)

    # ACTION
    def play(self):
        # pygame setup
        pygame.init()
        win = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Path Finder')
        clock = pygame.time.Clock()
        clicked = False

        while True:
            mouse_pos = pygame.mouse.get_pos()
            row = mouse_pos[1] // CELL_HEIGHT
            col = (mouse_pos[0] - MENU_WIDTH) // CELL_WIDTH
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    clicked = True
                    if (self.buttons_x <= mouse_pos[0] <= self.buttons_x + self.button_width):
                        if (self.first_button_y <= mouse_pos[1] <= self.first_button_y + self.button_height):
                            self.set_start = not(self.set_start)
                            self.set_end = False
                            self.set_walls = False
                            self.del_walls = False
                            self.path = []
                        elif (self.first_button_y + self.button_space <= mouse_pos[1] <= self.first_button_y + self.button_space + self.button_height):
                            self.set_end = not(self.set_end)
                            self.set_start = False
                            self.set_walls = False
                            self.del_walls = False
                            self.path = []
                        elif (self.first_button_y + 2 * self.button_space <= mouse_pos[1] <= self.first_button_y + 2 * self.button_space + self.button_height):
                            self.set_walls = not(self.set_walls)
                            self.set_start = False
                            self.set_end = False
                            self.del_walls = False
                            self.path = []
                        elif (self.first_button_y + 3 * self.button_space <= mouse_pos[1] <= self.first_button_y + 3 * self.button_space + self.button_height):
                            self.del_walls = not(self.del_walls)
                            self.set_start = False
                            self.set_end = False
                            self.set_walls = False
                            self.path = []
                        elif (self.first_button_y + 4 * self.button_space <= mouse_pos[1] <= self.first_button_y + 4 * self.button_space + self.button_height):
                            self.set_start = False
                            self.set_end = False
                            self.set_walls = False
                            self.del_walls = False
                            if self.start:
                                if self.end:
                                    pathfinder = PathFinder(self.matrix, win)
                                    self.path = pathfinder.create_path(
                                        self.start, self.end)
                                    if not self.path:
                                        self.draw_message(
                                            win, 'THERE IS NO WAY THERE')
                                else:
                                    self.draw_message(win, 'END POINT MISSING')
                            else:
                                self.draw_message(win, 'START POINT MISSING')

                        elif (self.first_button_y + 5 * self.button_space <= mouse_pos[1] <= self.first_button_y + 5 * self.button_space + self.button_height):
                            self.reset()

                    elif (self.set_start) and (mouse_pos[0] >= MENU_WIDTH) and ((row, col) != self.end) and ((row, col) not in self.walls):
                        if self.start == (row, col):
                            self.start = None
                            self.set_start = False
                        else:
                            self.start = (row, col)
                            self.set_start = False
                    elif (self.set_end) and (mouse_pos[0] >= MENU_WIDTH) and ((row, col) != self.start) and ((row, col) not in self.walls):
                        if self.end == (row, col):
                            self.end = None
                            self.set_end = False
                        else:
                            self.end = (row, col)
                            self.set_end = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    clicked = False

            if self.set_walls and mouse_pos[0] >= MENU_WIDTH and ((row, col) != self.start) and ((row, col) != self.end) and clicked:
                if (row, col) not in self.walls:
                    self.walls.append((row, col))
                    self.matrix[row][col] = 0
            elif self.del_walls and mouse_pos[0] >= MENU_WIDTH and ((row, col) != self.start) and ((row, col) != self.end) and clicked:
                if (row, col) in self.walls:
                    self.walls.remove((row, col))
                    self.matrix[row][col] = 1

            self.draw_items(win)
            pygame.display.update()
            clock.tick(60)


if __name__ == '__main__':
    game = Game()
    game.play()
