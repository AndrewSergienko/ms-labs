import asyncio
import random
import pandas as pd


class Model:
    def __init__(self, grid, victims, predators, tacts):
        self.grid = grid
        self.victims = victims
        self.predators = predators
        self.victims_len_stat = []
        self.predators_len_stat = []
        self.tacts = tacts

    def update_stat(self):
        self.victims_len_stat.append(len(self.victims))
        self.predators_len_stat.append(len(self.predators))
        self.tacts -= 1

    def while_condition(self):
        print([len(self.victims), len(self.predators)])
        return len(self.victims) > 0 and len(self.predators) > 0 and self.tacts > 0


class Entity:
    VICTIM_REPRODUCTION_AGE = None
    VICTIM_REPRODUCTION_PERIOD = None

    PREDATOR_REPRODUCTION_AGE = None
    PREDATOR_REPRODUCTION_PERIOD = None
    PREDATOR_LIFETIME = None

    def __init__(self, entity_type, age=None):
        self.entity_type = entity_type
        self.age = random.randint(0, 10) if not age else age
        self.pos = []
        self.next_pos = []
        self.lifetime = Entity.PREDATOR_LIFETIME
        self.next_repr_time = Entity.VICTIM_REPRODUCTION_PERIOD if entity_type == "victim" else Entity.PREDATOR_REPRODUCTION_PERIOD

    def get_neighboring_cells(self, grid):
        return [
            {'pos': [self.pos[0] + 1, self.pos[1]], 'content': grid[self.pos[0] + 1][self.pos[1]] if self.pos[0] < len(grid)-1 else None},
            {'pos': [self.pos[0], self.pos[1] + 1], 'content': grid[self.pos[0]][self.pos[1] + 1] if self.pos[1] < len(grid[0])-1 else None},
            {'pos': [self.pos[0] - 1, self.pos[1]], 'content': grid[self.pos[0] - 1][self.pos[1]] if self.pos[0] > 0 else None},
            {'pos': [self.pos[0], self.pos[1] - 1], 'content': grid[self.pos[0]][self.pos[1] - 1] if self.pos[1] > 0 else None},
        ]

    def get_neighboring_empty_cells(self, neighboring_cells):
        available_cells = []
        for cell in neighboring_cells:
            if cell['content'] == "empty":
                available_cells.append(cell)
        return available_cells

    def get_neighboring_victim_cells(self, neighboring_cells):
        available_cells = []
        for cell in neighboring_cells:
            if type(cell['content']) == Entity and cell['content'].entity_type == "victim":
                available_cells.append(cell)
        return available_cells

    def set_next_pos(self, grid):
        neighboring_cells = self.get_neighboring_cells(grid)
        available_cells = []
        if self.entity_type == "victim":
            available_cells = self.get_neighboring_empty_cells(neighboring_cells)
        if self.entity_type == "predator":
            available_cells = self.get_neighboring_victim_cells(neighboring_cells)
            if len(available_cells) == 0:
                available_cells = self.get_neighboring_empty_cells(neighboring_cells)
        if len(available_cells) == 0:
            self.next_pos = None
        else:
            cell = random.choice(available_cells)
            self.next_pos = cell['pos']

    def repr(self, model):
        neighboring_cells = self.get_neighboring_cells(model.grid)
        neighboring_empty_cells = self.get_neighboring_empty_cells(neighboring_cells)
        if len(neighboring_empty_cells) > 0:
            new_entity = Entity(entity_type=self.entity_type, age=0)
            pos = random.choice(neighboring_empty_cells)['pos']
            model.grid[pos[0]][pos[1]] = new_entity
            new_entity.pos = [pos[0], pos[1]]
            if self.entity_type == "victim":
                model.victims.append(new_entity)
            else:
                model.predators.append(new_entity)
            self.next_repr_time = Entity.PREDATOR_REPRODUCTION_PERIOD


async def create_model(params):
    grid = [["empty" for _ in range(params['y'])] for _ in range(params['x'])]

    Entity.VICTIM_REPRODUCTION_AGE = params['victim_repr_age']
    Entity.VICTIM_REPRODUCTION_PERIOD = params['victim_repr_period']
    Entity.PREDATOR_REPRODUCTION_AGE = params['predator_repr_age']
    Entity.PREDATOR_REPRODUCTION_PERIOD = params['predator_repr_period']
    Entity.PREDATOR_LIFETIME = params['predator_lifetime']

    victims = [Entity('victim') for _ in range(params['victim_num'])]
    predators = [Entity('predator') for _ in range(params['predator_num'])]

    for entity in victims + predators:
        while True:
            coords = [random.randint(0, params['x']-1), random.randint(0, params['y']-1)]
            if grid[coords[0]][coords[1]] == "empty":
                grid[coords[0]][coords[1]] = entity
                entity.pos = [coords[0], coords[1]]
                break
    print('creating')

    return Model(grid=grid, victims=victims, predators=predators, tacts=params['tacts'])


async def start(model):
    while model.while_condition():
        for entity in model.predators + model.victims:
            entity.age += 1
            if (entity.entity_type == "predator" and entity.age >= Entity.PREDATOR_REPRODUCTION_AGE)\
                    or (entity.entity_type == "victim" and entity.age >= Entity.VICTIM_REPRODUCTION_AGE):
                entity.next_repr_time = entity.next_repr_time - 1 if entity.next_repr_time > 0 else 0

        for victim in model.victims:
            victim.set_next_pos(model.grid)
            if victim.next_pos:
                model.grid[victim.next_pos[0]][victim.next_pos[1]] = victim
                model.grid[victim.pos[0]][victim.pos[1]] = "empty"
                victim.pos = victim.next_pos

        for victim in model.victims:
            if victim.next_repr_time == 0:
                victim.repr(model)

        for predator in model.predators:
            predator.set_next_pos(model.grid)
            if predator.next_pos:
                next_pos_content = model.grid[predator.next_pos[0]][predator.next_pos[1]]
                if type(next_pos_content) == Entity and next_pos_content.entity_type == "victim":
                    predator.lifetime = Entity.PREDATOR_LIFETIME
                    model.victims.remove(next_pos_content)
                predator.lifetime -= 1
                if predator.lifetime < 0:
                    model.predators.remove(predator)
                    model.grid[predator.pos[0]][predator.pos[1]] = "empty"
                else:
                    model.grid[predator.next_pos[0]][predator.next_pos[1]] = predator
                    model.grid[predator.pos[0]][predator.pos[1]] = "empty"
                    predator.pos = predator.next_pos

        for predator in model.predators:
            if predator.next_repr_time == 0:
                predator.repr(model)
        model.update_stat()
    return pd.DataFrame(data={"predators": model.predators_len_stat, "victims": model.victims_len_stat})


# model = create_model({
#             'x': 100,
#             'y': 100,
#             'victim_num': 50,
#             'predator_num': 5,
#             'victim_repr_age': 3,
#             'victim_repr_period': 3,
#             'predator_repr_age': 3,
#             'predator_repr_period': 4,
#             'predator_lifetime': 3,
#             'tacts': 200
#         })
# start(model)