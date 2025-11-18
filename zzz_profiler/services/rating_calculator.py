# zzz_profiler/services/rating_calculator.py

# --- ИЗМЕНЕНИЕ: Импортируем оба словаря порогов ---
from zzz_profiler.config import RANK_THRESHOLDS, AGENT_RANK_THRESHOLDS

def calculate_disk_rating(disk_data: dict, weights: dict, normalization_values: dict) -> float:
    total_rating = 0.0
    sub_stats = disk_data.get('sub_stats', [])

    for stat in sub_stats:
        stat_name = stat.get('name')
        stat_value_raw = stat.get('value', 0)
        
        if stat_name:
            normalization_value = normalization_values.get(stat_name, 1.0)
            if normalization_value == 0: continue
            is_percent = '%' in stat.get('format', '')
            actual_value = stat_value_raw / 100.0 if is_percent else stat_value_raw
            num_rolls = actual_value / normalization_value
            weight = weights.get(stat_name, 0)
            total_rating += num_rolls * weight

    return round(total_rating, 2)

def get_rank_from_rating(rating: float) -> str:
    for threshold, rank in RANK_THRESHOLDS:
        if rating >= threshold:
            return rank
    return 'D'

# --- НОВАЯ ФУНКЦИЯ ---
def get_agent_rank_from_score(score: float) -> str:
    """Определяет ранг всего агента на основе его общего счета."""
    for threshold, rank in AGENT_RANK_THRESHOLDS:
        if score >= threshold:
            return rank
    return 'D'