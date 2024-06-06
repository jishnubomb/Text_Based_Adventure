import sys
import random

class character():
    def __init__(self, name, health, hit, inventory, inventory_space, location):
        self.name = name
        self.health = health
        self.hit = hit
        self.inventory = inventory
        self.inventory_space = inventory_space
        self.location = location

class npc():
    def __init__(self, name, health, inventory, inventory_space, interactions):
        self.name = name
        self.health = health
        self.inventory = inventory
        self.inventory_space = inventory_space
        self.interactions = interactions

class chest():
    def __init__(self, name, key, inventory):
        self.name = name
        self.key = key
        self.inventory = inventory

class item():
    def __init__(self, name, effects, description):
        self.name = name
        self.effects = effects
        self.description = description

class enemy():
    def __init__(self, name, health, inventory, main_weapon, hit):
        self.name = name
        self.health = health
        self.inventory = inventory
        self.main_weapon = main_weapon
        self.hit = hit

class room:
    def __init__(self, description, NPCs, inventory, exits, enemies):
        self.description = description
        self.NPCs = NPCs
        self.inventory = inventory
        self.exits = exits
        self.enemies = enemies
        
class story:
    def __init__(self, story, actions):
        self.story = story
        self.actions = actions
        
def move(character, current_room, direction):
    if direction in current_room.exits.keys():
        return rooms[Player.location.exits[prompts[1]]-1], True
    else:
        if character == Player:
            print("That is not an option\nExits: {}"
                .format(str(Player.location.exits.keys())[11:-2]))
        return current_room, False

def view_chest(chest):
    print("Items: {}".format([item.name for item in chest.inventory]))
    choices = [0]
    while choices[0] != "exit":
        choices = input("What would you like to do? ").split()
        if len(choices) > 1:
            if choices[0] in ["grab", "get"]:
                pick_up(Player, [getattr(sys.modules[__name__], item, item)
                                     for item in choices[1:len(choices)]], chest)
            else:
                print("that is not an option")
    print("Chest closed")

def pick_up(user, items, chest):
    for item in items:
        if chest != "null":
            change_inventory(user, [item], chest)
        elif item in user.location.inventory:
            change_inventory(user, [item], Player.location)
        else:
            if user == Player:
                if type(item) == str:
                    print("{} is not in your room".format(item))
                else:
                    print("{} is not in your room".format(item.name))
         
def change_inventory(target, items, origin):
    if type(target) != type(room1):
        if len(target.inventory)+len(items) < target.inventory_space:
            for item in items:
                target.inventory.append(item)
                if origin != "null":
                    origin.inventory.remove(item)
                if target == Player:
                    print("{} added to inventory...".format(item.name))
        else:
            print("You do not have enough space in your inventory")
    else:
        for item in items:
            target.inventory.append(item)
            if target == Player:
                print("{} added to inventory...".format(item.name))
        if origin != "null":
            for item in items:
                origin.inventory.remove(item)


def use(user, target, item):
    if "damage" in item.effects.keys():
        damage = item.effects["damage"] +\
            random.randint(item.effects["vary"][0], item.effects["vary"][1])
        hit = random.randint(1, 100) + item.effects["hit"]
        if hit > target.hit:
            target.health = target.health - damage
            print("{} hit {} with {} for {} points of damage. {} has {} health "
                "left".format(user.name, target.name, item.name, damage,
                             target.name, target.health))
        else:
            print("{} misses {} by a slight amount and your {} whistles "
                "through empty air.".format(user.name, target.name, item.name))
            
        if target.health <= 0:
            if target == Player:
                death()
            elif type(target) == type(skeleton):
                del Player.location.enemies[target]
                print("The {} gives a last weak attempt to hit you before "
                    "falling over, dead.".format(target.name))
                change_inventory(Player.location, target.inventory, target)
                print("Objects: {}".format([item.name for item in
                                                Player.location.inventory]))
                return
            elif type(target) == type(thomas):
                del Player.location.enemies[target]
                print("The {} gives a last weak attempt to hit you before "
                    "falling over, dead.".format(target.name))
                return
        if type(target) == type(skeleton):
            use(target, user, target.main_weapon)
            
def talk(person):
    valid_choices = [interaction for interaction in person.interactions.keys()
                     if person.interactions[interaction]["unlocked"]]
    print("Options:")
    for choice in valid_choices:
        print(choice)
    choice = input("What would you like to say?")
    if choice in valid_choices:
        for task_type in person.interactions[choice]["result"]:
            for task in range(len(person.interactions[choice]["result"][task_type])):
                task_type(person.interactions[choice]["result"][task_type][task])

def info():
    pass

def death():
    pass

def end_game():
    pass

def change_inventory_init(values):
    target, items, orgin = values
    change_inventory(target, items, orgin)

def say(values):
    text = values[0]
    print(text)

def unlock(values):
    NPC, interaction = values
    NPC.interactions[interaction]["unlocked"] = True
    
