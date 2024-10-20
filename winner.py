import argparse
import pymongo
import random
import os
from dotenv import load_dotenv

load_dotenv()

def connect_to_db():
    """Connect to MongoDB using environment variables."""
    client = pymongo.MongoClient(os.getenv("MONGO_URI"))
    db = client[os.getenv("DB_NAME")]
    return db


def choose_winner(prize_id, db):
    
    points_collection = db["f24-points-syst"]
    users_collection = db["users"]
    
    # Aggregate users and their buy-ins for the specific prize
    pipeline = [
        {"$unwind": "$buy_ins"},
        {"$match": {"buy_ins.prize_id": prize_id}},
        {"$project": {
            "email": 1,
            "buy_in": "$buy_ins.buy_in"
        }},
    ]

    users = list(points_collection.aggregate(pipeline=pipeline))
    if not users:
        return None

    total_buy_ins = sum(user['buy_in'] for user in users)

    # generate wining number between 0 and total_buy_ins
    winning_ticket = random.uniform(0, total_buy_ins)

    # find the winner
    cumulative_sum = 0
    for user_p in users:
        cumulative_sum += user_p["buy_in"]
        
        if cumulative_sum > winning_ticket:

            user = users_collection.find_one({"email": user_p["email"]})
            if user:
                return {**user_p, **user}
            else:
                return user_p

    # This should never happen, but just in case
    return users[-1]


def main():
    # Argument parsing for CLI input
    parser = argparse.ArgumentParser(
        description="Choose a winner for a prize based on buy-ins."
    )
    parser.add_argument(
        "prizes",
        metavar="prize",
        type=str,
        nargs="+",
        help="List of prize IDs to select winners for.",
    )

    args = parser.parse_args()
    prizes = args.prizes

    # Connect to database
    db = connect_to_db()

    # Select winners for each prize
    for prize_id in prizes:
        winner = choose_winner(prize_id, db)
        if winner:
            print(f"The winner of {prize_id} is:")
            print(f"  Email: {winner['email']}")
            print(
                f"  Name: {winner.get('first_name', 'N/A')} {winner.get('last_name', 'N/A')}"
            )
            print(f"  School: {winner.get('school', 'N/A')}")
            print(f"  Major: {winner.get('major', 'N/A')}")
            print(f"  Registration Status: {winner.get('registration_status', 'N/A')}")
            print(f"  Buy-in: {winner['buy_in']}")
            print()
        else:
            print(f"No participants found for {prize_id}")
            print()
            
            
if __name__ == "__main__":
    main()
