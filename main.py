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
        'normal_leaders': "Обычные лидеры:",
        'cards': "Карты (доп. кубики):",
        'sudden_attack': "Внезапная атака",
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
        'assault_damage': "Атакующий наносит урон за штурм"
    },
    'en': {
        'title': "Dune: War for Arrakis - Battle Calculator",
        'attacker_frame': "Attacker",
        'defender_frame': "Defender",
        'normal_units': "Normal units:",
        'elite_units': "Elite units:",
        'special_elite_units': "Special elite units:",
        'normal_leaders': "Normal leaders:",
        'cards': "Cards (extra dice):",
        'sudden_attack': "Sudden Attack",
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
        'assault_damage': "Attacker suffers assault damage"
    }
}

current_lang = 'ru'

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
    if len(forms) == 3:
        # Русские правила склонения
        if num % 10 == 1 and num % 100 != 11:
            return f"{num} {forms[0]}"
        elif 2 <= num % 10 <= 4 and not (12 <= num % 100 <= 14):
            return f"{num} {forms[1]}"
        else:
            return f"{num} {forms[2]}"
    elif len(forms) == 2:
        # Правила для английского (единственное/множественное)
        return f"{num} {forms[0]}" if num == 1 else f"{num} {forms[1]}"
    else:
        # Непредвиденное количество форм - возвращаем число и первую форму как есть
        return f"{num} {forms[0]}"

def allocate_casualties(side_name, casualties, state, log_active=True):
    log = []
    while casualties > 0:
        # Понизить элитный отряд до обычного
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
        # Удалить обычного (безымянного) лидера
        if casualties > 0 and state['normal_leader'] > 0:
            state['normal_leader'] -= 1
            casualties -= 1
            if log_active:
                if current_lang == 'ru':
                    log.append(f"{side_name}: обычный лидер убит.")
                else:
                    log.append(f"{side_name}: normal leader killed.")
            continue
        # Удалить особого лидера, если их больше двух (удаляется самый слабый)
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
        # Понизить особый элитный отряд до обычного
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
        # Удалить обычные отряды, пока их не останется 4
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
        # Удалить любого оставшегося особого лидера (если остались)
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
        # Удалить оставшиеся обычные отряды
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

