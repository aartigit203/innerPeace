import random

MAX_BUTTON_LEN = 20  # WhatsApp hard limit

stories = [
    {
        "title": "Krishna the Butter Thief 🧈",
        "image": "https://i.imgur.com/3XK0Z6F.png",
        "audio": "",
        "text": """🌸 Krishna the Butter Thief 🧈
In the joyful village of Gokul, the gopis made fresh butter every day and hung it high from the ceiling.
But little Krishna always found a way to reach it!
With His friends, He made a human pyramid, climbed up, and broke the butter pots. Butter spilled everywhere, and Krishna happily shared it with His friends and even monkeys 🐒
One day, Mother Yashoda caught Him. Krishna looked innocent, but His butter-covered face told the truth 😄
Yashoda smiled and hugged Him lovingly.
💡 Learning: Krishna doesn't steal butter — He steals hearts.
🎯 Activity: Draw Krishna stealing butter.""",
        "quiz": {
            "question": "Why did Krishna steal butter?",
            "options": {
                "a": "He was hungry",       # 13 ✅
                "b": "He loved sharing",    # 16 ✅  (was 27 ❌)
                "c": "He wanted to hide it" # 20 ✅  (was 21 ❌)
            },
            "answer": "b"
        }
    },
    {
        "title": "Krishna and Kaliya 🐍",
        "image": "https://i.imgur.com/8Km9tLL.png",
        "audio": "",
        "text": """🌸 Krishna and Kaliya 🐍
The Yamuna river became poisonous because of a serpent named Kaliya.
Everyone was scared.
Krishna jumped into the river and faced the serpent bravely. Kaliya attacked, but Krishna danced on his heads and defeated him.
Finally, Kaliya surrendered, and Krishna forgave him.
The river became pure again 🌊✨
💡 Learning: Krishna removes negativity.
🎯 Activity: Draw Krishna dancing on Kaliya.""",
        "quiz": {
            "question": "What did Krishna do to Kaliya?",
            "options": {
                "a": "Ran away",            # 8  ✅
                "b": "Became friends",      # 13 ✅
                "c": "Danced on his heads"  # 19 ✅
            },
            "answer": "c"
        }
    },
    {
        "title": "Govardhan Lila 🌧️",
        "image": "https://i.imgur.com/F7z8p9O.png",
        "audio": "",
        "text": """🌸 Krishna Lifts Govardhan Hill 🌧️
Indra sent heavy rain to punish the villagers.
Krishna lifted Govardhan Hill with His little finger and protected everyone for 7 days.
Everyone stayed safe under the hill.
💡 Learning: Krishna protects His devotees.
🎯 Activity: Make a small hill using clay.""",
        "quiz": {
            "question": "How did Krishna protect them?",
            "options": {
                "a": "Built houses",        # 11 ✅
                "b": "Lifted a mountain",   # 16 ✅
                "c": "Stopped the rain"     # 14 ✅
            },
            "answer": "b"
        }
    },
    {
        "title": "Sudama and Krishna 🍚",
        "image": "https://i.imgur.com/B9xkY2T.png",
        "audio": "",
        "text": """🌸 Krishna and Sudama 🍚
Sudama was poor but loved Krishna deeply.
Krishna welcomed him with love and honored him.
Sudama returned home to find everything changed.
💡 Learning: True friendship is beyond wealth.
🎯 Activity: Say thank you to your friend.""",
        "quiz": {
            "question": "What did Sudama bring?",
            "options": {
                "a": "Gold",               # 4  ✅
                "b": "Fruits",             # 6  ✅
                "c": "Flattened Rice"      # 14 ✅  (was typo "Flattenned")
            },
            "answer": "c"
        }
    },
    {
        "title": "Putana Story 👶",
        "image": "https://i.imgur.com/6XgJ7Yk.png",
        "audio": "",
        "text": """🌸 Krishna and Putana 👶
Putana came to harm Krishna.
But Krishna gave her liberation.
💡 Learning: Krishna is merciful.
🎯 Activity: Color baby Krishna.""",
        "quiz": {
            "question": "Who was Putana?",
            "options": {
                "a": "A friend",           # 8  ✅
                "b": "A demon",            # 6  ✅  (fixed spelling too)
                "c": "A cow"               # 5  ✅
            },
            "answer": "b"
        }
    }
]


def _validate_stories():
    """Catch button length violations at startup, not silently at runtime."""
    for story in stories:
        quiz = story.get("quiz")
        if not quiz:
            continue
        for key, option in quiz["options"].items():
            assert len(option) <= MAX_BUTTON_LEN, (
                f"Story '{story['title']}' option '{key}' is {len(option)} chars "
                f"(max {MAX_BUTTON_LEN}): '{option}'"
            )

_validate_stories()  # runs once on import


def get_story():
    return random.choice(stories)







