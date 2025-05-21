import random
import copy
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Данные специальных лидеров: сколько мечей и щитов даёт каждый лидер при использовании символа "особый"
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

# Функция для форматирования числительных (мечей, щитов, символов) с правильным окончанием
def format_count(num, forms):
    # forms: (единственное, родит. ед., родит. мн.)
    if num % 10 == 1 and num % 100 != 11:
        return f"{num} {forms[0]}"
    elif 2 <= num % 10 <= 4 and not (12 <= num % 100 <= 14):
        return f"{num} {forms[1]}"
    else:
        return f"{num} {forms[2]}"

# Применение урона к армии с учётом приоритетов
def allocate_casualties(side_name, casualties, state, log_active=True):
    log = []
    while casualties > 0:
        # Понизить элитный отряд до обычного
        if casualties > 0 and state['elite'] > 0:
            state['elite'] -= 1
            state['normal'] += 1
            casualties -= 1
            if log_active:
                log.append(f"{side_name}: элитный отряд понижен до обычного.")
            continue
        # Убрать обычного (безымянного) лидера
        if casualties > 0 and state['normal_leader'] > 0:
            state['normal_leader'] -= 1
            casualties -= 1
            if log_active:
                log.append(f"{side_name}: обычный лидер убит.")
            continue
        # Убрать особого лидера, если их больше двух (удаляем самого слабого)
        if casualties > 0 and len(state['special_leaders']) > 2:
            weakest = min(state['special_leaders'], key=lambda name: special_leaders_data[name]['swords'] + special_leaders_data[name]['shields'])
            state['special_leaders'].remove(weakest)
            casualties -= 1
            if log_active:
                log.append(f"{side_name}: особый лидер {weakest} убит.")
            continue
        # Понизить особый элитный отряд до обычного
        if casualties > 0 and state['special_elite'] > 0:
            state['special_elite'] -= 1
            state['normal'] += 1
            casualties -= 1
            if log_active:
                log.append(f"{side_name}: особый элитный отряд понижен до обычного.")
            continue
        # Убрать обычные отряды, пока не останется 4
        if casualties > 0 and state['normal'] > 4:
            to_kill = min(casualties, state['normal'] - 4)
            state['normal'] -= to_kill
            casualties -= to_kill
            if log_active and to_kill > 0:
                if to_kill == 1:
                    log.append(f"{side_name}: 1 обычный отряд уничтожен.")
                else:
                    log.append(f"{side_name}: {to_kill} обычных отрядов уничтожено.")
            continue
        # Убрать оставшегося особого лидера (если есть)
        if casualties > 0 and len(state['special_leaders']) > 0:
            weakest = min(state['special_leaders'], key=lambda name: special_leaders_data[name]['swords'] + special_leaders_data[name]['shields'])
            state['special_leaders'].remove(weakest)
            casualties -= 1
            if log_active:
                log.append(f"{side_name}: особый лидер {weakest} убит.")
            continue
        # Убрать оставшиеся обычные отряды
        if casualties > 0 and state['normal'] > 0:
            if casualties >= state['normal']:
                num = state['normal']
                state['normal'] = 0
                casualties -= num
                if log_active:
                    if num == 1:
                        log.append(f"{side_name}: 1 обычный отряд уничтожен.")
                    else:
                        log.append(f"{side_name}: {num} обычных отрядов уничтожено.")
            else:
                num = casualties
                state['normal'] -= num
                casualties = 0
                if log_active:
                    if num == 1:
                        log.append(f"{side_name}: 1 обычный отряд уничтожен.")
                    else:
                        log.append(f"{side_name}: {num} обычных отрядов уничтожено.")
            continue
        break
    return log

