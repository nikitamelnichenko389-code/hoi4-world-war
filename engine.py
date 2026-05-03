import json
import os

def run_game():
    # Загружаем данные
    if os.path.exists('game_state.json'):
        with open('game_state.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    
    # ЛОГИКА: Каждое обновление дает +10 золота за каждый город
    for player in data["players"].values():
        player["gold"] += len(player["cities"]) * 10
    
    # Сохраняем результат
    with open('game_state.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    run_game()
