import math
import sys

def binomial_probability(n, k, s):
    if k > n:
        return 0

    # Probability of rolling the highest value (e.g., 6) on a die
    p_high = 1 / s
    
    # Probability of not rolling the highest value on a die
    p_low = 1 - p_high
    
    # Binomial coefficient: C(n, k)
    binomial_coeff = math.comb(n, k)
    
    # Binomial probability formula
    probability = binomial_coeff * (p_high ** k) * (p_low ** (n - k))
    
    return probability


def iterate_dict_reverse(d):
    """
    Iterates over the items in a dictionary in reverse order.

    Args:
        d (dict): The dictionary to iterate over.

    Yields:
        tuple: A key-value pair from the dictionary.
    """
    for key in reversed(list(d.keys())):
        yield key, d[key]

class ContestDice:
    t = 1
    n = 6

    def __init__(self, number, targeting = 1):
        self.n = number
        self.t = targeting

    def number(self):
        return self.n

    def targeting(self):
        return self.t

    def effective_sides(self, sides):
        return sides - (self.t - 1)

class OutcomeProbabilities:
    active_player_odds = 0
    opponent_odds = 0
    odds_of_tie = 0

    def tie(self, odds):
        self.odds_of_tie += odds
        return self

    def active_player_wins(self, odds):
        self.active_player_odds += odds
        return self

    def opponent_wins(self, odds):
        self.opponent_odds += odds
        return self

    def combine(self, cell_probability, sub_odds):
        self.tie(cell_probability * sub_odds.odds_of_tie)
        self.active_player_wins(cell_probability * sub_odds.active_player_odds)
        self.opponent_wins(cell_probability * sub_odds.opponent_odds)

    def print(self):
        print("Active Player wins: " + str(self.active_player_odds))
        print("Opponent wins: " + str(self.opponent_odds))
        print("Odds of tie:   " + str(self.odds_of_tie))

class Accumulator:
    rows = []
    header = []
    headerLabel = ""

    def setHeader(self, label, headerData):
        self.headerLabel = label
        self.header = headerData

    def addRow(self, rowNumber, rowData):
        self.rows.append([rowNumber] + rowData)

class PlaintextOutput(Accumulator):
    def print(self):
        print(self.headerLabel + "\t" + "\t".join(self.header))
        for row in self.rows:
            rowHeader = str(row[0])
            rowData = list(map(lambda p: f"{p * 100:.2f}%", row[1:]))
            print(rowHeader + "\t" + "\t".join(rowData))

class HTMLOutput(Accumulator):
    page = None
    style_map = {}

    def __init__(self, page, style_map):
        self.page = page
        self.style_map = style_map

    def print(self):
        page.print_header()
        print("<table>")
        colHeader = list(map(lambda h: self.column_header(h), self.header))
        print("<tr><th></th>\t" + "\t".join(colHeader) + "\t</tr>")
        for row in self.rows:
            rowHeader = str(row[0])
            rowData = list(map(lambda p: self.cell_contents(p), row[1:]))
            print("<tr><th class=opponent-row-header id='d-" + rowHeader + "'>" + rowHeader + "</th>\t" + "\t".join(rowData) + "\t</tr>")
        print("</table>")
        page.print_footer()

    def column_header(self, h):
        return f"<th class=active-player-col-header id='a-{h}'>{h}</th>"

    def cell_contents(self, p):
        style = self.style_lookup(p)
        return "<td class='" + style + "'>" + f"{p * 100:.2f}%" + "</td>"

    def style_lookup(self, p):
        for key, value in iterate_dict_reverse(self.style_map):
            if p >= key:
                return value;
        return ''

class TwoCombatantsPage:
    active_player_targeting = 1
    opponent_targeting = 1
    local = True

    def __init__(self, active_player_targeting, opponent_targeting, local):
        self.active_player_targeting = active_player_targeting
        self.opponent_targeting = opponent_targeting
        self.local = local

    def print_header(self):
        css_path = "../../css"
        print(f"<html><head><link rel='stylesheet' href='{css_path}/page.css'></head><body>")
        print("<a href='https://github.com/g1a/andromedas-edge-odds' class='github-fork-ribbon'data-ribbon='Fork me on GitHub' title='Fork me on GitHub'>Fork me on GitHub</a>")
        print("<div class='contents'>")
        print(f"<div class='horizontal-menu'><h3>Active Player</h3>")
        print("<ul id='active_player-menu'>")
        self.print_menu_contents(self.active_player_targeting, f"VAR-targeting-v-{self.opponent_targeting}-targeting")
        print("</ul></div>")
        print(f"<div class='vertical-menu'><h3>Opponent</h3>")
        print("<ul id='opponent-menu'>")
        self.print_menu_contents(self.opponent_targeting, f"{self.active_player_targeting}-targeting-v-VAR-targeting")
        print("</ul></div>")

    def print_footer(self):
        print("</div></body></html>")

    def print_menu_contents(self, selected_menu, link_template):
        for menu in range(1, 6):
            link_postfix = ""
            if (self.local):
                link_postfix = "/index.html"
            link = '../' + link_template.replace("VAR", str(menu)) + link_postfix
            if menu == selected_menu:
                print("<li class=selected>" + str(menu) + "</li>")
            else:
                print("<li class=unselected><a href='" + link + "'>" + str(menu) + "</a></li>")

