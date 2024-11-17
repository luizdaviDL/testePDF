import numpy as np
from datetime import datetime
import pandas as pd

# Função para verificar se o valor é uma data
def is_date(value):
    try:
        datetime.strptime(str(value), "%d/%m/%Y")  # Verifica o formato 'DD/MM/YYYY'
        return True
    except ValueError:
        return False

# Exemplo de DataFrame (como você forneceu)
data = {
    0: ['01/07/2024', np.nan, '01/07/2024', '02/07/2024', np.nan, np.nan, '02/07/2024'],
    1: [np.nan, '02-00-MIRI', np.nan, np.nan, np.nan, '03-00-XYZ', np.nan],
    2: [562.0, np.nan, 25.0, 150.0, np.nan, np.nan, 50.0],
    3: [12788.0, np.nan, 95.0, 500.0, np.nan, np.nan, 200.0],
    4: ['830 Online', np.nan, '70 recebida', '100 Online', np.nan, np.nan, '80 recebida'],
    5: ['5.621.278.800.604', np.nan, np.nan, '5.200.150.400.704', np.nan, np.nan, np.nan],
    6: ['10.080,00 C', np.nan, np.nan, '20.500,00 C', np.nan, np.nan, np.nan],
    7: [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]
}

# Criando o DataFrame
df = pd.DataFrame(data)

# Lista para armazenar as linhas agrupadas
linhas_agrupadas = []

# Iterando pelas linhas do DataFrame
for i in range(len(df) - 1):  # Não precisa verificar a última linha
    linha_atual = df.iloc[i]  # Linha atual
    linha_proxima = df.iloc[i + 1]  # Próxima linha

    # Verificando se o primeiro valor da linha atual não é uma data
    if not is_date(linha_atual[0]) and pd.isna(linha_atual[0]):  # Se for NaN
        # Verifica se a próxima linha também começa com NaN
        if pd.isna(linha_proxima[0]):
            # Se for o caso, une as duas linhas
            linha_unida = pd.concat([linha_atual, linha_proxima], axis=0)
            linhas_agrupadas.append(linha_unida)
        else:
            # Caso contrário, mantemos as linhas separadas
            linhas_agrupadas.append(linha_atual)
    else:
        # Quando a linha tem uma data, simplesmente adiciona a linha atual
        linhas_agrupadas.append(linha_atual)

# Verificando se a última linha foi adicionada (ela sempre deve ser, já que não tem próxima linha para verificar)
if len(df) > 0:
    linhas_agrupadas.append(df.iloc[-1])

# Convertendo as linhas agrupadas em um novo DataFrame
df_agrupado = pd.DataFrame(linhas_agrupadas).reset_index(drop=True)

# Exibindo o DataFrame final
print(df_agrupado)
