import operator
import json
import shlex
from rich import print
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table
from rich.panel import Panel

class uitools:
    def question_yn(question) :
        yes = {'yes','y', 'ye', ''}
        no = {'no','n'}
        while True:
            print(question)
            try:
                givenanswer = input().lower()
                if givenanswer in yes:
                    return True
                elif givenanswer in no:
                    return False
                else:
                    raise Exception("Please respond with 'yes' or 'no'.")
            except Exception as e:
                print(e)
            continue

    def question_int(question) :
        while True:
            print(question)
            try:
                givenanswer = int(input())
                return givenanswer
            except:
                print("Please enter a whole number.")
            continue


class character:
    def __init__(self, name, initiative, armorClass, conditions) :
        self.name = name
        self.initiative = initiative
        self.armorClass = armorClass
        self.conditions = conditions

    def addCondition(self, conditionname):
        defaultList = characterconditions.fetchDefaultList()
        if conditionname.lower() in defaultList.keys():
            self.conditions[conditionname] = characterconditions(defaultList[conditionname]["name"],defaultList[conditionname]["description"],defaultList[conditionname]["icon"])
        else:
            description = input("Enter a note or description")
            self.conditions[conditionname] = characterconditions(conditionname,description,"")

class characterconditions:
    def __init__(self, name, description, icon, turns = False) :
        self.name = name
        self.description = description
        self.icon = icon

    def fetchDefaultList() :
        file = open("config/defaultconditions.json")
        defaultList = json.load(file)
        file.close()
        return defaultList



class encounter:
    def __init__(self, name, participants, encounterRunning, currentRound) :
        self.name = name
        self.encounterRunning = encounterRunning
        if isinstance(participants, list):
            self.participants = participants
        else:
            print("Participants has to be a list")
        self.currentRound = currentRound

    def addCharacter(self, addMe) :
        # check if name already exist
        for i in self.participants:
            if i.name == addMe:
                duplicateAppendix = "*"
                addMe = " ".join((addMe, duplicateAppendix))
        self.participants.append(character(addMe,0,0,{}))
        print(f"Added {addMe}")

    def removeCharacter(self,removeMe):
        try:
            self.participants.pop(self.getIndexOfParticipantByName(removeMe))
            return
        except:
            print(f"There is no character named {removeMe}")


    def getIndexOfParticipantByName(self,charname):
        i = 1
        while i<=len(self.participants):
            if self.participants[i-1].name.lower() == charname.lower():
                return i-1
            else:
                i+=1
                continue
        return

    def getIndexOfParticipantByInitiative(self,initiative):
        i = 1
        CharactersAtThisInitiative = []
        while i<=len(self.participants):
            if self.participants[i-1].initiative == initiative:
                CharactersAtThisInitiative.append(i-1)
            i+=1
        return CharactersAtThisInitiative

    def battleCommands(self):
        commandNext = {"n","next",""}
        commandExit = {"e", "exit", "q", "quit"}
        commandRemove = {"r", "remove", "d", "del"}
        commandAdd = {"a", "add"}
        commandCondition = {"c", "con", "condition"}
        while True:
            print("What now?")
            battleAction = input().lower()
            if battleAction in commandNext:
                return
            battleAction = shlex.split(battleAction)
            if battleAction[0] in commandExit:
                self.encounterRunning = False
                return
            elif battleAction[0] in commandRemove:
                self.removeCharacter(battleAction[1])
            elif battleAction[0] in commandAdd:
                pass
            elif battleAction[0] in commandCondition:
                charind = self.getIndexOfParticipantByName(battleAction[1])
                if type(charind) == int :
                    conditionToAdd = battleAction[2]
                    # check if condition is already set, delete it
                    if len(self.participants[charind].conditions)>0 and conditionToAdd in self.participants[charind].conditions.keys() :
                        del self.participants[charind].conditions[conditionToAdd]
                    else:
                        self.participants[charind].addCondition(conditionToAdd)
            else:
                print("Make a valid choice! n = next, e = exit, r (charname), c (charname) (condition)")

    def runEncounter(self) :
        # Printing Initative Order
        self.participants = sorted(self.participants, key=lambda x: x.initiative, reverse = True)
        tableInitiativeOrder = Table(title="Initiative is as follows:")

        tableInitiativeOrder.add_column("Name")
        tableInitiativeOrder.add_column("Initiative", justify="right")
        for i in CurrentEncounter.participants:
            tableInitiativeOrder.add_row(i.name, str(i.initiative))
        print(tableInitiativeOrder)
        # Encounter start
        print(Markdown("## Starting Combat"))
        self.encounterRunning = True
        while self.encounterRunning == True:
            announceRound = f"### Round {self.currentRound}"
            print(Markdown(announceRound))

            highestInitiative = self.participants[0].initiative # is always highest because of sorted() earlier
            currentInitiative = highestInitiative

            while currentInitiative >= 1:
                activeCharacterIndex = self.getIndexOfParticipantByInitiative(currentInitiative)
                if len(activeCharacterIndex) != 0:
                    for i in activeCharacterIndex:
                        # showing character name and initiative value
                        print(Markdown(f"#### {self.participants[i].initiative}: Your turn, {self.participants[i].name}"))
                        # fetching all conditions
                        if len(self.participants[i].conditions) > 0 :
                            tableConditions = Table(title="Current Conditions")
                            tableConditions.add_column("Condition")
                            tableConditions.add_column("Description")
                            conditionlist = list(self.participants[i].conditions.values())
                            for i in conditionlist:
                                tableConditions.add_row(i.name, i.description)
                            print(tableConditions)
                    self.battleCommands()
                    self.participants = sorted(self.participants, key=lambda x: x.initiative, reverse = True)
                if self.encounterRunning == False:
                    break
                currentInitiative-= 1
                continue
            self.currentRound+= 1
        

print(Markdown("# DnD Initiative Tracker"))

# Build character list for the encounter

print(Markdown("## Who is playing?"))

choice_defaultCharacters = uitools.question_yn("Would you like to load the default hero characters?")
if choice_defaultCharacters == True :
    Hylwin = character("Hylwin",0,0,{})
    Zayne = character("Zayne",0,0,{})
    CurrentEncounter = encounter("Current Encounter",[Hylwin, Zayne], False, 1)
    for i in CurrentEncounter.participants:
        print(f"Added {i.name}")
else :
    CurrentEncounter = encounter("Current Encounter",[], False)

while True :
  choice_addCharacters = uitools.question_yn("Add a character?")
  if choice_addCharacters == True :
    print("What's the name?")
    CurrentEncounter.addCharacter(input())
    continue
  else :
    print("Alright. These are all the characters:")
    for i in CurrentEncounter.participants:
      print(i.name)
    break

# Getting the initiative order

print(Markdown("## Time to roll initiative"))
for i in CurrentEncounter.participants:
    i.initiative = uitools.question_int(f"Initiative for {i.name}?")

# Combat

CurrentEncounter.runEncounter()


# adding during battle
# adding status