def check(values):
    check, check_vars, result_func, result_vars = values
    if check == "item in inventory":
        if check_vars[0] in check_vars[1].inventory:
            result_func(result_vars)

end = story("The weight of your journey presses down upon you as you hold the scroll, its "
            "parchment glowing faintly with a mysterious light. You can feel the latent power "
            "emanating from the scroll. With reverent hands, you lift it into the air, The path "
            "back is surprisingly clear, as if the dungeon itself acknowledges your triumph. Each "
            "room you traverse seems less daunting, the shadows receding in the wake of your "
            "victory. The creatures that once threatened your progress now cower in the corners, "
            "sensing the power you wield. With a heart full of resolve and eyes set on the "
            "horizon, you prepare for the next chapter of your epic saga. The scroll's secrets "
            "beckon, promising new quests, hidden knowledge, and greater challenges. The legend "
            "of your deeds will echo through the ages, and the adventure, it seems, is only just "
            "beginning.", [end_game])

diamond = item("diamond", {"value": 1000}, "The diamond sparkles with a "
               "brilliance that captures the essence of starlight within its "
               "facets.")

gold_key = item("gold_key", {"key": None}, "The key gleams in the torchlight, "
                "its surface adorned with intricate engravings that catch and "
                "reflect the flickering flames")

wood_chest = chest("wood_chest", gold_key, [diamond])

gold_key.effects["key"] = wood_chest

scroll = item("scroll", {"story": end}, "The scroll, weathered and fragile, "
              "bears the weight of untold knowledge within its carefully penned "
              "characters. Its edges are frayed with age, hinting at the passage "
              "of time. The ink, faded but still legible, tells tales of "
              "forgotten magic, ancient prophecies, and arcane incantations.")

basic_sword = item("basic_sword", {"damage":10, "vary":[-1, 1], "hit":10},
    "A simple metal sword used by all novice swordsmen.")

bone_sword = item("bone_sword", {"damage":15, "vary":[-2, 2], "hit":15},
    "A simple metal sword used by all novice swordsmen.")

skeleton = enemy("skeleton", 20, [gold_key, bone_sword], bone_sword, 20)

thomas = npc("thomas", 50, [scroll], 10,
    {"greet thomas":{"unlocked": True,
                    "result":{say:[["How can I help you?"]],
                    unlock:[["thomas", "ask for a scroll"]]}},
    "ask for a scroll":{"unlocked": False,
                        "result":{say:[["I would like a diamond in return"]],
                         check:[["item in inventory", [diamond, "Player"], unlock,
                                ["thomas", "show him the diamond"]]]}},
    "show him the diamond":{"unlocked": False,
                            "result":{say:[["I will trade you here you go"]],
                             change_inventory_init:[["Player", [scroll], "thomas"],
                             ["thomas", [diamond], "Player"]]
                             }}})

room1 = room(
    "You are in a room that is steeped in a chilling atmosphere, with dimly"
    " flickering torches casting long shadows across blood-stained stone walls."
    " Thick iron chains hang from the ceiling, accompanied by various implements "
    "of torment scattered across crude wooden tables. The air is heavy with the "
    "scent of rust and decay, and the only sound is the occasional drip of water "
    "echoing ominously from unseen corners.",
             [],
             [],
             {"east":2},
             [])

room2 = room(
    "You enter the next room. This room is disorienting from the moment you "
    "step inside, as dozens of mirrors cover every surface, reflecting your "
    "image back at you from every angle. The reflections seem to warp and "
    "distort, creating an unsettling sense of unreality. Some mirrors are "
    "cracked or shattered, adding to the feeling of disarray. It's impossible "
    "to tell which direction is which, as the endless reflections stretch out "
    "into infinity, leaving you feeling trapped in a maze of your own likeness.",
             [],
             [basic_sword],
             {"east":5, "south":3, "west":1},
             [])

room3 = room(
    "As you enter this room, a palpable sense of unease washes over you. Stone "
    "sarcophagi line the walls, their lids adorned with faded engravings of "
    "long-forgotten nobles and warriors. Cobwebs cling to the ceiling, and the "
    "air is thick with the musty scent of decay. Shadows dance in the flickering "
    "torchlight, giving the impression that the deceased within might stir at "
    "any moment. An aura of solemnity hangs heavy in the air, as if the very "
    "walls are whispering tales of the departed.",
             [],
             [],
             {"east":4, "north":2},
             {skeleton:1})

room4 = room(
    "Upon entering, your gaze is immediately drawn to the solitary chest "
    "resting in the center of the room. The chamber is relatively plain "
    "compared to the grandeur of its contents, with stone walls devoid of "
    "adornment. Torch sconces line the perimeter, casting a warm glow that "
    "dances across the metal surface of the chest. A sense of anticipation "
    "fills the air as you approach the treasure, the promise of riches lying "
    "just within reach.",
             [],
             [wood_chest],
             {"north":5, "west":3},
             [])

