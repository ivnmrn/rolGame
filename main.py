from models import *
from ascii import *
import os

number_heroes = 3

Base.metadata.create_all(engine)


def query_creature(creature, id_creature):
    return session.query(creature).get(id_creature)


def choose_ability(hero):
    list_attacks = []
    command = None

    print('\n MENU:\n+----------------------------------------------------------------------------------+')
    print('Abilities:')
    for x in hero.attacks:
        if hero.level >= x.attack_level:
            print(f' [{x.id}] {x.ability_name}')
            list_attacks.append(x.id)
    while command not in list_attacks:
        try:
            command = int(input(
                '+----------------------------------------------------------------------------------+\nSelect your attack.\n'))
        except ValueError:
            print('Please insert a number')
        if command not in list_attacks:
            print(f'This ability is not available at level {hero.level}.')
    os.system('clear')
    return session.query(Attack).get(command)


def fight(champion, monster, art):
    battle = Battle(champion, monster)
    # Start battle
    print(f'You enter in combat against {monster.name}')
    monster.talk()
    while not battle.is_finished():
        print(art)
        command1 = choose_ability(champion)
        battle.execute_turn(command1)
        battle.current_status()


def game_over(reason):
    print("\n" + reason)
    print("Game Over!")


def cave():
    print('Notning yet')


def garden():
    print('Notning yet')


def castle():
    print('Yo see a castle.\nThe castles exterior is dark gray. '
          'It has five visible windows and many different chambers with conical roofs.'
          '\nWhat you will do? (enter/explore')

    answer = input(">").lower()

    if 'enter' in answer:
        print('Inside, there are gray walls made of stone and gray flooring made of tiles. '
              'The front entryway leads to several flights of stairs that can collapse. '
              'On each staircase is a sign with a message that warns the reader not to climb the stairs.\n'
              'Do you climb the stairs? (yes/no)')

        answer = input(">").lower()

        if answer == 'yes':
            vampire = session.query(Monster).get(4)
            fight(champion, vampire, monsters_art[vampire.name])
        elif answer == 'no':
            print('Nothing yet')
        else:
            game_over('Dont you know how to type something properly?')
    elif 'explore' in answer:
        garden()
    else:
        # else call game_over() function with the "reason" argument
        game_over('Dont you know how to type something properly?')


def start():
    print('\nYou are standing in a dark forest.')
    print('There is a route to your left and right, which one do you take? (l or r)')

    answer = input(">").lower()

    if "l" in answer:
        castle()
    elif "r" in answer:
        cave()
    else:
        # else call game_over() function with the "reason" argument
        game_over('Dont you know how to type something properly?')


# Champion Select
heroes = session.query(Hero).all()
print('Select your champion\n\n+----------------------------------------------------------------------------------+')
for x in heroes:
    print(f' [{x.id}] New {x.class_hero}')
print('+----------------------------------------------------------------------------------+')
id_hero = 0
while id_hero == 0 or id_hero > number_heroes:
    try:
        id_hero = int(input())
    except ValueError:
        print('Please insert a number')
champion = query_creature(Hero, id_hero)

os.system('clear')
print('Here starts your adventure!')
print(monsters_art[champion.class_hero])
# start the game
start()
