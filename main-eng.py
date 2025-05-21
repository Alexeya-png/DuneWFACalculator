import random
import copy
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

special_leaders_data = {
    "Paul Muad'Dib": {"swords": 2, "shields": 1},
    "Paul Atreides": {"swords": 1, "shields": 0},
    "Lady Jessica": {"swords": 0, "shields": 1},
    "Mother Jessica": {"swords": 0, "shields": 2},
    "Gurney Halleck": {"swords": 2, "shields": 1},
    "Alia": {"swords": 1, "shields": 0},
    "Stilgar": {"swords": 2, "shields": 0},
    "Chani": {"swords": 1, "shields": 1},
    "Baron Harkonnen": {"swords": 0, "shields": 2},
    "Beast Rabban": {"swords": 2, "shields": 0},
    "Feyd-Rautha": {"swords": 2, "shields": 1},
    "Thufir Hawat": {"swords": 1, "shields": 2},
    "Shaddam IV": {"swords": 2, "shields": 0},
    "G.H. Mohiam": {"swords": 0, "shields": 3},
    "Captain Aramsham": {"swords": 2, "shields": 0}
}

def format_count(num, forms):
    if num == 1:
        return f"{num} {forms[0]}"
    else:
        return f"{num} {forms[1]}"

def allocate_casualties(side_name, casualties, state, log_active=True):
    log = []
    while casualties > 0:
        if casualties > 0 and state['elite'] > 0:
            state['elite'] -= 1
            state['normal'] += 1
            casualties -= 1
            if log_active:
                log.append(f"{side_name}: elite unit downgraded to normal.")
            continue
        if casualties > 0 and state['normal_leader'] > 0:
            state['normal_leader'] -= 1
            casualties -= 1
            if log_active:
                log.append(f"{side_name}: normal leader killed.")
            continue
        # Remove a special leader if there are more than two (remove the weakest)
        if casualties > 0 and len(state['special_leaders']) > 2:
            weakest = min(state['special_leaders'], key=lambda name: special_leaders_data[name]['swords'] + special_leaders_data[name]['shields'])
            state['special_leaders'].remove(weakest)
            casualties -= 1
            if log_active:
                log.append(f"{side_name}: special leader {weakest} killed.")
            continue
        # Downgrade a special elite unit to normal
        if casualties > 0 and state['special_elite'] > 0:
            state['special_elite'] -= 1
            state['normal'] += 1
            casualties -= 1
            if log_active:
                log.append(f"{side_name}: special elite unit downgraded to normal.")
            continue
        # Remove normal units until only 4 remain
        if casualties > 0 and state['normal'] > 4:
            to_kill = min(casualties, state['normal'] - 4)
            state['normal'] -= to_kill
            casualties -= to_kill
            if log_active and to_kill > 0:
                if to_kill == 1:
                    log.append(f"{side_name}: 1 normal unit destroyed.")
                else:
                    log.append(f"{side_name}: {to_kill} normal units destroyed.")
            continue
        # Remove any remaining special leader (if any)
        if casualties > 0 and len(state['special_leaders']) > 0:
            weakest = min(state['special_leaders'], key=lambda name: special_leaders_data[name]['swords'] + special_leaders_data[name]['shields'])
            state['special_leaders'].remove(weakest)
            casualties -= 1
            if log_active:
                log.append(f"{side_name}: special leader {weakest} killed.")
            continue
        # Remove remaining normal units
        if casualties > 0 and state['normal'] > 0:
            if casualties >= state['normal']:
                num = state['normal']
                state['normal'] = 0
                casualties -= num
                if log_active:
                    if num == 1:
                        log.append(f"{side_name}: 1 normal unit destroyed.")
                    else:
                        log.append(f"{side_name}: {num} normal units destroyed.")
            else:
                num = casualties
                state['normal'] -= num
                casualties = 0
                if log_active:
                    if num == 1:
                        log.append(f"{side_name}: 1 normal unit destroyed.")
                    else:
                        log.append(f"{side_name}: {num} normal units destroyed.")
            continue
        break
    return log

