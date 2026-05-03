import pygame
import random
import sys

pygame.init()

# Define using square dimensions based on the height
DIMENSION = 720
START_X = 50
START_Y = 150
BLOCK_DIM = 60

COLOR_BG = (235, 235, 235)
COLOR_W = (245, 222, 179)
COLOR_B = (139, 69, 19)
COLOR_Q = (219, 112, 147)
COLOR_TXT = (50, 50, 50)

FONT_STYLE = pygame.font.SysFont("monospace", 22)

class ExecutionUnit:
    def __init__(self, capacity, display_surface):
        self.capacity = capacity
        self.display_surface = display_surface
        self.matrix = [random.randint(0, self.capacity - 1) for _ in range(self.capacity)]

    def measure_clashes(self, current_array):
        # Calculates how many pairs of queens are attacking each other
        penalty = 0
        for m in range(self.capacity):
            for n in range(m + 1, self.capacity):
                if current_array[m] == current_array[n] or abs(current_array[m] - current_array[n]) == abs(m - n):
                    penalty += 1
        return penalty

    def build_variants(self, current_array):
        # Generates all possible neighbor states by moving one queen
        collection = []
        for index in range(self.capacity):
            original = current_array[index]
            for step in range(self.capacity):
                if step != original:
                    mutated = list(current_array)
                    mutated[index] = step
                    collection.append((mutated, self.measure_clashes(mutated)))
        return collection

    def pick_optimal(self, variants):
        # Selects the best neighbor with the lowest clashes
        if not variants:
            return None, None
        variants.sort(key=lambda item: item[1])
        lowest = variants[0][1]
        matches = [x for x in variants if x[1] == lowest]
        selection = random.choice(matches)
        return selection[0], selection[1]

    def process(self):
        # Executes the hill-climbing optimization algorithm
        active_state = list(self.matrix)
        active_clashes = self.measure_clashes(active_state)
        counter = 0

        while active_clashes > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.redraw(active_state, active_clashes, counter)
            pygame.time.delay(150)

            possible_states = self.build_variants(active_state)
            best_state, best_clashes = self.pick_optimal(possible_states)

            # Restarts with a random state if stuck in local minimum
            if best_clashes >= active_clashes:
                active_state = [random.randint(0, self.capacity - 1) for _ in range(self.capacity)]
                active_clashes = self.measure_clashes(active_state)
                continue

            active_state = best_state
            active_clashes = best_clashes
            counter += 1

        self.redraw(active_state, active_clashes, counter, finished=True)
        self.matrix = active_state
        return active_state

    def redraw(self, state, penalty, iteration, finished=False):
        # Renders the board layout and queen positions
        self.display_surface.fill(COLOR_BG)

        for row_idx in range(self.capacity):
            for col_idx in range(self.capacity):
                cell_color = COLOR_W if (row_idx + col_idx) % 2 == 0 else COLOR_B
                pygame.draw.rect(
                    self.display_surface,
                    cell_color,
                    (START_X + col_idx * BLOCK_DIM, START_Y + row_idx * BLOCK_DIM, BLOCK_DIM, BLOCK_DIM)
                )

        for col_idx, row_idx in enumerate(state):
            c_x = int(START_X + col_idx * BLOCK_DIM + BLOCK_DIM // 2)
            c_y = int(START_Y + row_idx * BLOCK_DIM + BLOCK_DIM // 2)
            rad = int(BLOCK_DIM * 0.38)
            pygame.draw.circle(self.display_surface, COLOR_Q, (c_x, c_y), rad)

        text_one = FONT_STYLE.render(f"Clashes: {penalty}", True, COLOR_TXT)
        text_two = FONT_STYLE.render(f"Cycles: {iteration}", True, COLOR_TXT)
        self.display_surface.blit(text_one, (50, 30))
        self.display_surface.blit(text_two, (400, 30))

        if finished:
            text_end = FONT_STYLE.render("Target Configuration Reached!", True, (34, 139, 34))
            self.display_surface.blit(text_end, (50, DIMENSION - 60))

        pygame.display.flip()

def main():
    display = pygame.display.set_mode((DIMENSION, DIMENSION))
    pygame.display.set_caption("N-Queens System Optimizer")
    
    unit = ExecutionUnit(8, display)
    unit.process()
    
    alive = True
    while alive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                alive = False
                pygame.quit()
                sys.exit()

if __name__ == '__main__':
    main()