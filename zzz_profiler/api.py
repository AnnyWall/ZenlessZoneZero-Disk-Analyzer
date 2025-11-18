# zzz_profiler/api.py

import asyncio
from flask import Blueprint, jsonify
from enka import ZZZClient
from enka.errors import PlayerDoesNotExistError, GameMaintenanceError

# --- ИЗМЕНЕНИЕ ЗДЕСЬ: Абсолютные импорты ---
from zzz_profiler.services.rating_calculator import calculate_disk_rating, get_rank_from_rating, get_agent_rank_from_score
from zzz_profiler.config import DISK_SET_NAMES, STAT_WEIGHTS, STAT_NORMALIZATION_VALUES

api_bp = Blueprint('api', __name__)

async def fetch_zzz_data(uid: str):
    async with ZZZClient() as client:
        return await client.fetch_showcase(uid)

@api_bp.route('/profile/<uid>', methods=['GET'])
def get_user_profile(uid: str):
    try:
        raw_data = asyncio.run(fetch_zzz_data(uid))
        player_data = raw_data.player.model_dump(mode='json')
        
        agents_data = []
        if raw_data.agents:
            for agent in raw_data.agents:
                agent_dict = agent.model_dump(mode='json')
                
                agent_total_score = 0  # --- ВОССТАНАВЛИВАЕМ счетчик ---
                
                agent_name = agent.name
                profile_name = agent_name if agent_name in STAT_WEIGHTS else 'DEFAULT_DPS'
                weights = STAT_WEIGHTS[profile_name]
                
                discs_data = []
                if agent.discs:
                    for disc in agent.discs:
                        if not disc: continue
                        disc_dict = disc.model_dump(mode='json')
                        set_id = disc.set_id
                        disc_dict['set_name'] = DISK_SET_NAMES.get(set_id, f"Set ID {set_id}")
                        
                        rating = calculate_disk_rating(disc_dict, weights, STAT_NORMALIZATION_VALUES)
                        agent_total_score += rating  # --- ВОССТАНАВЛИВАЕМ суммирование ---
                        
                        rank = get_rank_from_rating(rating)
                        disc_dict['rating'] = rating
                        disc_dict['rank'] = rank
                        disc_dict['calculation_weights'] = weights
                        disc_dict['calculation_profile_name'] = profile_name 
                        
                        discs_data.append(disc_dict)
                
                agent_dict['discs'] = discs_data
                # --- ДОБАВЛЯЕМ ОБЩИЙ СЧЕТ И РАНГ АГЕНТА ---
                agent_dict['total_score'] = round(agent_total_score, 2)
                agent_dict['agent_rank'] = get_agent_rank_from_score(agent_total_score)
                
                agents_data.append(agent_dict)
        
        final_response = { "player": player_data, "agents": agents_data }
        return jsonify(final_response)

    except PlayerDoesNotExistError:
        return jsonify({"error": f"Профиль с UID {uid} не найден или скрыт."}), 404
    except GameMaintenanceError:
        return jsonify({"error": "Серверы игры на техобслуживании."}), 503
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "Произошла внутренняя ошибка сервера."}), 500