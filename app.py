import operator
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
    def __init__(self, name, initiative, armorClass) :
        self.name = name
        self.initiative = initiative
        self.armorClass = armorClass

class encounter:
    def __init__(self, name, participants, encounterRunning) :
        self.name = name
        self.encounterRunning = encounterRunning
        if isinstance(participants, list):
            self.participants = participants
        else:
            print("Participants has to be a list")

    def addCharacter(self, addMe) :
        # check if name already exist
        for i in self.participants:
            if i.name == addMe:
                duplicateAppendix = "*"
                addMe = " ".join((addMe, duplicateAppendix))
        self.participants.append(character(addMe,0,0))
        print(f"Added {addMe}")

    def removeCharacter(self,removeMe):
        i = 1
        while i<=len(self.participants):
            if self.participants[i-1].name.lower() == removeMe.lower():
                self.participants.pop(i-1)
            else:
                i+=1
                continue


    def battleCommands(self):
        commandNext = {"n","next",""}
        commandExit = {"e", "exit", "q", "quit"}
        commandRemove = {"r", "remove", "d", "del"}
        commandAdd = {"a", "add"}
        while True:
            print("What now?")
            battleAction = input().lower()
            if battleAction in commandNext:
                return
            battleAction = battleAction.split()
            if battleAction[0] in commandExit:
                self.encounterRunning = False
                return
            elif battleAction[0] in commandRemove and len(battleAction) == 2 :
                self.removeCharacter(battleAction[1])
            elif battleAction[0] in commandAdd and len(battleAction) == 2:
                pass
            else:
                print("Make a valid choice! n = next, e = exit, r (charname)")
        

print(Markdown("# DnD Initiative Tracker"))

# Build character list for the encounter

print(Markdown("## Who is playing?"))

choice_defaultCharacters = uitools.question_yn("Would you like to load the default hero characters?")
if choice_defaultCharacters == True :
    Hylwin = character("Hylwin",0,0)
    Zayne = character("Zayne",0,0)
    CurrentEncounter = encounter("Current Encounter",[Hylwin, Zayne], False)
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

CurrentEncounter.participants = sorted(CurrentEncounter.participants, key=lambda x: x.initiative, reverse = True)
tableInitiativeOrder = Table(title="Initiative is as follows:")

tableInitiativeOrder.add_column("Name")
tableInitiativeOrder.add_column("Initiative", justify="right")
for i in CurrentEncounter.participants:
    tableInitiativeOrder.add_row(i.name, str(i.initiative))
print(tableInitiativeOrder)

# Combat

print(Markdown("## Starting Combat"))
round = 0
CurrentEncounter.encounterRunning = True
while CurrentEncounter.encounterRunning == True:
    round+= 1
    announceRound = f"### Round {round}" 
    print(Markdown(announceRound))
    for i in CurrentEncounter.participants:
        print(Markdown(f"#### Your turn, {i.name}"))
        CurrentEncounter.battleCommands()
        if CurrentEncounter.encounterRunning == False:
            break


# adding during battle
# adding status