def simulate_battle(att, deff, settlement=False, sudden_attack=False, log_active=True):
    att_state = copy.deepcopy(att)
    def_state = copy.deepcopy(deff)
    log = []
    # Обработка внезапной атаки (логируем сразу, эффект применим в первом раунде)
    if sudden_attack and log_active:
        if current_lang == 'ru':
            log.append("Внезапная атака: атакующий получает +1 особый символ (звезда) в этом раунде.")
        else:
            log.append("Sudden attack: attacker gains +1 special symbol (star) this round.")
    round_num = 1
    # Боевые раунды
    while True:
        # Проверка наличия войск с обеих сторон
        att_units_count = att_state['normal'] + att_state['elite'] + att_state['special_elite']
        def_units_count = def_state['normal'] + def_state['elite'] + def_state['special_elite']
        if att_units_count == 0 or def_units_count == 0:
            break  # бой завершается, если у одной из сторон не осталось отрядов
        # Определение количества кубиков к броску (включая карты и поселение)
        att_cards_left = att_state.get('cards_left', att_state.get('cards', 0))
        def_cards_left = def_state.get('cards_left', def_state.get('cards', 0))
        att_cards_this_round = min(att_cards_left, max(0, 6 - att_units_count))
        def_cards_this_round = min(def_cards_left, max(0, 6 - def_units_count))
        attacker_dice = min(6, att_units_count + att_cards_this_round)
        defender_dice = min(6, def_units_count + def_cards_this_round + def_state.get('settlement', 0))
        # Обновляем оставшиеся карты
        att_state['cards_left'] = att_cards_left - att_cards_this_round
        def_state['cards_left'] = def_cards_left - def_cards_this_round
        # Броски кубиков атакующего
        a_swords = a_shields = a_stars = 0
        for _ in range(attacker_dice):
            roll = random.randint(1, 6)
            if roll <= 3:
                a_swords += 1
            elif roll <= 5:
                a_shields += 1
            else:
                a_stars += 1
        # Броски кубиков защитника
        d_swords = d_shields = d_stars = 0
        for _ in range(defender_dice):
            roll = random.randint(1, 6)
            if roll <= 3:
                d_swords += 1
            elif roll <= 5:
                d_shields += 1
            else:
                d_stars += 1
        # Применение эффекта внезапной атаки в первом раунде (+1 особый символ атакующему)
        if sudden_attack and round_num == 1:
            a_stars += 1
        # Общее количество лидеров у каждой стороны (для использования особых символов)
        total_att_leaders = att_state['normal_leader'] + len(att_state['special_leaders'])
        total_def_leaders = def_state['normal_leader'] + len(def_state['special_leaders'])
        att_extra_swords = att_extra_shields = 0
        def_extra_swords = def_extra_shields = 0
        att_used = []
        def_used = []
        # Использование особых символов атакующим лидерами
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
        # Использование особых символов защитником лидерами
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
        # Суммарные мечи и щиты после учета лидерских способностей
        total_a_swords = a_swords + att_extra_swords
        total_a_shields = a_shields + att_extra_shields
        total_d_swords = d_swords + def_extra_swords
        total_d_shields = d_shields + def_extra_shields
        # Особые элитные отряды отменяют выпавшие у противника щиты
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
        # Подсчет попаданий (мечи минус щиты противника)
        hits_on_def = total_a_swords - total_d_shields  # попаданий по защитнику
        hits_on_att = total_d_swords - total_a_shields  # попаданий по атакующему
        # Штраф атакующему за бой на поселении: +1 попадание (если защитник еще имеет силы)
        def_units_after = def_state['normal'] + def_state['elite'] + def_state['special_elite']
        if settlement and def_units_after > 0:
            penalty = 1
            penalty_log = allocate_casualties(text[current_lang]['assault_damage'], penalty, att_state, log_active=log_active)
            if log_active:
                log.extend(penalty_log)
        # Логирование результатов раунда
        if log_active:
            # Броски атакующего
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
            # Броски защитника
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
            # Использование особых символов атакующей стороной (детализация)
            if att_used:
                unnamed_count = sum(1 for x in att_used if x[0] == "Unnamed")
                parts = []
                if unnamed_count > 0:
                    if current_lang == 'ru':
                        leader_str = format_count(unnamed_count, ("безымянный лидер", "безымянных лидера", "безымянных лидеров"))
                        verb = "добавил" if unnamed_count == 1 else "добавили"
                        sword_str_u = format_count(unnamed_count, ("меч", "меча", "мечей"))
                        parts.append(f"{leader_str} {verb} {sword_str_u}")
                    else:
                        parts.append(f"{unnamed_count} unnamed leader{'s' if unnamed_count != 1 else ''} added {unnamed_count} sword{'s' if unnamed_count != 1 else ''}")
                for (name, sw, sh) in att_used:
                    if name == "Unnamed":
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
            # Использование особых символов защищающейся стороной (детализация)
            if def_used:
                unnamed_count = sum(1 for x in def_used if x[0] == "Unnamed")
                parts = []
                if unnamed_count > 0:
                    if current_lang == 'ru':
                        leader_str = format_count(unnamed_count, ("безымянный лидер", "безымянных лидера", "безымянных лидеров"))
                        verb = "добавил" if unnamed_count == 1 else "добавили"
                        sword_str_u = format_count(unnamed_count, ("меч", "меча", "мечей"))
                        parts.append(f"{leader_str} {verb} {sword_str_u}")
                    else:
                        parts.append(f"{unnamed_count} unnamed leader{'s' if unnamed_count != 1 else ''} added {unnamed_count} sword{'s' if unnamed_count != 1 else ''}")
                for (name, sw, sh) in def_used:
                    if name == "Unnamed":
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
            # Сводка по способностям и урону
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
        # Применение попаданий (урона) к отрядам
        if hits_on_def > 0:
            def_casualty_log = allocate_casualties(text[current_lang]['defender_frame'], hits_on_def, def_state, log_active=log_active)
            if log_active:
                log.extend(def_casualty_log)
        if hits_on_att > 0:
            att_casualty_log = allocate_casualties(text[current_lang]['attacker_frame'], hits_on_att, att_state, log_active=log_active)
            if log_active:
                log.extend(att_casualty_log)
        # Проверка оставшихся сил для продолжения боя
        att_units_alive = att_state['normal'] + att_state['elite'] + att_state['special_elite']
        def_units_alive = def_state['normal'] + def_state['elite'] + def_state['special_elite']
        if att_units_alive == 0 or def_units_alive == 0:
            break  # бой завершается, если одна сторона полностью уничтожена
        round_num += 1
    # Результаты боя после завершения всех раундов
    att_units = att_state['normal'] + att_state['elite'] + att_state['special_elite']
    def_units = def_state['normal'] + def_state['elite'] + def_state['special_elite']
    # Определение самого сильного лидера каждой стороны
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
    # Выжил ли самый сильный лидер у каждой стороны
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
    # Финальный исход боя
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
    """Обработчик кнопки 'Рассчитать бой'."""
    global current_lang
    # Считать значения полей ввода для обеих сторон
    att_state = {
        "normal": attacker_normal_var.get(),
        "elite": attacker_elite_var.get(),
        "special_elite": attacker_special_elite_var.get(),
        "normal_leader": attacker_normal_leader_var.get(),
        "special_leaders": [name for name, var in att_special_vars.items() if var.get()],
        "cards": attacker_cards_var.get(),
        "cards_left": attacker_cards_var.get(),
        "sudden_attack": sudden_attack_var.get()
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
    # Проверка ограничения: не более 6 отрядов у каждой стороны
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
    # Проведение 1000 симуляций боя для оценки вероятностей и статистики
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
            att_state, def_state, settlement=settlement_var.get(), sudden_attack=sudden_attack_var.get(), log_active=False
        )
        if outcome == "Attacker wins":
            attacker_wins += 1
        elif outcome == "Defender wins":
            defender_wins += 1
        # Накопление данных о выживших отрядах и выживших лидерах
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
    # Вывод результатов в текстовое поле
    output_text.configure(state="normal")
    output_text.delete("1.0", tk.END)
    # Вероятности побед и ничьей
    draws = simulations - attacker_wins - defender_wins
    attacker_pct = attacker_wins / simulations * 100
    defender_pct = defender_wins / simulations * 100
    draw_pct = draws / simulations * 100
    output_text.insert(tk.END, f"\n{text[current_lang]['attacker_win_chance']}: {attacker_pct:.1f}% | {text[current_lang]['defender_win_chance']}: {defender_pct:.1f}% | {text[current_lang]['draw']}: {draw_pct:.1f}% ({text[current_lang]['simulations']}: {simulations})")
    # Среднее количество выживших отрядов
    avg_att_survivors = attacker_survivors_total / simulations
    avg_def_survivors = defender_survivors_total / simulations
    output_text.insert(tk.END, f"\n{text[current_lang]['average_surviving']} {text[current_lang]['attacker_role']}: {avg_att_survivors:.1f}, {text[current_lang]['defender_role']}: {avg_def_survivors:.1f}")
    # Шанс выживания самого сильного лидера (если таковой был)
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
    # Считать значения полей ввода
    att_state = {
        "normal": attacker_normal_var.get(),
        "elite": attacker_elite_var.get(),
        "special_elite": attacker_special_elite_var.get(),
        "normal_leader": attacker_normal_leader_var.get(),
        "special_leaders": [name for name, var in att_special_vars.items() if var.get()],
        "sudden_attack": sudden_attack_var.get(),
        "cards": attacker_cards_var.get(),
        "cards_left": attacker_cards_var.get()
    }
    def_state = {
        "normal": defender_normal_var.get(),
        "elite": defender_elite_var.get(),
        "special_elite": defender_special_elite_var.get(),
        "normal_leader": defender_normal_leader_var.get(),
        "special_leaders": [name for name, var in def_special_vars.items() if var.get()],
        "cards": defender_cards_var.get(),
        "settlement": defender_settlement_var.get(),
        "cards_left": defender_cards_var.get()
    }
    # Проверка ограничения по отрядам
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
    # Получение детального лога одного боя
    battle_log = simulate_battle(att_state, def_state, settlement=settlement_var.get(), sudden_attack=sudden_attack_var.get(), log_active=True)
    # Отображение лога боя в новом окне
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
    # Переключаем язык
    current_lang = 'en' if current_lang == 'ru' else 'ru'
    # Обновляем тексты всех видимых элементов интерфейса
    root.title(text[current_lang]['title'])
    att_frame.config(text=text[current_lang]['attacker_frame'])
    def_frame.config(text=text[current_lang]['defender_frame'])
    attacker_normal_label.config(text=text[current_lang]['normal_units'])
    attacker_elite_label.config(text=text[current_lang]['elite_units'])
    attacker_special_elite_label.config(text=text[current_lang]['special_elite_units'])
    attacker_normal_leader_label.config(text=text[current_lang]['normal_leaders'])
    attacker_cards_label.config(text=text[current_lang]['cards'])
    sudden_attack_check.config(text=text[current_lang]['sudden_attack'])
    defender_settlement_label.config(text=text[current_lang]['settlement_dice'])
    att_af_leaders_label.config(text=text[current_lang]['atreides_fremen_leaders'])
    att_hc_leaders_label.config(text=text[current_lang]['harkonnen_corino_leaders'])
    def_af_leaders_label.config(text=text[current_lang]['atreides_fremen_leaders'])
    def_hc_leaders_label.config(text=text[current_lang]['harkonnen_corino_leaders'])
    attack_settlement_check.config(text=text[current_lang]['attack_on_settlement'])
    defender_normal_label.config(text=text[current_lang]['normal_units'])
    defender_elite_label.config(text=text[current_lang]['elite_units'])
    defender_special_elite_label.config(text=text[current_lang]['special_elite_units'])
    defender_normal_leader_label.config(text=text[current_lang]['normal_leaders'])
    defender_cards_label.config(text=text[current_lang]['cards'])
    calculate_button.config(text=text[current_lang]['calculate_battle'])
    log_button.config(text=text[current_lang]['show_battle_log'])
    # Кнопка переключения языка показывает целевой язык (EN или RU)
    lang_button.config(text="EN" if current_lang == 'ru' else "RU")

