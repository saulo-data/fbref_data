#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 09:18:27 2022

@author: saulo
"""

#importação das bibliotecas
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#carregamento dos dados dos campeões
urls = [
        'https://fbref.com/en/squads/b8fd03ef/2021-2022/matchlogs/s11160/schedule/Manchester-City-Scores-and-Fixtures-Premier-League#matchlogs_for', 
        'https://fbref.com/en/squads/53a2f082/2021-2022/matchlogs/s11174/schedule/Real-Madrid-Scores-and-Fixtures-La-Liga#matchlogs_for', 
        'https://fbref.com/en/squads/054efa67/2021-2022/matchlogs/s11193/schedule/Bayern-Munich-Scores-and-Fixtures-Bundesliga#matchlogs_for', 
        'https://fbref.com/en/squads/dc56fe14/2021-2022/matchlogs/s11222/schedule/Milan-Scores-and-Fixtures-Serie-A#matchlogs_for', 
        'https://fbref.com/en/squads/e2d8892c/2021-2022/matchlogs/s11183/schedule/Paris-Saint-Germain-Scores-and-Fixtures-Ligue-1#matchlogs_for'
        ]

teams = ['Man City', 'Real Madrid', 'Bayern Munich', 'Milan', 'Paris SG']

dfs_list = []
for url, team in zip(urls, teams):
    df = pd.read_html(url)[0]
    df['team'] = team
    dfs_list.append(df)

dfs = pd.concat(dfs_list)
dfs = dfs[['team', 'xG', 'Poss', 'Result', 'Venue']]
dfs[['xG', 'Poss']] = dfs[['xG', 'Poss']].apply(pd.to_numeric)


#configuração da aparência dos gráficos
sns.set_theme('notebook')
sns.set_style('whitegrid')
title = 'Relação entre xG e Posse de Bola dos campeões das cinco maiores ligas da Europa | Fonte: FBRef.com | @saulo_foot'
palette = ['lightblue', 'lightgray', 'red', 'black', 'purple']

#plotagem
g = sns.FacetGrid(data=dfs, col='team', hue='team', row='Venue', 
                  sharex=False, sharey=False, xlim=(-1, 6), ylim=(20, 90), palette=palette)
g.map(sns.kdeplot, 'xG', 'Poss', alpha=0.8, fill=True)
g.fig.subplots_adjust(top=0.85)
g.fig.suptitle(title)
g.set_titles(col_template='{col_name}', row_template='{row_name}')
sns.despine()
plt.show()
    