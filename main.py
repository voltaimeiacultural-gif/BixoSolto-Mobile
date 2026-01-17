import flet as ft
import requests
from bs4 import BeautifulSoup
import urllib3

# Desabilita avisos de segurança chatos por causa do verify=False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def main(page: ft.Page):
    # --- Configurações da Janela ---
    page.title = "Bixo Solto - Resultados Paratodos Bahia"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 420
    page.window_height = 750
    page.scroll = "auto"

    # --- Elementos da Interface ---
    titulo = ft.Text("BiXo Solto - Resultados Paratodos",
                     size=24, weight="bold", color="blue")
    subtitulo = ft.Text("FavelaCode", size=12, color="grey")

    area_resultados = ft.Column()
    loading = ft.ProgressBar(width=400, color="amber", visible=False)

    # --- CÉREBRO: Dicionário com Códigos UNICODE ---
    mapa_bichos = {
        "avestruz": "\U0001F426",  # 🐦
        "aguia": "\U0001F985",     # 🦅
        "burro": "\U0001F434",     # 🐴
        "borboleta": "\U0001F98B",  # 🦋
        "cachorro": "\U0001F436",  # 🐶
        "cabra": "\U0001F410",     # 🐐
        "carneiro": "\U0001F411",  # 🐑
        "camelo": "\U0001F42A",    # 🐪
        "cobra": "\U0001F40D",     # 🐍
        "coelho": "\U0001F430",    # 🐰
        "cavalo": "\U0001F40E",    # 🐎
        "elefante": "\U0001F418",  # 🐘
        "galo": "\U0001F413",      # 🐓
        "gato": "\U0001F408",      # 🐈
        "jacaré": "\U0001F40A",    # 🐊
        "leão": "\U0001F981",      # 🦁
        "macaco": "\U0001F412",    # 🐒
        "porco": "\U0001F437",     # 🐷
        "pavão": "\U0001F99A",     # 🦚
        "peru": "\U0001F983",      # 🦃
        "touro": "\U0001F402",     # 🐂
        "tigre": "\U0001F405",     # 🐅
        "urso": "\U0001F43B",      # 🐻
        "veado": "\U0001F98C",     # 🦌
        "vaca": "\U0001F42E"       # 🐮
    }

    def identificar_simbolo(texto):
        if not texto:
            return ""
        texto_lower = texto.lower()
        for nome_bicho, emoji_code in mapa_bichos.items():
            if nome_bicho in texto_lower:
                return f"{emoji_code} {texto}"
        return texto

    # --- Função que busca os dados ---
    def buscar_resultados(e):
        area_resultados.controls.clear()
        loading.visible = True
        btn_atualizar.disabled = True
        page.update()

        try:
            link = "https://www.resultadosagora.com/resultados-da-paratodos-bahia-de-hoje"

            # --- DISFARCE REFORÇADO ---
            # Imitamos um navegador completo para o site não bloquear
            cabecalho_req = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
                "Upgrade-Insecure-Requests": "1",
                "Connection": "keep-alive"
            }

            # O verify=False pula a checagem de segurança SSL que causa o erro 10054
            requisicao = requests.get(
                link, headers=cabecalho_req, verify=False, timeout=10)

            # Força UTF-8 para corrigir acentos (1Â.)
            requisicao.encoding = 'utf-8'

            site = BeautifulSoup(requisicao.text, 'html.parser')
            todas_tabelas = site.find_all('table', {'class': 'tabfull'})

            if not todas_tabelas:
                area_resultados.controls.append(
                    ft.Text("Nenhuma tabela encontrada ou bloqueio temporário.", color="red"))
            else:
                for i, tabela in enumerate(todas_tabelas):
                    linhas_visuais = []

                    # 1. Cabeçalho da Tabela
                    linhas_visuais.append(
                        ft.Container(
                            content=ft.Row([
                                ft.Text("PRÊMIO", width=70, weight="bold",
                                        size=12, text_align=ft.TextAlign.CENTER),
                                ft.Text("NÚMERO", width=80, weight="bold",
                                        size=12, text_align=ft.TextAlign.CENTER),
                                ft.Text("GRUPO/BICHO", expand=True, weight="bold",
                                        size=12, text_align=ft.TextAlign.LEFT),
                            ]),
                            bgcolor="bluegrey100",
                            padding=5,
                            border_radius=5
                        )
                    )

                    # 2. Processa as linhas
                    linhas_tabela_html = tabela.find_all('tr')

                    for index_linha, linha in enumerate(linhas_tabela_html):
                        colunas = linha.find_all(['th', 'td'])
                        dados = [c.get_text(strip=True) for c in colunas]

                        if not dados or "Prêmio" in dados[0]:
                            continue

                        if len(dados) >= 2:

                            col_premio = ft.Container(
                                content=ft.Text(
                                    dados[0], weight="bold", color="blue"),
                                width=70,
                                alignment=ft.alignment.Alignment(0, 0)
                            )

                            col_numero = ft.Container(
                                content=ft.Text(
                                    dados[1], size=16, weight="bold", font_family="monospace"),
                                width=80,
                                alignment=ft.alignment.Alignment(0, 0)
                            )

                            texto_original = dados[2] if len(dados) > 2 else ""
                            texto_com_emoji = identificar_simbolo(
                                texto_original)

                            col_resto = ft.Container(
                                content=ft.Text(texto_com_emoji, size=13),
                                expand=True,
                                alignment=ft.alignment.Alignment(-1, 0),
                                padding=ft.padding.only(left=10)
                            )

                            cor_fundo = "grey100" if index_linha % 2 == 0 else "white"

                            linha_formatada = ft.Container(
                                content=ft.Row(
                                    [col_premio, col_numero, col_resto], spacing=0),
                                bgcolor=cor_fundo,
                                padding=5,
                                border_radius=5
                            )

                            linhas_visuais.append(linha_formatada)

                    # 3. Cria o Card
                    card = ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                ft.Text(
                                    f"SORTEIO {i + 1}", weight="bold", size=18, color="black"),
                                ft.Divider(height=10, color="transparent"),
                                *linhas_visuais
                            ], spacing=2),
                            padding=10
                        ),
                        elevation=5,
                        margin=ft.margin.only(bottom=20)
                    )
                    area_resultados.controls.append(card)

        except Exception as erro:
            # Mostra o erro na tela se acontecer de novo
            area_resultados.controls.append(
                ft.Text(f"Erro de conexão: {erro}", color="red", size=16))
            print(f"Detalhe do erro: {erro}")

        loading.visible = False
        btn_atualizar.disabled = False
        page.update()

    # --- Botão de Atualizar ---
    btn_atualizar = ft.ElevatedButton(
        "Atualizar Resultados",
        icon="refresh",
        on_click=buscar_resultados,
        bgcolor="blue",
        color="white",
        height=50
    )

    page.add(
        ft.Column([
            titulo,
            subtitulo,
            ft.Divider(),
            btn_atualizar,
            loading,
            area_resultados
        ])
    )

    buscar_resultados(None)


ft.app(target=main)
