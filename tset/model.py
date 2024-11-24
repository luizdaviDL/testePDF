import base64
import io
import tabula
import pandas as pd
from IPython.display import display
#from PyPDF2 import PdfReader

class Model:
    def lerpdf(self, value):
        top = 100
        left = 50
        bottom = 500
        right = 400
        linhas_agrupadas = []
        # Decodifica a string base64
        #pdf_data = base64.b64decode(value)
        #pdf_file = io.BytesIO(pdf_data)  # Cria um objeto BytesIO a partir dos dados decodificados

        # Usa o tabula para extrair as tabelas do PDF
        # tabula.read_pdf retorna uma lista de DataFrames
        try:
            tabelas = tabula.read_pdf(value, pages='all', multiple_tables=True, guess=False, lattice=True, area=[10, 50, 850, 560])
            columnValue = [i for i in tabelas[0].columns]
            tabelasC = self.putTables(columnValue, tabelas)
            
            df = pd.concat(tabelasC, ignore_index=True)  
            df = self.convert('Lote',df)
            df = self.convert('Ag.\rorigem',df)
            i = 0          
            while i < len(df) - 1:   # Não precisa verificar a última linha
                linha_atual = df.iloc[i].values.tolist()  
                linha_atualDt = self.is_date(linha_atual[0]) 
                
                proximo = df.iloc[i+1].values.tolist()   
                proximoDt = self.is_date(proximo[0]) 
                
                if  linha_atualDt ==True and proximoDt ==False or pd.isna(proximo[0]):
                    stringProximo = [i for i in proximo if isinstance(i, str)]
                    stringAtual = str(linha_atual[2])
                    contatenarValor = ' '.join([stringAtual, stringProximo[0]])
                    linha_atual[2] = contatenarValor                    
                    linhas_agrupadas.append(linha_atual)
                    # Skip the `proximo` row by incrementing `i` by 2
                    i += 2
                else:
                    linhas_agrupadas.append(linha_atual)
                    i += 1
            if i < len(df): #adicionar a ultima linha
                linhas_agrupadas.append(df.iloc[i].values.tolist())

            resultF = pd.DataFrame(linhas_agrupadas, columns=df.columns)
            #convertLote = self.convert('Lote',resultF)
            #convertAg = self.convert('Ag.\rorigem',convertLote)
            return resultF

        except Exception as e:
            print(f"Ocorreu um erro ao tentar extrair as tabelas: {e}")
            return None


    def is_date(self, value):
        try:
            if pd.isna(value):
                return False
            # Tentativa de converter a string para data no formato DD/MM/YYYY
            pd.to_datetime(value, format='%d/%m/%Y', errors='raise')
            return True
        except (ValueError, TypeError):   
            return False 

    def convert(self, value, df):
        df =df
        # Specify columns that should retain the '0000' format and convert them to strings with zero-padding
        columns_to_format = [value]  # Replace with actual column names

        
        for col in columns_to_format:
            if col in df.columns:  # Verifica se a coluna existe no DataFrame
                if value=='Lote':
                    df[col] = df[col].apply(lambda x: '{:05.0f}'.format(x) if pd.notnull(x) and isinstance(x, (float, int)) else x)
                else:
                    df[col] = df[col].apply(lambda x: '{:04.0f}'.format(x) if pd.notnull(x) and isinstance(x, (float, int)) else x) 

            else:
                return df
        return df


    def putTables(self, coluns, tabelas):
        tabelas_filtradas = []
        for i in tabelas:
            if i.shape[1] == 1:  # Verifica se a tabela tem apenas uma coluna
                continue  # Ignora essa tabela se tiver apenas uma coluna
            
            # Ajuste o número de colunas do DataFrame para corresponder ao número de colunas na lista `coluns`
            if len(i.columns) == len(coluns):
                i.columns = coluns  # Atribui diretamente os nomes das colunas
            elif len(i.columns) < len(coluns):
                # Adiciona colunas extras com valores vazios, para igualar o comprimento
                i = i.reindex(columns=range(len(coluns))).fillna('')  # Adiciona colunas vazias
                i.columns = coluns  # Define os nomes das colunas
            else:
                # Trunca as colunas extras para que correspondam ao número de colunas em `coluns`
                i = i.iloc[:, :len(coluns)]  # Seleciona apenas o número necessário de colunas
                i.columns = coluns
            
            tabelas_filtradas.append(i)  # Adiciona a tabela processada à lista final
        
        return tabelas_filtradas
    

if __name__ == '__main__':
    sa = '6269.pdf'

    da = Model().lerpdf(sa)