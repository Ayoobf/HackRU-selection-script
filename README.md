# Winner Script

This script chooses a winner from the f24-points-syst collection.

## Choosing a winner

### Algorithm explanation

1. We aggregate the f24-points-syst data for each prize.
1. Sum all buy-ins for each prize to give total sample size.
1. Generate the wining ticket number between 0 and sample size.
1. We iterate through the list of participants. For each participant, we add their buy-ins to a cumulative sum. When this cumulative sum exceeds our "winning ticket" number, we've found our winner.

#### Complexity

Time and space complexity are both O(n).

## Setup

1. **Install the package:**

   You can install the package directly using pip from the local directory:

   ```bash
   pip install .
   ```

   Alternatively, if you prefer to install the dependencies separately, run:

   ```bash
   pip install -r requirements.txt
   ```

2. **Create a `.env` file** with the following fields:

   - `MONGO_URI`: Your MongoDB connection string.
   - `DB_NAME`: The name of the database that contains the collections.

## Usage

Run the script using the `winner` command, which is now available as a console script:

- **To choose winners for all prizes:**

   ```bash
   winner
   ```

- **To choose winners for specific prizes:**

   ```bash
   winner prizeA 
   ```

   or

   ```bash
   winner prizeA prizeB prizeC
   ```
   