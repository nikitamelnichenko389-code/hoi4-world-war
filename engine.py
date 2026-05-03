import json
import os
import sys

def run_game():
    if not os.path.exists('game_state.json'): return
    
    with open('game_state.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 1. Начисляем золото за владение городами
    for p in data["players"].values():
        p["gold"] += len(p["cities"]) * 10

    # 2. Обработка атаки через аргументы (от GitHub Action)
    if len(sys.argv) > 2:
        title = sys.argv[1] # Пример: "ATTACK:Берлин"
        attacker_login = sys.argv[2] # Кто нажал кнопку
        
        if title.startswith("ATTACK:"):
            target_city = title.split(":")[1]
            attacker_name = None
            
            # Определяем, кто атакует (поиск по логину или дефолтный)
            # В этой версии просто берем первого игрока для теста или сопоставляем
            attacker_name = "Никита" # Можно усложнить логику привязки
            
            for owner_name, owner_data in data["players"].items():
                if target_city in owner_data["cities"] and owner_name != attacker_name:
                    owner_data["cities"].remove(target_city)
                    data["players"][attacker_name]["cities"].append(target_city)
                    print(f"SUCCESS: {target_city} captured by {attacker_name}")
                    break

    with open('game_state.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    run_game()
