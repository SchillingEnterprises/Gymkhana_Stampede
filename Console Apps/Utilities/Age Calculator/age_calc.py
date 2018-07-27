from datetime import date


# Step 1
# Ask the user for their name and the year they were born.
name = input("Hello!  What is your name?  ")


while True:
    year_of_birth = input("What year were you born?  ")
    try:
        year_of_birth = int(year_of_birth)
    except ValueError:
        continue
    else:
        break


# Steps 2 & 3
# Calculate and print the year they'll turn 25, 50, 75, and 100.
    # If they're already past any of these ages, skip them.
milestones = [10, 16, 18, 21, 25, 50, 75, 100]


for milestone in milestones:
    if year_of_birth + milestone > date.today().year:
        print("{}, you will turn {} in {}".format(name, milestone, str(year_of_birth + milestone)))
