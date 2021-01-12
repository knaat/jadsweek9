import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set wide page mode
st.set_page_config(layout="wide")

#Read data into a Pandas dataframe and decorate with streamlit cache function to avoid reloading each time script executes:
@st.cache
def load_data():
    data = pd.read_csv('gapminder.csv')
    return data

df = load_data()

# Now start building up teh display with some titles.
st.title('JADS Week 9 -  Visualisation exercises')
st.sidebar.title('Controls sidebar')

# Radio selector to choose between exercises.
exercise = st.sidebar.radio('Exercise', ['Exercise 1', 'Exercise 2', 'Exercise 3'])

exercise1=False
exercise2=False
exercise3=False

if exercise == 'Exercise 1':
    exercise1=True
elif exercise == 'Exercise 2':
    exercise2=True
elif exercise == 'Exercise 3':   
    exercise3=True

if exercise1:

    # Display some headers
    st.header('Exercise 1: data loading & preprocessing')
    st.sidebar.header('Data Selection')

    # Define 2 columns with a dummy 'spacer column for better layout (column object is in beta) 
    c1, dum, c2 = st.beta_columns((10,1,10))

    # Radio selector to switch on/off interactive filtering. Initialised to 'No'.
    filter = st.sidebar.radio('Filter dataframe', ['No', 'Yes'], 0)

    if filter == 'Yes':
        st.sidebar.subheader('Filter on year & continent')
        year = st.sidebar.slider('Year', 1952, 2007, 1952, 5)
        continent = st.sidebar.radio('Continent', list(df['continent'].unique()))

        st.sidebar.subheader('Filter on country')
        countries_sel = st.sidebar.multiselect('Country', tuple(df['country'].unique()))

        if countries_sel == []: 
            df_disp = df[(df['year'] == year) & (df['continent'] == continent)].copy()
            c1.subheader('Data frame filtered on year and continent')

        else:
            df_disp = df[(df['country'].isin(countries_sel))].copy()
            c1.subheader('Data frame filtered on countries')

    else:
        df_disp=df.copy()
        c1.subheader('Unfiltered data frame')

    # Display dataframe with size set in pixels
    c1.dataframe(data=df_disp,width=1024, height=768)

    # Display header and statictics in column #2
    c2.subheader('Dataframe statistics')
    c2.dataframe(df_disp.describe())
    c2.dataframe(df_disp.describe(include='object'))

    # Expander section with some explanation. Press '+' to expand.  
    with st.beta_expander("Documentation", False):
            st.write("""
                The dataframe is by default displayed unfiltered. Select Filter dataframe to apply filters.
                The filtering on year & continent and on country are implemetend to demonstrate some of the filtering options.
                With a slider object min-max filtering can also very easily be implemented. 
                
                The dataframe can be *sorted* per column by clicking on the column header.

                It is worthwhile noting that every action on the controls initiates a rerun of the complete script. 
                Functions decorated with streamlit.cache are not rerun.
        """)