# Simulate a battle between two armies
def simulate_battle(att, deff, settlement=False, sudden_attack=False, log_active=True):
    att_state = copy.deepcopy(att)
    def_state = copy.deepcopy(deff)
    log = []
    round_num = 1
    att_cards_left = att_state.get('cards', 0)
    def_cards_left = def_state.get('cards', 0)
    while True:
        att_units = att_state['normal'] + att_state['elite'] + att_state['special_elite']
        def_units = def_state['normal'] + def_state['elite'] + def_state['special_elite']
        defender_settlement_cubes = def_state.get('settlement', 0)

        if att_units == 0 or def_units == 0:
            break

        att_cards_this_round = min(att_cards_left, max(0, 6 - att_units))
        def_cards_this_round = min(def_cards_left, max(0, 6 - def_units))

        attacker_dice = min(6, att_units + att_cards_this_round)
        defender_dice = min(6, def_units + def_cards_this_round + defender_settlement_cubes)
        att_cards_left -= att_cards_this_round
        def_cards_left -= def_cards_this_round

        a_swords = a_shields = a_stars = 0
        for _ in range(attacker_dice):
            roll = random.randint(1, 6)
            if roll <= 3:
                a_swords += 1
            elif roll <= 5:
                a_shields += 1
            else:
                a_stars += 1

        # Sudden attack: +1 star in the first round
        if round_num == 1 and sudden_attack:
            a_stars += 1
            if log_active:
                log.append("Sudden attack: attacker gains +1 special symbol (star) this round.")

        d_swords = d_shields = d_stars = 0
        for _ in range(defender_dice):
            roll = random.randint(1, 6)
            if roll <= 3:
                d_swords += 1
            elif roll <= 5:
                d_shields += 1
            else:
                d_stars += 1
        total_att_leaders = att_state['normal_leader'] + len(att_state['special_leaders'])
        total_def_leaders = def_state['normal_leader'] + len(def_state['special_leaders'])
        att_extra_swords = att_extra_shields = 0
        def_extra_swords = def_extra_shields = 0
        att_used = []
        def_used = []
        # Use of rolled "special" symbols by attacker (leaders)
        if a_stars > 0 and total_att_leaders > 0:
            leader_list = [("Unnamed", 1, 0)] * att_state['normal_leader']
            for name in att_state['special_leaders']:
                vals = special_leaders_data.get(name, {"swords": 0, "shields": 0})
                leader_list.append((name, vals['swords'], vals['shields']))
            if a_stars >= len(leader_list):
                for (name, sw, sh) in leader_list:
                    att_extra_swords += sw
                    att_extra_shields += sh
                    if log_active:
                        att_used.append((name, sw, sh))
            else:
                leader_list.sort(key=lambda x: (x[1] + x[2], x[1]), reverse=True)
                chosen = leader_list[:a_stars]
                for (name, sw, sh) in chosen:
                    att_extra_swords += sw
                    att_extra_shields += sh
                    if log_active:
                        att_used.append((name, sw, sh))
        # Use of rolled "special" symbols by defender
        if d_stars > 0 and total_def_leaders > 0:
            leader_list = [("Unnamed", 1, 0)] * def_state['normal_leader']
            for name in def_state['special_leaders']:
                vals = special_leaders_data.get(name, {"swords": 0, "shields": 0})
                leader_list.append((name, vals['swords'], vals['shields']))
            if d_stars >= len(leader_list):
                for (name, sw, sh) in leader_list:
                    def_extra_swords += sw
                    def_extra_shields += sh
                    if log_active:
                        def_used.append((name, sw, sh))
            else:
                leader_list.sort(key=lambda x: (x[1] + x[2], x[1]), reverse=True)
                chosen = leader_list[:d_stars]
                for (name, sw, sh) in chosen:
                    def_extra_swords += sw
                    def_extra_shields += sh
                    if log_active:
                        def_used.append((name, sw, sh))
        # Total swords and shields after applying leaders
        total_a_swords = a_swords + att_extra_swords
        total_a_shields = a_shields + att_extra_shields
        total_d_swords = d_swords + def_extra_swords
        total_d_shields = d_shields + def_extra_shields
        # Special elite units cancel opponent's shield results
        if att_state['special_elite'] > 0:
            cancel = min(total_d_shields, att_state['special_elite'])
            total_d_shields -= cancel
            if log_active and cancel > 0:
                log.append(f"Attacker's special elite cancel {cancel} shield result(s) of the defender.")
        if def_state['special_elite'] > 0:
            cancel = min(total_a_shields, def_state['special_elite'])
            total_a_shields -= cancel
            if log_active and cancel > 0:
                log.append(f"Defender's special elite cancel {cancel} shield result(s) of the attacker.")
        # Calculate hits (swords minus opponent shields)
        hits_on_def = total_a_swords - total_d_shields
        hits_on_att = total_d_swords - total_a_shields
        if hits_on_def < 0: hits_on_def = 0
        if hits_on_att < 0: hits_on_att = 0

        # Log results of the round
        if log_active:
            sword_str = format_count(a_swords, ("sword", "swords"))
            shield_str = format_count(a_shields, ("shield", "shields"))
            special_str = format_count(a_stars, ("special symbol", "special symbols"))
            log.append(f"Round {round_num}: attacker rolled {attacker_dice} {'die' if attacker_dice == 1 else 'dice'} -> {sword_str}, {shield_str}, {special_str}.")
            sword_str = format_count(d_swords, ("sword", "swords"))
            shield_str = format_count(d_shields, ("shield", "shields"))
            special_str = format_count(d_stars, ("special symbol", "special symbols"))
            log.append(f"Round {round_num}: defender rolled {defender_dice} {'die' if defender_dice == 1 else 'dice'} -> {sword_str}, {shield_str}, {special_str}.")
            if att_used:
                # Details of attacker leaders using special symbols
                unnamed_count = sum(1 for x in att_used if x[0] == "Unnamed")
                parts = []
                if unnamed_count > 0:
                    parts.append(f"{unnamed_count} unnamed leader{'s' if unnamed_count != 1 else ''} added {unnamed_count} sword{'s' if unnamed_count != 1 else ''}")
                for (name, sw, sh) in att_used:
                    if name == "Unnamed": continue
                    subparts = []
                    if sw: subparts.append(format_count(sw, ("sword", "swords")))
                    if sh: subparts.append(format_count(sh, ("shield", "shields")))
                    contribution = " and ".join(subparts)
                    parts.append(f"{name} added {contribution}")
                log.append("Attacker uses special symbols: " + "; ".join(parts) + ".")
            else:
                if a_stars > 0 and total_att_leaders == 0:
                    log.append("Attacker rolled special symbols, but no one can use them.")
            if def_used:
                unnamed_count = sum(1 for x in def_used if x[0] == "Unnamed")
                parts = []
                if unnamed_count > 0:
                    parts.append(f"{unnamed_count} unnamed leader{'s' if unnamed_count != 1 else ''} added {unnamed_count} sword{'s' if unnamed_count != 1 else ''}")
                for (name, sw, sh) in def_used:
                    if name == "Unnamed": continue
                    subparts = []
                    if sw: subparts.append(format_count(sw, ("sword", "swords")))
                    if sh: subparts.append(format_count(sh, ("shield", "shields")))
                    contribution = " and ".join(subparts)
                    parts.append(f"{name} added {contribution}")
                log.append("Defender uses special symbols: " + "; ".join(parts) + ".")
            else:
                if d_stars > 0 and total_def_leaders == 0:
                    log.append("Defender rolled special symbols, but no one can use them.")
            sword_str_a = format_count(total_a_swords, ("sword", "swords"))
            shield_str_a = format_count(total_a_shields, ("shield", "shields"))
            sword_str_d = format_count(total_d_swords, ("sword", "swords"))
            shield_str_d = format_count(total_d_shields, ("shield", "shields"))
            log.append(f"After abilities: attacker has {sword_str_a}, {shield_str_a}; defender has {sword_str_d}, {shield_str_d}.")
            log.append(f"Damage dealt: attacker took {hits_on_att} {'hit' if hits_on_att == 1 else 'hits'}, defender took {hits_on_def} {'hit' if hits_on_def == 1 else 'hits'}.")
        # Apply hits (damage) to units
        if hits_on_def > 0:
            def_casualty_log = allocate_casualties("Defender", hits_on_def, def_state, log_active=log_active)
            if log_active: log.extend(def_casualty_log)
        if hits_on_att > 0:
            att_casualty_log = allocate_casualties("Attacker", hits_on_att, att_state, log_active=log_active)
            if log_active: log.extend(att_casualty_log)

        # Check if defender still has units alive
        def_units_after = def_state['normal'] + def_state['elite'] + def_state['special_elite']

        # Penalty to attacker for battle at settlement: +1 hit
        if settlement and def_units_after > 0:
            penalty = 1
            penalty_log = allocate_casualties("Attacker suffers assault damage", penalty, att_state, log_active=log_active)
            if log_active:
                log.extend(penalty_log)

        # Log state after the round
        if log_active:
            att_special_leaders = ", ".join(att_state['special_leaders']) if att_state['special_leaders'] else "none"
            def_special_leaders = ", ".join(def_state['special_leaders']) if def_state['special_leaders'] else "none"
            log.append(f"End of round {round_num}: attacker - normal units: {att_state['normal']}, elite units: {att_state['elite']}, special elite units: {att_state['special_elite']}; normal leaders: {att_state['normal_leader']}, special leaders: {att_special_leaders}.")
            log.append(f"End of round {round_num}: defender - normal units: {def_state['normal']}, elite units: {def_state['elite']}, special elite units: {def_state['special_elite']}; normal leaders: {def_state['normal_leader']}, special leaders: {def_special_leaders}.")
            log.append("----")
        round_num += 1
    # Battle result (after exiting the loop)
    att_units = att_state['normal'] + att_state['elite'] + att_state['special_elite']
    def_units = def_state['normal'] + def_state['elite'] + def_state['special_elite']
    defender_settlement_cubes = def_state.get('settlement', 0)

    # Determine the strongest leader of each side
    att_strongest = None
    def_strongest = None
    leader_list = [("Unnamed", 1, 0)] * att_state['normal_leader']
    for name in att_state['special_leaders']:
        vals = special_leaders_data.get(name, {"swords": 0, "shields": 0})
        leader_list.append((name, vals['swords'], vals['shields']))
    if leader_list:
        leader_list.sort(key=lambda x: (x[1] + x[2], x[1]), reverse=True)
        att_strongest = leader_list[0][0]
    leader_list = [("Unnamed", 1, 0)] * def_state['normal_leader']
    for name in def_state['special_leaders']:
        vals = special_leaders_data.get(name, {"swords": 0, "shields": 0})
        leader_list.append((name, vals['swords'], vals['shields']))
    if leader_list:
        leader_list.sort(key=lambda x: (x[1] + x[2], x[1]), reverse=True)
        def_strongest = leader_list[0][0]
    # Survival of the strongest leaders
    att_strongest_survived = False
    def_strongest_survived = False
    if att_strongest is None:
        att_strongest_survived = False
    elif att_strongest == "Unnamed":
        att_strongest_survived = att_state['normal_leader'] > 0
    else:
        att_strongest_survived = att_strongest in att_state['special_leaders']
    if def_strongest is None:
        def_strongest_survived = False
    elif def_strongest == "Unnamed":
        def_strongest_survived = def_state['normal_leader'] > 0
    else:
        def_strongest_survived = def_strongest in def_state['special_leaders']
    # Determine outcome
    if att_units > 0 and def_units == 0:
        if log_active:
            log.append("Result: attacker wins!")
            return log
        else:
            return ("Attacker wins", att_units, def_units, att_strongest_survived, def_strongest_survived, att_strongest, def_strongest)
    elif def_units > 0 and att_units == 0:
        if log_active:
            log.append("Result: defender wins.")
            return log
        else:
            return ("Defender wins", att_units, def_units, att_strongest_survived, def_strongest_survived, att_strongest, def_strongest)
    else:
        if log_active:
            log.append("Result: both armies are destroyed.")
            return log
        else:
            return ("Both destroyed", att_units, def_units, att_strongest_survived, def_strongest_survived, att_strongest, def_strongest)