# Создание главного окна
root = tk.Tk()
root.title(text[current_lang]['title'])

# Рамки для ввода данных атакующей и защищающейся стороны
att_frame = ttk.LabelFrame(root, text=text[current_lang]['attacker_frame'])
def_frame = ttk.LabelFrame(root, text=text[current_lang]['defender_frame'])
att_frame.grid(row=0, column=0, padx=5, pady=5, sticky="n")
def_frame.grid(row=0, column=1, padx=5, pady=5, sticky="n")

# Переменные для входных данных атакующего
attacker_normal_var = tk.IntVar(value=0)
attacker_elite_var = tk.IntVar(value=0)
attacker_special_elite_var = tk.IntVar(value=0)
attacker_normal_leader_var = tk.IntVar(value=0)
attacker_cards_var = tk.IntVar(value=0)
# Переменные для входных данных защитника
defender_normal_var = tk.IntVar(value=0)
defender_elite_var = tk.IntVar(value=0)
defender_special_elite_var = tk.IntVar(value=0)
defender_normal_leader_var = tk.IntVar(value=0)
defender_cards_var = tk.IntVar(value=0)
# Прочие флажки и переменные
defender_settlement_var = tk.IntVar(value=0)    # кубы поселения у защитника
sudden_attack_var = tk.BooleanVar(value=False)  # внезапная атака
settlement_var = tk.BooleanVar(value=False)     # атака на поселение (штраф для атакующего)

