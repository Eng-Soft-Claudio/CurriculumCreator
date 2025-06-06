# CurriculumCreator

Gerador de currículos compatíveis com sistemas ATS (Applicant Tracking Systems), desenvolvido em Python.

---

## Descrição

O CurriculumCreator é uma ferramenta que automatiza a criação de currículos em formato .docx, otimizados para leitura por sistemas ATS. Utiliza Tkinter para a interface do usuário e a biblioteca ReportLab para gerar documentos estruturados a partir dos dados fornecidos.

---

## Funcionalidades

- Interface gráfica intuitiva para preenchimento dos dados.
- Geração automática de currículos em formato .pdf.
- Otimizado para sistemas ATS (Applicant Tracking Systems).
- Seções dinâmicas para adicionar múltiplas experiências profissionais e formações acadêmicas.
- Pré-visualização da estrutura do currículo através dos campos da interface.
- Permite salvar o currículo gerado em local escolhido pelo usuário.

---

## Tecnologias Utilizadas

- Python 3.x
- Tkinter (para a interface gráfica)
- ReportLab (para geração de PDF)

---

## Instalação

Clone o repositório:

    git clone https://github.com/Eng-Soft-Claudio/CurriculumCreator.git

Navegue até o diretório do projeto:

    cd CurriculumCreator

Crie e ative um ambiente virtual (opcional, mas recomendado):

    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows

Instale as dependências:

    pip install -r requirements.txt

---

## Uso

Execute o script principal para gerar o currículo:

    python curriculum.py

O script solicitará as informações necessárias e gerará um arquivo curriculo.docx no diretório atual.

---

## Estrutura do Projeto


    CurriculumCreator/
    ├── curriculum.py
    ├── requirements.txt
    └── README.md

---

## Licença

Direitos Autorais 2025 Cláudio de Lima Tosta

É concedida permissão, gratuita, a qualquer pessoa que obtenha uma cópia deste software e dos arquivos de documentação associados (o "Software"), para lidar com o Software sem restrições, incluindo, entre outras, os direitos de usar, copiar, modificar, mesclar, publicar, distribuir, sublicenciar e/ou vender cópias do Software, e para permitir que as pessoas a quem o Software é fornecido o façam, sujeito às seguintes condições:

O aviso de direitos autorais acima e este aviso de permissão devem ser incluídos em todas as cópias ou partes substanciais do Software.

O SOFTWARE É FORNECIDO "NO ESTADO EM QUE SE ENCONTRA", SEM GARANTIA DE QUALQUER TIPO, EXPRESSA OU IMPLÍCITA, INCLUINDO, MAS NÃO SE LIMITANDO ÀS GARANTIAS DE COMERCIALIZAÇÃO, ADEQUAÇÃO A UM DETERMINADO FIM E NÃO VIOLAÇÃO. EM NENHUMA HIPÓTESE OS AUTORES OU TITULARES DOS DIREITOS AUTORAIS SERÃO RESPONSÁVEIS POR QUALQUER RECLAMAÇÃO, DANOS OU OUTRA RESPONSABILIDADE, SEJA EM UMA AÇÃO CONTRATUAL, ATO ILÍCITO OU DE OUTRA FORMA, DECORRENTE DE, DE OU EM CONEXÃO COM O SOFTWARE OU O USO OU OUTRAS NEGOCIAÇÕES NO SOFTWARE.

---

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

---