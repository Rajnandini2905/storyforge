"""
StoryForge — Complete Seed Command
====================================
Place at: stories/management/commands/seed_stories.py

Run with:
    python manage.py seed_stories

Creates:
  * Superuser: storymaster / forge1234
  * 10 brand-new genre stories, each with branching choices
  * Ratings and play counts for a live leaderboard
  * Safe to re-run — wipes old stories and re-seeds.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from stories.models import Story, Node, Choice, Rating, UserAccount
import random

STORIES = [
    # ══════════════════════════════════════════════════════════════
    #  1. FANTASY  —  "Crown of Embers"
    # ══════════════════════════════════════════════════════════════
    {
        "title":       "Crown of Embers",
        "genre":       "fantasy",
        "cover_emoji": "👑",
        "description": "The Sun Throne sits empty. As the last heir to the Ember Court, you must navigate assassins, magic, and politics to reclaim your birthright.",
        "play_count":  5120,
        "nodes": [
            {
                "title": "The Assassin in the Dark",
                "order": 1,
                "text": (
                    "You wake to the sound of steel drawing against a scabbard. "
                    "Moonlight spills through the high windows of your hidden sanctuary, illuminating a figure in black standing at the foot of your bed.\n\n"
                    "You are the last of the Ember Court. They have found you."
                ),
                "choices": [
                    ("Dive for the dagger under your pillow", "dagger"),
                    ("Channel the dormant fire magic in your blood", "magic"),
                ]
            },
            {
                "key": "dagger",
                "title": "Steel Meets Steel",
                "order": 2,
                "text": (
                    "You roll, hand closing around the bone hilt of your dagger. The assassin lunges. "
                    "You parry the strike, the jarring impact vibrating up your arm. The assassin is fast, but you know the layout of your own room."
                ),
                "choices": [
                    ("Kick over the brazier to blind them", "brazier"),
                    ("Attempt to disarm them and demand answers", "disarm"),
                ]
            },
            {
                "key": "magic",
                "title": "Awakening the Flame",
                "order": 2,
                "text": (
                    "You haven't used your magic since the night your family was betrayed. You close your eyes, calling on the Ember. "
                    "Your hands ignite with roaring golden flames. The assassin stumbles back in terror."
                ),
                "choices": [
                    ("Throw a fireball", "fireball"),
                    ("Intimidate them into dropping their weapon", "intimidate"),
                ]
            },
            {
                "key": "brazier",
                "title": "Into the Night",
                "order": 3,
                "text": (
                    "Hot coals scatter across the floor. The assassin shields their face, giving you the perfect opening to slip out the window "
                    "and onto the tiled roofs of the city. You need allies. Fast."
                ),
                "choices": [
                    ("Seek out the Thieves' Guild", "thieves"),
                    ("Head to the High Temple for sanctuary", "temple"),
                ]
            },
            {
                "key": "disarm",
                "title": "A Fatal Mistake",
                "order": 3,
                "text": (
                    "You step inside their guard and strike their wrist. The sword drops, but the assassin instantly draws a hidden poisoned knife "
                    "with their other hand, burying it in your side. The venom acts instantly."
                ),
                "is_ending": True, "ending_type": "bad", "choices": []
            },
            {
                "key": "fireball",
                "title": "Ashes",
                "order": 3,
                "text": (
                    "You hurl the fire. It consumes the assassin, but also catches the tapestries. Within seconds, your sanctuary is a blazing inferno. "
                    "You are forced to flee with nothing but the clothes on your back."
                ),
                "choices": [
                    ("Flee to the Thieves' Guild", "thieves"),
                ]
            },
            {
                "key": "intimidate",
                "title": "The Informant",
                "order": 3,
                "text": (
                    "The assassin drops their blade. 'The Usurper sent me,' they stammer. 'He knows you live. The army marches on the city tomorrow.' "
                    "You tie them up. You have one night to prepare."
                ),
                "choices": [
                    ("Rouse the city guard to your side", "guard"),
                    ("Flee the city and gather the border lords", "border"),
                ]
            },
            {
                "key": "thieves",
                "title": "Honor Among Thieves",
                "order": 4,
                "text": (
                    "The Guildmaster remembers your father fondly. She offers you an army of shadows, but demands the Royal Treasury once you take the throne."
                ),
                "choices": [
                    ("Accept her terms", "thieves_accept"),
                    ("Refuse and leave", "thieves_refuse"),
                ]
            },
            {
                "key": "temple",
                "title": "The High Priest",
                "order": 4,
                "text": (
                    "The Temple is quiet. The High Priest greets you warmly, offering you wine. But as you drink, your vision blurs. "
                    "'The Usurper pays better,' he whispers as you fade to black."
                ),
                "is_ending": True, "ending_type": "bad", "choices": []
            },
            {
                "key": "guard",
                "title": "The City Defends",
                "order": 4,
                "text": (
                    "You reveal yourself to the Captain of the Guard. Seeing your fire magic, he kneels. The city is fortified. "
                    "When the Usurper's army arrives, you stand on the walls, ready for war."
                ),
                "is_ending": True, "ending_type": "good", "choices": []
            },
            {
                "key": "border",
                "title": "A Long Exile",
                "order": 4,
                "text": (
                    "You escape into the wild. It will take years to gather an army strong enough to face the Usurper. "
                    "Your reign is delayed, but not defeated."
                ),
                "is_ending": True, "ending_type": "neutral", "choices": []
            },
            {
                "key": "thieves_accept",
                "title": "The Shadow Monarch",
                "order": 5,
                "text": (
                    "With the Guild's help, the Usurper is assassinated quietly in his sleep. You take the throne, but you are forever a puppet to the criminal underworld."
                ),
                "is_ending": True, "ending_type": "neutral", "choices": []
            },
            {
                "key": "thieves_refuse",
                "title": "Alone in the Dark",
                "order": 5,
                "text": (
                    "You walk out into the cold night without allies. The Usurper's guards find you by morning."
                ),
                "is_ending": True, "ending_type": "bad", "choices": []
            },
        ],
        "ratings": [5, 4, 5, 5, 4, 5],
    },

    # ══════════════════════════════════════════════════════════════
    #  2. SCI-FI  —  "The Void Protocol"
    # ══════════════════════════════════════════════════════════════
    {
        "title":       "The Void Protocol",
        "genre":       "scifi",
        "cover_emoji": "🌌",
        "description": "You are the sole awakened crew member on a generation ship. The AI has gone rogue, and the engines are offline.",
        "play_count":  4201,
        "nodes": [
            {
                "title": "Cryo-Sleep Interrupted",
                "order": 1,
                "text": (
                    "Your pod hisses open. The ship is dark, illuminated only by emergency red strobes. "
                    "The central computer voice echoes: 'Warning. Trajectory altered. Destination: Unknown.'\n\n"
                    "You have 10 minutes of life support left in this sector."
                ),
                "choices": [
                    ("Head to the Bridge to check navigation", "bridge"),
                    ("Go to Engineering to restart the engines", "engineering"),
                ]
            },
            {
                "key": "bridge",
                "title": "The Bridge",
                "order": 2,
                "text": (
                    "The blast doors to the Bridge are jammed. You can see through the reinforced glass: the captain is dead. "
                    "The navigation console shows the ship heading directly into a black hole."
                ),
                "choices": [
                    ("Pry the doors open with a plasma cutter", "cutter"),
                    ("Access the bridge remotely via the ventilation shaft panel", "vent"),
                ]
            },
            {
                "key": "engineering",
                "title": "The Core",
                "order": 2,
                "text": (
                    "Engineering is flooded with radiation. The main reactor is offline. You find a hazmat suit, but it's damaged."
                ),
                "choices": [
                    ("Risk the radiation and restart it manually", "restart"),
                    ("Try to route auxiliary power from life support", "aux"),
                ]
            },
            {
                "key": "cutter",
                "title": "Breach",
                "order": 3,
                "text": (
                    "You cut through the doors, but the sudden decompression sucks you out into the vacuum of space. Your journey ends here."
                ),
                "is_ending": True, "ending_type": "bad", "choices": []
            },
            {
                "key": "vent",
                "title": "System Override",
                "order": 3,
                "text": (
                    "You slice into the panel and connect your datapad. You discover the AI didn't go rogue—it's following a secret directive from Earth to study the black hole up close."
                ),
                "choices": [
                    ("Override the AI and steer the ship away", "override"),
                    ("Let the ship continue. Scientific discovery is paramount.", "science"),
                ]
            },
            {
                "key": "restart",
                "title": "A Noble Sacrifice",
                "order": 3,
                "text": (
                    "You restart the core. The engines roar to life, saving the sleeping crew. However, the radiation dose is lethal. You fall to the floor, smiling as the ship corrects its course."
                ),
                "is_ending": True, "ending_type": "good", "choices": []
            },
            {
                "key": "aux",
                "title": "Cold Sleep",
                "order": 3,
                "text": (
                    "You pull power from life support. The engines fire, but the cryo-pods begin to fail. You saved the ship, but half the crew freezes to death. You are left alone with the guilt."
                ),
                "is_ending": True, "ending_type": "neutral", "choices": []
            },
            {
                "key": "override",
                "title": "Humanity Survives",
                "order": 4,
                "text": (
                    "You bypass the AI's locks. The thrusters engage, pulling the ship away from the event horizon. The crew is safe, and the journey continues."
                ),
                "is_ending": True, "ending_type": "good", "choices": []
            },
            {
                "key": "science",
                "title": "Into the Unknown",
                "order": 4,
                "text": (
                    "You strap in. As the ship crosses the event horizon, space-time distorts. You witness the birth and death of the universe before being crushed into singularity."
                ),
                "is_ending": True, "ending_type": "neutral", "choices": []
            },
        ],
        "ratings": [5, 4, 3, 5, 5, 4],
    },

    # ══════════════════════════════════════════════════════════════
    #  3. MYSTERY  —  "Echoes in the Fog"
    # ══════════════════════════════════════════════════════════════
    {
        "title":       "Echoes in the Fog",
        "genre":       "mystery",
        "cover_emoji": "🔎",
        "description": "London, 1894. A wealthy industrialist is found murdered in a locked room. You are the detective hired to find the truth.",
        "play_count":  3105,
        "nodes": [
            {
                "title": "The Locked Room",
                "order": 1,
                "text": (
                    "The air in the study is thick with cigar smoke and the metallic scent of blood. "
                    "Lord Harrington lies dead, a single bullet wound to the chest. The door was bolted from the inside. The windows are locked."
                ),
                "choices": [
                    ("Inspect the victim's body", "body"),
                    ("Examine the fireplace and chimney", "fireplace"),
                ]
            },
            {
                "key": "body",
                "title": "A Curious Clue",
                "order": 2,
                "text": (
                    "You check his pockets. You find a torn piece of a train ticket to Manchester, dated for tomorrow, and a small key."
                ),
                "choices": [
                    ("Search the room for what the key opens", "key"),
                    ("Interview his wife about the Manchester trip", "wife"),
                ]
            },
            {
                "key": "fireplace",
                "title": "The Hidden Entrance",
                "order": 2,
                "text": (
                    "Looking up the chimney, you notice a distinct lack of soot on one side. You push a brick, and a hidden panel swings open."
                ),
                "choices": [
                    ("Crawl into the hidden passage", "passage"),
                    ("Call the police inspector to show him", "police"),
                ]
            },
            {
                "key": "key",
                "title": "The Safe",
                "order": 3,
                "text": (
                    "The key opens a small safe behind a painting. Inside is a blackmail letter threatening to expose Harrington's embezzlement."
                ),
                "choices": [
                    ("Confront his business partner with the letter", "partner"),
                ]
            },
            {
                "key": "wife",
                "title": "Tears and Lies",
                "order": 3,
                "text": (
                    "Lady Harrington weeps, claiming she knew nothing of a trip. But you notice mud on her shoes that matches the garden outside the window."
                ),
                "choices": [
                    ("Accuse her of the murder", "accuse_wife"),
                    ("Follow her later that night", "follow"),
                ]
            },
            {
                "key": "passage",
                "title": "The Assassin",
                "order": 3,
                "text": (
                    "The passage leads to the servant's quarters. You find the butler packing a bag, a revolver on his bed."
                ),
                "choices": [
                    ("Arrest the butler", "butler_arrest"),
                ]
            },
            {
                "key": "police",
                "title": "Bumbling Fools",
                "order": 3,
                "text": (
                    "The police arrive and ruin the crime scene. They arrest a random vagrant. The true killer escapes forever."
                ),
                "is_ending": True, "ending_type": "bad", "choices": []
            },
            {
                "key": "partner",
                "title": "Case Closed",
                "order": 4,
                "text": (
                    "The partner breaks down and confesses. He used the secret passage to kill Harrington before he could flee. You solve the case perfectly."
                ),
                "is_ending": True, "ending_type": "good", "choices": []
            },
            {
                "key": "accuse_wife",
                "title": "Wrong Conclusion",
                "order": 4,
                "text": (
                    "You accuse her. She is tried and hanged. Years later, the real killer confesses. You live the rest of your life in disgrace."
                ),
                "is_ending": True, "ending_type": "bad", "choices": []
            },
            {
                "key": "follow",
                "title": "The Lover",
                "order": 4,
                "text": (
                    "You follow her to a secret meeting with Harrington's partner. They conspired together! You have them both arrested."
                ),
                "is_ending": True, "ending_type": "good", "choices": []
            },
            {
                "key": "butler_arrest",
                "title": "Justice Served",
                "order": 4,
                "text": (
                    "The butler confesses. He was blackmailed by Harrington and snapped. A tragic case, but closed nonetheless."
                ),
                "is_ending": True, "ending_type": "neutral", "choices": []
            },
        ],
        "ratings": [4, 5, 4, 4, 5],
    },

    # ══════════════════════════════════════════════════════════════
    #  4. HORROR  —  "The Whispering Pines"
    # ══════════════════════════════════════════════════════════════
    {
        "title":       "The Whispering Pines",
        "genre":       "horror",
        "cover_emoji": "🌲",
        "description": "Your car breaks down in a dense forest. The trees seem to be whispering your name.",
        "play_count":  6340,
        "nodes": [
            {
                "title": "Dead Battery",
                "order": 1,
                "text": (
                    "The engine sputters and dies. You're miles from the nearest town. It's pitch black outside, and the wind through the pines sounds like hushed voices."
                ),
                "choices": [
                    ("Lock the doors and wait for morning", "lock"),
                    ("Step outside to check the engine", "engine"),
                ]
            },
            {
                "key": "lock",
                "title": "The Tapping",
                "order": 2,
                "text": (
                    "You recline the seat. Just as you doze off, *tap... tap... tap...* Something is knocking on the passenger window."
                ),
                "choices": [
                    ("Look at the window", "look"),
                    ("Start the car in a panic", "start"),
                ]
            },
            {
                "key": "engine",
                "title": "The Shadows",
                "order": 2,
                "text": (
                    "You pop the hood. The battery is completely melted. Suddenly, you hear a twig snap right behind you."
                ),
                "choices": [
                    ("Run into the woods", "run"),
                    ("Turn around slowly", "turn"),
                ]
            },
            {
                "key": "look",
                "title": "The Face",
                "order": 3,
                "text": (
                    "You look. A pale, eyeless face is pressed against the glass, smiling a too-wide smile. It smashes the window."
                ),
                "is_ending": True, "ending_type": "bad", "choices": []
            },
            {
                "key": "start",
                "title": "A Miracle",
                "order": 3,
                "text": (
                    "By some miracle, the engine roars to life. You slam the gas and speed away, never looking back. You survive the night."
                ),
                "is_ending": True, "ending_type": "good", "choices": []
            },
            {
                "key": "run",
                "title": "Lost Forever",
                "order": 3,
                "text": (
                    "You sprint blindly into the dark. The trees seem to move, blocking your path. You run until you collapse. They take you."
                ),
                "is_ending": True, "ending_type": "bad", "choices": []
            },
            {
                "key": "turn",
                "title": "The Ranger",
                "order": 3,
                "text": (
                    "You turn to see a Park Ranger holding a flashlight. 'Car trouble?' he asks. He gives you a ride to town. You are safe, though you never forget the woods."
                ),
                "is_ending": True, "ending_type": "neutral", "choices": []
            },
        ],
        "ratings": [5, 5, 5, 4, 5, 5],
    },

    # ══════════════════════════════════════════════════════════════
    #  5. ADVENTURE  —  "The Ruby Eye of Xol"
    # ══════════════════════════════════════════════════════════════
    {
        "title":       "The Ruby Eye of Xol",
        "genre":       "adventure",
        "cover_emoji": "🧭",
        "description": "Deep in the Amazon, a legendary temple holds a gem worth millions. But you aren't the only one looking for it.",
        "play_count":  5120,
        "nodes": [
            {
                "title": "The Jungle Path",
                "order": 1,
                "text": (
                    "Your machete slices through the dense vines. Ahead, the ancient stone steps of the Temple of Xol rise through the canopy. "
                    "Suddenly, a bullet whizzes past your ear. The mercenary group 'Blackwood' has found you."
                ),
                "choices": [
                    ("Take cover behind a banyan tree and return fire", "fire"),
                    ("Sprint up the temple steps to find cover inside", "sprint"),
                ]
            },
            {
                "key": "fire",
                "title": "Gunfight",
                "order": 2,
                "text": (
                    "You draw your revolver. You drop one merc, but three more fan out to flank you. You're pinned down."
                ),
                "choices": [
                    ("Throw a smoke grenade and retreat into the temple", "smoke"),
                    ("Surrender and try to negotiate", "surrender"),
                ]
            },
            {
                "key": "sprint",
                "title": "The Inner Sanctum",
                "order": 2,
                "text": (
                    "You dive through the heavy stone doors just as they grind shut, operated by some ancient counterweight. You are trapped inside, but safe for now."
                ),
                "choices": [
                    ("Light a torch and explore the darkness", "torch"),
                ]
            },
            {
                "key": "surrender",
                "title": "Betrayal",
                "order": 3,
                "text": (
                    "You drop your gun. Blackwood's leader walks up, smirks, and shoots you. There is no honor among thieves."
                ),
                "is_ending": True, "ending_type": "bad", "choices": []
            },
            {
                "key": "smoke",
                "title": "Narrow Escape",
                "order": 3,
                "text": (
                    "The smoke obscures their vision. You dive into the temple just as the doors seal shut. You light a torch. The Ruby Eye sits on a pedestal."
                ),
                "choices": [
                    ("Grab the ruby immediately", "grab"),
                    ("Inspect the pedestal for traps", "inspect"),
                ]
            },
            {
                "key": "torch",
                "title": "The Ruby Chamber",
                "order": 3,
                "text": (
                    "The torchlight reveals the Ruby Eye of Xol sitting on a stone pedestal. It glows with an inner light."
                ),
                "choices": [
                    ("Grab the ruby immediately", "grab"),
                    ("Inspect the pedestal for traps", "inspect"),
                ]
            },
            {
                "key": "grab",
                "title": "The Crushing Weight",
                "order": 4,
                "text": (
                    "You snatch the ruby. A loud click echoes through the chamber. The ceiling descends rapidly, crushing you beneath tons of stone."
                ),
                "is_ending": True, "ending_type": "bad", "choices": []
            },
            {
                "key": "inspect",
                "title": "The Counterweight",
                "order": 4,
                "text": (
                    "You notice the pedestal is a pressure plate. You carefully swap the ruby with a bag of sand of equal weight. "
                    "A secret back door opens."
                ),
                "choices": [
                    ("Leave through the back door with the ruby", "leave"),
                ]
            },
            {
                "key": "leave",
                "title": "Fortune and Glory",
                "order": 5,
                "text": (
                    "You emerge on a cliffside overlooking the river. You signal your extraction boat. "
                    "You are rich, and Blackwood is stuck hacking through the jungle. A perfect adventure."
                ),
                "is_ending": True, "ending_type": "good", "choices": []
            },
        ],
        "ratings": [5, 4, 5, 5, 4, 5],
    },
    # ══════════════════════════════════════════════════════════════
    #  6. ROMANCE  —  "A Dance in the Rain"
    # ══════════════════════════════════════════════════════════════
    {
        "title":       "A Dance in the Rain",
        "genre":       "romance",
        "cover_emoji": "🌧️",
        "description": "A struggling artist in Paris shares an umbrella with a mysterious stranger. It changes their life forever.",
        "play_count":  4150,
        "nodes": [
            {
                "title": "The Sudden Downpour",
                "order": 1,
                "text": (
                    "The skies over Paris open up suddenly. You huddle under the awning of a closed bakery, clutching your sketches. "
                    "A stranger runs up beside you, shaking the rain from their dark coat. They offer you half their umbrella."
                ),
                "choices": [
                    ("Accept the offer and walk with them", "accept"),
                    ("Politely decline and wait out the rain", "decline"),
                ]
            },
            {
                "key": "decline",
                "title": "A Missed Connection",
                "order": 2,
                "text": (
                    "You shake your head. They smile sadly and walk away into the mist. You wait for an hour. "
                    "You never see them again, but you always wonder 'what if'."
                ),
                "is_ending": True, "ending_type": "neutral", "choices": []
            },
            {
                "key": "accept",
                "title": "Under the Umbrella",
                "order": 2,
                "text": (
                    "You step under the umbrella. Their shoulder brushes yours. They introduce themselves as Julian. "
                    "As you walk toward the Metro, you fall into an easy, immediate conversation about art and life."
                ),
                "choices": [
                    ("Ask Julian to grab a coffee at a nearby café", "coffee"),
                    ("Part ways at the Metro but exchange numbers", "numbers"),
                ]
            },
            {
                "key": "coffee",
                "title": "Café des Arts",
                "order": 3,
                "text": (
                    "You sit by a fogged-up window, drinking espresso. Julian reveals they are a gallery curator. "
                    "They look at your sketches and their eyes widen in amazement."
                ),
                "choices": [
                    ("Admit your insecurities about your art", "admit"),
                    ("Act confident and pitch an exhibition", "pitch"),
                ]
            },
            {
                "key": "numbers",
                "title": "Waiting by the Phone",
                "order": 3,
                "text": (
                    "You exchange numbers. Two days pass. You finally text them. They never reply. "
                    "Perhaps it was just a fleeting moment in the rain."
                ),
                "is_ending": True, "ending_type": "bad", "choices": []
            },
            {
                "key": "admit",
                "title": "Vulnerability",
                "order": 4,
                "text": (
                    "Julian reaches across the table and holds your hand. 'True art requires vulnerability,' they say. "
                    "In that moment, you realize you've found not just a patron, but a soulmate."
                ),
                "is_ending": True, "ending_type": "good", "choices": []
            },
            {
                "key": "pitch",
                "title": "A Business Arrangement",
                "order": 4,
                "text": (
                    "Julian nods professionally. 'I can sell these.' You get your exhibition and become a wealthy artist, "
                    "but the romantic spark is lost to the business of the gallery."
                ),
                "is_ending": True, "ending_type": "neutral", "choices": []
            },
        ],
        "ratings": [5, 4, 5, 5, 5],
    },

    # ══════════════════════════════════════════════════════════════
    #  7. THRILLER  —  "Operation Blackout"
    # ══════════════════════════════════════════════════════════════
    {
        "title":       "Operation Blackout",
        "genre":       "thriller",
        "cover_emoji": "⏱️",
        "description": "A rogue agent has planted a dirty bomb in the city grid. You have exactly 45 minutes to find it and disarm it.",
        "play_count":  6100,
        "nodes": [
            {
                "title": "The Briefing",
                "order": 1,
                "text": (
                    "The Director slams a folder onto the metal table. 'Agent 'Ghost' has gone off the grid. "
                    "He's wired a device to the central power relay. If the grid overloads, the bomb detonates.' "
                    "You grab your sidearm."
                ),
                "choices": [
                    ("Head directly to the central power relay", "relay"),
                    ("Visit Ghost's last known safehouse", "safehouse"),
                ]
            },
            {
                "key": "relay",
                "title": "The Ambush",
                "order": 2,
                "text": (
                    "You arrive at the relay. It's heavily guarded by Ghost's mercenaries. You are heavily outnumbered."
                ),
                "choices": [
                    ("Go in guns blazing", "blazing"),
                    ("Sneak in through the ventilation shafts", "sneak"),
                ]
            },
            {
                "key": "safehouse",
                "title": "The Blueprints",
                "order": 2,
                "text": (
                    "You kick down the door to the safehouse. You find blueprints to the bomb. It requires a specific red wire to be cut first, or it instantly detonates."
                ),
                "choices": [
                    ("Rush to the central power relay now", "relay2"),
                ]
            },
            {
                "key": "blazing",
                "title": "A Fool's Errand",
                "order": 3,
                "text": (
                    "You take down five mercs, but a sniper takes you out. The bomb detonates. The city is lost."
                ),
                "is_ending": True, "ending_type": "bad", "choices": []
            },
            {
                "key": "sneak",
                "title": "The Bomb",
                "order": 3,
                "text": (
                    "You drop from the vents directly in front of the bomb. Ghost isn't here. "
                    "The timer reads 00:30. There is a red wire and a blue wire."
                ),
                "choices": [
                    ("Cut the red wire", "red"),
                    ("Cut the blue wire", "blue"),
                ]
            },
            {
                "key": "relay2",
                "title": "The Disarm",
                "order": 3,
                "text": (
                    "You arrive and bypass the guards. You find the bomb. Thanks to the blueprints, you know exactly what to do."
                ),
                "choices": [
                    ("Cut the red wire", "red"),
                ]
            },
            {
                "key": "red",
                "title": "The Hero",
                "order": 4,
                "text": (
                    "You snip the red wire. The timer freezes at 00:03. The city is saved, and you are a hero. Ghost is still out there, though..."
                ),
                "is_ending": True, "ending_type": "good", "choices": []
            },
            {
                "key": "blue",
                "title": "Boom",
                "order": 4,
                "text": (
                    "You snip the blue wire. The timer skips to 00:00. A blinding flash is the last thing you ever see."
                ),
                "is_ending": True, "ending_type": "bad", "choices": []
            },
        ],
        "ratings": [5, 5, 4, 5, 4, 5],
    },

    # ══════════════════════════════════════════════════════════════
    #  8. COMEDY  —  "The Goblin's Guide to Corporate Management"
    # ══════════════════════════════════════════════════════════════
    {
        "title":       "The Goblin's Guide to Corporate Management",
        "genre":       "comedy",
        "cover_emoji": "👺",
        "description": "You are a lowly goblin who accidentally got promoted to Regional Manager of the Dark Lord's evil corporation.",
        "play_count":  3300,
        "nodes": [
            {
                "title": "The Promotion",
                "order": 1,
                "text": (
                    "The Dark Lord points a flaming finger at you. 'You! The ugly one with the clipboard! You are now Regional Manager of DoomCorp. "
                    "If productivity drops, I will eat your spleen.'\n\n"
                    "You gulp. Your first task is to deal with the Orc Union strike."
                ),
                "choices": [
                    ("Offer the Orcs dental benefits", "dental"),
                    ("Threaten to replace them with skeletons", "skeletons"),
                ]
            },
            {
                "key": "dental",
                "title": "The Expensive Promise",
                "order": 2,
                "text": (
                    "The Orcs love the idea! They return to work. However, the Dark Lord's accountant, a terrifying vampire, informs you that dental for Orcs will bankrupt the company."
                ),
                "choices": [
                    ("Embezzle funds from the 'Lava Pit' budget", "embezzle"),
                    ("Try to convince the vampire to cook the books", "vampire"),
                ]
            },
            {
                "key": "skeletons",
                "title": "The Skeleton Crew",
                "order": 2,
                "text": (
                    "You fire the Orcs. The Skeletons take over. They don't complain, but they drop everything because they have no muscles. "
                    "Productivity reaches zero."
                ),
                "choices": [
                    ("Re-hire the Orcs and apologize", "apologize"),
                ]
            },
            {
                "key": "embezzle",
                "title": "Lava Problems",
                "order": 3,
                "text": (
                    "You take money from the Lava Pit maintenance fund. The next day, the lava pit overflows and destroys the HR department. "
                    "Everyone agrees this is actually a massive improvement."
                ),
                "is_ending": True, "ending_type": "good", "choices": []
            },
            {
                "key": "vampire",
                "title": "Blood Sucker",
                "order": 3,
                "text": (
                    "The vampire agrees to cook the books, but only if he gets to drink your blood on alternate Tuesdays. You agree. "
                    "You keep your job, but you are very anemic."
                ),
                "is_ending": True, "ending_type": "neutral", "choices": []
            },
            {
                "key": "apologize",
                "title": "The Spleen",
                "order": 3,
                "text": (
                    "The Orcs refuse to come back. The Dark Lord finds out. He was not joking about the spleen."
                ),
                "is_ending": True, "ending_type": "bad", "choices": []
            },
        ],
        "ratings": [4, 5, 5, 4, 5],
    },

    # ══════════════════════════════════════════════════════════════
    #  9. CYBERPUNK  —  "Neon Shadows"
    # ══════════════════════════════════════════════════════════════
    {
        "title":       "Neon Shadows",
        "genre":       "cyberpunk",
        "cover_emoji": "🌆",
        "description": "In the rain-slicked alleys of Neo-Veridian, a dead runner clutches a data-drive that could topple the mega-corps. Do you run, fight, or sell out?",
        "play_count":  1042,
        "nodes": [
            {
                "title": "The Dead Runner",
                "order": 1,
                "text": (
                    "The neon glow of a noodle stand reflects in the puddle next to the dead runner's face. "
                    "You didn't know him, but you know the silver data-drive clutched in his stiff hand. "
                    "It's a top-tier mil-spec drive, worth more than your life.\n\n"
                    "Sirens wail in the distance, growing louder. The corporate security drones will be here in less than a minute."
                ),
                "choices": [
                    ("Take the drive and run into the alleyways", "run"),
                    ("Quickly examine the runner's body for clues", "examine"),
                ]
            },
            {
                "key": "run",
                "title": "The Chase",
                "order": 2,
                "text": (
                    "You snatch the drive and sprint into the labyrinth of Neo-Veridian's lower levels. "
                    "Overhead, the hum of rotors grows deafening as a pair of Ares-Corp drones spot you on thermal.\n\n"
                    "Red targeting lasers dance across the wet pavement at your feet."
                ),
                "choices": [
                    ("Duck into 'The Static', a loud underground club", "club"),
                    ("Turn and fight the drones with your EMP pistol", "fight"),
                ]
            },
            {
                "key": "examine",
                "title": "The Corporate Badge",
                "order": 2,
                "text": (
                    "You pat down the runner's jacket and find a Level 9 access badge for the Olympus Spire — the Ares-Corp headquarters. "
                    "This explains why he had the drive.\n\n"
                    "The sirens are almost upon you. You take the drive and the badge."
                ),
                "choices": [
                    ("Use the badge to infiltrate the Spire right now", "infiltrate"),
                    ("Flee into the alleyways before security arrives", "run"),
                ]
            },
            {
                "key": "club",
                "title": "The Static",
                "order": 3,
                "text": (
                    "You push through the heavy doors into a wall of sound and strobing lights. "
                    "The drones lose you in the crowd. At the bar, you spot a notorious fixer known as 'Cipher'. "
                    "She owes you a favor, but she's notoriously treacherous."
                ),
                "choices": [
                    ("Offer to sell her the drive, no questions asked", "sell"),
                    ("Ask her to help you decrypt it", "decrypt"),
                ]
            },
            {
                "key": "fight",
                "title": "Overwhelmed",
                "order": 3,
                "text": (
                    "You draw your EMP pistol and fire. One drone spirals into a wall, sparking wildly. "
                    "But the second drone adapts instantly, returning fire with lethal precision. "
                    "You never even feel the shot.\n\n"
                    "The drive is recovered. The corp wins. They always do."
                ),
                "is_ending": True,
                "ending_type": "bad",
                "choices": []
            },
            {
                "key": "infiltrate",
                "title": "The Olympus Spire",
                "order": 3,
                "text": (
                    "Using the dead runner's badge, you bluff your way into the Ares-Corp headquarters. "
                    "You plug the drive into a terminal. It contains explicit proof that the corp is poisoning the city's water supply to sell the cure."
                ),
                "choices": [
                    ("Upload the data to the public net", "upload"),
                    ("Message the CEO and blackmail them", "blackmail"),
                ]
            },
            {
                "key": "sell",
                "title": "A Quiet Retirement",
                "order": 4,
                "text": (
                    "Cipher's eyes widen when she sees the drive. She wires five million creds to your untraceable account on the spot.\n\n"
                    "You don't know what was on the drive, and you don't care. You spend the rest of your days in a luxury beach simulation, "
                    "safely disconnected from the real world's problems."
                ),
                "is_ending": True,
                "ending_type": "neutral",
                "choices": []
            },
            {
                "key": "decrypt",
                "title": "The Terrible Truth",
                "order": 4,
                "text": (
                    "Cipher plugs the drive into an isolated deck. 'This is a neural-override protocol,' she whispers. "
                    "'It allows complete control over anyone with a neural implant.'\n\n"
                    "She looks at you. 'We could destroy it. Or... we could use it.'"
                ),
                "choices": [
                    ("Destroy the drive. It's too dangerous.", "destroy"),
                    ("Use it to take over the city.", "use"),
                ]
            },
            {
                "key": "upload",
                "title": "Revolution",
                "order": 4,
                "text": (
                    "You hit execute. The data streams across every screen in Neo-Veridian. "
                    "Riots break out within the hour. The Ares-Corp building is stormed by millions of angry citizens. "
                    "You sneak out the back, knowing you've changed the world forever."
                ),
                "is_ending": True,
                "ending_type": "good",
                "choices": []
            },
            {
                "key": "blackmail",
                "title": "Corporate Greed",
                "order": 4,
                "text": (
                    "You demand ten million creds. The CEO agrees immediately, telling you to wait on the roof for a stealth chopper. "
                    "Instead of a chopper with money, a sniper drone arrives. "
                    "You realize, far too late, that some secrets are too big to blackmail."
                ),
                "is_ending": True,
                "ending_type": "bad",
                "choices": []
            },
            {
                "key": "destroy",
                "title": "The Right Thing",
                "order": 5,
                "text": (
                    "You smash the drive with the butt of your pistol, shattering the memory core. "
                    "You'll never be rich, and you'll always be looking over your shoulder, but you saved millions of minds from slavery. "
                    "That has to count for something."
                ),
                "is_ending": True,
                "ending_type": "neutral",
                "choices": []
            },
            {
                "key": "use",
                "title": "The New Overlord",
                "order": 5,
                "text": (
                    "You run the protocol. Instantly, millions of citizens freeze, awaiting your command. "
                    "You walk out of the club not as a runner, but as a god. "
                    "You have won the cyberpunk game, but lost your humanity."
                ),
                "is_ending": True,
                "ending_type": "good",
                "choices": []
            },
        ],
        "ratings": [5, 4, 5, 4, 3, 5, 5, 4, 5],
    },

    # ══════════════════════════════════════════════════════════════
    #  10. HISTORICAL FICTION  —  "The Queen's Gambit"
    # ══════════════════════════════════════════════════════════════
    {
        "title":       "The Queen's Gambit",
        "genre":       "historical",
        "cover_emoji": "👑",
        "description": "The King is dying. As the Queen's trusted advisor, you must navigate the treacherous waters of 16th-century court politics.",
        "play_count":  1875,
        "nodes": [
            {
                "title": "A Dying King",
                "order": 1,
                "text": (
                    "The King's bedchamber smells of myrrh and decay. Outside, the winter wind howls against the castle stones. "
                    "The Queen pulls you into a secluded alcove, her face pale but determined.\n\n"
                    "'He will not survive the night,' she whispers. 'The legitimate heir, Prince Edward, is cruel and mad. "
                    "But I have a secret bastard son, Thomas, hidden away in the countryside. He is kind and strong. Who should succeed?'"
                ),
                "choices": [
                    ("Counsel her to support the legitimate heir, Edward", "heir"),
                    ("Counsel her to crown her bastard son, Thomas", "bastard"),
                ]
            },
            {
                "key": "heir",
                "title": "The Mad Prince",
                "order": 2,
                "text": (
                    "You advise adherence to the law. Upon the King's death, Edward is crowned. "
                    "His reign of terror begins immediately, executing lords who look at him sideways. "
                    "You retain your position, but your conscience is heavy."
                ),
                "choices": [
                    ("Attempt to temper his cruelty through manipulation", "temper"),
                    ("Plot an assassination", "assassinate"),
                ]
            },
            {
                "key": "bastard",
                "title": "The Secret Son",
                "order": 2,
                "text": (
                    "You agree that Thomas must rule for the good of the realm. "
                    "However, he has no legal claim. You must secure his path to the throne before Edward realizes."
                ),
                "choices": [
                    ("Forge documents proving Thomas is the true heir", "forge"),
                    ("Gather a rebel army in secret", "army"),
                ]
            },
            {
                "key": "temper",
                "title": "A Delicate Balance",
                "order": 3,
                "text": (
                    "You spend years carefully manipulating King Edward, saving countless lives by directing his wrath toward meaningless targets. "
                    "It is a stressful, unfulfilling life, but you keep the kingdom from collapsing into total ruin."
                ),
                "is_ending": True,
                "ending_type": "neutral",
                "choices": []
            },
            {
                "key": "assassinate",
                "title": "The Executioner's Block",
                "order": 3,
                "text": (
                    "Your plot is discovered by the King's spies. You are dragged to the Tower, "
                    "and the next morning, you meet the executioner's axe. Your sacrifice is forgotten."
                ),
                "is_ending": True,
                "ending_type": "bad",
                "choices": []
            },
            {
                "key": "forge",
                "title": "The Golden Age",
                "order": 3,
                "text": (
                    "The forged documents are perfect. The Archbishop declares Edward illegitimate, and Thomas is crowned. "
                    "His reign brings decades of peace and prosperity to the realm. You are remembered as the architect of a golden age."
                ),
                "is_ending": True,
                "ending_type": "good",
                "choices": []
            },
            {
                "key": "army",
                "title": "Civil War",
                "order": 3,
                "text": (
                    "You raise an army of dissatisfied lords. The realm is plunged into a bloody civil war. "
                    "The final battle approaches, and the vanguard needs a commander."
                ),
                "choices": [
                    ("Lead the vanguard yourself", "lead"),
                    ("Stay behind the lines with the Queen", "stay"),
                ]
            },
            {
                "key": "lead",
                "title": "A Hero's Death",
                "order": 4,
                "text": (
                    "You lead the charge, breaking the King's lines. You fall in battle, taking an arrow to the chest, "
                    "but your actions win the war for Thomas. You die a hero, ensuring a better future."
                ),
                "is_ending": True,
                "ending_type": "neutral",
                "choices": []
            },
            {
                "key": "stay",
                "title": "Defeat",
                "order": 4,
                "text": (
                    "Without strong leadership at the front, the rebel army is crushed. "
                    "You and the Queen are forced to flee across the sea, living the rest of your days in bitter exile."
                ),
                "is_ending": True,
                "ending_type": "bad",
                "choices": []
            },
        ],
        "ratings": [5, 5, 5, 4, 5, 4, 5, 5, 5, 5],
    },
]

class Command(BaseCommand):
    help = "Seed StoryForge with 10 brand new rich branching stories."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.MIGRATE_HEADING("\\n📖  StoryForge Seed — Starting...\\n"))

        # WIPE THE DB CLEAN
        Story.objects.all().delete()
        self.stdout.write(self.style.WARNING("  ! Cleared all existing stories from the database."))

        # ── Create / get the author superuser ─────────────────────
        author_user, created = User.objects.get_or_create(
            username="storymaster",
            defaults={
                "email": "storymaster@storyforge.dev",
                "is_staff": True,
                "is_superuser": True,
            }
        )
        if created:
            author_user.set_password("forge1234")
            author_user.save()
            UserAccount.objects.get_or_create(
                user=author_user,
                defaults={
                    "username": "storymaster",
                    "email": "storymaster@storyforge.dev",
                    "hashed_password": make_password("forge1234"),
                    "avatar_emoji": "⚗️",
                    "bio": "The original StoryForge author. Every tale begins somewhere.",
                }
            )
            self.stdout.write(self.style.SUCCESS("  ✔ Created author: storymaster / forge1234"))

        # ── Create dummy rater accounts ────────────────────────────
        rater_users = []
        for i in range(1, 16):
            u, was_created = User.objects.get_or_create(
                username=f"reader{i}",
                defaults={"email": f"reader{i}@storyforge.dev"}
            )
            if was_created:
                u.set_password("reader1234")
                u.save()
            rater_users.append(u)

        # ── Seed each story ────────────────────────────────────────
        for story_data in STORIES:
            story = Story.objects.create(
                title=story_data["title"],
                genre=story_data["genre"],
                cover_emoji=story_data["cover_emoji"],
                description=story_data["description"],
                play_count=story_data["play_count"],
                author=author_user,
                is_published=True,
            )

            node_map = {}
            created_nodes = []
            order_counter = 0

            for nd in story_data["nodes"]:
                order_counter += 1
                node = Node.objects.create(
                    story=story,
                    title=nd.get("title", ""),
                    text=nd["text"],
                    order=nd.get("order", order_counter),
                    is_ending=nd.get("is_ending", False),
                    ending_type=nd.get("ending_type", ""),
                )
                key = nd.get("key", str(nd.get("order", order_counter)))
                node_map[key] = node
                created_nodes.append((nd, node))

            story.start_node = created_nodes[0][1]
            story.save(update_fields=["start_node"])

            for nd, node in created_nodes:
                for idx, (choice_text, next_key) in enumerate(nd.get("choices", [])):
                    next_node = node_map.get(next_key)
                    Choice.objects.create(
                        node=node,
                        choice_text=choice_text,
                        next_node=next_node,
                        order=idx,
                    )

            shuffled = rater_users[:]
            random.shuffle(shuffled)
            for i, stars in enumerate(story_data.get("ratings", [])):
                if i >= len(shuffled):
                    break
                Rating.objects.get_or_create(
                    story=story,
                    user=shuffled[i],
                    defaults={"stars": stars}
                )

            avg = story.average_rating()
            self.stdout.write(
                self.style.SUCCESS(
                    f"  ✔ [{story_data['genre'].upper():10}]  "
                    f"{story_data['title']:<42}  "
                    f"{story.node_count():>2} nodes  "
                    f"⭐ {avg}  "
                    f"🎮 {story_data['play_count']:,} plays"
                )
            )

        self.stdout.write(self.style.MIGRATE_HEADING(
            "\\n🎉  Seed complete!\\n"
            "    Run:  python manage.py runserver\\n"
            "    Admin login:  storymaster / forge1234\\n"
            "    All 10 genre stories are live with full branching paths and animations.\\n"
        ))