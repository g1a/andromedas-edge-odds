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
    attacker_odds = 0
    defender_odds = 0
    odds_of_tie = 0

    def tie(self, odds):
        self.odds_of_tie += odds
        return self

    def attacker_wins(self, odds):
        self.attacker_odds += odds
        return self

    def defender_wins(self, odds):
        self.defender_odds += odds
        return self

    def combine(self, cell_probability, sub_odds):
        self.tie(cell_probability * sub_odds.odds_of_tie)
        self.attacker_wins(cell_probability * sub_odds.attacker_odds)
        self.defender_wins(cell_probability * sub_odds.defender_odds)

    def print(self):
        print("Attacker wins: " + str(self.attacker_odds))
        print("Defender wins: " + str(self.defender_odds))
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
            print("<tr><th class=defender-row-header id='d-" + rowHeader + "'>" + rowHeader + "</th>\t" + "\t".join(rowData) + "\t</tr>")
        print("</table>")
        page.print_footer()

    def column_header(self, h):
        return f"<th class=attacker-col-header id='a-{h}'>{h}</th>"

    def cell_contents(self, p):
        style = self.style_lookup(p)
        return "<td class='" + style + "'>" + f"{p * 100:.2f}%" + "</td>"

    def style_lookup(self, p):
        for key, value in iterate_dict_reverse(self.style_map):
            if p >= key:
                return value;
        return ''

class TwoCombatantsPage:
    attacker_targeting = 1
    defender_targeting = 1
    local = True

    def __init__(self, attacker_targeting, defender_targeting, local):
        self.attacker_targeting = attacker_targeting
        self.defender_targeting = defender_targeting
        self.local = local

    def print_header(self):
        css_path = "../../css"
        print(f"<html><head><link rel='stylesheet' href='{css_path}/page.css'></head><body>")
        print("<a href='https://github.com/g1a/andromedas-edge-odds' class='github-fork-ribbon'data-ribbon='Fork me on GitHub' title='Fork me on GitHub'>Fork me on GitHub</a>")
        print("<div class='contents'>")
        print(f"<div class='horizontal-menu'><h3>Attacker</h3>")
        print("<ul id='attacker-menu'>")
        self.print_menu_contents(self.attacker_targeting, f"VAR-targeting-v-{self.defender_targeting}-targeting")
        print("</ul></div>")
        print(f"<div class='vertical-menu'><h3>Defender</h3>")
        print("<ul id='defender-menu'>")
        self.print_menu_contents(self.defender_targeting, f"{self.attacker_targeting}-targeting-v-VAR-targeting")
        print("</ul></div>")

    def print_footer(self):
        print("</div></body></html>")

    def print_menu_contents(self, selected_menu, link_template):
        for menu in range(1, 6):
            link_postfix = ""
            if (self.local):
                link_postfix = "/index.html"
            link = link_template.replace("VAR", str(menu)) + link_postfix
            if menu == selected_menu:
                print("<li class=selected>" + str(menu) + "</li>")
            else:
                print("<li class=unselected><a href='" + link + "'>" + str(menu) + "</a></li>")

def calculate_outcome_probabilities(attacker: ContestDice, defender: ContestDice, sides: int):
    outcome = OutcomeProbabilities()

    if sides <= 0 or (attacker.number() == 0 and defender.number() ==0):
        return outcome.tie(1)
    if attacker.number() <= 0:
        return outcome.defender_wins(1)
    if defender.number() <= 0:
        return outcome.attacker_wins(1)

    for attacker_highest_count in range(7):
        for defender_highest_count in range(7):
            attacker_probability = binomial_probability(attacker.number(), attacker_highest_count, attacker.effective_sides(sides))
            defender_probability = binomial_probability(defender.number(), defender_highest_count, defender.effective_sides(sides))
            cell_probability = attacker_probability * defender_probability
            if cell_probability > 0:
                if attacker_highest_count > defender_highest_count:
                    outcome.attacker_wins(cell_probability)
                elif attacker_highest_count < defender_highest_count:
                    outcome.defender_wins(cell_probability)
                else:
                    sub_attacker = ContestDice(attacker.number() - attacker_highest_count, attacker.targeting())
                    sub_defender = ContestDice(defender.number() - defender_highest_count, defender.targeting())
                    sub_odds = calculate_outcome_probabilities(sub_attacker, sub_defender, sides - 1)
                    outcome.combine(cell_probability, sub_odds)
    
    return outcome

def contest_table_for_targeting(attacker_targeting, defender_targeting, accumulator):
    accumulator.setHeader("D  \\ A", [str(i) for i in range(1,7)])
    for defender_dice in range(1, 7):
        row = []
        for attacker_dice in range(1, 7):
            attacker_contest_dice = ContestDice(attacker_dice, attacker_targeting)
            defender_contest_dice = ContestDice(defender_dice, defender_targeting)
            outcome = calculate_outcome_probabilities(attacker_contest_dice, defender_contest_dice, 6)
            row.append(outcome.attacker_odds)
        accumulator.addRow(defender_dice, row)

def probability_table(n, s):
    # Create a 7x7 table for possible outcomes (0 to 6 sixes for each player)
    print(f"Probability Table for {n} dice with {s}-sided dice:")
    
    # Print header row (attacker's number of sixes)
    header = ["Defender / Attacker"] + [str(i) for i in range(7)]
    print("\t".join(header))
    
    # Calculate and print each row (defender's number of sixes)
    for defender_sixes in range(7):
        row = [str(defender_sixes)]
        for attacker_sixes in range(7):
            # Get the probability of the defender rolling exactly defender_sixes
            # and the attacker rolling exactly attacker_sixes
            p_defender = binomial_probability(n, defender_sixes, s)
            p_attacker = binomial_probability(n, attacker_sixes, s)
            
            # The joint probability is the product of the two individual probabilities
            joint_probability = p_defender * p_attacker
            
            # Convert to percentage and append to the row
            row.append(f"{joint_probability * 100:.2f}%")
        
        # Print the row
        print("\t".join(row))


# TODO: Use a cli parser
if (len(sys.argv) < 3):
    print("Usage: python combat-odds.py attacker_targeting defender_targeting")
    sys.exit(1)

attacker_targeting = int(sys.argv[1])
defender_targeting = int(sys.argv[2])
local = False

accumulator = PlaintextOutput()
if ((len(sys.argv) >= 4) and (sys.argv[3] == '--html')):
    page = TwoCombatantsPage(attacker_targeting, defender_targeting, local)
    accumulator = HTMLOutput(page, {0: 'unlikely', 0.2: 'low', 0.45: 'even', 0.55: 'high', 0.8: 'likely'})

contest_table_for_targeting(attacker_targeting, defender_targeting, accumulator)

accumulator.print()
