#!/usr/bin/python3.4

"""
        Fadana algorithm - Fadana.py
            this function return the class of the new point.

            parameters
                point --> value (x,y)
                k --> The number of triplets we keep
                tableau --> All the existing points on the graph

        Author : Anthony LOHOU "RandomTony"
            anthonylohou.com

        Parent directory of Pytiaa => run 'python -m Pytiaa.Algorithms.Fadana'
        Else relative imports won't work1
"""

import sys
import math
import pylab
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from random import randrange
from Pytiaa.DataGen.randomGen import *
from Pytiaa.utils import dist


def fadana(new: tuple, points: list, k: int=10):
    # Checks k value
    if(k > len(points)):
        k = len(points)

    triplets = tripletCreat(points)
    # Compute analogical difference
    analogicalDiff = analogicalCalcul(new, points, triplets)
    # Sorting by AD
    analogicalDiff.sort(key=lambda l: l[1])
    analogicalDiff = analogicalDiff[:k]

    # Class calculation
    classes = classCalcul(points, triplets, analogicalDiff)

    return None if classes == [] else max(classes, key=lambda c: classes.count(c)), triplets, analogicalDiff


# Creation of triplets composed of points
def tripletCreat(points : list):
    triplets = []
    size = len(points)
    # Creates all existing triplets
    index = 0
    for i in range(size):
        for j in range(i+1, size):
            for k in range(j+1, size):
                triplets.append([index, i, j, k])
                index += 1
    return triplets

# Calcul Analogical difference between the new point and triplets
def analogicalCalcul(new : tuple, points : list, triplets : list):
    analogicalDiff = []
    for t in triplets:
        # Analogical difference A and B
        adx1 = points[t[1]][0] - points[t[2]][0]                # A - B
        ady1 = points[t[1]][1] - points[t[2]][1]
        # Analogical difference C and D
        adx2 = points[t[3]][0] - new[0]                         # C - D
        ady2 = points[t[3]][1] - new[1]
        # Real analogical difference
        adx = 1 - abs(adx1 - adx2)                              # AD = 1 - | (A - B) - (C - D) |
        ady = 1 - abs(ady1 - ady2)
        ad = adx + ady
        print(t)
        print(str(t[0]) + " -- " + str(ad))
        # Add to the list
        analogicalDiff.append([t[0], ad])
    return analogicalDiff


# Find the class of the new point for each triplet
def classCalcul(points : list, triplets : list, analogicalDiff : list):
    classes = []
    for a in analogicalDiff:
        t = triplets[a[0]][1:]
        if(points[t[0]][2]==points[t[1]][2]):
            classes.append(points[t[2]][2])
        elif(points[t[0]][2]==points[t[2]][2] and points[t[2]][2]!=points[t[1]][2]):
            classes.append(points[t[1]][2])

    return classes

