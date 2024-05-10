import sys
import random

# Define class for playable character
class Character():
    def __init__(self, name, health, hit, inventory, inventory_space, location):
        """
        Initialize a Character instance.

        Args:
        - name (str): Name of the character.
        - health (int): Current health points of the character.
        - hit (int): Hit points of the character.
        - inventory (list): List of items in the character's inventory.
        - inventory_space (int): Maximum capacity of the character's inventory.
        - location (Room): The current location of the character.
        """
        self.name = name
        self.health = health
        self.hit = hit
        self.inventory = inventory
        self.inventory_space = inventory_space
        self.location = location

# Define class for non-player characters
class NPC():
    def __init__(self, name, health, inventory, interactions):
        """
        Initialize an NPC instance.

        Args:
        - name (str): Name of the NPC.
        - health (int): Current health points of the NPC.
        - inventory (list): List of items in the NPC's inventory.
        - interactions (dict): Dictionary of interactions with the NPC and its responses.
        """
        self.name = name
        self.health = health
        self.inventory = inventory
        self.interactions = interactions

# Define class for chests containing items
class Chest():
    def __init__(self, name, key, inventory):
        """
        Initialize a Chest instance.

        Args:
        - name (str): Name of the chest.
        - key (Item): Key required to open the chest.
        - inventory (list): List of items stored in the chest.
        """
        self.name = name
        self.key = key
        self.inventory = inventory

# Define class for items that can be picked up and used
class Item():
    def __init__(self, name, effects, description):
        """
        Initialize an Item instance.

        Args:
        - name (str): Name of the item.
        - effects (dict): Dictionary of effects the item has when used.
        - description (str): Description of the item.
        """
        self.name = name
        self.effects = effects
        self.description = description

# Define class for enemies that characters can encounter
class Enemy():
    def __init__(self, name, health, inventory, main_weapon, hit):
        """
        Initialize an Enemy instance.

        Args:
        - name (str): Name of the enemy.
        - health (int): Current health points of the enemy.
        - inventory (list): List of items carried by the enemy.
        - main_weapon (Item): Main weapon used by the enemy.
        - hit (int): Hit points of the enemy.
        """
        self.name = name
        self.health = health
        self.inventory = inventory
        self.main_weapon = main_weapon
        self.hit = hit

# Define class for a room within the game world
class Room:
    def __init__(self, description, NPCs, inventory, exits, enemies):
        """
        Initialize a Room instance.

        Args:
        - description (str): Description of the room.
        - NPCs (list): List of non-player characters in the room.
        - inventory (list): List of items present in the room.
        - exits (dict): Dictionary of exits from the room.
        - enemies (list): List of enemies present in the room.
        """
        self.description = description
        self.NPCs = NPCs
        self.inventory = inventory
        self.exits = exits
        self.enemies = enemies
        
# Define class for a story or quest within the game
class Story:
    def __init__(self, story, actions):
        """
        Initialize a Story instance.

        Args:
        - story (str): Description or text of the story.
        - actions (str): Actions associated with the story.
        """
        self.story = story
        self.actions = actions
        
# Function to move the character to a different room
def move(character, current_room, direction):
    """
    Move the character to a different room.

    Args:
    - character (Character): The character being moved.
    - current_room (Room): The current room of the character.
    - direction (str): The direction in which the character wants to move.

    Returns:
    - Room: The new room the character has moved into.
    - bool: True if the move was successful, False otherwise.
    """
    if direction in current_room.exits.keys():
        # Move to the next room if the direction is a valid exit
        return rooms[Player.location.exits[prompts[1]]-1], True
    else:
        if character == Player:
            # Inform the player if the direction is not valid
            print("That is not an option\nExits: {}"
                .format(str(Player.location.exits.keys())[11:-2]))
        return current_room, False

# Function to view the contents of a chest
def view_chest(chest):
    """
    Display the contents of a chest and allow the player to interact with it.

    Args:
    - chest (Chest): The chest to be viewed.
    """
    print("Items: {}".format([item.name for item in chest.inventory]))
    choices = [0]
    while choices[0] != "exit":
        choices = input("What would you like to do? ").split()
        if len(choices) > 1:
            if choices[0] in ["grab", "get"]:
                # Allow the player to pick up items from the chest
                pick_up(Player, [getattr(sys.modules[__name__], item, item)
                                     for item in choices[1:len(choices)]], chest)
            else:
                print("that is not an option")
    print("Chest closed")

# Function to pick up items
def pick_up(user, items, chest):
    """
    Pick up items and add them to the player's inventory.

    Args:
    - user (Character): The character picking up the items.
    - items (list): The items to be picked up.
    - chest (Chest): The chest from which the items are being picked up (if applicable).
    """
    for item in items:
        if chest != "null":
            # If items are from a chest, add them to the player's inventory
            change_inventory(user, [item], chest)
        elif item in user.location.inventory:
            # If items are from the room's inventory, add them to the player's inventory
            change_inventory(user, [item], Player.location)
        else:
            if user == Player:
                if type(item) == str:
                    # Inform the player if the item is not in the room
                    print("{} is not in your room".format(item))
                else:
                    print("{} is not in your room".format(item.name))

# Function to change inventory
def change_inventory(target, items, origin):
    """
    Change the inventory of a character or room.

    Args:
    - target (Character or Room): The target whose inventory is being changed.
    - items (list): The items to be added to the inventory.
    - origin (Room or str): The origin of the items being added.
    """
    if type(target) != type(room1):
        if len(target.inventory)+len(items) < target.inventory_space:
            for item in items:
                # Add items to the target's inventory
                target.inventory.append(item)
                if origin != "null":
                    # If the items were given from another object remove the items from the origin
                    origin.inventory.remove(item)
                if target == Player:
                    # Inform the player about the item added to their inventory
                    print("{} added to inventory...".format(item.name))
        else:
            print("You do not have enough space in your inventory")
    else:
        for item in items:
            target.inventory.append(item)
            if target == Player:

                # Inform the player about the item added to their inventory
                print("{} added to inventory...".format(item.name))
        if origin != "null":
            # If the origin is not null, remove the items from the origin
            for item in items:
                origin.inventory.remove(item)

