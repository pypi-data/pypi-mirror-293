## Currencies Formatter
informações sobre a currencies lib
>
### Installing

```bash
$ pip install currencies_lib
```
>

### Uso

1. Execute a aplicação: `python main.py`
2. Insira o saldo inicial quando solicitado.
3. Adicione gastos usando a interface gráfica. Utilize "`-`" (menos) para adicionar um valor recebido, ao invés de gasto (Ao invés de ser reduzido como normalmente seria, é somado ao Saldo).
4. Exporte para Excel ou PDF para guardar as informações.
5. Importe arquivos exportados em Excel para editar informações salvas.

- Para exportar para Excel ou PDF, você só precisa adicionar um nome para o arquivo que será salvo e em seguida escolher um local para salvar o arquivo. Caso você não coloque um nome, ele receberá o nome padrão como "Controle de Gastos.(formato)" 

- Para importar arquivos, apenas o formato Excel está disponível (atualmente). Para importar, basta selecionar a opção de importação (Você pode fornecer um valor temporário no saldo inicial apenas para chegar à tela da aplicação) e escolher um arquivo que tenha sido exportado pela aplicação anteriormente. Arquivos feitos manualmente ou por outras aplicações possivelmente não irão funcionar, a importação é exclusiva para arquivos feitos por este modelo.

>

### Example of use

```python
from currencies_lib import BRL

value = 1250.50
result = BRL(value, currency_symbol=True)
print(result)
#> "R$ 1.250,50"
```
or
```python
from currencies_lib import *

value = 1250.50
result = Currency_Formatter.EUR(value, currency_symbol=True, eur_sign=True)
print(result)
#> "€ 1.250,50"
```
Don't import directly. The commom use is "from currencies lib ..."

>

### Contribuição

Sinta-se à vontade para [abrir uma issue](link_para_abrir_issue) ou enviar um [pull request](link_para_pull_request).

>