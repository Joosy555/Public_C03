# Import python packages.
import streamlit as st
import requests  
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
# session = get_active_session()

cnx = st.connection("snowflake")
session = cnx.session()

smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")  
#st.text(smoothiefroot_response.json())
sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)

# Write directly to the app.
st.title(f":cup_with_straw: Customize")
st.write(
  """Kies je fruit.
  **And if you're new to Streamlit,** check
  out our easy-to-follow guides at
  [docs.streamlit.io](https://docs.streamlit.io).
  """
)

name_on_order = st.text_input ('Name on Smoothe:')

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
     label = "What are your favorite fruits?"
    ,options = my_dataframe 
    ,max_selections = 5
)


ingredients_string = ''
if ingredients_list:
    #st.write("write:", ingredients_list)
    st.text(ingredients_list)

    for fruits_chosen in ingredients_list:
        ingredients_string += fruits_chosen + ' '

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                    values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    

    time_to_insert = st.button('Submit order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
        

else:
    st.write("Niets geselecteerd")
    
