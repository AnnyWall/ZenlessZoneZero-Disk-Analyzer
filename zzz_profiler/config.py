# zzz_profiler/config.py

STAT_NORMALIZATION_VALUES = {
    'Percent ATK': 4.5,
    'CRIT Rate': 3.2,
    'CRIT DMG': 6.4,
    'PEN Ratio': 0.0,      # Этот стат не роллится в сабстатах
    'Anomaly Mastery': 16, # Это плоский стат, не процентный
    'Anomaly Proficiency': 18,
    'Energy Regen': 0.0,   # Этот стат не роллится в сабстатах
    'ATK': 19,
    'HP': 254,
    'Percent HP': 4.5,
    'DEF': 15,
    'Percent DEF': 4.8,
    'Impact': 0.0,         # Этот стат не роллится в сабстатах
    'PEN': 9               # Это плоский стат, не процентный
}

STAT_WEIGHTS = {
    'DEFAULT_DPS': {
        'Percent ATK': 1.5, 'CRIT Rate': 2.0, 'CRIT DMG': 1.0, 'PEN Ratio': 1.5,
        'Energy Regen': 1.2, 'Impact': 0.5, 'ATK': 0.2, 'PEN': 0.1,
        'Anomaly Mastery': 0.5, 'Anomaly Proficiency': 0.5, 'Sheer Force': 0.0,
        'HP': 0.0, 'Percent HP': 0.0, 'DEF': 0.0, 'Percent DEF': 0.0
    },

    
    'Ellen': { 'Percent ATK': 1.5, 'CRIT Rate': 2.0, 'CRIT DMG': 2.0, 'PEN Ratio': 1, 'Energy Regen': 0, 'Impact': 0, 'ATK':  1, 'PEN': 1, 'Anomaly Mastery': 0, 'Anomaly Proficiency': 0, 'Sheer Force': 0.0, 'HP': 0.0, 'Percent HP': 0.0, 'DEF': 0.0, 'Percent DEF': 0.0 },
    'Grace': { 'Percent ATK': 1.5, 'CRIT Rate': 0, 'CRIT DMG': 0, 'PEN Ratio': 2, 'Energy Regen': 0, 'Impact': 0, 'ATK': 0.5, 'PEN': 1, 'Anomaly Mastery': 0, 'Anomaly Proficiency': 2, 'Sheer Force': 0.0, 'HP': 0.0, 'Percent HP': 0.0, 'DEF': 0.0, 'Percent DEF': 0.0 },
    'Koleda': { 'Percent ATK': 1, 'CRIT Rate': 2.0, 'CRIT DMG': 1.5, 'PEN Ratio': 1, 'Energy Regen': 0, 'Impact': 0, 'ATK': 1, 'PEN': 1, 'Anomaly Mastery': 0, 'Anomaly Proficiency': 0, 'Sheer Force': 0.0, 'HP': 0.0, 'Percent HP': 0.0, 'DEF': 0.0, 'Percent DEF': 0.0 },
    'Lighter': { 'Percent ATK': 1, 'CRIT Rate': 2.0, 'CRIT DMG': 1.5, 'PEN Ratio': 0.5, 'Energy Regen': 0, 'Impact': 0, 'ATK': 0.5, 'PEN': 0.5, 'Anomaly Mastery': 0, 'Anomaly Proficiency': 0, 'Sheer Force': 0.0, 'HP': 0.0, 'Percent HP': 0.0, 'DEF': 0.0, 'Percent DEF': 0.0 },
    'Lycaon': { 'Percent ATK': 1.5, 'CRIT Rate': 2.0, 'CRIT DMG': 2.0, 'PEN Ratio': 1, 'Energy Regen': 0, 'Impact': 0, 'ATK': 1, 'PEN': 1, 'Anomaly Mastery': 0, 'Anomaly Proficiency': 0, 'Sheer Force': 0.0, 'HP': 0.0, 'Percent HP': 0.0, 'DEF': 0.0, 'Percent DEF': 0.0 },
    'Rina': { 'Percent ATK': 1.5, 'CRIT Rate': 0, 'CRIT DMG': 0, 'PEN Ratio': 0.9, 'Energy Regen': 0, 'Impact': 0, 'ATK': 0.5, 'PEN': 0.9, 'Anomaly Mastery': 0, 'Anomaly Proficiency': 0, 'Sheer Force': 0.0, 'HP': 0.0, 'Percent HP': 0.0, 'DEF': 0.0, 'Percent DEF': 0.0 },
    'Zhu Yuan': { 'Percent ATK': 1.6, 'CRIT Rate': 2.0, 'CRIT DMG': 2.0, 'PEN Ratio': 1.5, 'Energy Regen': 1.2, 'Impact': 0.5, 'ATK': 0.2, 'PEN': 0.1, 'Anomaly Mastery': 0.5, 'Anomaly Proficiency': 0.5, 'Sheer Force': 0.0, 'HP': 0.0, 'Percent HP': 0.0, 'DEF': 0.0, 'Percent DEF': 0.0 },
    'Yidhari': { 'Percent ATK': 1, 'CRIT Rate': 2.0, 'CRIT DMG': 2.0, 'PEN Ratio': 0, 'Energy Regen': 0, 'Impact': 0, 'ATK': 0, 'PEN': 0, 'Anomaly Mastery': 0, 'Anomaly Proficiency': 0, 'Sheer Force': 0.0, 'HP': 1, 'Percent HP': 1.5, 'DEF': 0.0, 'Percent DEF': 0.0 },
    'Yixuan': { 'Percent ATK': 1, 'CRIT Rate': 2.0, 'CRIT DMG': 2.0, 'PEN Ratio': 1.5, 'Energy Regen': 0, 'Impact': 0, 'ATK': 0, 'PEN': 0.1, 'Anomaly Mastery': 0, 'Anomaly Proficiency': 0, 'Sheer Force': 0.0, 'HP': 0.5, 'Percent HP': 1.5, 'DEF': 0.0, 'Percent DEF': 0.0 },
    'Yuzuhа': { 'Percent ATK': 2, 'CRIT Rate': 0.5, 'CRIT DMG': 0.5, 'PEN Ratio': 0.3, 'Energy Regen': 0, 'Impact': 0, 'ATK': 1.5, 'PEN': 0.3, 'Anomaly Mastery': 0, 'Anomaly Proficiency': 1.4, 'Sheer Force': 0.0, 'HP': 0.0, 'Percent HP': 0.0, 'DEF': 0.0, 'Percent DEF': 0.0 },
    
    'Anby': { 'Percent ATK': 1, 'CRIT Rate': 2.0, 'CRIT DMG': 2.0, 'PEN Ratio': 0.5, 'Energy Regen': 0, 'Impact': 0, 'ATK': 0.5, 'PEN': 0.5, 'Anomaly Mastery': 0, 'Anomaly Proficiency': 0, 'Sheer Force': 0.0, 'HP': 0.0, 'Percent HP': 0.0, 'DEF': 0.0, 'Percent DEF': 0.0 },
    'Anton': { 'Percent ATK': 1.5, 'CRIT Rate': 2.0, 'CRIT DMG': 2.0, 'PEN Ratio': 1, 'Energy Regen': 0, 'Impact': 0, 'ATK': 0.5, 'PEN': 1, 'Anomaly Mastery': 0, 'Anomaly Proficiency': 0, 'Sheer Force': 0.0, 'HP': 0.0, 'Percent HP': 0.0, 'DEF': 0.0, 'Percent DEF': 0.0 },
    'Ben': { 'Percent ATK': 1.5, 'CRIT Rate': 1.5, 'CRIT DMG': 1.5, 'PEN Ratio': 1.5, 'Energy Regen': 1.2, 'Impact': 0.5, 'ATK': 0.2, 'PEN': 1.5, 'Anomaly Mastery': 0.5, 'Anomaly Proficiency': 0.5, 'Sheer Force': 0.0, 'HP': 0.0, 'Percent HP': 0.0, 'DEF': 1, 'Percent DEF': 2.0 },
    'Billy': { 'Percent ATK': 1.5, 'CRIT Rate': 2.0, 'CRIT DMG': 2.0, 'PEN Ratio': 0, 'Energy Regen': 0, 'Impact': 0, 'ATK': 1, 'PEN': 1, 'Anomaly Mastery': 0, 'Anomaly Proficiency': 0, 'Sheer Force': 0.0, 'HP': 0.0, 'Percent HP': 0.0, 'DEF': 0.0, 'Percent DEF': 0.0 },
    'Corin': { 'Percent ATK': 1.5, 'CRIT Rate': 2.0, 'CRIT DMG': 2.0, 'PEN Ratio': 1, 'Energy Regen': 0, 'Impact': 0, 'ATK': 1, 'PEN': 1, 'Anomaly Mastery': 0, 'Anomaly Proficiency': 0, 'Sheer Force': 0.0, 'HP': 0.0, 'Percent HP': 0.0, 'DEF': 0.0, 'Percent DEF': 0.0 },
    'Lucy': { 'Percent ATK': 2, 'CRIT Rate': 2.0, 'CRIT DMG': 2.0, 'PEN Ratio': 1.5, 'Energy Regen': 0, 'Impact': 0, 'ATK': 1.5, 'PEN': 1.5, 'Anomaly Mastery': 0, 'Anomaly Proficiency': 0, 'Sheer Force': 0.0, 'HP': 0.0, 'Percent HP': 0.0, 'DEF': 0.0, 'Percent DEF': 0.0 },
    'Manato': { 'Percent ATK': 0.5, 'CRIT Rate': 2.0, 'CRIT DMG': 2.0, 'PEN Ratio': 0, 'Energy Regen': 0, 'Impact': 0, 'ATK': 0.4, 'PEN': 0, 'Anomaly Mastery': 0, 'Anomaly Proficiency': 0, 'Sheer Force': 0.0, 'HP': 1, 'Percent HP': 1.5, 'DEF': 0.0, 'Percent DEF': 0.0 },
    'Nicole': { 'Percent ATK': 2, 'CRIT Rate': 0, 'CRIT DMG': 0, 'PEN Ratio': 1.5, 'Energy Regen': 0, 'Impact': 0, 'ATK': 1.5, 'PEN': 1.5, 'Anomaly Mastery': 0, 'Anomaly Proficiency': 2, 'Sheer Force': 0.0, 'HP': 0.0, 'Percent HP': 0.0, 'DEF': 0.0, 'Percent DEF': 0.0 },
    'Piper': { 'Percent ATK': 1.5, 'CRIT Rate': 0, 'CRIT DMG': 0, 'PEN Ratio': 1, 'Energy Regen': 0, 'Impact': 0, 'ATK': 1, 'PEN': 1, 'Anomaly Mastery': 0, 'Anomaly Proficiency': 2, 'Sheer Force': 0.0, 'HP': 0.0, 'Percent HP': 0.0, 'DEF': 0.0, 'Percent DEF': 0.0 },
    'Pulchra': { 'Percent ATK': 1.5, 'CRIT Rate': 2.0, 'CRIT DMG': 2.0, 'PEN Ratio': 1, 'Energy Regen': 0, 'Impact': 0, 'ATK': 1, 'PEN': 1, 'Anomaly Mastery': 0, 'Anomaly Proficiency': 0, 'Sheer Force': 0.0, 'HP': 0.0, 'Percent HP': 0.0, 'DEF': 0.0, 'Percent DEF': 0.0 },
    'Seth': { 'Percent ATK': 2, 'CRIT Rate': 0, 'CRIT DMG': 0, 'PEN Ratio': 0.5, 'Energy Regen': 0, 'Impact': 0, 'ATK': 1, 'PEN': 0.5, 'Anomaly Mastery': 0, 'Anomaly Proficiency': 1.5, 'Sheer Force': 0.0, 'HP': 0.0, 'Percent HP': 0.0, 'DEF': 0.0, 'Percent DEF': 0.0 },
    'Soukaku': { 'Percent ATK': 2, 'CRIT Rate': 2.0, 'CRIT DMG': 2.0, 'PEN Ratio': 1.5, 'Energy Regen': 0, 'Impact': 0, 'ATK': 1, 'PEN': 1, 'Anomaly Mastery': 0, 'Anomaly Proficiency': 0, 'Sheer Force': 0.0, 'HP': 0.0, 'Percent HP': 0.0, 'DEF': 0.0, 'Percent DEF': 0.0 },

    'Alice': { 'Percent ATK': 1.5, 'CRIT Rate': 0, 'CRIT DMG': 0, 'PEN Ratio': 1, 'Energy Regen': 0, 'Impact': 0, 'ATK': 0.5, 'PEN': 0, 'Anomaly Mastery': 0, 'Anomaly Proficiency': 2, 'Sheer Force': 0.0, 'HP': 0.0, 'Percent HP': 0.0, 'DEF': 0.0, 'Percent DEF': 0.0 },
    'Burnice': { 'Percent ATK': 1.5, 'CRIT Rate': 0, 'CRIT DMG': 0, 'PEN Ratio': 1, 'Energy Regen': 0, 'Impact': 0, 'ATK': 1, 'PEN': 0.1, 'Anomaly Mastery': 0, 'Anomaly Proficiency': 2, 'Sheer Force': 0.0, 'HP': 0.0, 'Percent HP': 0.0, 'DEF': 0.0, 'Percent DEF': 0.0 },
    'Caesar': { 'Percent ATK': 1.5, 'CRIT Rate': 2.0, 'CRIT DMG': 2.0, 'PEN Ratio': 1, 'Energy Regen': 0, 'Impact': 0, 'ATK': 0.8, 'PEN': 1, 'Anomaly Mastery': 0, 'Anomaly Proficiency': 0, 'Sheer Force': 0.0, 'HP': 0.0, 'Percent HP': 0.0, 'DEF': 0.0, 'Percent DEF': 0.0 },
    'Harumasa': { 'Percent ATK': 1.5, 'CRIT Rate': 2.0, 'CRIT DMG': 2.0, 'PEN Ratio': 1, 'Energy Regen': 0, 'Impact': 0, 'ATK': 0.5, 'PEN': 1, 'Anomaly Mastery': 0, 'Anomaly Proficiency': 0, 'Sheer Force': 0.0, 'HP': 0.0, 'Percent HP': 0.0, 'DEF': 0.0, 'Percent DEF': 0.0 },
    'Jane': { 'Percent ATK': 1.5, 'CRIT Rate': 0, 'CRIT DMG': 0, 'PEN Ratio': 1, 'Energy Regen': 0, 'Impact': 0, 'ATK': 1, 'PEN': 1, 'Anomaly Mastery': 0, 'Anomaly Proficiency': 2, 'Sheer Force': 0.0, 'HP': 0.0, 'Percent HP': 0.0, 'DEF': 0.0, 'Percent DEF': 0.0 },
    'Lucia': { 'Percent ATK': 0, 'CRIT Rate': 1.0, 'CRIT DMG': 0.5, 'PEN Ratio': 0, 'Energy Regen': 0, 'Impact': 0, 'ATK': 0, 'PEN': 0, 'Anomaly Mastery': 0, 'Anomaly Proficiency': 0, 'Sheer Force': 0.0, 'HP': 1.5, 'Percent HP': 2.0, 'DEF': 0.0, 'Percent DEF': 0.0 },
    'Miyabi': { 'Percent ATK': 1.5, 'CRIT Rate': 2.0, 'CRIT DMG': 2.0, 'PEN Ratio': 1, 'Energy Regen': 0, 'Impact': 0, 'ATK': 1, 'PEN': 1, 'Anomaly Mastery': 0, 'Anomaly Proficiency': 1, 'Sheer Force': 0.0, 'HP': 0.0, 'Percent HP': 0.0, 'DEF': 0.0, 'Percent DEF': 0.0 },
    'Nekomata': { 'Percent ATK': 1.5, 'CRIT Rate': 2.0, 'CRIT DMG': 2.0, 'PEN Ratio': 1, 'Energy Regen': 0, 'Impact': 0, 'ATK': 0.5, 'PEN': 1, 'Anomaly Mastery': 0, 'Anomaly Proficiency': 0, 'Sheer Force': 0.0, 'HP': 0.0, 'Percent HP': 0.0, 'DEF': 0.0, 'Percent DEF': 0.0 },
    'Qingyi': { 'Percent ATK': 1, 'CRIT Rate': 2.0, 'CRIT DMG': 1.5, 'PEN Ratio': 0.5, 'Energy Regen': 0, 'Impact': 0, 'ATK': 0.5, 'PEN': 0.5, 'Anomaly Mastery': 0, 'Anomaly Proficiency': 0, 'Sheer Force': 0.0, 'HP': 0.0, 'Percent HP': 0.0, 'DEF': 0.0, 'Percent DEF': 0.0 },
    'Soldier 11': { 'Percent ATK': 1.5, 'CRIT Rate': 2.0, 'CRIT DMG': 2.0, 'PEN Ratio': 1, 'Energy Regen': 0, 'Impact': 0, 'ATK': 1, 'PEN': 1, 'Anomaly Mastery': 0, 'Anomaly Proficiency': 0, 'Sheer Force': 0.0, 'HP': 0.0, 'Percent HP': 0.0, 'DEF': 0.0, 'Percent DEF': 0.0 },
    'Vivian': { 'Percent ATK': 1, 'CRIT Rate': 0, 'CRIT DMG': 0, 'PEN Ratio': 0.5, 'Energy Regen': 0, 'Impact': 0, 'ATK': 0.5, 'PEN': 0.5, 'Anomaly Mastery': 0, 'Anomaly Proficiency': 2, 'Sheer Force': 0.0, 'HP': 0.0, 'Percent HP': 0.0, 'DEF': 0.0, 'Percent DEF': 0.0 },
    'Anby: Soldier O': { 'Percent ATK': 1.5, 'CRIT Rate': 2.0, 'CRIT DMG': 2.0, 'PEN Ratio': 1, 'Energy Regen': 0, 'Impact': 0, 'ATK': 0.5, 'PEN': 0, 'Anomaly Mastery': 0, 'Anomaly Proficiency': 0, 'Sheer Force': 0.0, 'HP': 0.0, 'Percent HP': 0.0, 'DEF': 0.0, 'Percent DEF': 0.0 },
    'Evelyn': { 'Percent ATK': 1.5, 'CRIT Rate': 2.0, 'CRIT DMG': 2.0, 'PEN Ratio': 1, 'Energy Regen': 0, 'Impact': 0, 'ATK': 0.5, 'PEN': 1, 'Anomaly Mastery': 0, 'Anomaly Proficiency': 0, 'Sheer Force': 0.0, 'HP': 0.0, 'Percent HP': 0.0, 'DEF': 0.0, 'Percent DEF': 0.0 },
    'Hugo': { 'Percent ATK': 1.5, 'CRIT Rate': 2.0, 'CRIT DMG': 2.0, 'PEN Ratio': 0.5, 'Energy Regen': 0, 'Impact': 0, 'ATK': 1, 'PEN': 0.5, 'Anomaly Mastery': 0, 'Anomaly Proficiency': 0, 'Sheer Force': 0.0, 'HP': 0.0, 'Percent HP': 0.0, 'DEF': 0.0, 'Percent DEF': 0.0 },
    'Ju Fufu': { 'Percent ATK': 1.5, 'CRIT Rate': 2.0, 'CRIT DMG': 1.0, 'PEN Ratio': 0.5, 'Energy Regen': 0, 'Impact': 0, 'ATK': 1.5, 'PEN': 0.5, 'Anomaly Mastery': 0, 'Anomaly Proficiency': 0, 'Sheer Force': 0.0, 'HP': 0.0, 'Percent HP': 0.0, 'DEF': 0.0, 'Percent DEF': 0.0 },
    'Orphie & Magus': { 'Percent ATK': 1.5, 'CRIT Rate': 2.0, 'CRIT DMG': 2.0, 'PEN Ratio': 1, 'Energy Regen': 0, 'Impact': 0, 'ATK': 0.5, 'PEN': 1, 'Anomaly Mastery': 0, 'Anomaly Proficiency': 0, 'Sheer Force': 0.0, 'HP': 0.0, 'Percent HP': 0.0, 'DEF': 0.0, 'Percent DEF': 0.0 },
    'Pan Yinhu': { 'Percent ATK': 2, 'CRIT Rate': 1.5, 'CRIT DMG': 1.0, 'PEN Ratio': 1, 'Energy Regen': 0, 'Impact': 0, 'ATK': 2, 'PEN': 1, 'Anomaly Mastery': 0, 'Anomaly Proficiency': 0, 'Sheer Force': 0.0, 'HP': 0.0, 'Percent HP': 0.0, 'DEF': 0.0, 'Percent DEF': 0.0 },
    'Seed': { 'Percent ATK': 1.5, 'CRIT Rate': 2.0, 'CRIT DMG': 2.0, 'PEN Ratio': 1, 'Energy Regen': 0, 'Impact': 0, 'ATK': 0.5, 'PEN': 1, 'Anomaly Mastery': 0, 'Anomaly Proficiency': 0, 'Sheer Force': 0.0, 'HP': 0.0, 'Percent HP': 0.0, 'DEF': 0.0, 'Percent DEF': 0.0 },
    'Trigger': { 'Percent ATK': 1, 'CRIT Rate': 2.0, 'CRIT DMG': 1.5, 'PEN Ratio': 0.5, 'Energy Regen': 0, 'Impact': 0, 'ATK': 0.5, 'PEN': 0.5, 'Anomaly Mastery': 0, 'Anomaly Proficiency': 0, 'Sheer Force': 0.0, 'HP': 0.0, 'Percent HP': 0.0, 'DEF': 0.0, 'Percent DEF': 0.0 },
    'Yanagi': { 'Percent ATK': 1.5, 'CRIT Rate': 0, 'CRIT DMG': 0, 'PEN Ratio': 1, 'Energy Regen': 0, 'Impact': 0, 'ATK': 1, 'PEN': 1, 'Anomaly Mastery': 0, 'Anomaly Proficiency': 2, 'Sheer Force': 0.0, 'HP': 0.0, 'Percent HP': 0.0, 'DEF': 0.0, 'Percent DEF': 0.0 },
    
}


