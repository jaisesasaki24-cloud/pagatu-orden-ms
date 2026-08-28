import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import threading

def seleccionar_carpeta():
    carpeta = filedialog.askdirectory()
    if carpeta:
        txt_ruta.delete(0, tk.END)
        txt_ruta.insert(0, carpeta)

def analizar_proyecto():
    ruta_raiz = txt_ruta.get()
    if not ruta_raiz or not os.path.exists(ruta_raiz):
        messagebox.showerror("Error", "Por favor selecciona una carpeta de proyecto válida.")
        return

    # Extensiones o carpetas a omitir para no saturar el txt con binarios o dependencias pesadas
    carpetas_excluidas = {'.git', '.idea', '.vscode', 'target', 'build', 'node_modules', 'bin', 'obj'}
    extensiones_excluidas = {'.png', '.jpg', '.jpeg', '.gif', '.pdf', '.exe', '.dll', '.jar', '.class', '.zip', '.tar', '.gz'}

    btn_analizar.config(state=tk.DISABLED)
    progreso_lbl.config(text="Analizando y generando archivo...")
    
    def tarea():
        try:
            nombre_salida = "proyecto_completo_analisis.txt"
            ruta_salida = os.path.join(ruta_raiz, nombre_salida)

            arbol_texto = []
            archivos_contenido = []

            # Generar estructura de directorios y recopilar código
            for root, dirs, files in os.walk(ruta_raiz):
                # Modificar dirs in-place para omitir carpetas pesadas
                dirs[:] = [d for d in dirs if d not in carpetas_excluidas]
                
                rel_path = os.path.relpath(root, ruta_raiz)
                if rel_path == ".":
                    nivel = 0
                    arbol_texto.append(f"📁 {os.path.basename(root)}/")
                else:
                    nivel = rel_path.count(os.sep) + 1
                    indent = "    " * (nivel - 1) + "├── "
                    arbol_texto.append(f"{indent}📁 {os.path.basename(root)}/")

                sub_indent = "    " * nivel + "├── "
                for file in files:
                    if any(file.endswith(ext) for ext in extensiones_excluidas):
                        continue
                    arbol_texto.append(f"{sub_indent}📄 {file}")
                    
                    # Leer contenido del archivo de texto/código
                    archivo_path = os.path.join(root, file)
                    rel_file_path = os.path.relpath(archivo_path, ruta_raiz)
                    
                    try:
                        with open(archivo_path, 'r', encoding='utf-8', errors='ignore') as f:
                            contenido = f.read()
                        
                        archivos_contenido.append(f"\n{'='*80}\n")
                        archivos_contenido.append(f"ARCHIVO: {rel_file_path}\n")
                        archivos_contenido.append(f"{'='*80}\n\n")
                        archivos_contenido.append(contenido)
                        archivos_contenido.append("\n\n")
                    except Exception as e:
                        archivos_contenido.append(f"\n[No se pudo leer el archivo {rel_file_path}: {e}]\n")

            # Escribir el resultado completo en el txt
            with open(ruta_salida, 'w', encoding='utf-8') as salida:
                salida.write("="*80 + "\n")
                salida.write("ESTRUCTURA DEL PROYECTO\n")
                salida.write("="*80 + "\n\n")
                salida.write("\n".join(arbol_texto))
                salida.write("\n\n\n")
                salida.write("="*80 + "\n")
                salida.write("CONTENIDO DE LOS ARCHIVOS\n")
                salida.write("="*80 + "\n")
                salida.writelines(archivos_contenido)

            ventana.after(0, lambda: exito_proceso(ruta_salida))
        except Exception as e:
            ventana.after(0, lambda: error_proceso(str(e)))

    threading.Thread(target=tarea).start()

def exito_proceso(ruta):
    btn_analizar.config(state=tk.NORMAL)
    progreso_lbl.config(text="¡Análisis completado con éxito!")
    messagebox.showinfo("Éxito", f"El archivo TXT se ha generado correctamente en:\n{ruta}")

def error_proceso(err):
    btn_analizar.config(state=tk.NORMAL)
    progreso_lbl.config(text="Error en el proceso.")
    messagebox.showerror("Error", f"Ocurrió un error: {err}")

# Configuración de la interfaz gráfica (GUI)
ventana = tk.Tk()
ventana.title("Analizador de Proyectos a TXT")
ventana.geometry("550x300")
ventana.resizable(False, False)

# Estilo visual básico
from tkinter import font
fuente_titulo = font.Font(family="Helvetica", size=12, weight="bold")
fuente_normal = font.Font(family="Helvetica", size=10)

lbl_titulo = tk.Label(ventana, text="Generador de TXT de Estructura y Código", font=fuente_titulo)
lbl_titulo.pack(pady=15)

frame_ruta = tk.Frame(ventana)
frame_ruta.pack(pady=5, padx=20, fill=tk.X)

txt_ruta = tk.Entry(frame_ruta, font=fuente_normal)
txt_ruta.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))

btn_examinar = tk.Button(frame_ruta, text="Seleccionar Carpeta", command=seleccionar_carpeta, font=fuente_normal)
btn_examinar.pack(side=tk.RIGHT)

btn_analizar = tk.Button(ventana, text="Analizar y Generar TXT", command=analizar_proyecto, font=fuente_titulo, bg="#4CAF50", fg="white", padx=10, pady=5)
btn_analizar.pack(pady=20)

progreso_lbl = tk.Label(ventana, text="", font=fuente_normal, fg="gray")
progreso_lbl.pack(pady=5)

ventana.mainloop()