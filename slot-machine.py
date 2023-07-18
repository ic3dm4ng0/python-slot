import requests
import time
import os
from random import randint, uniform

API_KEY = ""
VALUE_RANGE = (0, 16)
ROW_SIZE = 7
ROW_COUNT = 5
URL = "https://api.random.org/json-rpc/2/invoke"
HEADERS = {"Content-Type": "application/json"}

MAX_BET = 100
MIN_BET = 0.1

class Generator:
    TICKETS = {
        (0, 0): "E",
        (1, 6): "A",
        (7, 11): "B",
        (12, 14): "C",
        (15, 16): "D"
    }

    COLORS = {
        "E": "\033[34m",  # Blue
        "A": "\033[37m",  # White
        "B": "\033[91m",  # Orange
        "C": "\033[33m",  # Yellow
        "D": "\033[35m",  # Magenta
    }

    @staticmethod
    def numberToTicket(number: int) -> str:
        for key, ticket in Generator.TICKETS.items():
            if key[0] <= number <= key[1]:
                return ticket

    @staticmethod
    def ticketToColor(ticket: str) -> str:
        return Generator.COLORS.get(ticket, "")

    @staticmethod
    def generateNumberRow(isProp: bool) -> str:
        row = ""
        if isProp:
            for _ in range(ROW_SIZE):
                number = Generator.numberToTicket(randint(*VALUE_RANGE))
                row += str(number)
        else:
            payload = {
                "jsonrpc": "2.0",
                "method": "generateIntegers",
                "params": {
                    "apiKey": API_KEY,
                    "n": ROW_SIZE,
                    "min": VALUE_RANGE[0],
                    "max": VALUE_RANGE[1],
                    "replacement": True
                },
                "id": 1
            }
            response = requests.post(URL, headers=HEADERS, json=payload).json()
            randomNumbers = response["result"]["random"]["data"]

            for number in randomNumbers:
                row += str(Generator.numberToTicket(number))

        return row

class SlotMachine:
    PAYOUTS = {
        "A": 0.9,
        "B": 1.185,
        "C": 2.285,
        "D": 3.735,
        "E": 7.485
    }
    MIN_LETTERS = {
        "A": 6,
        "B": 5,
        "C": 4,
        "D": 3,
        "E": 2
    }

    def __init__(self):
        self.balance = 100
        self.oldBalance = self.balance
        self.allTimeHigh = self.balance
        self.allTimeLow = self.balance
        self.minDelay = 0.1
        self.animUpdateRange = (25, 40)
        self.maxDelay = 2

    def generateDisplaySlotAnimation(self) -> str:
        rows = [Generator.generateNumberRow(True) for _ in range(ROW_COUNT)]
        winner = Generator.generateNumberRow(False)
        currentDelay = self.minDelay
        updates = randint(self.animUpdateRange[0], self.animUpdateRange[1])

        for spinCount in range(1, updates + 1):
            rowCount = 0
            separator = "—" * (ROW_SIZE * 4 - 1)

            for i, row in enumerate(rows):
                for j, char in enumerate(row, start=1):
                    separatorMarker = (f"\033[32m <-\033[0m" if i == 2 and j == ROW_SIZE else " | ")
                    print(Generator.ticketToColor(char) + char + "\033[0m", end=separatorMarker)

                rowCount += 1
                print()
                print(separator if rowCount != 5 else " ")

            if spinCount >= updates - randint(8, 12):
                currentDelay *= uniform(1.15, 1.3)
            currentDelay = min(self.maxDelay * uniform(0.85, 1), currentDelay)

            time.sleep(currentDelay)
            if spinCount < updates:
                os.system("cls")

            rows = [Generator.generateNumberRow(True) if spinCount != updates - 3 else winner] + rows[:-1]

        return winner

    def countTickets(self, tickets: str) -> dict:
        return {
            ticket: tickets.count(ticket)
            for ticket in "ABCDE"
        }
    
    def calculatePayout(self, ticketCounts: dict, dollarAmount: float) -> float:
        return sum(
            (self.PAYOUTS[key] * dollarAmount) * ticketCounts[key]
            for key in ticketCounts
            if ticketCounts[key] >= self.MIN_LETTERS[key]
        )

