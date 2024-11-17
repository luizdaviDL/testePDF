import base64
import io
import tabula
import pandas as pd
from IPython.display import display
from PyPDF2 import PdfReader

class Model:
    def lerpdf(self, value):
        top = 100
        left = 50
        bottom = 500
        right = 400
        linhas_agrupadas = []
        # Decodifica a string base64
        pdf_data = base64.b64decode(value)
        pdf_file = io.BytesIO(pdf_data)  # Cria um objeto BytesIO a partir dos dados decodificados

        # Usa o tabula para extrair as tabelas do PDF
        # tabula.read_pdf retorna uma lista de DataFrames
        try:
            tabelas = tabula.read_pdf(pdf_file, pages='all', multiple_tables=True, guess=False, lattice=True, area=[top, left, bottom, right])
            columnValue = [i for i in tabelas[0].columns]
            tabelasC = self.putTables(columnValue, tabelas)
            
            df = pd.concat(tabelasC, ignore_index=True)  
            df = self.convert('Lote',df)
            df = self.convert('Ag.\rorigem',df)
            i = 0          
            while i < len(df) - 1:   # Não precisa verificar a última linha
                linha_atual = df.iloc[i].values.tolist()   
                proximo = df.iloc[i+1].values.tolist()   
                
                if  isinstance(linha_atual[0], str)  and pd.isna(proximo[0]):
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


    def convert(self, value, df):
        df =df
        # Specify columns that should retain the '0000' format and convert them to strings with zero-padding
        columns_to_format = [value]  # Replace with actual column names

        
        for col in columns_to_format:
            if value=='Lote':
                df[col] = df[col].apply(lambda x: '{:05.0f}'.format(x) if pd.notnull(x) and isinstance(x, (float, int)) else x)
            else:
                df[col] = df[col].apply(lambda x: '{:04.0f}'.format(x) if pd.notnull(x) and isinstance(x, (float, int)) else x)

        return df


    def putTables(self, coluns, tabelas):
        tabelas = tabelas
        for i in tabelas:
            if len(i.columns) == len(coluns):
                i.columns = coluns  # Assign the new column names
            elif len(i.columns) < len(coluns):
                # If there are fewer columns, pad the list with empty strings or some default value
                i.columns = coluns[:len(i.columns)] + [''] * (len(coluns) - len(i.columns))
            else:
                # If there are more columns, truncate the list to match
                i.columns = coluns[:len(i.columns)]
        return tabelas