<h1>organizador_planilha</h1>

<h2>Introdução</h2>

<p>O <strong>organizador_planilha</strong> é uma ferramenta prática para realizar consultas em bancos de dados MySQL e exportar os resultados para uma planilha Excel. Além disso, ele oferece funcionalidades para sanitizar nomes de colunas e dados, e organizar planilhas com base em uma coluna específica.</p>

<h2>Instalação</h2>

<p>Para instalar o <strong>organizador_planilha</strong>, execute:</p>

<pre><code>pip install organizador_planilha</code></pre>

<h2>Uso Básico</h2>
<h3>Importando o Pacote</h3>

<pre><code>from organizador_planilha import buscar_planilha, organizar_planilha</code></pre>

<h3>1. buscar_planilha(query, banco, servidor, senha, usuario, nome_planilha)</h3>

<p>Executa uma consulta SQL no banco de dados especificado e exporta os resultados para uma planilha Excel.</p>

<h4>Parâmetros:</h4>
<ul>
    <li><code>query</code> (str): A consulta SQL a ser executada.</li>
    <li><code>banco</code> (str): O nome do banco de dados.</li>
    <li><code>servidor</code> (str): O endereço do servidor MySQL.</li>
    <li><code>senha</code> (str): A senha para acessar o banco de dados.</li>
    <li><code>usuario</code> (str): O nome do usuário do banco de dados.</li>
    <li><code>nome_planilha</code> (str): O nome do arquivo Excel a ser gerado (sem extensão).</li>
</ul>

<h4>Exemplo de Uso:</h4>

<pre><code>buscar_planilha(
    query="SELECT * FROM minha_tabela",
    banco="meu_banco",
    servidor="localhost",
    senha="minha_senha",
    usuario="meu_usuario",
    nome_planilha="resultado_consulta"
)
</code></pre>

<h3>2. organizar_planilha(input_path, output_path, coluna_ordenar)</h3>

<p>Organiza uma planilha (em formato .csv ou .xlsx) com base em uma coluna específica e salva o resultado em um novo arquivo.</p>

<h4>Parâmetros:</h4>
<ul>
    <li><code>input_path</code> (str): Caminho para a planilha de entrada.</li>
    <li><code>output_path</code> (str): Caminho para salvar a planilha organizada.</li>
    <li><code>coluna_ordenar</code> (str): Nome da coluna pela qual a planilha deve ser organizada.</li>
</ul>

<h4>Exemplo de Uso:</h4>

<pre><code>organizar_planilha(
    input_path="dados.csv",
    output_path="dados_organizados.xlsx",
    coluna_ordenar="nome"
)
</code></pre>

<h2>Interface Gráfica</h2>

<p>O pacote também fornece uma interface gráfica para facilitar a interação com o usuário. Esta interface permite inserir os parâmetros da consulta SQL e executar o processo de forma interativa.</p>

<h3>Iniciando a Interface Gráfica</h3>

<p>Para iniciar a interface gráfica, use:</p>

<pre><code>from organizador_planilha import gui

gui.run()
</code></pre>

<h2>Exemplo de Uso</h2>
<h3>Script Completo</h3>

<pre><code>from organizador_planilha import buscar_planilha, organizar_planilha

# Executando uma consulta e gerando uma planilha Excel
buscar_planilha(
    query="SELECT * FROM minha_tabela",
    banco="meu_banco",
    servidor="localhost",
    senha="minha_senha",
    usuario="meu_usuario",
    nome_planilha="resultado_consulta"
)

# Organizando a planilha gerada com base na coluna 'nome'
organizar_planilha(
    input_path="resultado_consulta.xlsx",
    output_path="resultado_organizado.xlsx",
    coluna_ordenar="nome"
)
</code></pre>

<h2>Contribuição</h2>

<p>Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests no repositório do GitHub. Ao contribuir, siga as melhores práticas de codificação e inclua testes para suas mudanças.</p>
