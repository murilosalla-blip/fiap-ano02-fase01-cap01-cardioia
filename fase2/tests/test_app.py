"""Teste funcional do front: abre a aplicação e executa uma simulação."""

from pathlib import Path

from streamlit.testing.v1 import AppTest


CAMINHO_APP = Path(__file__).resolve().parents[1] / "app.py"

app = AppTest.from_file(str(CAMINHO_APP))
app.run(timeout=60)

if app.exception:
    raise AssertionError(f"Erro ao abrir o front: {app.exception}")

abas = [item.label for item in app.tabs]
for aba_esperada in [
    "Início",
    "Nova avaliação",
    "ECG experimental",
    "Histórico da sessão",
    "Evidências",
    "Sobre",
]:
    if aba_esperada not in abas:
        raise AssertionError(f"A aba '{aba_esperada}' não foi encontrada.")

links = {item.label: item.url for item in app.get("link_button")}
if links.get("Conhecer o protótipo administrativo") != (
    "https://julia-carvalho96.github.io/grupo-aura-cardioia-portal/"
):
    raise AssertionError("O vínculo com o portal administrativo não foi exibido.")

subtitulos_iniciais = [str(item.value) for item in app.subheader]
if "Análise experimental de ECG" not in subtitulos_iniciais:
    raise AssertionError("A transparência do experimento visual não foi exibida.")

botoes = [
    botao
    for botao in app.button
    if botao.label == "Executar simulação"
]
if len(botoes) != 1:
    raise AssertionError(
        "O botão 'Executar simulação' não foi encontrado de forma única."
    )

botoes[0].click()
app.run(timeout=120)

if app.exception:
    mensagens = [str(excecao.value) for excecao in app.exception]
    raise AssertionError(
        "A simulação gerou uma exceção: " + " | ".join(mensagens)
    )

subtitulos = [str(item.value) for item in app.subheader]
if "Resultado da simulação" not in subtitulos:
    raise AssertionError("A seção de resultado não apareceu após a simulação.")

textos = " ".join(str(item.value) for item in app.markdown)
alertas = " ".join(
    str(item.value)
    for colecao in [app.warning, app.error, app.info]
    for item in colecao
)
if "Estimativa para o desfecho da base Cleveland" not in textos:
    raise AssertionError("A definição específica da estimativa não foi exibida.")
if "Campos não informados" not in alertas:
    raise AssertionError("O aviso sobre imputação de campos ausentes não foi exibido.")
if "não é a chance geral" not in alertas:
    raise AssertionError("O alerta contra interpretação clínica não foi exibido.")

botoes_extracao = [
    botao
    for botao in app.button
    if botao.label == "Identificar sintomas e associações"
]
if len(botoes_extracao) != 1:
    raise AssertionError("O botão de extração textual não foi encontrado.")
botoes_extracao[0].click()
app.run(timeout=120)
if app.exception:
    raise AssertionError(f"A extração textual falhou: {app.exception}")
if not any("Expressões encontradas" in str(item.value) for item in app.success):
    raise AssertionError("A extração não exibiu as expressões identificadas.")

botoes_risco = [
    botao
    for botao in app.button
    if botao.label == "Classificar frase"
]
if len(botoes_risco) != 1:
    raise AssertionError("O botão do classificador textual não foi encontrado.")
botoes_risco[0].click()
app.run(timeout=120)
if app.exception:
    raise AssertionError(f"A classificação textual falhou: {app.exception}")
textos = " ".join(str(item.value) for item in app.markdown)
if "Resultado do classificador textual acadêmico" not in textos:
    raise AssertionError("O resultado textual não apareceu após o clique.")

historicos = [
    quadro.value
    for quadro in app.dataframe
    if "Modalidade" in getattr(quadro.value, "columns", [])
]
if not historicos or len(historicos[0]) < 3:
    raise AssertionError(
        "O histórico da sessão não registrou as três modalidades executadas."
    )

print(
    "Produto unificado aberto; navegação, portal, ECG, histórico e simulações "
    "tabular, extrativa e textual validados."
)
