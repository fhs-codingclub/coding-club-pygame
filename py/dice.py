import random 
import time 
def generate_random_dice_rolls(num_rolls, num_sides=20):
    """Generate a list of random dice rolls.

    Args:
        num_rolls (int): The number of dice rolls to generate.
        num_sides (int): The number of sides on each die.

    Returns:
        list: A list containing the results of the dice rolls.
    """

    return [random.randint(1, num_sides) for _ in range(num_rolls)]
# Example usage:
def when_life_gives_you_lemons(): # i dont care if you question the name of this function i love it and you need to deal with it.
    multiplier = 1.1 # (profecitcy damage multiplier)
    if __name__ == "__main__":
     rolls = generate_random_dice_rolls(1, 20)
    print("Random Dice Rolls:", rolls)
    if rolls[0] == 10 or rolls[0] == 20:
        time.sleep(1)
        rolls2 = generate_random_dice_rolls(6, 6)
        print("Critical Hit!") 
        time.sleep(1)
        print("Rolls for bonus damage:", rolls2)
        print("Total:", sum(rolls2))
        print("Total Damage with Critical Hit:", sum(rolls2) * multiplier)

    if rolls[0] == 1:
        print("Critical fail!") 
        rolls1 = generate_random_dice_rolls(2, 6)
        print("Rolls for fail Penalty:", rolls1)
        print("Total fail Penalty:", sum(rolls1))

    if rolls[0] > 1 and rolls[0] < 15:
        print("Normal Roll.")  
        time.sleep(1)
        rolls3 = generate_random_dice_rolls(3, 6)
        time.sleep(1)
        print("Rolls for damage:", rolls3)
        time.sleep(1)
        print("Total damage:", sum(rolls3))

    if rolls[0] >= 15 and rolls[0] < 19:
        print("Good Roll!") 
        rolls4 = generate_random_dice_rolls(4, 6)
        print("Rolls for damage:", rolls4)
        print("Total damage:", sum(rolls4))

when_life_gives_you_lemons()