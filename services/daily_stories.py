daily_stories = [
{"day":1,"title":"Advent of Lord Krishna","text":"Krishna takes birth...","video":" https://youtu.be/94Kbj7DtBc4?si=Ah6TprrfOw9RnpMd&t=302"},
{"day":2,"title":"Prayers by DemiGods","text":"Prayers by DemiGods for LordKrishna in Womb","video":"https://youtu.be/EtMEKkGEbU8?si=lJGTghf2cZ8p3GKx"},
{"day":3,"title":"Killing Daemons","text":"Killing of Daemons.","video":"https://youtu.be/EUAj3IUQXb4?si=bveDWY0bWhzM1x9n"}
]

def get_daily_story(day):
    return daily_stories[(day-1) % len(daily_stories)]
