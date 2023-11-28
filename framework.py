import json

class ArgumentationGame:
    def __init__(self, json_file, claimed_argument):
        self.load_json(json_file)
        self.claimed_argument = claimed_argument
        self.proponent_arguments = [claimed_argument]
        self.opponent_arguments = []
        self.current_round = 0

    def load_json(self, json_file):
        with open(json_file, 'r') as file:
            data = json.load(file)
            self.arguments = data["Arguments"]
            self.attack_relations = data["Attack Relations"]

    def play_round(self):
        print(f"Round {self.current_round}:")
        self.current_round += 1

        # Proponent's turn
        proponent_move = self.proponent_arguments[-1]
        print(f"Proponent's argument: {self.arguments[proponent_move]}")

        # Get the attacks on the proponent's move
        attacks = [pair[1] for pair in self.attack_relations if pair[0] == proponent_move]

        if not attacks:
            print("Proponent cannot make a move. Opponent wins!")
            return False

        # Opponent's turn
        print("Options for Opponent:")
        for idx, attack in enumerate(attacks):
            print(f"{idx}: {self.arguments[attack]}")

        choice = int(input("Choose your attack: "))
        opponent_move = attacks[choice]

        # Check if the opponent move was previously used by the proponent
        if opponent_move in self.proponent_arguments:
            print("Opponent wins! Proponent contradicted itself.")
            return False

        self.opponent_arguments.append(opponent_move)

        # Proponent's response
        response_attacks = [pair[1] for pair in self.attack_relations if pair[0] == opponent_move]
        if response_attacks:
            self.proponent_arguments.append(response_attacks[0])  # Simple strategy for proponent
        else:
            print("Proponent has no moves left. Opponent wins!")
            return False

        # Check if the proponent contradicts itself or cannot move
        if self.proponent_arguments[-1] in self.opponent_arguments:
            print("Proponent used an argument previously used by Opponent. Opponent wins!")
            return False

        return True

    def start_game(self):
        print("Starting the Argumentation Game...")
        while self.play_round():
            pass


# Example usage
game = ArgumentationGame('argumentation_framework.json', '0')  # Assuming '0' is the claimed argument
game.start_game()
