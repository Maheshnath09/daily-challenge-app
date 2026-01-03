"""
Seed script to populate database with sample challenges.
Run with: python -m app.seed_challenges
"""
import asyncio
from datetime import date, timedelta
from app.database import AsyncSessionLocal, create_tables
from app.models.challenge import Challenge, ChallengeCategory, ChallengeDifficulty


# Sample challenges for 14 days
SAMPLE_CHALLENGES = [
    # Day 1 - Easy Coding
    {
        "title": "FizzBuzz Classic",
        "description": """Write a function that prints numbers from 1 to 100.

**Rules:**
- For multiples of 3, print "Fizz" instead of the number
- For multiples of 5, print "Buzz" instead of the number  
- For multiples of both 3 and 5, print "FizzBuzz"

Submit your solution in any programming language.""",
        "category": ChallengeCategory.CODING,
        "difficulty": ChallengeDifficulty.EASY,
        "expected_output": "1, 2, Fizz, 4, Buzz, Fizz, 7, 8, Fizz, Buzz, 11, Fizz, 13, 14, FizzBuzz...",
    },
    # Day 2 - Medium Logic
    {
        "title": "River Crossing Puzzle",
        "description": """A farmer needs to cross a river with a wolf, a goat, and a cabbage.

**Constraints:**
- The boat can only carry the farmer and ONE item at a time
- If left alone, the wolf will eat the goat
- If left alone, the goat will eat the cabbage
- The wolf won't eat the cabbage

**Question:** What is the minimum number of crossings needed, and what is the sequence?

Submit your solution with the step-by-step sequence.""",
        "category": ChallengeCategory.LOGIC,
        "difficulty": ChallengeDifficulty.MEDIUM,
        "expected_output": "7 crossings",
    },
    # Day 3 - Hard Life
    {
        "title": "Cold Shower Challenge",
        "description": """Take a 2-minute cold shower.

**Rules:**
- Water must be COLD (not lukewarm)
- Full 2 minutes under the water
- No breaks or pauses

**Why?** Cold exposure builds mental resilience and discipline.

Mark complete when done. Be honest.""",
        "category": ChallengeCategory.LIFE,
        "difficulty": ChallengeDifficulty.HARD,
        "expected_output": None,
    },
    # Day 4 - Easy Logic
    {
        "title": "Pattern Recognition",
        "description": """What comes next in this sequence?

2, 6, 12, 20, 30, ?

Show your work and explain the pattern.""",
        "category": ChallengeCategory.LOGIC,
        "difficulty": ChallengeDifficulty.EASY,
        "expected_output": "42",
    },
    # Day 5 - Medium Coding
    {
        "title": "Palindrome Checker",
        "description": """Write a function that checks if a string is a palindrome.

**Requirements:**
- Ignore case (e.g., "Racecar" is a palindrome)
- Ignore spaces and punctuation
- Return true/false

**Test cases:**
- "A man a plan a canal Panama" → true
- "hello" → false
- "Was it a car or a cat I saw" → true""",
        "category": ChallengeCategory.CODING,
        "difficulty": ChallengeDifficulty.MEDIUM,
        "expected_output": "A function that handles edge cases",
    },
    # Day 6 - Easy Life
    {
        "title": "No Phone Morning",
        "description": """Don't check your phone for the first 30 minutes after waking up.

**Rules:**
- No social media
- No email
- No messages
- Alarm clock is allowed

**Instead:** Stretch, meditate, drink water, or just exist.

Mark complete when done. Be honest.""",
        "category": ChallengeCategory.LIFE,
        "difficulty": ChallengeDifficulty.EASY,
        "expected_output": None,
    },
    # Day 7 - Hard Coding
    {
        "title": "Binary Search Tree",
        "description": """Implement a Binary Search Tree with the following operations:

1. `insert(value)` - Insert a new value
2. `search(value)` - Return true if value exists
3. `delete(value)` - Remove a value
4. `inorder()` - Return sorted array of all values

Handle edge cases like duplicates and empty tree.""",
        "category": ChallengeCategory.CODING,
        "difficulty": ChallengeDifficulty.HARD,
        "expected_output": "Complete BST implementation with all methods",
    },
    # Day 8 - Medium Life
    {
        "title": "Talk to a Stranger",
        "description": """Have a genuine conversation with someone you don't know.

**Rules:**
- Must be in person (not online)
- At least 2 minutes of conversation
- Ask them a question about themselves
- Be genuinely curious

**Examples:** Coffee shop, gym, waiting in line, neighbor.

Describe the interaction briefly.""",
        "category": ChallengeCategory.LIFE,
        "difficulty": ChallengeDifficulty.MEDIUM,
        "expected_output": None,
    },
    # Day 9 - Hard Logic
    {
        "title": "Einstein's Riddle",
        "description": """There are 5 houses in 5 different colors. In each house lives a person of a different nationality. Each person drinks a different beverage, smokes a different brand of cigar, and keeps a different pet.

**Clues:**
1. The Brit lives in the red house.
2. The Swede keeps dogs.
3. The Dane drinks tea.
4. The green house is on the left of the white house.
5. The person in the green house drinks coffee.
6. The person who smokes Pall Mall has birds.
7. The person in the yellow house smokes Dunhill.
8. The person in the center house drinks milk.
9. The Norwegian lives in the first house.
10. The person who smokes Blends lives next to the one with cats.
11. The person who keeps horses lives next to Dunhill smoker.
12. The person who smokes BlueMaster drinks beer.
13. The German smokes Prince.
14. The Norwegian lives next to the blue house.
15. The person who smokes Blends has a neighbor who drinks water.

**Question:** Who owns the fish?""",
        "category": ChallengeCategory.LOGIC,
        "difficulty": ChallengeDifficulty.HARD,
        "expected_output": "The German owns the fish",
    },
    # Day 10 - Easy Coding
    {
        "title": "Reverse a String",
        "description": """Write a function to reverse a string WITHOUT using built-in reverse functions.

**Examples:**
- "hello" → "olleh"
- "12345" → "54321"
- "" → ""

Submit your solution with at least 2 different approaches.""",
        "category": ChallengeCategory.CODING,
        "difficulty": ChallengeDifficulty.EASY,
        "expected_output": "Multiple approaches shown",
    },
    # Day 11 - Medium Logic
    {
        "title": "The Monty Hall Problem",
        "description": """You're on a game show with 3 doors. Behind one door is a car. Behind the others, goats.

1. You pick a door (say, Door 1)
2. The host (who knows what's behind each door) opens another door (say, Door 3) showing a goat
3. The host asks: "Do you want to switch to Door 2?"

**Question:** Should you switch? Prove your answer mathematically.

Show the probability calculation.""",
        "category": ChallengeCategory.LOGIC,
        "difficulty": ChallengeDifficulty.MEDIUM,
        "expected_output": "Yes, switching gives 2/3 probability of winning",
    },
    # Day 12 - Hard Life
    {
        "title": "24-Hour Digital Detox",
        "description": """No recreational screen time for 24 hours.

**Allowed:**
- Work-related tasks (if absolutely necessary)
- Phone calls only

**Not allowed:**
- Social media
- Streaming services
- Games
- Mindless browsing

**Instead:** Read, exercise, talk to people, be bored.

Mark complete after 24 hours. Be honest.""",
        "category": ChallengeCategory.LIFE,
        "difficulty": ChallengeDifficulty.HARD,
        "expected_output": None,
    },
    # Day 13 - Medium Coding
    {
        "title": "Two Sum Problem",
        "description": """Given an array of integers and a target sum, find two numbers that add up to the target.

**Requirements:**
- Return the indices of the two numbers
- You may not use the same element twice
- Assume exactly one solution exists
- Optimize for O(n) time complexity

**Example:**
- Input: nums = [2, 7, 11, 15], target = 9
- Output: [0, 1] (because nums[0] + nums[1] = 9)""",
        "category": ChallengeCategory.CODING,
        "difficulty": ChallengeDifficulty.MEDIUM,
        "expected_output": "O(n) solution using hash map",
    },
    # Day 14 - Easy Logic
    {
        "title": "Light Bulb Problem",
        "description": """You have 3 light switches outside a room. Inside the room is 1 light bulb.

**Rules:**
- You can only enter the room ONCE
- You cannot see inside the room from outside
- The door is closed

**Question:** How can you determine which switch controls the bulb?

Explain your strategy.""",
        "category": ChallengeCategory.LOGIC,
        "difficulty": ChallengeDifficulty.EASY,
        "expected_output": "Use heat from the bulb",
    },
]


async def seed_challenges():
    """Seed the database with sample challenges."""
    await create_tables()
    
    async with AsyncSessionLocal() as db:
        # Check if challenges already exist
        from sqlalchemy import select
        result = await db.execute(select(Challenge))
        existing = result.scalars().first()
        
        if existing:
            print("Challenges already seeded. Skipping...")
            return
        
        # Seed challenges starting from today
        today = date.today()
        
        for i, challenge_data in enumerate(SAMPLE_CHALLENGES):
            active_date = today + timedelta(days=i)
            
            challenge = Challenge(
                title=challenge_data["title"],
                description=challenge_data["description"],
                category=challenge_data["category"],
                difficulty=challenge_data["difficulty"],
                expected_output=challenge_data.get("expected_output"),
                active_date=active_date,
                is_active=(i == 0)  # Only first challenge is active
            )
            
            db.add(challenge)
            print(f"Added challenge: {challenge.title} (Active: {active_date})")
        
        await db.commit()
        print(f"\n✓ Seeded {len(SAMPLE_CHALLENGES)} challenges successfully!")


if __name__ == "__main__":
    asyncio.run(seed_challenges())
