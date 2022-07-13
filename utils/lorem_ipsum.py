#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import random

with open(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets/lorem_ipsum.txt")
) as f:
    LOREM_IPSUM = f.read().strip()
LOREM_SPLIT = LOREM_IPSUM.split("\n\n")
SPLIT_COUNT = len(LOREM_SPLIT)


def get_lorem_paragraphs(count=4, rand=0):
    OUT = ""
    if rand: rand = random.randint(0,SPLIT_COUNT)
    for i in range(count):
        OUT += LOREM_SPLIT[(i+rand) % SPLIT_COUNT] + "\n\n"
    return OUT
