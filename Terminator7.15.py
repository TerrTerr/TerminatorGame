Terminators = []
Rebels = []
Weapons = []

import random
import time
from colorama import Fore, Style

def slow_print(s):
    for c in s:
        print(c, end='', flush=True)
        time.sleep(0.05)
    print()

class Terminator:
    def __init__(self, tag, health, weapon, armor, reflexes, to_hit=None, evade=None, user_controlled=False):
        self.tag = tag
        self.health = health
        self.weapon = weapon
        self.armor = armor
        self.orient = True
        self.nuclear = True
        self.reflexes = reflexes
        self.to_hit = to_hit if to_hit is not None else random.randint(1, 100)  # Set to_hit
        self.evade = evade if evade is not None else random.randint(1, 25)
        self.user_controlled = user_controlled
        self.turn_count = 0
        Terminators.append(self)

    def __repr__(self):
        return "This {tag} has {health} hit points remaining. They are a Terminator.".format(tag = self.tag, health=self.health)

    def impersonate(self, Rebel):
        time.sleep(1) 
        slow_print("{rebel}? It's Maggie, your next door neighbor I saw you run into this factory, is everything okay?".format(rebel=Rebel.codename))
        slow_print(Fore.GREEN + "The vocal impersonation of Maggie is uncanny and while it is obvious that Maggie is not in the factory, it is nonetheless unsettling." + Style.RESET_ALL)
        slow_print(Fore.GREEN + "Human Attack and Evade stats temporarily reduced." + Style.RESET_ALL)
        Rebel.to_hit = max(0, Rebel.to_hit - 20) 
        Rebel.evade = max(0, Rebel.evade - 20) 
        Rebel.freakout = 3
    
    def take_turn(self, target):
        self.turn_count += 1
        if self.orient:
            if self.user_controlled:
                while True:
                    print(" ")
                    print(" ")
                    action = input("{0}, it's your turn! Type: \nATT to attack \nIMP to impersonate \n".format(self.tag)).upper()
                    if action == 'ATT':
                        self.attack(target)
                        break
                    elif action == 'IMP':
                        self.impersonate(target)
                        break
                    else:
                        slow_print(Fore.RED + "Invalid action! Type: \nATT to attack \nIMP to reorient\n" + Style.RESET_ALL)
            else:
                if self.turn_count % 5 == 0:
                    self.impersonate(target)
                else:
                    self.attack(target)
        else:
            self.Reorient()

    def Reorient(self):
        self.orient = True
        time.sleep(1) 
        slow_print("SQUAWK System Reorienting...")

    def attack(self, character):  
        hit_roll = random.randint(1, 100)
        required_roll = max((self.to_hit + self.weapon.accuracy_bonus) - (character.evade if character.evade else 0), 1)

        if hit_roll <= 5:
            slow_print(Fore.BLUE + "{0} attacks with their {1} and misses.".format(self.tag, self.weapon.name) + Style.RESET_ALL)

        elif hit_roll >= 96:
            damage_dealt = self.weapon.damage * 2
            damage_dealt -= (damage_dealt * (character.armor.percent_absorption / 100))
            character.health -= damage_dealt
            slow_print(Fore.RED + "{0} landed a CRITICAL HIT on {1} using {2}, causing {3} damage. {1}'s remaining health: {4}".format(
                self.tag,
                character.codename if isinstance(character, Rebel) else character.tag,
                self.weapon.name,
                damage_dealt,
                character.health) + Style.RESET_ALL)

        elif hit_roll > required_roll:
            slow_print(Fore.BLUE + "{0} attacks with their {1} and misses.".format(self.tag, self.weapon.name) + Style.RESET_ALL)

        else:
            if self.orient:
                    damage_dealt = self.weapon.damage 
                    damage_dealt -= (damage_dealt * (character.armor.percent_absorption / 100))
                    character.health -= damage_dealt                
                    slow_print(Fore.RED + "{0} attacked {1} using {2}, causing {3} damage. {1}'s remaining health: {4}".format(
                        self.tag,
                        character.codename if isinstance(character, Rebel) else character.tag,
                        self.weapon.name,
                        damage_dealt,   
                        character.health) + Style.RESET_ALL)
                    
                    if isinstance(character, Terminator):
                        character.orient = False
                        slow_print(Fore.GREEN + "{0} is disoriented.".format(character.tag) + Style.RESET_ALL)

                    if isinstance(character, Rebel):
                        bleed_roll = random.randint(1, 100)
                        if bleed_roll <= 33:
                            character.bleed = True
                            slow_print(Fore.GREEN + "{0} is bleeding badly!".format(character.codename) + Style.RESET_ALL)

            else:
                slow_print(Fore.GREEN + "{0} is disoriented and must reorient before attacking.".format(self.tag) + Style.RESET_ALL)