def update_defender_count(var, others):
    total = var.get() + sum(v.get() for v in others)
    if total > 6:
        var.set(max(0, 6 - sum(v.get() for v in others)))
        messagebox.showerror("Error", "Total units cannot exceed 6!")

root = tk.Tk()
root.title("Dune: War for Arrakis - Battle Calculator")

att_frame = ttk.LabelFrame(root, text="Attacker")
def_frame = ttk.LabelFrame(root, text="Defender")
att_frame.grid(row=0, column=0, padx=5, pady=5, sticky="n")
def_frame.grid(row=0, column=1, padx=5, pady=5, sticky="n")

# Input fields for attacker
attacker_normal_var = tk.IntVar(value=0)
attacker_elite_var = tk.IntVar(value=0)
attacker_special_elite_var = tk.IntVar(value=0)
attacker_normal_leader_var = tk.IntVar(value=0)
attacker_cards_var = tk.IntVar(value=0)
defender_settlement_var = tk.IntVar(value=0)
sudden_attack_var = tk.BooleanVar(value=False)

ttk.Label(att_frame, text="Normal units:").grid(row=0, column=0, sticky="e")
ttk.Spinbox(att_frame, from_=0, to=6, textvariable=attacker_normal_var, width=5).grid(row=0, column=1)
ttk.Label(att_frame, text="Elite units:").grid(row=1, column=0, sticky="e")
ttk.Spinbox(att_frame, from_=0, to=6, textvariable=attacker_elite_var, width=5).grid(row=1, column=1)
ttk.Label(att_frame, text="Special elite units:").grid(row=2, column=0, sticky="e")
ttk.Spinbox(att_frame, from_=0, to=6, textvariable=attacker_special_elite_var, width=5).grid(row=2, column=1)
ttk.Label(att_frame, text="Normal leaders:").grid(row=3, column=0, sticky="e")
ttk.Spinbox(att_frame, from_=0, to=10, textvariable=attacker_normal_leader_var, width=5).grid(row=3, column=1)
ttk.Label(att_frame, text="Cards (extra dice):").grid(row=4, column=0, sticky="e")
ttk.Spinbox(att_frame, from_=0, to=10, textvariable=attacker_cards_var, width=5).grid(row=4, column=1)
ttk.Checkbutton(att_frame, text="Sudden Attack", variable=sudden_attack_var).grid(row=5, column=0, padx=0, pady=5, sticky="w")
ttk.Label(def_frame, text="Settlement (dice):").grid(row=5, column=0, sticky="e")
ttk.Spinbox(def_frame, from_=0, to=3, textvariable=defender_settlement_var, width=5).grid(row=5, column=1)