# Ограничение: у защитника суммарно <= 6 отрядов (следим за спинбоксами)
def update_defender_count(var, others):
    total = var.get() + sum(v.get() for v in others)
    if total > 6:
        var.set(max(0, 6 - sum(v.get() for v in others)))
        messagebox.showerror(text[current_lang]['error_title'], text[current_lang]['units_limit_error'])

defender_normal_var.trace_add('write', lambda *args: update_defender_count(defender_normal_var, [defender_elite_var, defender_special_elite_var]))
defender_elite_var.trace_add('write', lambda *args: update_defender_count(defender_elite_var, [defender_normal_var, defender_special_elite_var]))
defender_special_elite_var.trace_add('write', lambda *args: update_defender_count(defender_special_elite_var, [defender_normal_var, defender_elite_var]))

# Поля ввода для атакующей стороны
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
attacker_cards_label = ttk.Label(att_frame, text=text[current_lang]['cards'])
attacker_cards_label.grid(row=4, column=0, sticky="e")
ttk.Spinbox(att_frame, from_=0, to=10, textvariable=attacker_cards_var, width=5).grid(row=4, column=1)
sudden_attack_check = ttk.Checkbutton(att_frame, text=text[current_lang]['sudden_attack'], variable=sudden_attack_var)
sudden_attack_check.grid(row=5, column=0, padx=0, pady=5, sticky="w")

