#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 27 10:25:54 2022

@author: saulo
"""

#importação das bibliotecas
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import adjustText

#carregamento dos dados
url = 'https://fbref.com/en/comps/Big5/shooting/players/Big-5-European-Leagues-Stats'
df = pd.read_html(url, header=1)[0]

df0 = df.iloc[:, :6]
df1 = df.iloc[:, 6:].apply(pd.to_numeric, errors='coerce').fillna(0)
df2 = pd.concat([df0, df1], axis=1)

leagues = {'eng Premier League': 'Premier League', 
          'it Serie A': 'Serie A', 
          'es La Liga': 'La Liga', 
          'fr Ligue 1': 'Ligue 1', 
          'de Bundesliga': 'Bundesliga'}
df2.Comp.replace(leagues, inplace=True)

#filtrar jogadores com o mínimo de minutos em campo acima da mediana
mediana_min = df2['90s'].median()
df2 = df2[df2['90s']>mediana_min]

#filtrar jogadores com no mínimo 10 gols
df2 = df2[df2.Gls > 10]

#determinando o padrão de gráfico para as plotagens
sns.set_theme('notebook')
sns.set_style('darkgrid')

#plotagem da distribuição dos gols
plt.figure(figsize=(8,8))
plt.title('Distribuição dos gols nas principais ligas europeias')
sns.boxplot(data=df2, y='Gls')
plt.show()

#plotagem do gráfico npxG Vs np:G-xG
plt.figure(figsize=(15,10))
sns.scatterplot(data=df2, x='npxG', y='np:G-xG', alpha=0.7, size='Gls', sizes=(50, 350), hue='Gls', edgecolor='black', palette='Greens')
sns.despine()
plt.axvline(x=df2['npxG'].median(), **{'ls': '-.', 'c': 'black'}, label='Mediana')
plt.axhline(y=df2['np:G-xG'].median(), **{'ls': '-.', 'c': 'black'})
plt.legend(title='Gols')
plt.title('Relação entre gols e gols esperados(xG) nas principais ligas europeias')
texts = [plt.text(row['npxG'], row['np:G-xG'], f'{row.Player}', fontdict=dict(size=12)) for index, row in df2[df2.Gls >= 20].iterrows()]
adjustText.adjust_text(texts)
plt.show()

#dados dos jogadores com no mínimo 20 gols
df_strikers = df2[df2.Gls >= 20]

#plotagem da distância média de seus arremates
plt.figure(figsize=(15,10))
plt.xticks(rotation='90')
sns.barplot(data=df_strikers.sort_values('Dist'), x='Player', y='Dist', palette='Greens_d')
plt.axhline(y=df_strikers.Dist.median(), **{'ls': '-.', 'c': 'black'}, label='Mediana')
sns.despine()
plt.title('Distância média de chutes dos jogadores que marcaram 20 gols ou mais nas principais ligas europeias')
plt.legend()
plt.show()

#verificando a contribuição de cada jogador com 20 gols ou mais para suas
#respectivas equipes
lista_strikers = [striker for striker in df_strikers.Player]
url2 = 'https://fbref.com/en/comps/Big5/playingtime/players/Big-5-European-Leagues-Stats'
strikers_on_off = pd.read_html(url2, header=1)[0]
strikers_on_off.Comp.replace(leagues, inplace=True)
strikers_on_off = strikers_on_off.rename(columns={'On-Off.1': 'On-Off/xG'})

strikers_on_off = strikers_on_off[strikers_on_off.Player.isin(lista_strikers)]
strikers_on_off0 = strikers_on_off.iloc[:, :6]
strikers_on_off1 = strikers_on_off.iloc[:, 6:].apply(pd.to_numeric, 
                                                     errors='coerce').fillna(0)
strikers_on_off2 = pd.concat([strikers_on_off0, strikers_on_off1], axis=1)
strikers_on_off2['onxG/90'] = np.round(strikers_on_off2['onxG'] 
                                       / strikers_on_off2['MP'], decimals=2)

#plotagem do gráfico On-Off/xG Vs onxG/90
plt.figure(figsize=(15, 10))
sns.scatterplot(data=strikers_on_off2, x='onxG/90', y='On-Off/xG', s=190, hue='Comp')
sns.despine()
plt.title('Contribuição de cada jogador na performance de suas equipes')
texts = [plt.text(row['onxG/90'], row['On-Off/xG'], f'{row.Player}', fontdict={'color': 'darkgreen'}) for index, row in strikers_on_off2.iterrows()]
adjustText.adjust_text(texts)
plt.axhline(y=strikers_on_off2['On-Off/xG'].mean(),  **{'ls': '-.', 'c': 'black'}, label='Média')
plt.axvline(x=strikers_on_off2['onxG/90'].mean(),  **{'ls': '-.', 'c': 'black'})
plt.legend(loc='upper left')
plt.show()

#plotagem do gráfico da influência de seus artilheiros por liga
plt.figure(figsize=(35, 10))
plt.title('Dependência de seus artilheiros por liga')
sns.barplot(data=strikers_on_off2.sort_values('On-Off/xG'), x='Comp',
            y=strikers_on_off2['On-Off/xG'], ci=None, color='g')
sns.despine();