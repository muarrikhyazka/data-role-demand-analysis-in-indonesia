import pandas as pd
import streamlit as st
from PIL import Image
from bokeh.models.widgets import Div
import plotly.express as px
import base64
import nltk
nltk.download('punkt')
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
import webbrowser


title = 'Data Role Demand Analysis In Indonesia'




# Layout
img = Image.open('assets/icon_pink-01.png')
st.set_page_config(page_title=title, page_icon=img, layout='wide')






st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.center {
  display: block;
  margin-left: auto;
  margin-right: auto;
#   width: 50%;
}
</style> """, unsafe_allow_html=True)


padding = 0
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)

file_name='style.css'
with open(file_name) as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)






# Content
@st.cache
def load_data():
    df_raw = pd.read_csv(r'data/LinkedinScrape_Data_Indonesia_.csv', sep=';')
    df = df_raw.copy()
    return df_raw, df

df_raw, df = load_data()
df_merged = df_raw.copy()

def render_svg(svg):
    """Renders the given svg string."""
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s" class="center" width="100" height="100"/>' % b64
    st.write(html, unsafe_allow_html=True)


# Sidebar color
st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #ef4da0;
    }
</style>
""", unsafe_allow_html=True)

def redirect(_url):
    link = ''
    st.markdown(link, unsafe_allow_html=True)


with st.sidebar:
    f = open("assets/icon-01.svg","r")
    lines = f.readlines()
    line_string=''.join(lines)

    render_svg(line_string)

    st.write('\n')
    st.write('\n')
    st.write('\n')

    if st.button('🏠 HOME'):
        js = "window.location.href = 'https://muarrikhyazka.github.io'"  # Current tab
        html = '<img src onerror="{}">'.format(js)
        div = Div(text=html)
        st.bokeh_chart(div)

    if st.button('🍱 GITHUB'):
        # js = "window.location.href = 'https://www.github.com/muarrikhyazka'"  # Current tab
        js = "window.open('https://www.github.com/muarrikhyazka')"
        html = '<img src onerror="{}">'.format(js)
        div = Div(text=html)
        st.bokeh_chart(div)
        # redirect('https://www.github.com/muarrikhyazka')
        # webbrowser.open('https://www.github.com/muarrikhyazka')








st.title(title)


st.subheader('Business Understanding')
st.write(
    """
    As we know, start from 2020 data role are being popular and hype. Many companies open job opportunity on data role, many courses about data coming up. Now the question is, on 2023 are data role still popular and needed anymore? Thats why I do this project for clarity. Beside that, I also want to know what skill which is needed most on companies.
    """
)


st.subheader('Data Understanding')
st.write(
    """
    I scraped data from linkedin website with 'Data' keyword and region boundary only on Indonesia. I did this on April 14th 2023.
    """
)


st.dataframe(df.sample(5))



st.subheader('Exploratory Data Analysis')

df_location = df.groupby('Location')['Date'].count().reset_index()
df_location.columns = ['Location', 'Count']
fig_1 = px.bar(df_location.sort_values(by = 'Count', ascending = False), x='Location', y="Count", barmode="group", text='Count')
fig_1.update_traces(textposition="outside")
st.plotly_chart(fig_1, use_container_width=True)

st.write(
    """
    Mostly companies which are needed data person are in Jakarta. Many data job are in big cities in Java. Outside of Java only 2 jobs. There is big gap here.
    """
)

df_type = df.groupby('Type')['Date'].count().reset_index()
df_type.columns = ['Type', 'Count']
fig_2 = px.bar(df_type.sort_values(by = 'Count', ascending = False).iloc[:10], x='Type', y="Count", barmode="group", text='Count')
fig_2.update_traces(textposition="outside")
st.plotly_chart(fig_2, use_container_width=True)

st.write(
    """
    Of course mostly on fulltime. For college student who need internship, there are many available opportunities here.
    """
)

df_level = df.groupby('Level')['Date'].count().reset_index()
df_level.columns = ['Level', 'Count']
fig_3 = px.bar(df_level.sort_values(by = 'Count', ascending = False), x='Level', y="Count", barmode="group", text='Count')
fig_3.update_traces(textposition="outside")
st.plotly_chart(fig_3, use_container_width=True)

