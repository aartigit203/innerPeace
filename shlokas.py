shlokas = [

# 😔 ANXIETY / OVERWHELM
{
    "keywords": [
        "anxious", "anxiety", "panic", "overwhelmed", "stress",
        "i feel anxious", "i am stressed", "i feel panic"
    ],
    "verse": "Bhagavad-gita 2.14",
    "link": "https://vedabase.io/en/library/bg/2/14/",
    "message": """🌸 Krishna explains that happiness and distress are temporary—like changing seasons.

Right now, your mind may feel heavy, but this moment will pass.

✨ You are not your anxiety. You are the eternal soul—peaceful and steady by nature.

Instead of fighting the feeling, gently observe it… and bring your mind back to Krishna.

🧘 Try chanting slowly:
Hare Krishna Hare Krishna Krishna Krishna Hare Hare  
Hare Rama Hare Rama Rama Rama Hare Hare  

Let the sound calm your heart.

📖 Read full verse & purport:
https://vedabase.io/en/library/bg/2/14/

Krishna is always with you 💖"""
},

# 😢 SADNESS / DEPRESSION
{
    "keywords": [
        "sad", "depressed", "i feel low", "unhappy", "crying",
        "i feel empty", "i feel broken"
    ],
    "verse": "Bhagavad-gita 2.20",
    "link": "https://vedabase.io/en/library/bg/2/20/",
    "message": """🌸 Krishna reminds us that the soul is eternal—it never dies, never breaks.

What you are feeling now is real… but it is not your true identity.

✨ Deep within, you are full of peace, strength, and light.

Even in your lowest moments, Krishna is sitting in your heart, quietly supporting you.

You are never alone in this journey.

📖 Read full verse & purport:
https://vedabase.io/en/library/bg/2/20/

Stay close to Him 💖"""
},

# 😕 CONFUSION / LIFE DIRECTION
{
    "keywords": [
        "confused", "confusion", "lost", "no direction",
        "what should i do", "i dont know what to do",
        "feeling lost in life"
    ],
    "verse": "Bhagavad-gita 18.66",
    "link": "https://vedabase.io/en/library/bg/18/66/",
    "message": """🌸 When everything feels confusing, Krishna gives the simplest guidance:

✨ Surrender to Him.

You don’t have to solve life alone. When you align with Krishna, clarity naturally comes.

Take one small step with faith today.

Even if you don’t see the full path, He sees it for you.

📖 Read full verse & purport:
https://vedabase.io/en/library/bg/18/66/

Trust Him 💖"""
},

# 😡 ANGER / FRUSTRATION
{
    "keywords": [
        "angry", "anger", "frustrated", "irritated",
        "i feel angry", "i get angry easily"
    ],
    "verse": "Bhagavad-gita 2.63",
    "link": "https://vedabase.io/en/library/bg/2/63/",
    "message": """🌸 Krishna explains that anger clouds judgment and leads to confusion.

Right now, pause… breathe… step back.

✨ You are not your reaction—you have the power to choose peace.

Responding calmly is true strength.

📖 Read full verse & purport:
https://vedabase.io/en/library/bg/2/63/

Let Krishna guide your mind 💖"""
},

# 😞 FAILURE / SELF-DOUBT
{
    "keywords": [
        "failure", "i failed", "not good enough",
        "i feel useless", "mistake", "loser"
    ],
    "verse": "Bhagavad-gita 2.47",
    "link": "https://vedabase.io/en/library/bg/2/47/",
    "message": """🌸 Krishna teaches that your duty is to act—not to control results.

Failure does not define you.

✨ Every effort you make is valuable and part of your growth.

Even setbacks are steps forward in Krishna’s plan.

Keep going with faith.

📖 Read full verse & purport:
https://vedabase.io/en/library/bg/2/47/

You are stronger than you think 💪💖"""
},

# 🤍 LONELINESS
{
    "keywords": [
        "lonely", "alone", "no one cares",
        "i feel alone", "nobody understands me"
    ],
    "verse": "Bhagavad-gita 9.22",
    "link": "https://vedabase.io/en/library/bg/9/22/",
    "message": """🌸 Krishna personally cares for those who turn to Him.

Even if people don’t understand you, Krishna understands your heart completely.

✨ He is always with you—closer than anyone else.

You are deeply loved.

📖 Read full verse & purport:
https://vedabase.io/en/library/bg/9/22/

You are never truly alone 💖"""
},

# 🌍 PURPOSE OF LIFE
{
    "keywords": [
        "purpose of life", "what is purpose",
        "why are we here", "meaning of life",
        "what is the goal of life"
    ],
    "verse": "Bhagavad-gita 18.66",
    "link": "https://vedabase.io/en/library/bg/18/66/",
    "message": """🌸 The true purpose of life is to reconnect with Krishna.

We are not this body—we are eternal souls meant for loving relationship with Him.

✨ Everything else is temporary, but this connection is eternal.

By remembering, serving, and loving Krishna, life becomes meaningful and peaceful.

📖 Read full verse & purport:
https://vedabase.io/en/library/bg/18/66/

This is your real journey 💖"""
},

# 🧠 OVERTHINKING / RESTLESS MIND
{
    "keywords": [
        "overthinking", "too many thoughts",
        "restless mind", "mind not calm",
        "i cant stop thinking"
    ],
    "verse": "Bhagavad-gita 6.26",
    "link": "https://vedabase.io/en/library/bg/6/26/",
    "message": """🌸 The mind naturally wanders—but Krishna teaches how to guide it.

✨ Gently bring your mind back again and again.

Do not fight it harshly—guide it with patience.

With practice, peace will come.

📖 Read full verse & purport:
https://vedabase.io/en/library/bg/6/26/

Stay steady 💖"""
},

# 😨 FEAR OF FUTURE
{
    "keywords": [
        "fear of future", "future anxiety",
        "what will happen", "uncertain future"
    ],
    "verse": "Bhagavad-gita 4.7",
    "link": "https://vedabase.io/en/library/bg/4/7/",
    "message": """🌸 Krishna appears whenever there is imbalance—to protect and guide.

You don’t need to fear the future.

✨ Trust that everything is unfolding under divine care.

Walk forward with faith.

📖 Read full verse & purport:
https://vedabase.io/en/library/bg/4/7/

You are protected 💖"""
}

]

# 🔍 MATCH FUNCTION
def find_shloka_response(text):
    text_lower = text.lower()

    for item in shlokas:
        for keyword in item["keywords"]:
            if keyword in text_lower:
                return f"""Hare Krishna 🙏

Krishna says in {item['verse']}:

{item['message']}"""

    return None

