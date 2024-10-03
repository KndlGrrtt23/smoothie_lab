# Import python packages
import streamlit as st
import requests
#from snowflake.snowpark.context import get_active_session #removed to added in CNX = st.connection("Snowflake") below##
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie! 
 More streamlit documentation here: 
[docs.streamlit.io](https://docs.streamlit.io).
    """
)

name_on_order = st.text_input('Name on Smoothie')
st.write('The name of your smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
   #session = get_active_session() ##This was in original streamlit code##
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)


ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe 
    , max_selections=5
    )


if ingredients_list: 
    ingredients_string = ''
    
    for fruit_chosen in ingredients_list: 
        ingredients_string += fruit_chosen + ' '

    st.write(ingredients_string)
    
    my_insert_stmt = """ insert into SMOOTHIES.PUBLIC.ORDERS(INGREDIENTS, NAME_ON_ORDER)
            values ('""" + ingredients_string + """','"""+name_on_order+ """')"""
    
    st.write(my_insert_stmt)
   # st.stop() #kills streamlit function
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
       
        st.success('Your Smoothie is ordered!', icon="✅")


fruityvice_response = request.get("https://fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_response)
