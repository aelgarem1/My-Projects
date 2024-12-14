import random as r

while True:

    you_win = []
    user_score = 0
    computer_score = 0
    for round in range(3):
        choices = [1,2,3]
  
        print("Enter a choice: \n 1. Rock \n 2. paper \n 3. scissor \n")  

        user_choice = int(input('Your Choice(1,2,3): '))
        while user_choice.alpha():
                print('Please enter a valid number between 1 and 3')
                user_choice = int(input('Your Choice(1,2,3): '))
        while user_choice > 3 or user_choice <= 0:
                print('Please enter a number between 1 and 3')
                user_choice = int(input('Your Choice(1,2,3): '))
            
        
        choices.remove(user_choice)
        user_choice = int(input('Your Choice(1,2,3): '))
        computer_choice = r.choice(choices)
        if (computer_choice == 1 and user_choice == 2) or (computer_choice == 1 and user_choice == 3) or (computer_choice == 2 and user_choice == 3):
            print('YOU WIN')
            user_score +=1
            you_win.append(1)
            print(f"ROUND \'{round + 1}\' SCORE:\n USER {user_score} : ROBOT {computer_score}")
        else:
            print('LOSER!')
            #print(computer_choice)
            computer_score += 1
            print(f"ROUND \'{round + 1}\' SCORE:\n USER {user_score} : ROBOT {computer_score}")
    if user_score > computer_score:
        print(f'Winner in a total of {len(you_win)} out of 3 rounds')
    elif user_score == computer_score:
        print('Tie')
    else:
        print('Try harder next time')
    answer = input('Do you wish to play again? (y/n)')
    while answer.lower() not in ('y', 'n'):
        answer = input('Do you wish to play again? (y/n)')
    if answer.lower() == 'n':
        print('BYE!')
        break


