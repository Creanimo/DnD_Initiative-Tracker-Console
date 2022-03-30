class uitools:
   def question_yn(question) :
    yes = {'yes','y', 'ye', ''}
    no = {'no','n'}
    print(question)
    choice = input().lower()
    if choice in yes:
        return True
    elif choice in no:
        return False
    else:
        print("Please respond with 'yes' or 'no'")
        question_yn(question)

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
        self.participants.append(character(addMe,0,0))

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