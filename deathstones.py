# 0:Insanity, 1:Plague, 2:Hunger, 3:Mana 4:Body, 5:Level, 6:Death, 7:Divine, 8:Neutral

import numpy as np
import random
import argparse

parser = \
    argparse.ArgumentParser(description='Calculate stone probabilities.'
                            )

parser.add_argument('--insanity',
                    help='the number of insanity stones to put in',
                    default=4, type=int)
parser.add_argument('--plague',
                    help='the number of plague stones to put in',
                    default=0, type=int)
parser.add_argument('--hunger',
                    help='the number of hunger stones to put in',
                    default=0, type=int)
parser.add_argument('--mana', help='the number of mana stones to put in'
                    , default=4, type=int)
parser.add_argument('--body', help='the number of body stones to put in'
                    , default=4, type=int)
parser.add_argument('--level',
                    help='the number of level stones to put in',
                    default=4, type=int)
parser.add_argument('--death',
                    help='the number of death stones to put in',
                    default=3, type=int)
parser.add_argument('--divine',
                    help='the number of divine stones to put in',
                    default=10, type=int)
parser.add_argument('--neutral',
                    help='the number of neutral stones to put in',
                    default=13, type=int)
parser.add_argument('--freeDivines',
                    help='the number of free divine stones', default=0,
                    type=int)
parser.add_argument('--numTests', help='the number of times to test',
                    default=1e5, type=int)
parser.add_argument('--numStonesPulled',
                    help='the number of stones to pull', default=5,
                    type=int)
parser.add_argument('--setSize',
                    help='The required size of sets', default=3,
                    type=int)

args = parser.parse_args()

numTests = int(args.numTests)
numStonesPulled = int(args.numStonesPulled)
numFreeStones = args.freeDivines
setSize = int(args.setSize)
outcomeCodes = [
    'Death',
    'Level',
    'Body',
    'Mana',
    'Hunger',
    'Plague',
    'Insanity',
    'Neutral',
    'Teir 1 Blessing',
    'Teir 2 Blessing',
    'Teir 3 Blessing',
    'Teir 4 Blessing',
    'Teir 5+ Blessing',
    ]
stoneCounts = [  # Describes the number of each stone in the pile
    args.insanity,
    args.plague,
    args.hunger,
    args.mana,
    args.body,
    args.level,
    args.death,
    args.divine,
    args.neutral,
    ]
# print(str(stoneCounts))
print "total stones: {}".format(sum(stoneCounts))

checkpointEvery = 10000  # Say that your progress every this many tests


def findStoneCounts(selectedStones, numStoneTypes):

# Given a list of stones states the count of each type of stone

    selectedStoneCounts = np.zeros(numStoneTypes)
    for stone in selectedStones:
        selectedStoneCounts[int(stone)] += 1
    return selectedStoneCounts

# This function is not needed. 
def reduceStones(selectedStoneCounts):

    # reduces the stones so that white stones are removed to counter other stones, in the order based on the order of sevirity on top of the doc

    selectedStoneCounts[7] += numFreeStones  # Adds some Divine Stones to your pool

    # for i in [5,4,3,2,1,0]:

    for i in [0,1,2,3,4,5]:
        reduce = min(selectedStoneCounts[i], selectedStoneCounts[7])  # Reduce both by the smallest amount that will make
        selectedStoneCounts[i] -= reduce
        selectedStoneCounts[7] -= reduce
    return selectedStoneCounts


def findStoneOutcome(stones):

    # Finds what effect the stones do. Must have reducStones stone values as an input
    # Output values: 0:PD, 1:level, 2: Body, 3: Mana, 4: Hunger, 5: Plague, 6: Insanity, 7: Neutral, 8: teir 1 blessing, 9: teir 2 blessing, 10: teir 3 blessing, 11: teir 4 blessing, 12: teir 5+ blessing
    # print(stones)

    death = stones[6]
    level = stones[5]
    body = stones[4]
    mana = stones[3]
    hunger = stones[2]
    plague = stones[1]
    insanity = stones[0]
    divine = stones[7]
    neutral = stones[8]
    if death >= setSize:
        return 0 # PD
    elif level >= setSize:
        return 1 # Level
    elif body >= setSize:
        return 2 # body
    elif mana >= setSize:
        return 3 #Mana
    elif insanity >= setSize:
        return 6 #Insanity
    elif divine >= setSize:
        return 8 #T1 blessing
    else:
        return 7
    #raise ValueError('the input for this function is bad')


# Output values: 0:PD, 1:level, 2: Body, 3: Mana, 4: Hunger, 5: Plague, 6: Insanity, 7: Neutral, 8: teir 1 blessing, 9: teir 2 blessing, 10: teir 3 blessing, 11: teir 4 blessing, 12: teir 5+ blessing

# Generates the list of the stones based on the amounts

def pullStones(numStonesPulled):
    stones = np.array([])
    for i in range(len(stoneCounts)):
        for j in range(stoneCounts[i]):
            stones = np.append(stones, [i])

    allStoneCodes = np.zeros(len(outcomeCodes))  # list of all the randomly generated modes of stones.
    for i in range(numTests):
        selectedStones = np.array(random.sample(stones,
                                  numStonesPulled))  # All the stones that were randomly chosen
        selectedStoneCounts = findStoneCounts(selectedStones,
                len(stoneCounts))  # The quantities of the stones that were randomly chosen
        effectCode = findStoneOutcome(selectedStoneCounts)
        allStoneCodes[int(effectCode)] += 1
        if i % checkpointEvery == 0:
            print 'CHECKPOINT: {0}% done.'.format(str(100 * float(i)
                    / float(numTests)))

    print '''
STONES USED:
{} Insanity stones 
{} plague stones
{} hunger stones
{} mana stones
{} body stones
{} level stones
{} death stones
{} divine stones
{} neutral stones'''.format(
        args.insanity,
        args.plague,
        args.hunger,
        args.mana,
        args.body,
        args.level,
        args.death,
        args.divine,
        args.neutral,
        )

    print 'Pulling {} stones, with {} free divine stones'.format(args.numStonesPulled,
            args.freeDivines)
    print 'Tested {} times'.format(int(args.numTests))

    # print "\n{} Stones: ---------------------------------".format(numStonesPulled)

    print '\nRESAULTS:'
    for i in range(len(allStoneCodes)):

        # print(str(100*float(allStoneCodes[i])/float(numTests)))

        print '{}: {}%'.format(outcomeCodes[i], str(100
                               * float(allStoneCodes[i])
                               / float(numTests)))


    # for i in [0,1,2,3,6,7]:
    #    print(str(100*float(allStoneCodes[i])/float(numTests)) + "%")
    # numBlessings = allStoneCodes[8]+allStoneCodes[9]+allStoneCodes[10]+allStoneCodes[11]+allStoneCodes[12]
    # print(str(100*float(numBlessings)/float(numTests)) + "%")
# for i in range(4,30):
#    pullStones(i)

pullStones(numStonesPulled)
