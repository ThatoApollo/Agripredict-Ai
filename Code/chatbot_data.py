"""Example questions and predefined answers; farming information is separate from model outputs."""

FALLBACK = 'I could not confidently match that question to a supported topic. Ask one question about AgriPredict, its data, results, units, production scenarios or a supported maize topic. I cannot forecast prices or weather, diagnose crop problems or give field-specific prescriptions.'

# These short phrases lose their meaning when English stop words are removed.
ASSISTANT_HELP_QUESTIONS = [
    'what can you do',
    'what can you not do',
    'what are your limitations',
    'tell me your limitations',
    'what is your purpose',
]

INTENTS = {
    'assistant_help': {
        'examples': [
            'what is this chatbot for',
            'what is the purpose of the chatbot',
            'what can the assistant help me with',
            'what questions can i ask you',
            'what topics can you answer',
            'what are your abilities',
            'explain your capabilities',
            'how do i use this chatbot',
            'can you calculate my yield',
            'can the chatbot make predictions',
            'do you remember previous questions',
            'can you remember our conversation',
            'are your replies generated or prepared',
            'can you browse the internet',
            'are you able to search online',
            'what are the limits of this assistant',
        ],
        'answer': (
            'I explain AgriPredict, its dataset, yield inputs, units, recorded results '
            'and planning scenarios, and provide prepared information on supported maize topics. '
            'Ask one question at a time. My replies come from prepared information; '
            'I may not recognise every wording. I handle each question independently, '
            'even though the chat history remains visible. I do not browse the internet '
            'or calculate field yield estimates: use the dashboard form for those. '
            'I cannot forecast weather, prices or income, diagnose crop problems, '
            'prescribe treatments or guarantee a harvest. Ask a local agricultural '
            'adviser for field-specific guidance.'
        ),
    },
    'annual_yield_trends': {
        'examples': [
            'explain the annual yield chart',
            'what do the mean and median lines show',
            'how did maize yield change over time',
            'why did yield increase in 2017',
            'why did yield decrease in 2018',
            'why is the mean higher than the median',
            'what could explain the annual yield changes',
            'does the chart follow the same farms',
            'what is the difference between mean and median yield',
            'explain the yield trend from 2016 to 2020',
            'what does the historical yield graph mean',
            'did maize production increase over time',
        ],
        'answer': (
            'The chart shows recorded yield per hectare, not total maize production. '
            'Mean yield is the arithmetic average; median yield is the middle value '
            'when yields are ordered. Mean yields were 2.633, 3.400, 3.095, 2.957 '
            'and 3.064 tonnes per hectare from 2016 to 2020 respectively. '
            'The mean rose in 2017, fell in 2018 and 2019, then rose slightly in 2020. '
            'The median was below the mean in every year, consistent with higher-yield '
            'observations pulling the mean upwards. This does not by itself describe '
            'the whole distribution. Weather, management and differences in the fields '
            'and locations sampled could contribute to annual changes, but this '
            'analysis does not establish their causes. These are sample summaries, '
            'not national averages or a history of the same farms. Five annual points '
            'do not establish a reliable long-term trend or seasonal pattern.'
        ),
    },
    'about_project': {
        'examples': [
            'what is agripredict',
            'what does this system do',
            'tell me about this project',
            'what is this dashboard for',
            'who is this tool for',
            'what is the purpose of this app',
            'explain the project',
            'what problem does agripredict solve',
            'who should use this',
        ],
        'answer': 'AgriPredict AI is a student prototype for experimental maize yield estimates using Kenyan field observations from 2016–2020. It supports discussion of harvest, storage and transport scenarios. It does not guarantee a harvest.',
    },
    'how_estimate': {
        'examples': [
            'how does the yield estimate work',
            'how is the yield predicted',
            'how do i get an estimate',
            'what inputs do i enter',
            'how do i use the estimate tab',
            'what does the model use to predict yield',
            'how is the estimate calculated',
            'which model makes the prediction',
            'how do i estimate my yield',
        ],
        'answer': 'The main model is multiple linear regression. Its seven inputs are latitude, longitude, elevation, soil clay, soil pH, soil organic carbon and whether hybrid seed was used. It returns yield in tonnes per hectare. Enter the field details in the dashboard and press Estimate yield. The text assistant itself does not calculate a field estimate.',
    },
    'prediction_timing': {
        'examples': [
            'when is the prediction made',
            'what is the prediction time',
            'does it use rainfall',
            'does the model use weather',
            'why is weather not used',
            'what information is known at planting',
            'which inputs are allowed',
            'why not use fertiliser amounts',
            'does it use future information',
            'is this a forecast at planting',
        ],
        'answer': 'The proposed estimate is at planting time, using location, elevation, soil information and hybrid status. Actual full-season rainfall, harvest measurements and reported crop problems are excluded. Planting date and reported seasonal fertiliser totals are also excluded from the current model. Practical availability of equivalent soil information remains an assumption.',
    },
    'data_source': {
        'examples': [
            'what data was used',
            'where does the data come from',
            'which dataset is this',
            'how many records are there',
            'what years does the data cover',
            'which country is the data from',
            'tell me about the dataset',
            'who collected the data',
            'is this data from south africa',
        ],
        'answer': 'The project uses 7,258 Kenyan field observations from 2016–2020 in the One Acre Fund dataset published on Zenodo. These are not verified unique farms. Yield was measured in two randomly placed 36 square metre sampling plots per field, then supplied in kg/ha and converted to tonnes/ha. Source: https://zenodo.org/records/11122388',
    },
    'units': {
        'examples': [
            'what are the units',
            'what is a tonne per hectare',
            'is the estimate per hectare or total',
            'what does t/ha mean',
            'what unit is the yield in',
            'yield versus production difference',
            'is this the total harvest',
            'kilograms or tonnes',
        ],
        'answer': 'Yield is in tonnes per hectare (t/ha): how much maize one hectare produces. Production is the total for a whole field, calculated as yield (t/ha) multiplied by the area in hectares. The source data stores yield in kg/ha and the project divides it by 1,000.',
    },
    'production_scenario': {
        'examples': [
            'how is production calculated',
            'how do i calculate total harvest',
            'what is the production scenario',
            'how many tonnes will my field produce',
            'calculate production for my area',
            'multiply by hectares',
            'how do i plan storage volume',
            'is production the same as cooperative deliveries',
        ],
        'answer': 'Multiply yield in tonnes per hectare by a compatible field area in hectares. For example, an assumed 3 t/ha over 2 hectares gives a 6-tonne scenario. This is not a guaranteed harvest or expected cooperative delivery. MAE is an average error, not a prediction interval. This assistant explains the calculation but does not calculate a new field forecast.',
    },
    'performance': {
        'examples': [
            'how accurate is the model',
            'what is the model performance',
            'how good are the predictions',
            'what is the mae',
            'what is the rmse',
            'does the model beat the baseline',
            'model accuracy',
            'how big are the errors',
            'show me the results',
            'which model performed best',
            'what is the average error of the predictions',
            'how far off are the estimates',
            'what are the test scores',
        ],
        # Fixed historical results for the current dataset and modelling procedure.
        # Update these scores after changing the data, split or model.
        'answer': (
            'Recorded 2020 errors, in tonnes per hectare: '
            'Linear regression: MAE 1.258, RMSE 1.653. '
            'Historical baseline: MAE 1.206, RMSE 1.540. '
            'The historical baseline had lower recorded MAE and RMSE than linear regression. '
            'Lower values mean smaller prediction errors; these are not accuracy percentages. '
            'Linear regression was adopted for simplicity after test results were known. '
            'These fixed historical scores are not a new independent test or a guarantee '
            'for another field.'
        ),
    },
    'error_meaning': {
        'examples': [
            'explain mae',
            'explain the mae error',
            'what does mae mean',
            'explain rmse',
            'what is mean absolute error',
            'what is root mean squared error',
            'how do i read the error numbers',
            'what is the baseline',
            'what is a historical mean baseline',
            'how is the baseline calculated',
        ],
        'answer': 'MAE is the average absolute prediction error in tonnes per hectare. RMSE gives more weight to large errors. Lower values mean smaller errors. Our historical baseline predicts the fitting records’ mean yield for every field. It uses 2016–2018 for validation and 2016–2019 for the 2020 comparison.',
    },
    'limitations': {
        'examples': [
            'what are the limitations',
            'can i trust the estimate',
            'is the prediction guaranteed',
            'will i get this harvest',
            'how reliable is this',
            'what are the risks of using this',
            'is it accurate for my farm',
            'does it work for every region',
            'what can go wrong',
        ],
        'answer': "Treat the estimate as a rough planning figure, not a promise. It is based on Kenyan survey fields from 2016 to 2020, it does not know the coming season's weather, and individual fields vary a lot around the average. Different years also contain different sampled fields, so patterns between years should not be read as proven cause and effect.",
    },
    'neural_network': {
        'examples': [
            'what is the neural network',
            'do you use deep learning',
            'tell me about the neural network',
            'is there an ai model',
            'what is mlp',
            'how does the neural network perform',
            'why is the neural network not used',
            'what machine learning algorithms are used',
        ],
        'answer': 'Linear regression is the selected yield prediction algorithm. It was adopted for simplicity after the test results were known. It combines the seven inputs in a straightforward calculation that is easier to explain and maintain. This choice does not establish that it is the most accurate option or guarantee future performance. The algorithm selection documentation will explain the alternatives and trade-offs.',
    },
    'planting_timing_advice': {
        'examples': [
            'when should i plant maize',
            'what is the best planting date',
            'does planting date matter',
            'should i plant early',
            'when do i plant before the rains',
            'best time to sow maize',
        ],
        'answer': 'This prototype cannot recommend a planting date. Ask a local agricultural adviser for guidance suited to your area and variety. Planting date is not an input to our current yield model.',
    },
    'soil_acidity': {
        'examples': [
            'does soil ph matter',
            'what is a good soil ph for maize',
            'should i apply lime',
            'what if my soil is acidic',
            'how does soil affect yield',
            'what soil is best for maize',
            'how much lime do i need',
            'is lime good for maize',
            'what is liming',
        ],
        'answer': 'Soil tests can help identify acidity and nutrient needs. Ask a local agricultural adviser to interpret a suitable test before deciding on lime. AgriPredict uses soil pH as an input but cannot prescribe a lime rate. General reference: https://www.farmafrica.org/wp-content/uploads/2025/11/Farm-Africa-Maize-Production-Training-Manual.pdf',
    },
    'seed_variety': {
        'examples': [
            'should i use hybrid seed',
            'what is a hybrid maize',
            'how do i choose a maize variety',
            'what does maturity mean for maize',
            'what is a three way hybrid',
            'do hybrids yield more',
        ],
        'answer': 'Choose a variety suited to local conditions and the intended use, with advice from a local adviser or seed supplier. Our model records only whether hybrid seed was used; it does not compare named varieties or prove that hybrid seed causes higher yield. General reference: https://www.organic-africa.net/fileadmin/organic-africa/documents/training-manual/chapter-09/Africa_Manual_M09-2.pdf',
    },
    'fertiliser': {
        'examples': [
            'how much fertiliser should i apply',
            'what fertiliser rate do i use',
            'how much nitrogen for maize',
            'should i use compost or manure',
            'what fertiliser is best',
            'fertilizer recommendation',
            'how much fertilizer per hectare',
            'how much fertilizer do i apply',
            'what fertilizer rate for maize',
        ],
        'answer': 'AgriPredict does not prescribe fertiliser rates. A soil test and local agricultural advice can inform nutrient decisions. Reported seasonal fertiliser totals are excluded because we have not established what amount was known at planting. General reference: https://www.farmafrica.org/wp-content/uploads/2025/11/Farm-Africa-Maize-Production-Training-Manual.pdf',
    },
    'pests_disease': {
        'examples': [
            'my maize leaves are yellow',
            'what pest is eating my maize',
            'how do i treat maize disease',
            'what pesticide should i use',
            'there are insects on my crop',
            'diagnose my crop problem',
            'fall armyworm control',
            'what is wrong with my plants',
        ],
        'answer': 'I cannot diagnose crop problems or recommend chemicals from a description. Please show the plants to a local agricultural extension officer or agronomist. In this project pest and disease records are reported later in the season, so they are not used in the planting-time estimate.',
    },
    'storage_harvest': {
        'examples': [
            'how should i plan storage',
            'how do i store maize',
            'how much storage space do i need',
            'transport planning for harvest',
            'when should i harvest',
            'how do i plan labour for harvest',
            'how do i dry maize grain',
        ],
        'answer': 'Yield multiplied by field area gives a production scenario that can support storage and transport discussions. Storage arrangements and drying methods need local guidance. This assistant cannot determine storage dimensions or guarantee a harvest. General reference: https://www.fao.org/4/x0530e/x0530e05.htm',
    },
    'out_of_scope': {
        'examples': [
            'what will the maize price be',
            'predict maize prices',
            'what is the weather forecast',
            'will it rain this season',
            'can you predict south african yields',
            'estimate yield for free state',
            'what about wheat',
            'can you predict other crops',
            'how much money will i make',
            'when will the cooperative deliveries arrive',
            'what will maize cost next month',
            'what is the weather like in another city',
            'weather forecast for tomorrow',
            'what is the rainfall forecast',
        ],
        'answer': 'That is outside what this prototype covers. It does not forecast prices, weather or income, it does not cover crops other than maize, and it was built on Kenyan records so it should not be used for South African provinces. It also cannot estimate cooperative deliveries.',
    },
}
