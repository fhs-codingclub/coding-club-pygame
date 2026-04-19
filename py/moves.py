MOVES = {
    "Slash": {"damage_mult": 1.0, "accuracy": 90, "effect": None},
    "Smoulder": {"damage_mult": 0.5, "accuracy": 100, "effect": "lower_atk"},
    "Drive": {"damage_mult": 1.5, "accuracy": 70, "effect": "recoil"},
    "Harden": {"damage_mult": 0, "accuracy": 100, "effect": "raise_def"}
}

ENEMY_MOVES = {
    "Pollutinate": {"damage": 15, "effect": "poison", "text": "sprays toxic spores!"},
    "Bloom Swap":  {"damage": 0,  "effect": "stat_swap", "text": "switches its faces!"},
    "Chomp":       {"damage": 20, "effect": "none", "text": "bites down hard!"},
    "Evil Plot":   {"damage": 0,  "effect": "buff_atk", "text": "is planning something wicked..."},
    "Reject":      {"damage": 5,  "effect": "recoil", "text": "spits out nasty gunk!"}
}