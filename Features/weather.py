import locale
import requests
import random
import warnings
warnings.simplefilter('ignore')

# Constants
URL = 'https://wttr.in/{loc}?{fore}{metric}{col}AF&lang={lang}&format={format}'
ERR_MSG = 'Error: could not reach the service. Status code: {}.'
CONN_ERR = 'Error: connection not available.'
FORECAST_HELP = 'Shows also the forecasts for today and tomorrow.'
METRIC_HELP = 'Use the International System of Units.'
USCS_HELP = 'Use the United States Customary Units.'
LANG_HELP = 'Choose preferred language. ISO 639-1 code.'
COLORS_HELP = 'Keep or remove terminal sequences for colors. Default is keep.'
ONELINE_HELP = 'Shorter summary that fits in one line and uses emojis.'

def default_lang():
    """
    Gets default language ISO 639-1 code.
    """
    return locale.getdefaultlocale()[0][:2]

def get_weather_data(location='', forecast=False, metric='m', language=default_lang(), colors=True, forMat='', formattingBool=False):
    """
    Retrieve weather data using the wttr.in API.

    Args:
        location (str): Location for weather forecast.
        forecast (bool): Whether to include forecasts for today and tomorrow.
        metric (str): Specify the units system: 'm' for International System of Units, 'u' for United States Customary Units.
        language (str): Preferred language ISO 639-1 code.
        colors (bool): Whether to include terminal sequences for colors.
        one_line (bool): Whether to generate a shorter summary that fits in one line and uses emojis.
        format (str): The way you get your results in : j1 for json, v2 for data rich o/p, empty for for ascii o/p, %m for moon phase. Turn formattingBool True to enable this.

    Returns:
        str: Weather data fetched from the API.
    """
    url = URL.format(
        loc=location,
        fore='2' if forecast else '0',
        metric=metric if metric is not None else '',
        lang=language,
        col='' if colors else 'T',
        format=forMat if formattingBool else 'j1'
    )
    try:
        response = requests.get(url)
        if response.ok:
            weather_data = response.json()
            # return response.text
            return {
                "current_condition": {
                    "Temperature (Celsius)": weather_data['current_condition'][0]['temp_C'],
                    "Temperature (Fahrenheit)": weather_data['current_condition'][0]['temp_F'],
                    "Feels Like (Celsius)": weather_data['current_condition'][0]['FeelsLikeC'],
                    "Feels Like (Fahrenheit)": weather_data['current_condition'][0]['FeelsLikeF'],
                    "Cloud Cover (%)": weather_data['current_condition'][0]['cloudcover'],
                    "Humidity (%)": weather_data['current_condition'][0]['humidity'],
                    "Observation Time": weather_data['current_condition'][0]['localObsDateTime'],
                    "Precipitation (mm)": weather_data['current_condition'][0]['precipMM'],
                    "Precipitation (inches)": weather_data['current_condition'][0]['precipInches'],
                    "Pressure (mb)": weather_data['current_condition'][0]['pressure'],
                    "Pressure (inches)": weather_data['current_condition'][0]['pressureInches'],
                    "UV Index": weather_data['current_condition'][0]['uvIndex'],
                    "Visibility (km)": weather_data['current_condition'][0]['visibility'],
                    "Visibility (miles)": weather_data['current_condition'][0]['visibilityMiles'],
                    "Weather Description": weather_data['current_condition'][0]['weatherDesc'][0]['value'],
                    "Wind Direction (16-point)": weather_data['current_condition'][0]['winddir16Point'],
                    "Wind Direction (Degree)": weather_data['current_condition'][0]['winddirDegree'],
                    "Wind Speed (km/h)": weather_data['current_condition'][0]['windspeedKmph'],
                    "Wind Speed (mph)": weather_data['current_condition'][0]['windspeedMiles']
                },
                "nearest_area": {
                    "Area Name": weather_data['nearest_area'][0]['areaName'][0]['value'],
                    "Country": weather_data['nearest_area'][0]['country'][0]['value'],
                    "Region": weather_data['nearest_area'][0]['region'][0]['value'],
                    "Latitude": weather_data['nearest_area'][0]['latitude'],
                    "Longitude": weather_data['nearest_area'][0]['longitude'],
                    "Population": weather_data['nearest_area'][0]['population']
                },
                "weather_forecast": {
                    "Date": weather_data['weather'][0]['date'],
                    "Astronomy": {
                        "Moon Phase": weather_data['weather'][0]['astronomy'][0]['moon_phase'],
                        "Moon Illumination (%)": weather_data['weather'][0]['astronomy'][0]['moon_illumination'],
                        "Moonrise Time": weather_data['weather'][0]['astronomy'][0]['moonrise'],
                        "Moonset Time": weather_data['weather'][0]['astronomy'][0]['moonset'],
                        "Sunrise Time": weather_data['weather'][0]['astronomy'][0]['sunrise'],
                        "Sunset Time": weather_data['weather'][0]['astronomy'][0]['sunset']
                    },
                    "Average Temperature (Celsius)": weather_data['weather'][0]['avgtempC'],
                    "Average Temperature (Fahrenheit)": weather_data['weather'][0]['avgtempF'],
                    "Hourly Forecast": [
                        {
                            "Time": hour_data['time'],
                            "Temperature (Celsius)": hour_data['tempC'],
                            "Temperature (Fahrenheit)": hour_data['tempF'],
                            "Feels Like (Celsius)": hour_data['FeelsLikeC'],
                            "Feels Like (Fahrenheit)": hour_data['FeelsLikeF'],
                            "Wind Speed (km/h)": hour_data['windspeedKmph'],
                            "Wind Speed (mph)": hour_data['windspeedMiles'],
                            "Wind Direction (16-point)": hour_data['winddir16Point'],
                            "Wind Direction (Degree)": hour_data['winddirDegree'],
                            "Humidity (%)": hour_data['humidity'],
                            "Precipitation (mm)": hour_data['precipMM'],
                            "Precipitation (inches)": hour_data['precipInches'],
                            "Pressure (mb)": hour_data['pressure'],
                            "Pressure (inches)": hour_data['pressureInches'],
                            "UV Index": hour_data['uvIndex'],
                            "Visibility (km)": hour_data['visibility'],
                            "Visibility (miles)": hour_data['visibilityMiles'],
                            "Weather Description": hour_data['weatherDesc'][0]['value']
                        }
                        for hour_data in weather_data['weather'][0]['hourly']
                    ]
                }
            }
        else:
            return ERR_MSG.format(response.status_code)
    except requests.exceptions.ConnectionError:
        return CONN_ERR

