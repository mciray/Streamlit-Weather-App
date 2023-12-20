import requests
import streamlit as st
from PIL import Image
from io import BytesIO

## http://api.weatherstack.com/ sitesine gidip (ücretsiz) api key alın ve yerleştirin.

api_key = "##"  # API key'i buraya ekleyin


def get_weather(city):
    try:
        api_url = f"http://api.weatherstack.com/current?access_key={api_key}&query={city}"
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API isteği başarısız oldu. Hata kodu: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"API isteği sırasında bir hata oluştu: {e}")
        return None

def main():
    st.title("Hava Durumu Uygulaması")

    city = st.text_input("Şehir adını girin:", value="Ankara")

    if city:
        weather_data = get_weather(city)

        if weather_data:
            col1, col2 = st.columns(2)

            with col1:
                st.write("Şehir:", weather_data["location"]["name"])
                st.write("Ülke:", weather_data["location"]["country"])
                st.write("Bölge:", weather_data["location"]["region"])
                st.write("Sıcaklık (°C):", weather_data["current"]["temperature"])
                st.write("Hissedilen Sıcaklık (°C):", weather_data["current"]["feelslike"])
                st.write("Nem (%):", weather_data["current"]["humidity"])
                st.write("Rüzgar Hızı (km/s):", weather_data["current"]["wind_speed"])

            with col2:
                st.write("Hava Durumu:", weather_data["current"]["weather_descriptions"][0])
                st.write("Görüş Mesafesi (km):", weather_data["current"]["visibility"])
                st.write("Bulut Örtüsü (%):", weather_data["current"]["cloudcover"])
                st.write("Basınç (hPa):", weather_data["current"]["pressure"])
                image = Image.open(BytesIO(requests.get(weather_data["current"]["weather_icons"][0]).content))
                st.image(image, caption=weather_data["current"]["weather_descriptions"][0])

            if weather_data["current"]["temperature"] <= 0:
                st.snow()  # Sıcaklık 0°C veya daha düşükse kar efekti göster
        else:
            st.warning("Hava durumu bilgileri alınamadı.")

if __name__ == "__main__":
    main()
