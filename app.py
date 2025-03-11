import os
from dotenv import load_dotenv
import requests
import flet
from flet import Page, TextField, Dropdown, DropdownOption, Text, Column, Container, ElevatedButton, Colors

load_dotenv()

# Cargar API Key desde variables de entorno
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def get_weather(city):
    """Devuelve la información del clima para la ciudad"""
    if not WEATHER_API_KEY:
        return "Error: La API Key de OpenWeather no está configurada."

    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=es"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            return f"El clima en {city}: {description}, temperatura: {temp} ºC"
        else:
            return f"Error al obtener el clima: {data.get('message', 'Ciudad no encontrada')}"
    except Exception as e:
        return f"Error al consultar el clima: {str(e)}"

def get_ai_response(prompt):
    """Devuelve la respuesta de OpenAI"""
    if not OPENAI_API_KEY:
        return "Error: La API Key de OpenAI no está configurada."

    try:
        import openai
        client = openai.OpenAI(api_key=OPENAI_API_KEY)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un asistente amigable y útil."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return f"Error al consultar OpenAI: {str(e)}"

# Inicio de Flet
def main(page: Page):
    page.title = "Chatbot Mejorado"
    page.bgcolor = Colors.BLUE_GREY_900
    page.theme_mode = "dark"

    input_box = TextField(
        label="Escribe tu mensaje",
        border_color=Colors.BLUE_200,
        focused_border_color=Colors.BLUE_400,
        text_style=flet.TextStyle(color=Colors.WHITE),
        expand=True
    )

    mode_dropdown = Dropdown(
        options=[
            DropdownOption("chat", "Chat con IA"),
            DropdownOption("weather", "Consultar Clima")
        ],
        value="chat",
        label="Modo",
        border_color=Colors.BLUE_200,
        color=Colors.WHITE
    )

    chat_area = Column(scroll="auto", expand=True)

    def send_message(e):
        user_message = input_box.value
        if not user_message:
            return

        # Mostrar el mensaje del usuario
        chat_area.controls.append(Text(f"Usuario: {user_message}", color=Colors.WHITE))

        # Procesar según el modo seleccionado
        if mode_dropdown.value == "weather":
            response = get_weather(user_message)
        else:
            response = get_ai_response(user_message)

        # Mostrar respuesta
        chat_area.controls.append(Text(f"Chatbot: {response}", color=Colors.BLUE_200))

        # Limpiar el input y actualizar UI
        input_box.value = ""
        chat_area.update()
        page.update()

    send_button = ElevatedButton(
        text="Enviar",
        on_click=send_message,
        bgcolor=Colors.BLUE_700,
        color=Colors.WHITE
    )

    chat_container = Container(
        content=chat_area,
        bgcolor=Colors.BLUE_GREY_800,
        padding=10,
        border_radius=10,
        expand=True
    )

    input_container = Container(
        content=flet.Row(
            controls=[
                mode_dropdown,
                input_box,
                send_button
            ],
            spacing=10
        )
    )

    page.window_width = 800
    page.window_height = 600

    page.add(chat_container, input_container)
    page.update()

if __name__ == "__main__":
    flet.app(target=main)
