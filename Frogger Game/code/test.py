import pygame, sys
from random import choice
from settings import *
from player import *
from os import walk



path_list = []
def import_cars():
	

	for index, folder in enumerate(walk('../graphics/cars')):
		for file_name in folder[2]:
			path_list.append(folder[0].replace('\\', '/') + '/' + file_name)


import_cars()
print(path_list)