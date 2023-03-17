import copy
import random
import os

weapons = [
    "Another assassin's mobile phone (Not yours)",
    'Some butter (in or out of wrapper)',
    'A teapot or cafetierre (If one not available, jug of water)',
    'A loo roll',
    'A bar of soap',
    'A phone charger',
    'A book',
    'An eggcup',
    'A pillow',
    'A jug of water',
    'A bottle of wine',
    'A pair of boxers',
    'A pot/pan',
    'Light bulb',
    'Peppercorn',
    'Pair of knickers',
    'A credit/debit card',
    'A mug',
    'A bracelet',
    'A multicoloured sock',
    'A pair of spectables/sunglasses',
]

rooms = [
    'the kitchen',
    'the sitting room',
    'the hall',
    'the games room'
    'any bathroom',
    'any bedroom',
    'any outside area',
    'the kitchen',
    'the sitting room',
    'the sitting room',
    'the games room',
    'any outside',
    'any outside',
]

killers = [
    'Iona',
    'Tom',
    'Chloe',
    'Archie',
    'Isobel',
    'Jack',
    'Hector',
    'George',
    'Chiara',
    'Olivia',
    'Bruno',
    'Harry',
]


def run():
    random.shuffle(killers)
    random.shuffle(weapons)
    random.shuffle(rooms)
    victims = [killers[-1]] + killers[:-1]
    k_v_w_r = {k: {'v': v, 'w': w, 'r': r} for k, v, w, r in zip(killers, victims, weapons[:len(killers)], rooms[:len(killers)])}

    while True:
        player = input('Enter your full first name, killer: ').title()
        if v_w_r := k_v_w_r.get(player):
            print(f'You are killing {v_w_r["v"]} with {v_w_r["w"]} in {v_w_r["r"]}. Write this down and do not tell anyone!')
            input('Press any key to clear the results.')
            os.system('clear')
        else:
            print('This name is not in the list! Remember to use your full first name, no nicknames')


if __name__ == '__main__':
    run()