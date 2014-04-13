# algorithmic tone row composer
# Python 3 only
# Copyright 2014 Chris Muggli-Miller
# rontasu@gmail.com

# Free for personal use
# Do not redistribute without my permission

# Composes a 12-tone row using every tone in the Western chromatic scale exactly once.
# Instead of choosing each note at random, the program is given an awareness of
# the preceeding melodic interval, and it decides the next note based on that interval.
# The result is that the row sounds unusually melodic (tone rows normally sound dissonant),
# but it still adheres to the rule of using every note once and only once.

# I think of this as computer-assisted composing, not pure algorithmic composing, because
# the program doesn't have any say over the rules. All it does is give us a list of notes based on
# a predetermined set of rules. Another way to think of it
# is that the program is really just displacing some tedious calculations that a human
# would otherwise need to do.


import random # very important for decision-making...

# First, create a list of the display names for all of the notes.
alltones = ['C','C#','D','D#','E','F','F#','G','Ab','A','Bb','B']

# Here, we have to keep track of each note by marking it '1' so that the
# same note never gets used twice. Each position in the usedtones list corresponds to the respective note name in the alltones list.
usedtones = [0,0,0,0,0,0,0,0,0,0,0,0] # 0 = not yet used, 1 = already used

# Next, these two variables keep track of the last two notes that were chosen
# so that we can determine the interval that was between them.
previousnote = -1 # -1 means the note is yet undefined; valid range is 0-11
previousnote2 = -1

# This function checks whether the desired note is available. If it is, it returns the desired note.
# If not, it randomly chooses a new note. It will keep trying until it finds an available note.
def getNewNote(desiredpitch):
    while usedtones[desiredpitch] == 1:
        desiredpitch = random.randint(0, 11) # can't re-use a pitch, so pick a new one
    return desiredpitch

# This function moves from one pitch to another based on the chosen interval.
# An interval (for our purposes) is just a number specifying by how many semitones
# the pitch should be moved. I.e., an interval of '2' means return a new pitch
# that is two semitones higher than the given pitch.
def moveByInterval(pitchclass, interval):
    pitchclass += interval # move the pitch by 'interval' amount of semitones

    # wrap the new pitch into range, if necessary
    # (move it up or down by one octave so that it always falls between 0-11)
    if pitchclass < 0:
        pitchclass += 12
    elif pitchclass > 11:
        pitchclass -= 12

    return pitchclass

# start composing a tone row!
# pick a first pitch at random (musically, it doesn't matter what note comes first)
currentnote = random.randint(0, 11)
usedtones[currentnote] = 1

print(alltones[currentnote], end = ' ') # print each note as we choose it - this is how we display the row to the user

previousnote = currentnote

# pick a 2nd pitch
# Now we start to see some logic. Choose from the following list of pleasant-sounding
# intervals to determine the 2nd note. This way, the first interval in the row will always
# sound pleasing and never dissonant. (This rule is based on my musical opinion, and it doesn't
# have to be this way necessarily.)
intervaltype = random.randint(1, 4)
if intervaltype == 1: # use a major 3rd
    interval = 4
elif intervaltype == 2: # minor 3rd
    interval = 3
elif intervaltype == 3: # perfect 4th
    interval = 5
elif intervaltype == 4: # perfect 5th
    interval = 7

# store the last two chosen notes
previousnote2 = previousnote
previousnote = currentnote

currentnote = moveByInterval(previousnote, interval)
usedtones[currentnote] = 1

print(alltones[currentnote], end = ' ') # display the 2nd note we chose above

# now pick the next 10 pitches
# Here the decision-making logic is minimal. We could use more than this,
# but it turns out this works surprisingly well. We actually don't want TOO much logic
# or else the rules become too rigid and the program will compose the same
# thing every time.
for i in range(10):

    # keep record of the last two chosen notes...
    previousnote2 = previousnote
    previousnote = currentnote

    # get the interval of the last two notes
    previousinterval = previousnote2 - previousnote

    # intelligently choose a new pitch based on the interval between the previous two
    if previousinterval == 4:
        chance = random.randint(1, 4) # roll a 4-sided die, basically
        if chance == 1:
            currentnote = getNewNote(random.randint(0, 11)) # a 1-in-4 chance of skipping the logic and choosing randomly
            usedtones[currentnote] = 1
        else:
            currentnote = getNewNote(moveByInterval(previousnote, 3)) # if the previous interval was a minor 3rd, attempt to follow it with a major 2nd
            usedtones[currentnote] = 1
    elif previousinterval == 5:
        chance = random.randint(1, 4) # roll the die
        if chance == 1:
            currentnote = getNewNote(random.randint(0, 11))
            usedtones[currentnote] = 1
        else:
            currentnote = getNewNote(moveByInterval(previousnote, -4)) # if the previous interval was a major 3rd, attempt to follow by going down a minor 3rd
            usedtones[currentnote] = 1
    else:
        currentnote = getNewNote(random.randint(0, 11)) # if all else fails, just pick randomly
        usedtones[currentnote] = 1

    print(alltones[currentnote], end = ' ')

print('\nEnd of row!')
