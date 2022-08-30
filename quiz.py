import json, sys, logging
import numpy as np


def try_to_enable_debug_mode ():
    # Check if debug mode is on
    if (sys.argv[2]=='-d'):
            logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')
    else:
        logging.basicConfig(level=logging.ERROR, format='%(asctime)s:%(levelname)s:%(message)s')


def open_db (db_json):
# Open db_json file and creating variable data from db
    with open(f"{db_json}","r") as f:
        data = json.load(f)
    return data


def quiz_questions (number_of_questions=7, db_of_questions=11):
# Create set of question numbers in variable list_of_questions based on number_of_question defining length of created list and db_of_questions defining numbers of all question in data base
    list_of_questions = []
    # Reapete filling list with random numbers of list_of_question until reaches number_of_questions
    while len(list_of_questions)!=number_of_questions:
        question_mark = np.random.randint(0,db_of_questions)
        if (list_of_questions.count(question_mark)==0):
            list_of_questions.append(question_mark)
            logging.debug(f"Random number that's append to list {question_mark}")
    logging.debug(f'Random list {list_of_questions}')
    # Return list of random numbers of questions
    return list_of_questions


def handle_quiz_game ():
# Main quiz game app
    try:
        # Create variable data_base by loading data from json db
        data_base = open_db(sys.argv[1])['quiz']
    except:
        logging.error("File sys.argv[1] doesn't exist")
        print("File sys.argv[1] doesn't exist")
        quit()
    # Create list of questions
    questions = quiz_questions()
    logging.debug(f'The list of numbers of questions {questions}')
    score = 0
    logging.debug(f'Starting score {score}')
    max_score = len(questions)
    logging.debug(f'Max score {max_score}')
    while(questions):
    # Contiunue to display quiz questions untli list is empty 
        for question in data_base:
            # Check if json db is correct
            try:
                # Set current question from last number from list questions
                current_question = question['q'+str(questions[-1])]
                logging.debug(f'Current number of question{current_question}')
                # Create random list to display answers in random order 
                answers =  quiz_questions(len(current_question['option']),len(current_question['option']))
                logging.debug(f'List of order to display option to answer {answers}')
                print(current_question['question'])
                logging.debug(f"Correct answer {current_question['answer']}")
                # Print all possible options
                for idx, option in enumerate(answers, start=1):
                    print(f'{idx}: ', current_question['option'][option])
                # Pick answer from input
                answer = input("Type numer of your answer or type 'r' for reload or 'q' for quiting game : ")
                logging.debug(f'Input value: {answer}')
                try:
                # Handling error input if is not a number or it's float number or negative 
                    logging.debug(f"The boolean of answer is {current_question['option'][answers[abs(int(answer))-1]]==current_question['answer']}")
                    if(current_question['option'][answers[abs(int(answer))-1]]==current_question['answer']):
                        score+=1
                        print(f'Correct your score is: {score}')
                    else:
                        print(f'Incorrect your score is: {score}')
                except:
                    logging.debug(f"Switching to option modes to reload or quit, the values of reload is: {answer == 'r'} and quit is: {answer == 'q'}")
                    # Option to quit or realod game durring game sesion
                    if (answer == 'q'):
                        print('Quiting game')
                        quit()
                    elif(answer == 'r'):
                        print('Reloading game')
                        handle_quiz_game()
                    else:
                        print(f'Incorrect your score is: {score}')
            except TypeError:
                # Throw message if json db is not correct formated and exiting game
                print('json file is incorectly formated')
                logging.error('json file is incorectly formated')
                quit()
        questions.pop()
        # Delete last element in the question list
        logging.debug(f'Current list of questions {questions} and lenght of list is {len(questions)}')
    print(f'End of game your score is {score} and max score was {max_score}. You achieved ' + str(round(score/max_score*100,2))+" %")
    # Print result of quiz game
    while (True):
    # Option to reload game or quit
        end = input("Do you wanna play more? type 'r' for reload or 'q' to exit game ")
        logging.debug(f"Value of input {end}, switching to option modes to reload or quit, the values of reload is: {end == 'r'} and quit is: {end == 'q'}")
        if(end == 'r'):
            print('Reloading game')
            handle_quiz_game()
        elif(end == 'q'):
            print('Quiting game')
            quit()
        print('Incorect value please try again')

def main():
    # Checks for debug mode and starts game
    if((len(sys.argv)==3)):
        try_to_enable_debug_mode()
    handle_quiz_game()


if __name__=='__main__':
    main()