# Checkboxes for attacker's special leaders
att_special_vars = {name: tk.BooleanVar(value=False) for name in special_leaders_data.keys()}
row_index = 6
ttk.Label(att_frame, text="Atreides/Fremen Leaders:").grid(row=6, column=0, columnspan=2, sticky="w", pady=(5,0))
row_index += 1
for name in ["Paul Atreides", "Paul Muad'Dib", "Lady Jessica", "Mother Jessica", "Gurney Halleck", "Alia", "Stilgar", "Chani"]:
    ttk.Checkbutton(att_frame, text=name, variable=att_special_vars[name]).grid(row=row_index, column=0, columnspan=2, sticky="w")
    row_index += 1
ttk.Label(att_frame, text="Harkonnen/Corino Leaders:").grid(row=row_index, column=0, columnspan=2, sticky="w", pady=(5,0))
row_index += 1
for name in ["Baron Harkonnen", "Beast Rabban", "Feyd-Rautha", "Thufir Hawat", "Shaddam IV", "G.H. Mohiam", "Captain Aramsham"]:
    ttk.Checkbutton(att_frame, text=name, variable=att_special_vars[name]).grid(row=row_index, column=0, columnspan=2, sticky="w")
    row_index += 1
max_unit_size = 6
# Input fields for defender
defender_normal_var = tk.IntVar(value=0)
defender_elite_var = tk.IntVar(value=0)
defender_special_elite_var = tk.IntVar(value=0)
defender_normal_leader_var = tk.IntVar(value=0)