# Симуляция боя между двумя армиями
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

        # Внезапная атака: +1 звезда в первом раунде
        if round_num == 1 and sudden_attack:
            a_stars += 1
            if log_active:
                log.append("Внезапная атака: атакующий получает +1 особый символ (звезда) в этом раунде.")

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
        # Применение выпавших "особых" символов атакующим (лидерами)
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
        # Применение "особых" символов защитником
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
        # Суммарные мечи и щиты после учета лидеров
        total_a_swords = a_swords + att_extra_swords
        total_a_shields = a_shields + att_extra_shields
        total_d_swords = d_swords + def_extra_swords
        total_d_shields = d_shields + def_extra_shields
        # Особые элитные отряды отменяют результаты щитов противника
        if att_state['special_elite'] > 0:
            cancel = min(total_d_shields, att_state['special_elite'])
            total_d_shields -= cancel
            if log_active and cancel > 0:
                log.append(f"Особые элитные атакующего отменяют {cancel} результат(ов) щита у защитника.")
        if def_state['special_elite'] > 0:
            cancel = min(total_a_shields, def_state['special_elite'])
            total_a_shields -= cancel
            if log_active and cancel > 0:
                log.append(f"Особые элитные защитника отменяют {cancel} результат(ов) щита у атакующего.")
        # Подсчет попаданий (мечи минус щиты противника)
        hits_on_def = total_a_swords - total_d_shields
        hits_on_att = total_d_swords - total_a_shields
        if hits_on_def < 0: hits_on_def = 0
        if hits_on_att < 0: hits_on_att = 0

        # Логирование результатов раунда
        if log_active:
            sword_str = format_count(a_swords, ("меч", "меча", "мечей"))
            shield_str = format_count(a_shields, ("щит", "щита", "щитов"))
            special_str = format_count(a_stars, ("особый символ", "особых символа", "особых символов"))
            log.append(f"Раунд {round_num}: атакующий бросил {attacker_dice} кубиков -> {sword_str}, {shield_str}, {special_str}.")
            sword_str = format_count(d_swords, ("меч", "меча", "мечей"))
            shield_str = format_count(d_shields, ("щит", "щита", "щитов"))
            special_str = format_count(d_stars, ("особый символ", "особых символа", "особых символов"))
            log.append(f"Раунд {round_num}: защитник бросил {defender_dice} кубиков -> {sword_str}, {shield_str}, {special_str}.")
            if att_used:
                # Детализация использования лидеров атакующего
                unnamed_count = sum(1 for x in att_used if x[0] == "Unnamed")
                parts = []
                if unnamed_count > 0:
                    parts.append(f"{unnamed_count} безымянн(ых) лидер(ов) добавил(и) {unnamed_count} меч")
                for (name, sw, sh) in att_used:
                    if name == "Unnamed": continue
                    subparts = []
                    if sw: subparts.append(format_count(sw, ("меч", "меча", "мечей")))
                    if sh: subparts.append(format_count(sh, ("щит", "щита", "щитов")))
                    contribution = " и ".join(subparts)
                    parts.append(f"{name} добавил {contribution}")
                log.append("Атакующий использует особые символы: " + "; ".join(parts) + ".")
            else:
                if a_stars > 0 and total_att_leaders == 0:
                    log.append("Атакующий выбросил особые символы, но некому их использовать.")
            if def_used:
                unnamed_count = sum(1 for x in def_used if x[0] == "Unnamed")
                parts = []
                if unnamed_count > 0:
                    parts.append(f"{unnamed_count} безымянн(ых) лидер(ов) добавил(и) {unnamed_count} меч")
                for (name, sw, sh) in def_used:
                    if name == "Unnamed": continue
                    subparts = []
                    if sw: subparts.append(format_count(sw, ("меч", "меча", "мечей")))
                    if sh: subparts.append(format_count(sh, ("щит", "щита", "щитов")))
                    contribution = " и ".join(subparts)
                    parts.append(f"{name} добавил {contribution}")
                log.append("Защитник использует особые символы: " + "; ".join(parts) + ".")
            else:
                if d_stars > 0 and total_def_leaders == 0:
                    log.append("Защитник выбросил особые символы, но некому их использовать.")
            sword_str_a = format_count(total_a_swords, ("меч", "меча", "мечей"))
            shield_str_a = format_count(total_a_shields, ("щит", "щита", "щитов"))
            sword_str_d = format_count(total_d_swords, ("меч", "меча", "мечей"))
            shield_str_d = format_count(total_d_shields, ("щит", "щита", "щитов"))
            log.append(f"Итого после способностей: у атакующего {sword_str_a}, {shield_str_a}; у защитника {sword_str_d}, {shield_str_d}.")
            log.append(f"Нанесённый урон: атакующий получил {hits_on_att} попаданий, защитник получил {hits_on_def} попаданий.")
        # Применяем попадания (урон) к отрядам
        if hits_on_def > 0:
            def_casualty_log = allocate_casualties("Защитник", hits_on_def, def_state, log_active=log_active)
            if log_active: log.extend(def_casualty_log)
        if hits_on_att > 0:
            att_casualty_log = allocate_casualties("Атакующий", hits_on_att, att_state, log_active=log_active)
            if log_active: log.extend(att_casualty_log)

        # Проверяем - жив ли ещё кто-то у защитника
        def_units_after = def_state['normal'] + def_state['elite'] + def_state['special_elite']

        # Штраф атакующему за бой на поселении: +1 попадание
        if settlement and def_units_after > 0:
            penalty = 1
            penalty_log = allocate_casualties("Атакующий наносит урон за штурм", penalty, att_state,
                                              log_active=log_active)
            if log_active:
                log.extend(penalty_log)

        # Логирование состояния после раунда
        if log_active:
            att_special_leaders = ", ".join(att_state['special_leaders']) if att_state['special_leaders'] else "нет"
            def_special_leaders = ", ".join(def_state['special_leaders']) if def_state['special_leaders'] else "нет"
            log.append(f"Конец раунда {round_num}: атакующий - обычных отрядов: {att_state['normal']}, элитных: {att_state['elite']}, особых элитных: {att_state['special_elite']}; обычных лидеров: {att_state['normal_leader']}, особых лидеров: {att_special_leaders}.")
            log.append(f"Конец раунда {round_num}: защитник - обычных отрядов: {def_state['normal']}, элитных: {def_state['elite']}, особых элитных: {def_state['special_elite']}; обычных лидеров: {def_state['normal_leader']}, особых лидеров: {def_special_leaders}.")
            log.append("----")
        round_num += 1
    # Результат боя (после выхода из цикла)
    att_units = att_state['normal'] + att_state['elite'] + att_state['special_elite']
    def_units = def_state['normal'] + def_state['elite'] + def_state['special_elite']
    defender_settlement_cubes = def_state.get('settlement', 0)

    # Определение самого сильного лидера у каждой стороны
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
    # Выживание сильнейших лидеров
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
    # Определение результата
    if att_units > 0 and def_units == 0:
        if log_active:
            log.append("Итог: победа атакующего!")
            return log
        else:
            return ("Attacker wins", att_units, def_units, att_strongest_survived, def_strongest_survived,att_strongest, def_strongest)
    elif def_units > 0 and att_units == 0:
        if log_active:
            log.append("Итог: победа защитника.")
            return log
        else:
            return ("Defender wins", att_units, def_units, att_strongest_survived, def_strongest_survived,att_strongest, def_strongest)
    else:
        if log_active:
            log.append("Итог: обе армии уничтожены.")
            return log
        else:
            return (
            "Both destroyed", att_units, def_units, att_strongest_survived, def_strongest_survived, att_strongest,
            def_strongest)

