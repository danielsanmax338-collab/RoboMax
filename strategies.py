from history import get_last_games_stats
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def get_odds_placeholder():
    return {
        'ht_goal': 1.60,
        'over_05': 1.30,
        'over_15': 1.80,
        'over_25': 2.40,
        'home_win': 1.50,
        'away_win': 2.60
    }

def get_odds(game, stats):
    return stats.get('odds') or game.get('odds') or get_odds_placeholder()

def average_pct(total_pct, venue_pct):
    return (total_pct + venue_pct) / 2

def has_favorite(odds, threshold):
    return min(odds.get('home_win', 99), odds.get('away_win', 99)) <= threshold

def check_strategy_1_gol_ht_super_favorito(game, stats):
    minute = game['minute']
    if minute > 25:
        return False
    appm = stats['appm']
    chances = stats['corners'] + stats['shots']
    odds = get_odds(game, stats)
    if appm < 0.8 or chances < 10 or odds['ht_goal'] < 1.50:
        return False
    if not has_favorite(odds, 1.30):
        return False
    home_hist = get_last_games_stats(game['home_id'], is_home=True)
    away_hist = get_last_games_stats(game['away_id'], is_home=False)
    home_avg = average_pct(home_hist['gols_ht_pct_total'], home_hist['gols_ht_pct_venue'])
    away_avg = average_pct(away_hist['gols_ht_pct_total'], away_hist['gols_ht_pct_venue'])
    return home_avg >= 70 or away_avg >= 70

def check_strategy_2_gol_ht_sem_favorito(game, stats):
    minute = game['minute']
    if minute > 25:
        return False
    appm = stats['appm']
    chances = stats['corners'] + stats['shots']
    odds = get_odds(game, stats)
    if appm < 1.0 or chances < 10 or odds['ht_goal'] < 1.50:
        return False
    if has_favorite(odds, 1.30):
        return False
    home_hist = get_last_games_stats(game['home_id'], is_home=True)
    away_hist = get_last_games_stats(game['away_id'], is_home=False)
    home_avg = average_pct(home_hist['gols_ht_pct_total'], home_hist['gols_ht_pct_venue'])
    away_avg = average_pct(away_hist['gols_ht_pct_total'], away_hist['gols_ht_pct_venue'])
    return home_avg >= 80 or away_avg >= 80

def check_strategy_3_over_limite_favorito(game, stats):
    minute = game['minute']
    if minute > 70:
        return False
    appm = stats['appm']
    chances = stats['corners'] + stats['shots']
    if appm < 0.8 or chances < 20:
        return False
    score = game['score']
    if score not in ["0x0", "1x1", "2x2", "0x1", "1x2", "2x3"]:
        return False
    goals = sum(map(int, score.split('x')))
    odds = get_odds(game, stats)
    over_odds = {0: odds['over_05'], 1: odds['over_15'], 2: odds['over_25']}.get(goals, 0)
    if over_odds < 1.50:
        return False
    if not has_favorite(odds, 1.80):
        return False
    home_hist = get_last_games_stats(game['home_id'], is_home=True)
    away_hist = get_last_games_stats(game['away_id'], is_home=False)
    home_05_avg = average_pct(home_hist['gols_05_ft_pct_total'], home_hist['gols_05_ft_pct_venue'])
    home_15_avg = average_pct(home_hist['gols_15_ft_pct_total'], home_hist['gols_15_ft_pct_venue'])
    away_05_avg = average_pct(away_hist['gols_05_ft_pct_total'], away_hist['gols_05_ft_pct_venue'])
    away_15_avg = average_pct(away_hist['gols_15_ft_pct_total'], away_hist['gols_15_ft_pct_venue'])
    home_ok = home_05_avg >= 80 and home_15_avg >= 80
    away_ok = away_05_avg >= 80 and away_15_avg >= 80
    return home_ok or away_ok

def check_strategy_4_over_limite_sem_favorito(game, stats):
    minute = game['minute']
    if minute > 70:
        return False
    appm = stats['appm']
    chances = stats['corners'] + stats['shots']
    if appm < 1.0 or chances < 30:
        return False
    score = game['score']
    if score not in ["0x0", "1x1", "2x2", "0x1", "1x2", "2x3"]:
        return False
    goals = sum(map(int, score.split('x')))
    odds = get_odds(game, stats)
    over_odds = {0: odds['over_05'], 1: odds['over_15'], 2: odds['over_25']}.get(goals, 0)
    if over_odds < 1.50:
        return False
    if has_favorite(odds, 1.80):
        return False
    home_hist = get_last_games_stats(game['home_id'], is_home=True)
    away_hist = get_last_games_stats(game['away_id'], is_home=False)
    home_05_avg = average_pct(home_hist['gols_05_ft_pct_total'], home_hist['gols_05_ft_pct_venue'])
    home_15_avg = average_pct(home_hist['gols_15_ft_pct_total'], home_hist['gols_15_ft_pct_venue'])
    away_05_avg = average_pct(away_hist['gols_05_ft_pct_total'], away_hist['gols_05_ft_pct_venue'])
    away_15_avg = average_pct(away_hist['gols_15_ft_pct_total'], away_hist['gols_15_ft_pct_venue'])
    home_ok = home_05_avg >= 90 and home_15_avg >= 80
    away_ok = away_05_avg >= 90 and away_15_avg >= 80
    return home_ok or away_ok