def normal_changed(*a): update_defender_count(defender_normal_var, [defender_elite_var, defender_special_elite_var])
def elite_changed(*a): update_defender_count(defender_elite_var, [defender_normal_var, defender_special_elite_var])
def special_changed(*a): update_defender_count(defender_special_elite_var, [defender_normal_var, defender_elite_var])

defender_normal_var.trace_add('write', normal_changed)
defender_elite_var.trace_add('write', elite_changed)
defender_special_elite_var.trace_add('write', special_changed)

defender_cards_var = tk.IntVar(value=0)
ttk.Label(def_frame, text="Normal units:").grid(row=0, column=0, sticky="e")
ttk.Spinbox(def_frame, from_=0, to=6, textvariable=defender_normal_var, width=5).grid(row=0, column=1)
ttk.Label(def_frame, text="Elite units:").grid(row=1, column=0, sticky="e")
ttk.Spinbox(def_frame, from_=0, to=6, textvariable=defender_elite_var, width=5).grid(row=1, column=1)
ttk.Label(def_frame, text="Special elite units:").grid(row=2, column=0, sticky="e")
ttk.Spinbox(def_frame, from_=0, to=6, textvariable=defender_special_elite_var, width=5).grid(row=2, column=1)
ttk.Label(def_frame, text="Normal leaders:").grid(row=3, column=0, sticky="e")
ttk.Spinbox(def_frame, from_=0, to=10, textvariable=defender_normal_leader_var, width=5).grid(row=3, column=1)
ttk.Label(def_frame, text="Cards (extra dice):").grid(row=4, column=0, sticky="e")
ttk.Spinbox(def_frame, from_=0, to=10, textvariable=defender_cards_var, width=5).grid(row=4, column=1)
# Checkboxes for defender's special leaders
def_special_vars = {name: tk.BooleanVar(value=False) for name in special_leaders_data.keys()}
row_index = 6
ttk.Label(def_frame, text="Atreides/Fremen Leaders:").grid(row=6, column=0, columnspan=2, sticky="w", pady=(15,0))
row_index += 1
for name in ["Paul Atreides", "Paul Muad'Dib", "Lady Jessica", "Mother Jessica", "Gurney Halleck", "Alia", "Stilgar", "Chani"]:
    ttk.Checkbutton(def_frame, text=name, variable=def_special_vars[name]).grid(row=row_index, column=0, columnspan=2, sticky="w")
    row_index += 1