# Function to use an item or attack an enemy
def use(user, target, item):
    """
    Use an item or attack an enemy.

    Args:
    - user (Character): The character using the item or attacking.
    - target (Character or Enemy): The target of the action.
    - item (Item): The item being used (if applicable).
    """
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
                # If the player's health reaches zero or below, trigger death function
                death()
            elif type(target) == type(skeleton):
                # If the target is an enemy, remove it from the room's enemy list
                del Player.location.enemies[target]
                print("The {} gives a last weak attempt to hit you before "
                    "falling over, dead.".format(target.name))
                # Transfer the enemy's inventory to the room
                change_inventory(Player.location, target.inventory, target)
                print("Objects: {}".format([item.name for item in
                                                Player.location.inventory]))
                return

        if type(target) == type(skeleton):
            # If the target is an enemy, use its main weapon against the player
            use(target, user, target.main_weapon)

# Function to provide information or hints to the player
def info():
    pass

# Function to handle player death
def death():
    pass

# Define the end story of the game
end = Story("THE END", "end game")

# Define game items
diamond = Item("diamond", {"value": 1000}, "The diamond sparkles with a "
               "brilliance that captures the essence of starlight within its "
               "facets.")

gold_key = Item("gold_key", {"key": None}, "The key gleams in the torchlight, "
                "its surface adorned with intricate engravings that catch and "
                "reflect the flickering flames")

wood_chest = Chest("wood_chest", gold_key, [diamond])

gold_key.effects["key"] = wood_chest

scroll = Item("scroll", {"story": end}, "The scroll, weathered and fragile, "
              "bears the weight of untold knowledge within its carefully penned "
              "characters. Its edges are frayed with age, hinting at the passage "
              "of time. The ink, faded but still legible, tells tales of "
              "forgotten magic, ancient prophecies, and arcane incantations.")

basic_sword = Item("basic_sword", {"damage":10, "vary":[-1, 1], "hit":10},
    "A simple metal sword used by all novice swordsmen.")

bone_sword = Item("bone_sword", {"damage":15, "vary":[-2, 2], "hit":15},
    "A simple metal sword used by all novice swordsmen.")

skeleton = Enemy("skeleton", 20, [gold_key, bone_sword], bone_sword, 20)

# Define game rooms
room1 = Room(
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

room2 = Room(
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

room3 = Room(
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

room4 = Room(
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

room5 = Room(
    "Upon entering, your eyes are drawn to a solitary wooden cart stationed "
    "in the middle of the room. Laden with an assortment of goods, from basic "
    "supplies to rare trinkets, it seems to serve as a makeshift marketplace "
    "within the dungeon's depths. Crates and barrels are stacked nearby, each "
    "containing its own treasure trove of items waiting to be discovered. The air "
    "is tinged with the scent of ancient dust and the promise of adventure, as "
    "if the very walls whisper tales of the treasures that have passed through "
    "this chamber.",
             [],
             [],
             {"west":2, "south":4},
             [])

rooms = [room1, room2, room3, room4, room5]

# Function to welcome the player and initialize the game
def welcome():
    """
    Welcome the player and initialize the game.

    Returns:
    - tuple: A tuple containing player information and starting location.
    """
    print("Welcome to Dungeon of Darkness!")
    name = input("What is your name, adventurer? ")
    health = 100
    inventory = []
    inventory_space = 10
    hit = 30
    print("Good luck in the dungeons {}!".format(name))
    return name, health, hit, inventory, inventory_space, room1

# Initialize the player character
name, health, hit, inventory, inventory_space, location = welcome()
Player = Character(name, health, hit, inventory, inventory_space, location)

# Display initial room description and available actions
prompts = "0"
print(Player.location.description)
print("Exits: {}".format(str(Player.location.exits.keys())
                         .strip("dict_keys(").strip(")")))
print("Enemies: {}".format([enemy.name for enemy in Player.location.enemies]))
print("NPC's: {}".format([NPC.name for NPC in
                                 Player.location.NPCs]))
print("Other things: {}".format([item.name for item in
                                 Player.location.inventory]))

# Main game loop
while prompts[0] != "quit":
    # Loop until a valid input is received
    while True:
        # Prompt the player for input
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
                # Use the item or attack the target
                use(Player, getattr(sys.modules[__name__], prompts[3], prompts[3]),
                    getattr(sys.modules[__name__], prompts[1], prompts[1]))
            else:
                print("The target is not in the current room")
        else:
            print("You do not have {}".format
                  (prompts[1]))
    elif len(prompts) > 1:
        if prompts[0] in ["go", "move", "walk", "run"]:
            # Move to the specified direction
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
            # Pick up items
            pick_up(Player, [getattr(sys.modules[__name__], item, item)
                             for item in prompts[1:len(prompts)]], "null")
        elif prompts[0] in ["open", "view"]:
            if (type(getattr(sys.modules[__name__],prompts[1], prompts[1])) == 
            type(wood_chest) and getattr(sys.modules[__name__], prompts[1],
                                         prompts[1])
            in Player.location.inventory):
                if (getattr(sys.modules[__name__], prompts[1], prompts[1]).key in
                    Player.inventory):
                    # View the contents of a chest
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
        # Provide information or hints to the player
        info()
    else:
        print("That is not an option")
