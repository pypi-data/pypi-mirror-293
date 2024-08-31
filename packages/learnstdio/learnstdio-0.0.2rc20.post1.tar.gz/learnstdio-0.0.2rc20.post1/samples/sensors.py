#   ---------------------------------------------------------------------------------
#   Copyright (c) Learnstdio. All rights reserved.
#   Licensed under the MIT License. See LICENSE in project root for information.
#   ---------------------------------------------------------------------------------
"""This is sensors mock module, used as example illustration."""

def get_phase_iv(phase):
    """Return the current and voltage for PHASE"""
    if phase == 'a':
        return -64.59840133, 0.131668579
    if phase == 'b':
        return -34.48079878, -0.563834635
    if phase == 'c':
        return -27.25006492, 0.432166056
