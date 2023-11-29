import pygame


AMOUNT_OF_PLAYERS = 3

# Units
warrior = pygame.transform.scale(pygame.image.load("warrior.png"), (60, 60))
archer = pygame.transform.scale(pygame.image.load("archer.png"), (60, 60))
swordsman = pygame.transform.scale(pygame.image.load("swordsman.png"), (60, 60))
slinger = pygame.transform.scale(pygame.image.load("slinger.png"), (60, 60))
chariot = pygame.transform.scale(pygame.image.load("chariot.png"), (60, 60))


def generate_different_colors(img_path: str, num: int):
    """
    Generates units of different colors
    :param img_path:
    :param num:
    :return:
    """
    colors = [(100, 100, 200, 255), (200, 50, 50, 255), (200, 50, 200, 255)]
    # Blue, Red, Purple

    def change_color(image_path: str, color: (int, int, int, int)):
        img = pygame.transform.scale(pygame.image.load(image_path), (60, 60))
        for x in range(img.get_width()):
            for y in range(img.get_height()):
                pixel_color = img.get_at((x, y))
                if pixel_color == (0, 0, 0, 255):  # Check if the pixel is black
                    img.set_at((x, y), color)  # Change to blue
        return img

    colored = [change_color(img_path, colors[i]) for i in range(num)]
    return colored


images_warrior = generate_different_colors("warrior.png", 3)
images_archer = generate_different_colors("archer.png", 3)
images_swordsman = generate_different_colors("swordsman.png", 3)
images_chariot = generate_different_colors("chariot.png", 3)
images_slinger = generate_different_colors("slinger.png", 3)


unit_stats = {"warrior": {"strength_melee": 20, "strength_ranged": 0, "range": 0, "movement": 2, "images": images_warrior},
              "archer": {"strength_melee": 15, "strength_ranged": 25, "range": 2, "movement": 2, "images": images_archer},
              "chariot": {"strength_melee": 28, "strength_ranged": 0, "range": 0, "movement": 3, "images": images_chariot},
              "swordsman": {"strength_melee": 35, "strength_ranged": 0, "range": 0, "movement": 2, "images": images_swordsman},
              "slinger": {"strength_melee": 5, "strength_ranged": 15, "range": 1, "movement": 2, "images": images_slinger},}


class Unit:
    def __init__(self, name, location, team):
        self.type = name
        self.health = 100
        self.strength = unit_stats[name]["strength_melee"]
        self.ranged_strength = unit_stats[name]["strength_ranged"]
        self.range = unit_stats[name]["range"]
        self.movement_max = unit_stats[name]["movement"]
        self.movement_left = self.movement_max
        self.location = location
        self.image = unit_stats[name]["images"][team-1]
        self.fortified = False
        self.team = team


def create_unit(name, location, team):
    return Unit(name, location, team)
