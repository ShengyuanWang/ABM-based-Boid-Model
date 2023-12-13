# import packages required
import numpy as np
import random
class Predator:

    def __init__(self, xstr=0, ystr=0,xlim=1000, ylim=1000, vlim=10, turnFactor=0.1, visualRange=100, protectionRange=8,
                 centeringFactor=0.005, avoidFactor=0.05, matchingFactor=0.05, maxSpeed=7, minSpeed=5,maxBias=0.01,
                 biasIncrement=0.00004, biasValue=0.001, hungry=10, seed=123):
        random.seed(seed)
        self.x = random.random()*xlim +xstr# x-position
        self.y = random.random()*ylim +ystr# y-position
        self.vx = random.random() # x-velocity
        self.vy = random.random() # y-velocity
        self.vx, self.vy = self.vx / np.linalg.norm([self.vx, self.vy]) * vlim, self.vy / np.linalg.norm([self.vx, self.vy]) * vlim # velocity normalization
        self.turnFactor = turnFactor # How much the boids can turn (Default: 0.01, static)
        self.visualRange = visualRange # How far the boids can see (Default: 40, static)
        self.protectionRange = protectionRange # How far the boids can keep away from each other (Default: 8, static)
        self.centeringFactor = centeringFactor # How much the boids move towards the center (Default: 0.0005, static)
        self.avoidFactor = avoidFactor # How much the boids avoid each other (Default: 0.05, static)
        self.matchingFactor = matchingFactor # How much the boids match each other's speed (Default: 0.05, static)
        self.maxSpeed, self.minSpeed = maxSpeed, minSpeed # Maximum and minimum speed of the boids (Default: 6, 3, static)
        self.maxBias = maxBias # Maximum bias value for the boids to move towards the center (Default: 0.01, static)
        self.biasIncrement = biasIncrement # How much the bias value increases each time (Default: 0.00004, static)
        self.biasValue = biasValue # Bias value for the boids to move towards the center (Default: 0.001, changable)
        self.hungry = hungry # How many boids the predator can eat (Default: 10, static)

    def edgeTurning(self, leftMargin, rightMargin, bottomMargin, topMargin):
      """
        Calculate the velocity of the boid to turn away from the edge of the screen
      :param boid: the boid to calculate the velocity
      :return: the velocity of the boid (x-velocity, y-velocity)
      """
      if self.x < leftMargin:
        self.vx += self.turnFactor
      elif self.x > rightMargin:
        self.vx -= self.turnFactor
      if self.y < bottomMargin:
        self.vy += self.turnFactor
      elif self.y > topMargin:
        self.vy -= self.turnFactor

    def bias(self):
        """
            Calculate the velocity of the boid to move towards the center of the screen
        :param boid: the boid to calculate the velocity
        :return: the velocity of the boid (x-velocity, y-velocity)
        """
        self.vx += (1-self.biasValue) * self.vx + self.biasValue
        self.vy += (1-self.biasValue) * self.vy + self.biasValue
        #TODO: we can make the bias value change over time

    def catchBoid(self, boids):
        closestBoid = None
        for boid in boids:
            distance = np.sqrt((self.x - boid.x)**2 + (self.y - boid.y)**2)
            if distance < self.visualRange:
                closestBoid = boid
            if distance < self.protectionRange:
                self.hungry -= 1
        if closestBoid:
            dir_x, dir_y = closestBoid.x - self.x, closestBoid.y - self.y
            dir_x, dir_y = dir_x / np.linalg.norm([dir_x, dir_y]), dir_y / np.linalg.norm([dir_x, dir_y])
            speed = np.sqrt(self.vx**2 + self.vy**2)
            self.vx, self.vy = dir_x * speed, dir_y * speed


    def speedLimit(self):
      """
        Calculate the velocity of the boid to limit the speed
      :param boid: the boid to calculate the velocity
      :return: the velocity of the boid (x-velocity, y-velocity)
      """
      speed = np.sqrt(self.vx**2 + self.vy**2)
      self.maxSpeed = self.hungry * 0.8 + 2
      self.vx, self.vy = self.vx / speed * self.maxSpeed, self.vy / speed * self.maxSpeed

    def updatePredator(self, boids, leftMargin, rightMargin, bottomMargin, topMargin):
        """
        Update the velocity and position of the boid
        :param boid: the boid to update
        :param boids: all the boids
        :return: the updated boid
        """
        self.catchBoid(boids)
        self.edgeTurning(leftMargin, rightMargin, bottomMargin, topMargin)
        self.bias()
        self.speedLimit()
        self.x += self.vx
        self.y += self.vy
        if self.x > rightMargin:
            self.x += leftMargin - rightMargin
        elif self.x < leftMargin:
            self.x += rightMargin - leftMargin
        if self.y > topMargin:
            self.y += bottomMargin - topMargin
        elif self.y < bottomMargin:
            self.y += topMargin - bottomMargin
        self.hungry += 0.2