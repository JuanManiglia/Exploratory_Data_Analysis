import itertools
from typing import Counter
import pandas as pd
from SRC.UTILS.Librerias import *     
from SRC.UTILS.Path import anime, chrome, img
class Csv:

    def __init__(self,csv):
        self.csv = csv

    def invocar_dataset(path):
        df = pd.read_csv(anime)
        return df

    def guardar_dataset(df,nombre):
        df.to_csv(nombre, index=False )

    def mostrar_df(df):
        return df.head()

    def rename(df,col1,nombre):
        df.rename(columns={col1: nombre}, inplace=True)
        return df

    def order_for(df,col1, asc=True):
        df = df.sort_values(col1,ascending=asc)
        return df    

    def delete_colunms(df, lista):
        if type(lista) == list:
            for i in lista:
                df = df.drop(i, axis=1)
        else:
            df = df.drop(lista, axis=1)
        return df
    
    def delete_rows(df, lista):
        for i in lista:
            df = df.drop(i)
        return df

    def delete_unknown(df,lista):#################################
        for i in lista:
            unknown = df[ df[i] == 'Unknown' ].index
            df = df.drop(unknown , inplace=True)
        return df
    
    def delete_unknown2(df):
        Unknown = df[ df['Ranked'] == 'Unknown' ].index
        df.drop(Unknown , inplace=True)
        Unknown = df[ df['Rating'] == 'Unknown'].index
        df.drop(Unknown, inplace=True)
        Unknown = df[ df['Score'] == 'Unknown'].index
        df.drop(Unknown, inplace=True)
        Unknown = df[ df['Studios'] == 'Unknown'].index
        df.drop(Unknown, inplace=True)
        return df
    
    def delete_specific_type(df,lista):#############################
        for i in lista:
            specific = df[ df['Type'] == i ].index
            df = df.drop(specific , inplace=True)
        return df
    
    def delete_specific_type2(df):
        Special = df[ df['Type'] == 'Special' ].index
        df.drop(Special , inplace=True)
        ONA = df[ df['Type'] == 'ONA'].index
        df.drop(ONA, inplace=True)
        Music = df[ df['Type'] == 'Music'].index
        df.drop(Music, inplace=True)
        return df    
    
    # def convert_to_float(df,columna):
    #     for x,y in enumerate(df[columna]): no funcionan asi que uso .astype
    #         if type(y) == str:
    #             df[columna][x] = float(y)
    #     return df
    
    # def convert_to_int(df,columna):
    #     for x,y in enumerate(df[columna]):
    #         if type(y) == str:
    #             df[columna][x] = int(y)
    #         else:
    #             df[columna][x] = int(y)
    #     return df

    def aired_to_year(df,columna):
        lista = []
        for i in df[columna]:
            lista.append(i+'\n')
        dates = []
        for x in df[columna]:
            if 'to' in x:
                dates.append(x.split(R' to'))
            else:
                dates.append(x)
        Year_aired = []
        for y in dates:
            if isinstance(y, list):
                from_value = y[0]
                Year_aired.append(from_value)
            elif isinstance(y, str):
                from_value = y
                Year_aired.append(from_value)
        df['Year_Aired'] = Year_aired
        return df
        
    def only_year (df,columna):
        lista_year = []
        for i in df[columna]:
            if ',' in i:
                lista_year.append(i.split(R', '))
            else:
                lista_year.append(i)
        Year = []
        for x in lista_year:
            try:
                if isinstance(x, list):
                    from_value = int(x[1])
                    Year.append(from_value)
                elif isinstance(x, str):
                    from_value = int(x)
                    Year.append(from_value)
            except:
                Year.append('Unknown')
        df['Year'] = Year
        return df
    
    def agrupar_por_suma(df,col1):
        df = df.groupby([col1]).sum()
        return df

    def agrupar_por_count(df,col1,nombre):
        df = pd.DataFrame(df.groupby(col1)[col1].count().rename(nombre))
        df = df.sort_values(nombre,ascending=False)
        return df

    def agrupar_por_promedio(df,col1):
        df = df.groupby([col1]).mean()
        return df      

    def agrupar_genero(df,col1):
        lista = []
        lista_2 = []
        lista_final = []
        for i in df[col1]:
            lista.append(i)
        for x in lista:
            lista_2.append(x.split(','))
        text = "" 
        for row in lista_2: 
            for word in row : 
                text = text + " " + word
        return text

    # def filter_Year(df,col1,year):
    #     df[df[col1] > year]

    def generos(df):
        generos = df['Genres'].apply(lambda x: x.split(', ')).values.tolist()
        Genres = itertools.chain(*generos) # toma una serie de iterables y devuelve un iterable
        genres_cantidad = Counter(Genres) # cuenta la cantidad de elementos

        df_genres = pd.DataFrame.from_dict(genres_cantidad, orient='index').reset_index()
        df_genres.columns = ['Genres', 'Count']
        df_genres = df_genres.sort_values('Count', ascending=False)
        return df_genres

    def side_by_side(*args,titles=cycle([''])):
        html_str=''
        for df,title in zip(args, chain(titles,cycle(['</br>'])) ):
            html_str+='<th style="text-align:center"><td style="vertical-align:top">'
            html_str+=f'<h2>{title}</h2>'
            html_str+=df.to_html().replace('table','table style="display:inline"')
            html_str+='</td></th>'
        display_html(html_str,raw=True)

    def super_animes(df):
        anime_mas_mean = df['Score'].mean()
        anime_mas_vistos = df['Watched'].max()*.70

        df = df[(df['Score'] >= anime_mas_mean) & (df['Watched'] >= anime_mas_vistos)].sort_values('Ranked')
        return df

    def mi_df(df,lista):
        df = df[df.Name.isin(lista)]
        return df

    def gusto(df,df2):
        if df['Score'].describe()[1] < df2['Score'].describe()[1]:
            x = 'Tienes Buen Gusto'
        else:
            x ='Que Gusto más Malo'
        # print(x)
        return x



