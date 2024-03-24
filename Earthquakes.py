import streamlit as st
import plotly.express as px
import pandas as pd
import joblib
import sklearn


st.set_page_config(
    layout="wide",
    page_title='Earthquake analysis',
    page_icon='🪙'
)


df_format = pd.read_csv('cleaned_dff.csv')
mon_highest = df_format.groupby('Month_Name')['Year'].count().sort_values( ascending=False).reset_index().head(10)
df_time = df_format.groupby(['Year','tsunami'])['sig'].count().reset_index().sort_values(by= 'sig')
occu_avg = df_format.groupby(['net','tsunami'])['sig'].size().sort_values(ascending= False).reset_index()
impact = df_format.groupby(['location','nst'])['sig'].size().sort_values(ascending= False).reset_index().head(500)
algorithms = df_format.groupby(['magtype','tsunami'])['sig'].count().sort_values(ascending= False).reset_index()
earthquakes_avg = df_format.groupby(['location','magnitude'])['title'].count().sort_values(ascending= False).reset_index().head(100)
affected = df_format.groupby(['alert','mmi'])['sig'].count().sort_values(ascending= False).reset_index()



model = joblib.load('model.pkl')


df_Preprocess = pd.read_csv('cleaned_df_format.csv')





page =  st.sidebar.radio('Select page', ['About','Univariate', 'Bivariate',
                    'Multivariate Analysis','model for tsunami'])


if page == 'About':
    
    def main():
        
        st.title('  Earthquake from 1995 to 2023')
        
        st.image('5555-5.jpg')
        
        tab1, tab2 = st.tabs(['📈 About',' Earthquake Project'])
        
        with tab2:
            
            col1, col2, col3 = st.columns([100,0.5,6])
            
            with col1:
                
                st.write(df_format)
        with tab1:
            st.write('title : title name given to the earthquake')
            st.write('magnitude :  The magnitude of the earthquake')          
            st.write('date_time :  date and time')
            st.write('cdi :  The maximum reported intensity for the event range')
            st.write ('mmi :  The maximum estimated instrumental intensity for the event')
            st.write('alert :  The alert level - “green”, “yellow”, “orange”, and “red”')
            st.write('tsunami :  "1" for events in oceanic regions and "0" otherwise')
            st.write('sig :  A number describing how significant the event is. Larger numbers indicate a more significant event. ')
            st.write('net :  The ID of a data contributor. Identifies the network considered to be the preferred source of information')
            st.write('nst :  The total number of seismic stations used to determine earthquake location.')
            st.write('dmin :  Horizontal distance from the epicenter to the nearest station')
            st.write('gap :  The largest azimuthal gap between azimuthally adjacent stations (in degrees). ')
            st.write('magType :  The method or algorithm used to calculate the preferred magnitude for the event')
            st.write('depth :  The depth where the earthquake begins to rupture')
            st.write('latitude  / longitude :  coordinate system by means of which the position or location of any place on Earth')
            st.write('location :  location within the country')
            st.write( 'continent :  continent of the earthquake hit country')
            st.write('country :  affected country')
                
            
        
    if __name__ == '__main__':

        main()
        
if page == 'Univariate':

    def main():
        
        st.title(' Univariate Analysis for earthquake')
    
        # create tabs of numerical and categorical features
        tab1, tab2 = st.tabs(['Numerical Features', 'Categorical Features'])
        
        # Numerical Features
        num_cols = df_format.select_dtypes(exclude= 'object').columns
        
        for col in num_cols:
            tab1.plotly_chart(px.histogram(df_format, x = col))
            
        # Categorical features
        cat_cols = df_format.select_dtypes(include= 'object').columns
        
        for col in cat_cols:
            tab2.plotly_chart(px.histogram(df_format, x = col))
            
            
    if __name__ == '__main__':

        main()
    
