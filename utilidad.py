import matplotlib.pyplot as plt
import random

# genero valores aleatorios de alpha
alpha_costo = random.uniform(0.001, 0.1)
alpha_beneficio = random.uniform(0.001, 0.1)

# defino las funciones de beneficio y de costo
def costo(contaminacion):
    return -0.9 * (100 - 100 * np.exp(-alpha_costo * contaminacion))

def beneficio(contaminacion):
    return 100 - (100 * np.exp(-alpha_beneficio * contaminacion))

# genero los valores de contaminacion
contaminacion = np.linspace(0, 100, 1000)

# calculo los costos y beneficios respectivos
costo_valores = costo(contaminacion)
beneficio_valores = beneficio(contaminacion)

# grafico la funcion de costo
plt.figure(figsize=(10, 6))
plt.plot(contaminacion, costo_valores)
plt.title(f'funcion de costo (alpha = {alpha_costo:.4f})')
plt.xlabel('contaminacion')
plt.ylabel('costo')
plt.grid(True)
plt.show()

# grafico la funcion de beneficio
plt.figure(figsize=(10, 6))
plt.plot(contaminacion, beneficio_valores)
plt.title(f'funcion de beneficio (alpha = {alpha_beneficio:.4f})')
plt.xlabel('contaminacion')
plt.ylabel('beneficio')
plt.grid(True)
plt.show()

# grafico las dos juntas
plt.figure(figsize=(10, 6))
plt.plot(contaminacion, costo_valores, label='costo')
plt.plot(contaminacion, beneficio_valores, label='beneficio')

# calculo y grafico la suma de las dos
sum_valores = costo_valores + beneficio_valores
plt.plot(contaminacion, sum_valores, label='Sum')

# encuentro y grafico el maximo de la suma
max_sum = np.max(sum_valores)
max_index = np.argmax(sum_valores)
max_contaminacion = contaminacion[max_index]

plt.plot(max_contaminacion, max_sum, 'ro', label='suma maxima')

plt.title('costo, beneficio, y suma de las dos')
plt.xlabel('contaminacion')
plt.ylabel('valor')
plt.legend()
plt.grid(True)
plt.show()

print(f"suma maxima: {max_sum:.2f} en el nivel de contaminacion:   {max_contaminacion:.2f}")