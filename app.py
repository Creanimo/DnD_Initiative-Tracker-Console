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

