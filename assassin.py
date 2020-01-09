import copy
import random

weapons = [
    "Another assassin's mobile phone (Not yours)",
    'Christmas Ornament',
    'Rolling Pin',
    'Wifi Password',
    'Butter',
    'Teapot',
    'Oak leaf',
    'Right wellington boot',
    'Loo roll',
    'Tampon',
    'Phone charger',
    'Slice of cake or ham',
    'Thick book',
    'Eggcup',
    'Lamp shade',
    'Pillow',
    'Framed picture',
    'Jug of water',
    'Bottle of whiskey',
    "Pair of boxers",
    'Jenga',
    'Pottery animal',
    'Light bulb',
    'Peppercorn',
    "Pair of knickers",
    'Passport',
    'Mug',
    "Megan's collar",
    'Bottle of Burren Balsamics',
    'Multicoloured sock',
]

rooms = [
    'Kitchen',
    'Sitting room',
    'Hall',
    'Dorm (with the bunk beds)',
    'A bedroom (not the dorm)',
]

killers = [
    'Iona',
    'Luc',
    'Ben',
    'Rand',
    'Kirsty',
    'Ollie',
    'Zoe',
]


random.shuffle(killers)
random.shuffle(weapons)

victims = [killers[-1]] + killers[:-1]

k_v_w = zip(killers, victims, weapons[:len(killers)])

for x, y, z in k_v_w:
    print(f'You are killing {y} with a {z}\n in {}')
