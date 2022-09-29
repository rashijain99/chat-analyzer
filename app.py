import streamlit as st
from preprocessor import preprocess
from func import fetch_stats, most_busy_users, create_wordcloud, most_common_words, emoji_counter, monthly_timeline, daily_timeline, mostbusy_day, mostbusy_month, activity_heatmap
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data  = bytes_data.decode("utf-8")
    # st.text(data)
    df = preprocess(data)

    # st.dataframe(df)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notifications')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)


    # stats area
    if st.sidebar.button("Show Analysis"):
        num_messages , words , num_media , links= fetch_stats(selected_user , df)
        st.header("Top Statistics")
        col1 , col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media)
        with col4:
            st.header("Links Shared")
            st.title(links)    

     
    # Monthly Timeline
    st.header("Monthly Timeline") 
    timeline = monthly_timeline(selected_user, df)
    col1 , col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots()
        ax.plot(timeline['time'],timeline['message'] , color='purple')
        plt.xticks(rotation ='vertical')
        st.pyplot(fig)
    with col2:
        fig, ax = plt.subplots()
        width = 0.75
        ax.barh(timeline['time'],timeline['message'], width, color = "orange")
        for i, v in enumerate(timeline['message']):
            ax.text(v + 3, i + .25, str(v), color = 'red', fontweight = 'bold')
        st.pyplot(fig)


    # Daily Timeline
    st.header("Daily Timeline") 
    day_timeline = daily_timeline(selected_user, df)
    fig, ax = plt.subplots()
    ax.plot(day_timeline['only_date'],day_timeline['message'] , color='brown')
    plt.xticks(rotation ='vertical')
    st.pyplot(fig)


    st.title("Activity Map")
    col1 , col2 = st.columns(2)
    with col1:
        # Monthly Activity Map
        st.header("Most Busy Month") 
        month_name_count  = mostbusy_month(selected_user, df)
        fig, ax = plt.subplots()
        width = 0.75
        ax.barh(month_name_count['month_name'], month_name_count['month_count'], width, color = "lightgreen")
        for i, v in enumerate(month_name_count['month_count']):
            ax.text(v + 3, i + .25, str(v),color = 'green', fontweight = 'bold')
        st.pyplot(fig)

    with col2:
        # Weekly Activity Map
        st.header("Most Busy Day") 
        day_name_count  = mostbusy_day(selected_user, df)
        fig, ax = plt.subplots()
        width = 0.75
        ax.barh(day_name_count['day_name'] , day_name_count['day_count'], width, color = "skyblue")
        for i, v in enumerate(day_name_count['day_count']):
            ax.text(v + 3, i + .25, str(v),color = 'blue', fontweight = 'bold')
        st.pyplot(fig)
    
    # Activity Heatmap
    st.title("Weekly Activity Map")
    user_heatmap = activity_heatmap(selected_user,df)
    fig, ax = plt.subplots()
    ax = sns.heatmap(user_heatmap)
    st.pyplot(fig)
    
    
    

    # finding the busiest users in the group level
    if selected_user == 'Overall': 
        st.header("Most Busy Users")
        x , new_df2= most_busy_users(df)
        fig, ax = plt.subplots()
        col1 , col2 = st.columns(2) 
        with col1:
           ax.bar(x.index, x.values , color='purple')
           plt.xticks(rotation ='vertical')
           st.pyplot(fig)
        with col2:
            st.header("Users Contribution")
            st.dataframe(new_df2)   


    # wordcloud       
    st.header("Word Cloud")
    df_wc = create_wordcloud(selected_user, df)
    fig, ax = plt.subplots()
    plt.imshow(df_wc)
    st.pyplot(fig)


    # most common words
    st.header("Most Common Words")
    most_common_df = most_common_words(selected_user,df) 
    fig, ax = plt.subplots()
    ax.barh(most_common_df[0],most_common_df[1], color= "gray")
    plt.xticks(rotation ='vertical')
    st.pyplot(fig)


    # emoji analysis
    st.header("Emoji Analysis")
    emoji_count = emoji_counter(selected_user,df)
    col1 , col2 = st.columns(2) 
    with col1:
        st.dataframe(emoji_count)
    with col2:
        fig, ax = plt.subplots()
        ax.pie(emoji_count[1].head(8), labels = emoji_count[0].head(8),autopct='%1.1f%%')
        st.pyplot(fig)
                 

    
    
            