class Rebel:
    def __init__(self, codename, health, weapon, armor, reflexes, to_hit=None, evade=None, user_controlled = False):
        self.codename = codename
        self.health = health
        self.weapon = weapon
        self.armor = armor
        self.in_love = True
        self.reflexes = reflexes
        self.to_hit = to_hit if to_hit is not None else random.randint(1, 100) 
        self.evade = evade if evade is not None else random.randint(1, 25)
        self.bleed = False
        self.breather_uses = 0
        self.freakout = 0 
        self.original_to_hit = self.to_hit 
        self.original_evade = self.evade
        self.user_controlled = user_controlled
        Rebels.append(self)

    def __repr__(self):
        return "This {codename} has {health} hit points remaining. They are a Rebel.".format(codename = self.codename, health=self.health)
   
    def take_turn(self, target):
        if self.freakout > 0:
            self.freakout -= 1
            if self.freakout == 0: 
                self.to_hit = self.original_to_hit
                self.evade = self.original_evade
        if self.user_controlled:
            while True:
                print(" ")
                print(" ")               
                action = input("{0}, it's your turn! Type: \nATT to attack \nMED to stop bleeding/heal\n".format(self.codename)).upper()
                if action.upper() == 'ATT':
                    self.attack(target)
                    break
                elif action.upper() == 'MED':
                    if self.breather_uses < 3:
                        self.breather()
                        break
                    else:
                        slow_print(Fore.BLUE + "{0} has used up all their Med Packs!".format(self.codename) + Style.RESET_ALL)
                else:
                    slow_print(Fore.RED + "Invalid action! Type: \nATT to attack \nMED to stop bleeding/heal\n" + Style.RESET_ALL)
        else:
            if self.bleed and self.breather_uses < 3:
                self.breather()
            else:
                self.attack(target)
                
    def breather(self):
        if self.breather_uses < 3:
            self.health += 25
            self.bleed = False
            self.breather_uses += 1
            slow_print(Fore.LIGHTBLUE_EX + "{0} uses their Med Pack to staunchh their bleeding. \nA quick stim injection adds 25 points of health. \nTotal health is now {1}.".format(self.codename, self.health) + Style.RESET_ALL)
        else:
            pass

    def attack(self, character):  
        hit_roll = random.randint(1, 100)
        required_roll = max((self.to_hit + self.weapon.accuracy_bonus) - (character.evade if character.evade else 0), 1)
        if hit_roll <= 5:
            slow_print(Fore.BLUE + "{0} attacks with their {1} and misses.".format(self.codename, self.weapon.name) + Style.RESET_ALL)
        elif hit_roll >= 96:
            damage_dealt = self.weapon.damage * 2
            damage_dealt -= (damage_dealt * (character.armor.percent_absorption / 100))
            character.health -= damage_dealt
            slow_print(Fore.RED + "{0} landed a CRITICAL HIT on {1} using {2}, causing {3} damage. {1}'s remaining health: {4}".format(
                self.codename,
                character.tag if isinstance(character, Terminator) else character.codename,
                self.weapon.name,
                damage_dealt,
                character.health) + Style.RESET_ALL)
            if isinstance(character, Terminator):
                character.orient = False
                slow_print(Fore.GREEN + "{0} is disoriented.".format(character.tag) + Style.RESET_ALL)
        elif hit_roll > required_roll:
            slow_print(Fore.BLUE + "{0} attacks with their {1} and misses.".format(self.codename, self.weapon.name) + Style.RESET_ALL)
        else:
            damage_dealt = self.weapon.damage 
            damage_dealt -= (damage_dealt * (character.armor.percent_absorption / 100))
            character.health -= damage_dealt      
            slow_print(Fore.RED + "{0} attacked {1} using {2}, causing {3} damage. {1}'s remaining health: {4}".format(
                self.codename,
                character.tag if isinstance(character, Terminator) else character.codename,
                self.weapon.name,
                damage_dealt,
                character.health) + Style.RESET_ALL)
            if isinstance(character, Terminator):
                character.orient = False
                slow_print(Fore.GREEN + "{0} is disoriented.".format(character.tag) + Style.RESET_ALL)

    def ambush(self, terminator):
        self.attack(terminator)
        self.attack(terminator)

