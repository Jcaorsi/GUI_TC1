"""
plotter.py - Manejo de gráficos
Se encarga de crear y personalizar los gráficos de las señales
"""

import matplotlib.pyplot as plt
import numpy as np

class Plotter:
    """
    Clase que maneja la creación y personalización de gráficos
    """
    
    def __init__(self):
        """
        Inicializa el graficador con colores predefinidos
        """
        # Colores para cada canal (hasta 10 canales)
        self.colores = [
            '#FF6B6B',  # Rojo
            '#4ECDC4',  # Turquesa
            '#45B7D1',  # Azul claro
            '#FFA07A',  # Salmon
            '#98D8C8',  # Verde menta
            '#FFD93D',  # Amarillo
            '#6BCB77',  # Verde
            '#C44569',  # Rosa oscuro
            '#A8E6CF',  # Verde pastel
            '#FF8B94'   # Rosa claro
        ]
    
    def graficar_canales(self, ax, df, canales):
        """
        Grafica los canales seleccionados en el eje proporcionado
        
        Args:
            ax: Eje de matplotlib donde graficar
            df: DataFrame con los datos
            canales (list): Lista de nombres de canales a graficar
        """
        # Limpiar el gráfico anterior
        ax.clear()
        
        # Obtener la columna de tiempo (primera columna)
        tiempo = df[df.columns[0]]
        
        # Graficar cada canal
        for i, canal in enumerate(canales):
            # Seleccionar color (ciclar si hay más canales que colores)
            color = self.colores[i % len(self.colores)]
            
            # Obtener datos del canal
            voltaje = df[canal]
            
            # Graficar
            ax.plot(tiempo, voltaje, 
                   label=f'Canal {canal}',
                   color=color,
                   linewidth=1.5,
                   alpha=0.8)  # Transparencia
        
        # Configurar el gráfico
        self.configurar_grafico(ax)
        
        # Agregar leyenda si hay múltiples canales
        if len(canales) > 1:
            ax.legend(loc='upper right', framealpha=0.9)
    
    def configurar_grafico(self, ax):
        """
        Configura el aspecto visual del gráfico
        
        Args:
            ax: Eje de matplotlib a configurar
        """
        # Títulos y etiquetas
        ax.set_title('Señales del Osciloscopio', fontsize=14, fontweight='bold', pad=15)
        ax.set_xlabel('Tiempo (s)', fontsize=11)
        ax.set_ylabel('Voltaje (V)', fontsize=11)
        
        # Grilla
        ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
        ax.set_axisbelow(True)  # Grilla detrás de las líneas
        
        # Formato de los ejes
        ax.ticklabel_format(style='scientific', axis='x', scilimits=(-6, -6))
        
        # Márgenes
        ax.margins(x=0.01)
    
    def graficar_con_estadisticas(self, ax, df, canal, mostrar_promedio=True, mostrar_rms=False):
        """
        Grafica un canal con líneas de referencia estadísticas
        
        Args:
            ax: Eje de matplotlib
            df: DataFrame con los datos
            canal (str): Nombre del canal
            mostrar_promedio (bool): Si mostrar línea de promedio
            mostrar_rms (bool): Si mostrar línea RMS
        """
        # Limpiar
        ax.clear()
        
        # Obtener datos
        tiempo = df[df.columns[0]]
        voltaje = df[canal]
        
        # Graficar señal principal
        ax.plot(tiempo, voltaje, label=f'Canal {canal}', 
               color=self.colores[0], linewidth=1.5)
        
        # Calcular y mostrar estadísticas
        if mostrar_promedio:
            promedio = voltaje.mean()
            ax.axhline(y=promedio, color='red', linestyle='--', 
                      linewidth=1, label=f'Promedio: {promedio:.3f} V', alpha=0.7)
        
        if mostrar_rms:
            rms = np.sqrt(np.mean(voltaje**2))
            ax.axhline(y=rms, color='orange', linestyle='--', 
                      linewidth=1, label=f'RMS: {rms:.3f} V', alpha=0.7)
            ax.axhline(y=-rms, color='orange', linestyle='--', 
                      linewidth=1, alpha=0.7)
        
        # Configurar
        self.configurar_grafico(ax)
        ax.legend(loc='upper right', framealpha=0.9)
    
    def graficar_fft(self, ax, df, canal):
        """
        Grafica la Transformada Rápida de Fourier (análisis de frecuencia)
        
        Args:
            ax: Eje de matplotlib
            df: DataFrame con los datos
            canal (str): Nombre del canal
        """
        # Limpiar
        ax.clear()
        
        # Obtener datos
        tiempo = df[df.columns[0]]
        voltaje = df[canal]
        
        # Calcular paso de tiempo
        dt = tiempo.iloc[1] - tiempo.iloc[0]
        
        # Calcular FFT
        fft = np.fft.fft(voltaje)
        freq = np.fft.fftfreq(len(voltaje), dt)
        
        # Solo frecuencias positivas
        mask = freq > 0
        freq = freq[mask]
        fft_mag = np.abs(fft[mask])
        
        # Graficar
        ax.plot(freq, fft_mag, color=self.colores[2], linewidth=1.5)
        
        # Configurar
        ax.set_title(f'Análisis de Frecuencia - Canal {canal}', 
                    fontsize=14, fontweight='bold', pad=15)
        ax.set_xlabel('Frecuencia (Hz)', fontsize=11)
        ax.set_ylabel('Magnitud', fontsize=11)
        ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
        ax.set_xlim(left=0)
    
    def comparar_canales(self, ax, df, canal1, canal2):
        """
        Crea un gráfico XY comparando dos canales
        
        Args:
            ax: Eje de matplotlib
            df: DataFrame con los datos
            canal1 (str): Primer canal (eje X)
            canal2 (str): Segundo canal (eje Y)
        """
        # Limpiar
        ax.clear()
        
        # Obtener datos
        x = df[canal1]
        y = df[canal2]
        
        # Graficar
        ax.plot(x, y, color=self.colores[4], linewidth=1.5, alpha=0.7)
        
        # Configurar
        ax.set_title(f'Comparación: Canal {canal1} vs Canal {canal2}', 
                    fontsize=14, fontweight='bold', pad=15)
        ax.set_xlabel(f'Canal {canal1} (V)', fontsize=11)
        ax.set_ylabel(f'Canal {canal2} (V)', fontsize=11)
        ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
        ax.set_axisbelow(True)