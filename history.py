import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def get_last_games_stats(team_id, is_home=True):
    if not team_id:
        return {'gols_ht_pct': 0, 'gols_05_ft_pct': 0, 'gols_15_ft_pct': 0}
    
    url = f"https://api.sofascore.com/api/v1/team/{team_id}/events/last/5"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code != 200:
            return {'gols_ht_pct': 0, 'gols_05_ft_pct': 0, 'gols_15_ft_pct': 0}
        
        data = res.json()
        games = data.get('events', [])
        if not games:
            return {'gols_ht_pct': 0, 'gols_05_ft_pct': 0, 'gols_15_ft_pct': 0}
        
        ht_goals = 0
        ft_05 = 0
        ft_15 = 0
        total = len(games)
        
        for g in games:
            if is_home and g.get('homeTeam', {}).get('id') != team_id:
                continue
            if not is_home and g.get('awayTeam', {}).get('id') != team_id:
                continue
                
            p1_home = g.get('homeScore', {}).get('period1', 0) or 0
            p1_away = g.get('awayScore', {}).get('period1', 0) or 0
            ft_home = g.get('homeScore', {}).get('current', 0) or 0
            ft_away = g.get('awayScore', {}).get('current', 0) or 0
            
            if p1_home + p1_away > 0:
                ht_goals += 1
            if ft_home + ft_away > 0:
                ft_05 += 1
            if ft_home + ft_away > 1:
                ft_15 += 1
        
        return {
            'gols_ht_pct': (ht_goals / total) * 100,
            'gols_05_ft_pct': (ft_05 / total) * 100,
            'gols_15_ft_pct': (ft_15 / total) * 100
        }
    except Exception as e:
        print(f"[HISTÓRICO ERRO] {e}")
        return {'gols_ht_pct': 0, 'gols_05_ft_pct': 0, 'gols_15_ft_pct': 0}
