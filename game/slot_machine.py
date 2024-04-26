import random as rd

def run(money):
    slotMachine = [0, 0, 0]
    fruits = ["🍍", "🍊", "🍋", "🍌", "🍉", "🍇", "🍓", "🍈", "🍒", "🥝", "🍎", "💰"]
    sums = 0
    Notbad = 0
    Lucky = 0
    Jackpot = 0
    while money:
        print("remain number: %d" % (money))
        money -= 1
        for i, _ in enumerate(slotMachine):
            fruit = rd.choice(fruits)
            slotMachine[i] = fruit
        
        print(*slotMachine)

        for fruit in slotMachine:
            fruitCount = slotMachine.count(fruit)
            bankrollCount = slotMachine.count("💰")
            if fruitCount == 2:
                print("Not bad +3.5$")
                Notbad += 3.5
                sums += 3.5
                break
            elif bankrollCount == 3:
                print("Jackpot! +100$")
                Jackpot += 100
                sums += 100
                break
            elif fruitCount == 3:
                print("Lucky! +20$")
                Lucky += 20
                sums += 20
                break
    
    print("\nNot bad: +{0}$\nLucky: +{1}$\nJackpot: +{2}$".format(Notbad, Lucky, Jackpot))
    return str(sums) + "$"

print("1 game = 1$")
print(run(int(input("input money: "))))