"""Supported example questions and reviewed, general-purpose responses."""
TOPICS = {
    "platform": (
        ["how do i use agripredict", "what does the dashboard show", "how do i choose a province", "what can this platform do"],
        "AgriPredict supports provincial maize planning for Free State, Mpumalanga and North West. "
        "The dashboard is still being developed. The completed scripts provide historical trends and model comparisons. "
        "Ask about data, model performance, limitations or general maize farming."
    ),
    "estimate": (
        ["what is the yield estimate", "predict maize yield for free state", "what is the forecast for mpumalanga", "expected yield for north west"],
        "I cannot calculate a new yield estimate in this chat. The current scripts evaluate historical seasons; "
        "a current-season forecast is not yet connected. Yield is measured in tonnes per planted hectare and represents a provincial average."
    ),
    "performance": (
        ["how accurate are the models", "what are the mae and rmse results", "which model performed best", "show model performance"],
        "Model scores are not currently available. Run Code/yield_model.py to generate Results/model_metrics.csv. "
        "MAE and RMSE measure prediction error; lower values are better."
    ),
    "data": (
        ["where does the data come from", "what dataset was used", "what dataset did you use", "how many seasons and records", "what weather inputs are used"],
        "The prepared dataset has 72 records across three provinces and 24 seasons, 2000/01–2023/24. "
        "Inputs include October–December rainfall, January rainfall and October–January mean temperature. "
        "Weather represents an equal average of three sample points per province. Consult Data_summary.md for source details."
    ),
    "limitations": (
        ["what are the limitations", "can you guarantee the harvest", "is this a prediction for my farm", "can i trust the estimates"],
        "The dataset is small, and provincial averages cannot predict an individual farm's harvest. "
        "Model errors and simplified weather representation limit confidence. Results support planning scenarios and do not guarantee a harvest."
    ),
    "storage": (
        ["how do i plan storage capacity", "how do i calculate production volume", "help with maize procurement planning", "convert yield to tonnes"],
        "For a scenario, multiply yield in tonnes per planted hectare by assumed planted hectares to obtain tonnes. "
        "Keep the area basis consistent. A cooperative must also estimate what share it will actually receive; "
        "provincial production is not the same as deliveries to its stores. This chat does not calculate a live storage requirement."
    ),
    "planting": (
        ["when should i plant maize", "what is the best maize planting date", "how deep should i plant maize seed", "what affects maize planting time"],
        "Maize planting decisions depend on local rainfall, soil moisture and temperature, and the chosen cultivar. "
        "Use district guidance and cultivar recommendations to choose dates and depth. A single planting schedule will not suit every field."
    ),
    "soil": (
        ["how do i prepare soil for maize", "should i take a soil sample", "how do i test soil acidity", "do i need lime for my soil"],
        "A soil test helps establish acidity and nutrient status before deciding on lime or fertiliser. "
        "Follow the laboratory's sampling instructions and discuss the results with a local adviser. "
        "Seedbed preparation should suit the soil and tillage system."
    ),
    "irrigation": (
        ["how much water does maize need", "when should i irrigate maize", "how do i schedule irrigation", "how does rainfall affect crop water needs"],
        "Crop water needs vary with growth stage, weather and soil conditions. "
        "Check soil moisture and recent rainfall before setting irrigation amounts or timing. "
        "This assistant cannot determine a field-specific irrigation schedule."
    ),
    "fertiliser": (
        ["how much fertiliser should i apply", "when should i top dress maize", "how do i decide nutrient rates", "what fertiliser does maize need"],
        "Base nutrient rates on soil test results and a realistic yield target. "
        "Application timing depends on crop needs, soil and expected rainfall. "
        "Ask a local agronomist to interpret the results and recommend rates for your field."
    ),
    "rotation": (
        ["what is crop rotation", "should i rotate maize with legumes", "what crop should follow maize", "why alternate maize and soybean"],
        "Crop rotation grows different crops in sequence on the same land. "
        "Maize–legume rotations can support soil fertility management. Choose a rotation that suits local growing conditions and your market."
    ),
    "crop_stress": (
        ["why are maize leaves turning yellow", "what causes stunted maize plants", "my maize is wilting", "my maize is not growing well"],
        "I cannot diagnose crop stress from a short description. Note the affected growth stage, "
        "whether damage is patchy or widespread, recent weather and any inputs applied. "
        "Ask a local extension officer or agronomist to inspect the crop before choosing treatment."
    ),
    "pests": (
        ["what insect is eating maize", "there are holes in maize leaves", "worms in my maize cobs", "how do i identify a maize pest"],
        "Pest identification needs more evidence than a chat description. "
        "Record where damage occurs, how many plants are affected and what insects are present. "
        "Use clear photographs or a sample to obtain local identification before considering treatment. "
        "I do not recommend pesticide products or doses."
    ),
    "disease": (
        ["what disease causes maize leaf marks", "maize leaves have rust spots", "is this a fungal disease", "how do i identify maize disease"],
        "Leaf marks alone do not confirm a disease. Record how symptoms spread and which leaves are affected, "
        "and ask an extension officer or plant specialist to examine the plants. "
        "I cannot confirm a diagnosis or prescribe a chemical treatment."
    ),
}