class Plot:

    def __init__(self,df):
        self.df = df

    def mapa_calor(df):
        plt.figure(figsize=(10,10))
        sns.heatmap(df.corr(),vmin=-1, vmax=1, square=True, 
                    cmap=sns.diverging_palette(220, 20, s=85, 
                    l=25, n=100), annot= True, linewidths= .3);

    def hist(df,col1,key):
        plt.figure(figsize=(10,5))
        if len(df[key].unique()) == 3:
            sns.histplot(data=df, x=col1, hue=key, bins=50, kde=True, 
            element='step', palette=['#e28743','#21130d','#2596be'])
            plt.show();
        else:
            sns.histplot(data=df, x=col1, hue=key, bins=50, kde=True, 
            element='step')
            plt.show();

    def box(df,coly,colx):
        plt.figure(figsize=(10,5))
        sns.boxplot(data = df,
                    y = coly,
                    x = colx);
        plt.xticks(rotation=-15);

    def linea_sombra(df, coly, colx):
        plt.figure(figsize=(10,5))
        sns.regplot(x=df[colx], y=df[coly], 
                    line_kws={"color":'#e28743',"alpha":0.7,"lw":5})
        plt.show()

    def regplot(df,col1):
        plt.figure(figsize=(25,5))
        sns.regplot(x=df.index, y=df[col1], line_kws={"color":"orange","alpha":0.7,"lw":5})
        plt.grid(True)
        plt.xticks(rotation=-45)
        plt.show();

    def scatter(df,col1):
        trace1 = go.Scatter(
                    x = df.index,
                    y = df[col1],
                    name = 'Name',
                    mode= 'lines+markers',
                    marker = dict(color = '#e28743'))

        data = [trace1]

        layout = dict(title = 'Relacion Year ' + col1,
             xaxis= dict(title= 'Year',ticklen= 5)
           )

        fig = go.Figure(data = data, layout=layout)

        iplot(fig)

    def scatter_sin_group(df,col1,col2):
        trace1 = go.Scatter(
                    x = df[col1],
                    y = df[col2],
                    name = 'Name',
                    mode= 'lines+markers',
                    marker = dict(color = '#e28743'))

        data = [trace1]

        layout = dict(title = 'Relacion ' + col1 + col2,
             xaxis= dict(title= 'Year',ticklen= 5)
           )

        fig = go.Figure(data = data, layout=layout)

        iplot(fig)

    def palabras(lista):
        plt.subplots(figsize=(10,10))
        wordcloud = WordCloud(
                          background_color='white',
                          width=512,
                          height=384
                         ).generate(lista)
        plt.imshow(wordcloud)
        plt.axis('off')
        plt.show();

    def palabras_2(dicc):
        plt.subplots(figsize=(10,10))
        wc = WordCloud(width=1024, height=768, background_color='white', max_font_size=400, random_state=50)
        # Del diccionario de frecuencia
        wc.generate_from_frequencies(dicc)
        plt.imshow(wc)
        plt.axis('off')
        plt.show();



    def barras(df, col1, col2):
        plt.figure(figsize=(9,12))
        sns.barplot(x=df[col1], y=df[col2])
        plt.xticks(rotation=-90)
    
    def barras_index(df, col1):
        plt.figure(figsize=(16,9))
        total = float(len(df))
        ax = sns.barplot(x=df.index, y=df[col1])
        for p in ax.patches:
            height = p.get_height()
            ax.text(p.get_x()+p.get_width()/2.,
                height + 3,
                '{:1.2f}'.format(height),
                ha="center")
        plt.xticks(rotation=-90)




class Trans:

    def reescalado(df,col1,col2):
        std_scale = preprocessing.StandardScaler().fit(df[[col1, 
                                                    col2]])
        df_std = std_scale.transform(df[[col1, col2]])
        return df_std

class Webscraping:

    def screenshot(lista):
        for i in lista:

            driver = webdriver.Chrome(chrome)
            # driver = webdriver.Chrome(R'..\SRC\UTILS\chromedriver.exe')
            driver.get('https://www.google.es/imghp?hl=es-419&ogbl')
        
            WebDriverWait(driver, 2)\
                .until(EC.element_to_be_clickable((By.XPATH,
                                            '/html/body/div[2]/div[1]/div[3]/span/div/div/div[3]/button[2]/div')))\
                .click()

            time.sleep(3)

            box = driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/form/div[1]/div[1]/div[1]/div/div[2]/input')
            box.send_keys(i+' anime cover')
            box.send_keys(Keys.ENTER)

            for a in range(1, 2):
                try:
                    driver.find_element_by_xpath('//*[@id="islrg"]/div[1]/div['+str(a)+']/a[1]/div[1]/img').screenshot(R'..\SRC\UTILS\imagenes\image.('+str(i)+').png')
                except:
                    pass
            driver.close();



