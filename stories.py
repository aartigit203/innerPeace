import random

stories = [

{
"title": "Krishna the Butter Thief 🧈",
"image": "https://i.imgur.com/3XK0Z6F.png",
"audio": "",  # 👉 add narration link later
"text": """🌸 Krishna the Butter Thief 🧈

In the joyful village of Gokul, the gopis made fresh butter every day and hung it high from the ceiling.

But little Krishna always found a way to reach it!

With His friends, He made a human pyramid, climbed up, and broke the butter pots. Butter spilled everywhere, and Krishna happily shared it with His friends and even monkeys 🐒

One day, Mother Yashoda caught Him. Krishna looked innocent, but His butter-covered face told the truth 😄

Yashoda smiled and hugged Him lovingly.

💡 Learning: Krishna doesn’t steal butter — He steals hearts.

🎯 Activity: Draw Krishna stealing butter."""
,

    "quiz": {
    "question": "Why did Krishna steal butter?",
    "options": {
        "a": "He was hungry ",
        "b": "He loved butter and sharing",
        "c": "He wanted to hide it "
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

🎯 Activity: Draw Krishna dancing on Kaliya."""
,
    "quiz": {
    "question": "What did Krishna do to Kaliya?",
    "options": {
        "a": "Ran away ",
        "b": "Became friends ",
        "c": "Danced on his heads"
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

🎯 Activity: Make a small hill using clay."""
,
    "quiz": {
    "question": "How did Krishna protect villagers?",
    "options": {
        "a": "Built houses ",
        "b": "Lifted mountain",
        "c": "Stopped rain "
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

🎯 Activity: Say thank you to your friend."""
,
    "quiz": {
    "question": "What did Sudama bring?",
    "options": {
        "a": "Gold",
        "b": "Fruits",
        "c": "Flattenned Rice"
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

🎯 Activity: Color baby Krishna."""
,
    "quiz": {
    "question": "Who was Putana?",
    "options": {
        "a": "Friend",
        "b": "Daemon",
        "c": "Cow"
    },
    "answer": "b"
}

}

]

def get_story():
    return random.choice(stories)
