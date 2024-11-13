import dash
import dash_latex as dl
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import webbrowser
import threading
import os
#import pywebview
# Inicializar la aplicación Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

server = app.server  # Asegúrate de tener esto si necesitas exponer el servidor Flask



# Definición del diseño de la aplicación
app.layout = dbc.Container([
    html.H1("Calculadora en Varios Sistemas Numéricos (Flotantes)", style={'text-align': 'center', 'fontsize': '24x'}),
    html.Br(),
    dbc.Row([
        dbc.Col(html.Label("Sistema Numérico de Entrada para el Número 1:"), width=3),
        dbc.Col(html.Label("Sistema Numérico de Entrada para el Número 2:"), width=3),
        dbc.Col(html.Label("Orden de la división:"), width=3),
        dbc.Col(html.Label("Orden de la Potencia:"), width=3)
    ]),
    dbc.Row([
        dbc.Col(dcc.Dropdown(
            id='formato-entrada-numero1',
            options=[{'label': 'Decimal', 'value': 'dec'},
                     {'label': 'Binario', 'value': 'bin'},
                     {'label': 'Octal', 'value': 'oct'},
                     {'label': 'Hexadecimal', 'value': 'hex'}],
            value='dec'
        ), width=3),
        dbc.Col(dcc.Dropdown(
            id='formato-entrada-numero2',
            options=[{'label': 'Decimal', 'value': 'dec'},
                     {'label': 'Binario', 'value': 'bin'},
                     {'label': 'Octal', 'value': 'oct'},
                     {'label': 'Hexadecimal', 'value': 'hex'}],
            value='dec'
        ), width=3),
        
        dbc.Col(dcc.Dropdown(
            id='orden_div',
            options=[{'label': dl.DashLatex(r""" $${Número1} \over {Número2}.$$ """), 'value': 'num1/num2'},
                     {'label': dl.DashLatex(r""" $${Número2} \over {Número1}.$$ """), 'value': 'num2/num1'}],
            value = 'num1/num2 '
        ), width=3),
        
        dbc.Col(dcc.Dropdown(
            id='orden_pot',
            options=[{'label': dl.DashLatex(r""" $${Número1} ^ {Número2}.$$ """), 'value': 'num1^num2'},
                     {'label': dl.DashLatex(r""" $${Número2} ^ {Número1}.$$ """), 'value': 'num2^num1'}],
            value = 'num1^num2 '
        ), width=3)
    ]),
    
 html.Br(),
    dbc.Row([
        dbc.Col(html.Label("Número Raíz Cuadrada"), width=3),
        dbc.Col(html.Label("Número raíz Cúbica"), width=3)
    ]),
    
    dbc.Row([
        dbc.Col(dcc.Dropdown(
            id='raiz_cuad',
            options=[{'label': dl.DashLatex(r""" $$ \sqrt{Numero 1}$$ """), 'value': 'num1'},
                     {'label': dl.DashLatex(r""" $$ \sqrt{Numero 2}$$ """), 'value': 'num2'}],
            value = 'num1/num2 '
        ), width=3),
        dbc.Col(dcc.Dropdown(
            id='raiz_cub',
            options=[{'label': dl.DashLatex(r""" $${Número1}^{1 \over 3}$$ """), 'value': 'num1'},
                     {'label': dl.DashLatex(r""" $${Número2}^{1 \over 3}$$ """), 'value': 'num2'}],
            value = 'num1^num2 '
        ), width=3)
    ]),
    
    
    
    
    html.Br(),
    dbc.Input(id='numero1', type='text', placeholder="Primer número"),
    html.Br(),        
    dbc.Input(id='numero2', type='text', placeholder="Segundo número (solo para operaciones que lo requieren)"),
    
    html.Br(),
    html.Label("Operación:"),
  dbc.Row(
    [
        dbc.Col(
            dbc.Button(dl.DashLatex(r""" $$Suma$$ """), id='suma', n_clicks=0, color="primary", outline=False),
            md =4,  # Ajusta el tamaño en pantallas medianas y mayores
            className="mb-1"  # Margen inferior para evitar solapamiento vertical
        ),
        dbc.Col(
            dbc.Button(dl.DashLatex(r""" $$Resta$$ """), id='resta', n_clicks=0, color="primary", outline=False),
            md =4,
            className="mb-1"
        ),
        dbc.Col(
            dbc.Button(dl.DashLatex(r""" $$Multiplicación$$ """), id='multiplicacion', n_clicks=0, color="primary", outline=False),
            md =4,
            className="mb-1"
        ),
        dbc.Col(
            dbc.Button(dl.DashLatex(r""" $$División$$ """), id='division', n_clicks=0, color="primary", outline=False),
            md =4,
            className="mb-1"
        ),
        dbc.Col(
            dbc.Button(dl.DashLatex(r""" $$Potencia$$ """), id='potencia', n_clicks=0, color="primary", outline=False),
            md =4,
            className="mb-1"
        ),
        dbc.Col(
            dbc.Button(dl.DashLatex(r""" $$Raíz\ cuadrada$$ """), id='raiz-cuadrada', n_clicks=0, color="primary", outline=False),
            md =4,
            className="mb-1"
        ),
        dbc.Col(
            dbc.Button(dl.DashLatex(r""" $$Raíz\ cúbica$$ """), id='raiz-cubica', n_clicks=0, color="primary", outline=False),
            md =4,
            className="mb-1"
        )
    ],
    justify="center",
    #className="g-1"  # Espaciado entre las columnas
),

    html.Br(),
    html.Label("Formato de Salida:"),
    dcc.Dropdown(
        id='formato-salida',
        options=[{'label': 'Decimal', 'value': 'dec'},
                 {'label': 'Binario', 'value': 'bin'},
                 {'label': 'Octal', 'value': 'oct'},
                 {'label': 'Hexadecimal', 'value': 'hex'}],
        value='dec'
    ),
    html.Br(),
    html.H3("Resultado:", style={'text-align': 'center'}),
    html.Div(id='resultado', style={'font-size': '24px', 'font-weight': 'bold', 'text-align': 'center'})
])