ttk.Label(def_frame, text="Harkonnen/Corino Leaders:").grid(row=row_index, column=0, columnspan=2, sticky="w", pady=(5,0))
row_index += 1
for name in ["Baron Harkonnen", "Beast Rabban", "Feyd-Rautha", "Thufir Hawat", "Shaddam IV", "G.H. Mohiam", "Captain Aramsham"]:
    ttk.Checkbutton(def_frame, text=name, variable=def_special_vars[name]).grid(row=row_index, column=0, columnspan=2, sticky="w")
    row_index += 1

# Checkbox "attack on settlement"
settlement_var = tk.BooleanVar(value=False)
ttk.Checkbutton(root, text="Attack on settlement (attacker penalty)", variable=settlement_var).grid(row=1, column=0, columnspan=2, pady=5)

# Output text field for battle result/log
output_text = tk.Text(root, width=100, height=30, wrap="word")
output_text.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
scrollbar = ttk.Scrollbar(root, orient="vertical", command=output_text.yview)
scrollbar.grid(row=3, column=2, sticky="ns")
output_text.configure(yscrollcommand=scrollbar.set, state="disabled")

# Handler for "Calculate Battle" button
def run_calculation():
    att_strongest_name = ""
    def_strongest_name = ""
    att_state = {
        "normal": attacker_normal_var.get(),
        "elite": attacker_elite_var.get(),
        "special_elite": attacker_special_elite_var.get(),
        "normal_leader": attacker_normal_leader_var.get(),
        "special_leaders": [name for name, var in att_special_vars.items() if var.get()],
        "cards": attacker_cards_var.get(),
        "sudden_attack": sudden_attack_var.get(),
        "cards_left": attacker_cards_var.get()
    }
    def_state = {
        "normal": defender_normal_var.get(),
        "elite": defender_elite_var.get(),
        "special_elite": defender_special_elite_var.get(),
        "normal_leader": defender_normal_leader_var.get(),
        "special_leaders": [name for name, var in def_special_vars.items() if var.get()],
        "cards": defender_cards_var.get(),
        "cards_left": defender_cards_var.get(),
        "settlement": defender_settlement_var.get()
    }
    # Check: total number of units should not exceed 6
    total_att_units = att_state['normal'] + att_state['elite'] + att_state['special_elite']
    total_def_units = def_state['normal'] + def_state['elite'] + def_state['special_elite']
    if total_att_units > 6 or total_def_units > 6:
        error_msg = ""
        if total_att_units > 6 and total_def_units > 6:
            error_msg = "Both armies have more than 6 units in total."
        elif total_att_units > 6:
            error_msg = "The attacking army has more than 6 units in total."
        else:
            error_msg = "The defending army has more than 6 units in total."
        messagebox.showerror("Error", error_msg)
        return
    # Run 1000 battles to estimate probabilities and statistics
    simulations = 1000
    attacker_wins = defender_wins = 0
    attacker_survivors_total = 0
    defender_survivors_total = 0
    attacker_leader_survived_count = 0
    defender_leader_survived_count = 0
    for _ in range(simulations):
        outcome, att_left, def_left, att_leader_alive, def_leader_alive, att_strongest, def_strongest = simulate_battle(att_state, def_state, settlement=settlement_var.get(), sudden_attack=sudden_attack_var.get(), log_active=False)
        if outcome == "Attacker wins":
            attacker_wins += 1
        elif outcome == "Defender wins":
            defender_wins += 1
        # Accumulate statistics on survivors and leaders
        attacker_survivors_total += att_left
        defender_survivors_total += def_left
        if att_leader_alive: attacker_leader_survived_count += 1
        if def_leader_alive: defender_leader_survived_count += 1
        if att_strongest: att_strongest_name = att_strongest
        if def_strongest: def_strongest_name = def_strongest
    # Output results
    output_text.configure(state="normal")
    output_text.delete("1.0", tk.END)
    # Win probabilities and draw
    draws = simulations - attacker_wins - defender_wins
    attacker_pct = attacker_wins / simulations * 100
    defender_pct = defender_wins / simulations * 100
    draw_pct = draws / simulations * 100
    output_text.insert(tk.END, f"\nAttacker win chance: {attacker_pct:.1f}% | defender win chance: {defender_pct:.1f}% | draw: {draw_pct:.1f}% (simulations: {simulations})")
    # Average surviving units for attacker and defender
    avg_att_survivors = attacker_survivors_total / simulations
    avg_def_survivors = defender_survivors_total / simulations
    output_text.insert(tk.END, f"\nAverage surviving units – attacker: {avg_att_survivors:.1f}, defender: {avg_def_survivors:.1f}")
    # Chance of survival of the strongest leader for each side
    leader_att_survival_pct = (attacker_leader_survived_count / simulations) * 100
    leader_def_survival_pct = (defender_leader_survived_count / simulations) * 100
    if att_strongest_name and att_strongest_name != "none":
        output_text.insert(tk.END, f"\nChance of attacker's strongest leader ({att_strongest_name}) surviving: {leader_att_survival_pct:.1f}%")
    if def_strongest_name and def_strongest_name != "none":
        output_text.insert(tk.END, f"\nChance of defender's strongest leader ({def_strongest_name}) surviving: {leader_def_survival_pct:.1f}%")
    output_text.configure(state="disabled")
    output_text.yview_moveto(0)