def calculate_outcome_probabilities(active_player: ContestDice, opponent: ContestDice, sides: int):
    outcome = OutcomeProbabilities()

    if sides <= 0 or (active_player.number() == 0 and opponent.number() ==0):
        return outcome.tie(1)
    if active_player.number() <= 0:
        return outcome.opponent_wins(1)
    if opponent.number() <= 0:
        return outcome.active_player_wins(1)

    for active_player_highest_count in range(7):
        for opponent_highest_count in range(7):
            active_player_probability = binomial_probability(active_player.number(), active_player_highest_count, active_player.effective_sides(sides))
            opponent_probability = binomial_probability(opponent.number(), opponent_highest_count, opponent.effective_sides(sides))
            cell_probability = active_player_probability * opponent_probability
            if cell_probability > 0:
                if active_player_highest_count > opponent_highest_count:
                    outcome.active_player_wins(cell_probability)
                elif active_player_highest_count < opponent_highest_count:
                    outcome.opponent_wins(cell_probability)
                else:
                    sub_active_player = ContestDice(active_player.number() - active_player_highest_count, active_player.targeting())
                    sub_opponent = ContestDice(opponent.number() - opponent_highest_count, opponent.targeting())
                    sub_odds = calculate_outcome_probabilities(sub_active_player, sub_opponent, sides - 1)
                    outcome.combine(cell_probability, sub_odds)
    
    return outcome

def contest_table_for_targeting(active_player_targeting, opponent_targeting, accumulator):
    accumulator.setHeader("D  \\ A", [str(i) for i in range(1,7)])
    for opponent_dice in range(1, 7):
        row = []
        for active_player_dice in range(1, 7):
            active_player_contest_dice = ContestDice(active_player_dice, active_player_targeting)
            opponent_contest_dice = ContestDice(opponent_dice, opponent_targeting)
            outcome = calculate_outcome_probabilities(active_player_contest_dice, opponent_contest_dice, 6)
            row.append(outcome.active_player_odds)
        accumulator.addRow(opponent_dice, row)

def probability_table(n, s):
    # Create a 7x7 table for possible outcomes (0 to 6 sixes for each player)
    print(f"Probability Table for {n} dice with {s}-sided dice:")
    
    # Print header row (active_player's number of sixes)
    header = ["Opponent / Active"] + [str(i) for i in range(7)]
    print("\t".join(header))
    
    # Calculate and print each row (opponent's number of sixes)
    for opponent_sixes in range(7):
        row = [str(opponent_sixes)]
        for active_player_sixes in range(7):
            # Get the probability of the opponent rolling exactly opponent_sixes
            # and the active_player rolling exactly active_player_sixes
            p_opponent = binomial_probability(n, opponent_sixes, s)
            p_active_player = binomial_probability(n, active_player_sixes, s)
            
            # The joint probability is the product of the two individual probabilities
            joint_probability = p_opponent * p_active_player
            
            # Convert to percentage and append to the row
            row.append(f"{joint_probability * 100:.2f}%")
        
        # Print the row
        print("\t".join(row))


# TODO: Use a cli parser
if (len(sys.argv) < 3):
    print("Usage: python combat-odds.py active_player_targeting opponent_targeting")
    sys.exit(1)

active_player_targeting = int(sys.argv[1])
opponent_targeting = int(sys.argv[2])
local = False

accumulator = PlaintextOutput()
if ((len(sys.argv) >= 4) and (sys.argv[3] == '--html')):
    page = TwoCombatantsPage(active_player_targeting, opponent_targeting, local)
    accumulator = HTMLOutput(page, {0: 'unlikely', 0.2: 'low', 0.45: 'even', 0.55: 'high', 0.8: 'likely'})

contest_table_for_targeting(active_player_targeting, opponent_targeting, accumulator)

accumulator.print()
