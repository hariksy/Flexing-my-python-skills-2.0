#Arambikkalaangala!?

import os
from datetime import datetime

# Constants
MAX_SESSION_HOURS = 2  
BREAK_MINUTES = 15  
DEFAULT_BREAK_COUNT = 4  
MINUTES_IN_HOUR = 60  

# Function to calculate dynamic revision time
def calculate_revision_time(total_hours, familiarity):
    """
    Calculates dynamic revision time based on familiarity and study duration.
    - More time is allocated for less familiar topics.
    - Shorter total hours have less proportion allocated for revision.
    """
    avg_familiarity = sum(familiarity) / len(familiarity)
    
    # Dynamic allocation of revision time
    if avg_familiarity <= 2:  # Topics are unfamiliar
        revision_percentage = 0.3  # 30% of time for revision
    elif avg_familiarity <= 4:  # Moderately familiar
        revision_percentage = 0.2  # 20% of time for revision
    else:  # Familiar topics
        revision_percentage = 0.1  # 10% of time for revision

    return total_hours * revision_percentage

# Function to calculate study schedule
def allocate_study_time(topics, familiarity, importance, total_hours, breaks, weak_topic):
    revision_time = calculate_revision_time(total_hours, familiarity)  # Calculate revision time
    study_hours = total_hours - revision_time - (BREAK_MINUTES * breaks / MINUTES_IN_HOUR) 
    topic_weights = [(5 - fam) + imp for fam, imp in zip(familiarity, importance)]
    if weak_topic in topics:
        weak_index = topics.index(weak_topic)
        topic_weights[weak_index] += max(topic_weights) * 0.5
    
    total_weight = sum(topic_weights)
    time_per_topic = [(weight / total_weight) * study_hours for weight in topic_weights]
    
    schedule = []
    for topic, time in zip(topics, time_per_topic):
        while time > MAX_SESSION_HOURS:
            schedule.append((topic, MAX_SESSION_HOURS))
            time -= MAX_SESSION_HOURS
        if time > 0:
            schedule.append((topic, round(time, 2)))

    # Add revision as a final task
    schedule.append(("Revision", round(revision_time, 2)))
    return schedule

# Main function
def main():
    print("=" * 50)
    print("Welcome to the Scheduler!")
    print("=" * 50)
    print(
        "This program is designed to help you plan your study sessions effortlessly. "
        "\n\nThe idea is simple: automate the pre-study planning so you can focus entirely on learning. "
        "\n\nNo more time spent deciding what to study or how much time to allocate — the Scheduler has got it covered! "
        "\n\nRemember, the suggested time blocks are flexible. Adjust them as you need, "
        "\n\nbecause the ultimate goal is *you studying.* "
        "\n\nSo, let’s get started and make your study session as productive as possible!"
    )
    print("=" * 50)
    print(
    "This program helps you plan your study sessions effectively by dividing your time based on familiarity and importance of topics. "
    "\n\nBefore we start, here’s how to rate your topics:\n"
    "Familiarity:\n"
    "  - 0: You know nothing about this topic and need to learn it from scratch.\n"
    "  - 1: You have heard about this topic but lack clarity.\n"
    "  - 2: You have basic understanding but need more detailed study.\n"
    "  - 3: You understand it partially but require further practice.\n"
    "  - 4: You’re comfortable with this topic and just need a quick review.\n"
    "  - 5: You’re an expert and can skim through it confidently.\n"
    "\nImportance:\n"
    "  - 0: This topic is not important for your exam or goals.\n"
    "  - 1: It’s mildly relevant but not a priority.\n"
    "  - 2: It’s moderately important and could appear in the exam.\n"
    "  - 3: It’s fairly important and deserves attention.\n"
    "  - 4: It’s a key topic that you should focus on.\n"
    "  - 5: It’s critical and highly likely to appear in the exam; skipping is not an option.\n"
    "\nTake your time to rate thoughtfully. Accurate ratings lead to better planning!"
)
    print("=" * 50)
    
    # Input topics
    topics = input("Enter your topics (comma-separated): ").split(",")
    topics = [topic.strip() for topic in topics]
    
    familiarity = []
    importance = []
    for topic in topics:
        fam = float(input(f"How well do you know '{topic}'? (0 = None, 5 = Expert): "))
        familiarity.append(fam)
        imp = float(input(f"How important is '{topic}'? (0 = Not at all, 5 = Very important): "))
        importance.append(imp)

    weak_topic = input("Enter the topic you're least confident about (or press Enter to skip): ").strip()
    total_hours = float(input("How many total study hours do you have? "))
    breaks = input(f"How many breaks? (Default = {DEFAULT_BREAK_COUNT}): ")
    breaks = int(breaks) if breaks.isdigit() else DEFAULT_BREAK_COUNT

    # Generate schedule
    schedule = allocate_study_time(topics, familiarity, importance, total_hours, breaks, weak_topic)

    # Save and display schedule
    file_name = f"study_schedule_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(file_name, "w") as file:
        file.write("Study Schedule:\n")
        file.write("-" * 40 + "\n")
        for topic, hours in schedule:
            minutes = round(hours * MINUTES_IN_HOUR)
            file.write(f"{topic}: {hours:.2f} hours ({minutes} minutes)\n")
        file.write("-" * 40 + "\n")
        file.write(f"Total Study Time (excluding breaks and revision): {total_hours - (BREAK_MINUTES * breaks / MINUTES_IN_HOUR):.2f} hours\n")
        file.write(f"Total Break Time: {BREAK_MINUTES * breaks} minutes\n")
    
    # Output schedule
    print("\nYour Study Schedule:")
    print("-" * 40)
    for topic, hours in schedule:
        minutes = round(hours * MINUTES_IN_HOUR)
        print(f"{topic}: {hours:.2f} hours ({minutes} minutes)")
    print("-" * 40)
    print(f"Total Study Time (excluding breaks and revision): {total_hours - (BREAK_MINUTES * breaks / MINUTES_IN_HOUR):.2f} hours")
    print(f"Total Break Time: {BREAK_MINUTES * breaks} minutes")
    print("-" * 50)
    print(f"Schedule saved as: {file_name}")
    print("-" * 50)
    print("Note: Continuous spaced-out revision gives efficient output. Review material at increasing intervals for better retention.")
    print("-" * 50)

if __name__ == "__main__":
    main()

#enna vazhka da idhu!, sighs