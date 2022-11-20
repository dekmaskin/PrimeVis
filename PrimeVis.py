# Prime Visualizer - Mapping primes on an image
import numpy as np
import cv2 as cv
import os
import math

class Primes:
    def __init__(self, n):
        self.primes = []
        self.lenght = n

    def gen_primes(self):
        n = self.lenght
        self.primes = [True for i in range(n + 1)]

        p = 2
        while (p * p <= n):
            
            # If primes[p] is not changed, then it is a prime
            if (self.primes[p] == True):
                
                # Update all multiples of p
                for i in range(p * 2, n + 1, p):
                    self.primes[i] = False
            p += 1
        # Zero and one are not primes
        self.primes[0]= False
        self.primes[1]= False
        print("Primes generated!")

    # Print primes numbers
    def print_primes(self, n):
        for p in range(n + 1):
            if self.primes[p]:
                print(p)

class Image:
    def __init__(self, x, y):
        self.x_size = x
        self.y_size = y
        self.image = np.zeros((self.x_size,self.y_size,3), np.uint8)
    
    def set_dir(self, path, directory, fileName):
        self.path = path
        self.directory = directory
        self.name = fileName

        os.chdir(self.directory)
    
    def save_img(self):
        # Using cv2.imwrite() method
        # Saving the image
        iswritten = cv.imwrite(self.name, self.image)
        if iswritten:
            print("Image saved!")
    
    def makePattern(self, x_dots, y_dots, dot_radius, dot_spacing, primeList):
        
        self.x_dots = x_dots
        self.y_dots = y_dots
        self.dot_radius = dot_radius
        self.dot_spacing = dot_spacing
        primes = primeList

        color = (0, 255, 0)
        thickness = -1

        # Calculate the first dot coordinate. Using floor to avoid floats.
        dot_x = self.dot_spacing + self.dot_radius * 2
        dot_y = self.dot_spacing + self.dot_radius * 2

        # Place dots
        i = 1
        for y in range(1, self.y_dots):
        
            for x in range(1, self.x_dots):

                if primes[i] == True:
                    self.image = cv.circle(self.image, (dot_x, dot_y), self.dot_radius, color, thickness)
                dot_x += self.dot_spacing + self.dot_radius * 2
                i += 1
            dot_x = self.dot_spacing + self.dot_radius * 2 # Reset x position
            dot_y += self.dot_spacing + self.dot_radius * 2
        print("Dots done!")


# Settings
x_dots      =    997      # How many dots in x-axis
y_dots      =    997      # How many dots in y-axis
dot_radius  =    8      # Dot radius
dot_spacing =    5      # Spacing between dots

path = r'C:\Users\johan\Documents\Programmering\PrimeVis\PrimeImage.png'
directory = r'C:\Users\johan\Documents\Programmering\PrimeVis'
filename = 'PrimeImage.png'

# Calculate image size
img_x_size = (x_dots * dot_radius * 2) + (x_dots * dot_spacing) + dot_spacing
img_y_size = (y_dots * dot_radius * 2) + (y_dots * dot_spacing) + dot_spacing

# Calculate how many primes needs to be generated
max_primes  = x_dots * y_dots

# Get a list of primes numbers
primeList = Primes(max_primes)
primeList.gen_primes()

# Create and set up image object
img = Image(img_y_size, img_x_size)
img.set_dir(path, directory, filename)

img.makePattern(x_dots, y_dots, dot_radius, dot_spacing, primeList.primes)
img.save_img()