class Weapon:
    def __init__(self, name, sort, damage, accuracy_bonus=0):
        self.name = name
        self.sort = sort
        self.damage = damage
        self.accuracy_bonus = accuracy_bonus
        Weapons.append(self.name)

    def __repr__(self):
        return "This {name} can cause {damage} points of damage. It is a weapon.".format(name = self.name, damage=self.damage)

class Armor:
    def __init__(self, strength, percent_absorption):
        self.strength = strength
        self.percent_absorption = percent_absorption

#Weapons
Machete = Weapon("Machete", "Edged", 15, 5)
Blades = Weapon("Blades", "Edged", 35, 0)
Shotgun = Weapon("Sawed Off Shotgun", "Gun", 27, 20)
Uzi = Weapon("Uzi", "Gun", 42, -12)
Automatic_Pistol = Weapon("Colt Chambered Pistol", "Gun", 20, 0)
AK47 = Weapon("AK47", "Gun", 55, -10)
Gatling = Weapon("Gatling Gun", "Gun", 92, -20)
Grenade_Launcher = Weapon("Grenade Launcher", "Gun", 72, 0)
Longslide = Weapon(".45 longslide with laser sighting", "Gun", 20, 35)
Twelve_Gauge = Weapon("12 Gauge Auto-Loader", "Gun", 37, 45)

#Armor
Light = Armor("Light", 5)
Medium = Armor("Medium", 30)
Heavy = Armor("Heavy", 50)
Extreme = Armor("Extreme", 75)  

#Rebels
Sarah = Rebel('Sarah Connors', 78, Machete, Light, 81, 38, user_controlled=False)
John_Young = Rebel('Young John Connors', 58, Automatic_Pistol, Light, 26, 34, user_controlled=False)
Reese = Rebel("Reese", 87, Shotgun, Light, 92, 40, user_controlled=False)
Enrique = Rebel('Enrique Salceda', 61, AK47, Medium, 55, 29, user_controlled=False)

#Terminators
T800 = Terminator("T-800", 350, Longslide, Heavy, 45, 10, user_controlled=False)
T1000 = Terminator("T-1000", 225, Blades, Extreme, 64, 32, user_controlled=False)
#T3000 = Terminator("T-3000", 540, Machete, Heavy, 100, 100, user_controlled=False)

def yes_or_no(question):
    while True:
        answer = input(question + " (yes/no): ").lower().strip()
        if answer in ['yes', 'no']:
            return answer == 'yes'
        else:
            time.sleep(1) 
            slow_print("Please answer 'yes' or 'no'.")

def choose_option(question, option1, option2):
    while True:
        answer = input(question + " ({0}/{1}): ".format(option1, option2)).lower().strip()
        if answer in [option1, option2]:
            return answer
        else:
            time.sleep(1) 
            slow_print("Please answer '{0}' or '{1}'.".format(option1, option2))

def choose_character(character_type):
    while True:
        characters = Rebels if character_type == 'Rebel' else Terminators
        for i, character in enumerate(characters):
            slow_print("{0}. {1}".format(i+1, character.codename if isinstance(character, Rebel) else character.tag))
        choice = input("Choose your {0} (enter the number): ".format(character_type))
        if choice.isdigit() and 1 <= int(choice) <= len(characters):
            chosen_character = characters[int(choice) -1] 
            chosen_character.user_controlled = True
            return chosen_character
        else:
            slow_print("Invalid choice. Please choose a number from the list.")

