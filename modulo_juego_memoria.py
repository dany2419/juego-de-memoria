import customtkinter as ctk
import random
import pygame
import numpy as np
from pygame import mixer
from tkinter import messagebox

# Configuración inicial
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")
pygame.init()
mixer.init()

# Función para generar sonidos
def generar_sonido(frecuencia, duracion=0.8):
    tasa_muestreo = 44100
    t = np.linspace(0, duracion, int(tasa_muestreo * duracion))
    onda = 0.5 * np.sin(2 * np.pi * frecuencia * t)
    return pygame.sndarray.make_sound((onda * 32767).astype(np.int16))

# Crear sonidos
try:
    exito = generar_sonido(800)
    error = generar_sonido(200)
except Exception as e:
    print(f"Error en sonidos: {e}")
    exito, error = None, None

ventana = ctk.CTk()
ventana.title("AcompañaIA - Juego de Memoria Mejorado")
ventana.geometry("600x600")
ventana.configure(bg="#3a2945")

# Variables del juego
botones = []
orden_original = []
orden_usuario = []

# Crear marco para instrucciones
marco_instrucciones = ctk.CTkFrame(ventana, fg_color="#CEC2DA")
marco_instrucciones.pack(pady=15)

ctk.CTkLabel(marco_instrucciones, 
            text="💡 Tocá los cuadrados en el orden en que brillaron",
            text_color="#2d2d2d",
            font=("Arial", 14, "bold")).pack(padx=20, pady=20)

def reiniciar_juego():
    global orden_original, orden_usuario
    orden_original = random.sample(range(6), 6)
    orden_usuario = []
    reproducir_secuencia()

def reproducir_secuencia():
    delay = 500
    for i, idx in enumerate(orden_original):
        ventana.after(i * delay, lambda idx=idx: resaltar_boton(idx))
        ventana.after((i + 1) * delay, lambda idx=idx: desresaltar_boton(idx))

def resaltar_boton(idx):
    botones[idx].configure(fg_color="#ffd700", hover_color="#ffd700")

def desresaltar_boton(idx):
    botones[idx].configure(fg_color="#6a5acd", hover_color="#7b68ee")

def verificar_respuesta(idx):
    orden_usuario.append(idx)
    
    if orden_usuario == orden_original[:len(orden_usuario)]:
        if len(orden_usuario) == 6:
            if exito: exito.play()
            messagebox.showinfo("¡Éxito!", "¡Secuencia completa correctamente!")
            reiniciar_juego()
    else:
        if error: error.play()
        messagebox.showwarning("Error", "Secuencia incorrecta. Intenta de nuevo")
        reiniciar_juego()

# Marco para los botones del juego
marco_botones = ctk.CTkFrame(ventana, fg_color="#f0e6f7")
marco_botones.pack(pady=20)

# Crear 6 botones en grid 3x2
for i in range(6):
    btn = ctk.CTkButton(
        marco_botones,
        text=str(i+1),
        width=100,
        height=100,
        fg_color="#6a5acd",
        hover_color="#7b68ee",
        font=("Arial", 20, "bold"),
        text_color="white",
        corner_radius=10,
        command=lambda i=i: verificar_respuesta(i)
    )
    btn.grid(row=i//3, column=i%3, padx=15, pady=15)  # Cambiado a grid 3x2
    botones.append(btn)

# Botón de reinicio
ctk.CTkButton(ventana, 
             text="🔁 Iniciar Juego", 
             command=reiniciar_juego,
             fg_color="#4CAF50",
             hover_color="#45a049",
             font=("Arial", 14, "bold")).pack(pady=20)

ventana.mainloop()