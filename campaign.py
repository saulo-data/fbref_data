#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 10:23:13 2022

@author: https://github.com/saulo-data
"""

#importação das bibliotecas
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from adjustText import adjust_text

#carregamento, limpeza e transformação dos dados
url = 'https://fbref.com/en/comps/Big5/Big-5-European-Leagues-Stats'
current = '2021-2022'
current_season = pd.read_html(url)[0]
current_season['Temporada'] = current
current_season = current_season[current_season.LgRk==1]
teams = [row['Squad'] for index, row in current_season.iterrows()]

last = '2020-2021'
url2 = f'https://fbref.com/en/comps/Big5/{last}/{last}/Big-5-European-Leagues-Stats'
last_season = pd.read_html(url2)[0]
last_season['Temporada'] = '2020-2021'
last_season = last_season[last_season.Squad.isin(teams)]

df = pd.concat([last_season, current_season])
df.rename(columns={'Squad': 'Equipe'}, inplace=True)

#configuração do gráfico
plt.figure(figsize=(17,10))
plt.title('Evolução dos campeões em relação à temporada passada | Fonte: FBRef.com | @saulo_foot', 
          fontdict={'fontweight': 'bold', 'fontsize': 12})
plt.xlabel('Gols Esperados por 90 min', fontdict={'fontweight': 'bold'})
plt.ylabel('Pontos por partida', fontdict={'fontweight': 'bold'})

#plotagem
sns.scatterplot(data=df, x='xGD/90', y='Pts/G', hue='Equipe', 
                palette=['red', 'lightblue', 'green', 'darkblue', 'black'], 
                style='Temporada', s=550,
                alpha=.8, ec='black')

for (index_1, row_1), (index_2, row_2) in zip(df[df.Temporada=='2020-2021'].
                                              sort_values('Equipe').iterrows(), 
                                              df[df.Temporada=='2021-2022'].
                                              sort_values('Equipe').iterrows()):
    plt.quiver(row_1['xGD/90'], row_1['Pts/G'], (row_2['xGD/90']-row_1['xGD/90']), 
              (row_2['Pts/G'] - row_1['Pts/G']), angles='xy', 
              scale_units='xy', scale=1.06, color='black')

plt.show()




