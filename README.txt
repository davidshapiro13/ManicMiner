And Or Star by David Shapiro
for AI Planning Course

How To Run:
- python3 ManicMiner.py
- View the Policy based on location
    (note  that I used coordinates from assingment, not same as internal)

Assumptions:
- Robot will try actions that are impossible so that probability moving in desired direction increases
- Robot is allowed in pothole and landslide state though not desirable
- There is no planned action in Goal state
- Robot can only move up, down, left and right
- Policy does not need to have an action for every state

We don't need the discount factor (gamma) in this problem because we want all the
rewards (or in our case, costs) to be equally effective, regardless of time so that would
mean setting gamma to 1 which is also really the same as just not including it at all.

KNOWN PROBLEM WITH CODE:

My algorithm thinks the robot should move right from it's start even though if the robot could see the
bigger picture, it would notice that that is a bad idea overall. I wasn't able to fix that bug though even
though I tried a lot. I believe because of this bug, it also didn't include Spot (1, 4) in the policy.
Any advice would be appreciated. 

I researched python syntax qyestions online in additon to AO* explainations