if exercise2:

    # Display some headers
    st.header('Exercise 2: Matplotlib/Seaborn basic workflow')
    st.sidebar.header('Data Selection')

    # Define 2 columns with a dummy 'spacer' column for better layout (column object is in beta) 
    c1, dum, c2 = st.beta_columns((10,1,10))

    # Radio selector to switch on/off interactive filtering. Initialised to 'No'.
    filter = st.sidebar.radio('Filter dataframe', ['No', 'Yes'], 0)

    if filter == 'Yes':
        st.sidebar.subheader('Filter on year & county')
        year = st.sidebar.slider('Year', 1952, 2007, 1952, 5)
        countries_sel = st.sidebar.multiselect('Country', df['country'].unique())
        st.sidebar.write('N.B. All countries assumed when no country selected')

        if countries_sel == []: 
            df_disp = df[(df['year'] == year)].copy()
        else:
            df_disp = df[(df['year'] == year) & (df['country'].isin(countries_sel))].copy()
    else:
        df_disp=df.copy()


    st.sidebar.header('Mapplotlib options')
    # Switch seaborn stylesheet on/off
    style = st.sidebar.radio('Set seaborn stylesheet',['No','Yes'],0)   
    if style == 'Yes':
        plt.style.use('seaborn')
    else:
         plt.style.use('default')

    c1.subheader('Mapplotlib scatter')
    c2.subheader('Seaborn regplot')
    
    #Create a Figure with 1 Axis:
    fig1 = plt.figure(figsize=(8,6))
    ax1 = plt.axes()

    #Create scatter plot of Gapminder data
    ax1.scatter(x=df_disp['gdpPercap'], y=df_disp['lifeExp'])

    #Create line plot with the curve y = 4.95 + 7.2 log(x)
    X = np.linspace(1,50000)  #Creates an array with the numbers [1,2,3,...,50000]
    y = 4.95+7.2*np.log(X)    #Uses the Numpy log() function
    ax1.plot(X,y,'--r')

    ax1.set(xlabel='GDP per capita (USD)', 
        ylabel='Life expectancy',
        title='Gapminder data');

    # Display mapplotlib plot in column1
    c1.pyplot(fig1)

    #Create a Figure with 1 Axis:
    fig2 = plt.figure(figsize=(8,6))
    ax2 = plt.axes()

    #Create scatter plot of Gapminder data
    sns.regplot(data=df_disp, x='gdpPercap', y='lifeExp', logx=True, ax=ax2, line_kws={'color': 'red'})

    ax2.set(xlabel='GDP per capita (USD)', 
        ylabel='Life expectancy',
        title='Gapminder data', 
        xlim=(-5000, 100000),
        ylim=(0,90) );

    c2.pyplot(fig2)

    c1.subheader('Mapplotlib plot')
    c2.subheader('Seaborn lineplot')

    fig3 = plt.figure(figsize=(8,6))
    ax3 = plt.axes()

    for c in ['Nigeria','China','United States','Norway','Netherlands']:
        #For each country c, we select the corresponding rows and plot the GDP over the years
        df_c = df_disp[df_disp['country']==c].copy()   #select rows referring to country == c 
        ax3.plot(df_c['year'],df_c['gdpPercap'], label=c)

    # Plot the legend and titles
    ax3.legend()
    ax3.set(xlabel='Year', 
        ylabel='GDP per capita',
        title='Gapminder data');
    
    # Display mapplotlib plot in column1
    c1.pyplot(fig3)

    fig4 = plt.figure(figsize=(8,6))
    ax4 = plt.axes()
    c=['Nigeria','China','United States','Norway','Netherlands']
    df_c = df_disp[df_disp['country'].isin(c)].copy()   
    sns.lineplot(data=df_c, x=df_c['year'],y=df_c['gdpPercap'], hue='country', ax=ax4)

    ax4.set(xlabel='Year', 
        ylabel='GDP per capita',
        title='Gapminder data');

    c2.pyplot(fig4)

    st.subheader('Mapplotlib 2 sub plots')

    #Create a Figure with two Axes (=subplots):
    fig5, ax5 = plt.subplots(nrows=1, ncols=2, figsize=(16,6))

    #Make scatter plot in ax[0]
    ax5[0].scatter(x=df['gdpPercap'], y=df['lifeExp'])
    ax5[0].set(xlabel='GDP per capita (USD)', ylabel='Life expectancy',title='Gapminder data')

    #In ax[1], make scatter plots for four individual countries, 
    #showing development from 1952 through 2007
    for c in ['China','Nigeria','Norway','United States']:
        df_c=df_disp[df_disp['country']==c]  #select rows referring to country == c
        #scatterplot indicating years by size of dots (small=1952, large=2007) and country by color
        ax5[1].scatter(x=df_c['gdpPercap'],y=df_c['lifeExp'],
                    s=4*(df_c['year']-1947), 
                    alpha=.3,
                    label=c)   #Each scatter plot gets a label containing country name to be used in legend

    ax5[1].set(xlabel='GDP per capita (USD)', yticklabels=[], title='1952 through 2007')

    #Add a legend, which uses the labels given in the ax5[1].scatter command above
    ax5[1].legend(frameon=False, ncol=2);

    st.pyplot(fig5)

    st.subheader('Seaborn 2 sub plots')

    #Create a Figure with two Axes (=subplots):
    fig6, ax6 = plt.subplots(nrows=1, ncols=2, figsize=(16,6))

    #Make scatter plot in ax[0]
    sns.scatterplot(data=df_disp, x='gdpPercap', y='lifeExp', ax=ax6[0])
    ax6[0].set(xlabel='GDP per capita (USD)', ylabel='Life expectancy',title='Gapminder data')

    #In ax6[1], make scatterplot for four individual countries, 
    #showing development from 1952 through 2007
    c=['China','Nigeria','Norway','United States']
    df_c = df_disp[df_disp['country'].isin(c)].copy()   
    sns.scatterplot(data=df_c, x='gdpPercap',y='lifeExp',hue='country', size='year',sizes=(1,200),alpha=.7, ax=ax6[1])
    ax6[1].set(xlabel='GDP per capita (USD)', ylabel='Life expectancy',title='Gapminder data')
    
    st.pyplot(fig6)

