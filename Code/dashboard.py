"""Run from the project root: python -m streamlit run Code/dashboard.py"""
import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

import chatbot
import settings
from preparation import load_data

st.set_page_config(page_title='AgriPredict AI', page_icon='🌽', layout='wide')


@st.cache_resource
def assistant_model():
    return chatbot.build_classifier()


try:
    data = load_data()
except (OSError, ValueError, TypeError) as error:
    st.error('The field records could not be opened. Please ask the person managing this app to check the dataset.')
    st.stop()

# Use the same earlier records used to calculate the saved model's baseline.
training_history = data[data['year'] < settings.TEST_YEAR]
historical_baseline = float(training_history[settings.TARGET].mean())
model_path = settings.PROJECT_DIR / 'Results' / 'yield_model.joblib'
model_bundle = None
try:
    # Only load the locally generated, trusted project artifact.
    model_bundle = joblib.load(model_path)
    if model_bundle['selected_model'] != 'Linear regression':
        model_bundle = None
    elif model_bundle['features'] != settings.FEATURES:
        model_bundle = None
    elif model_bundle['unit'] != settings.UNIT:
        model_bundle = None
    elif not np.isclose(model_bundle['historical_baseline_mean'], historical_baseline):
        model_bundle = None
except Exception:
    model_bundle = None

st.title('🌿 AgriPredict AI · Maize harvest planning')
with st.container(border=True, key='overview'):
    st.subheader('Maize field overview')
    origin_column, observation_column, years_column, latest_year_column = st.columns(4)
    with origin_column:
        with st.container(border=True):
            st.metric('Origin', 'Kenya')
    with observation_column:
        with st.container(border=True):
            st.metric('Field observations', f'{len(data):,}')
    with years_column:
        with st.container(border=True):
            st.metric('Years covered', str(data['year'].nunique()))
    with latest_year_column:
        with st.container(border=True):
            st.metric('Latest recorded year', str(int(data['year'].max())))

input_column, result_column = st.columns([1.18, 1], gap='small')
with input_column:
    with st.container(border=True, height='stretch', key='field-panel'):
        st.subheader('Estimate your yield')
        st.caption('Use comparable soil measurements. Unknown details should not be guessed.')
        with st.form('field_details', border=False):
            left_input_column, right_input_column = st.columns(2)
            with left_input_column:
                latitude = st.number_input('Latitude', min_value=-90.0, max_value=90.0,
                    value=None, placeholder='e.g. -1.2864',
                    format='%.3f', help='Your field’s north–south position in decimal degrees.', key='latitude')
                elevation = st.number_input('Height above sea level (metres)', value=None,
                    min_value=0.0, step=1.0, placeholder='e.g. 1200', key='elevation')
                clay = st.number_input('Clay in the soil (%)', min_value=0.0, max_value=100.0,
                    value=None, placeholder='e.g. 25', key='clay')
            with right_input_column:
                longitude = st.number_input('Longitude', min_value=-180.0, max_value=180.0,
                    value=None, placeholder='e.g. 36.8172',
                    format='%.3f', help='Your field’s east–west position in decimal degrees.', key='longitude')
                soil_ph = st.number_input('Soil pH', min_value=0.0, max_value=14.0,
                    value=None, placeholder='e.g. 5.6',
                    help='A measure of how acidic or alkaline the soil is.', key='ph')
                organic_carbon = st.number_input('Organic carbon in the soil (g/kg)', min_value=0.0,
                    value=None, placeholder='e.g. 8.4',
                    help='Use the organic carbon value, not an organic matter percentage.', key='carbon')
            hybrid = st.selectbox('Was commercial hybrid seed used?', ['Yes', 'No'], index=None,
                placeholder='Choose an answer', key='hybrid')
            submitted = st.form_submit_button('Estimate yield', type='primary', width='stretch')
        if submitted:
            # Clear the previous estimate even if this submission is invalid.
            st.session_state.pop('estimate', None)
            # Keep this order aligned with settings.FEATURES and the saved model.
            numeric_inputs = [latitude, longitude, elevation, clay, soil_ph, organic_carbon]
            if any(value is None for value in numeric_inputs) or hybrid is None:
                st.warning('Please complete all field details before requesting an estimate.')
            elif model_bundle is None:
                st.error('The saved prediction model is unavailable. Please ask the person managing this app to restore it.')
            else:
                prediction_inputs = pd.DataFrame([numeric_inputs + [1 if hybrid == 'Yes' else 0]], columns=settings.FEATURES)
                out_of_range_features = []
                for feature in settings.FEATURES:
                    value = prediction_inputs.iloc[0][feature]
                    if value < training_history[feature].min() or value > training_history[feature].max():
                        out_of_range_features.append(feature)
                if out_of_range_features:
                    st.warning('Some details fall outside the values in the earlier field records. This prototype cannot provide a supported estimate for these details.')
                else:
                    try:
                        predicted_yield = float(model_bundle['estimator'].predict(prediction_inputs)[0])
                        if not np.isfinite(predicted_yield) or predicted_yield < 0:
                            raise ValueError('Unsupported yield output')
                        st.session_state['estimate'] = {'yield': predicted_yield,
                            'inputs': prediction_inputs.iloc[0].to_dict()}
                    except Exception:
                        st.error('An estimate could not be calculated for these details. Please ask the person managing this app to check the model.')

