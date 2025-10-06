#! /usr/bin/env python

from mjhand import MJHand, convert_34_array_to_string_dict

mjhand = MJHand()
hand_1000 = mjhand.sample_win_hand(1000)
for h in hand_1000["hands"]:
    hand_dict = convert_34_array_to_string_dict(h)
    print(hand_dict)