# Поля ввода для защищающейся стороны
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
defender_cards_label = ttk.Label(def_frame, text=text[current_lang]['cards'])
defender_cards_label.grid(row=4, column=0, sticky="e")
ttk.Spinbox(def_frame, from_=0, to=10, textvariable=defender_cards_var, width=5).grid(row=4, column=1)
defender_settlement_label = ttk.Label(def_frame, text=text[current_lang]['settlement_dice'])
defender_settlement_label.grid(row=5, column=0, sticky="e")
ttk.Spinbox(def_frame, from_=0, to=3, textvariable=defender_settlement_var, width=5).grid(row=5, column=1)

# Флажки выбора особых лидеров для атакующего
att_special_vars = {name: tk.BooleanVar(value=False) for name in special_leaders_data.keys()}
row_index = 6
att_af_leaders_label = ttk.Label(att_frame, text=text[current_lang]['atreides_fremen_leaders'])
att_af_leaders_label.grid(row=row_index, column=0, columnspan=2, sticky="w", pady=(5, 0))
row_index += 1
for name in ["Paul Atreides", "Paul Muad'Dib", "Lady Jessica", "Mother Jessica", "Gurney Halleck", "Alia", "Stilgar", "Chani"]:
    ttk.Checkbutton(att_frame, text=name, variable=att_special_vars[name]).grid(row=row_index, column=0, columnspan=2, sticky="w")
    row_index += 1
att_hc_leaders_label = ttk.Label(att_frame, text=text[current_lang]['harkonnen_corino_leaders'])
att_hc_leaders_label.grid(row=row_index, column=0, columnspan=2, sticky="w", pady=(5, 0))
row_index += 1
for name in ["Baron Harkonnen", "Beast Rabban", "Feyd-Rautha", "Thufir Hawat", "Shaddam IV", "G.H. Mohiam", "Captain Aramsham"]:
    ttk.Checkbutton(att_frame, text=name, variable=att_special_vars[name]).grid(row=row_index, column=0, columnspan=2, sticky="w")
    row_index += 1

# Флажки выбора особых лидеров для защитника
def_special_vars = {name: tk.BooleanVar(value=False) for name in special_leaders_data.keys()}
row_index = 6
def_af_leaders_label = ttk.Label(def_frame, text=text[current_lang]['atreides_fremen_leaders'])
def_af_leaders_label.grid(row=6, column=0, columnspan=2, sticky="w", pady=(15, 0))
row_index += 1
for name in ["Paul Atreides", "Paul Muad'Dib", "Lady Jessica", "Mother Jessica", "Gurney Halleck", "Alia", "Stilgar", "Chani"]:
    ttk.Checkbutton(def_frame, text=name, variable=def_special_vars[name]).grid(row=row_index, column=0, columnspan=2, sticky="w")
    row_index += 1
def_hc_leaders_label = ttk.Label(def_frame, text=text[current_lang]['harkonnen_corino_leaders'])
def_hc_leaders_label.grid(row=row_index, column=0, columnspan=2, sticky="w", pady=(5, 0))
row_index += 1
for name in ["Baron Harkonnen", "Beast Rabban", "Feyd-Rautha", "Thufir Hawat", "Shaddam IV", "G.H. Mohiam", "Captain Aramsham"]:
    ttk.Checkbutton(def_frame, text=name, variable=def_special_vars[name]).grid(row=row_index, column=0, columnspan=2, sticky="w")
    row_index += 1

# Флажок "Атака на поселение"
attack_settlement_check = ttk.Checkbutton(root, text=text[current_lang]['attack_on_settlement'], variable=settlement_var)
attack_settlement_check.grid(row=1, column=0, columnspan=2, pady=5)

# Текстовое поле для вывода результатов/лога боя и полоса прокрутки
output_text = tk.Text(root, width=100, height=30, wrap="word")
output_text.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
scrollbar = ttk.Scrollbar(root, orient="vertical", command=output_text.yview)
scrollbar.grid(row=3, column=3, sticky="ns")
output_text.configure(yscrollcommand=scrollbar.set, state="disabled")

# Кнопки управления
calculate_button = ttk.Button(root, text=text[current_lang]['calculate_battle'], command=run_calculation)
calculate_button.grid(row=2, column=0, padx=5, pady=5)
log_button = ttk.Button(root, text=text[current_lang]['show_battle_log'], command=show_log)
log_button.grid(row=2, column=1, padx=5, pady=5)
lang_button = ttk.Button(root, text="EN" if current_lang == 'ru' else "RU", command=switch_language)
lang_button.grid(row=2, column=2, padx=5, pady=5)

# Запуск основного цикла приложения (Tkinter)
root.mainloop()
