from dragon import Dragon, load_game, calculate_days_passed
import os
from datetime import datetime


def main():
    print("Welcome to the Dragon Pet Game!")
    

    dragon = load_game()
    if dragon is None:

        name = input("What is your dragon's name? ")
        color = input("What color is your dragon (e.g., Red, Blue)? ")
        dragon = Dragon(name, color)
    else:

        print(f"Welcome back to {dragon.name} (Color: {dragon.color})!")
        days_passed = calculate_days_passed(dragon.last_time)
        if days_passed > 0:
            dragon.daily_decay(days_passed)
            if not dragon.check_status():
                if os.path.exists("dragon_save.json"):
                    os.remove("dragon_save.json")
                return


    while True:
        print(f"\n=== Day {dragon.day} (Today: {datetime.now().strftime('%Y-%m-%d')}) ===")
        print(f"{dragon.name}'s Info: Health: {dragon.health}, Mood: {dragon.mood}, Experience: {dragon.experience}, Level: {dragon.level}")
        print("What do you want to do?")
        print("1. Feed")
        print("2. Train")
        print("3. Adventure")
        print("4. Use Skill")
        print("5. Save and Quit")
        choice = input("Enter a number (1-5): ")


        if choice == "1":
            dragon.feed()
        elif choice == "2":
            dragon.train()
        elif choice == "3":
            dragon.adventure()
        elif choice == "4":
            dragon.use_skill()
        elif choice == "5":
            dragon.last_time = datetime.now().strftime("%Y-%m-%d")
            dragon.save()
            print("Game saved! See you next time!")
            break
        else:
            print("Please pick a number between 1 and 5!")
            continue


        dragon.update_level()
        if not dragon.check_status():
            if os.path.exists("dragon_save.json"):
                os.remove("dragon_save.json")
            break
        dragon.last_time = datetime.now().strftime("%Y-%m-%d")
        dragon.save()


if __name__ == "__main__":
    main()