import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def get_last_games_stats(team_id, is_home=True):
    if not team_id:
        return {
            'gols_ht_pct_total': 0,
            'gols_ht_pct_venue': 0,
            'gols_05_ft_pct_total': 0,
            'gols_05_ft_pct_venue': 0,
            'gols_15_ft_pct_total': 0,
            'gols_15_ft_pct_venue': 0
        }
    
    url = f"https://api.sofascore.com/api/v1/team/{team_id}/events/last/5"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code != 200:
            return {
                'gols_ht_pct_total': 0,
                'gols_ht_pct_venue': 0,
                'gols_05_ft_pct_total': 0,
                'gols_05_ft_pct_venue': 0,
                'gols_15_ft_pct_total': 0,
                'gols_15_ft_pct_venue': 0
            }
        
        data = res.json()
        games = data.get('events', [])
        if not games:
            return {
                'gols_ht_pct_total': 0,
                'gols_ht_pct_venue': 0,
                'gols_05_ft_pct_total': 0,
                'gols_05_ft_pct_venue': 0,
                'gols_15_ft_pct_total': 0,
                'gols_15_ft_pct_venue': 0
            }

        ht_goals_total = 0
        ft_05_total = 0
        ft_15_total = 0
        ht_goals_venue = 0
        ft_05_venue = 0
        ft_15_venue = 0
        total_games = len(games)
        venue_games = 0

        for g in games:
            p1_home = g.get('homeScore', {}).get('period1', 0) or 0
            p1_away = g.get('awayScore', {}).get('period1', 0) or 0
            ft_home = g.get('homeScore', {}).get('current', 0) or 0
            ft_away = g.get('awayScore', {}).get('current', 0) or 0

            if p1_home + p1_away > 0:
                ht_goals_total += 1
            if ft_home + ft_away > 0:
                ft_05_total += 1
            if ft_home + ft_away > 1:
                ft_15_total += 1

            is_venue = g.get('homeTeam', {}).get('id') == team_id if is_home else g.get('awayTeam', {}).get('id') == team_id
            if is_venue:
                venue_games += 1
                if p1_home + p1_away > 0:
                    ht_goals_venue += 1
                if ft_home + ft_away > 0:
                    ft_05_venue += 1
                if ft_home + ft_away > 1:
                    ft_15_venue += 1

        total_div = total_games if total_games else 1
        venue_div = venue_games if venue_games else 1

        return {
            'gols_ht_pct_total': (ht_goals_total / total_div) * 100,
            'gols_ht_pct_venue': (ht_goals_venue / venue_div) * 100 if venue_games else 0,
            'gols_05_ft_pct_total': (ft_05_total / total_div) * 100,
            'gols_05_ft_pct_venue': (ft_05_venue / venue_div) * 100 if venue_games else 0,
            'gols_15_ft_pct_total': (ft_15_total / total_div) * 100,
            'gols_15_ft_pct_venue': (ft_15_venue / venue_div) * 100 if venue_games else 0
        }
    except Exception as e:
        print(f"[HISTÓRICO ERRO] {e}")
        return {
            'gols_ht_pct_total': 0,
            'gols_ht_pct_venue': 0,
            'gols_05_ft_pct_total': 0,
            'gols_05_ft_pct_venue': 0,
            'gols_15_ft_pct_total': 0,
            'gols_15_ft_pct_venue': 0
        }