def _draw(new: tuple, points: tuple, triplets: tuple, anaDiff: tuple, cl: str, plt):
    NB_TRIPLET_DISPLAYED = 4
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    fig = plt.gcf()

    # IMAGE 1 #
    # Training set
    plt.scatter(
        [point[0] for point in points],
        [point[1] for point in points],
        c=[point[2] for point in points]
    )
    plt.scatter(new[0], new[1], c="#000000")
    pylab.savefig('img1')

    # IMAGE 2 #
    # Triplets
    tripletsDisplayed = [choice(triplets) for i in range(NB_TRIPLET_DISPLAYED)]
    # Highlights triplets
    label = ['A', 'B', 'C']
    for i, t in enumerate(tripletsDisplayed):
        patchs = [fig.gca().add_artist(plt.Circle((points[t[i+1]][0], points[t[i+1]][1]), radius=0.02, color='#FF0000')) for i in range(3)]
        texts = [pylab.text(points[t[i+1]][0], points[t[i+1]][1], label[i]) for i in range(3)]
        pylab.savefig('img'+str(i+2))
        # Clear circles and texts
        for i in range(3):
            patchs[i].remove()
            texts[i].remove()

    # IMAGE 3 #
    # computes analogical difference
    print("On trouve les meilleurs triplets en résolvant le calcul de différence analogique")
    print(tripletsDisplayed[0])
    txt = pylab.text(.5, 1.05, 'Find best triplets solving analogical difference')
    a = points[tripletsDisplayed[0][1]]
    b = points[tripletsDisplayed[0][2]]
    c = points[tripletsDisplayed[0][3]]
    patchs = [fig.gca().add_artist(plt.Circle((points[tripletsDisplayed[0][i+1]][0],
                                       points[tripletsDisplayed[0][i+1]][1]),
                                       radius=0.02,
                                       color='#FF0000')) for i in range(3)]
    pylab.savefig('img5')
    txt.remove()
    # remove patches
    for p in patchs:
        p.remove()

    # IMAGE 4 #
    annot = []
    for i, p in enumerate([a, b, c]):
        # Fancy annotation describing the x and y values and the place in the equation of the point
        annot.append(plt.annotate(label[i] + '\nx = '+ str(round(p[0], 3)) + '\ny = ' + str(round(p[1], 3)),
            xy=(p[0], p[1]), xytext=(-20,20),
            textcoords='offset points', ha='center', va='bottom',
            bbox=dict(boxstyle='round,pad=0.2', fc='yellow', alpha=0.3),
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.5',
                            color='red')))
    # print("On calcul la difference analogique de chaque composante (valeurs normalisées)")
    txt = pylab.text(.6, 1.05, 'A - B, on each attribut')
    adx1 = a[0] - b[0]                # A - B
    ady1 = a[1] - b[1]
    txt1 = pylab.text(.095, 1.08, "Ax - Bx = " + str(adx1))
    txt2 = pylab.text(.095, 1.02, "Ay - By = " + str(ady1))
    pylab.savefig('img6')
    # Analogical difference C and D
    txt.remove()
    txt1.remove()
    txt2.remove()

    txt = pylab.text(.6, 1.05, 'C - D, on each attribut')
    adx2 = c[0] - new[0]                         # C - D
    ady2 = c[1] - new[1]
    txt1 = pylab.text(.095, 1.08, "Cx - Dx = " + str(adx2))
    txt2 = pylab.text(.095, 1.02, "Cy - Dy = " + str(ady2))
    pylab.savefig('img7')
    txt.remove()
    txt1.remove()
    txt2.remove()

    # remove annoations
    for a in annot:
        a.remove()

    # Real analogical difference
    # pylab.text('AD = 1 - | (a - B) - (C - D) |, on each attribute, then sum everything to get the final analogical difference')
    adx = 1 - abs(adx1 - adx2)                              # AD = 1 - | (A - B) - (C - D) |
    # print("AD(Ax, Bx) = 1 - | (Ax - Bx) - (Cx - Dx) | = " + str(adx))
    ady = 1 - abs(ady1 - ady2)
    # print("AD(Ay, By) = 1 - | (Ay - By) - (Cy - Dy) | = " + str(ady))
    ad = adx + ady
    # print("AD(A, B, C, D) Finale = " + str(ad))
    txt = pylab.text(.5, 1.05, "AD(A, B, C, D) Finale = " + str(ad))
    pylab.savefig('img8')
    txt.remove()

    # IMAGE 5 #
    for i, closest in enumerate(anaDiff):
        tplt = triplets[closest[0]]
        # Circles to highlight the current points of the equation
        w, x, y = points[tplt[1]], points[tplt[2]], points[tplt[3]]
        annot1 = plt.annotate(s='A', xy=(w[0], w[1]))
        annot2 = plt.annotate(s='B', xy=(x[0], x[1]))
        annot3 = plt.annotate(s='C', xy=(y[0], y[1]))
        textEquation = pylab.text(.5, 1.05, str(w[-1]) + " : " + str(x[-1]) + " :: " + str(y[-1]) + " : x")
        pylab.savefig('img' + str(i + 9))
        # Clear the circles & txt
        for annot in [annot1, annot2, annot3]:
            annot.remove()
        textEquation.remove()

    # IMAGE 6 #
    plt.scatter(new[0], new[1], c=cl)
    pylab.savefig('img14')


def main(argv):
    # points= random_generation(50, 6)
    points= random_generation(5, 2)
    # points= group_generation(6, 10,.2)
    # points= percent_generation([0.05,0.25,0.15,0.25,0.1,0.2], 50,.2)
    classe = fadana([0.5,0.4], points, k=10)
    new = (.5, .4)
    classe, triplets, analogicalDiff = fadana(new, points, k=10)
    _draw(new, points, triplets, analogicalDiff, classe, plt)

    print("Class :", classe)


        # plt.show()

if(__name__ == "__main__"):
    sys.exit(main(sys.argv))