st.write(
    """
    Its a good news for freshgradutes because there are so many opportunities for them on entry level. This role is still much needed as well on mid-senior level.
    """
)


df_industry = df.groupby('Industry')['Date'].count().reset_index()
df_industry.columns = ['Industry', 'Count']
fig_4 = px.bar(df_industry.sort_values(by = 'Count', ascending = False).iloc[:10], x='Industry', y="Count", barmode="group", text='Count')
fig_4.update_traces(textposition="outside")
st.plotly_chart(fig_4, use_container_width=True)

st.write(
    """
    Still dominated by IT industry.
    """
)

df_company = df.groupby('Company')['Date'].count().reset_index()
df_company.columns = ['Company', 'Count']
fig_5 = px.bar(df_company.sort_values(by = 'Count', ascending = False).iloc[:10], x='Company', y="Count", barmode="group", text='Count')
fig_5.update_traces(textposition="outside")
st.plotly_chart(fig_5, use_container_width=True)

st.write(
    """
    Here they shown by company, just as reference for jobseeker. In average, per company needs 2 data role.
    """
)


st.write(
    """
    \n
    \n
    \n
    I did analysis on job description text to know what skills and characteristics mostly needed by companies, so it can be guides for jobseekers.
    """
)

st.write(
    """
    \n
    \n

    First of all, I did text preprocessing. Below is the details :
    \n1. Convert to lowercase and clean punctuations, characters, and whitespaces
    \n2. Tokenization : Split the text by word
    \n3. Remove Stopwords : Stopword is meaningless word and not importance word such as 'and', 'or', 'which', etc. Thats why we dont need it and remove it. Here used stopwords from nltk library
    \n4. Stemming : Remove -ing, -ly, etc. 
    \n5. Lemmatisation : Convert the word into root word.
    """
)


@st.cache
def load_data_text():
    df_desc_clean = pd.read_csv(r'data/df_description_clean.csv', sep=';')
    return df_desc_clean

df_desc_clean = load_data_text()

def show_word_freq(df, text_column):
    ## convert to corpus
    top=20
    corpus = df[text_column]
    lst_tokens = nltk.tokenize.word_tokenize(corpus.str.cat(sep=" "))


    fig, ax = plt.subplots(nrows=1, ncols=2)
    fig.suptitle("Most frequent words", fontsize=15)
    fig.set_size_inches(18.5, 10.5)
        
    ## calculate words unigrams
    dic_words_freq = nltk.FreqDist(lst_tokens)
    dtf_uni = pd.DataFrame(dic_words_freq.most_common(), 
                        columns=["Word","Freq"])
    dtf_uni.set_index("Word").iloc[:top,:].sort_values(by="Freq").plot(
                    kind="barh", title="Unigrams", ax=ax[0], 
                    legend=False).grid(axis='x')
    ax[0].set(ylabel=None)
        
    ## calculate words bigrams
    dic_words_freq = nltk.FreqDist(nltk.ngrams(lst_tokens, 2))
    dtf_bi = pd.DataFrame(dic_words_freq.most_common(), 
                        columns=["Word","Freq"])
    dtf_bi["Word"] = dtf_bi["Word"].apply(lambda x: " ".join(
                    string for string in x) )
    dtf_bi.set_index("Word").iloc[:top,:].sort_values(by="Freq").plot(
                    kind="barh", title="Bigrams", ax=ax[1],
                    legend=False).grid(axis='x')
    ax[1].set(ylabel=None)
    return fig

text_chart = show_word_freq(df_desc_clean, 'Description Clean')
st.pyplot(text_chart.figure)


st.write(
    """
    From the charts above, we can know that skills and characteristics mostly needed by companies are :
    \n1. Bachelor Degree.
    \n2. Data Analysis Skill.
    \n3. Communication Skill.
    \n4. Analytical Skill.
    \n5. Attention Detail.
    \n6. Data Visualization.
    \n7. Project Management.
    \n8. Machine Learning.
    """
)





c1, c2 = st.columns(2)
with c1:
    st.info('**[Github Repo](https://github.com/muarrikhyazka/data-role-demand-analysis-in-indonesia)**', icon="🍣")

