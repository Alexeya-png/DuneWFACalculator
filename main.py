import random
import copy
import tkinter as tk
from tkinter import ttk, messagebox

text = {
    'ru': {
        'title': "Dune: War for Arrakis - Калькулятор боя",
        'attacker_frame': "Атакующий",
        'defender_frame': "Защитник",
        'normal_units': "Обычные отряды:",
        'elite_units': "Элитные отряды:",
        'special_elite_units': "Особые элитные отряды:",
        'ornithopter_units': "Ударный орнитоптер:",
        'normal_leaders': "Обычные лидеры:",
        'cards': "Карты (доп. кубики):",
        'sudden_attack': "Внезапная атака",
        'ongoing_attack': "Атака +1 кубик",
        'sardaukar_attack': "Атака сардаукарами",
        'sudden_attack_4max': "Внезапная атака 4max",
        'settlement_dice': "Поселение (кубики):",
        'atreides_fremen_leaders': "Лидеры Атрейдес/Фримен:",
        'harkonnen_corino_leaders': "Лидеры Харконнен/Коррино:",
        'attack_on_settlement': "Атака на поселение (штраф атакующему)",
        'calculate_battle': "Рассчитать бой",
        'show_battle_log': "Показать лог боя",
        'error_title': "Ошибка",
        'units_limit_error': "Суммарно можно не более 6 отрядов!",
        'both_armies_over_6': "В обеих армиях суммарно больше 6 фигурок.",
        'attacker_over_6': "У атакующей армии суммарно больше 6 фигурок.",
        'defender_over_6': "У защищающейся армии суммарно больше 6 фигурок.",
        'attacker_win_chance': "Шанс победы атакующего",
        'defender_win_chance': "шанс победы защитника",
        'draw': "ничья",
        'simulations': "симуляций",
        'average_surviving': "Среднее выживших отрядов –",
        'attacker_role': "атакующий",
        'defender_role': "защитник",
        'strongest_leader_survival_att': "Шанс выживания самого сильного лидера атакующего",
        'strongest_leader_survival_def': "Шанс выживания самого сильного лидера защитника",
        'battle_log_title': "Лог боя",
        'assault_damage': "Атакующий наносит урон за штурм",
        'worm_attack_normal': "Атака червем",
        'worm_attack_shai': "Атака Шай-Хулуд",
        'ongoing_attack_log': "Атака +1 кубик: атакующий получает +1 кубик в этом раунде."
    },
    'en': {
        'title': "Dune: War for Arrakis - Battle Calculator",
        'attacker_frame': "Attacker",
        'defender_frame': "Defender",
        'normal_units': "Normal units:",
        'elite_units': "Elite units:",
        'special_elite_units': "Special elite units:",
        'ornithopter_units': "Strike Ornithopter:",
        'normal_leaders': "Normal leaders:",
        'cards': "Cards (extra dice):",
        'sudden_attack': "Sudden Attack",
        'ongoing_attack': "Attack +1 die",
        'sardaukar_attack': "Sardaukar Attack",
        'sudden_attack_4max': "Sudden Attack (max 4 dice)",
        'settlement_dice': "Settlement (dice):",
        'atreides_fremen_leaders': "Atreides/Fremen Leaders:",
        'harkonnen_corino_leaders': "Harkonnen/Corino Leaders:",
        'attack_on_settlement': "Attack on settlement (attacker penalty)",
        'calculate_battle': "Calculate Battle",
        'show_battle_log': "Show Battle Log",
        'error_title': "Error",
        'units_limit_error': "Total units cannot exceed 6!",
        'both_armies_over_6': "Both armies have more than 6 units in total.",
        'attacker_over_6': "The attacking army has more than 6 units in total.",
        'defender_over_6': "The defending army has more than 6 units in total.",
        'attacker_win_chance': "Attacker win chance",
        'defender_win_chance': "defender win chance",
        'draw': "draw",
        'simulations': "simulations",
        'average_surviving': "Average surviving units –",
        'attacker_role': "attacker",
        'defender_role': "defender",
        'strongest_leader_survival_att': "Chance of attacker's strongest leader surviving",
        'strongest_leader_survival_def': "Chance of defender's strongest leader surviving",
        'battle_log_title': "Battle Log",
        'assault_damage': "Attacker suffers assault damage",
        'worm_attack_normal': "Worm attack (normal)",
        'worm_attack_shai': "Worm attack (Shai-Hulud)",
        'ongoing_attack_log': "Ongoing attack: attacker gains +1 die this round."
    }
}

current_lang = 'ru'

