import requests
import time

# Token do seu bot do Telegram e seu Chat ID
TELEGRAM_TOKEN = '7591189777:AAFeolW2yeoEkqsboMT1BXHwlRHjaq7_zqw'
TELEGRAM_CHAT_ID = '664085312'

def enviar_alerta(mensagem):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': mensagem}
    requests.post(url, data=payload)

def verificar_jogos():
    url = 'https://api.sofascore.com/api/v1/sport/football/events/live'
    resposta = requests.get(url)

    if resposta.status_code != 200:
        print("Erro ao acessar a API do Sofascore.")
        return

    jogos = resposta.json().get('events', [])

    for jogo in jogos:
        try:
            tempo = int(jogo['status']['minute'])
            placar = jogo['homeScore']['current'] + jogo['awayScore']['current']

            if placar == 0 and 20 <= tempo <= 35:
                stats_url = f"https://api.sofascore.com/api/v1/event/{jogo['id']}/statistics"
                stats = requests.get(stats_url).json()

                total_chutes = 0
                for grupo in stats.get('statistics', []):
                    for item in grupo.get('groups', []):
                        for stat in item.get('statisticsItems', []):
                            if stat.get('name') == "Chutes no gol":
                                total_chutes = stat.get('home', 0) + stat.get('away', 0)

                if total_chutes >= 4:
                    nome_jogo = f"{jogo['homeTeam']['name']} x {jogo['awayTeam']['name']}"
                    alerta = (
                        f"ALERTA DE POSSÍVEL OVER 0.5 FT!\n"
                        f"{nome_jogo} - {tempo}min\n"
                        f"Placar: 0x0\n"
                        f"Chutes no gol: {total_chutes}\n"
                        f"Verifique para entrada ao vivo!"
                    )
                    enviar_alerta(alerta)

        except Exception as e:
            print("Erro ao processar jogo:", e)

# Loop infinito: verifica a cada 2 minutos
while True:
    verificar_jogos()
    time.sleep(120)
