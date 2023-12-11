import json
import random
import sys

# function loading json file
def load_data(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)
    
# function to identify possible answers for the opponent
def find_opponent_arguments(attacks, proponent_args, opponent_answers):
    return {str(attack[0]): arguments[str(attack[0])] 
            for attack in attacks 
            if str(attack[1]) in proponent_args and str(attack[0]) not in opponent_answers}

# function to print out the possible answers for the opponent
def print_dic(dic):
    print("\n")
    for key, value in dic.items():
        print(key, value)

# function to play the game
def play_game(arguments, attacks_relations, proponent_arg):
    proponent_args = {}
    opponent_answers = {}
    
    proponent_args[proponent_arg] = arguments[proponent_arg]

    # playing the game till someone wins
    while True:
        opponent_args = find_opponent_arguments(attacks_relations, proponent_args, opponent_answers)

        if proponent_arg in opponent_answers:
            print("I used an argument that you used before. Congratulations, you won.")
            break
        elif not opponent_args:
            print("Unfortunately, you don't have any arguments left. Therefore, you lost.")
            break

        print_dic(opponent_args)
        opponent_answer = input(f"\nI chose \"{arguments[proponent_arg]}\". Choose one of the above arguments by entering its number: ")
        opponent_answers[opponent_answer] = arguments[opponent_answer]

        for attack in attacks_relations:
            if str(attack[1]) == opponent_answer and str(attack[0]) not in opponent_answers:
                proponent_arg = str(attack[0])
                proponent_args[proponent_arg] = arguments[proponent_arg]
                break
        else:
            print("I don't have any arguments against that. Congratulations, you won.")
            break

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <json_file_name> <proponent_argument_number>")
        sys.exit(1)

    json_file = sys.argv[1]
    proponent_arg = sys.argv[2]

    data = load_data(json_file)
    arguments = data["Arguments"]
    attacks_relations = data["Attack Relations"]

    play_game(arguments, attacks_relations, proponent_arg)