def update_defender_count(var, others):
    total = var.get() + sum(v.get() for v in others)
    if total > 6:
        var.set(max(0, 6 - sum(v.get() for v in others)))
        messagebox.showerror("Ошибка", "Суммарно можно не более 6 отрядов!")

root = tk.Tk()
root.title("Dune: War for Arrakis - Калькулятор боя")

att_frame = ttk.LabelFrame(root, text="Атакующий")
def_frame = ttk.LabelFrame(root, text="Защитник")
att_frame.grid(row=0, column=0, padx=5, pady=5, sticky="n")
def_frame.grid(row=0, column=1, padx=5, pady=5, sticky="n")

# Поля ввода для атакующей стороны
attacker_normal_var = tk.IntVar(value=0)
attacker_elite_var = tk.IntVar(value=0)
attacker_special_elite_var = tk.IntVar(value=0)
attacker_normal_leader_var = tk.IntVar(value=0)
attacker_cards_var = tk.IntVar(value=0)
defender_settlement_var = tk.IntVar(value=0)
sudden_attack_var = tk.BooleanVar(value=False)

ttk.Label(att_frame, text="Обычные отряды:").grid(row=0, column=0, sticky="e")
ttk.Spinbox(att_frame, from_=0, to=6, textvariable=attacker_normal_var, width=5).grid(row=0, column=1)
ttk.Label(att_frame, text="Элитные отряды:").grid(row=1, column=0, sticky="e")
ttk.Spinbox(att_frame, from_=0, to=6, textvariable=attacker_elite_var, width=5).grid(row=1, column=1)
ttk.Label(att_frame, text="Особые элитные отряды:").grid(row=2, column=0, sticky="e")
ttk.Spinbox(att_frame, from_=0, to=6, textvariable=attacker_special_elite_var, width=5).grid(row=2, column=1)
ttk.Label(att_frame, text="Обычные лидеры:").grid(row=3, column=0, sticky="e")
ttk.Spinbox(att_frame, from_=0, to=10, textvariable=attacker_normal_leader_var, width=5).grid(row=3, column=1)
ttk.Label(att_frame, text="Карты (доп. кубики):").grid(row=4, column=0, sticky="e")
ttk.Spinbox(att_frame, from_=0, to=10, textvariable=attacker_cards_var, width=5).grid(row=4, column=1)
ttk.Checkbutton(att_frame, text="Внезапная атака", variable=sudden_attack_var).grid(row=5, column=0, padx=0, pady=5, sticky="w")
ttk.Label(def_frame, text="Поселение (кубики):").grid(row=5, column=0, sticky="e")
ttk.Spinbox(def_frame, from_=0, to=3, textvariable=defender_settlement_var, width=5).grid(row=5, column=1)

