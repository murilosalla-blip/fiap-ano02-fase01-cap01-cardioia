"""Front acadêmico do CardioIA — Fase 2.

Execução:
    streamlit run fase2/app.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st


DIRETORIO_FASE2 = Path(__file__).resolve().parent
sys.path.insert(0, str(DIRETORIO_FASE2 / "src"))

from classificar_risco_texto import (  # noqa: E402
    avaliar_entrada_textual,
    treinar_modelo_completo,
)
from extrair_sintomas import analisar_relato, carregar_mapa  # noqa: E402
from treinar_baselines import carregar_dados, criar_modelos  # noqa: E402


st.set_page_config(
    page_title="CardioIA",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="collapsed",
)


ROTULOS_VARIAVEIS = {
    "idade": "Idade",
    "sexo": "Sexo",
    "tipo_dor_peito": "Tipo de dor no peito",
    "pressao_arterial_repouso": "Pressão arterial em repouso",
    "colesterol": "Colesterol",
    "acucar_jejum_maior_120": "Glicemia de jejum acima de 120 mg/dl",
    "eletrocardiograma_repouso": "Resultado do ECG em repouso",
    "frequencia_cardiaca_maxima": "Frequência cardíaca máxima",
    "angina_induzida_exercicio": "Angina induzida por exercício",
    "depressao_st_exercicio": "Depressão do segmento ST",
    "inclinacao_st_pico_exercicio": "Inclinação do segmento ST",
    "num_vasos_principais": "Número de vasos principais",
    "resultado_thal": "Resultado do atributo thal",
}

ROTULOS_CATEGORIAS = {
    "masculino": "Masculino",
    "feminino": "Feminino",
    "angina_tipica": "Angina típica",
    "angina_atipica": "Angina atípica",
    "dor_nao_anginosa": "Dor não anginosa",
    "assintomatico": "Assintomático",
    "sim": "Sim",
    "nao": "Não",
    "normal": "Normal",
    "anormalidade_onda_st_t": "Anormalidade da onda ST-T",
    "hipertrofia_ventricular_esquerda": "Hipertrofia ventricular esquerda",
    "ascendente": "Ascendente",
    "plana": "Plana",
    "descendente": "Descendente",
    "defeito_fixo": "Defeito fixo",
    "defeito_reversivel": "Defeito reversível",
}


def aplicar_estilo() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at 92% 8%, rgba(200, 29, 119, 0.10), transparent 30rem),
                #fcfafc;
        }
        .block-container {
            max-width: 1180px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }
        .hero {
            padding: 2rem 2.2rem;
            border-radius: 24px;
            color: white;
            background: linear-gradient(120deg, #50133f 0%, #9d145e 58%, #d92d84 100%);
            box-shadow: 0 18px 45px rgba(80, 19, 63, 0.18);
            margin-bottom: 1.4rem;
        }
        .hero h1 {
            margin: 0;
            font-size: 2.55rem;
            letter-spacing: -0.04em;
        }
        .hero p {
            margin: 0.65rem 0 0;
            max-width: 760px;
            font-size: 1.05rem;
            opacity: 0.92;
        }
        .academic-badge {
            display: inline-block;
            padding: 0.35rem 0.75rem;
            margin-bottom: 0.8rem;
            border: 1px solid rgba(255,255,255,0.45);
            border-radius: 999px;
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }
        .result-card {
            padding: 1.5rem;
            border: 1px solid #eadce5;
            border-radius: 20px;
            background: white;
            box-shadow: 0 8px 28px rgba(62, 22, 49, 0.08);
        }
        .result-number {
            color: #9d145e;
            font-size: 3rem;
            font-weight: 750;
            line-height: 1;
        }
        .muted {
            color: #6f626b;
            font-size: 0.92rem;
        }
        div[data-testid="stMetric"] {
            border: 1px solid #eadce5;
            background: white;
            padding: 1rem;
            border-radius: 16px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_resource(show_spinner="Preparando o modelo acadêmico...")
def obter_modelo():
    """Treina o modelo selecionado usando todos os registros para demonstração."""
    atributos, alvo = carregar_dados()
    modelo = criar_modelos()["regressao_logistica"]
    modelo.fit(atributos, alvo)
    return modelo


@st.cache_resource(show_spinner="Preparando o classificador textual...")
def obter_modelo_textual():
    return treinar_modelo_completo()


@st.cache_resource(show_spinner=False)
def obter_mapa_conhecimento():
    return carregar_mapa()


def formatar_categoria(valor: str) -> str:
    return ROTULOS_CATEGORIAS.get(valor, valor.replace("_", " ").capitalize())


def resumir_registro(registro: pd.DataFrame) -> pd.DataFrame:
    """Formata os valores efetivamente enviados ao modelo."""
    linhas = []
    for variavel, valor in registro.iloc[0].items():
        if pd.isna(valor):
            valor_exibido = "Não informado — preenchido automaticamente"
        elif isinstance(valor, str):
            valor_exibido = formatar_categoria(valor)
        elif float(valor).is_integer():
            valor_exibido = str(int(valor))
        else:
            valor_exibido = f"{float(valor):.1f}"

        linhas.append(
            {
                "Campo": ROTULOS_VARIAVEIS.get(variavel, variavel),
                "Valor utilizado": valor_exibido,
            }
        )
    return pd.DataFrame(linhas)


def criar_formulario() -> pd.DataFrame | None:
    st.subheader("Dados da simulação")
    st.caption(
        "Preencha valores fictícios ou de exemplo. Não insira nome, CPF, prontuário "
        "ou qualquer informação que identifique uma pessoa."
    )

    with st.form("formulario_simulacao"):
        coluna_1, coluna_2, coluna_3 = st.columns(3)

        with coluna_1:
            idade = st.number_input("Idade", min_value=18, max_value=100, value=54)
            sexo = st.selectbox(
                "Sexo biológico",
                ["feminino", "masculino"],
                format_func=formatar_categoria,
            )
            tipo_dor = st.selectbox(
                "Tipo de dor no peito",
                [
                    "angina_tipica",
                    "angina_atipica",
                    "dor_nao_anginosa",
                    "assintomatico",
                ],
                format_func=formatar_categoria,
                help=(
                    "Descreve o tipo de dor registrado. É diferente do campo "
                    "'Angina induzida por exercício'."
                ),
            )
            pressao = st.number_input(
                "Pressão arterial em repouso (mm Hg)",
                min_value=70,
                max_value=250,
                value=130,
            )
            colesterol = st.number_input(
                "Colesterol sérico (mg/dl)",
                min_value=80,
                max_value=700,
                value=245,
            )

        with coluna_2:
            acucar = st.selectbox(
                "Glicemia de jejum acima de 120 mg/dl",
                ["nao", "sim"],
                format_func=formatar_categoria,
            )
            ecg = st.selectbox(
                "ECG em repouso",
                [
                    "normal",
                    "anormalidade_onda_st_t",
                    "hipertrofia_ventricular_esquerda",
                ],
                format_func=formatar_categoria,
            )
            frequencia = st.number_input(
                "Frequência cardíaca máxima (bpm)",
                min_value=50,
                max_value=230,
                value=150,
            )
            angina_exercicio = st.selectbox(
                "Angina induzida por exercício",
                ["nao", "sim"],
                format_func=formatar_categoria,
            )
            depressao_st = st.number_input(
                "Depressão do segmento ST",
                min_value=0.0,
                max_value=10.0,
                value=1.0,
                step=0.1,
            )

        with coluna_3:
            inclinacao = st.selectbox(
                "Inclinação do ST no pico do exercício",
                ["ascendente", "plana", "descendente"],
                format_func=formatar_categoria,
            )
            vasos_exibicao = st.selectbox(
                "Número de vasos principais",
                ["Não informado", "0", "1", "2", "3"],
                help="Quantidade observada por fluoroscopia na base original.",
            )
            thal_exibicao = st.selectbox(
                "Resultado do atributo thal",
                [
                    "Não informado",
                    "normal",
                    "defeito_fixo",
                    "defeito_reversivel",
                ],
                format_func=lambda valor: (
                    valor if valor == "Não informado" else formatar_categoria(valor)
                ),
                help=(
                    "A documentação original da UCI fornece os rótulos, mas não "
                    "expande o significado clínico da sigla."
                ),
            )
            st.info(
                "O modelo foi desenvolvido com uma base histórica pequena. "
                "Valores fora do perfil original aumentam a incerteza."
            )

        enviado = st.form_submit_button(
            "Executar simulação",
            type="primary",
            width="stretch",
        )

    if not enviado:
        return None

    vasos = np.nan if vasos_exibicao == "Não informado" else float(vasos_exibicao)
    thal = np.nan if thal_exibicao == "Não informado" else thal_exibicao

    return pd.DataFrame(
        [
            {
                "idade": int(idade),
                "pressao_arterial_repouso": float(pressao),
                "colesterol": float(colesterol),
                "frequencia_cardiaca_maxima": float(frequencia),
                "depressao_st_exercicio": float(depressao_st),
                "num_vasos_principais": vasos,
                "sexo": sexo,
                "tipo_dor_peito": tipo_dor,
                "acucar_jejum_maior_120": acucar,
                "eletrocardiograma_repouso": ecg,
                "angina_induzida_exercicio": angina_exercicio,
                "inclinacao_st_pico_exercicio": inclinacao,
                "resultado_thal": thal,
            }
        ]
    )


def explicar_predicao(modelo, registro: pd.DataFrame) -> pd.DataFrame:
    """Calcula contribuições locais da Regressão Logística."""
    preprocessador = modelo.named_steps["preprocessamento"]
    estimador = modelo.named_steps["modelo"]
    valores = preprocessador.transform(registro)[0]
    coeficientes = estimador.coef_[0]
    nomes = preprocessador.get_feature_names_out()
    contribuicoes = valores * coeficientes

    linhas = []
    for nome, contribuicao in zip(nomes, contribuicoes, strict=True):
        nome_limpo = nome.replace("numerico__", "").replace("categorico__", "")
        rotulo = nome_limpo
        for variavel, traducao in sorted(
            ROTULOS_VARIAVEIS.items(),
            key=lambda item: len(item[0]),
            reverse=True,
        ):
            if nome_limpo == variavel:
                rotulo = traducao
                break
            prefixo = f"{variavel}_"
            if nome_limpo.startswith(prefixo):
                categoria = nome_limpo[len(prefixo):]
                rotulo = f"{traducao}: {formatar_categoria(categoria)}"
                break

        linhas.append(
            {
                "Fator": rotulo,
                "Contribuição": float(contribuicao),
                "Efeito": (
                    "Aumentou a estimativa"
                    if contribuicao > 0
                    else "Reduziu a estimativa"
                ),
            }
        )

    tabela = pd.DataFrame(linhas)
    tabela["Magnitude"] = tabela["Contribuição"].abs()
    return tabela.sort_values("Magnitude", ascending=False)


def mostrar_resultado(registro: pd.DataFrame) -> None:
    modelo = obter_modelo()
    probabilidade = float(modelo.predict_proba(registro)[0, 1])
    classe = (
        "Padrão compatível com presença"
        if probabilidade >= 0.5
        else "Padrão compatível com ausência"
    )

    st.markdown("---")
    st.subheader("Resultado da simulação")

    coluna_resultado, coluna_contexto = st.columns([1, 1.25], gap="large")
    with coluna_resultado:
        st.markdown(
            f"""
            <div class="result-card">
                <div class="muted">Estimativa para o desfecho da base Cleveland</div>
                <div class="result-number">{probabilidade:.1%}</div>
                <p><strong>Classe matemática:</strong> {classe}</p>
                <p class="muted">
                    Desfecho estudado: presença de estreitamento angiográfico
                    acima de 50%. Corte acadêmico para classificação: 50%.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.progress(probabilidade)

    with coluna_contexto:
        st.warning(
            "Este percentual não é a chance geral de uma pessoa ter doença "
            "cardíaca. Ele não realiza diagnóstico, não mede risco de infarto e "
            "não deve orientar decisões de saúde."
        )
        st.write(
            "Leia o número apenas como a estimativa produzida por uma Regressão "
            "Logística para o desfecho específico da base Cleveland, composta "
            "por 303 registros históricos."
        )

    campos_ausentes = [
        ROTULOS_VARIAVEIS[coluna]
        for coluna in ["num_vasos_principais", "resultado_thal"]
        if pd.isna(registro.iloc[0][coluna])
    ]
    if campos_ausentes:
        st.warning(
            f"Campos não informados: {', '.join(campos_ausentes)}. O pipeline "
            "preencheu automaticamente valores ausentes usando a mediana para "
            "campos numéricos e a categoria mais frequente para categóricos. "
            "Isso não significa que esses exames sejam normais."
        )

    with st.expander("Conferir os valores usados na simulação"):
        st.dataframe(
            resumir_registro(registro),
            width="stretch",
            hide_index=True,
        )

    st.subheader("O que mais influenciou o resultado")
    st.caption(
        "Os valores abaixo são forças relativas dentro do cálculo — não são "
        "pontos percentuais. Associação estatística não significa causalidade."
    )
    explicacao = explicar_predicao(modelo, registro)
    aumentaram = explicacao[explicacao["Contribuição"] > 0].head(4)
    reduziram = explicacao[explicacao["Contribuição"] < 0].head(4)

    coluna_aumentaram, coluna_reduziram = st.columns(2, gap="large")
    with coluna_aumentaram:
        st.markdown("#### Aumentaram a estimativa")
        if aumentaram.empty:
            st.caption("Nenhum fator entre os de maior influência.")
        else:
            tabela_aumentaram = aumentaram[["Fator", "Magnitude"]].rename(
                columns={"Magnitude": "Força relativa"}
            )
            st.dataframe(
                tabela_aumentaram.style.format({"Força relativa": "{:.3f}"}),
                width="stretch",
                hide_index=True,
            )

    with coluna_reduziram:
        st.markdown("#### Reduziram a estimativa")
        if reduziram.empty:
            st.caption("Nenhum fator entre os de maior influência.")
        else:
            tabela_reduziram = reduziram[["Fator", "Magnitude"]].rename(
                columns={"Magnitude": "Força relativa"}
            )
            st.dataframe(
                tabela_reduziram.style.format({"Força relativa": "{:.3f}"}),
                width="stretch",
                hide_index=True,
            )

    with st.expander("Por que alguns resultados parecem contraintuitivos?"):
        st.write(
            "O modelo aprende associações desta amostra histórica, não regras "
            "médicas universais. Por exemplo, na base usada, o desfecho positivo "
            "apareceu em 30,4% dos 23 registros com angina típica e em 72,9% dos "
            "144 registros assintomáticos. Por isso, 'angina típica' pode reduzir "
            "a estimativa do modelo, sem indicar proteção clínica."
        )
        st.write(
            "Também são campos diferentes: **tipo de dor no peito** descreve o "
            "padrão da dor; **angina induzida por exercício** informa se ela "
            "apareceu durante esforço."
        )


