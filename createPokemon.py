import random
import copy
import csv

########################################################################
########################################################################
# _________    _____________   ____ 
# \_   ___ \  /   _____/\   \ /   / 
# /    \  \/  \_____  \  \   Y   /  
# \     \____ /        \  \     /   
#  \______  //_______  /   \___/    
#         \/         \/             
########################################################################
########################################################################

def makeListFromString(s):
    isWord = False
    result = []
    currentWord = ""
    for c in s:
        if isWord:
            currentWord += c

        if c == "," and isWord:
            result.append(currentWord[2:-2])
            currentWord = ""
            isWord = not isWord
        elif c == ",":
            isWord = not isWord
    return result

pokemonList = dict()
with open("pokemon-data.csv", "r") as file:
    csvreader = csv.reader(file, delimiter=";")
    for pokemon in csvreader:
        pokemonList[pokemon[0]] = {
            "Type": pokemon[1],
            "Abilities": makeListFromString(pokemon[2]),
            "HP": (pokemon[4]),
            "Attack": (pokemon[5]),
            "Defense": (pokemon[6]),
            "Special Attack": (pokemon[7]),
            "Special Defense": (pokemon[8]),
            "Speed": (pokemon[9]),
            "Evolution": pokemon[10],
            "Move Set": makeListFromString(pokemon[11])
        }

moveList = dict()
with open("move-data.csv", "r") as file:
    csvreader = csv.reader(file, delimiter=",")
    for move in csvreader:
        moveList[move[1]] = {
            "Type": move[2],
            "Category": move[3],
            "PP": move[5],
            "Power": move[6],
            "Accuracy": move[7]
        }

index = 32

########################################################################
########################################################################
# __________         __                                      
# \______   \ ____  |  | __  ____    _____    ____    ____   
#  |     ___//  _ \ |  |/ /_/ __ \  /     \  /  _ \  /    \  
#  |    |   (  <_> )|    < \  ___/ |  Y Y  \(  <_> )|   |  \ 
#  |____|    \____/ |__|_ \ \___  >|__|_|  / \____/ |___|  / 
#                        \/     \/       \/              \/  
########################################################################
########################################################################                                                


def almostEqual(d1, d2, epsilon=10**-7): #helper-fn
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d): #helper-fn
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

# Takes in list of possible moves and returns 4 distinct ones in a list
def selectMoves(moveSet, i):
    addedMoves = [""] * i
    while i > 0:
        move = moveSet[random.randint(0, len(moveSet)-1)]
        temp = ""
        for word in move.split("'"):
            temp += word + "-"
        temp = temp[:-1]
        move = temp
        if not (move in addedMoves) and moveList[move]["Power"] != "None":
            addedMoves[i-1] = move
            i -= 1
    return addedMoves

