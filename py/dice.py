import random 
import time 


def roll_dice(num_dice=1, num_sides=20):
    return [random.randint(1, num_sides) for _ in range(num_dice)]


def roll_d20():
    return random.randint(1, 20)


def roll_attack():
    roll = roll_d20()
    multiplier = 1.1  # (proficiency damage multiplier)
    
    if roll == 1:
        # Critical fail - miss and take self damage
        return {
            'roll': roll,
            'result_type': 'critical_fail',
            'damage_dice': 1,
            'damage_sides': 4,
            'multiplier': 0,  # No damage to enemy
            'message': 'Critical Fail!'
        }
    elif roll == 20 or roll == 19:
        # Critical hit! (keeping original logic where 19 and 20 are crits)
        return {
            'roll': roll,
            'result_type': 'critical_hit',
            'damage_dice': 3,
            'damage_sides': 4,
            'multiplier': multiplier,
            'message': 'Critical Hit!'
        }
    elif roll >= 15 and roll < 19:
        # Good hit
        return {
            'roll': roll,
            'result_type': 'good_hit',
            'damage_dice': 2,
            'damage_sides': 4,
            'multiplier': multiplier,
            'message': 'Good Roll!'
        }
    elif roll > 1 and roll < 15:
        # Normal hit
        return {
            'roll': roll,
            'result_type': 'normal_hit',
            'damage_dice': 1,
            'damage_sides': 4,
            'multiplier': multiplier,
            'message': 'Normal Roll.'
        }
    else:
        # Roll 19: also a hit
        return {
            'roll': roll,
            'result_type': 'good_hit',
            'damage_dice': 2,
            'damage_sides': 4,
            'multiplier': multiplier,
            'message': 'Good Roll!'
        }


def calculate_damage(attack_result, base_attack=0):
    if attack_result['multiplier'] == 0:
        return 0
    
    dice_damage = sum(roll_dice(attack_result['damage_dice'], attack_result['damage_sides']))
    total = int((dice_damage + base_attack) * attack_result['multiplier'])
    return max(1, total)


# Legacy function for backwards compatibility
def generate_random_dice_rolls(num_rolls, num_sides=20):
    return roll_dice(num_rolls, num_sides)


# Example usage:
def when_life_gives_you_lemons():  # i dont care if you question the name of this function i love it and you need to deal with it. insperational
    multiplier = 1.1  # (proficiency damage multiplier)
    
    rolls = roll_dice(1, 20)
    print("Random Dice Rolls:", rolls)
    
    if rolls[0] == 19 or rolls[0] == 20:
        time.sleep(1)
        rolls2 = roll_dice(6, 6)
        print("Critical Hit!") 
        time.sleep(1)
        print("Rolls for bonus damage:", rolls2)
        print("Total:", sum(rolls2))
        print("Total Damage with Critical Hit:", sum(rolls2) * multiplier)

    if rolls[0] == 1:
        print("Critical fail!") 
        rolls1 = roll_dice(2, 6)
        print("Rolls for fail Penalty:", rolls1)
        print("Total fail Penalty:", sum(rolls1))

    if rolls[0] > 1 and rolls[0] < 15:
        print("Normal Roll.")  
        time.sleep(1)
        rolls3 = roll_dice(3, 6)
        time.sleep(1)
        print("Rolls for damage:", rolls3)
        time.sleep(1)
        print("Total damage:", sum(rolls3))

    if rolls[0] >= 15 and rolls[0] < 19:
        print("Good Roll!") 
        rolls4 = roll_dice(4, 6)
        print("Rolls for damage:", rolls4)
        print("Total damage:", sum(rolls4))


if __name__ == "__main__":
    when_life_gives_you_lemons()