if exercise3:

    # Display some headers
    st.header('Exercise 3: Working with multiple (interactive) plots')

    df_disp=df.copy()

    st.sidebar.header('Mapplotlib & data select options')
    # Switch seaborn stylesheet on/off
    style = st.sidebar.radio('Set seaborn stylesheet',['No','Yes'],0)   
    if style == 'Yes':
        plt.style.use('seaborn')
    else:
         plt.style.use('default')

    markercolor = st.sidebar.color_picker('Pick a color of symbols in scatter plot', '#EA7272')
    markeredgecolor = st.sidebar.color_picker('Pick a color for edge of symbols in scatter plot', '#A80303')

    year = st.sidebar.slider('Select the year to select', 1952, 2007, 1952, 5,)
    dfyear = df_disp[df_disp['year'] == year].copy()

    st.subheader('Mapplotlib scatter plots')
    fig7, ax7 = plt.subplots(nrows=1, ncols=2, figsize=(12,4))

    xscale = st.sidebar.radio('Set scale of x-axis to logarithmic',['No','Yes'],0)   
    if xscale == 'Yes':
        ax7[0].set_xscale('log')
    else:
        ax7[0].set_xscale('linear')

    ax7[0].scatter(x=dfyear['gdpPercap'], y=dfyear['lifeExp'], color = markercolor, edgecolors = markeredgecolor )
    ax7[0].set(xlabel='GDP per capita (USD)', ylabel='Life expectancy',title='Year '+str(year))
    if year == 2007:
        #Adding text labels in the graph
        ax7[0].text(42000,67,"Norway\nKuwait\nSingapore",size=10,color='grey');

    for c in ['China','Nigeria','Norway','United States']:
        cdata=df_disp[df_disp['country']==c]  
        ax7[1].scatter(x=cdata['gdpPercap'],y=cdata['lifeExp'],s=4*(cdata['year']-1947), alpha=.3,
                    label=c)   
        #Here, we add the connecting lines:
        ax7[1].plot(cdata['gdpPercap'],cdata['lifeExp'], alpha=.5)
    ax7[1].set(xlabel='GDP per capita (USD)', yticklabels=[], title='1952 through 2007')
    ax7[1].legend(frameon=False, ncol=2)

    # Display 2 mapplotlib sub-plots
    st.pyplot(fig7)

    #Find out 3 countries with biggest GDP
    if year == 2007:
        st.write(dfyear[dfyear['gdpPercap'] > 45000].head())

    #Distribution plots
    fig8, ax8 = plt.subplots(nrows=1, ncols=2, figsize=(12,4))

    #left graph: total distribution (histogram)
    sns.histplot(dfyear['lifeExp'],ax=ax8[0], kde=True)
    ax8[0].set(xlim=(25,95), title='Year '+str(year))

    #right graph: life expectancy per continent (kde-plots)
    for c in dfyear['continent'].unique():
        sns.kdeplot(dfyear[dfyear['continent']==c]['lifeExp'], label=c, x=ax8[1])

    ax8[1].set(ylim=(0,.50),yticks=[],xlim=(25,95),title='Year '+str(year) )
    ax8[1].legend();

    # Display 2 mapplotlib sub-plots
    st.pyplot(fig8)

    # Expander section with some explanation. Press '+' to expand.  
    with st.beta_expander("Documentation", False):
            st.write("""
               Text plotted and dataframe appear when year 2007 is selected. 
        """)