class Pokemon(object):
    def __init__(self, level, name, stats):
        self.name = name
        self.type = stats["Type"]
        self.lvl = level
        # Get move set for this instance
        moveSet = stats["Move Set"]
        self.moves = selectMoves(moveSet, 4)
        # Stats
        self.baseHP , self.modHP = int(stats["HP"]), 2       
        self.hp = roundHalfUp(self.baseHP + self.lvl * self.modHP)
        self.baseATK, self.modATK = int(stats["Attack"]), 1.1 
        self.attack = roundHalfUp(self.baseATK + self.lvl * self.modATK)
        self.baseSPATK, self.modSPATK = int(stats["Special Attack"]), 1.1 
        self.SPattack = roundHalfUp(self.baseSPATK + self.lvl * self.modSPATK)
        self.baseDEF, self.modDEF = int(stats["Defense"]), 0.5 
        self.defense = roundHalfUp(self.baseDEF + self.lvl * self.modDEF)
        self.baseSPDEF, self.modSPDEF = int(stats["Special Defense"]), 0.5 
        self.SPdefense = roundHalfUp(self.baseSPDEF + self.lvl * self.modSPDEF)
        self.baseSPD, self.modSPD = int(stats["Speed"]), 1.1 
        self.speed = roundHalfUp(self.baseSPD + self.lvl * self.modSPD)
    
    def getMaxHP(self):
        return roundHalfUp(self.baseHP + self.lvl * self.modHP)

    def incrHP(self, incr):
        self.hp = int(roundHalfUp(self.hp + incr))

    def decrHP(self, decr):
        self.hp = int(roundHalfUp(self.hp - decr))
    
    def incrAttack(self, incr):
        self.attack = int(roundHalfUp(self.attack + incr))

    def decrAttack(self, decr):
        self.attack = int(roundHalfUp(self.attack - decr))
    
    def incrDefense(self, incr):
        self.defense = int(roundHalfUp(self.defense + incr))

    def decrDefense(self, decr):
        self.defense = int(roundHalfUp(self.defense - decr))
    
    def incrSpeed(self, incr):
        self.speed = int(roundHalfUp(self.speed + incr))

    def decrSpeed(self, decr):
        self.speed = int(roundHalfUp(self.speed - decr))


    def __repr__(self):
        return(
        f"\n{self.name}"
        f"\nlevel={self.lvl}, type={self.type},"
        f"\nmoves={self.moves}"
        f"\nhp={self.hp}, atk={self.attack}, spatk={self.SPattack}, df="
        f"{self.defense}, spdf={self.SPdefense}, sp={self.speed}"
        f"\n")

def doDamage(power, attacker, defender, modATK, modDEF):
    dmg = int(power*attacker.attack*modATK/(1+modDEF*defender.defense))
    defender.decrHP(dmg)
    return dmg

def doAttack(move, attacker, defender, attacker0 = 0, defender0 = 0):
    modATK = 0.01
    modDEF = 0.01
    moveName = move
    move = moveList[move]
    # Deals 40 damage to defender
    if move["Power"] != "None":
        if move["Category"] == "Physical":
            power = int(move["Power"])
            dmg = int(power*attacker.attack*modATK/(1+modDEF*defender.defense))
            defender.decrHP(dmg)
            return f"{attacker.name} used {moveName}! It did {dmg} damage!"
        elif move["Category"] == "Special":
            power = int(move["Power"])
            dmg = int(power*attacker.SPattack*modATK/
                      (1+modDEF*defender.SPdefense))
            defender.decrHP(dmg)
            return f"{attacker.name} used {moveName}! It did {dmg} damage!"

def startEncounter():
    pok1 = random.choice(list(pokemonList.keys()))
    pok2 = random.choice(list(pokemonList.keys()))
    j0 = Pokemon(20, pok1, pokemonList[pok1])
    p0 = Pokemon(20, pok2, pokemonList[pok2])
    j1 = copy.deepcopy(j0)
    p1 = copy.deepcopy(p0)

    while j1.hp > 0 and p1.hp > 0:
        if j1.speed > p1.speed:
            first1, first0 = j1, j0
            second1, second0 = p1, p0
        else:
            first1, first0 = p1, p0
            second1, second0 = j1, j0
        move0 = selectMove(first1, second1)
        move1 = selectMove(second1, first1)
        print("\n\n\n")
        print(doAttack(move0, first1, second1, first0, second0))
        if second1.hp < 0:
            print(f"{first1.name} wins!")
            break
        print(doAttack(move1, second1, first1, second0, first0))
        if first1.hp < 0:
            print(f"{second1.name} wins!")

def selectMove(attack, defend):    
    print(f"\nIt's {attack.name}'s (level {attack.lvl}) turn! It has " +
            f"{attack.hp} hp. {defend.name} has {defend.hp} hp. Moves:")
    for i in range(len(attack.moves)):
        print(f"{i} - {attack.moves[i]}   ", end="")
    print("")
    i = 0
    while i < 1:
        index = input("Choose your move: ")
        if index.isdigit() and 0 <= int(index) < len(attack.moves):
            return attack.moves[int(index)]
        else:
            print("\n\nPlease don't be an ass and choose a valid move")

startEncounter()