AGENT_METADATA = {

    'Ellen': {'specialty': 'Attack', 'icon_file': 'icon_attack.png'},
    'Grace': {'specialty': 'Anomaly', 'icon_file': 'icon_anomaly.png'},
    'Koleda': {'specialty': 'Stun', 'icon_file': 'icon_stun.png'},
    'Lighter': {'specialty': 'Stun', 'icon_file': 'icon_stun.png'},
    'Lycaon': {'specialty': 'Stun', 'icon_file': 'icon_stun.png'},
    'Rina': {'specialty': 'Support', 'icon_file': 'icon_support.png'},
    'Zhu Yuan': {'specialty': 'Attack', 'icon_file': 'icon_attack.png'},
    'Yidhari': {'specialty': 'Rupture', 'icon_file': 'icon_rupture.png'},
    'Yixuan': {'specialty': 'Rupture', 'icon_file': 'icon_rupture.png'},
    'Yuzuha': {'specialty': 'Support', 'icon_file': 'icon_support.png'},
    

    'Alice': {'specialty': 'Anomaly', 'icon_file': 'icon_anomaly.png'},
    'Anby': {'specialty': 'Stun', 'icon_file': 'icon_stun.png'},
    'Anton': {'specialty': 'Attack', 'icon_file': 'icon_attack.png'},
    'Ben': {'specialty': 'Defense', 'icon_file': 'icon_defense.png'},
    'Billy': {'specialty': 'Attack', 'icon_file': 'icon_attack.png'},
    'Burnice': {'specialty': 'Anomaly', 'icon_file': 'icon_anomaly.png'},
    'Caesar': {'specialty': 'Defense', 'icon_file': 'icon_defense.png'},
    'Corin': {'specialty': 'Attack', 'icon_file': 'icon_attack.png'},
    'Harumasa': {'specialty': 'Attack', 'icon_file': 'icon_attack.png'},
    'Jane': {'specialty': 'Anomaly', 'icon_file': 'icon_anomaly.png'},
    'Lucia': {'specialty': 'Support', 'icon_file': 'icon_support.png'},
    'Lucy': {'specialty': 'Support', 'icon_file': 'icon_support.png'},
    'Manato': {'specialty': 'Rupture', 'icon_file': 'icon_rupture.png'},
    'Miyabi': {'specialty': 'Anomaly', 'icon_file': 'icon_anomaly.png'},
    'Nekomata': {'specialty': 'Attack', 'icon_file': 'icon_attack.png'},
    'Nicole': {'specialty': 'Support', 'icon_file': 'icon_support.png'},
    'Piper': {'specialty': 'Anomaly', 'icon_file': 'icon_anomaly.png'},
    'Pulchra': {'specialty': 'Stun', 'icon_file': 'icon_stun.png'},
    'Qingyi': {'specialty': 'Stun', 'icon_file': 'icon_stun.png'},
    'Seth': {'specialty': 'Defense', 'icon_file': 'icon_defense.png'},
    'Soldier 11': {'specialty': 'Attack', 'icon_file': 'icon_attack.png'},
    'Soukaku': {'specialty': 'Support', 'icon_file': 'icon_support.png'},
    'Vivian': {'specialty': 'Anomaly', 'icon_file': 'icon_anomaly.png'},
    'Anby: Soldier O': {'specialty': 'Attack', 'icon_file': 'icon_attack.png'},
    'Astra Yao': {'specialty': 'Support', 'icon_file': 'icon_support.png'},
    'Banyue': {'specialty': 'Rupture', 'icon_file': 'icon_rupture.png'},
    'Dialyn': {'specialty': 'Stun', 'icon_file': 'icon_stun.png'},
    'Evelyn': {'specialty': 'Attack', 'icon_file': 'icon_attack.png'},
    'Hugo': {'specialty': 'Attack', 'icon_file': 'icon_attack.png'},
    'Ju Fufu': {'specialty': 'Stun', 'icon_file': 'icon_stun.png'},
    'Orphie & Magus': {'specialty': 'Attack', 'icon_file': 'icon_attack.png'},
    'Pan Yinhu': {'specialty': 'Defense', 'icon_file': 'icon_defense.png'},
    'Seed': {'specialty': 'Attack', 'icon_file': 'icon_attack.png'},
    'Trigger': {'specialty': 'Stun', 'icon_file': 'icon_stun.png'},
    'Yanagi': {'specialty': 'Anomaly', 'icon_file': 'icon_anomaly.png'},
    

    'DEFAULT': {'specialty': 'Unknown', 'icon_file': None}
}


RANK_THRESHOLDS = [
    (7.0, 'SS'), (6.0, 'S'), (5.0, 'A'), (4.0, 'B'), (2.0, 'C'),
]

AGENT_RANK_THRESHOLDS = [
    (40, 'SS'), 
    (35, 'S'),  
    (30, 'A'),  
    (24, 'B'),  
    (18, 'C'),  
]

DISK_SET_NAMES = {
    31000: "Thunder-wielding Heavyweight", 31100: "Peacemaker's Provisions",
    31300: "Hot-Blooded Striker", 32200: "Monsoon Mood", 32400: "Twisted Mind",
    32600: "Improvisational Dance", 32700: "Reverberating Metallic",
    33000: "Talon of the Chimera", 33100: "Woodpecker Electro"
}