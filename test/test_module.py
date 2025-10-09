#! /usr/bin/env python
import sys
sys.path.append('../')
from time import time
from mjhand import MJHand, convert_34_array_to_string_dict

# Initialize the generator
mjh = MJHand()

# Sample 10 winning hands and print them
hands = mjh.sample_win_hand(10)
for i, h in enumerate(hands["hands"]):
    print(f'hand-{i:02d}:', h)

# Sample a winning hand
result = mjh.sample_win_hand(num_samples=1)
winning_hand = result["hands"][0]  # 34-array format
win_tile = result["win_tiles_onehot"][0]  # winning tile index

print(f"Winning hand: {winning_hand}")
print(f"Winning tile: {win_tile}")

# Convert to readable format
hand_dict = convert_34_array_to_string_dict(winning_hand)
print(f"Hand in readable format: {hand_dict}")

# Generate random hands for practice
random_hands = mjh.sample_random_hand(num_samples=5, num_tiles=14)
print(f"Random hands shape: {random_hands.shape}")

# Find similar winning hands
query_hand = random_hands[0]  # Use first random hand as query
t0 = time()
similar_hands = mjh.search_knn_win_hand(query_hand, k=1000)
print(f"Found {similar_hands['hands'].shape[1]} similar hands in {time() - t0:.2f} seconds")
print(f"Manhattan Distances: {similar_hands['manhattan'][:5]}")  # Show first 5 distances