elif page == 'Bivariate':
    
    def main():
        
        st.title(' Bivariate Analysis for earthquake')
        
        st.header(' features VS Target Variable (title)')
        
        
        select_col = st.selectbox('Select Feature', ['magnitude', 'mmi',  'sig', 'nst','Year','alert','magtype'])
        
        select_plot = st.selectbox('Select Plot Type', ['Box plot', 'Violin Plot', 'Bar Chart Plot'])
        
        if select_plot == 'Box plot':
            
            st.plotly_chart(px.box(df_format, x= 'title', y= select_col))
            
        elif select_plot == 'Violin Plot':
            
            st.plotly_chart(px.violin(df_format, x= 'title', y= select_col))

        else:
            
            st.plotly_chart(px.bar(df_format, x= 'title', y= select_col))
            
        st.title(' relationship between all the data') 
        
        st.plotly_chart(px.imshow(df_format.corr(), text_auto=True, width=1000, height=900))    
        
    if __name__ == '__main__':

        main()
        
        
elif page == 'Multivariate Analysis':
    
    def main():
        
        st.header('1- The most common alert and its impact on the event?') 
        
        st.plotly_chart(px.scatter(df_format, x='alert' , y='sig',  color='tsunami',title='RelationShip between sig  vs alert'))
        
        st.header('2- The months that witness the most earthquakes')
        
        st.plotly_chart(px.pie(mon_highest, names='Month_Name', values='Year',color='Month_Name'))   
        
        st.header('3- Is there a change in the intensity of earthquakes over time? Is there any effect of a tsunami?')
        
        st.plotly_chart( px.line(df_time, x= 'sig', y= ['Year'],  color= 'tsunami', title= 'Total earthquakes & tsunami over Time Period (1995-2023)'))
        
        st.header('4- What is the most media coverage of the event?')
        
        st.plotly_chart(px.bar(occu_avg, x= 'net', y= 'sig',color='tsunami'))
        
        st.header('5-The impact of earthquake prediction stations on the residential area')
        
        st.plotly_chart(px.bar(impact, x= 'location', y= 'sig',color='nst'))
        
        st.header('6- impact of algorithms on event importance')
        
        st.plotly_chart(px.bar(algorithms, x= 'magtype', y= 'sig', color= 'tsunami' ))
        
        st.header('7- How many earthquakes have occurred and what is the strength of the earthquake?')
        
        st.plotly_chart(px.bar(earthquakes_avg, x= 'location', y= 'title', color= 'magnitude'))
        
        st.header('8- What is the alert rate affected by the event?')
        
        st.plotly_chart(px.bar(affected, x= 'alert', y= 'sig',color= 'mmi'))
        
        

      
    if __name__ == '__main__':
        
        main()

        
if page == 'model for tsunami':
    

    def main():

        st.title('tsunami based on data')
        
        magnitude = st.selectbox('magnitude', df_Preprocess.magnitude.unique())
        location = st.selectbox('location', df_Preprocess.location.unique())
        magtype = st.selectbox('magtype', df_Preprocess.magtype.unique())
        cdi = st.slider('cdi', min_value = 0, max_value = 9, value = 3, step = 1)
        mmi = st.slider('mmi', min_value = 1, max_value = 10, value = 1, step = 1)
        dmin = st.slider('dmin', min_value = 0, max_value = 4, value = 0, step = 1)
        gap = st.slider('gap', min_value = 0, max_value = 72, value = 20, step = 5)
        depth = st.slider('depth',min_value = 0, max_value = 114, value = 3, step = 5)
        nst = st.number_input('nst', min_value = 48 , max_value = 900, value = 50, step = 10)
        sig = st.slider('sig', min_value = 650, max_value = 1150, value = 700, step = 10)
        
        
# Data Format

        data = {
            'cdi': cdi,
            'mmi': mmi,
            'dmin': dmin,
            'gap': gap,
            'depth': depth,
            'sig': sig,
            'magnitude' : magnitude,
            'nst': nst,
            'magtype': magtype,
            'location': location}

        model = joblib.load('model.pkl')
        pred = model.predict(pd.DataFrame(data, index=[0]))
        if st.button('Predict'):
            if pred == 0:
                st.error('Not tsunami')
            else:
                st.success('yes tsunami')

    if __name__ == '__main__':

        main()
