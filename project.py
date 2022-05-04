import streamlit as st
import pandas as pd
import numpy as np
import functions

st.markdown("<h1 style='text-align: center; color: red;'>Safety LA April</h1>", unsafe_allow_html=True)

hide_table_row_index = """
            <style>
            tbody th {display:none}
            .blank {display:none}
            </style>
            """

st.markdown(hide_table_row_index, unsafe_allow_html=True)

zip_list = list(range(90001, 91610+1))
zipcode = str(st.selectbox(
     'Enter Your Zip Code:',
     zip_list))

area = functions.getArea(zipcode)
if area is None: 
	st.error('We do not have case record assiciate with this zip code!')
else:
	st.write('Your zip code ' + zipcode + ' is in ' + area + '.')
	with st.container():
		col1, col2 = st.columns((1, 2))

		with col1:
			safetyIndex = functions.getIndex(area)
			st.metric(label="Safety index", value=safetyIndex)
			st.info('Light crimes are crimes cause no property damage or injury. \nMedium crimes are crimes cause huge property damage and injury. \nSevere crimes are crimes associate with abuse, severe injury even fatality.')

		with col2:
			option = st.radio('What do you want to know?', ('Summary', 'Individual Cases'))
			if option == 'Summary':
				st.write('Summary of crime cases in the area:')
				st.table(functions.getAreaStats(area))
				
			if option == 'Individual Cases':
				number = st.slider("How many cases do you want to view?", min_value = 1, max_value = 50,value = 5)
				st.write('Recent ' + str(number) + ' cases in ' + area + ':')
				st.write('(Click on expand to show all details.)')
				df = functions.getCases(area, number)
				st.dataframe(df)

overview = st.container()
overview.subheader('Overview of Cases Happend in April')
with overview:
	st.dataframe(functions.overview())

with st.sidebar:
	st.write('Report new case:')
	st.info('Please be aware, all the submitted cases need to be verified first. In other word, the submission will NOT impact anything you see on the website immediately.')
	zipcode = str(st.selectbox('Zipcode:', zip_list))
	date = st.number_input('Day of Month', min_value = 1, max_value = 31)
	casetype = st.selectbox('Type of Case: ', functions.crimetypes())
	st.write(' ')
	if st.button('Submit'):
		resp = functions.userUpload(zipcode, date, casetype)
		if resp.status_code == 200:
			st.success('Case submitted!')
		else:
			st.error('Submission failed. Check back later.')

