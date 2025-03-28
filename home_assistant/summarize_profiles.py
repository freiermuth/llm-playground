import requests
from ollama import Client
from os import getenv
from json import dumps

def get_weather_forecast(coordinates):
    url = f"https://api.weather.gov/gridpoints/{coordinates}/forecast"
    r = requests.get(url)
    r.raise_for_status()
    data = r.json()
    return data['properties']['periods']


def chat_ollama(prompt): 
    ollama_hostname = getenv('OLLAMA_HOST')
    print("Ollama hostname:", ollama_hostname)

    client = Client(
    host=f'http://{ollama_hostname}:11434',
    headers={'x-some-header': 'some-value'}
    )
    response = client.chat(model='llama3.1:8b', messages=[
        {
            'role': 'user',
            'content': prompt,
        },
    ])

    print(response.message.content)


if __name__ == "__main__":

    weather = get_weather_forecast(getenv("WEATHER_COORDINATES"))

    weather_prompt = f"""
    - Here is the weather data in JSON format. It contains the forecast for the next few days, starting with a more detailed description of the next two days. 
    ```json
        {dumps(weather, indent=2)}
    ```
    - Give me a summary level forcecast for each period given the wetaher data, as if you're a casual friend telling me wehat to expect. 
    - Each period has a field `name` that you should use to identify each period.
    - Order the summary by the `startTime` of each period.
    - Let me know if severe weather is expected, or if outdoor activites would be impacted by the weather.
    - Be friendly and concise. 
    - Include timing when relevant.
    - Check for consistency in the period name and your message. 
    - if you don't know what day of the week it is, don't guess.
    """

    response = chat_ollama(weather_prompt)