print("Welcome, User.")
if yes_or_no("Would you like to play a game of TERMINATOR DEATH MATCH?"):
    character_type = choose_option("Would you prefer to play as a rebel or as a terminator?", "rebel", "terminator").title()
    user_character = choose_character(character_type)
    time.sleep(1) 
    slow_print("You are playing as {0}.\n".format(user_character.codename if isinstance(user_character, Rebel) else user_character.tag))

    if isinstance(user_character, Rebel):
        slow_print("You're body is exhausted.  Your mind is terrified.  Behind you, somewhere, is a machine from the future sent to kill you.  It never gets tired.  It never feels pain.  And it never stops.  Just when all hope seemed lost, you see a factory in the distance.  Perfect you think!  Perfect.  You sneak to a basement door down a long concrete staircase.  It's locked but nothing you can't pick.  A moment later you're inside and... What the?  The goddamn terminator is right in front of you! You lift your weapon, grit your teeth and fight.")
    else:
        slow_print("Human target located, heading towards abandoned factory.  They always go inside when near an abandpned factory.  You will beat them there, you compute as you break the handle to the main entrance.  Now where will they come from?  The basement, the structure's lowest point, where the rats always come from. You make your way there and once there find your prey, a termination target.  You lift your weapon.  If you understood smiles, you would have had on your face as you aim your weapon and fight.")

    # Get the list of characters from the opposing side opposing_characters = Terminators if isinstance(user_character, Rebel) else Rebels
    opposing_characters = Terminators if isinstance(user_character, Rebel) else Rebels

    # Choose a random character from the opposing side
    random_opponent = random.choice(opposing_characters)

    # Set the players list
    players = [user_character, random_opponent]

    while players[0].health > 0 and players[1].health > 0:
        print(" ")
        print(" ")
        print("NEW ROUND")

        for p in players:
            if isinstance(p, Rebel) and p.bleed:
                bleed_damage = 5
                p.health -= bleed_damage
                slow_print(Fore.GREEN + "{0} is bleeding, causing 5 points of damage, reducing health to {1}.".format(p.codename, p.health) + Style.RESET_ALL)
        
        for p in players:
            if isinstance(p, Terminator) and p.orient == False:
                slow_print(Fore.GREEN + "{0} is disoriented and needs to reorient.".format(p.tag) +Style.RESET_ALL)

        time.sleep(1)
        print(" ")
        print(" ")
        input("\nPress enter to continue with the next reflex roll...")
        # Reflex Rolls
        random.shuffle(players)
        reflex_scores = [(p, p.reflexes + random.randint(1, 100)) for p in players]
        reflex_scores.sort(key=lambda x: x[1], reverse=True)
        first_player, second_player = reflex_scores[0][0], reflex_scores[1][0]

        #reflex roll results
        time.sleep(1)  
        slow_print("{0} rolled {1} + {2} (reflexes) = {3}".format(first_player.codename if isinstance(first_player, Rebel) else first_player.tag, reflex_scores[0][1] - first_player.reflexes, first_player.reflexes, reflex_scores[0][1]))
        time.sleep(1)  
        slow_print("{0} rolled {1} + {2} (reflexes) = {3}".format(second_player.codename if isinstance(second_player, Rebel) else second_player.tag, reflex_scores[1][1] - second_player.reflexes, second_player.reflexes, reflex_scores[1][1]))
        time.sleep(1)  
        slow_print("{0} wins the roll and goes first!\n".format(first_player.codename if isinstance(first_player, Rebel) else first_player.tag))
    
        #player turns
        first_player.take_turn(second_player)
        if second_player.health <= 0:
            break

        second_player.take_turn(first_player)
        if first_player.health <= 0:
            break
        
    if players[0].health <= 0:
        if isinstance(players[0], Rebel):
            slow_print("The Terminator has won TERMINATOR DEATH MATCHH!  Now bulldozers will raze the Earth and robots will hunt humans down until they are extinct!")
        else:
            slow_print("The Human has won the TERMINATOR DEATH MATCH!  Now humans can live without the threat of an artificial intelligence armageddon, free to spend their days staring at social media. :)")
    elif players[1].health <= 0:  
        if isinstance(players[1], Rebel):
            slow_print("The Terminator has won TERMINATOR DEATH MATCHH!  Now bulldozers will raze the Earth and robots will hunt humans down until they are extinct!")
        else:
            slow_print("The Human has won the TERMINATOR DEATH MATCH!  Now humans can live without the threat of an artificial intelligence armageddon, free to spend their days staring at social media. :)")
 
else:
    time.sleep(4) 
    slow_print("Cha...   Cha... ")
    slow_print("Cha... Cha... Cha... Cha.Cha.ChaChaChaChaCha...")
    slow_print("Chicken!")
    