# Function to display the detailed log of a single battle
def show_log():
    att_state = {
        "normal": attacker_normal_var.get(),
        "elite": attacker_elite_var.get(),
        "special_elite": attacker_special_elite_var.get(),
        "normal_leader": attacker_normal_leader_var.get(),
        "special_leaders": [name for name, var in att_special_vars.items() if var.get()],
        "sudden_attack": sudden_attack_var.get(),
        "cards": attacker_cards_var.get()
    }
    def_state = {
        "normal": defender_normal_var.get(),
        "elite": defender_elite_var.get(),
        "special_elite": defender_special_elite_var.get(),
        "normal_leader": defender_normal_leader_var.get(),
        "special_leaders": [name for name, var in def_special_vars.items() if var.get()],
        "cards": defender_cards_var.get(),
        "settlement": defender_settlement_var.get()
    }
    # Check total units (no more than 6)
    total_att_units = att_state['normal'] + att_state['elite'] + att_state['special_elite']
    total_def_units = def_state['normal'] + def_state['elite'] + def_state['special_elite']
    if total_att_units > 6 or total_def_units > 6:
        error_msg = ""
        if total_att_units > 6 and total_def_units > 6:
            error_msg = "Both armies have more than 6 units in total."
        elif total_att_units > 6:
            error_msg = "The attacking army has more than 6 units in total."
        else:
            error_msg = "The defending army has more than 6 units in total."
        messagebox.showerror("Error", error_msg)
        return
    # Get log of a single battle
    log = simulate_battle(att_state, def_state, settlement=settlement_var.get(), sudden_attack=sudden_attack_var.get(), log_active=True)
    # Display battle log in a new window
    log_window = tk.Toplevel(root)
    log_window.title("Battle Log")
    text = tk.Text(log_window, width=100, height=30, wrap="word")
    text.pack(side="left", fill="both", expand=True)
    scrollbar = ttk.Scrollbar(log_window, orient="vertical", command=text.yview)
    scrollbar.pack(side="right", fill="y")
    text.configure(yscrollcommand=scrollbar.set, state="normal")
    for line in log:
        text.insert(tk.END, line + "\n")
    text.configure(state="disabled")
    text.yview_moveto(0)

# Control buttons
ttk.Button(root, text="Calculate Battle", command=run_calculation).grid(row=2, column=0, padx=5, pady=5)
ttk.Button(root, text="Show Battle Log", command=show_log).grid(row=2, column=1, padx=5, pady=5)

root.mainloop()