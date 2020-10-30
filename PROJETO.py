import pandas as pd
import urllib
import sys
data =int(input('Qual a data será analizada? formato AAAAMMDD: \n'))
        
data=int(data)
#colnames=['Data','Cod Moeda', 'Tipo', 'Moeda', 'Taxa Compra','Taxa Venda','Paridade Compra','Paridade Venda'] 

#base de dados com as taxas
colnames=['Cod Moeda', 'Tipo', 'Moeda', 'Taxa Compra','Taxa Venda','Paridade Compra','Paridade Venda'] 

while True:
    try:
        df=pd.read_csv('https://www4.bcb.gov.br/Download/fechamento/{}.csv'.format(data),decimal=',',delimiter=';',names=colnames, header=None, skipfooter=1,engine='python')
        break
    except urllib.error.HTTPError as err:
        print ("x \nO arquivo de cotação não existe")
        sys.exit(0)
        
        
#para moedas do tipo A, o valor em dolar é a taxa de compra dividido pela cotação do dolar
#para moedas do tipo B, o valor em dolar é a própria paridade
def conversor(x):
    if x['Tipo']=='A':
        return  x['Taxa Compra']/df[df['Moeda']=='USD']['Taxa Compra'].values[0]
    else:
        return x['Paridade Compra']
    
#ou seja, leia-se, por exemplo, 1 euro está 1,18 dolares...
df['Cotação em USD']=df.apply(conversor, axis=1)


#base de dados com nome dos paises e códigos.20
while True:
    try:
        df2=pd.read_csv('https://www4.bcb.gov.br/Download/fechamento/M{}.csv'.format(data),decimal=',',delimiter=';', engine='python')
        break
    except urllib.error.HTTPError as err:
        print ("x \n o arquivo com nome dos paises não existe")
        sys.exit(0)

#Como mais de um código aparecia em mais de um país, utilizou-se o código abaixo
#para por os paises que possuem o mesmo código na mesma linha separados por vírgulas.
df2['País'] = df2['País'].str.split(', ')
alinhar=df2.groupby('Código').agg({'País':'sum','Nome':'first'}).reset_index()
#Removendo colchetes dos nomes dos paises
alinhar['País'] = alinhar['País'].astype(str).str[1:-1]

#Criou-se uma coluna no df com os nomes para verificação dos códigos que contém em ambos os dataframes.
alinhar['Comparou']=alinhar['Código'].isin(df['Cod Moeda'])

# Foi especificada a condição True junto ao nomes dos paises com o objetivo de gerar um novo dataframe que será
#adicionado ao dataframe com as cotações.
dfvalores=alinhar[alinhar['Comparou']==True][['País','Nome']]

#Criou-se então a coluna com os nomes dos paises
df[['Nomes dos Paises','Nome']]=dfvalores.values

#limpeza de caracteres inválidos na coluna Nomes dos Paises
regras = {" ":'' , "'REPUBLICA'":'' , "'REPUBLICADA'":'' , ",,":',' , '"':'' , "'":''}
for chave,valor in regras.items():
    df['Nomes dos Paises'] = df['Nomes dos Paises'].str.replace(chave,valor)
    
#somente um exemplo dos paises da última linha (um código) após utilizar a função do groupby
df['Nomes dos Paises'][154]

#o símbolo da moeda com menor cotação
aa=df[df['Taxa Compra']==df['Taxa Compra'].min()]['Moeda'].values[0]

#o valor da cotação desta moeda frente ao dólar na data especificada.
bb=df['Cotação em USD'].min()

#nome do pais de origem da moeda
cc=df[df['Cotação em USD']==df['Cotação em USD'].min()]['Nomes dos Paises'].values[0]

#o símbolo da moeda com menor cotação
aa2=df[df['Taxa Compra']==df['Taxa Compra'].min()]['Nome'].values[0]


aa3=df[df['Moeda']=='USD']['Nome'][0]


print('\nO símbolo da moeda com menor cotação é: \n{}'.format(aa))

print('\nO valor da cotação desta moeda frente ao dólar na data especificada segue a seguinte relação: \n1 {} vale {} {}'.format(aa2, bb, aa3))

if len(cc.split(','))==1:
    print('\nO nome do país de origem dessa moeda é: \n{}'.format(cc))
else:
    print('\nHá {} países com essa moeda, sendo eles: \n{}'.format(len(cc.split(',')),cc))
                                                                

input("press close to exit") 

#Como não é uma API, o código precisará ser atualizado caso ocorram modificações nos arquivos publicados pelo banco central 

