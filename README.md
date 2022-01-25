# Projeto Ap Coders
 
Como rodar a aplicação:

1: Você precisará instalar Python, MySQL e XAMPP na sua máquina
2: Quando terminar o processo de instalação das três tecnologias, estabeleça uma conexão através do XAMPP
3: Acesse um server local através do MySQL Workbench
4: Copie e cole o texto dentro de scriptsql.txt, localizado no diretório do programa, para dentro do campo de SQLFile e aperte o símbolo de raio para executá-lo
![image](https://user-images.githubusercontent.com/85131296/150904803-34503bea-2338-4634-91d3-b00a941fcfc8.png)

5: Agora que você tem uma base de dados, abra config.ini com o bloco de notas e altere os valores dentro para aqueles que se adequem a sua base de dados
6: Com tudo isso pronto abra o prompt de comando e usando o comando cd vá até a pasta onde está armazenado o código
7: digite "python AppGestao.py" sem aspas e o programa irá ser executado

As tecnologias utilizadas foram Pycharm, MySQL Workbench, Python e MySQL

Não houve padrão de implementação utilizado

Foram adicionadas colunas primary key a todas as tabelas

As colunas da tabela inquilinos são: nome, idade, sexo, telefone, email e inq_id
As colunas da tabela unidades são: uni_id, proprietario, condomínio e endereco
As colunas da tabela despesas são: descricao, tipo_despesa, valor, vencimento_fatura, status_pagamento, fk_uni_id e des_id

