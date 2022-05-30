#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 30 15:03:08 2022

@author: https://github.com/saulo-data
"""

#importação das bibliotecas
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


#carregamento dos dados
url = 'https://fbref.com/en/comps/Big5/playingtime/players/Big-5-European-Leagues-Stats'
df = pd.read_html(url, header=1)[0]


leagues = {'eng Premier League': 'Premier League', 
          'it Serie A': 'Serie A', 
          'es La Liga': 'La Liga', 
          'fr Ligue 1': 'Ligue 1', 
          'de Bundesliga': 'Bundesliga'}

df.Comp.replace(leagues, inplace=True)

#filtragem dos dados
df1 = df.iloc[:, :6]
df2 = df.iloc[:, 6:].apply(pd.to_numeric, errors='coerce').fillna(0)
df = pd.concat([df1, df2], axis=1)
df.drop('Matches', axis=1, inplace=True)
df = df[df['90s'] >= 15]

#setagem dos estilos dos gráficos
sns.set_theme('notebook')
sns.set_style('white')

#plotagem
plt.figure(figsize=(12, 8))
plt.title('Gols Esperados(xG) e saldo(xG+/-) de Ederson, em campo, no contexto das grandes ligas europeias')
sns.scatterplot(data=df[df.Player != 'Ederson'], x='onxG', y='xG+/-', 
                alpha=0.7, ec='white', s=90, color='lightblue')
sns.scatterplot(data=df[df.Player == 'Ederson'], x='onxG', y='xG+/-', 
                s=180, alpha=0.7, ec='black', color='darkblue')
plt.axvline(x=df.onxG.median(), **{'ls': '-.', 'c': 'black'}, label='Mediana')
plt.axhline(y=df['xG+/-'].median(), **{'ls': '-.', 'c': 'black'})
sns.despine()
text = plt.text(80, 60, 'Ederson')
plt.legend()
plt.show()


