import datetime, random
from typing import List, Optional


def get_birthdays(number_of_birthdays: int) -> List:
    """Returns a list of number random date objects for birthdays."""
    # The year is unimportant for this simulation, as long as all
    # birthdays have the same year.
    start_of_year = datetime.date(2001, 1, 1)

    birthdays = []
    for i in range(number_of_birthdays):
        # Get a random day into the year:
        random_number_of_days = datetime.timedelta(days=random.randint(0, 364))
        birthday = start_of_year + random_number_of_days
        birthdays.append(birthday)

    return birthdays


def get_match(birthdays: List) -> Optional[int]:
    """Returns the date object of a birthday that occurs more than once in the birthdays list."""
    if len(birthdays) == len(set(birthdays)):
        # All birthdays are unique, so return None.
        return None

    # Compare each birthday to every other birthday:
    for a, birthday_a in enumerate(birthdays):
        if birthday_a in birthdays[a + 1:]:
            # Return the matching birthday.
            return birthday_a


def main():
    print("""Birthday Paradox (https://en.wikipedia.org/wiki/Birthday_problem)
    The Birthday Paradox shows us that in a group of N people, the odds
    that two of them have matching birthdays is surprisingly large.
    This program does a Monte Carlo simulation (that is, repeated random
    simulations) to explore this concept.""")

    while True:
        # Keep asking until the user enters a valid amount.
        print("How many birthdays shall I generate? (Max 100)")
        response = input("> ")
        if response.isdecimal() and (0 < int(response) <= 100):
            num_bdays = int(response)
            break  # User entered valid number
        else:
            print("Wrong input. Try again.")

    # Run through 100,000 simulations:
    print('Generating', num_bdays, 'random birthdays 100,000 times...')
    input('Press Enter to begin...')

    print('Beginning 100,000 simulations...')
    sim_match = 0  # How many simulations had matching birthdays in them.

    for i in range(100_000):
        # Report on the progress every 10,000 simulations:
        if i % 10_000 == 0:
            print(i, 'simulations were conducted...')

        birthdays = get_birthdays(num_bdays)

        if get_match(birthdays) is not None:
            sim_match += 1

    print('100,000 simulations has been done.')
    # Display simulation results:
    probability = round(sim_match / 100_000 * 100, 2)

    print('Out of 100,000 simulations of', num_bdays, 'people, there was a')

    print('matching birthday in that group', sim_match, 'times. This means')

    print('that', num_bdays, 'people have a', probability, '% chance of')

    print('having a matching birthday in their group.')

    print('That\'s probably more than you would think!')


if __name__ == "__main__":
    main()

