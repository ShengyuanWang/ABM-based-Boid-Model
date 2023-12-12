# import packages required
import numpy as np
import random
class Boid:

    def __init__(self, xstr=0, ystr=0, xlim=1000, ylim=1000, vlim=10, turnFactor=0.3, visualRange=40, protectionRange=8,
                 centeringFactor=0.005, avoidFactor=0.01, matchingFactor=0.5, maxSpeed=6, minSpeed=3, predatorturnfactor=0.5, predatorRange=100, mountainturnfactor=0.05, mountainRange=80, maxBias=0.01,
                 biasIncrement=0.00004, biasValue=0.001):
        self.x = random.random()*xlim +xstr# x-position
        self.xstr = xstr
        self.ystr = ystr
        self.xlim = xlim
        self.ylim = ylim
        self.y = random.random()*ylim +ystr# y-position
        self.vx = random.random() * 2 - 1 # x-velocity
        self.vy = random.random() * 2 - 1# y-velocity
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
        self.predatorturnfactor = predatorturnfactor # How much the boids can turn when they see a predator (Default: 0.5, static)
        self.predatorRange = predatorRange # How far the boids can see predators (Default: 100, static)
        self.mountainturnfactor = mountainturnfactor # How much the boids can turn when they see a mountain (Default: 0.1, static)
        self.mountainRange = mountainRange # How far the boids can see mountains (Default: 200, static)

    def distance(self, boid2):
      """
        Calculate the distance between two boids
      :param boid1: the first boid
      :param boid2: the second boid
      :return: the distance between the two boids
      """
      return np.sqrt((self.x - boid2.x)**2 + (self.y - boid2.y)**2)

    def separation(self, boids):
      """
        Calculate the velocity of the boid to avoid other boids
      :param boid: the boid to calculate the velocity
      :param boids: all the boids
      :return: the velocity of the boid (x-velocity, y-velocity)
      """
      closeDistanceX, closeDistanceY = 0, 0
      numBoids = 0
      for otherBoid in boids:
        if otherBoid != self and self.distance(otherBoid) < self.protectionRange:
            closeDistanceX += self.x - otherBoid.x
            closeDistanceY += self.y - otherBoid.y
            numBoids += 1
      if numBoids > 0:
        self.vx = closeDistanceX * self.avoidFactor
        self.vy = closeDistanceY * self.avoidFactor

    def alignment(self, boids):
      """
        Calculate the velocity of the boid to match the velocity of other boids
      :param boid: the boid to calculate the velocity
      :param boids: all the boids
      :return: the velocity of the boid (x-velocity, y-velocity)
      """
      avgVx, avgVy = 0, 0
      numBoids = 0
      for otherBoid in boids:
          avgVx += otherBoid.vx
          avgVy += otherBoid.vy
          numBoids += 1
      if numBoids > 0:
        avgVx /= numBoids
        avgVy /= numBoids
        self.vx += (avgVx - self.vx) * self.matchingFactor
        self.vy += (avgVy - self.vy) * self.matchingFactor
        return ((avgVx-self.vx)**2 + (avgVy-self.vy)**2)**0.5 ## average speed - bird speed
      return 0

    def cohension(self, boids):
      """
        Calculate the velocity of the boid to move towards the center of other boids
      :param boid: the boid to calculate the velocity
      :param boids: all the boids
      :return: the velocity of the boid (x-velocity, y-velocity)
      """
      centeringX, centeringY = 0, 0
      numBoids = 0
      for boid in boids:
          centeringX += boid.x
          centeringY += boid.y
          numBoids += 1
      if numBoids > 0:
        centeringX /= numBoids
        centeringY /= numBoids
        self.vx += (centeringX - self.x) * self.centeringFactor
        self.vy += (centeringY - self.y) * self.centeringFactor
        return ((centeringX-self.x)**2 + (centeringY-self.y)**2)**0.5 # problems here with the centeringX and centeringY # ignore the visual range
      return 0

    # def cohensionWithoutVisual(self, boids):
    #   """
    #     Calculate the velocity of the boid to move towards the center of other boids
    #   :param boid: the boid to calculate the velocity
    #   :param boids: all the boids
    #   :return: the velocity of the boid (x-velocity, y-velocity)
    #   """
    #   centeringX, centeringY = 0, 0
    #   numBoids = 0
    #   for otherBoid in boids:
    #     if otherBoid != self:
    #       centeringX += otherBoid.x
    #       centeringY += otherBoid.y
    #       numBoids += 1
    #   if numBoids > 0:
    #     centeringX /= numBoids
    #     centeringY /= numBoids
    #     self.vx += (centeringX - self.x) * self.centeringFactor
    #     self.vy += (centeringY - self.y) * self.centeringFactor
    #     return ((centeringX-self.x)**2 + (centeringY-self.y)**2)**0.5 / numBoids # problems here with the centeringX and centeringY # ignore the visual range
    #   return 0

    def centerPosition(self, boids):
        centeringX, centeringY = 0, 0
        numBoids = 0
        for otherBoid in boids:
            centeringX += otherBoid.x
            centeringY += otherBoid.y
            numBoids += 1
        if numBoids > 0:
            centeringX /= numBoids
            centeringY /= numBoids

        return centeringX, centeringY

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


    def speedLimit(self):
      """
        Calculate the velocity of the boid to limit the speed
      :param boid: the boid to calculate the velocity
      :return: the velocity of the boid (x-velocity, y-velocity)
      """
      speed = np.sqrt(self.vx**2 + self.vy**2)
      if speed > self.maxSpeed:
        self.vx *= self.maxSpeed / speed
        self.vy *= self.maxSpeed / speed
      elif speed < self.minSpeed:
        self.vx *= self.minSpeed / speed
        self.vy *= self.minSpeed / speed

    def avoidPreadator(self, predators):
        num_predators = 0
        predator_dx, predator_dy = 0, 0
        for predator in predators:
            dx = self.x - predator.x
            dy = self.y - predator.y
            if (abs(dx)<self.predatorRange and abs(dy)<self.predatorRange):
                if (self.distance(predator) < self.predatorRange):
                    predator_dx += self.x - predator.x
                    predator_dy += self.y - predator.y
                    num_predators += 1
        if num_predators > 0:
            self.vx += predator_dx * self.predatorturnfactor
            self.vy += predator_dy * self.predatorturnfactor

    def avoidMountain(self, mountains):
        num_mountains = 0
        mountain_dx, mountain_dy = 0, 0
        for mountain in mountains:
            dx = self.x - mountain.x
            dy = self.y - mountain.y
            if (abs(dx)<self.mountainRange and abs(dy)<self.mountainRange):
                if (self.distance(mountain) < self.mountainRange):
                    mountain_dx += self.x - mountain.x
                    mountain_dy += self.y - mountain.y
                    num_mountains += 1
        if num_mountains > 0:
            self.vx += mountain_dx * self.mountainturnfactor
            self.vy += mountain_dy * self.mountainturnfactor



    def updateBoid(self, boids, predators, mountains, leftMargin, rightMargin, bottomMargin, topMargin, factor):
        """
        Update the velocity and position of the boid
        :param boid: the boid to update
        :param boids: all the boids
        :return: the updated boid
        """
        self.separation(boids)
        self.alignment(boids)
        self.cohension(boids)
        if factor == 1:
            self.avoidPreadator(predators)
            self.avoidMountain(mountains)
        if factor == 2:
            self.avoidPreadator(predators)
        if factor == 3:
            self.avoidMountain(mountains)
        self.edgeTurning(leftMargin+(rightMargin-leftMargin)/4, rightMargin-(rightMargin-leftMargin)/4, bottomMargin + (topMargin-bottomMargin)/2, topMargin-(topMargin-bottomMargin)/2)
        self.bias()
        self.speedLimit()
        self.x += self.vx
        self.y += self.vy
        # if self.x > rightMargin:
        #     self.x += leftMargin - rightMargin
        # elif self.x < leftMargin:
        #     self.x += rightMargin - leftMargin
        # if self.y > topMargin:
        #     self.y += bottomMargin - topMargin
        # elif self.y < bottomMargin:
        #     self.y += topMargin - bottomMargin

    # def cohesionWithoutVisual(self, boids, size):
    #     centeringX, centeringY = 0, 0
    #     numBoids = 0
    #     for otherBoid in boids:
    #         centeringX += otherBoid.x
    #         centeringY += otherBoid.y
    #         numBoids += 1
    #     centeringX /= numBoids
    #     centeringY /= numBoids
    #     self.vx += (centeringX - self.x) * self.centeringFactor
    #     self.vy += (centeringY - self.y) * self.centeringFactor
    #     if centeringX - self.x < 0:
    #         difX = min(centeringX - self.x + size, self.x - centeringX)
    #     else:
    #         difX = min(centeringX - self.x, self.x - centeringX + size)
    #     if centeringY - self.y < 0:
    #         difY = min(centeringY - self.y + size, self.y - centeringY)
    #     else:
    #         difY = min(centeringY - self.y, self.y - centeringY + size)
    #     return ((difX) ** 2 + (
    #                 difY) ** 2) ** 0.5 / numBoids  # problems here with the centeringX and centeringY # ignore the visual range