# Función para convertir un número de cualquier base a decimal usando álgebra modular.
def a_decimal(numero_str, base):
    """
    Convierte un número en una base arbitraria a su valor en base decimal.
    
    :param numero_str: El número en formato de cadena, que puede tener una parte entera y decimal.
    :param base: La base en la que se encuentra el número (por ejemplo, 2 para binario, 16 para hexadecimal).
    :return: El número convertido a decimal como un número de punto flotante.
    """
    
    # Limpiar la entrada y convertir todo a minúsculas
    numero_str = numero_str.strip().lower()
    resultado = 0  # Inicializamos el resultado
    
    
    
    # Verificar si el número es negativo
    es_negativo = numero_str[0] == '-'  # Si el primer carácter es '-', es negativo
    if es_negativo:
        numero_str = numero_str[1:]  # Eliminar el signo negativo para procesar el número
    
    resultado = 0  # Inicializamos el resultado

    # Verificamos si el número tiene una parte decimal
    if '.' in numero_str:
        entero, decimal = numero_str.split('.')  # Dividimos la parte entera y decimal
        entero = entero[::-1]  # Invertimos la parte entera para procesar de derecha a izquierda

        # Convertimos la parte entera de la base a decimal
        for i, digito in enumerate(entero):
            resultado += int(digito, base) * (base ** i)

        # Convertimos la parte decimal
        decimales = 0
        for i, digito in enumerate(decimal):
            decimales += int(digito, base) * (base ** -(i + 1))
        resultado += decimales  # Sumamos la parte decimal al resultado

    else:
        numero_str = numero_str[::-1]  # Invertimos solo la parte entera
        for i, digito in enumerate(numero_str):
            resultado += int(digito, base) * (base ** i)

    # Si el número original era negativo, multiplicamos el resultado por -1
    if es_negativo:
        resultado = -resultado

    return resultado  # Retornamos el resultado en base decimal

