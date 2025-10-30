import requests
import time
import os
from strategies import *
from notify import send_alert

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

PROCESSED_GAMES = set()

def get_live_games():
    url = "https://api.sofascore.com/api/v1/sport/football/events/live"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        return res.json().get('events', []) if res.status_code == 200 else []
    except:
        return []

def get_game_stats(event_id):
    try:
        info = requests.get(f"https://api.sofascore.com/api/v1/event/{event_id}", headers=HEADERS, timeout=10).json()['event']
        minute = info.get('homeScore', {}).get('currentPeriodStartMinute', 0)
        if minute is None: minute = 0
        score = f"{info['homeScore']['current']}x{info['awayScore']['current']}"
        
        dangerous_attacks = corners = shots = 0
        stats_res = requests.get(f"https://api.sofascore.com/api/v1/event/{event_id}/statistics", headers=HEADERS, timeout=10)
        if stats_res.status_code == 200:
            data = stats_res.json()
            if 'statistics' in data and data['statistics']:
                for group in data['statistics'][0]['groups']:
                    for item in group['statisticsItems']:
                        name = item['name'].lower()
                        home_val = int(item['home']) if str(item['home']).isdigit() else 0
                        away_val = int(item['away']) if str(item['away']).isdigit() else 0
                        total = home_val + away_val
                        if 'dangerous' in name or 'perigoso' in name:
                            dangerous_attacks = total
                        elif 'corner' in name or 'escanteio' in name:
                            corners = total
                        elif 'shot' in name or 'finaliza' in name:
                            shots = total
        
        return {
            'minute': minute,
            'score': score,
            'dangerous_attacks': dangerous_attacks,
            'corners': corners,
            'shots': shots,
            'appm': dangerous_attacks / minute if minute > 0 else 0,
            'home_id': info['homeTeam']['id'],
            'away_id': info['awayTeam']['id']
        }
    except:
        return None

def main_loop():
    print("🤖 Robô iniciado! Verificando jogos a cada 60 segundos...")
    while True:
        try:
            for game in get_live_games():
                event_id = game['id']
                if event_id in PROCESSED_GAMES:
                    continue
                stats = get_game_stats(event_id)
                if not stats or stats['minute'] == 0:
                    continue
                game_data = {
                    'id': event_id,
                    'home': game['homeTeam']['name'],
                    'away': game['awayTeam']['name'],
                    'score': stats['score'],
                    'minute': stats['minute'],
                    'home_id': stats['home_id'],
                    'away_id': stats['away_id']
                }
                if check_strategy_1_gol_ht_super_favorito(game_data, stats):
                    send_alert(f"✅ GOL HT SUPER FAVORITO\n{game_data['home']} x {game_data['away']}\nMinuto: {stats['minute']}")
                    PROCESSED_GAMES.add(event_id)
                elif check_strategy_2_gol_ht_sem_favorito(game_data, stats):
                    send_alert(f"✅ GOL HT SEM FAVORITO\n{game_data['home']} x {game_data['away']}\nMinuto: {stats['minute']}")
                    PROCESSED_GAMES.add(event_id)
                elif check_strategy_3_over_limite_favorito(game_data, stats):
                    send_alert(f"✅ OVER LIMITE FAVORITO\n{game_data['home']} x {game_data['away']}\nPlacar: {stats['score']}")
                    PROCESSED_GAMES.add(event_id)
                elif check_strategy_4_over_limite_sem_favorito(game_data, stats):
                    send_alert(f"✅ OVER LIMITE SEM FAVORITO\n{game_data['home']} x {game_data['away']}\nPlacar: {stats['score']}")
                    PROCESSED_GAMES.add(event_id)
            time.sleep(60)
        except KeyboardInterrupt:
            break
        except:
            time.sleep(30)

if __name__ == "__main__":
    main_loop()