def current_weather_details(location:str=''):
        
    weather_data = get_weather_data(location=location)
    # Weather details to display
    weather_info = weather_data["current_condition"]
    area_location = weather_data['nearest_area']
    
    weather_reports = weather_reports = [
    f"In {area_location['Region']}, {area_location['Country']}, we're experiencing {weather_info['Weather Description'].lower()} with a temperature of {weather_info['Temperature (Celsius)']}°C. It feels like {weather_info['Feels Like (Celsius)']}°C with a humidity level of {weather_info['Humidity (%)']}%. Wind speed is {weather_info['Wind Speed (km/h)']} km/h, and the sky is {weather_info['Cloud Cover (%)']}% covered with clouds.",
    f"The current weather in {area_location['Region']}, {area_location['Country']} is {weather_info['Weather Description'].lower()}, with a temperature of {weather_info['Temperature (Celsius)']}°C. It feels like {weather_info['Feels Like (Celsius)']}°C with {weather_info['Humidity (%)']}% humidity. Wind speed is {weather_info['Wind Speed (km/h)']} km/h, and cloud cover is {weather_info['Cloud Cover (%)']}%.",
    f"{area_location['Region']}, {area_location['Country']}: {weather_info['Weather Description'].lower()} weather with a temperature of {weather_info['Temperature (Celsius)']}°C. It feels like {weather_info['Feels Like (Celsius)']}°C, with humidity at {weather_info['Humidity (%)']}%. Wind speed: {weather_info['Wind Speed (km/h)']} km/h. Cloud cover: {weather_info['Cloud Cover (%)']}%.",
    f"The weather forecast for {area_location['Region']}, {area_location['Country']} predicts {weather_info['Weather Description'].lower()} with a temperature of {weather_info['Temperature (Celsius)']}°C. It feels like {weather_info['Feels Like (Celsius)']}°C, humidity at {weather_info['Humidity (%)']}%, wind speed at {weather_info['Wind Speed (km/h)']} km/h, and cloud cover at {weather_info['Cloud Cover (%)']}%.",
    f"{area_location['Region']}, {area_location['Country']} is currently experiencing {weather_info['Weather Description'].lower()} weather with a temperature of {weather_info['Temperature (Celsius)']}°C. It feels like {weather_info['Feels Like (Celsius)']}°C, with humidity at {weather_info['Humidity (%)']}%. The wind speed is {weather_info['Wind Speed (km/h)']} km/h, and the sky is {weather_info['Cloud Cover (%)']}% covered with clouds.",
    f"Here in {area_location['Region']}, {area_location['Country']}, we have {weather_info['Weather Description'].lower()} weather with a temperature of {weather_info['Temperature (Celsius)']}°C. The real feel is {weather_info['Feels Like (Celsius)']}°C, and the humidity level is {weather_info['Humidity (%)']}%. The wind speed is {weather_info['Wind Speed (km/h)']} km/h, and the sky is {weather_info['Cloud Cover (%)']}% covered with clouds.",
    f"The current weather condition in {area_location['Region']}, {area_location['Country']} is {weather_info['Weather Description'].lower()}, with a temperature of {weather_info['Temperature (Celsius)']}°C. It feels like {weather_info['Feels Like (Celsius)']}°C, with {weather_info['Humidity (%)']}% humidity. Wind speed is {weather_info['Wind Speed (km/h)']} km/h, and cloud cover is {weather_info['Cloud Cover (%)']}%.",
    f"{area_location['Region']}, {area_location['Country']}: {weather_info['Weather Description'].lower()} weather with a temperature of {weather_info['Temperature (Celsius)']}°C. It feels like {weather_info['Feels Like (Celsius)']}°C, with humidity at {weather_info['Humidity (%)']}%. Wind speed: {weather_info['Wind Speed (km/h)']} km/h. Cloud cover: {weather_info['Cloud Cover (%)']}%.",
    f"The weather forecast for {area_location['Region']}, {area_location['Country']} predicts {weather_info['Weather Description'].lower()} with a temperature of {weather_info['Temperature (Celsius)']}°C. It feels like {weather_info['Feels Like (Celsius)']}°C, humidity at {weather_info['Humidity (%)']}%, wind speed at {weather_info['Wind Speed (km/h)']} km/h, and cloud cover at {weather_info['Cloud Cover (%)']}%.",
    f"{area_location['Region']}, {area_location['Country']} is currently experiencing {weather_info['Weather Description'].lower()} weather with a temperature of {weather_info['Temperature (Celsius)']}°C. It feels like {weather_info['Feels Like (Celsius)']}°C, with humidity at {weather_info['Humidity (%)']}%. The wind speed is {weather_info['Wind Speed (km/h)']} km/h, and the sky is {weather_info['Cloud Cover (%)']}% covered with clouds.",
    f"Currently in {area_location['Region']}, {area_location['Country']}, the weather is {weather_info['Weather Description'].lower()} with a temperature of {weather_info['Temperature (Celsius)']}°C. The real feel is {weather_info['Feels Like (Celsius)']}°C, with a humidity level of {weather_info['Humidity (%)']}%. Wind speed is {weather_info['Wind Speed (km/h)']} km/h, and the sky is {weather_info['Cloud Cover (%)']}% covered with clouds.",
    f"{area_location['Region']}, {area_location['Country']} is under the influence of {weather_info['Weather Description'].lower()} weather with a temperature of {weather_info['Temperature (Celsius)']}°C. It feels like {weather_info['Feels Like (Celsius)']}°C, with humidity at {weather_info['Humidity (%)']}%. The wind speed is {weather_info['Wind Speed (km/h)']} km/h, and the sky is {weather_info['Cloud Cover (%)']}% covered with clouds.",
    f"Today's weather in {area_location['Region']}, {area_location['Country']} is {weather_info['Weather Description'].lower()} with a temperature of {weather_info['Temperature (Celsius)']}°C. Feels like {weather_info['Feels Like (Celsius)']}°C, humidity is {weather_info['Humidity (%)']}%, wind speed at {weather_info['Wind Speed (km/h)']} km/h, and cloud cover at {weather_info['Cloud Cover (%)']}%.",
    f"Current conditions in {area_location['Region']}, {area_location['Country']} include {weather_info['Weather Description'].lower()} weather with a temperature of {weather_info['Temperature (Celsius)']}°C. It feels like {weather_info['Feels Like (Celsius)']}°C with a humidity level of {weather_info['Humidity (%)']}%. Wind speed is {weather_info['Wind Speed (km/h)']} km/h, and the sky is {weather_info['Cloud Cover (%)']}% covered with clouds.",
    f"Presently in {area_location['Region']}, {area_location['Country']}, we're experiencing {weather_info['Weather Description'].lower()} with a temperature of {weather_info['Temperature (Celsius)']}°C. It feels like {weather_info['Feels Like (Celsius)']}°C with a humidity level of {weather_info['Humidity (%)']}%. Wind speed is {weather_info['Wind Speed (km/h)']} km/h, and the sky is {weather_info['Cloud Cover (%)']}% covered with clouds.",
    f"The weather in {area_location['Region']}, {area_location['Country']} is {weather_info['Weather Description'].lower()} with a temperature of {weather_info['Temperature (Celsius)']}°C. It feels like {weather_info['Feels Like (Celsius)']}°C with a humidity level of {weather_info['Humidity (%)']}%. Wind speed is {weather_info['Wind Speed (km/h)']} km/h, and the sky is {weather_info['Cloud Cover (%)']}% covered with clouds.",
    f"At the moment, {area_location['Region']}, {area_location['Country']} is experiencing {weather_info['Weather Description'].lower()} weather with a temperature of {weather_info['Temperature (Celsius)']}°C. It feels like {weather_info['Feels Like (Celsius)']}°C with a humidity level of {weather_info['Humidity (%)']}%. Wind speed is {weather_info['Wind Speed (km/h)']} km/h, and the sky is {weather_info['Cloud Cover (%)']}% covered with clouds.",
    f"Observing {area_location['Region']}, {area_location['Country']} at this time, we're seeing {weather_info['Weather Description'].lower()} weather with a temperature of {weather_info['Temperature (Celsius)']}°C. It feels like {weather_info['Feels Like (Celsius)']}°C with a humidity level of {weather_info['Humidity (%)']}%. Wind speed is {weather_info['Wind Speed (km/h)']} km/h, and the sky is {weather_info['Cloud Cover (%)']}% covered with clouds.",
    f"Currently, in {area_location['Region']}, {area_location['Country']}, {weather_info['Weather Description'].lower()} weather is prevailing with a temperature of {weather_info['Temperature (Celsius)']}°C. It feels like {weather_info['Feels Like (Celsius)']}°C with a humidity level of {weather_info['Humidity (%)']}%. Wind speed is {weather_info['Wind Speed (km/h)']} km/h, and the sky is {weather_info['Cloud Cover (%)']}% covered with clouds.",
    f"Right now in {area_location['Region']}, {area_location['Country']}, we're experiencing {weather_info['Weather Description'].lower()} with a temperature of {weather_info['Temperature (Celsius)']}°C. It feels like {weather_info['Feels Like (Celsius)']}°C with a humidity level of {weather_info['Humidity (%)']}%. Wind speed is {weather_info['Wind Speed (km/h)']} km/h, and the sky is {weather_info['Cloud Cover (%)']}% covered with clouds.",
    f"Currently in {area_location['Region']}, {area_location['Country']}, the weather is {weather_info['Weather Description'].lower()} with a temperature of {weather_info['Temperature (Celsius)']}°C. It feels like {weather_info['Feels Like (Celsius)']}°C with a humidity level of {weather_info['Humidity (%)']}%. Wind speed is {weather_info['Wind Speed (km/h)']} km/h, and the sky is {weather_info['Cloud Cover (%)']}% covered with clouds.",
    f"In {area_location['Region']}, {area_location['Country']}, the weather is currently {weather_info['Weather Description'].lower()} with a temperature of {weather_info['Temperature (Celsius)']}°C. It feels like {weather_info['Feels Like (Celsius)']}°C with a humidity level of {weather_info['Humidity (%)']}%. Wind speed is {weather_info['Wind Speed (km/h)']} km/h, and the sky is {weather_info['Cloud Cover (%)']}% covered with clouds.",
    f"At this moment, {area_location['Region']}, {area_location['Country']} is experiencing {weather_info['Weather Description'].lower()} with a temperature of {weather_info['Temperature (Celsius)']}°C. It feels like {weather_info['Feels Like (Celsius)']}°C with a humidity level of {weather_info['Humidity (%)']}%. Wind speed is {weather_info['Wind Speed (km/h)']} km/h, and the sky is {weather_info['Cloud Cover (%)']}% covered with clouds.",
    f"Observing the current weather in {area_location['Region']}, {area_location['Country']}, we're seeing {weather_info['Weather Description'].lower()} with a temperature of {weather_info['Temperature (Celsius)']}°C. It feels like {weather_info['Feels Like (Celsius)']}°C with a humidity level of {weather_info['Humidity (%)']}%. Wind speed is {weather_info['Wind Speed (km/h)']} km/h, and the sky is {weather_info['Cloud Cover (%)']}% covered with clouds.",
    f"At this time in {area_location['Region']}, {area_location['Country']}, {weather_info['Weather Description'].lower()} weather is prevailing with a temperature of {weather_info['Temperature (Celsius)']}°C. It feels like {weather_info['Feels Like (Celsius)']}°C with a humidity level of {weather_info['Humidity (%)']}%. Wind speed is {weather_info['Wind Speed (km/h)']} km/h, and the sky is {weather_info['Cloud Cover (%)']}% covered with clouds.",
    f"Currently in {area_location['Region']}, {area_location['Country']}, the weather is {weather_info['Weather Description'].lower()} with a temperature of {weather_info['Temperature (Celsius)']}°C. It feels like {weather_info['Feels Like (Celsius)']}°C with a humidity level of {weather_info['Humidity (%)']}%. Wind speed is {weather_info['Wind Speed (km/h)']} km/h, and the sky is {weather_info['Cloud Cover (%)']}% covered with clouds.",
    f"In {area_location['Region']}, {area_location['Country']}, the weather is currently {weather_info['Weather Description'].lower()} with a temperature of {weather_info['Temperature (Celsius)']}°C. It feels like {weather_info['Feels Like (Celsius)']}°C with a humidity level of {weather_info['Humidity (%)']}%. Wind speed is {weather_info['Wind Speed (km/h)']} km/h, and the sky is {weather_info['Cloud Cover (%)']}% covered with clouds.",
    f"At this moment, {area_location['Region']}, {area_location['Country']} is experiencing {weather_info['Weather Description'].lower()} with a temperature of {weather_info['Temperature (Celsius)']}°C. It feels like {weather_info['Feels Like (Celsius)']}°C with a humidity level of {weather_info['Humidity (%)']}%. Wind speed is {weather_info['Wind Speed (km/h)']} km/h, and the sky is {weather_info['Cloud Cover (%)']}% covered with clouds.",
    f"Observing the current weather in {area_location['Region']}, {area_location['Country']}, we're seeing {weather_info['Weather Description'].lower()} with a temperature of {weather_info['Temperature (Celsius)']}°C. It feels like {weather_info['Feels Like (Celsius)']}°C with a humidity level of {weather_info['Humidity (%)']}%. Wind speed is {weather_info['Wind Speed (km/h)']} km/h, and the sky is {weather_info['Cloud Cover (%)']}% covered with clouds.",
    f"At this time in {area_location['Region']}, {area_location['Country']}, {weather_info['Weather Description'].lower()} weather is prevailing with a temperature of {weather_info['Temperature (Celsius)']}°C. It feels like {weather_info['Feels Like (Celsius)']}°C with a humidity level of {weather_info['Humidity (%)']}%. Wind speed is {weather_info['Wind Speed (km/h)']} km/h, and the sky is {weather_info['Cloud Cover (%)']}% covered with clouds."
    ]

    return random.choice(weather_reports)

# print(current_weather_details(location=''))