def pagina_textual() -> None:
    st.subheader("Análise de relatos simulados")
    st.caption(
        "Demonstração da extração por mapa de conhecimento e do classificador "
        "TF-IDF solicitado na Fase 2. Use apenas frases fictícias."
    )

    aba_extracao, aba_risco = st.tabs(
        ["Extrair sintomas", "Classificar risco textual"]
    )

    with aba_extracao:
        st.markdown("#### Associação por mapa de conhecimento")
        relato_extracao = st.text_area(
            "Relato fictício",
            value=(
                "Há dois dias sinto dor forte no peito e falta de ar, e não "
                "consigo subir escadas."
            ),
            height=120,
            key="relato_extracao",
        )
        if st.button(
            "Identificar sintomas e associações",
            type="primary",
            width="stretch",
        ):
            resultado = analisar_relato(
                relato_extracao,
                obter_mapa_conhecimento(),
            )
            if not resultado["encontrou_correspondencia"]:
                st.info(
                    "Nenhuma expressão do mapa de conhecimento foi encontrada. "
                    "Isso não confirma ausência de doença."
                )
            else:
                st.success(
                    "Expressões encontradas: "
                    + ", ".join(resultado["sintomas_identificados"])
                )
                hipoteses = pd.DataFrame(resultado["hipoteses_associadas"])
                hipoteses = hipoteses.rename(
                    columns={
                        "doenca_associada": "Associação no mapa",
                        "prioridade_no_mapa": "Prioridade didática",
                        "sintomas_identificados": "Expressões",
                        "quantidade_correspondencias": "Correspondências",
                    }
                )
                hipoteses["Expressões"] = hipoteses["Expressões"].apply(
                    lambda valores: ", ".join(valores)
                )
                st.dataframe(
                    hipoteses[
                        [
                            "Associação no mapa",
                            "Prioridade didática",
                            "Expressões",
                            "Correspondências",
                        ]
                    ],
                    width="stretch",
                    hide_index=True,
                )
            st.warning(
                "As associações são exemplos baseados em palavras-chave e não "
                "constituem diagnóstico."
            )

    with aba_risco:
        st.markdown("#### Classificação com TF-IDF")
        relato_risco = st.text_area(
            "Frase fictícia para classificação",
            value=(
                "Sinto aperto forte no peito, suor frio e dificuldade para "
                "respirar desde esta manhã."
            ),
            height=120,
            key="relato_risco",
        )
        if st.button(
            "Classificar frase",
            type="primary",
            width="stretch",
        ):
            if not relato_risco.strip():
                st.error("Digite uma frase fictícia antes de classificar.")
            else:
                modelo = obter_modelo_textual()
                avaliacao = avaliar_entrada_textual(modelo, relato_risco)
                probabilidade = float(avaliacao["probabilidade_alto_risco"])
                classe = str(avaliacao["classe"])
                st.markdown(
                    f"""
                    <div class="result-card">
                        <div class="muted">
                            Resultado do classificador textual acadêmico
                        </div>
                        <div class="result-number">{probabilidade:.1%}</div>
                        <p><strong>Classe estimada:</strong> {classe.title()}</p>
                        <p class="muted">
                            Percentual matemático atribuído à classe “alto risco”
                            na base simulada.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.progress(probabilidade)
                for alerta in avaliacao["alertas"]:
                    st.info(alerta)
                st.warning(
                    "A classificação foi treinada em frases simuladas. Não use "
                    "este resultado para decidir urgência ou atendimento médico."
                )

    with st.expander("Como as duas técnicas funcionam?"):
        st.write(
            "**Extração:** normaliza o texto e procura expressões cadastradas "
            "no mapa de conhecimento. **Classificação:** converte unigramas e "
            "bigramas em vetores TF-IDF e aplica uma Regressão Logística."
        )
        st.write(
            "Os módulos textual, tabular e visual usam bases de origens "
            "diferentes e permanecem independentes."
        )


def pagina_desempenho() -> None:
    st.subheader("Desempenho observado")
    st.caption("Avaliação no conjunto de teste com 61 pacientes.")

    colunas = st.columns(4)
    colunas[0].metric("ROC AUC", "0,958")
    colunas[1].metric("Acurácia", "86,9%")
    colunas[2].metric("Sensibilidade", "92,9%")
    colunas[3].metric("F1", "86,7%")

    st.markdown("#### Avaliação descritiva por sexo")
    desempenho = pd.DataFrame(
        [
            {
                "Sexo": "Feminino",
                "n": 20,
                "Casos positivos": 7,
                "Acurácia": 0.950,
                "Precisão": 1.000,
                "Sensibilidade": 0.857,
                "F1": 0.923,
                "ROC AUC": 1.000,
            },
            {
                "Sexo": "Masculino",
                "n": 41,
                "Casos positivos": 21,
                "Acurácia": 0.829,
                "Precisão": 0.769,
                "Sensibilidade": 0.952,
                "F1": 0.851,
                "ROC AUC": 0.938,
            },
        ]
    )
    st.dataframe(
        desempenho.style.format(
            {
                "Acurácia": "{:.1%}",
                "Precisão": "{:.1%}",
                "Sensibilidade": "{:.1%}",
                "F1": "{:.1%}",
                "ROC AUC": "{:.3f}",
            }
        ),
        width="stretch",
        hide_index=True,
    )
    st.info(
        "Os grupos são pequenos e desbalanceados. A ROC AUC de 1,000 entre "
        "mulheres pode ser consequência da amostra reduzida e não demonstra "
        "desempenho perfeito em outras populações."
    )

    st.markdown("#### Avaliação descritiva por faixa etária")
    desempenho_idade = pd.DataFrame(
        [
            {
                "Faixa etária": "Até 49 anos",
                "n": 18,
                "Casos positivos": 5,
                "Acurácia": 1.000,
                "Precisão": 1.000,
                "Sensibilidade": 1.000,
                "F1": 1.000,
                "ROC AUC": 1.000,
            },
            {
                "Faixa etária": "50 a 59 anos",
                "n": 25,
                "Casos positivos": 12,
                "Acurácia": 0.840,
                "Precisão": 0.786,
                "Sensibilidade": 0.917,
                "F1": 0.846,
                "ROC AUC": 0.981,
            },
            {
                "Faixa etária": "60 anos ou mais",
                "n": 18,
                "Casos positivos": 11,
                "Acurácia": 0.778,
                "Precisão": 0.769,
                "Sensibilidade": 0.909,
                "F1": 0.833,
                "ROC AUC": 0.870,
            },
        ]
    )
    st.dataframe(
        desempenho_idade.style.format(
            {
                "Acurácia": "{:.1%}",
                "Precisão": "{:.1%}",
                "Sensibilidade": "{:.1%}",
                "F1": "{:.1%}",
                "ROC AUC": "{:.3f}",
            }
        ),
        width="stretch",
        hide_index=True,
    )
    st.info(
        "Cada faixa contém somente 18 a 25 pacientes. O resultado de 100% até "
        "49 anos ocorreu em apenas 18 registros de teste e não deve ser "
        "interpretado como desempenho perfeito ou ausência de viés."
    )


def pagina_sobre() -> None:
    st.subheader("Sobre o modelo")
    st.write(
        "O CardioIA compara dois classificadores supervisionados e seleciona a "
        "Regressão Logística por desempenho na validação cruzada. O front treina "
        "uma cópia desse modelo com toda a base para permitir simulações."
    )

    st.markdown(
        """
        #### Limitações principais

        - Base Cleveland com 303 registros de uma única instituição.
        - Dados coletados na década de 1980 e sem representatividade brasileira.
        - Distribuição desigual entre sexos e ausência de informação étnico-racial.
        - Variável-alvo simplificada para presença ou ausência de doença.
        - Não houve validação clínica, prospectiva ou externa.
        - As modalidades textual e visual não são combinadas com este modelo.

        #### Privacidade

        O formulário não envia informações para uma API própria nem armazena os
        valores preenchidos. Ainda assim, use apenas dados fictícios ou exemplos
        e nunca forneça identificadores pessoais.
        """
    )


def main() -> None:
    aplicar_estilo()
    st.markdown(
        """
        <div class="hero">
            <div class="academic-badge">Protótipo acadêmico • Fase 2</div>
            <h1>CardioIA</h1>
            <p>
                Uma demonstração transparente de NLP e Machine Learning
                aplicado a dados cardiovasculares simulados e históricos.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.error(
        "Uso exclusivamente educacional. Este protótipo não realiza diagnóstico "
        "e não substitui avaliação médica."
    )

    aba_textual, aba_simulacao, aba_desempenho, aba_sobre = st.tabs(
        [
            "Triagem textual",
            "Modelo tabular",
            "Desempenho tabular",
            "Metodologia e limitações",
        ]
    )

    with aba_textual:
        pagina_textual()

    with aba_simulacao:
        area_resultado = st.container()
        registro = criar_formulario()

        if registro is not None:
            st.session_state["ultimo_registro"] = registro
            st.toast(
                "Simulação concluída. O resultado foi exibido acima do formulário.",
                icon="✅",
            )

        if "ultimo_registro" in st.session_state:
            with area_resultado:
                try:
                    mostrar_resultado(st.session_state["ultimo_registro"])
                except Exception as erro:
                    st.error(
                        "Não foi possível concluir a simulação. "
                        "Atualize a página e tente novamente."
                    )
                    st.exception(erro)

    with aba_desempenho:
        pagina_desempenho()

    with aba_sobre:
        pagina_sobre()


if __name__ == "__main__":
    main()