# Флажки для особых лидеров атакующего
att_special_vars = {name: tk.BooleanVar(value=False) for name in special_leaders_data.keys()}
row_index = 6
ttk.Label(att_frame, text="Лидеры Атрейдес/Фримен:").grid(row=6, column=0, columnspan=2, sticky="w", pady=(5,0))
row_index += 1
for name in ["Paul Atreides", "Paul Muad'Dib", "Lady Jessica", "Mother Jessica", "Gurney Halleck", "Alia", "Stilgar", "Chani"]:
    ttk.Checkbutton(att_frame, text=name, variable=att_special_vars[name]).grid(row=row_index, column=0, columnspan=2, sticky="w")
    row_index += 1
ttk.Label(att_frame, text="Лидеры Харконнен/Коррино:").grid(row=row_index, column=0, columnspan=2, sticky="w", pady=(5,0))
row_index += 1
for name in ["Baron Harkonnen", "Beast Rabban", "Feyd-Rautha", "Thufir Hawat", "Shaddam IV", "G.H. Mohiam", "Captain Aramsham"]:
    ttk.Checkbutton(att_frame, text=name, variable=att_special_vars[name]).grid(row=row_index, column=0, columnspan=2, sticky="w")
    row_index += 1
max_unit_size = 6
# Поля ввода для защищающейся стороны
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
ttk.Label(def_frame, text="Обычные отряды:").grid(row=0, column=0, sticky="e")
ttk.Spinbox(def_frame, from_=0, to=6, textvariable=defender_normal_var, width=5).grid(row=0, column=1)
ttk.Label(def_frame, text="Элитные отряды:").grid(row=1, column=0, sticky="e")
ttk.Spinbox(def_frame, from_=0, to=6, textvariable=defender_elite_var, width=5).grid(row=1, column=1)
ttk.Label(def_frame, text="Особые элитные отряды:").grid(row=2, column=0, sticky="e")
ttk.Spinbox(def_frame, from_=0, to=6, textvariable=defender_special_elite_var, width=5).grid(row=2, column=1)
ttk.Label(def_frame, text="Обычные лидеры:").grid(row=3, column=0, sticky="e")
ttk.Spinbox(def_frame, from_=0, to=10, textvariable=defender_normal_leader_var, width=5).grid(row=3, column=1)
ttk.Label(def_frame, text="Карты (доп. кубики):").grid(row=4, column=0, sticky="e")
ttk.Spinbox(def_frame, from_=0, to=10, textvariable=defender_cards_var, width=5).grid(row=4, column=1)
# Флажки для особых лидеров защитника
def_special_vars = {name: tk.BooleanVar(value=False) for name in special_leaders_data.keys()}
row_index = 6
ttk.Label(def_frame, text="Лидеры Атрейдес/Фримен:").grid(row=6, column=0, columnspan=2, sticky="w", pady=(5,0))
row_index += 1
for name in ["Paul Muad'Dib", "Lady Jessica", "Gurney Halleck", "Alia", "Stilgar", "Chani"]:
    ttk.Checkbutton(def_frame, text=name, variable=def_special_vars[name]).grid(row=row_index, column=0, columnspan=2, sticky="w")
    row_index += 1