room5 = room(
    "Upon entering, your eyes are drawn to a solitary wooden cart stationed "
    "in the middle of the room. Laden with an assortment of goods, from basic "
    "supplies to rare trinkets, it seems to serve as a makeshift marketplace "
    "within the dungeon's depths. Crates and barrels are stacked nearby, each "
    "containing its own treasure trove of items waiting to be discovered. The air "
    "is tinged with the scent of ancient dust and the promise of adventure, as "
    "if the very walls whisper tales of the treasures that have passed through "
    "this chamber.",
             [thomas],
             [],
             {"west":2, "south":4},
             [])

rooms = [room1, room2, room3, room4, room5]

def welcome():
    print("Welcome to Dungeon of Darkness!")
    name = input("What is your name, adventurer? ")
    health = 100
    inventory = []
    inventory_space = 10
    hit = 30
    #Damage, Shield
    #modifiers = [1.2, .9]
    #Accuracy, Damage_Range
    #stats = [90, 5]
    print("Good luck in the dungeons {}!".format(name))
    return name, health, hit, inventory, inventory_space, room1

name, health, hit, inventory, inventory_space, location = welcome()
Player = character(name, health, hit, inventory, inventory_space, location)

thomas.interactions["show him the diamond"]["result"][change_inventory_init][0][0] = Player
thomas.interactions["show him the diamond"]["result"][change_inventory_init][0][2] = thomas
thomas.interactions["greet thomas"]["result"][unlock][0][0] = thomas
thomas.interactions["ask for a scroll"]["result"][check][0][3][0] = thomas
thomas.interactions["ask for a scroll"]["result"][check][0][1][1] = Player
thomas.interactions["show him the diamond"]["result"][change_inventory_init][1][0] = thomas
thomas.interactions["show him the diamond"]["result"][change_inventory_init][1][2] = Player

prompts = "0"
print(Player.location.description)
print("Exits: {}".format(str(Player.location.exits.keys())
                         .strip("dict_keys(").strip(")")))
print("Enemies: {}".format([enemy.name for enemy in Player.location.enemies]))
print("NPC's: {}".format([NPC.name for NPC in
                                 Player.location.NPCs]))
print("Other things: {}".format([item.name for item in
                                 Player.location.inventory]))
while prompts[0] != "quit":
    while True:
        prompts = input("What would you like to do? ").casefold().split()
        if len(prompts) > 0:
            break
    if len(prompts) > 3:
        if (prompts[0] == "use" and getattr(sys.modules[__name__], prompts[1],
                                            prompts[1])
            in Player.inventory  and prompts[2] == "on"):
            if (prompts[3] in [enemy.name.casefold() for
                    enemy in Player.location.enemies] or
                prompts[3] in [npc.name.casefold() for
                npc in Player.location.NPCs]):
                use(Player, getattr(sys.modules[__name__], prompts[3], prompts[3]),
                    getattr(sys.modules[__name__], prompts[1], prompts[1]))
            else:
                print("The target is not in the current room")
        else:
            print("You do not have {}".format
                  (prompts[1]))
    elif len(prompts) > 2:
        if prompts[0] in ["talk", "chat", "interact"] and prompts[1] == "with":
            if getattr(sys.modules[__name__], prompts[2], prompts[2]) in Player.location.NPCs:
                talk(getattr(sys.modules[__name__], prompts[2], prompts[2]))
    elif len(prompts) > 1:
        if prompts[0] in ["go", "move", "walk", "run"]:
            Player.location, check = move(Player, Player.location, prompts[1])
            if check:
                print(Player.location.description)
                print("Exits: {}".format(str(Player.location.exits.keys())
                    .strip("dict_keys(").strip(")")))
                print("Enemies: {}".format([enemy.name for enemy in
                                            Player.location.enemies]))
                print("NPC's: {}".format([NPC.name for NPC in
                                 Player.location.NPCs]))
                print("Other things: {}".format([item.name for item in
                                                Player.location.inventory]))
        elif prompts[0] in ["grab", "get"]:
            pick_up(Player, [getattr(sys.modules[__name__], item, item)
                             for item in prompts[1:len(prompts)]], "null")
        elif prompts[0] in ["open", "view"]:
            if (type(getattr(sys.modules[__name__],prompts[1], prompts[1])) == 
            type(wood_chest) and getattr(sys.modules[__name__], prompts[1],
                                         prompts[1])
            in Player.location.inventory):
                if (getattr(sys.modules[__name__], prompts[1], prompts[1]).key in
                    Player.inventory):
                    view_chest(getattr(sys.modules[__name__], prompts[1],
                                       prompts[1]))
                else:
                    print("You do not have the key for this chest. {} required."
                          .format(getattr(sys.modules[__name__], prompts[1],
                                          prompts[1]).key))
            else:
                print("The chest you are looking for is not in this room.")
        else:
            print("That is not an option")
    elif prompts[0] == "quit":
        print("Cya Next Time Adventurer!")
    elif prompts[0] == "info":
        info()
    else:
        print("That is not an option")
