from dash import Dash, html, dcc, Input, Output, dash_table
import io
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from dash.dash_table.Format import Format, Group, Scheme, Symbol

# URL do Google Sheets
sheet_url = "https://docs.google.com/spreadsheets/d/1a0Az4vHSeZPPaLUg_MKZrD4DRPcqL4vcGABB9kpeY1c/export?format=csv"

app = Dash(__name__)

# Obter o mês corrente para inicialização
mes_corrente = datetime.now().strftime("%Y-%m")

app.layout = html.Div([
    html.Div([
        html.Img(src='assets/logo.png', style={'height': '60px', 'marginRight': '20px'}),
        html.H1("Monitor Financeiro - Contas a Pagar",
                style={'textAlign': 'right', 'marginBottom': '0', 'color': '#b30000', 'flex': '1'})
    ], style={
        'display': 'flex',
        'alignItems': 'center',
        'justifyContent': 'flex-end',
        'marginBottom': '30px',
        'width': '100%'
    }),

    # KPIs principais
    html.Div([
        html.Div([
            # Rótulo do mês será exibido no elemento de delta abaixo
            html.H3("Total Geral", style={'color': '#007bff', 'marginBottom': '5px'}),
            html.H2(id='total-geral', style={'color': '#007bff', 'margin': '0'}),
            html.Div(id='total-geral-delta', style={'marginTop': '8px'})
        ], style={'backgroundColor': '#fff', 'padding': '10px', 'borderRadius': '10px',
                  'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'textAlign': 'center', 'flex': '1'}),

        html.Div([
            html.H3("Total em Aberto", style={'color': '#dc3545', 'marginBottom': '5px'}),
            html.H2(id='total-aberto', style={'color': '#dc3545', 'margin': '0'}),
            html.Div(id='total-aberto-delta', style={'marginTop': '8px'})
        ], style={'backgroundColor': '#fff', 'padding': '10px', 'borderRadius': '10px',
                  'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'textAlign': 'center', 'flex': '1'}),

        html.Div([
            html.H3("Total Liquidado", style={'color': '#28a745', 'marginBottom': '5px'}),
            html.H2(id='total-liquidado', style={'color': '#28a745', 'margin': '0'}),
            html.Div(id='total-liquidado-delta', style={'marginTop': '8px'})
        ], style={'backgroundColor': '#fff', 'padding': '10px', 'borderRadius': '10px',
                  'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'textAlign': 'center', 'flex': '1'}),

        html.Div([
            html.H3("Contas Vencidas", style={'color': '#ffc107', 'marginBottom': '5px'}),
            html.H2(id='contas-vencidas', style={'color': '#ffc107', 'margin': '0'}),
            html.Div(id='contas-vencidas-delta', style={'marginTop': '8px'})
        ], style={'backgroundColor': '#fff', 'padding': '10px', 'borderRadius': '10px',
                  'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'textAlign': 'center', 'flex': '1'}),

        # Novo card: Gastos Mensais (gráfico compacto)
        html.Div([
            html.H3("Gastos Mensais", style={'color': '#20a387', 'marginBottom': '5px'}),
            dcc.Graph(id='card-gastos-mensais', config={'displayModeBar': False}, style={'height': '110px'})
        ], style={'backgroundColor': '#fff', 'padding': '10px', 'borderRadius': '10px',
                  'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'textAlign': 'center', 'flex': '1'})
    ], style={'display': 'flex', 'gap': '20px', 'marginBottom': '30px'}),

    # Filtros (estilo minimalista)
    html.Div([
        html.Div([
            html.Label("Tipo de Documento:", style={'fontWeight': '600', 'marginBottom': '6px', 'color': '#495057', 'fontSize': '13px'}),
            dcc.Dropdown(
                id='dropdown-tipo-doc',
                options=[],
                value=None,
                placeholder="Selecione o tipo de documento",
                clearable=True,
                style={'width': '100%', 'borderRadius': '8px', 'padding': '4px 6px', 'height': '36px', 'border': '1px solid #e9ecef', 'backgroundColor': '#ffffff'}
            )
    ], className='filter-item', style={'flex': '1', 'marginRight': '18px'}),

        html.Div([
            html.Label("Status do Pagamento:", style={'fontWeight': '600', 'marginBottom': '6px', 'color': '#495057', 'fontSize': '13px'}),
            dcc.Dropdown(
                id='dropdown-status',
                options=[
                    {'label': 'Todos', 'value': 'todos'},
                    {'label': 'Em Aberto', 'value': 'aberto'},
                    {'label': 'Liquidado', 'value': 'liquidado'}
                ],
                value='todos',
                clearable=False,
                style={'width': '100%', 'borderRadius': '8px', 'padding': '4px 6px', 'height': '36px', 'border': '1px solid #e9ecef', 'backgroundColor': '#ffffff'}
            )
    ], className='filter-item', style={'flex': '1', 'marginRight': '18px'}),

        html.Div([
            html.Label("Mês de Vencimento:", style={'fontWeight': '600', 'marginBottom': '6px', 'color': '#495057', 'fontSize': '13px'}),
            dcc.Dropdown(
                id='dropdown-mes',
                options=[],
                value=mes_corrente,  # Definindo o mês corrente como valor padrão
                placeholder="Selecione o mês",
                clearable=True,
                style={'width': '100%', 'borderRadius': '8px', 'padding': '4px 6px', 'height': '36px', 'border': '1px solid #e9ecef', 'backgroundColor': '#ffffff'}
            )
    ], className='filter-item', style={'flex': '1', 'marginRight': '18px'}),

        html.Div([
            html.Label("Fornecedor:", style={'fontWeight': '600', 'marginBottom': '6px', 'color': '#495057', 'fontSize': '13px'}),
            dcc.Dropdown(
                id='dropdown-fornecedor',
                options=[],
                value=None,
                placeholder="Selecione um fornecedor",
                clearable=True,
                style={'width': '100%', 'borderRadius': '8px', 'padding': '4px 6px', 'height': '36px', 'border': '1px solid #e9ecef', 'backgroundColor': '#ffffff'}
            )
    ], className='filter-item', style={'flex': '1', 'marginRight': '18px'}),

        html.Div([
            html.Label("Agrupamento:", style={'fontWeight': '600', 'marginBottom': '6px', 'color': '#495057', 'fontSize': '13px'}),
            dcc.Dropdown(
                id='dropdown-agrupamento',
                options=[
                    {'label': 'Normal (todos os lançamentos)', 'value': 'normal'},
                    {'label': 'Agrupado por dia (analítico)', 'value': 'diario'},
                    {'label': 'Agrupado por dia e filial', 'value': 'dia_filial'}
                ],
                value='dia_filial',
                clearable=False,
                style={'width': '100%', 'borderRadius': '8px', 'padding': '4px 6px', 'height': '36px', 'border': '1px solid #e9ecef', 'backgroundColor': '#ffffff'}
            )
        ], className='filter-item', style={'flex': '1'})
    ], className='filters-row', style={'display': 'flex', 'marginBottom': '30px', 'padding': '12px', 'backgroundColor': '#ffffff', 'borderRadius': '10px', 'boxShadow': '0 1px 2px rgba(0,0,0,0.06)'}),

    # Tabela de dados
    html.Div([
        html.H3("📋 Detalhes das Contas", style={'marginTop': '0', 'marginBottom': '20px'}),
        dash_table.DataTable(
            id='tabela-contas',
            columns=[],
            data=[],
            # permitir que o conteúdo quebre linha e não seja cortado rapidamente
            # usar altura responsiva maior para ocupar mais espaço vertical na tela
            style_table={'overflowX': 'auto', 'overflowY': 'auto', 'maxHeight': 'calc(100vh - 120px)', 'height': 'calc(100vh - 120px)', 'width': '100%'},
            style_header={
                'backgroundColor': '#d63384',
                'color': 'white',
                'fontWeight': 'bold',
                'textAlign': 'center',
                'position': 'sticky',
                'top': 0
            },
            style_cell={
                'backgroundColor': '#f8f9fa',
                'color': '#333333',
                'textAlign': 'center',
                'padding': '8px',
                'fontSize': '12px',
                'border': '1px solid #dee2e6',
                # permitir quebra de linha e largura automática para leitura
                'whiteSpace': 'normal',
                'height': 'auto',
                'overflow': 'visible',
                'textOverflow': 'clip',
                'minWidth': '80px', 'width': 'auto', 'maxWidth': '600px'
            },
            style_cell_conditional=[
                {
                    'if': {'column_id': 'Data'},
                    'minWidth': '120px', 'width': '180px', 'maxWidth': '400px',
                    'textAlign': 'left'
                },
                {
                    'if': {'column_id': 'Nome Fantasia Agente'},
                    'textAlign': 'left',
                    'minWidth': '200px', 'width': 'auto', 'maxWidth': '800px'
                },
                {
                    'if': {'column_id': 'Tipo Doc.'},
                    'minWidth': '80px', 'width': '80px', 'maxWidth': '120px'
                },
                {
                    'if': {'column_id': 'Número Doc.'},
                    'minWidth': '100px', 'width': '120px', 'maxWidth': '160px'
                },
                {
                    'if': {'column_id': 'AP'},
                    'minWidth': '60px', 'width': '80px', 'maxWidth': '100px'
                },
                {
                    'if': {'column_id': 'Líquido'},
                    'minWidth': '120px', 'width': '140px', 'maxWidth': '200px'
                },
                {
                    'if': {'column_id': 'Saldo em Aberto'},
                    'minWidth': '120px', 'width': '140px', 'maxWidth': '200px'
                },
                {
                    'if': {'column_id': 'Complemento'},
                    'textAlign': 'left',
                    'minWidth': '150px', 'width': 'auto', 'maxWidth': '600px'
                }
            ],
            style_data_conditional=[
                {
                    'if': {'filter_query': '{Saldo em Aberto} > 0'},
                    'backgroundColor': '#fff3cd',
                    'color': 'black',
                },
                {
                    'if': {'filter_query': '{Data} contains "Total"'},
                    'backgroundColor': '#d63384',
                    'color': 'white',
                    'fontWeight': 'bold'
                },
                {
                    'if': {'filter_query': '{Data} contains "DATA:"'},
                    'backgroundColor': '#007bff',
                    'color': 'white',
                    'fontWeight': 'bold',
                    'fontSize': '14px'
                },
                {
                    'if': {'filter_query': '{Data} contains "TOTAL DIA:"'},
                    # cor suavizada (teal) para total do dia, combina melhor com o visual
                    'backgroundColor': "#767676",
                    'color': 'white',
                    'fontWeight': 'normal',
                    'fontSize': '14px'
                },
                # destaque para linhas que contenham o nome da filial (caso sensível)
                {
                    'if': {'filter_query': '{Data} contains "Filial:"'},
                    'backgroundColor': '#e8f7ff',
                    'color': '#084298',
                    'fontWeight': 'bold'
                },
                {
                    'if': {'filter_query': '{Data} contains "FILIAL:"'},
                    'backgroundColor': '#e8f7ff',
                    'color': '#084298',
                    'fontWeight': 'bold'
                },
                {
                    'if': {'filter_query': '{Data} contains "Total " && {Data} contains "Filial:"'},
                    'backgroundColor': '#767676',
                    'color': 'white',
                    'fontWeight': 'normal'
                },
                {
                    'if': {'column_id': 'Data', 'filter_query': '{Data} contains "Total"'},
                    'textAlign': 'left'
                },
                {
                    'if': {'column_id': 'Nome Fantasia Agente'},
                    'textAlign': 'left'
                },
                {
                    'if': {'column_id': 'Complemento'},
                    'textAlign': 'left'
                },
                {
                    'if': {
                        'column_id': 'Tipo Doc.',
                        'filter_query': '{Tipo Doc.} = "PREV"'
                    },
                    'backgroundColor': '#ffb6c1',
                    'color': 'black'
                },
                {
                    'if': {
                        'column_id': 'Tipo Doc.',
                        'filter_query': '{Tipo Doc.} = "PREVPDC"'
                    },
                    'backgroundColor': '#90ee90',
                    'color': 'black'
                }
            ],
            page_action='none',
            sort_action='native',
            filter_action='native',
            fixed_rows={'headers': True}
        )
    ], style={'marginBottom': '30px'}),

    # Gráficos
    html.Div([
        html.Div([
            dcc.Graph(id='grafico-vencimentos')
        ], style={'width': '50%', 'display': 'inline-block'}),

        html.Div([
            dcc.Graph(id='grafico-tipos-documento')
        ], style={'width': '50%', 'display': 'inline-block'})
    ], style={'marginBottom': '20px'}),

    html.Div([
        dcc.Graph(id='grafico-fornecedores')
    ]),

    dcc.Interval(
        id='intervalo-atualizacao',
        interval=60*1000,
        n_intervals=0
    ),
    
    # Store para armazenar os dados carregados e evitar recarregamentos
    dcc.Store(id='store-dados'),

    # Botão de impressão da página
    html.Div([
        html.Button('Imprimir Página', id='btn-print', n_clicks=0,
                    style={'backgroundColor': '#007bff', 'color': 'white', 'border': 'none',
                           'padding': '10px 16px', 'borderRadius': '6px', 'cursor': 'pointer'}),
        html.Div(id='print-output', style={'display': 'none'})
    ], style={'textAlign': 'right', 'marginTop': '20px'})
], style={'width': '100%', 'margin': '0', 'padding': '12px 24px', 'boxSizing': 'border-box'})

# ----------------------------
# Funções utilitárias
# ----------------------------
def format_brl(valor):
    """Formata número float em R$ com vírgula como decimal."""
    try:
        return f"R$ {float(valor):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except:
        return "R$ 0,00"

def carregar_dados():
    """Carrega e processa os dados das contas a pagar."""
    try:
        df = pd.read_csv(sheet_url)

        # Limpeza e normalização
        if 'Tipo Doc.' in df.columns:
            df['Tipo Doc.'] = df['Tipo Doc.'].astype(str).str.strip()

        # Conversão robusta de valores monetários
        for col in ['Retenção IR', 'Líquido', 'Saldo em Aberto']:
            if col in df.columns:
                df[col] = (
                    df[col]
                    .astype(str)
                    .str.replace(r'[^\d,-]', '', regex=True)
                    .str.replace('.', '', regex=False)
                    .str.replace(',', '.', regex=False)
                    .replace('', '0')
                )
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        # Conversão robusta de datas
        if 'Prorrogado' in df.columns:
            df['Prorrogado'] = pd.to_datetime(
                df['Prorrogado'],
                dayfirst=True,
                errors='coerce'
            )
            
            # Criar coluna de mês no formato 'YYYY-MM'
            df['Mes'] = df['Prorrogado'].dt.to_period('M').astype(str)
            
            # Criar coluna de mês numérico para comparações
            df['Mes_Num'] = df['Prorrogado'].dt.month

        # Verificar contas vencidas
        hoje = datetime.now().date()
        if 'Prorrogado' in df.columns:
            df['Vencido'] = df['Prorrogado'].dt.date < hoje

        return df

    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

# ----------------------------
# Callbacks
# ----------------------------
@app.callback(
    Output('store-dados', 'data'),
    Input('intervalo-atualizacao', 'n_intervals')
)
def atualizar_store(n):
    """Carrega os dados do Google Sheet e armazena em um dcc.Store."""
    df = carregar_dados()
    return df.to_json(date_format='iso', orient='split')

@app.callback(
    Output('dropdown-tipo-doc', 'options'),
    Output('dropdown-fornecedor', 'options'),
    Output('dropdown-mes', 'options'),
    Input('store-dados', 'data')
)
def atualizar_opcoes(json_data):
    df = pd.read_json(io.StringIO(json_data), orient='split') if json_data else pd.DataFrame()

    if df.empty:
        return [], [], []

    # Tipos de documento
    if 'Tipo Doc.' in df.columns:
        tipos = sorted(df['Tipo Doc.'].dropna().unique())
        tipos_doc = [{'label': 'Todos', 'value': 'todos'}] + [{'label': t, 'value': t} for t in tipos]
    else:
        tipos_doc = [{'label': 'Todos', 'value': 'todos'}]

    # Fornecedores
    if 'Nome Fantasia Agente' in df.columns:
        forn = sorted(df['Nome Fantasia Agente'].dropna().unique())
        fornecedores = [{'label': 'Todos', 'value': 'todos'}] + [{'label': f, 'value': f} for f in forn]
    else:
        fornecedores = [{'label': 'Todos', 'value': 'todos'}]

    # Meses
    if 'Mes' in df.columns:
        # Garante que o mês corrente esteja sempre na lista de opções
        meses_dados = set(df['Mes'].dropna().unique())
        mes_corrente_str = datetime.now().strftime("%Y-%m")
        meses_dados.add(mes_corrente_str)
        
        meses_ordenados = sorted(list(meses_dados), key=lambda x: pd.to_datetime(x))
        meses_opt = [{'label': 'Todos', 'value': 'todos'}] + [{'label': m, 'value': m} for m in meses_ordenados]
    else:
        meses_opt = [{'label': 'Todos', 'value': 'todos'}]
        mes_corrente_str = datetime.now().strftime("%Y-%m")

    return tipos_doc, fornecedores, meses_opt

def filtrar_dataframe(df, tipo_doc, status, fornecedor, mes):
    """Função auxiliar para aplicar filtros ao DataFrame."""
    df_filtrado = df.copy()

    # Aplicar filtros
    if tipo_doc and tipo_doc != 'todos' and 'Tipo Doc.' in df_filtrado.columns:
        df_filtrado = df_filtrado[df_filtrado['Tipo Doc.'] == tipo_doc]

    if status and status != 'todos' and 'Saldo em Aberto' in df_filtrado.columns:
        if status == 'aberto':
            df_filtrado = df_filtrado[df_filtrado['Saldo em Aberto'] > 0]
        elif status == 'liquidado':
            df_filtrado = df_filtrado[df_filtrado['Saldo em Aberto'] == 0]

    if fornecedor and fornecedor != 'todos' and 'Nome Fantasia Agente' in df_filtrado.columns:
        df_filtrado = df_filtrado[df_filtrado['Nome Fantasia Agente'] == fornecedor]

    if mes and mes != 'todos' and 'Mes' in df_filtrado.columns:
        df_filtrado = df_filtrado[df_filtrado['Mes'] == mes]
    
    return df_filtrado

@app.callback(
    Output('total-liquidado', 'children'),
    Output('total-aberto', 'children'),
    Output('contas-vencidas', 'children'),
    Output('total-geral', 'children'),
    Input('dropdown-tipo-doc', 'value'),
    Input('dropdown-status', 'value'),
    Input('dropdown-fornecedor', 'value'),
    Input('dropdown-mes', 'value'),
    Input('store-dados', 'data')
)
def atualizar_kpis(tipo_doc, status, fornecedor, mes, json_data):
    df = pd.read_json(io.StringIO(json_data), orient='split') if json_data else pd.DataFrame()

    if df.empty or 'Mes' not in df.columns:
        return "R$ 0,00", "R$ 0,00", "0", "R$ 0,00"

    # Se nenhum mês foi selecionado, usar o mês corrente
    mes_selecionado = mes if mes and mes != 'todos' else datetime.now().strftime("%Y-%m")

    df_filtrado = filtrar_dataframe(df, tipo_doc, status, fornecedor, mes_selecionado)

    # Cálculo dos KPIs
    total_aberto = 0
    total_liquidado = 0
    total_geral = 0
    contas_vencidas = 0

    if 'Líquido' in df_filtrado.columns:
        total_geral = df_filtrado['Líquido'].sum()
        
        if 'Saldo em Aberto' in df_filtrado.columns:
            # Total Liquidado (Saldo em Aberto == 0)
            total_liquidado = df_filtrado.loc[df_filtrado['Saldo em Aberto'] == 0, 'Líquido'].sum()
            
            # Total em Aberto
            total_aberto = df_filtrado.loc[df_filtrado['Saldo em Aberto'] > 0, 'Saldo em Aberto'].sum()
            
            # Contas vencidas
            if 'Vencido' in df_filtrado.columns:
                contas_vencidas = len(df_filtrado[(df_filtrado['Vencido'] == True) & 
                                                (df_filtrado['Saldo em Aberto'] > 0)])

    return (
        format_brl(total_liquidado),
        format_brl(total_aberto),
        str(contas_vencidas),
        format_brl(total_geral)
    )


@app.callback(
    Output('total-geral-delta', 'children'),
    Input('dropdown-mes', 'value'),
    Input('dropdown-tipo-doc', 'value'),
    Input('dropdown-status', 'value'),
    Input('dropdown-fornecedor', 'value'),
    Input('store-dados', 'data')
)
def atualizar_total_geral_delta(mes, tipo_doc, status, fornecedor, json_data):
    """Calcula variação percentual do Total Geral entre mês selecionado e mês anterior."""
    df = pd.read_json(io.StringIO(json_data), orient='split') if json_data else pd.DataFrame()
    if df.empty or 'Prorrogado' not in df.columns or 'Líquido' not in df.columns:
        return ''

    # Determinar mês selecionado e mês anterior
    mes_sel = mes if mes and mes != 'todos' else datetime.now().strftime('%Y-%m')
    mes_dt = pd.to_datetime(mes_sel)
    mes_anterior = (mes_dt - pd.DateOffset(months=1)).strftime('%Y-%m')

    df['Mes'] = pd.to_datetime(df['Prorrogado']).dt.to_period('M').astype(str)

    df_fil_sel = filtrar_dataframe(df, tipo_doc, status, fornecedor, mes_sel)
    df_fil_ant = filtrar_dataframe(df, tipo_doc, status, fornecedor, mes_anterior)

    total_sel = df_fil_sel['Líquido'].sum() if not df_fil_sel.empty and 'Líquido' in df_fil_sel.columns else 0
    total_ant = df_fil_ant['Líquido'].sum() if not df_fil_ant.empty and 'Líquido' in df_fil_ant.columns else 0

    # Calcular variação percentual
    if total_ant == 0:
        if total_sel == 0:
            perc = 0
        else:
            perc = 100
    else:
        perc = ((total_sel - total_ant) / total_ant) * 100

    # Formatar bloco similar ao print (valor e variação com seta)
    arrow = '▲' if perc >= 0 else '▼'
    color = 'red' if perc >= 0 else 'green'
    perc_str = f"{abs(perc):.1f}%"

    # Nome do mês em português
    meses_pt = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    try:
        mes_nome_pt = meses_pt[mes_dt.month - 1]
    except Exception:
        mes_nome_pt = pd.to_datetime(mes_sel).strftime('%B')

    texto = html.Div([
        html.Div(f"Mês Atual: {mes_nome_pt}", style={'fontSize': '12px', 'color': '#666'}),
        html.Div([
            html.Span(arrow, style={'color': color, 'marginRight': '6px', 'fontSize': '14px'}),
            html.Span(perc_str, style={'fontWeight': '700', 'marginRight': '8px'}),
            html.Span('Comparado ao mês anterior', style={'fontSize': '11px', 'color': '#666', 'verticalAlign': 'middle'})
        ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'gap': '6px', 'marginTop': '6px'})
    ], style={'textAlign': 'center'})

    return texto


@app.callback(
    Output('total-aberto-delta', 'children'),
    Input('dropdown-mes', 'value'),
    Input('dropdown-tipo-doc', 'value'),
    Input('dropdown-status', 'value'),
    Input('dropdown-fornecedor', 'value'),
    Input('store-dados', 'data')
)
def atualizar_total_aberto_percent(mes, tipo_doc, status, fornecedor, json_data):
    """Calcula o percentual do que está em aberto sobre o total (Líquido) no mês selecionado."""
    df = pd.read_json(io.StringIO(json_data), orient='split') if json_data else pd.DataFrame()
    if df.empty or 'Prorrogado' not in df.columns or 'Líquido' not in df.columns or 'Saldo em Aberto' not in df.columns:
        return ''

    mes_sel = mes if mes and mes != 'todos' else datetime.now().strftime('%Y-%m')
    df['Mes'] = pd.to_datetime(df['Prorrogado']).dt.to_period('M').astype(str)

    df_fil = filtrar_dataframe(df, tipo_doc, status, fornecedor, mes_sel)

    total_geral = df_fil['Líquido'].sum() if not df_fil.empty else 0
    total_aberto = df_fil.loc[df_fil['Saldo em Aberto'] > 0, 'Saldo em Aberto'].sum() if not df_fil.empty else 0

    if total_geral == 0:
        perc = 0
    else:
        perc = (total_aberto / total_geral) * 100

    perc_str = f"{perc:.1f}%"

    # escolher uma figurinha (emoji) simples para colocar antes do percentual
    # emojis alterados para teste: 0%, bom, atenção, crítico
    if perc == 0:
        icon = '▫️'
    elif perc < 20:
        icon = '✅'
    elif perc < 50:
        icon = '⚠️'
    else:
        icon = '❗'

    # Nome do mês em português, similar ao cartão Total Geral
    meses_pt = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    try:
        mes_dt = pd.to_datetime(mes_sel)
        mes_nome_pt = meses_pt[mes_dt.month - 1]
    except Exception:
        mes_nome_pt = pd.to_datetime(mes_sel).strftime('%B') if mes_sel else ''

    # Exibir o mês e, abaixo, o ícone seguido do percentual com rótulo ao lado
    bloco = html.Div([
        html.Div(f"Mês Atual: {mes_nome_pt}", style={'fontSize': '12px', 'color': '#666', 'marginBottom': '6px'}),
        html.Div([
            html.Span(icon, style={'marginRight': '8px', 'fontSize': '14px'}),
            html.Span(perc_str, style={'fontWeight': '700', 'color': '#dc3545', 'marginRight': '8px'}),
            html.Span('Percentual em aberto', style={'fontSize': '11px', 'color': '#666', 'alignSelf': 'center'})
        ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'gap': '6px'})
    ], style={'textAlign': 'center'})

    return bloco


@app.callback(
    Output('total-liquidado-delta', 'children'),
    Input('dropdown-mes', 'value'),
    Input('dropdown-tipo-doc', 'value'),
    Input('dropdown-status', 'value'),
    Input('dropdown-fornecedor', 'value'),
    Input('store-dados', 'data')
)
def atualizar_total_liquidado_percent(mes, tipo_doc, status, fornecedor, json_data):
    """Calcula o percentual liquidado (Total Liquidado / Total Geral) para o mês selecionado."""
    df = pd.read_json(io.StringIO(json_data), orient='split') if json_data else pd.DataFrame()
    if df.empty or 'Prorrogado' not in df.columns or 'Líquido' not in df.columns or 'Saldo em Aberto' not in df.columns:
        return ''

    mes_sel = mes if mes and mes != 'todos' else datetime.now().strftime('%Y-%m')
    df['Mes'] = pd.to_datetime(df['Prorrogado']).dt.to_period('M').astype(str)

    df_fil = filtrar_dataframe(df, tipo_doc, status, fornecedor, mes_sel)

    total_geral = df_fil['Líquido'].sum() if not df_fil.empty else 0
    total_liquidado = df_fil.loc[df_fil['Saldo em Aberto'] == 0, 'Líquido'].sum() if not df_fil.empty else 0

    if total_geral == 0:
        # Se não há contas no período, considera-se 100% liquidado (nenhuma pendência)
        perc = 100
    else:
        perc = (total_liquidado / total_geral) * 100

    perc_str = f"{perc:.1f}%"

    # emojis/símbolos: crítico, atenção, bom, perfeito. Alto % é bom.
    if perc < 50:
        icon = '❗'  # Crítico
    elif perc < 80:
        icon = '⚠️'  # Atenção
    elif perc < 100:
        icon = '✅'  # Bom
    else:  # perc == 100
        icon = '🏆'  # Perfeito

    # Nome do mês em português
    meses_pt = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    try:
        mes_dt = pd.to_datetime(mes_sel)
        mes_nome_pt = meses_pt[mes_dt.month - 1]
    except Exception:
        mes_nome_pt = pd.to_datetime(mes_sel).strftime('%B') if mes_sel else ''

    bloco = html.Div([
        html.Div(f"Mês Atual: {mes_nome_pt}", style={'fontSize': '12px', 'color': '#666', 'marginBottom': '6px'}),
        html.Div([
            html.Span(icon, style={'marginRight': '8px', 'fontSize': '14px'}),
            html.Span(perc_str, style={'fontWeight': '700', 'color': '#28a745', 'marginRight': '8px'}),
            html.Span('Percentual liquidado', style={'fontSize': '11px', 'color': '#666', 'alignSelf': 'center'})
        ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'gap': '6px'})
    ], style={'textAlign': 'center'})

    return bloco


@app.callback(
    Output('contas-vencidas-delta', 'children'),
    Input('store-dados', 'data'),
    Input('dropdown-mes', 'value')
)
def atualizar_contas_vencidas_delta(json_data, mes):
    """Exibe o número de documentos vencidos de meses anteriores."""
    df = pd.read_json(io.StringIO(json_data), orient='split') if json_data else pd.DataFrame()
    if df.empty or 'Prorrogado' not in df.columns or 'Saldo em Aberto' not in df.columns:
        return ''

    # Garante que 'Prorrogado' é datetime
    df['Prorrogado'] = pd.to_datetime(df['Prorrogado'], errors='coerce')

    # Define o primeiro dia do mês atual
    hoje = datetime.now()
    primeiro_dia_mes_atual = hoje.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # Filtra documentos de meses anteriores que ainda estão em aberto
    df_vencidos_anterior = df[
        (df['Prorrogado'] < primeiro_dia_mes_atual) &
        (df['Saldo em Aberto'] > 0)
    ]
    
    num_vencidos_anterior = len(df_vencidos_anterior)

    if num_vencidos_anterior > 0:
        icon = '⚠️'
        text = f"{num_vencidos_anterior} - Doc(s) Vencido(s) em Meses Anteriores"
        color = "#ff6207"  # Laranja
    else:
        icon = '✅'
        text = "Nenhum doc vencido"
        color = '#28a745'  # Verde
        
    # Determinar o nome do mês selecionado
    mes_sel = mes if mes and mes != 'todos' else datetime.now().strftime('%Y-%m')
    meses_pt = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    try:
        mes_dt = pd.to_datetime(mes_sel)
        mes_nome_pt = meses_pt[mes_dt.month - 1]
    except Exception:
        mes_nome_pt = pd.to_datetime(mes_sel).strftime('%B') if mes_sel else ''

    bloco = html.Div([
        html.Div(f"Mês Atual: {mes_nome_pt}", style={'fontSize': '12px', 'color': '#666', 'marginBottom': '6px'}),
        html.Div([
            html.Span(icon, style={'marginRight': '8px', 'fontSize': '14px'}),
            html.Span(text, style={'fontWeight': '700', 'color': color})
        ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'gap': '6px'})
    ], style={'textAlign': 'center'})

    return bloco

@app.callback(
    Output('grafico-vencimentos', 'figure'),
    Output('grafico-tipos-documento', 'figure'),
    Output('grafico-fornecedores', 'figure'),
    Output('tabela-contas', 'columns'),
    Output('tabela-contas', 'data'),
    Input('dropdown-tipo-doc', 'value'),
    Input('dropdown-status', 'value'),
    Input('dropdown-fornecedor', 'value'),
    Input('dropdown-agrupamento', 'value'),
    Input('dropdown-mes', 'value'),
    Input('store-dados', 'data')
)
def atualizar_graficos_e_tabela(tipo_doc, status, fornecedor, agrupamento, mes, json_data):
    df = pd.read_json(io.StringIO(json_data), orient='split') if json_data else pd.DataFrame()
    
    # FIX: Converter a coluna de data de string (do JSON) para datetime
    if 'Prorrogado' in df.columns:
        df['Prorrogado'] = pd.to_datetime(df['Prorrogado'], errors='coerce')

    if df.empty or 'Mes' not in df.columns:
        empty_fig = go.Figure()
        return empty_fig, empty_fig, empty_fig, [], []

    # Se nenhum mês foi selecionado, usar o mês corrente
    mes_selecionado = mes if mes and mes != 'todos' else datetime.now().strftime("%Y-%m")

    df_filtrado = filtrar_dataframe(df, tipo_doc, status, fornecedor, mes_selecionado)

    # Gráficos
    # Substituir: mostrar os 5 dias do mês selecionado com maior volume de pagamentos (soma de 'Líquido')
    fig_vencimentos = go.Figure()
    if not df_filtrado.empty and 'Prorrogado' in df_filtrado.columns and 'Saldo em Aberto' in df_filtrado.columns:
        df_days = df_filtrado.dropna(subset=['Prorrogado']).copy()
        if not df_days.empty:
            df_days['Dia'] = df_days['Prorrogado'].dt.strftime('%d/%m/%Y')
            daily_sum = df_days.groupby('Dia', as_index=False)['Saldo em Aberto'].sum()
            # top5 dias por saldo em aberto
            top5 = daily_sum.nlargest(5, 'Saldo em Aberto').sort_values('Saldo em Aberto', ascending=True)

            # preparar texto formatado em moeda brasileira para aparecer dentro das barras
            top5['Saldo_fmt'] = top5['Saldo em Aberto'].apply(lambda v: format_brl(v))

            # destacar o maior dia (último da ordenação ascendente)
            colors = ['#636efa'] * len(top5)
            if len(colors) > 0:
                colors[-1] = '#f39c12'  # destaque laranja para o maior

            # decidir posição do texto: se a barra for pequena em relação ao máximo, colocar fora (à direita)
            max_val = top5['Saldo em Aberto'].max() if not top5.empty else 0
            positions = []
            text_colors = []
            for v in top5['Saldo em Aberto']:
                if max_val > 0 and v < (max_val * 0.12):
                    positions.append('outside')
                    text_colors.append('#000')
                else:
                    positions.append('inside')
                    text_colors.append('#fff' if v == max_val else '#000')

            fig_vencimentos = px.bar(
                top5,
                x='Saldo em Aberto',
                y='Dia',
                orientation='h',
                title='Top 5 Dias por Volume de Pagamentos (Saldo em Aberto)',
                labels={'Saldo em Aberto': 'Saldo (R$)', 'Dia': 'Dia'},
                text='Saldo_fmt'
            )
            # aplicar cores e posições/cores de texto por ponto
            fig_vencimentos.update_traces(marker_color=colors, textposition=positions, textfont=dict(color=text_colors), insidetextanchor='middle')
            fig_vencimentos.update_layout(title_x=0.5, xaxis_title='Valor (R$)', yaxis_title='Dia', uniformtext_minsize=8)
            fig_vencimentos.update_xaxes(tickprefix='R$ ', tickformat=',.2f', automargin=True)

    fig_tipos = go.Figure()
    if not df_filtrado.empty and 'Tipo Doc.' in df_filtrado.columns:
        tipos_count = df_filtrado['Tipo Doc.'].value_counts().reset_index()
        tipos_count.columns = ['Tipo Doc.', 'count']
        fig_tipos = px.pie(
            tipos_count,
            values='count',
            names='Tipo Doc.',
            title='Distribuição por Tipo de Documento'
        )
    fig_tipos.update_layout(title_x=0.5)

    fig_fornecedores = go.Figure()
    if not df_filtrado.empty and 'Nome Fantasia Agente' in df_filtrado.columns and 'Saldo em Aberto' in df_filtrado.columns:
        forn_valores = df_filtrado.groupby('Nome Fantasia Agente', as_index=False)['Saldo em Aberto'].sum()
        forn_valores = forn_valores.nlargest(10, 'Saldo em Aberto')
        fig_fornecedores = px.bar(
            forn_valores,
            x='Saldo em Aberto',
            y='Nome Fantasia Agente',
            orientation='h',
            title='Top 10 Fornecedores por Valor em Aberto'
        )
    fig_fornecedores.update_layout(title_x=0.5, yaxis={'categoryorder': 'total ascending'})

    # Tabela - MODIFICAÇÃO AQUI para agrupar por DIA e FILIAL em uma única linha
    if agrupamento == 'diario' and 'Prorrogado' in df_filtrado.columns:
        df_aux = df_filtrado.copy()
        df_aux = df_aux.sort_values(['Prorrogado', 'Líquido'], ascending=[True, False])
        col_order = ['Data', 'Nome Fantasia Agente', 'Tipo Doc.', 'Número Doc.', 'AP', 'Líquido', 'Saldo em Aberto', 'Complemento']
        todas_as_linhas = []
        df_aux['Data_fmt'] = df_aux['Prorrogado'].dt.strftime('%d/%m/%Y')

        for data_str in df_aux['Data_fmt'].dropna().unique():
            lancamentos_dia = df_aux[df_aux['Data_fmt'] == data_str].copy()
            linha_data = pd.DataFrame([{
                'Data': f"Data: {data_str}",
                'Nome Fantasia Agente': None,
                'Tipo Doc.': None,
                'Número Doc.': None,
                'AP': None,
                'Líquido': None,
                'Saldo em Aberto': None,
                'Complemento': None
            }])

            lanc = lancamentos_dia[['Data_fmt', 'Nome Fantasia Agente', 'Tipo Doc.', 'Número Doc.', 'AP', 'Líquido', 'Saldo em Aberto', 'Complemento']].copy()
            lanc = lanc.rename(columns={'Data_fmt': 'Data'})

            total_liq = lancamentos_dia['Líquido'].sum(min_count=1)
            total_saldo = lancamentos_dia['Saldo em Aberto'].sum(min_count=1)
            linha_total = pd.DataFrame([{
                'Data': f"Total do dia {data_str}",
                'Nome Fantasia Agente': None,
                'Tipo Doc.': None,
                'Número Doc.': None,
                'AP': None,
                'Líquido': total_liq,
                'Saldo em Aberto': total_saldo,
                'Complemento': None
            }])

            linha_data = linha_data[[c for c in col_order if c in linha_data.columns]]
            lanc = lanc[[c for c in col_order if c in lanc.columns]]
            linha_total = linha_total[[c for c in col_order if c in linha_total.columns]]

            todas_as_linhas.append(linha_data)
            todas_as_linhas.append(lanc)
            todas_as_linhas.append(linha_total)

        if todas_as_linhas:
            df_tabela = pd.concat(todas_as_linhas, ignore_index=True, sort=False)
            final_cols = [c for c in col_order if c in df_tabela.columns]
            df_tabela = df_tabela[final_cols]
        else:
            df_tabela = pd.DataFrame(columns=[c for c in col_order])
            
    elif agrupamento == 'dia_filial' and 'Prorrogado' in df_filtrado.columns and 'Nome Fantasia Filial' in df_filtrado.columns:
        df_aux = df_filtrado.copy()
        df_aux = df_aux.sort_values(['Prorrogado', 'Nome Fantasia Filial', 'Líquido'], 
                                   ascending=[True, True, False])
        col_order = ['Data', 'Nome Fantasia Agente', 'Tipo Doc.', 
                    'Número Doc.', 'AP', 'Líquido', 'Saldo em Aberto', 'Complemento']
        todas_as_linhas = []
        df_aux['Data_fmt'] = df_aux['Prorrogado'].dt.strftime('%d/%m/%Y')

        # Agrupar por DATA e FILIAL juntos
        for data_str in df_aux['Data_fmt'].dropna().unique():
            df_data = df_aux[df_aux['Data_fmt'] == data_str]
            
            # dicionário simples de abreviações para nomes longos de filial
            abreviacoes_filial = {
                'ALTIPLANO ENGENHARIA LTDA': 'ALTIPLANO',
                'ATP SERVIÇO EM ACESSO POR CORDAS E TREINAMENTOS LTDA': 'ATP'
            }

            # Agrupar por filial dentro da data
            for filial in df_data['Nome Fantasia Filial'].dropna().unique():
                df_filial = df_data[df_data['Nome Fantasia Filial'] == filial]
                filial_display = abreviacoes_filial.get(filial.strip().upper(), filial)

                # Linha de cabeçalho combinando DATA e FILIAL
                linha_cabecalho = pd.DataFrame([{
                    'Data': f"Data: {data_str} - Filial: {filial_display}",
                    'Nome Fantasia Agente': None,
                    'Tipo Doc.': None,
                    'Número Doc.': None,
                    'AP': None,
                    'Líquido': None,
                    'Saldo em Aberto': None,
                    'Complemento': None
                }])

                # Lançamentos da filial
                lanc = df_filial[['Data_fmt', 'Nome Fantasia Agente', 
                                'Tipo Doc.', 'Número Doc.', 'AP', 'Líquido', 
                                'Saldo em Aberto', 'Complemento']].copy()
                lanc = lanc.rename(columns={'Data_fmt': 'Data'})

                # Total da filial
                total_filial_liq = df_filial['Líquido'].sum(min_count=1)
                total_filial_saldo = df_filial['Saldo em Aberto'].sum(min_count=1)
                linha_total_filial = pd.DataFrame([{
                    'Data': f"Total {data_str} - {filial_display}",
                    'Nome Fantasia Agente': None,
                    'Tipo Doc.': None,
                    'Número Doc.': None,
                    'AP': None,
                    'Líquido': total_filial_liq,
                    'Saldo em Aberto': total_filial_saldo,
                    'Complemento': None
                }])

                # Adicionar à lista
                todas_as_linhas.append(linha_cabecalho)
                todas_as_linhas.append(lanc)
                todas_as_linhas.append(linha_total_filial)
            
            # Total do dia (todas as filiais)
            total_dia_liq = df_data['Líquido'].sum(min_count=1)
            total_dia_saldo = df_data['Saldo em Aberto'].sum(min_count=1)
            linha_total_dia = pd.DataFrame([{
                'Data': f"TOTAL DIA: {data_str}",
                'Nome Fantasia Agente': None,
                'Tipo Doc.': None,
                'Número Doc.': None,
                'AP': None,
                'Líquido': total_dia_liq,
                'Saldo em Aberto': total_dia_saldo,
                'Complemento': None
            }])
            
            todas_as_linhas.append(linha_total_dia)
        
        # Combinar todos os dados
        if todas_as_linhas:
            df_tabela = pd.concat(todas_as_linhas, ignore_index=True, sort=False)
            final_cols = [c for c in col_order if c in df_tabela.columns]
            df_tabela = df_tabela[final_cols]
        else:
            df_tabela = pd.DataFrame(columns=[c for c in col_order])

    else:
        colunas_exibir = ['Prorrogado', 'Nome Fantasia Agente', 'Tipo Doc.', 'Número Doc.', 'AP', 'Líquido', 'Saldo em Aberto', 'Complemento']
        colunas_disponiveis = [col for col in colunas_exibir if col in df_filtrado.columns]
        df_tabela = df_filtrado[colunas_disponiveis].copy()

        # Ordenar decrescente pela coluna 'Líquido' se existir
        if 'Líquido' in df_tabela.columns:
            df_tabela = df_tabela.sort_values('Líquido', ascending=False)

        if 'Prorrogado' in df_tabela.columns:
            df_tabela['Prorrogado'] = df_tabela['Prorrogado'].dt.strftime('%d/%m/%Y')
            cols = df_tabela.columns.tolist()
            idx = cols.index('Prorrogado')
            cols[idx] = 'Data'
            df_tabela.columns = cols

    if 'Tipo Doc.' in df_tabela.columns:
        df_tabela['Tipo Doc.'] = df_tabela['Tipo Doc.'].astype(str).str.strip()

    # Remover valores None/NaN que aparecem como 'None' na tabela: usar string vazia
    df_tabela = df_tabela.fillna('')
    # Alguns valores já foram convertidos para a string 'None' em etapas anteriores;
    # substituir essas strings indesejadas por string vazia para não aparecerem na UI.
    df_tabela = df_tabela.replace({
        'None': '',
        'nan': '',
        'NaN': '',
        'NaT': ''
    })

    columns = [{"name": i, "id": i} for i in df_tabela.columns]

    money_cols = ['Líquido', 'Saldo em Aberto']
    for col in columns:
        if col['id'] in money_cols:
            col['type'] = 'numeric'
            col['format'] = Format(
                scheme=Scheme.fixed,
                precision=2,
                group=Group.yes,
                group_delimiter='.',
                decimal_delimiter=',',
                symbol=Symbol.yes,
                symbol_prefix='R$ '
            )

    data = df_tabela.to_dict('records')

    return fig_vencimentos, fig_tipos, fig_fornecedores, columns, data


@app.callback(
    Output('card-gastos-mensais', 'figure'),
    Input('dropdown-tipo-doc', 'value'),
    Input('dropdown-status', 'value'),
    Input('dropdown-fornecedor', 'value'),
    Input('store-dados', 'data'),
    Input('dropdown-mes', 'value')
)
def atualizar_card_gastos_mensais(tipo_doc, status, fornecedor, json_data, mes):
    df = pd.read_json(io.StringIO(json_data), orient='split') if json_data else pd.DataFrame()
    if df.empty or 'Prorrogado' not in df.columns or 'Líquido' not in df.columns:
        return go.Figure()

    # Aplicar filtros semelhantes
    mes_sel = mes if mes and mes != 'todos' else None
    df['Mes'] = pd.to_datetime(df['Prorrogado']).dt.to_period('M').astype(str)
    df_fil = filtrar_dataframe(df, tipo_doc, status, fornecedor, mes_sel) if mes_sel else filtrar_dataframe(df, tipo_doc, status, fornecedor, None)

    # Preparar meses fixos JAN..DEZ (PT-BR)
    meses_pt_abrev = ['JAN','FEV','MAR','ABR','MAI','JUN','JUL','AGO','SET','OUT','NOV','DEZ']
    df['Mes_Period'] = pd.to_datetime(df['Prorrogado']).dt.to_period('M')
    monthly_all = df.groupby(df['Mes_Period'])['Líquido'].sum().reset_index()
    # Criar mapa mês->valor
    monthly_map = {p.strftime('%Y-%m'): v for p, v in zip(monthly_all['Mes_Period'], monthly_all['Líquido'])}

    # Construir arrays para 12 meses do ano corrente
    ano_atual = datetime.now().year
    x = meses_pt_abrev
    y = []
    for i in range(1,13):
        key = f"{ano_atual}-{i:02d}"
        y.append(monthly_map.get(key, 0))

    # Identificar maior e menor para destaque
    max_idx = int(pd.Series(y).idxmax()) if any(v != 0 for v in y) else None
    min_idx = int(pd.Series(y).idxmin()) if any(v != 0 for v in y) else None

    cores = ['#36cbbd'] * 12
    if max_idx is not None:
        cores[max_idx] = '#f39c12'  # destaque em laranja para o maior
    if min_idx is not None:
        cores[min_idx] = '#9aa0a6'  # cor neutra para o menor

    fig = go.Figure()
    fig.add_trace(go.Bar(x=x, y=y, marker_color=cores, showlegend=False))

    # Linha tracejada com a média dos 12 meses
    try:
        mean_val = float(pd.Series(y).mean())
    except Exception:
        mean_val = 0.0

    # adicionar linha horizontal tracejada representando a média
    fig.add_trace(go.Scatter(
        x=x,
        y=[mean_val] * len(x),
        mode='lines',
        line=dict(color='#ff6b6b', width=1.5, dash='dash'),
        hoverinfo='skip',
        showlegend=False
    ))

    # anotação removida: mantemos apenas a linha tracejada (sem texto no card)

    fig.update_layout(margin=dict(l=8, r=8, t=18, b=40), showlegend=False,
                      xaxis=dict(tickmode='array', tickangle=0, tickfont=dict(size=9)),
                      yaxis=dict(visible=False),
                      plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')

    return fig

# Client-side callback para impressão: chama window.print() no navegador
app.clientside_callback(
    "function(n_clicks){ if(n_clicks>0){ window.print(); } return ''; }",
    Output('print-output', 'children'),
    Input('btn-print', 'n_clicks')
)

# Rodar o app
if __name__ == '__main__':
    app.run(debug=True)

#server = app.server  # necessário para o Render, ai favor não apagar.

#if __name__ == '__main__': # necessário para o Render, ai favor não apagar.
#    app.run_server(host="0.0.0.0", port=8050, debug=True) # necessário para o Render, ai favor não apagar.