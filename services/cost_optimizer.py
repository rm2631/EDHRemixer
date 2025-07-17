class CostOptimizer:
    def __init__(self, cost):
        self.cost = cost
        self.brackets = [
            18,
            36,
            55,
            72,
            90,
            108,
            126,
            144,
            162,
            180,
            198,
            216,
            234,
            396,
            504,
            612,
        ]

    def print_cost_per_card_estimator(self, num_cards: int):
        filtered_brackets = list(filter(lambda x: x >= num_cards, self.brackets))
        if len(filtered_brackets) == 0:
            raise ValueError("Number of cards is too high")
        bracket = filtered_brackets[0]

        return -0.0003 * bracket + 0.5731
