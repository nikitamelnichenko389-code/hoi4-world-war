import json, os, sys

def run_game():
    if not os.path.exists('game_state.json'): return
    with open('game_state.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 1. ЭКОНОМИКА: Начисление ресурсов за удержание территорий и фабрики
    for p in data["players"].values():
        p["gold"] += (len(p["cities"]) * 5) + (p.get("factories", 1) * 10)

    # 2. ОБРАБОТКА КОМАНД (через Issues)
    if len(sys.argv) > 2:
        command = sys.argv[1]
        user = sys.argv[2] # GitHub Login пользователя

        # РЕГИСТРАЦИЯ
        if command.startswith("REGISTER:"):
            c_name = command.split(":")[1]
            if c_name in data["available_countries"] and user not in data["players"]:
                c_data = data["available_countries"].pop(c_name)
                data["players"][user] = c_data
                data["players"][user]["country_name"] = c_name

        # ДЕЙСТВИЯ ЗАРЕГИСТРИРОВАННЫХ ИГРОКОВ
        elif user in data["players"]:
            p = data["players"][user]
            if command.startswith("ATTACK:"):
                target = command.split(":")[1]
                for o_name, o_data in data["players"].items():
                    if target in o_data["cities"] and o_name != user:
                        # Логика боя: Нужно иметь >= дивизий, чем у защитника
                        if p["divisions"] >= o_data["divisions"]:
                            o_data["cities"].remove(target)
                            p["cities"].append(target)
                            p["divisions"] = max(0, p["divisions"] - 1) # Потери
                            data["world_tension"] += 2
                        break
            
            elif command == "BUILD_DIV" and p["gold"] >= 50:
                p["gold"] -= 50; p["divisions"] += 1
            elif command == "BUILD_FAC" and p["gold"] >= 150:
                p["gold"] -= 150; p["factories"] += 1
            elif command == "BUILD_SHIP" and p["gold"] >= 100 and p.get("dockyards", 0) > 0:
                p["gold"] -= 100; p["ships"] += 1

    with open('game_state.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    run_game()