def de_decimal(numero, base):
    """
    Convierte un número en base decimal a cualquier base especificada.
    
    :param numero: El número en base decimal.
    :param base: La base a la que queremos convertir el número (por ejemplo, 2 para binario, 16 para hexadecimal).
    :return: El número convertido a la base deseada como una cadena.
    """
    if numero is None:
        return "Resultado no válido"
    
    if base < 2 or base > 16:
        return "Base fuera de rango (debe ser entre 2 y 16)"
    
    if numero == 0:
        return "0"  # Si el número es 0, simplemente retornamos 0
    
    # Si el número es negativo, lo manejamos por separado
    signo = "-" if numero < 0 else ""
    numero = abs(numero)
    
    # Parte entera del número decimal
    entero = int(numero)  # Extraemos la parte entera
    decimal = numero - entero  # Calculamos la parte decimal
    resultado_entero = ""  # Iniciamos la cadena para la parte entera
    
    # Convertimos la parte entera a la base deseada
    while entero > 0:
        residuo = entero % base
        if residuo < 10:
            resultado_entero = str(residuo) + resultado_entero
        else:
            resultado_entero = chr(residuo - 10 + ord('A')) + resultado_entero
        entero //= base  # Dividimos entre base, descartando el residuo

    # Parte decimal del número
    resultado_decimal = ""  # Iniciamos la cadena para la parte decimal
    while decimal > 0 and len(resultado_decimal) < 20:  # Limitar la parte decimal a 20 dígitos
        decimal *= base  # Multiplicamos la parte decimal por la base
        digito = int(decimal)  # Extraemos la parte entera del nuevo valor
        if digito < 10:
            resultado_decimal += str(digito)
        else:
            resultado_decimal += chr(digito - 10 + ord('A'))
        decimal -= digito  # Restamos la parte entera para obtener la nueva parte decimal

    # Si la parte decimal existe, la agregamos al resultado final
    if resultado_decimal:
        return signo + resultado_entero + '.' + resultado_decimal
    else:
        return signo + resultado_entero  # Solo retornamos la parte entera si no hay parte decimal










