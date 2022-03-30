import operator

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
    def __init__(self, name, participants) :
        self.name = name
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

    def battleCommands():
        commandNext = {"n","next",""}
        commandExit = {"e", "exit", "q", "quit"}
        while True:
            print("What now?")
            battleAction = input().lower()
            if battleAction in commandNext:
                return
            elif battleAction in commandExit:
                return "exitEncounter"
            else:
                print("Make a valid choice! n = next, e = exit")
        


# Build character list for the encounter

choice_defaultCharacters = uitools.question_yn("Would you like to load the default hero characters?")
if choice_defaultCharacters == True :
    Hylwin = character("Hylwin",0,0)
    Zayne = character("Zayne",0,0)
    CurrentEncounter = encounter("Current Encounter",[Hylwin, Zayne])
    for i in CurrentEncounter.participants:
        print(f"Added {i.name}")
else :
    CurrentEncounter = encounter("Current Encounter",[])

while True :
  choice_addCharacters = uitools.question_yn("Add a character?")
  print(choice_addCharacters)
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

print("Time to roll initiative")
for i in CurrentEncounter.participants:
    i.initiative = uitools.question_int(f"Initiative for {i.name}?")
print("Initiative is as follows:")
sortedInitiative = sorted(CurrentEncounter.participants, key=lambda x: x.initiative, reverse = True)
for i in sortedInitiative:
    print(f"{i.name} - {i.initiative}")

# Combat

print("Starting Combat")
round = 0
while True:
    round+= 1
    print(f"Round {round}")
    for i in sortedInitiative:
        ExitAction = False
        print(f"Your turn, {i.name}")
        collectCommand = ""
        collectCommand = encounter.battleCommands()
        if collectCommand ==  "exitEncounter":
            break
    if collectCommand ==  "exitEncounter":
        break