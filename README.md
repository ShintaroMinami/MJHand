# MJHand

Japanese Riichi Mahjong Win-Hand Generator

[![Python](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

MJHand is a Python module for generating valid Japanese Riichi Mahjong winning hands (和了手).
## Features

- **Win-Hand Sampling**: Generate random valid winning hands based on theoretical hand frequencies
- **Random Hand Generation**: Create random 14-tile hands for simulation
- **Nearest Neighbor Search**: Find winning hands similar to a given query hand using Manhattan distance

## Installation

### From GitHub
```bash
pip install git+https://github.com/ShintaroMinami/MJHand.git
```

### From Source
```bash
git clone https://github.com/ShintaroMinami/MJHand.git
cd MJHand
pip install -e .
```

## Dependencies

- numpy
- tqdm

## Quick Start

```python
from mjhand import MJHand, convert_34_array_to_string_dict

# Initialize the generator
mj = MJHand()

# Sample a winning hand
result = mj.sample_win_hand(num_samples=1)
winning_hand = result["hands"][0]  # 34-element array format
win_tile = result["win_tiles"][0]  # winning tile index

print(f"Winning hand: {winning_hand}")
print(f"Winning tile: {win_tile}")

# Convert to readable format
hand_dict = convert_34_array_to_string_dict(winning_hand)
print(f"Hand in readable format: {hand_dict}")

# Generate random hands for practice
random_hands = mj.sample_random_hand(num_samples=5, num_tiles=14)
print(f"Random hands shape: {random_hands.shape}")

# Find similar winning hands
query_hand = random_hands[0]  # Use the first random hand as query
similar_hands = mj.search_knn_win_hand(query_hand, k=10)
print(f"Found {len(similar_hands['hands'])} similar hands")
print(f"Distances: {similar_hands['dist_manhattan'][:5]}")  # Show the first 5 distances
```

## Hand Representation

Hands are represented using the 34-element array format:
- Indices 0-8: 1-9 of man (萬子)
- Indices 9-17: 1-9 of pin (筒子) 
- Indices 18-26: 1-9 of sou (索子)
- Indices 27-33: East, South, West, North, White, Green, Red (字牌)

Each element in the array represents the count of that tile type (0-4).

## API Reference

### MJHand Class

#### `__init__(pkl_dir=None, seed=None)`
Initialize the MJHand generator.

**Parameters:**
- `pkl_dir` (str, optional): Directory containing pickle files with hand patterns
- `seed` (int, optional): Random seed for reproducibility

#### `sample_win_hand(num_samples=1)`
Sample valid winning hands from the database.

**Parameters:**
- `num_samples` (int): Number of hands to sample

**Returns:**
- `dict`: Dictionary containing:
  - `hands`: Array of winning hands (34-element array format)
  - `win_tiles`: Array of winning tile indices
  - `win_tiles_onehot`: One-hot encoded winning tiles

#### `sample_random_hand(num_samples=1, num_tiles=14)`
Generate random hands (not necessarily winning).

**Parameters:**
- `num_samples` (int): Number of hands to generate
- `num_tiles` (int): Number of tiles per hand (default: 14)

**Returns:**
- `numpy.ndarray`: Array of random hands in 34-element array format

#### `search_knn_win_hand(query_hand, k=1000)`
Find the k nearest winning hands to a query hand.

**Parameters:**
- `query_hand` (numpy.ndarray): Query hand in 34-element array format
- `k` (int): Number of nearest neighbors to return

**Returns:**
- `dict`: Dictionary containing:
  - `hands`: Array of the k nearest winning hands
  - `dist_manhattan`: Manhattan distances to the query hand

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
