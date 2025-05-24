import random
import json
import os
from datetime import datetime


class Dragon:
    def __init__(self, name, color):

        self.name = name
        self.color = color
        self.health = 80
        self.mood = 80
        self.experience = 0
        self.level = 1
        self.day = 0
        self.skill_used = False  
        self.flame_breath_on = False  
        self.last_time = datetime.now().strftime("%Y-%m-%d")  
        self.max_health = 100
        self.max_mood = 100


    def feed(self):
        self.health = self.health + 10
        if self.health > self.max_health:
            self.health = self.max_health
        self.mood = self.mood + 10
        if self.mood > self.max_mood:
            self.mood = self.max_mood
        print(f"{self.name} ate some food! Health: {self.health}, Mood: {self.mood}")

 
    def train(self):
        if self.mood >= 50:
            self.experience = self.experience + 10
        else:
            self.experience = self.experience + 5
            print("Mood is low! Experience gain is halved. Try feeding or using Dragon Roar.")
        self.mood = self.mood - 10
        if self.mood < 0:
            self.mood = 0
        print(f"{self.name} trained! Experience: {self.experience}, Mood: {self.mood}")

 
    def adventure(self):
        if self.level < 3:
            print(f"{self.name} is too young to adventure! Reach Level 3.")
            return

        events = ["treasure", "food", "toy", "sick", "hunt_fail"]
        if self.flame_breath_on:
            events = ["treasure", "food", "toy"]
            print(f"{self.name}'s Flame Breath makes the adventure safe!")
        event = random.choice(events)
        if event == "treasure":
            self.experience = self.experience + 10
            print(f"{self.name} found treasure! Experience +10")
        elif event == "food":
            self.health = self.health + 10
            if self.health > self.max_health:
                self.health = self.max_health
            print(f"{self.name} found food! Health +10")
        elif event == "toy":
            self.mood = self.mood + 10
            if self.mood > self.max_mood:
                self.mood = self.max_mood
            print(f"{self.name} found a toy! Mood +10")
        elif event == "sick":
            self.health = self.health - 10
            if self.health < 0:
                self.health = 0
            print(f"{self.name} got sick! Health -10")
        elif event == "hunt_fail":
            self.mood = self.mood - 10
            if self.mood < 0:
                self.mood = 0
            print(f"{self.name} failed hunting! Mood -10")


    def use_skill(self):
        if self.skill_used:
            print(f"{self.name} already used a skill today!")
            return
        if self.level == 1:
            print(f"{self.name} has no skills yet!")
        elif self.level == 2:
            self.mood = self.mood + 5
            if self.mood > self.max_mood:
                self.mood = self.max_mood
            print(f"{self.name} used Dragon Roar! Mood +5")
            self.skill_used = True
        elif self.level == 3:
            print(f"{self.name} used Dragon Claw Attack! (No effect, but adventure mode is unlocked)")
            self.skill_used = True
        elif self.level == 4:
            self.flame_breath_on = True
            print(f"{self.name} used Flame Breath! Adventure will be safe.")
            self.skill_used = True


    def update_level(self):
        if self.experience >= 150:
            self.level = 4
        elif self.experience >= 100:
            self.level = 3
        elif self.experience >= 50:
            self.level = 2
        level_names = {1: "Baby Dragon", 2: "Young Dragon", 3: "Youth Dragon", 4: "Ancient Dragon"}
        print(f"{self.name} is a {level_names[self.level]} (Level {self.level})")


    def daily_decay(self, days):
        self.health = self.health - 5 * days
        if self.health < 0:
            self.health = 0
        self.mood = self.mood - 5 * days
        if self.mood < 0:
            self.mood = 0
        self.day = self.day + days
        self.skill_used = False
        self.flame_breath_on = False
        print(f"{days} day(s) passed. Health: {self.health}, Mood: {self.mood}")

    def check_status(self):
        if self.health == 0 or self.mood == 0:
            print(f"{self.name} ran away! You lose!")
            return False
        if self.level == 4 and self.health == 100 and self.mood == 100:
            print(f"Wow! {self.name} is a perfect Ancient Dragon! You win!")
            return False
        return True


    def save(self):
        dragon_data = {
            "name": self.name,
            "color": self.color,
            "health": self.health,
            "mood": self.mood,
            "experience": self.experience,
            "level": self.level,
            "day": self.day,
            "last_time": self.last_time
        }
        with open("dragon_save.json", "w") as file:
            json.dump(dragon_data, file)
        print("Game saved!")


def load_game():
    if not os.path.exists("dragon_save.json"):
        return None
    with open("dragon_save.json", "r") as file:
        data = json.load(file)
        dragon = Dragon(data["name"], data["color"])
        dragon.health = data["health"]
        dragon.mood = data["mood"]
        dragon.experience = data["experience"]
        dragon.level = data["level"]
        dragon.day = data["day"]
        dragon.last_time = data["last_time"]
        return dragon


def calculate_days_passed(last_time):
    last_date = datetime.strptime(last_time, "%Y-%m-%d")
    today = datetime.now()
    days = (today.date() - last_date.date()).days
    if days < 0:
        days = 0
    return days