estimate = st.session_state.get('estimate')
with result_column:
    with st.container(border=True, key='yield-panel'):
        st.subheader('Your estimated yield')
        with st.container(border=True, key='yield-result'):
            if estimate is None:
                st.metric('Yield per hectare', '— t/ha')
                st.caption('Submit your field details to see an estimate.')
            else:
                st.metric('Yield estimate', f"{estimate['yield']:.2f} t/ha")
                st.caption('Based on your last submitted details. Press Estimate yield again after making changes.')
        st.caption('An early estimate using the sampled Kenyan conditions. It does not know the coming season’s weather or guarantee a harvest.')
        if model_bundle is None:
            st.warning('Yield estimates are currently unavailable. Past records and saved results can still be viewed.')
    with st.container(border=True, height='stretch', key='scenario-panel'):
        st.subheader('Planning scenario')
        area = st.number_input('Enter planted area (hectares)', min_value=0.0, max_value=10000000.0,
            value=None, step=0.5, key='area')
        if area is not None and estimate is not None:
            production = estimate['yield'] * area
            st.metric('Estimated production for this scenario', f'{production:,.0f} tonnes')
        else:
            st.metric('Estimated production for this scenario', '— tonnes')
            if estimate is None:
                st.caption('Submit your field details to calculate production.')
            else:
                st.caption('Enter planted area to calculate production.')

with st.container(border=True, height='stretch', key='chart-panel'):
    st.subheader('Recorded yield over time')
    annual_yields = data.groupby('year')[settings.TARGET].agg(['mean', 'median'])

    figure, axes = plt.subplots(figsize=(7, 3.8))
    axes.plot(annual_yields.index, annual_yields['mean'], marker='o',
            color='#168345', label='Mean yield')
    axes.plot(annual_yields.index, annual_yields['median'], marker='s',
            color='#7a8eae', label='Median yield')
    axes.set_xticks(annual_yields.index)
    axes.set_ylim(bottom=0)
    axes.set_ylabel('Yield (t/ha)')
    axes.set_xlabel('Year')
    axes.legend(loc='upper center', bbox_to_anchor=(0.5, -0.22), ncol=2, frameon=False)
    axes.grid(alpha=0.15)
    axes.spines['top'].set_visible(False)
    axes.spines['right'].set_visible(False)
    figure.tight_layout()
    st.pyplot(figure)
    plt.close(figure)

    st.caption(
        'Mean: The average yield for each year, calculated by adding all '
        'recorded yields and dividing by the number of observations.'
    )
    st.caption(
        'Median: The central yield for each year. After sorting yields from '
        'lowest to highest, it is the middle value—or the average of the '
        'two middle values.'
    )
    st.caption(
        'Chart purpose: Compare average and central yields across 2016–2020 '
        'to see how yields varied in the sampled Kenyan fields. Different '
        'fields may be included each year; the chart does not represent '
        'national averages or predict future yields.'
    )

with st.container(border=True, key='assistant-panel'):
    st.subheader('AgriPredict Assistant')
    st.caption('Ask one question about this project, its results or a supported maize topic. Ask “What can you do?” for help. Replies come from prepared information; each question is handled on its own.')
    if 'messages' not in st.session_state:
        st.session_state['messages'] = [{'role': 'assistant', 'content': 'Hello! Ask “What can you do?” to see my abilities and limits, or ask about yield estimates, the data, model errors or harvest planning.'}]
    if st.button('Clear chat'):
        st.session_state['messages'] = st.session_state['messages'][:1]
    with st.container(height=150, border=False):
        for message in st.session_state['messages']:
            with st.chat_message(message['role']):
                st.write(message['content'])
    question = st.chat_input('Ask about AgriPredict or maize planning', max_chars=1000)
    if question:
        answer, topic, confidence = chatbot.respond(question, assistant_model())
        st.session_state['messages'].append({'role': 'user', 'content': question})
        st.session_state['messages'].append({'role': 'assistant', 'content': answer})
        st.rerun()
st.caption('Student prototype · Kenyan field records, 2016–2020 · Experimental harvest planning support')