ttk.Label(def_frame, text="Лидеры Харконнен/Коррино:").grid(row=row_index, column=0, columnspan=2, sticky="w", pady=(5,0))
row_index += 1
for name in ["Baron Harkonnen", "Beast Rabban", "Feyd-Rautha", "Thufir Hawat", "Shaddam IV", "G.H. Mohiam", "Captain Aramsham"]:
    ttk.Checkbutton(def_frame, text=name, variable=def_special_vars[name]).grid(row=row_index, column=0, columnspan=2, sticky="w")
    row_index += 1

# Флажок "атака на поселение"
settlement_var = tk.BooleanVar(value=False)
ttk.Checkbutton(root, text="Атака на поселение (штраф атакующему)", variable=settlement_var).grid(row=1, column=0, columnspan=2, pady=5)

# Поле вывода результата/лога боя
output_text = tk.Text(root, width=100, height=30, wrap="word")
output_text.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
scrollbar = ttk.Scrollbar(root, orient="vertical", command=output_text.yview)
scrollbar.grid(row=3, column=2, sticky="ns")
output_text.configure(yscrollcommand=scrollbar.set, state="disabled")

# Функция обработки нажатия кнопки "Рассчитать бой"
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
    # Проверка: суммарное количество отрядов не должно превышать 6
    total_att_units = att_state['normal'] + att_state['elite'] + att_state['special_elite']
    total_def_units = def_state['normal'] + def_state['elite'] + def_state['special_elite']
    if total_att_units > 6 or total_def_units > 6:
        error_msg = ""
        if total_att_units > 6 and total_def_units > 6:
            error_msg = "В обеих армиях суммарно больше 6 фигурок."
        elif total_att_units > 6:
            error_msg = "У атакующей армии суммарно больше 6 фигурок."
        else:
            error_msg = "У защищающейся армии суммарно больше 6 фигурок."
        messagebox.showerror("Ошибка", error_msg)
        return
    # Проведение 1000 боёв для оценки вероятностей и статистики
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
        # Накопление статистики по выжившим и лидерам
        attacker_survivors_total += att_left
        defender_survivors_total += def_left
        if att_leader_alive: attacker_leader_survived_count += 1
        if def_leader_alive: defender_leader_survived_count += 1
        if att_strongest: att_strongest_name = att_strongest
        if def_strongest: def_strongest_name = def_strongest
    # Вывод результатов
    output_text.configure(state="normal")
    output_text.delete("1.0", tk.END)
    # Вероятности побед и ничьей
    draws = simulations - attacker_wins - defender_wins
    attacker_pct = attacker_wins / simulations * 100
    defender_pct = defender_wins / simulations * 100
    draw_pct = draws / simulations * 100
    output_text.insert(tk.END, f"\nШанс победы атакующего: {attacker_pct:.1f}%  |  шанс победы защитника: {defender_pct:.1f}%  |  ничья: {draw_pct:.1f}%   (симуляций: {simulations})")
    # Среднее количество выживших отрядов у атакующего и защитника
    avg_att_survivors = attacker_survivors_total / simulations
    avg_def_survivors = defender_survivors_total / simulations
    output_text.insert(tk.END, f"\nСреднее выживших отрядов – атакующий: {avg_att_survivors:.1f}, защитник: {avg_def_survivors:.1f}")
    # Шанс выживания самого сильного лидера у каждой стороны
    leader_att_survival_pct = (attacker_leader_survived_count / simulations) * 100
    leader_def_survival_pct = (defender_leader_survived_count / simulations) * 100
    if att_strongest_name and att_strongest_name != "нет":
        output_text.insert(
            tk.END,
            f"\nШанс выживания самого сильного лидера атакующего ({att_strongest_name}): {leader_att_survival_pct:.1f}%"
        )

    if def_strongest_name and def_strongest_name != "нет":
        output_text.insert(
            tk.END,
            f"\nШанс выживания самого сильного лидера защитника ({def_strongest_name}): {leader_def_survival_pct:.1f}%"
        )
    output_text.configure(state="disabled")
    output_text.yview_moveto(0)

