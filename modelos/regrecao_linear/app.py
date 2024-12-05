
import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression


df = pd.read_csv('pizzas.csv')

X = df[['diametro']]
y = df[['preco']]

modelo = LinearRegression()

modelo.fit(X, y)

st.title('Previsão de preço de pizzas')

diametro = st.number_input('Qual o diâmetro da pizza?')

if diametro:
    preco = modelo.predict([[diametro]])[0][0]

    st.write(f'O diametro da pizza é {diametro} e o preço é  R$ {preco:.2f}')