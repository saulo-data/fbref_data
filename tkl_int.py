#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 31 15:58:35 2022

@author: https://github.com/saulo-data
"""

#importação das bibliotecas
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#carregamento, limpeza e transformação dos dados
url = 'https://fbref.com/en/comps/Big5/defense/players/Big-5-European-Leagues-Stats'
df = pd.read_html(url, header=1)[0]

leagues = {'eng Premier League': 'Premier League', 
          'it Serie A': 'Serie A', 
          'es La Liga': 'La Liga', 
          'fr Ligue 1': 'Ligue 1', 
          'de Bundesliga': 'Bundesliga'}

df.Comp.replace(leagues, inplace=True)
df = df[df.Pos == 'FW']
df[['90s', 'Tkl+Int']] = df[['90s','Tkl+Int']].apply(pd.to_numeric)
df = df[df['90s']>25]
df = df[['Player', 'Comp', 'Tkl+Int']]

#plotagem
sns.set_theme('notebook')
sns.set_style('whitegrid')

plt.figure(figsize=(20, 10))
plt.title('Roubadas de Bola + Interceptações(Tkl+Int) das principais ligas europeias | Fonte: Fbref.com')
g = sns.boxplot(data=df, x='Comp', y='Tkl+Int', linewidth=3, palette='mako')
g.set(xlabel=None)
sns.despine()
plt.show()