special_leaders_data = {
    "Paul Muad'Dib": {"swords": 2, "shields": 1},
    "Paul Atreides": {"swords": 1, "shields": 0},
    "Lady Jessica": {"swords": 0, "shields": 1},
    "Mother Jessica": {"swords": 0, "shields": 2},
    "Gurney Halleck": {"swords": 2, "shields": 1},
    "Stabban Tuek": {"swords": 1, "shields": 1},
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
    if len(forms) == 3:
        if num % 10 == 1 and num % 100 != 11:
            return f"{num} {forms[0]}"
        elif 2 <= num % 10 <= 4 and not (12 <= num % 100 <= 14):
            return f"{num} {forms[1]}"
        else:
            return f"{num} {forms[2]}"
    elif len(forms) == 2:
        return f"{num} {forms[0]}" if num == 1 else f"{num} {forms[1]}"
    else:
        return f"{num} {forms[0]}"

def allocate_casualties(side_name, casualties, state, log_active=True, settlement_flag=False):
    log = []
    if settlement_flag:
        while casualties > 0:
            if casualties > 0 and state['elite'] > 0:
                state['elite'] -= 1
                state['normal'] += 1
                casualties -= 1
                if log_active:
                    if current_lang == 'ru':
                        log.append(f"{side_name}: элитный отряд понижен до обычного.")
                    else:
                        log.append(f"{side_name}: elite unit downgraded to normal.")
                continue
            if casualties > 0 and state['normal_leader'] > 0:
                state['normal_leader'] -= 1
                casualties -= 1
                if log_active:
                    if current_lang == 'ru':
                        log.append(f"{side_name}: обычный лидер убит.")
                    else:
                        log.append(f"{side_name}: normal leader killed.")
                continue
            if casualties > 0 and state.get('ornithopter', 0) > 0:
                state['ornithopter'] -= 1
                casualties -= 2
                if casualties < 0:
                    casualties = 0
                if log_active:
                    if current_lang == 'ru':
                        log.append(f"{side_name}: ударный орнитоптер сбит.")
                    else:
                        log.append(f"{side_name}: strike ornithopter shot down.")
                continue
            if casualties > 0 and state['normal'] > 0:
                total_units = state['normal'] + state['elite'] + state['special_elite']
                if total_units + state.get('settlement', 0) >= 6:
                    to_kill = min(casualties, state['normal'], (total_units + state.get('settlement', 0) - 5))
                    state['normal'] -= to_kill
                    casualties -= to_kill
                    if log_active and to_kill > 0:
                        if to_kill == 1:
                            if current_lang == 'ru':
                                log.append(f"{side_name}: 1 обычный отряд уничтожен.")
                            else:
                                log.append(f"{side_name}: 1 normal unit destroyed.")
                        else:
                            if current_lang == 'ru':
                                log.append(f"{side_name}: {to_kill} обычных отрядов уничтожено.")
                            else:
                                log.append(f"{side_name}: {to_kill} normal units destroyed.")
                    continue
            if casualties > 0 and state['special_elite'] > 0:
                state['special_elite'] -= 1
                state['normal'] += 1
                casualties -= 1
                if log_active:
                    if current_lang == 'ru':
                        log.append(f"{side_name}: особый элитный отряд понижен до обычного.")
                    else:
                        log.append(f"{side_name}: special elite unit downgraded to normal.")
                continue
            if casualties > 0 and len(state['special_leaders']) > 0:
                weakest = min(state['special_leaders'], key=lambda name: special_leaders_data[name]['swords'] + special_leaders_data[name]['shields'])
                state['special_leaders'].remove(weakest)
                casualties -= 1
                if log_active:
                    if current_lang == 'ru':
                        log.append(f"{side_name}: особый лидер {weakest} убит.")
                    else:
                        log.append(f"{side_name}: special leader {weakest} killed.")
                continue
            if casualties > 0 and state['normal'] > 0:
                if casualties >= state['normal']:
                    num = state['normal']
                    state['normal'] = 0
                    casualties -= num
                    if log_active:
                        if num == 1:
                            if current_lang == 'ru':
                                log.append(f"{side_name}: 1 обычный отряд уничтожен.")
                            else:
                                log.append(f"{side_name}: 1 normal unit destroyed.")
                        else:
                            if current_lang == 'ru':
                                log.append(f"{side_name}: {num} обычных отрядов уничтожено.")
                            else:
                                log.append(f"{side_name}: {num} normal units destroyed.")
                else:
                    num = casualties
                    state['normal'] -= num
                    casualties = 0
                    if log_active:
                        if num == 1:
                            if current_lang == 'ru':
                                log.append(f"{side_name}: 1 обычный отряд уничтожен.")
                            else:
                                log.append(f"{side_name}: 1 normal unit destroyed.")
                        else:
                            if current_lang == 'ru':
                                log.append(f"{side_name}: {num} обычных отрядов уничтожено.")
                            else:
                                log.append(f"{side_name}: {num} normal units destroyed.")
                continue
            break
        return log
    while casualties > 0:
        if casualties > 0 and state['elite'] > 0:
            state['elite'] -= 1
            state['normal'] += 1
            casualties -= 1
            if log_active:
                if current_lang == 'ru':
                    log.append(f"{side_name}: элитный отряд понижен до обычного.")
                else:
                    log.append(f"{side_name}: elite unit downgraded to normal.")
            continue
        if casualties > 0 and state['normal_leader'] > 0:
            state['normal_leader'] -= 1
            casualties -= 1
            if log_active:
                if current_lang == 'ru':
                    log.append(f"{side_name}: обычный лидер убит.")
                else:
                    log.append(f"{side_name}: normal leader killed.")
            continue
        if casualties > 0 and state.get('ornithopter', 0) > 0:
            state['ornithopter'] -= 1
            casualties -= 2
            if casualties < 0:
                casualties = 0
            if log_active:
                if current_lang == 'ru':
                    log.append(f"{side_name}: ударный орнитоптер сбит.")
                else:
                    log.append(f"{side_name}: strike ornithopter shot down.")
            continue
        if casualties > 0 and len(state['special_leaders']) > 2:
            weakest = min(state['special_leaders'], key=lambda name: special_leaders_data[name]['swords'] + special_leaders_data[name]['shields'])
            state['special_leaders'].remove(weakest)
            casualties -= 1
            if log_active:
                if current_lang == 'ru':
                    log.append(f"{side_name}: особый лидер {weakest} убит.")
                else:
                    log.append(f"{side_name}: special leader {weakest} killed.")
            continue
        if casualties > 0 and state['special_elite'] > 0:
            state['special_elite'] -= 1
            state['normal'] += 1
            casualties -= 1
            if log_active:
                if current_lang == 'ru':
                    log.append(f"{side_name}: особый элитный отряд понижен до обычного.")
                else:
                    log.append(f"{side_name}: special elite unit downgraded to normal.")
            continue
        if casualties > 0 and state['normal'] > 4:
            to_kill = min(casualties, state['normal'] - 4)
            state['normal'] -= to_kill
            casualties -= to_kill
            if log_active and to_kill > 0:
                if to_kill == 1:
                    if current_lang == 'ru':
                        log.append(f"{side_name}: 1 обычный отряд уничтожен.")
                    else:
                        log.append(f"{side_name}: 1 normal unit destroyed.")
                else:
                    if current_lang == 'ru':
                        log.append(f"{side_name}: {to_kill} обычных отрядов уничтожено.")
                    else:
                        log.append(f"{side_name}: {to_kill} normal units destroyed.")
            continue
        if casualties > 0 and len(state['special_leaders']) > 0:
            weakest = min(state['special_leaders'], key=lambda name: special_leaders_data[name]['swords'] + special_leaders_data[name]['shields'])
            state['special_leaders'].remove(weakest)
            casualties -= 1
            if log_active:
                if current_lang == 'ru':
                    log.append(f"{side_name}: особый лидер {weakest} убит.")
                else:
                    log.append(f"{side_name}: special leader {weakest} killed.")
            continue
        if casualties > 0 and state['normal'] > 0:
            if casualties >= state['normal']:
                num = state['normal']
                state['normal'] = 0
                casualties -= num
                if log_active:
                    if num == 1:
                        if current_lang == 'ru':
                            log.append(f"{side_name}: 1 обычный отряд уничтожен.")
                        else:
                            log.append(f"{side_name}: 1 normal unit destroyed.")
                    else:
                        if current_lang == 'ru':
                            log.append(f"{side_name}: {num} обычных отрядов уничтожено.")
                        else:
                            log.append(f"{side_name}: {num} normal units destroyed.")
            else:
                num = casualties
                state['normal'] -= num
                casualties = 0
                if log_active:
                    if num == 1:
                        if current_lang == 'ru':
                            log.append(f"{side_name}: 1 обычный отряд уничтожен.")
                        else:
                            log.append(f"{side_name}: 1 normal unit destroyed.")
                    else:
                        if current_lang == 'ru':
                            log.append(f"{side_name}: {num} обычных отрядов уничтожено.")
                        else:
                            log.append(f"{side_name}: {num} normal units destroyed.")
            continue
        break
    return log

def simulate_battle(att, deff, settlement=False, sudden_attack=False, sudden_attack_4max=False, ongoing_attack=False, sardaukar_attack=False, worm_attack_normal=False, worm_attack_shai=False, log_active=True):
    att_state = copy.deepcopy(att)
    def_state = copy.deepcopy(deff)
    log = []
    if worm_attack_normal or worm_attack_shai:
        dice = 4 if worm_attack_normal else 6
        hits = 0
        for _ in range(dice):
            roll = random.randint(1, 6)
            if roll <= 3:
                hits += 1
        if log_active:
            if current_lang == 'ru':
                hit_str = format_count(hits, ("попадание", "попадания", "попаданий"))
                log.append(f"Атака червями ({'обычная' if worm_attack_normal else 'Шай-Хулуд'}): атакующий перед боем нанес {hit_str}.")
            else:
                hit_str = format_count(hits, ("hit", "hits"))
                log.append(f"Worm attack ({'normal' if worm_attack_normal else 'Shai-Hulud'}): attacker inflicted {hit_str} before the battle.")
        worm_log = allocate_casualties(text[current_lang]['defender_frame'], hits, def_state, log_active=log_active)
        if log_active:
            log.extend(worm_log)
    if (sudden_attack or sudden_attack_4max) and log_active:
        if current_lang == 'ru':
            if sudden_attack_4max:
                log.append("Внезапная атака (4 макс): атакующий получает +1 особый символ (звезда) в этом раунде, защитник бросает не более 4 кубиков.")
            else:
                log.append("Внезапная атака: атакующий получает +1 особый символ (звезда) в этом раунде.")
        else:
            if sudden_attack_4max:
                log.append("Sudden attack (4 max): attacker gains +1 special symbol (star) this round, defender rolls at most 4 dice.")
            else:
                log.append("Sudden attack: attacker gains +1 special symbol (star) this round.")
    round_num = 1
    while True:
        att_units_count = att_state['normal'] + att_state['elite'] + att_state['special_elite']
        def_units_count = def_state['normal'] + def_state['elite'] + def_state['special_elite']
        if att_units_count == 0 or def_units_count == 0:
            break
        att_cards_left = att_state.get('cards_left', att_state.get('cards', 0))
        def_cards_left = def_state.get('cards_left', def_state.get('cards', 0))
        att_cards_this_round = min(att_cards_left, max(0, 6 - att_units_count))
        if round_num == 1 and (sudden_attack or sudden_attack_4max):
            def_cards_this_round = 0
            if sudden_attack_4max:
                defender_dice = min(4, def_units_count + def_state.get('settlement', 0))
            else:
                defender_dice = min(6, def_units_count + def_state.get('settlement', 0))
        else:
            def_cards_this_round = min(def_cards_left, max(0, 6 - def_units_count))
            defender_dice = min(6, def_units_count + def_cards_this_round + def_state.get('settlement', 0))
        attacker_dice = min(6, att_units_count + att_cards_this_round)
        att_state['cards_left'] = att_cards_left - att_cards_this_round
        if (sudden_attack or sudden_attack_4max) and round_num == 1:
            def_state['cards_left'] = def_cards_left
        else:
            def_state['cards_left'] = def_cards_left - def_cards_this_round
        if ongoing_attack:
            attacker_dice = min(6, attacker_dice + 1)
            if log_active:
                log.append(text[current_lang]['ongoing_attack_log'])
        a_swords = a_shields = a_stars = 0
        for _ in range(attacker_dice):
            roll = random.randint(1, 6)
            if roll <= 3:
                a_swords += 1
            elif roll <= 5:
                a_shields += 1
            else:
                a_stars += 1
        d_swords = d_shields = d_stars = 0
        for _ in range(defender_dice):
            roll = random.randint(1, 6)
            if roll <= 3:
                d_swords += 1
            elif roll <= 5:
                d_shields += 1
            else:
                d_stars += 1
        if (sudden_attack or sudden_attack_4max) and round_num == 1:
            a_stars += 1
        total_att_leaders = att_state['normal_leader'] + len(att_state['special_leaders']) + att_state.get('ornithopter', 0)
        total_def_leaders = def_state['normal_leader'] + len(def_state['special_leaders']) + def_state.get('ornithopter', 0)
        att_extra_swords = att_extra_shields = 0
        def_extra_swords = def_extra_shields = 0
        att_used = []
        def_used = []
        if a_stars > 0 and total_att_leaders > 0:
            leader_list = []
            for _ in range(att_state['normal_leader']):
                leader_list.append(("Unnamed", 1, 0))
            for name in att_state['special_leaders']:
                vals = special_leaders_data.get(name, {"swords": 0, "shields": 0})
                leader_list.append((name, vals['swords'], vals['shields']))
            for _ in range(att_state.get('ornithopter', 0)):
                leader_list.append(("Ornithopter", 1, 0))
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
        if d_stars > 0 and total_def_leaders > 0:
            leader_list = []
            for _ in range(def_state['normal_leader']):
                leader_list.append(("Unnamed", 1, 0))
            for name in def_state['special_leaders']:
                vals = special_leaders_data.get(name, {"swords": 0, "shields": 0})
                leader_list.append((name, vals['swords'], vals['shields']))
            for _ in range(def_state.get('ornithopter', 0)):
                leader_list.append(("Ornithopter", 1, 0))
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
        total_a_swords = a_swords + att_extra_swords
        total_a_shields = a_shields + att_extra_shields
        total_d_swords = d_swords + def_extra_swords
        total_d_shields = d_shields + def_extra_shields
        if att_state['special_elite'] > 0:
            cancel = min(total_d_shields, att_state['special_elite'])
            total_d_shields -= cancel
            if log_active and cancel > 0:
                if current_lang == 'ru':
                    log.append(f"Особые элитные атакующего отменяют {cancel} результат(ов) щита у защитника.")
                else:
                    log.append(f"Attacker's special elite cancel {cancel} shield result(s) of the defender.")
        if def_state['special_elite'] > 0:
            cancel = min(total_a_shields, def_state['special_elite'])
            total_a_shields -= cancel
            if log_active and cancel > 0:
                if current_lang == 'ru':
                    log.append(f"Особые элитные защитника отменяют {cancel} результат(ов) щита у атакующего.")
                else:
                    log.append(f"Defender's special elite cancel {cancel} shield result(s) of the attacker.")
        hits_on_def = total_a_swords - total_d_shields
        hits_on_att = total_d_swords - total_a_shields
        if hits_on_def < 0:
            hits_on_def = 0
        if hits_on_att < 0:
            hits_on_att = 0
        if log_active:
            if current_lang == 'ru':
                dice_word_att = "кубиков"
            else:
                dice_word_att = "die" if attacker_dice == 1 else "dice"
            sword_str = format_count(a_swords, ("меч", "меча", "мечей")) if current_lang == 'ru' else format_count(a_swords, ("sword", "swords"))
            shield_str = format_count(a_shields, ("щит", "щита", "щитов")) if current_lang == 'ru' else format_count(a_shields, ("shield", "shields"))
            special_str = format_count(a_stars, ("особый символ", "особых символа", "особых символов")) if current_lang == 'ru' else format_count(a_stars, ("special symbol", "special symbols"))
            if current_lang == 'ru':
                log.append(f"Раунд {round_num}: атакующий бросил {attacker_dice} {dice_word_att} -> {sword_str}, {shield_str}, {special_str}.")
            else:
                log.append(f"Round {round_num}: attacker rolled {attacker_dice} {dice_word_att} -> {sword_str}, {shield_str}, {special_str}.")
            if current_lang == 'ru':
                dice_word_def = "кубиков"
            else:
                dice_word_def = "die" if defender_dice == 1 else "dice"
            sword_str = format_count(d_swords, ("меч", "меча", "мечей")) if current_lang == 'ru' else format_count(d_swords, ("sword", "swords"))
            shield_str = format_count(d_shields, ("щит", "щита", "щитов")) if current_lang == 'ru' else format_count(d_shields, ("shield", "shields"))
            special_str = format_count(d_stars, ("особый символ", "особых символа", "особых символов")) if current_lang == 'ru' else format_count(d_stars, ("special symbol", "special symbols"))
            if current_lang == 'ru':
                log.append(f"Раунд {round_num}: защитник бросил {defender_dice} {dice_word_def} -> {sword_str}, {shield_str}, {special_str}.")
            else:
                log.append(f"Round {round_num}: defender rolled {defender_dice} {dice_word_def} -> {sword_str}, {shield_str}, {special_str}.")
            if att_used:
                unnamed_count = sum(1 for x in att_used if x[0] == "Unnamed")
                orn_count = sum(1 for x in att_used if x[0] == "Ornithopter")
                parts = []
                if unnamed_count > 0:
                    if current_lang == 'ru':
                        leader_str = format_count(unnamed_count, ("безымянный лидер", "безымянных лидера", "безымянных лидеров"))
                        verb = "добавил" if unnamed_count == 1 else "добавили"
                        sword_str_u = format_count(unnamed_count, ("меч", "меча", "мечей"))
                        parts.append(f"{leader_str} {verb} {sword_str_u}")
                    else:
                        parts.append(f"{unnamed_count} unnamed leader{'s' if unnamed_count != 1 else ''} added {unnamed_count} sword{'s' if unnamed_count != 1 else ''}")
                if orn_count > 0:
                    if current_lang == 'ru':
                        parts.append(f"Ударный орнитоптер добавил {format_count(orn_count, ('меч', 'меча', 'мечей'))}")
                    else:
                        parts.append(f"Strike ornithopter added {orn_count} sword{'s' if orn_count != 1 else ''}")
                for (name, sw, sh) in att_used:
                    if name in ("Unnamed", "Ornithopter"):
                        continue
                    subparts = []
                    if sw:
                        subparts.append(format_count(sw, ("меч", "меча", "мечей")) if current_lang == 'ru' else format_count(sw, ("sword", "swords")))
                    if sh:
                        subparts.append(format_count(sh, ("щит", "щита", "щитов")) if current_lang == 'ru' else format_count(sh, ("shield", "shields")))
                    contribution = " и ".join(subparts) if current_lang == 'ru' else " and ".join(subparts)
                    if current_lang == 'ru':
                        parts.append(f"{name} добавил {contribution}")
                    else:
                        parts.append(f"{name} added {contribution}")
                if current_lang == 'ru':
                    log.append("Атакующий использует особые символы: " + "; ".join(parts) + ".")
                else:
                    log.append("Attacker uses special symbols: " + "; ".join(parts) + ".")
            else:
                if a_stars > 0 and total_att_leaders == 0:
                    if current_lang == 'ru':
                        log.append("Атакующий выбросил особые символы, но некому их использовать.")
                    else:
                        log.append("Attacker rolled special symbols, but no one can use them.")
            if def_used:
                unnamed_count = sum(1 for x in def_used if x[0] == "Unnamed")
                orn_count = sum(1 for x in def_used if x[0] == "Ornithopter")
                parts = []
                if unnamed_count > 0:
                    if current_lang == 'ru':
                        leader_str = format_count(unnamed_count, ("безымянный лидер", "безымянных лидера", "безымянных лидеров"))
                        verb = "добавил" if unnamed_count == 1 else "добавили"
                        sword_str_u = format_count(unnamed_count, ("меч", "меча", "мечей"))
                        parts.append(f"{leader_str} {verb} {sword_str_u}")
                    else:
                        parts.append(f"{unnamed_count} unnamed leader{'s' if unnamed_count != 1 else ''} added {unnamed_count} sword{'s' if unnamed_count != 1 else ''}")
                if orn_count > 0:
                    if current_lang == 'ru':
                        parts.append(f"Ударный орнитоптер добавил {format_count(orn_count, ('меч', 'меча', 'мечей'))}")
                    else:
                        parts.append(f"Strike ornithopter added {orn_count} sword{'s' if orn_count != 1 else ''}")
                for (name, sw, sh) in def_used:
                    if name in ("Unnamed", "Ornithopter"):
                        continue
                    subparts = []
                    if sw:
                        subparts.append(format_count(sw, ("меч", "меча", "мечей")) if current_lang == 'ru' else format_count(sw, ("sword", "swords")))
                    if sh:
                        subparts.append(format_count(sh, ("щит", "щита", "щитов")) if current_lang == 'ru' else format_count(sh, ("shield", "shields")))
                    contribution = " и ".join(subparts) if current_lang == 'ru' else " and ".join(subparts)
                    if current_lang == 'ru':
                        parts.append(f"{name} добавил {contribution}")
                    else:
                        parts.append(f"{name} added {contribution}")
                if current_lang == 'ru':
                    log.append("Защитник использует особые символы: " + "; ".join(parts) + ".")
                else:
                    log.append("Defender uses special symbols: " + "; ".join(parts) + ".")
            else:
                if d_stars > 0 and total_def_leaders == 0:
                    if current_lang == 'ru':
                        log.append("Защитник выбросил особые символы, но некому их использовать.")
                    else:
                        log.append("Defender rolled special symbols, but no one can use them.")
            sword_str_a = format_count(total_a_swords, ("меч", "меча", "мечей")) if current_lang == 'ru' else format_count(total_a_swords, ("sword", "swords"))
            shield_str_a = format_count(total_a_shields, ("щит", "щита", "щитов")) if current_lang == 'ru' else format_count(total_a_shields, ("shield", "shields"))
            sword_str_d = format_count(total_d_swords, ("меч", "меча", "мечей")) if current_lang == 'ru' else format_count(total_d_swords, ("sword", "swords"))
            shield_str_d = format_count(total_d_shields, ("щит", "щита", "щитов")) if current_lang == 'ru' else format_count(total_d_shields, ("shield", "shields"))
            if current_lang == 'ru':
                log.append(f"Итого после способностей: у атакующего {sword_str_a}, {shield_str_a}; у защитника {sword_str_d}, {shield_str_d}.")
                log.append(f"Нанесённый урон: атакующий получил {hits_on_att} попаданий, защитник получил {hits_on_def} попаданий.")
            else:
                log.append(f"After abilities: attacker has {sword_str_a}, {shield_str_a}; defender has {sword_str_d}, {shield_str_d}.")
                log.append(f"Damage dealt: attacker took {hits_on_att} {'hit' if hits_on_att == 1 else 'hits'}, defender took {hits_on_def} {'hit' if hits_on_def == 1 else 'hits'}.")
        if hits_on_def > 0:
            def_casualty_log = allocate_casualties(text[current_lang]['defender_frame'], hits_on_def, def_state, log_active=log_active, settlement_flag=settlement)
            if log_active:
                log.extend(def_casualty_log)
        if hits_on_att > 0:
            att_casualty_log = allocate_casualties(text[current_lang]['attacker_frame'], hits_on_att, att_state, log_active=log_active)
            if log_active:
                log.extend(att_casualty_log)
        att_units_alive = att_state['normal'] + att_state['elite'] + att_state['special_elite']
        def_units_alive = def_state['normal'] + def_state['elite'] + def_state['special_elite']
        if att_units_alive == 0 or def_units_alive == 0:
            break
        def_units_after = def_state['normal'] + def_state['elite'] + def_state['special_elite']
        if settlement and def_units_after > 0 and not sardaukar_attack:
            penalty = 1
            penalty_log = allocate_casualties(text[current_lang]['assault_damage'], penalty, att_state, log_active=log_active)
            if log_active:
                log.extend(penalty_log)
        if log_active:
            att_special_leaders = ", ".join(att_state['special_leaders']) if att_state['special_leaders'] else "нет"
            def_special_leaders = ", ".join(def_state['special_leaders']) if def_state['special_leaders'] else "нет"
            log.append(f"Конец раунда {round_num}: атакующий - обычных отрядов: {att_state['normal']}, элитных: {att_state['elite']}, особых элитных: {att_state['special_elite']}; обычных лидеров: {att_state['normal_leader']}, орнитоптеров: {att_state.get('ornithopter', 0)}, особых лидеров: {att_special_leaders}.")
            log.append(f"Конец раунда {round_num}: защитник - обычных отрядов: {def_state['normal']}, элитных: {def_state['elite']}, особых элитных: {def_state['special_elite']}; обычных лидеров: {def_state['normal_leader']}, орнитоптеров: {def_state.get('ornithopter', 0)}, особых лидеров: {def_special_leaders}.")
            log.append("----")
        round_num += 1
    att_units = att_state['normal'] + att_state['elite'] + att_state['special_elite']
    def_units = def_state['normal'] + def_state['elite'] + def_state['special_elite']
    att_strongest = None
    def_strongest = None
    leader_list = []
    for _ in range(att_state['normal_leader']):
        leader_list.append(("Unnamed", 1, 0))
    for name in att_state['special_leaders']:
        vals = special_leaders_data.get(name, {"swords": 0, "shields": 0})
        leader_list.append((name, vals['swords'], vals['shields']))
    for _ in range(att_state.get('ornithopter', 0)):
        leader_list.append(("Ornithopter", 1, 0))
    if leader_list:
        leader_list.sort(key=lambda x: (x[1] + x[2], x[1]), reverse=True)
        att_strongest = leader_list[0][0]
    leader_list = []
    for _ in range(def_state['normal_leader']):
        leader_list.append(("Unnamed", 1, 0))
    for name in def_state['special_leaders']:
        vals = special_leaders_data.get(name, {"swords": 0, "shields": 0})
        leader_list.append((name, vals['swords'], vals['shields']))
    for _ in range(def_state.get('ornithopter', 0)):
        leader_list.append(("Ornithopter", 1, 0))
    if leader_list:
        leader_list.sort(key=lambda x: (x[1] + x[2], x[1]), reverse=True)
        def_strongest = leader_list[0][0]
    if att_strongest is None:
        att_strongest_survived = False
    elif att_strongest == "Unnamed":
        att_strongest_survived = att_state['normal_leader'] > 0
    elif att_strongest == "Ornithopter":
        att_strongest_survived = att_state.get('ornithopter', 0) > 0
    else:
        att_strongest_survived = att_strongest in att_state['special_leaders']
    if def_strongest is None:
        def_strongest_survived = False
    elif def_strongest == "Unnamed":
        def_strongest_survived = def_state['normal_leader'] > 0
    elif def_strongest == "Ornithopter":
        def_strongest_survived = def_state.get('ornithopter', 0) > 0
    else:
        def_strongest_survived = def_strongest in def_state['special_leaders']
    if log_active:
        if att_units > 0 and def_units == 0:
            log.append("Итог: победа атакующего!" if current_lang == 'ru' else "Result: attacker wins!")
        elif def_units > 0 and att_units == 0:
            log.append("Итог: победа защитника." if current_lang == 'ru' else "Result: defender wins.")
        else:
            log.append("Итог: обе армии уничтожены." if current_lang == 'ru' else "Result: both armies are destroyed.")
        return log
    else:
        if att_units > 0 and def_units == 0:
            return ("Attacker wins", att_units, def_units, att_strongest_survived, def_strongest_survived, att_strongest, def_strongest)
        elif def_units > 0 and att_units == 0:
            return ("Defender wins", att_units, def_units, att_strongest_survived, def_strongest_survived, att_strongest, def_strongest)
        else:
            return ("Both destroyed", att_units, def_units, att_strongest_survived, def_strongest_survived, att_strongest, def_strongest)

def run_calculation():
    global current_lang
    att_state = {
        "normal": attacker_normal_var.get(),
        "elite": attacker_elite_var.get(),
        "special_elite": attacker_special_elite_var.get(),
        "normal_leader": attacker_normal_leader_var.get(),
        "ornithopter": attacker_ornithopter_var.get(),
        "special_leaders": [name for name, var in att_special_vars.items() if var.get()],
        "cards": attacker_cards_var.get(),
        "cards_left": attacker_cards_var.get(),
        "sudden_attack": sudden_attack_var.get(),
        "sardaukar_attack": sardaukar_attack_var.get(),
        "sudden_attack_4max": sudden_attack_4max_var.get(),
        "worm_attack_normal": worm_attack_normal_var.get(),
        "worm_attack_shai": worm_attack_shai_var.get()
    }
    def_state = {
        "normal": defender_normal_var.get(),
        "elite": defender_elite_var.get(),
        "special_elite": defender_special_elite_var.get(),
        "normal_leader": defender_normal_leader_var.get(),
        "ornithopter": defender_ornithopter_var.get(),
        "special_leaders": [name for name, var in def_special_vars.items() if var.get()],
        "cards": defender_cards_var.get(),
        "cards_left": defender_cards_var.get(),
        "settlement": defender_settlement_var.get()
    }
    total_att_units = att_state['normal'] + att_state['elite'] + att_state['special_elite']
    total_def_units = def_state['normal'] + def_state['elite'] + def_state['special_elite']
    if total_att_units > 6 or total_def_units > 6:
        if total_att_units > 6 and total_def_units > 6:
            error_msg = text[current_lang]['both_armies_over_6']
        elif total_att_units > 6:
            error_msg = text[current_lang]['attacker_over_6']
        else:
            error_msg = text[current_lang]['defender_over_6']
        messagebox.showerror(text[current_lang]['error_title'], error_msg)
        return
    simulations = 1000
    attacker_wins = defender_wins = 0
    attacker_survivors_total = 0
    defender_survivors_total = 0
    attacker_leader_survived_count = 0
    defender_leader_survived_count = 0
    att_strongest_name = ""
    def_strongest_name = ""
    for _ in range(simulations):
        outcome, att_left, def_left, att_leader_alive, def_leader_alive, att_strongest, def_strongest = simulate_battle(
            att_state, def_state, settlement=settlement_var.get(), sudden_attack=sudden_attack_var.get(), sudden_attack_4max=sudden_attack_4max_var.get(), sardaukar_attack=sardaukar_attack_var.get(), worm_attack_normal=worm_attack_normal_var.get(), worm_attack_shai=worm_attack_shai_var.get(), ongoing_attack=ongoing_attack_var.get(), log_active=False
        )
        if outcome == "Attacker wins":
            attacker_wins += 1
        elif outcome == "Defender wins":
            defender_wins += 1
        attacker_survivors_total += att_left
        defender_survivors_total += def_left
        if att_leader_alive:
            attacker_leader_survived_count += 1
        if def_leader_alive:
            defender_leader_survived_count += 1
        if att_strongest:
            att_strongest_name = att_strongest
        if def_strongest:
            def_strongest_name = def_strongest
    output_text.configure(state="normal")
    output_text.delete("1.0", tk.END)
    draws = simulations - attacker_wins - defender_wins
    attacker_pct = attacker_wins / simulations * 100
    defender_pct = defender_wins / simulations * 100
    draw_pct = draws / simulations * 100
    output_text.insert(tk.END, f"\n{text[current_lang]['attacker_win_chance']}: {attacker_pct:.1f}% | {text[current_lang]['defender_win_chance']}: {defender_pct:.1f}% | {text[current_lang]['draw']}: {draw_pct:.1f}% ({text[current_lang]['simulations']}: {simulations})")
    avg_att_survivors = attacker_survivors_total / simulations
    avg_def_survivors = defender_survivors_total / simulations
    output_text.insert(tk.END, f"\n{text[current_lang]['average_surviving']} {text[current_lang]['attacker_role']}: {avg_att_survivors:.1f}, {text[current_lang]['defender_role']}: {avg_def_survivors:.1f}")
    leader_att_survival_pct = (attacker_leader_survived_count / simulations) * 100
    leader_def_survival_pct = (defender_leader_survived_count / simulations) * 100
    if att_strongest_name and att_strongest_name != ("нет" if current_lang == 'ru' else "none"):
        output_text.insert(tk.END, f"\n{text[current_lang]['strongest_leader_survival_att']} ({att_strongest_name}): {leader_att_survival_pct:.1f}%")
    if def_strongest_name and def_strongest_name != ("нет" if current_lang == 'ru' else "none"):
        output_text.insert(tk.END, f"\n{text[current_lang]['strongest_leader_survival_def']} ({def_strongest_name}): {leader_def_survival_pct:.1f}%")
    output_text.configure(state="disabled")
    output_text.yview_moveto(0)

def show_log():
    global current_lang
    att_state = {
        "normal": attacker_normal_var.get(),
        "elite": attacker_elite_var.get(),
        "special_elite": attacker_special_elite_var.get(),
        "normal_leader": attacker_normal_leader_var.get(),
        "ornithopter": attacker_ornithopter_var.get(),
        "special_leaders": [name for name, var in att_special_vars.items() if var.get()],
        "sudden_attack": sudden_attack_var.get(),
        "sardaukar_attack": sardaukar_attack_var.get(),
        "sudden_attack_4max": sudden_attack_4max_var.get(),
        "worm_attack_normal": worm_attack_normal_var.get(),
        "worm_attack_shai": worm_attack_shai_var.get(),
        "cards": attacker_cards_var.get(),
        "cards_left": attacker_cards_var.get()
    }
    def_state = {
        "normal": defender_normal_var.get(),
        "elite": defender_elite_var.get(),
        "special_elite": defender_special_elite_var.get(),
        "normal_leader": defender_normal_leader_var.get(),
        "ornithopter": defender_ornithopter_var.get(),
        "special_leaders": [name for name, var in def_special_vars.items() if var.get()],
        "cards": defender_cards_var.get(),
        "settlement": defender_settlement_var.get(),
        "cards_left": defender_cards_var.get()
    }
    total_att_units = att_state['normal'] + att_state['elite'] + att_state['special_elite']
    total_def_units = def_state['normal'] + def_state['elite'] + def_state['special_elite']
    if total_att_units > 6 or total_def_units > 6:
        if total_att_units > 6 and total_def_units > 6:
            error_msg = text[current_lang]['both_armies_over_6']
        elif total_att_units > 6:
            error_msg = text[current_lang]['attacker_over_6']
        else:
            error_msg = text[current_lang]['defender_over_6']
        messagebox.showerror(text[current_lang]['error_title'], error_msg)
        return
    battle_log = simulate_battle(att_state, def_state, settlement=settlement_var.get(), sudden_attack=sudden_attack_var.get(), sudden_attack_4max=sudden_attack_4max_var.get(), sardaukar_attack=sardaukar_attack_var.get(), worm_attack_normal=worm_attack_normal_var.get(), worm_attack_shai=worm_attack_shai_var.get(), ongoing_attack=ongoing_attack_var.get(), log_active=True)
    log_window = tk.Toplevel(root)
    log_window.title(text[current_lang]['battle_log_title'])
    text_widget = tk.Text(log_window, width=100, height=30, wrap="word")
    text_widget.pack(side="left", fill="both", expand=True)
    scrollbar = ttk.Scrollbar(log_window, orient="vertical", command=text_widget.yview)
    scrollbar.pack(side="right", fill="y")
    text_widget.configure(yscrollcommand=scrollbar.set, state="normal")
    for line in battle_log:
        text_widget.insert(tk.END, line + "\n")
    text_widget.configure(state="disabled")
    text_widget.yview_moveto(0)

def switch_language():
    global current_lang
    current_lang = 'en' if current_lang == 'ru' else 'ru'
    root.title(text[current_lang]['title'])
    att_frame.config(text=text[current_lang]['attacker_frame'])
    def_frame.config(text=text[current_lang]['defender_frame'])
    attacker_normal_label.config(text=text[current_lang]['normal_units'])
    attacker_elite_label.config(text=text[current_lang]['elite_units'])
    attacker_special_elite_label.config(text=text[current_lang]['special_elite_units'])
    attacker_ornithopter_label.config(text=text[current_lang]['ornithopter_units'])
    attacker_normal_leader_label.config(text=text[current_lang]['normal_leaders'])
    attacker_cards_label.config(text=text[current_lang]['cards'])
    sudden_attack_check.config(text=text[current_lang]['sudden_attack'])
    ongoing_attack_check.config(text=text[current_lang]['ongoing_attack'])
    sardaukar_attack_check.config(text=text[current_lang]['sardaukar_attack'])
    sudden_attack_4max_check.config(text=text[current_lang]['sudden_attack_4max'])
    worm_attack_normal_check.config(text=text[current_lang]['worm_attack_normal'])
    worm_attack_shai_check.config(text=text[current_lang]['worm_attack_shai'])
    defender_settlement_label.config(text=text[current_lang]['settlement_dice'])
    att_af_leaders_label.config(text=text[current_lang]['atreides_fremen_leaders'])
    att_hc_leaders_label.config(text=text[current_lang]['harkonnen_corino_leaders'])
    def_af_leaders_label.config(text=text[current_lang]['atreides_fremen_leaders'])
    def_hc_leaders_label.config(text=text[current_lang]['harkonnen_corino_leaders'])
    attack_settlement_check.config(text=text[current_lang]['attack_on_settlement'])
    defender_normal_label.config(text=text[current_lang]['normal_units'])
    defender_elite_label.config(text=text[current_lang]['elite_units'])
    defender_special_elite_label.config(text=text[current_lang]['special_elite_units'])
    defender_ornithopter_label.config(text=text[current_lang]['ornithopter_units'])
    defender_normal_leader_label.config(text=text[current_lang]['normal_leaders'])
    defender_cards_label.config(text=text[current_lang]['cards'])
    calculate_button.config(text=text[current_lang]['calculate_battle'])
    log_button.config(text=text[current_lang]['show_battle_log'])
    lang_button.config(text="EN" if current_lang == 'ru' else "RU")

root = tk.Tk()
root.title(text[current_lang]['title'])

att_frame = ttk.LabelFrame(root, text=text[current_lang]['attacker_frame'])
def_frame = ttk.LabelFrame(root, text=text[current_lang]['defender_frame'])
att_frame.grid(row=0, column=0, padx=5, pady=5, sticky="n")
def_frame.grid(row=0, column=1, padx=5, pady=5, sticky="n")

attacker_normal_var = tk.IntVar(value=0)
attacker_elite_var = tk.IntVar(value=0)
attacker_special_elite_var = tk.IntVar(value=0)
attacker_ornithopter_var = tk.IntVar(value=0)
attacker_normal_leader_var = tk.IntVar(value=0)
attacker_cards_var = tk.IntVar(value=0)

defender_normal_var = tk.IntVar(value=0)
defender_elite_var = tk.IntVar(value=0)
defender_special_elite_var = tk.IntVar(value=0)
defender_ornithopter_var = tk.IntVar(value=0)
defender_normal_leader_var = tk.IntVar(value=0)
defender_cards_var = tk.IntVar(value=0)

defender_settlement_var = tk.IntVar(value=0)
sudden_attack_var = tk.BooleanVar(value=False)
ongoing_attack_var = tk.BooleanVar(value=False)
sardaukar_attack_var = tk.BooleanVar(value=False)
sudden_attack_4max_var = tk.BooleanVar(value=False)
worm_attack_normal_var = tk.BooleanVar(value=False)
worm_attack_shai_var = tk.BooleanVar(value=False)
settlement_var = tk.BooleanVar(value=False)

attack_modes = {
    'sudden': sudden_attack_var,
    'ongoing': ongoing_attack_var,
    'sardaukar': sardaukar_attack_var,
    'sudden_4max': sudden_attack_4max_var
}

for key, var in attack_modes.items():
    others = [v for k, v in attack_modes.items() if k != key]
    var.trace_add(
        'write',
        lambda *args, v=var, others=others: v.get() and [o.set(False) for o in others]
    )

worm_attack_normal_var.trace_add('write', lambda *args: worm_attack_shai_var.set(False) if worm_attack_normal_var.get() else None)
worm_attack_shai_var.trace_add('write', lambda *args: worm_attack_normal_var.set(False) if worm_attack_shai_var.get() else None)

attacker_normal_label = ttk.Label(att_frame, text=text[current_lang]['normal_units'])
attacker_normal_label.grid(row=0, column=0, sticky="e")
ttk.Spinbox(att_frame, from_=0, to=6, textvariable=attacker_normal_var, width=5).grid(row=0, column=1)

attacker_elite_label = ttk.Label(att_frame, text=text[current_lang]['elite_units'])
attacker_elite_label.grid(row=1, column=0, sticky="e")
ttk.Spinbox(att_frame, from_=0, to=6, textvariable=attacker_elite_var, width=5).grid(row=1, column=1)

attacker_special_elite_label = ttk.Label(att_frame, text=text[current_lang]['special_elite_units'])
attacker_special_elite_label.grid(row=2, column=0, sticky="e")
ttk.Spinbox(att_frame, from_=0, to=6, textvariable=attacker_special_elite_var, width=5).grid(row=2, column=1)

attacker_normal_leader_label = ttk.Label(att_frame, text=text[current_lang]['normal_leaders'])
attacker_normal_leader_label.grid(row=3, column=0, sticky="e")
ttk.Spinbox(att_frame, from_=0, to=10, textvariable=attacker_normal_leader_var, width=5).grid(row=3, column=1)

attacker_ornithopter_label = ttk.Label(att_frame, text=text[current_lang]['ornithopter_units'])
attacker_ornithopter_label.grid(row=4, column=0, sticky="e")
ttk.Spinbox(att_frame, from_=0, to=2, textvariable=attacker_ornithopter_var, width=5).grid(row=4, column=1)

attacker_cards_label = ttk.Label(att_frame, text=text[current_lang]['cards'])
attacker_cards_label.grid(row=5, column=0, sticky="e")
ttk.Spinbox(att_frame, from_=0, to=10, textvariable=attacker_cards_var, width=5).grid(row=5, column=1)

sudden_attack_check = ttk.Checkbutton(att_frame, text=text[current_lang]['sudden_attack'], variable=sudden_attack_var)
sudden_attack_check.grid(row=6, column=0, columnspan=2, padx=0, pady=0, sticky="w")

sudden_attack_4max_check = ttk.Checkbutton(att_frame, text=text[current_lang]['sudden_attack_4max'], variable=sudden_attack_4max_var)
sudden_attack_4max_check.grid(row=7, column=0, columnspan=2, padx=0, pady=0, sticky="w")

ongoing_attack_check = ttk.Checkbutton(att_frame, text=text[current_lang]['ongoing_attack'], variable=ongoing_attack_var)
ongoing_attack_check.grid(row=8, column=0, sticky="w", padx=0, pady=0)

sardaukar_attack_check = ttk.Checkbutton(att_frame, text=text[current_lang]['sardaukar_attack'], variable=sardaukar_attack_var)
sardaukar_attack_check.grid(row=9, column=0, columnspan=2, padx=0, pady=0, sticky="w")

worm_attack_normal_check = ttk.Checkbutton(att_frame, text=text[current_lang]['worm_attack_normal'], variable=worm_attack_normal_var)
worm_attack_normal_check.grid(row=10, column=0, columnspan=2, padx=0, pady=0, sticky="w")

worm_attack_shai_check = ttk.Checkbutton(att_frame, text=text[current_lang]['worm_attack_shai'], variable=worm_attack_shai_var)
worm_attack_shai_check.grid(row=11, column=0, columnspan=2, padx=0, pady=0, sticky="w")

defender_normal_label = ttk.Label(def_frame, text=text[current_lang]['normal_units'])
defender_normal_label.grid(row=0, column=0, sticky="e")
ttk.Spinbox(def_frame, from_=0, to=6, textvariable=defender_normal_var, width=5).grid(row=0, column=1)

defender_elite_label = ttk.Label(def_frame, text=text[current_lang]['elite_units'])
defender_elite_label.grid(row=1, column=0, sticky="e")
ttk.Spinbox(def_frame, from_=0, to=6, textvariable=defender_elite_var, width=5).grid(row=1, column=1)

defender_special_elite_label = ttk.Label(def_frame, text=text[current_lang]['special_elite_units'])
defender_special_elite_label.grid(row=2, column=0, sticky="e")
ttk.Spinbox(def_frame, from_=0, to=6, textvariable=defender_special_elite_var, width=5).grid(row=2, column=1)

defender_normal_leader_label = ttk.Label(def_frame, text=text[current_lang]['normal_leaders'])
defender_normal_leader_label.grid(row=3, column=0, sticky="e")
ttk.Spinbox(def_frame, from_=0, to=10, textvariable=defender_normal_leader_var, width=5).grid(row=3, column=1)

defender_ornithopter_label = ttk.Label(def_frame, text=text[current_lang]['ornithopter_units'])
defender_ornithopter_label.grid(row=4, column=0, sticky="e")
ttk.Spinbox(def_frame, from_=0, to=3, textvariable=defender_ornithopter_var, width=5).grid(row=4, column=1)

defender_cards_label = ttk.Label(def_frame, text=text[current_lang]['cards'])
defender_cards_label.grid(row=5, column=0, sticky="e")
ttk.Spinbox(def_frame, from_=0, to=10, textvariable=defender_cards_var, width=5).grid(row=5, column=1)

defender_settlement_label = ttk.Label(def_frame, text=text[current_lang]['settlement_dice'])
defender_settlement_label.grid(row=6, column=0, sticky="e")
ttk.Spinbox(def_frame, from_=0, to=3, textvariable=defender_settlement_var, width=5).grid(row=6, column=1)

att_special_vars = {name: tk.BooleanVar(value=False) for name in special_leaders_data.keys()}
row_index = 12
att_af_leaders_label = ttk.Label(att_frame, text=text[current_lang]['atreides_fremen_leaders'])
att_af_leaders_label.grid(row=row_index, column=0, columnspan=2, sticky="w", pady=(5, 0))
row_index += 1
for name in ["Paul Atreides", "Paul Muad'Dib", "Lady Jessica", "Mother Jessica", "Gurney Halleck", "Alia", "Stilgar", "Chani", "Stabban Tuek"]:
    ttk.Checkbutton(att_frame, text=name, variable=att_special_vars[name]).grid(row=row_index, column=0, columnspan=2, sticky="w")
    row_index += 1
att_hc_leaders_label = ttk.Label(att_frame, text=text[current_lang]['harkonnen_corino_leaders'])
att_hc_leaders_label.grid(row=row_index, column=0, columnspan=2, sticky="w", pady=(5, 0))
row_index += 1
for name in ["Baron Harkonnen", "Beast Rabban", "Feyd-Rautha", "Thufir Hawat", "Shaddam IV", "G.H. Mohiam", "Captain Aramsham"]:
    ttk.Checkbutton(att_frame, text=name, variable=att_special_vars[name]).grid(row=row_index, column=0, columnspan=2, sticky="w")
    row_index += 1

def_special_vars = {name: tk.BooleanVar(value=False) for name in special_leaders_data.keys()}
row_index = 7
def_af_leaders_label = ttk.Label(def_frame, text=text[current_lang]['atreides_fremen_leaders'])
def_af_leaders_label.grid(row=row_index, column=0, columnspan=2, sticky="w", pady=(15, 0))
row_index += 1
for name in ["Paul Atreides", "Paul Muad'Dib", "Lady Jessica", "Mother Jessica", "Gurney Halleck", "Alia", "Stilgar", "Chani", "Stabban Tuek"]:
    ttk.Checkbutton(def_frame, text=name, variable=def_special_vars[name]).grid(row=row_index, column=0, columnspan=2, sticky="w")
    row_index += 1
def_hc_leaders_label = ttk.Label(def_frame, text=text[current_lang]['harkonnen_corino_leaders'])
def_hc_leaders_label.grid(row=row_index, column=0, columnspan=2, sticky="w", pady=(5, 0))
row_index += 1
for name in ["Baron Harkonnen", "Beast Rabban", "Feyd-Rautha", "Thufir Hawat", "Shaddam IV", "G.H. Mohiam", "Captain Aramsham"]:
    ttk.Checkbutton(def_frame, text=name, variable=def_special_vars[name]).grid(row=row_index, column=0, columnspan=2, sticky="w")
    row_index += 1

attack_settlement_check = ttk.Checkbutton(root, text=text[current_lang]['attack_on_settlement'], variable=settlement_var)
attack_settlement_check.grid(row=1, column=0, columnspan=2, pady=5)

output_text = tk.Text(root, width=100, height=30, wrap="word")
output_text.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
scrollbar = ttk.Scrollbar(root, orient="vertical", command=output_text.yview)
scrollbar.grid(row=3, column=3, sticky="ns")
output_text.configure(yscrollcommand=scrollbar.set, state="disabled")

calculate_button = ttk.Button(root, text=text[current_lang]['calculate_battle'], command=run_calculation)
calculate_button.grid(row=2, column=0, padx=5, pady=5)
log_button = ttk.Button(root, text=text[current_lang]['show_battle_log'], command=show_log)
log_button.grid(row=2, column=1, padx=5, pady=5)
lang_button = ttk.Button(root, text="EN" if current_lang == 'ru' else "RU", command=switch_language)
lang_button.grid(row=2, column=2, padx=5, pady=5)

root.mainloop()