# Функция для показа подробного лога одного боя
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
    # Проверка суммарного количества отрядов (не более 6)
    total_att_units = att_state['normal'] + att_state['elite'] + att_state['special_elite']
    total_def_units = def_state['normal'] + def_state['elite'] + def_state['special_elite']
    if total_att_units > 6 or total_def_units > 6:
        error_msg = ""
        if total_att_units > 6 and total_def_units > 6:
            error_msg = "В обеих армиях суммарно больше 6 фигурок."
        elif total_att_units > 6:
            error_msg = "У атакующей армии суммарно больше 6 фигурок."
        else:
            error_msg = "У защищающейся армии суммарно больше 6 фигурок."
        messagebox.showerror("Ошибка", error_msg)
        return
    # Получение лога одного боя
    log = simulate_battle(att_state, def_state, settlement=settlement_var.get(), sudden_attack=sudden_attack_var.get(),
                          log_active=True)
    # Отображение лога боя в новом окне
    log_window = tk.Toplevel(root)
    log_window.title("Лог боя")
    text = tk.Text(log_window, width=100, height=30, wrap="word")
    text.pack(side="left", fill="both", expand=True)
    scrollbar = ttk.Scrollbar(log_window, orient="vertical", command=text.yview)
    scrollbar.pack(side="right", fill="y")
    text.configure(yscrollcommand=scrollbar.set, state="normal")
    for line in log:
        text.insert(tk.END, line + "\n")
    text.configure(state="disabled")
    text.yview_moveto(0)

# Кнопки управления
ttk.Button(root, text="Рассчитать бой", command=run_calculation).grid(row=2, column=0, padx=5, pady=5)
ttk.Button(root, text="Показать лог боя", command=show_log).grid(row=2, column=1, padx=5, pady=5)

root.mainloop()
