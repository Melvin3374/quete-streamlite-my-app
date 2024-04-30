import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px

st.title('Hello and :orange[Welcome !] :sunglasses:')

st.subheader("Voici un dataset de voitures &mdash;\
            :car:"                   )

link = "https://raw.githubusercontent.com/murpi/wilddata/master/quests/cars.csv"
df = pd.read_csv(link)
df

# drop les valeurs nulles
df.dropna(inplace=True)

# Affichage du sélecteur de continents (pour sélection multiple)
selected_continent = st.radio(":blue[Sélectionnez un continent]", df['continent'].unique())

# Filtrer le DataFrame en fonction du continent sélectionné
filtered_df = df[df['continent'] == selected_continent]



# Heatmap pour voir la corrélation entre les colonnes
st.subheader('Heatmap de corrélation entre les colonnes', divider='rainbow')
df2 = filtered_df.copy()
df2['continent'] = df2['continent'].factorize()[0]
viz_correlation = sns.heatmap(df2.corr(),
                               center=0,
                               cmap=sns.color_palette("vlag", as_cmap=True)
                               )

st.pyplot(viz_correlation.figure)

multi = '''
On peut voir sur la heatmap les éléments corrélés entre eux :
- En rouge les corrélations positives et en bleu les négatives
- Par exemple, le nombre de cylindre et positivement corrélé au cubes ou à la puissance hp, comme au poids du véhicule
- En revanche, la consommaton mpg est inversement proportionnelle (et donc corrélé négativement) au cylndre, la puissance ou le poids

Il est intéressant de voir que le continent est corrélé positivement à la consomation et négativement à au poids.'''
st.markdown(multi)

# Scatter plot
st.subheader('Scatterplot : miles parcourus par galons par rapport à la Puissance de la voiture', divider='rainbow')
fig = px.scatter(filtered_df, x="mpg", y="hp", color="continent",
                 title=f"Nombre de miles parcourus par galons / Puissance en chevaux ({selected_continent})",
                 color_discrete_map={"US": "lightgreen", "Europe": "lightblue", "Japan": "orange"})
fig.update_xaxes(title_text="Consommation (mpg)")
fig.update_yaxes(title_text="Puissance en chevaux (hp)")

st.plotly_chart(fig)
multi = '''Plus les hp sont élevés moins le véhicule a d'autonomie énergétique de plus on peut voir par pays la différence de répartition, notamment le Japon qui est à l'opposé des US.'''
st.markdown(multi)

# Distribution des variablesst.title("Ensemble de subplots pour réprésenter les différente colonnes et leur distribution")
st.subheader('Ensemble de subplots pour réprésenter les différente colonnes et leur distribution', divider='rainbow')
fig, axes = plt.subplots(2, 5, figsize=(15, 8))
fig.suptitle('Distribution des variables', fontsize=10)
fig.tight_layout(pad=3.0)
for i, col in enumerate(df.columns[0:]):
    sns.histplot(filtered_df[col], bins='sturges', kde=True, ax=axes[i // 5, i % 5])
    axes[i // 5, i % 5].set_title(col)
    axes[i // 5, i % 5].set_xlabel('')
    axes[i // 5, i % 5].set_ylabel('')
st.pyplot(fig)

multi = '''Il y a un plus grand nombre de petites cylindrées dans le dataset ce qui implique :
- Plus grand nombre de voitures avec un petit cubage, petit hp, petit poids par rapport aux autres
- En revanche on a une distribution de time-to-60 équilibré ce qui est dur à la forte puissance des voitures plus cylindrées qui vient compenser le plus grand nombre de petites cylindrées.
'''
st.markdown(multi)

# Scatter plot avec facet_col
st.subheader('Scatterplot des cylindrées avec leur cubage par pays', divider='rainbow')
fig4 = px.scatter(filtered_df, x="continent", y="cubicinches", size="cylinders", hover_name="year", facet_col="cylinders", template="plotly_dark")
st.plotly_chart(fig4)
multi = '''
- Les USA ont les voiture qui ont les plus grosses cylindrées et donc avec le plus de cubage
- A l'inverse le Japon a les voitures qui ont les plus petit cylindres donc le plus petit cubage'''
st.markdown(multi)
