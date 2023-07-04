#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 00:02:43 2023

@author: tom
"""

import pygame

from pygame.locals import *
from os import sys

import ctypes
import pathlib
import time
import os
import sys
from tkinter import *
from ctypes import *
import random
import time


##################################################
# Initialize C bindings
##################################################

# Load the shared library into ctypes
if sys.platform == 'win32':
  libname = os.path.join(pathlib.Path().absolute(), "libparticle.dll")
else : 
  libname = os.path.join(pathlib.Path().absolute(), "libparticle.so")
c_lib = ctypes.CDLL(libname)

# Define python equivalent class

class PARTICLE(Structure):
    _fields_ = [("position", c_float*2),
                ("next_pos", c_float*2),
                ("velocity", c_float*2),
                ("inv_mass", c_float),
                ("radius",   c_float),
                ("solid_id", c_int),
                ("draw_id",  c_int),
                ("halo_id", c_int),
                ("temperature", c_float)]
    
class SPHERECOLLIDER(Structure):
    _fields_ = [("center", c_float*2), 
              ("radius", c_float)]
    
class PLANECOLLIDER(Structure):
    _field_ = [("point", c_float*2),
               ("normale", c_float*2)]

class CONTEXT(Structure):
    _fields_ = [("num_particles", c_int),
                ("capacity_particles", c_int),
                ("particles", POINTER(PARTICLE) ),
                ("num_ground_sphere", c_int),
                ("ground_spheres", POINTER(SPHERECOLLIDER)), 
                ("num_ground_plane", c_int), 
                ("ground_plane", POINTER(PLANECOLLIDER))]

# ("pos", c_float*2) => fixed size array of two float


# Declare proper return types for methods (otherwise considered as c_int)
c_lib.initializeContext.restype = POINTER(CONTEXT) # return type of initializeContext is Context*
c_lib.getParticle.restype = PARTICLE
c_lib.getGroundSphereCollider.restype = SPHERECOLLIDER
# WARNING : python parameter should be explicitly converted to proper c_type of not integer.
# If we already have a c_type (including the one deriving from Structure above)
# then the parameter can be passed as is.

##################################################
# Class managing the UI
##################################################
def color_generator():
    r, g, b = random.randint(0,255), random.randint(0,255),random.randint(0,255)
    return f"#{r:02x}{g:02x}{b:02x}"

def couleur_orange(t):
    r = int(min(t*510, 255))
    g = int(t*255)
    b = int(max(0, (t-0.5)*510))
    return f"#{r:02x}{g:02x}{b:02x}"

def couleur_rouge(t):
    r = int(min(t*510, 255))
    g = 0
    b = 0
    return f"#{r:02x}{g:02x}{b:02x}"

def couleur_chaleur(t):
    if t>0.5:
        return couleur_orange(t)
    else:
        return couleur_rouge(t)
    
def couleur_chaleur2(t):
    """on affiche uniquement celle sufisament chaude"""
    if t>0.47:
       return couleur_chaleur(t)
    else:
        return couleur_chaleur(0)
    
def couleur_chaleurRVBA(t):
    """pour le halo lumnineux"""
    alpha = 0.5
    couleur = couleur_chaleur2(t)
    couleur_rvba = couleur + hex(int(alpha * 255))[2:].zfill(2)
    return couleur_rvba
    
#_______________________________________________________

pygame.init()

largeur = 800
hauteur = 800
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Effet de halo lumineux sur un cercle")


centre_x = largeur // 2
centre_y = hauteur // 2
rayon_cercle = 50
couleur_cercle = (255, 0, 0)  # Rouge (RVB)

rayon_max = 60
couleur_centrale = (255, 255, 0)  # Jaune (RVB)
couleur_externe = (255, 0, 0, 100)  # Jaune transparent (RVBA)

while True:
    fenetre.fill((0, 0, 0))  # Effacer la fenêtre avec du noir

    # Dessiner le cercle initial
    

    # Créer une surface pour le halo lumineux
    surface_halo = pygame.Surface((rayon_max * 2, rayon_max * 2), pygame.SRCALPHA)
    print(surface_halo)
    #pygame.draw.circle(surface_halo, couleur_centrale, (rayon_max, rayon_max), rayon_max)
    pygame.draw.circle(surface_halo, couleur_externe, (rayon_max, rayon_max), rayon_max, 10)
    
    pygame.draw.circle(fenetre, couleur_cercle, (centre_x, centre_y), rayon_cercle)
    
    # Afficher le halo lumineux autour du cercle
    fenetre.blit(surface_halo, (centre_x - rayon_max, centre_y - rayon_max))

    pygame.display.flip()  # Mettre à jour l'affichage

    for event in pygame.event.get():
        pygame.quit()
        
            