slotMachine = SlotMachine()

class Menu:
    @staticmethod
    def displayMenu():
        os.system("cls")
        print("[1] Play Slot")
        print("[2] How to Play")
        print("[3] Paytable")
        print()
        print(f"[4] Cash out ${slotMachine.balance}")
        print()
        return int(input("Enter what you would like to do: "))
    
    @staticmethod
    def displayPaytable():
        os.system("cls")
        print("- A: Minimum amount is 6. $0.9:1 per appearance.")
        print("- B: Minimum amount is 5. $1.185:1 per appearance.")
        print("- C: Minimum amount is 4. $2.285:1 per appearance.")
        print("- D: Minimum amount is 3. $3.735:1 per appearance.")
        print("- E: Minimum amount is 2. $7.485:1 per appearance.")
        print()
        input("Press Enter to continue.")
        os.system("cls")
    
    @staticmethod
    def displayHowToPlay():
        os.system("cls")
        print("- Before each spin, you enter a bet amount (this will control how much you earn)")
        print("- A series of randomly generated rows appear in the spin gradually slowing down until you land on the final row")
        print("- Note that the rows aside from the winner are merely props and you were never going to win them in the first place")
        print("- If you hit the minimum amount of a certain letter (according to the Paytable), you win!")
        print("- The amount you win is also dependent on the Paytable.")
        print()
        input("Press Enter to continue.")
        os.system("cls")
    
    @staticmethod
    def cashout():
        print(f"Cashed out ${slotMachine.balance}")
        print()
        print(f"Profit/loss: {'(+$' if slotMachine.balance - slotMachine.oldBalance > 0 else '(-'}{abs(slotMachine.balance - slotMachine.oldBalance)})")
        print(f"ALL TIME HIGH: ${slotMachine.allTimeHigh}")
        print(f"all time low: ${slotMachine.allTimeLow}")
        print()
        input("Press enter to continue ")
        exit(0)

def main():
    slotMachine.allTimeHigh = slotMachine.balance
    slotMachine.allTimeLow = slotMachine.balance

    while True:
        inputValue = Menu.displayMenu()
        os.system("cls")

        if inputValue == 1:
            print(f"Balance: ${slotMachine.balance}")
            slotMachine.oldBalance = slotMachine.balance
            bet = float(input("How much money would you like to bet on this spin? $"))
            if bet > slotMachine.balance or bet > MAX_BET or bet < MIN_BET:
                print(f"Cannot bet more than balance or ${MAX_BET} OR less than ${MIN_BET}.")
                input("Press Enter to continue ")
                os.system("cls")
                continue

            os.system("cls")
            winningRow = slotMachine.generateDisplaySlotAnimation()
            winnings = slotMachine.calculatePayout(slotMachine.countTickets(winningRow), bet)

            slotMachine.balance -= bet

            if winnings != 0:
                slotMachine.balance += winnings
                print(f"New balance: ${slotMachine.balance} {'(+$' if slotMachine.balance - slotMachine.oldBalance > 0 else '(-'}{abs(slotMachine.balance - slotMachine.oldBalance)})")

            if slotMachine.balance > slotMachine.allTimeHigh:
                slotMachine.allTimeHigh = slotMachine.balance
            elif slotMachine.balance < slotMachine.allTimeLow:
                slotMachine.allTimeLow = slotMachine.balance
            
            print()
            input("Press Enter to continue ")
            os.system("cls")
        elif inputValue == 2:
            Menu.displayHowToPlay()
        elif inputValue == 3:
            Menu.displayPaytable()
        elif inputValue == 4:
            Menu.cashout()
        if slotMachine.balance == 0:
            Menu.cashout()
            input("Press Enter to continue ")
            exit(0)

if __name__ == "__main__":
    main()
