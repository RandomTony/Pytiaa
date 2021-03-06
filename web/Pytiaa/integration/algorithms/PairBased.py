import os
import sys
import math
import pylab
import matplotlib.pyplot as plt

from random import choice
from django.conf import settings
from integration.algorithms.utils import dist, removeFiles
from integration.algorithms.constants import *

def PairBased(new: tuple, points: tuple, k: int=1):
	c, points, classe = _nearest_neighbor(new, points)
	if(classe is None):
		couples = _couples_creation(c, points)
		classe = _compute_class(couples, c)
	return classe, c, couples

def _nearest_neighbor(new, points):
	classe = None
	# Compute the nearest neighbor
	c = (points[0], dist(new[0], points[0][0], new[1], points[0][1]))
	for p in points:
		distance = dist(new[0], p[0], new[1], p[1])
		if(distance < c[1]):
			c = (p, distance)
	points.remove(c[0])

	# If the NN and the new point are the same, their class is the same
	if(new[0] == c[0][0] and new[1] == c[0][1]):
		classe = c[0][2]

	return c, points, classe

def _couples_creation(c, points):
	# dist(a, b)
	couples = []
	for ida, a in enumerate(points):
		for idb in range(ida):
			couples.append([a, points[idb], dist(a[0], points[idb][0], a[1], points[idb][1])])

	# dist(a, b) ~= dist(c, d)
	for couple in couples:
		couple[-1] = abs(couple[-1] - c[1]) # couples[-1] is the distance
	couples.sort(key=lambda c: c[2])
	couples.reverse()

	return couples

def _compute_class(couples, c):
		# Class computation
	classe = None
	while(classe is None and couples != []):
		closest = couples.pop()
		w, x, y = closest[0], closest[1], c[0]
		# Solving analogical equation
		if(w[2] == x[2] and x[2] == y[2]):
			# 1 : 1 :: 1 : x
			classe = w[2]
		elif(w[2] == x[2] and y[2] != w[2]):
			# 1 : 1 :: 0 : x
			classe = y[2]
		elif(w[2] != x[2] and w[2] == y[2]):
			# 1 : 0 :: 1 : x
			classe = x[2]

	return classe

def _reset(ax, points, c):
	plt.xlim(0, 1)
	plt.ylim(0, 1)
	plt.scatter(
		[point[0] for point in points],
		[point[1] for point in points],
		c=[point[2] for point in points],
		s=POINTS_SIZE,
		linewidths=0
	)
	plt.scatter(c[0][0], c[0][1], c=c[0][2], s=POINTS_SIZE, linewidths=0)

def pb_draw(new, points, c, couples, classe, plt=plt):
	FOLDER = os.path.join(settings.BASE_DIR, 'static/img/pairBased/')
	NB_COUPLES_DISPLAYED = 4

	removeFiles(FOLDER) # remove previous files

	# IMAGE 1 #
	_reset(plt, points, c)
	pylab.savefig(FOLDER + '0/' + '0')

	# IMAGE 2 #
	plt.scatter(new[0], new[1], c="#000000", s=POINTS_SIZE, linewidths=0)
	pylab.savefig(FOLDER  + '1/' + '0')

	# IMAGE 3 #
	plt.plot([new[0], c[0][0]], [new[1], c[0][1]], c="#878787", alpha=.3)
	pylab.text(0.5, 1.05, 'Nearest neighbor, dist='+str(round(c[1], 4)), fontsize=12)
	pylab.savefig(FOLDER + '2/' + '0')

	# IMAGE 4 #
	# Clear and redraw the points, axes, ...
	plt.clf()
	_reset(plt, points, c)
	plt.scatter(new[0], new[1], c="#000000", s=POINTS_SIZE, linewidths=0)

	# Select random couples to display
	displayedCouples = [choice(couples) for i in range(NB_COUPLES_DISPLAYED)]
	for c in [choice(couples) for i in range(NB_COUPLES_DISPLAYED)]:
		plt.plot([c[0][0], c[1][0]], [c[0][1], c[1][1]], c="#878787", alpha=.3)	# Draw the line between the two points
		midx, midy = (c[0][0] + c[1][0]) / 2, (c[0][1] + c[1][1]) / 2	# Where the text is placed
		annot = plt.annotate(str(round(c[2], 3)), xy=(midx, midy), xytext=(-15,15),
            		textcoords='offset points', ha='center', va='bottom',
            		arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.5'))
		# pylab.text(midx, midy, str(round(c[2], 3)))	 # Display the distance between the two points
	pylab.savefig(FOLDER + '3/' + '0')
	annot.remove()

	# IMAGE 5 #
	if(classe is None):
		print("Can't classify")
	print("Solving analogical equation, first solved => class given to the new point")
	# Clear and redraw the points, axes, ...
	plt.clf()
	_reset(plt, points, c)
	plt.scatter(new[0], new[1], c="#000000", s=POINTS_SIZE, linewidths=0)
	# pylab.text(0.5, 1.05, 'Couples creation + distance computation', fontsize=12)

	for i, closest in enumerate(couples):
		# Circles to highlight the current points of the equation
		w, x, y = closest[0], closest[1], c[0]
		annot1 = plt.annotate(s='A', xy=(w[0], w[1]))
		annot2 = plt.annotate(s='B', xy=(x[0], x[1]))
		annot3 = plt.annotate(s='C', xy=(y[0], y[1]))
		textEquation = pylab.text(.5, 1.05, str(w[-1]) + " : " + str(x[-1]) + " :: " + str(y[-1]) + " : x")
		pylab.savefig(FOLDER + '4/' + str(i))
		# Clear the circles & txt
		for annot in [annot1, annot2, annot3]:
			annot.remove()
		textEquation.remove()

	# IMAGE 6 #
	_reset(plt, points, c)
	plt.scatter(new[0], new[1], c=classe, s=POINTS_SIZE, linewidths=0)
	pylab.savefig(FOLDER + '5/0')

def main(argv):
	points = [
		[.25, .75, "red"],
		[.5, .8, "red"],
		[.2, .5, "red"],
		[.7, .1, "blue"],
		[.45, .28, "blue"],
		[.34, .67, "blue"],
	]
	new = (.5, .5)

	classe, c, couples = PairBased(new ,points)
	print(classe)
	pb_draw(new, points, c, couples, classe, plt)


	return 0

if(__name__ == '__main__'):
	sys.exit(main(sys.argv))
