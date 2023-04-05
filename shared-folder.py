import os
import http.server
import socketserver
import urllib.parse
import tkinter as tk

class DownloadButtonHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def list_directory(self, path):
        try:
            # Copia del método original en la clase base
            list = os.listdir(path)
        except OSError:
            self.send_error(404, "Directorio no encontrado")
            return None

        list.sort(key=lambda a: a.lower())
        if f := self.send_head():
            try:
                # Agregar un botón de descarga para cada directorio en la lista
                display_path = urllib.parse.unquote(self.path, errors='surrogatepass')
                title = 'Descargar todo el directorio "{}"'.format(display_path)
                download_button = '<a href="{}" download="{}.zip"><button>{}</button></a>'.format(
                    self.path + '.zip', display_path, title)
                self.wfile.write(download_button.encode('utf-8'))
                
                # Copia del código original en la clase base
                self.wfile.write(b"<hr>\n<ul>\n")
                for name in list:
                    fullname = os.path.join(path, name)
                    displayname = linkname = name
                    # Append / for directories or @ for symbolic links
                    if os.path.isdir(fullname):
                        displayname = name + "/"
                        linkname = name + "/"
                    if os.path.islink(fullname):
                        displayname = name + "@"
                    self.wfile.write(b'<li><a href="%s">%s</a></li>\n'
                                      % (urllib.parse.quote(linkname, errors='surrogatepass'),
                                         urllib.parse.quote(displayname, errors='surrogatepass')))
                self.wfile.write(b"</ul>\n")
            except:
                pass

def start_server():
    PORT = int(port_entry.get())
    DIRECTORY = directory_entry.get()

    # Obtener la ruta absoluta del directorio especificado por el usuario
    abs_directory = os.path.abspath(DIRECTORY)

    # Configurar el manejador para servir archivos estáticos desde el directorio especificado
    Handler = http.server.SimpleHTTPRequestHandler
    os.chdir(abs_directory)

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Sirviendo en el puerto {PORT}")
        print(f"Abre un navegador y visita http://localhost:{PORT}/ para acceder a {DIRECTORY}")
        httpd.serve_forever()

# Crear la ventana principal de la aplicación
root = tk.Tk()
root.title("Compartir Directorio")
root.maxsize(1000, 400)

# Crear un frame para los inputs
input_frame = tk.Frame(root)

# Crear los inputs de puerto y directorio
port_label = tk.Label(input_frame, text="Puerto:")
port_label.pack(side=tk.LEFT)

port_entry = tk.Entry(input_frame)
port_entry.pack(side=tk.LEFT)

directory_label = tk.Label(input_frame, text="Directorio:")
directory_label.pack(side=tk.LEFT)

directory_entry = tk.Entry(input_frame)
directory_entry.pack(side=tk.LEFT)

# Agregar el frame de inputs a la ventana principal
input_frame.pack()

# Crear el botón de iniciar el servidor
start_button = tk.Button(root, text="Iniciar Servidor", command=start_server)
start_button.pack()

# Iniciar el loop principal de la UI
root.mainloop()
