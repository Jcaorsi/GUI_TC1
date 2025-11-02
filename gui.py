"""
gui.py - Interfaz gráfica del visor de osciloscopio
Maneja todos los elementos visuales y la interacción con el usuario
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from data_handler import DataHandler
from plotter import Plotter

class OsciloscopioGUI:
    """
    Clase que maneja toda la interfaz gráfica
    """
    
    def __init__(self, root):
        """
        Inicializa la ventana y todos sus componentes
        
        Args:
            root: Ventana principal de tkinter
        """
        self.root = root
        self.root.title("Visor de Osciloscopio - CSV")
        self.root.geometry("1200x700")
        
        # Crear instancias de las clases auxiliares
        self.data_handler = DataHandler()
        self.plotter = Plotter()
        
        # Variable para guardar los datos cargados
        self.df = None
        
        # Crear los componentes de la interfaz
        self.crear_menu()
        self.crear_panel_control()
        self.crear_area_grafico()
        
    def crear_menu(self):
        """
        Crea la barra de menú superior
        """
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menú Archivo
        archivo_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=archivo_menu)
        archivo_menu.add_command(label="Abrir CSV", command=self.abrir_archivo)
        archivo_menu.add_separator()
        archivo_menu.add_command(label="Salir", command=self.root.quit)
        
        # Menú Ayuda
        ayuda_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=ayuda_menu)
        ayuda_menu.add_command(label="Acerca de", command=self.mostrar_acerca_de)
    
    def crear_panel_control(self):
        """
        Crea el panel lateral con botones y controles
        """
        # Frame (contenedor) para los controles
        panel = tk.Frame(self.root, width=200, bg='lightgray', relief=tk.RAISED, borderwidth=2)
        panel.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Título del panel
        tk.Label(panel, text="Controles", font=('Arial', 14, 'bold'), bg='lightgray').pack(pady=10)
        
        # Botón para cargar archivo
        btn_cargar = tk.Button(panel, text="📁 Cargar CSV", command=self.abrir_archivo,
                               width=20, height=2, bg='#4CAF50', fg='white', font=('Arial', 10, 'bold'))
        btn_cargar.pack(pady=10)
        
        # Separador visual
        ttk.Separator(panel, orient='horizontal').pack(fill='x', pady=10)
        
        # Label para mostrar información del archivo
        tk.Label(panel, text="Canales:", font=('Arial', 10, 'bold'), bg='lightgray').pack(pady=5)
        
        # Frame para los checkboxes de canales
        self.frame_canales = tk.Frame(panel, bg='lightgray')
        self.frame_canales.pack(pady=5)
        
        # Lista para guardar las variables de los checkboxes
        self.canal_vars = []
        
        # Botón para actualizar gráfico
        self.btn_graficar = tk.Button(panel, text="🔄 Actualizar Gráfico", 
                                      command=self.actualizar_grafico,
                                      width=20, height=2, bg='#2196F3', fg='white',
                                      state=tk.DISABLED)
        self.btn_graficar.pack(pady=20)
        
        # Información del archivo
        self.info_label = tk.Label(panel, text="No hay archivo cargado", 
                                   bg='lightgray', wraplength=180, justify=tk.LEFT)
        self.info_label.pack(pady=10)
    
    def crear_area_grafico(self):
        """
        Crea el área donde se mostrará el gráfico
        """
        # Frame para el gráfico
        frame_grafico = tk.Frame(self.root)
        frame_grafico.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Crear figura de matplotlib
        self.fig = Figure(figsize=(10, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Señales del Osciloscopio")
        self.ax.set_xlabel("Tiempo (s)")
        self.ax.set_ylabel("Voltaje (V)")
        self.ax.grid(True, alpha=0.3)
        
        # Crear canvas para mostrar el gráfico en tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame_grafico)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Agregar toolbar de matplotlib (zoom, pan, guardar)
        toolbar = NavigationToolbar2Tk(self.canvas, frame_grafico)
        toolbar.update()
    
    def abrir_archivo(self):
        """
        Abre un diálogo para seleccionar un archivo CSV y lo carga
        """
        # Abrir diálogo para seleccionar archivo
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo CSV",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
        )
        
        # Si el usuario seleccionó un archivo
        if archivo:
            try:
                # Cargar los datos usando el DataHandler
                self.df = self.data_handler.cargar_csv(archivo)
                
                # Actualizar la interfaz
                self.crear_checkboxes_canales()
                self.actualizar_info_archivo(archivo)
                self.btn_graficar.config(state=tk.NORMAL)
                
                # Graficar automáticamente
                self.actualizar_grafico()
                
                messagebox.showinfo("Éxito", "Archivo cargado correctamente")
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{str(e)}")
    
    def crear_checkboxes_canales(self):
        """
        Crea checkboxes para cada canal detectado en el CSV
        """
        # Limpiar checkboxes anteriores
        for widget in self.frame_canales.winfo_children():
            widget.destroy()
        
        self.canal_vars = []
        
        # Obtener nombres de columnas (excepto la primera que es el tiempo)
        columnas = self.df.columns[1:]
        
        # Crear un checkbox por cada canal
        for col in columnas:
            var = tk.BooleanVar(value=True)  # Por defecto seleccionado
            chk = tk.Checkbutton(self.frame_canales, text=f"Canal {col}", 
                                variable=var, bg='lightgray')
            chk.pack(anchor=tk.W, padx=10)
            self.canal_vars.append((col, var))
    
    def actualizar_info_archivo(self, archivo):
        """
        Actualiza la información mostrada sobre el archivo cargado
        
        Args:
            archivo: Ruta del archivo cargado
        """
        nombre = archivo.split('/')[-1]  # Obtener solo el nombre del archivo
        num_puntos = len(self.df)
        num_canales = len(self.df.columns) - 1
        
        info = f"Archivo: {nombre}\n\n"
        info += f"Canales: {num_canales}\n"
        info += f"Puntos: {num_puntos}"
        
        self.info_label.config(text=info)
    
    def actualizar_grafico(self):
        """
        Actualiza el gráfico con los canales seleccionados
        """
        if self.df is None:
            return
        
        # Obtener canales seleccionados
        canales_seleccionados = [col for col, var in self.canal_vars if var.get()]
        
        if not canales_seleccionados:
            messagebox.showwarning("Advertencia", "Selecciona al menos un canal")
            return
        
        # Limpiar gráfico anterior
        self.ax.clear()
        
        # Graficar usando el Plotter
        self.plotter.graficar_canales(self.ax, self.df, canales_seleccionados)
        
        # Redibujar canvas
        self.canvas.draw()
    
    def mostrar_acerca_de(self):
        """
        Muestra información sobre la aplicación
        """
        messagebox.showinfo("Acerca de", 
                          "Visor de Osciloscopio v1.0\n\n"
                          "Aplicación para visualizar datos CSV\n"
                          "de osciloscopios de laboratorio")