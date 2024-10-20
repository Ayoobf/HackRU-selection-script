# Winner Script

This script chooses a winner from the f24-points-syst collection.

## Choosing a winner

### Algorithm explanation

1. We aggregate the f24-points-syst data for each prize.
1. Sum all buy-ins for each prize to give total sample size.
1. Generate the wining ticket number between 0 and sample size.
1. We iterate through the list of participants. For each participant, we add their buy-ins to a cumulative sum. When this cumulative sum exceeds our "winning ticket" number, we've found our winner.

#### Complexity

Time and space complexity are both O(n)

## Setup

1. Install dependencies

```python
pip install -r requirements.txt
```

2. Create a `.env` file with `MONGO_URI` and `DB_NAME` fields
3. Run the script `python winner.py`
