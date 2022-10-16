import os
import configparser

id1 = 5502592053

config = configparser.ConfigParser()
if os.path.exists(f"Leveling/users/{id1}/data.ini"):
    data = open(f"Leveling/users/{id1}/data.ini", "a")
    config.read(f"Leveling/users/{id1}/data.ini")
    belvlprog = config.get("Level", "lvlprog")
    nowlvlprog = int(belvlprog)+1
    lvlprog = config.get("Level", "lvlprog")
    lvl = config.get("Level", "lvl")
    topprog = config.get("Level", "topprog")
    config.set("Level","lvlprog", f"{nowlvlprog}")
    if lvl == 0:
        config.set("Level","topprog", f"30")
    if lvlprog > topprog:
        if int(topprog) > 1:
            config.set("Level","lvlprog", "0")
            config.set("Level","lvl", f"{int(lvl)+1}")
        else:
            pass
    else:
        config.set("Level","topprog", f"{int(lvl)*3}")
    with open(f"Leveling/users/{id1}/data.ini", "w") as configfile:
        config.write(configfile)
    print(f"{lvlprog}/{topprog}, lvl:{lvl}")
else:
    os.mkdir(f"Leveling/users/{id1}")
    config.add_section("Level")
    config.set("Level","lvlprog", "1")
    config.set("Level","lvl", "0")
    config.set("Level","topprog", "10")
    with open(f"Leveling/users/{id1}/data.ini", "w") as configfile:
        config.write(configfile)
    lvlprog = config.get("Level", "lvlprog")
    print(lvlprog)