# Callback para manejar la lógica de la calculadora y actualizar el resultado
@app.callback(
    Output('resultado', 'children'),
    [Input('formato-entrada-numero1', 'value'),
     Input('formato-entrada-numero2', 'value'),
     Input('formato-salida', 'value'),
     Input('numero1', 'value'),
     Input('numero2', 'value'),
     Input('suma', 'n_clicks'),
     Input('resta', 'n_clicks'),
     Input('multiplicacion', 'n_clicks'),
     Input('division', 'n_clicks'),
     Input('potencia', 'n_clicks'),
     Input('raiz-cuadrada', 'n_clicks'),
     Input('raiz-cubica', 'n_clicks'),
     Input('orden_div', 'value'),
     Input('orden_pot', 'value'),
     Input('raiz_cuad', 'value'),
     Input('raiz_cub', 'value')]
)
def actualizar_resultado(formato_entrada1, formato_entrada2, formato_salida, num1, num2, n_suma, n_resta, n_mult, n_div, n_pot, n_raiz_cuad, n_raiz_cub,
                         orden_div,orden_pot,raiz_cuad,raiz_cub):
    # Verificar si el callback fue disparado por una de las operaciones
    ctx = dash.callback_context
    if not ctx.triggered:
        return "Seleccione una operación."
    
    boton_presionado = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Si no hay números ingresados, no hacer nada
    if not num1:
        return "Por favor, ingrese un número."
    else:
        # Validar que el número ingresado corresponda al sistema seleccionado
        try:
            numero1_decimal = a_decimal(num1, {'bin': 2, 'oct': 8, 'hex': 16, 'dec': 10}[formato_entrada1])
        except ValueError:
            return f"El valor ingresado no es válido para el sistema {formato_entrada1} para el primer número."
        
        
    # Convertir num1 y num2 a decimal
    numero1_decimal = a_decimal(num1, {'bin': 2, 'oct': 8, 'hex': 16, 'dec': 10}[formato_entrada1])
    if numero1_decimal is None:
        return "Entrada no válida para el primer número."
    
    if num2:
        try:
            numero2_decimal = a_decimal(num2, {'bin': 2, 'oct': 8, 'hex': 16, 'dec': 10}[formato_entrada2])
        except ValueError:
            return f"El valor ingresado no es válido para el sistema {formato_entrada2} para el segundo número."
        if numero2_decimal is None:
            return "Entrada no válida para el segundo número."
    else:
        numero2_decimal = None
    resultado = None

    # Realizar la operación correspondiente solo si un botón fue presionado
    if boton_presionado == 'suma':
        if numero2_decimal is None:
            return "Ingrese el segundo número para la suma."
        resultado = numero1_decimal + numero2_decimal
        
    elif boton_presionado == 'resta':
        if numero2_decimal is None:
            return "Ingrese el segundo número para la resta."
        resultado = numero1_decimal - numero2_decimal
        
    elif boton_presionado == 'multiplicacion':
        if numero2_decimal is None:
            return "Ingrese el segundo número para la multiplicación."
        resultado = numero1_decimal * numero2_decimal
        
    elif boton_presionado == 'division':
        if orden_div == 'num1/num2':
            if numero2_decimal != 0 and numero2_decimal is not None: 
                resultado = numero1_decimal / numero2_decimal 
            else:
                return "Error: División por cero o ingrese denominador"
        else:
            if numero1_decimal != 0 and numero1_decimal is not None:
                resultado = numero2_decimal / numero1_decimal  
            else:
                return "Error: División por cero o ingrese denominador"
            
        
    elif boton_presionado == 'potencia':
        
        if orden_pot == 'num1^num2':
            if numero2_decimal is None:
                return "Ingrese el segundo número para la potencia."
            resultado = numero1_decimal ** numero2_decimal
            
        else:
            if numero2_decimal is None:
                return "Ingrese el segundo número para la potencia."
            resultado = numero2_decimal ** numero1_decimal
        
    elif boton_presionado == 'raiz-cuadrada':
        
        if raiz_cuad == 'num1':
            if numero1_decimal < 0:
                return "No se puede calcular la raíz cuadrada de un número negativo."
            resultado = numero1_decimal ** 0.5
        else:
            if numero2_decimal < 0:
                return "No se puede calcular la raíz cuadrada de un número negativo."
            resultado = numero2_decimal ** 0.5
        
    elif boton_presionado == 'raiz-cubica':
       if raiz_cuad == 'num1':
           if numero1_decimal < 0:
               return "No se puede calcular la raíz cuadrada de un número negativo."
           resultado = numero1_decimal ** (1/3)
       else:
           if numero2_decimal < 0:
               return "No se puede calcular la raíz cuadrada de un número negativo."
           resultado = numero2_decimal ** (1/3)

    # Convertir el resultado al formato de salida
    if resultado is not None:
        return de_decimal(resultado, {'bin': 2, 'oct': 8, 'hex': 16, 'dec': 10}[formato_salida])
    # else:
    #     return 'Defina la operación'
    return "Defina la operación"

# Ejecutar el servidor en localhost sin necesidad de internet
# if __name__ == '__main__':
#     app.run_server(debug=True, host='127.0.0.1', port=8050)


if __name__ == '__main__':
    # Cambia el host a '0.0.0.0' y usa el puerto de la variable de entorno
    port = int(os.environ.get('PORT', 8050))  # Render define la variable PORT automáticamente
    app.run_server(debug=True, host='0.0.0.0', port=port)
