import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

uploaded_file = st.file_uploader('Upload a CSV file', type='csv')
if uploaded_file:    
    #Read data into a Pandas dataframe
    #df = pd.read_csv('gapminder.csv')

    df = pd.read_csv(uploaded_file)

    df2007 = df[df['year']==2007].copy()
    df1952 = df[df['year']==1952].copy()

    fig, ax = plt.subplots(nrows=1, ncols=4, figsize=(32,6))

    #Create scatter plot of Gapminder data and fit linear function
    sns.regplot(data=df2007, x='gdpPercap', y='lifeExp', order=1, ax=ax[0], line_kws={'color': 'red'})

    ax[0].set(xlabel='GDP per capita (USD)', 
            ylabel='Life expectancy',
            title='Linear fit', 
            xlim=(-5000, 100000),
            ylim=(0,90) );

    #Create scatter plot of Gapminder data and fit logarithmic function
    sns.regplot(data=df2007, x='gdpPercap', y='lifeExp', order=2, ax=ax[1], line_kws={'color': 'red'})

    ax[1].set(xlabel='GDP per capita (USD)', 
            ylabel='Life expectancy',
            title='2nd Order polynomial fit', 
            xlim=(-5000, 100000),
            ylim=(0,90) );

   #Create scatter plot of Gapminder data and fit logarithmic function
    sns.regplot(data=df2007, x='gdpPercap', y='lifeExp', order=3, ax=ax[2], line_kws={'color': 'red'})

    ax[2].set(xlabel='GDP per capita (USD)', 
            ylabel='Life expectancy',
            title='3rd Order polynomial fit', 
            xlim=(-5000, 100000),
            ylim=(0,90) );

    #Create scatter plot of Gapminder data and fit logarithmic function
    sns.regplot(data=df2007, x='gdpPercap', y='lifeExp', logx=True, ax=ax[3], line_kws={'color': 'red'})

    ax[3].set(xlabel='GDP per capita (USD)', 
            ylabel='Life expectancy',
            title='Logarithmic fit', 
            xlim=(-5000, 100000),
            ylim=(0,90) );

    plot = st.pyplot(fig)
