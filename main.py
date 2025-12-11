import os
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt


def conectar():
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="inventario"
        )
        return con
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"No se pudo conectar:\n{e}")
        return None
def mostrar_frame(frame):
    for f in (frame_inicio, frame_principal, frame_productos, frame_existencias, frame_movimientos):
        f.pack_forget()
    frame.pack(fill="both", expand=True)
ventana = tk.Tk()
ventana.title("Sistema de Inventario")
ventana.geometry("900x600")
ventana.config(bg="light green")

frame_todo = tk.Frame(ventana, bg="light blue")
frame_todo.pack(fill="both", expand=True)

frame_inicio = tk.Frame(frame_todo, bg="light pink")
frame_inicio.pack(fill="both", expand=True)

titulo = tk.Label(frame_inicio,
    text="SISTEMA DE CONTROL DE INVENTARIO (LA ESPERANZA)",
    font=("Arial Black", 16, "bold"),
    bg="violet",
    fg="white"
)
titulo.pack(pady=20)

texto = """Giro: Tienda Comercial
Ubicación: 114 Sanchez Colin
Contacto: 7131159271
Año de Fundación: 2015
Tipo de Servicio: Venta de Producto
Público Objetivo: General
Número de empleados: 3
Días y horarios de Servicio: Toda la Semana de 8 am a 9 pm
Infraestructura: 1 local, 1 bodega
Seguridad y permiso: Sí
Proveedores: 12 """

eti1 = tk.Label(frame_inicio, text=texto, bg="light blue", fg="#333333", font=("Colibri", 12))
eti1.pack(pady=10)

boton_entrar = tk.Button(
    frame_inicio,
    text="Entrar al Sistema",
    bg="light green",
    font=("Colibri", 11, "bold"),
    command=lambda: mostrar_frame(frame_principal)
)
boton_entrar.pack(pady=20)

frame_principal = tk.Frame(frame_todo, bg="light blue")

eti1 = tk.Label(frame_principal, text="Tienda la Esperanza",
    font=("Cambria", 18, "bold"), bg="light green", fg="#2b2b2b")
eti1.pack(pady=30)

eti2 = tk.Label(frame_principal, text="Selecciona una opción:",
    font=("Cambria", 12), bg="light pink", fg="#444")
eti2.pack(pady=10)


frame_productos = tk.Frame(frame_todo, bg="light yellow")

titulo_productos = tk.Label(frame_productos, text="PRODUCTOS",
    font=("Arial Black", 18, "bold"), bg="orange", fg="white")
titulo_productos.pack(pady=20)

tk.Label(frame_productos, text="Código").place(x=30, y=80)
tk.Label(frame_productos, text="Descripción").place(x=230, y=80)

pro_codigo = tk.Entry(frame_productos)
pro_codigo.place(x=90, y=80)

pro_descr = tk.Entry(frame_productos)
pro_descr.place(x=330, y=80)

tabla_pro = ttk.Treeview(frame_productos, columns=("codigo", "descripcion"), show="headings")
tabla_pro.heading("codigo", text="CÓDIGO")
tabla_pro.heading("descripcion", text="DESCRIPCIÓN")

tabla_pro.column("codigo", width=120)
tabla_pro.column("descripcion", width=200)

tabla_pro.place(x=30, y=140)

def mostrarPro():
    con = conectar()
    if not con: return
    c1 = con.cursor()
    c1.execute("SELECT * FROM productos")
    tabla_pro.delete(*tabla_pro.get_children())
    for fila in c1:
        tabla_pro.insert("", tk.END, values=fila)
    con.close()

def insertarPro():
    con = conectar()
    if not con: return
    c1 = con.cursor()
    c1.execute("INSERT INTO productos VALUES (%s,%s)", (pro_codigo.get(), pro_descr.get()))
    con.commit()
    mostrarPro()
    con.close()

def eliminarPro():
    con = conectar()
    if not con: return
    c1 = con.cursor()
    c1.execute("DELETE FROM productos WHERE pro_codigo_k = %s", (pro_codigo.get(),))
    con.commit()
    mostrarPro()
    con.close()

def buscarPro():
    con = conectar()
    if not con: return
    c1 = con.cursor()
    c1.execute("SELECT * FROM productos WHERE pro_codigo_k = %s", (pro_codigo.get(),))
    tabla_pro.delete(*tabla_pro.get_children())
    for fila in c1:
        tabla_pro.insert("", tk.END, values=fila)
    con.close()

def actualizarPro():
    con = conectar()
    if not con: return
    c1 = con.cursor()
    c1.execute("UPDATE productos SET pro_descripcion=%s WHERE pro_codigo_k=%s",
               (pro_descr.get(), pro_codigo.get()))
    con.commit()
    mostrarPro()
    con.close()

def generarE():
    #conexion base de datos
    con = conectar()
    c1 = con.cursor()
    #crear lista y diccionario
    valores = {}
    cc = []
    dd = []
    #sentencia para seleccionar datos
    c1.execute("select *from productos")
    x = 1
    for fila in c1:
        c,d = fila
        cc.insert(x,c)
        dd.insert(x,d)
        x = x+1
    print(cc,dd)
    valores = {"codigo": cc,
               "descripcion": dd}
    dataframe = pd.DataFrame(valores)
    dataframe.to_excel("./productos.xlsx",
                       index=False)
    #Mostrar archivo
    os.system("start EXCEL.EXE productos.xlsx")
    dataframe.to_excel("./productos.xlsx",
                       index=False)
tk.Button(frame_productos, text="Mostrar", width=12, command=mostrarPro).place(x=30, y=370)
tk.Button(frame_productos, text="Insertar", width=12, command=insertarPro).place(x=150, y=370)
tk.Button(frame_productos, text="Eliminar", width=12, command=eliminarPro).place(x=270, y=370)
tk.Button(frame_productos, text="Buscar", width=12, command=buscarPro).place(x=390, y=370)
tk.Button(frame_productos, text="Actualizar", width=12, command=actualizarPro).place(x=510, y=370)
tk.Button(frame_productos, text="Reporte", width=12, command=generarE).place(x=650, y=100)

tk.Button(frame_productos, text="Volver al menú", width=15,
          command=lambda: mostrar_frame(frame_principal)).place(x=720, y=20)

frame_existencias = tk.Frame(frame_todo, bg="light yellow")

titulo_existencias = tk.Label(frame_existencias, text="EXISTENCIAS",
    font=("Arial Black", 18, "bold"), bg="orange", fg="white")
titulo_existencias.pack(pady=20)

tk.Label(frame_existencias, text="Código").place(x=30, y=80)
tk.Label(frame_existencias, text="Lote").place(x=230, y=80)
tk.Label(frame_existencias, text="Cantidad").place(x=430, y=80)

ex_codigo = tk.Entry(frame_existencias)
ex_codigo.place(x=90, y=80)

ex_lote = tk.Entry(frame_existencias)
ex_lote.place(x=280, y=80)

ex_cantidad = tk.Entry(frame_existencias)
ex_cantidad.place(x=510, y=80)

tabla_ex = ttk.Treeview(frame_existencias, columns=("codigo","lote","cantidad"), show="headings")
tabla_ex.heading("codigo", text="CÓDIGO")
tabla_ex.heading("lote", text="LOTE")
tabla_ex.heading("cantidad", text="CANTIDAD")

tabla_ex.column("codigo", width=120)
tabla_ex.column("lote", width=200)
tabla_ex.column("cantidad", width=100)

tabla_ex.place(x=30, y=140)

def mostrarEx():
    con = conectar()
    if not con: return
    c1 = con.cursor()
    c1.execute("SELECT * FROM existencias")
    tabla_ex.delete(*tabla_ex.get_children())
    for fila in c1:
        tabla_ex.insert("", tk.END, values=fila)
    con.close()

def insertarEx():
    con = conectar()
    if not con: return
    c1 = con.cursor()
    c1.execute("INSERT INTO existencias VALUES (%s,%s,%s)",
               (ex_codigo.get(), ex_lote.get(), ex_cantidad.get()))
    con.commit()
    mostrarEx()
    con.close()

def eliminarEx():
    con = conectar()
    if not con: return
    c1 = con.cursor()
    c1.execute("DELETE FROM existencias WHERE exi_codigo_k = %s", (ex_codigo.get(),))
    con.commit()
    mostrarEx()
    con.close()

def buscarEx():
    con = conectar()
    if not con: return
    c1 = con.cursor()
    c1.execute("SELECT * FROM existencias WHERE exi_codigo_k = %s", (ex_codigo.get(),))
    tabla_ex.delete(*tabla_ex.get_children())
    for fila in c1:
        tabla_ex.insert("", tk.END, values=fila)
    con.close()

def actualizarEx():
    con = conectar()
    if not con: return
    c1 = con.cursor()
    c1.execute("UPDATE existencias SET exi_lote=%s, exi_cantidad=%s WHERE exi_codigo_k=%s",
               (ex_lote.get(), ex_cantidad.get(), ex_codigo.get()))
    con.commit()
    mostrarEx()
    con.close()

def generarP():
    #conexion base de datos
    con = conectar()
    c1 = con.cursor()
    #crear lista y diccionario
    valor = {}
    cc = []
    ll = []
    ca = []
    #sentencia para seleccionar datos
    c1.execute("select *from existencias")
    x = 1
    for fila in c1:
        cod,l,c = fila
        cc.insert(x,cod)
        ll.insert(x,l)
        ca.insert(x,c)
        x = x+1
    print(cc,ll,ca)
    valor = {"codigo_producto": cc,
               "lote": ll,
             "cantidad": ca}
    dataframe = pd.DataFrame(valor)
    dataframe.to_excel("./existencias.xlsx",
                       index=False)
    #Mostrar archivo
    os.system("start EXCEL.EXE existencias.xlsx")
    dataframe.to_excel("./existencias.xlsx",
                       index=False)
def grafica():
    con = conectar()
    if not con:
        return

    c1 = con.cursor()
    c1.execute("SELECT MOV_MOVIMIENTO, MOV_FECHA, MOV_CANTIDAD FROM movimientos")

    entradas = []
    salidas = []
    fechasE = []
    fechasS = []

    for mov in c1:
        tipo, fecha, cantidad = mov

        if tipo.lower() == "ingreso":
            entradas.append(cantidad)
            fechasE.append(fecha)
        else:
            salidas.append(cantidad)
            fechasS.append(fecha)

    con.close()

    fig, ax = plt.subplots()
    if entradas:
        ax.plot(fechasE, entradas, color='tab:purple', label='Entradas')
    if salidas:
        ax.plot(fechasS, salidas, color='tab:green', label='Salidas')

    ax.legend(loc='upper right')
    ax.set_xlabel("Fecha", fontsize=12)
    ax.set_ylabel("Cantidad")
    ax.set_title("Control de Entradas y Salidas")

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

tk.Button(frame_existencias, text="Mostrar", width=12, command=mostrarEx).place(x=30, y=370)
tk.Button(frame_existencias, text="Insertar", width=12, command=insertarEx).place(x=150, y=370)
tk.Button(frame_existencias, text="Eliminar", width=12, command=eliminarEx).place(x=270, y=370)
tk.Button(frame_existencias, text="Buscar", width=12, command=buscarEx).place(x=390, y=370)
tk.Button(frame_existencias, text="Actualizar", width=12, command=actualizarEx).place(x=510, y=370)
tk.Button(frame_existencias, text="Reporte", width=12, command=generarP).place(x=650, y=100)
tk.Button(frame_existencias, text="Grafica", width=12, command=grafica).place(x=650, y=200)

tk.Button(frame_existencias, text="Volver al menú", width=15,
          command=lambda: mostrar_frame(frame_principal)).place(x=720, y=20)

frame_movimientos = tk.Frame(frame_todo, bg="light yellow")

titulo_mov = tk.Label(frame_movimientos, text="MOVIMIENTOS",
    font=("Arial Black", 18, "bold"), bg="orange", fg="white")
titulo_mov.pack(pady=20)


labels = ["Código", "Movimiento", "Fecha", "Producto", "Lote", "Costo", "Cantidad", "Total"]
entradas = []
y = 80

for text in labels:
    tk.Label(frame_movimientos, text=text).place(x=30, y=y)
    e = tk.Entry(frame_movimientos)
    e.place(x=150, y=y)
    entradas.append(e)
    y += 40

(mov_codigo, mov_tipo, mov_fecha, mov_prod, mov_lote,
 mov_costo, mov_cant, mov_total) = entradas

columnas = ("MOV_CODIGO_K","MOV_MOVIMIENTO","MOV_FECHA","PRO_CODIGO_K",
            "EXI_LOTE","MOV_COSTO","MOV_CANTIDAD","MOV_TOTAL")

tabla_mov = ttk.Treeview(frame_movimientos, columns=columnas, show="headings")
for col in columnas:
    tabla_mov.heading(col, text=col)
    tabla_mov.column(col, width=100)

tabla_mov.place(x=30, y=420)

def mostrarMov():
    con = conectar()
    if not con: return
    c1 = con.cursor()
    c1.execute("SELECT * FROM movimientos")
    tabla_mov.delete(*tabla_mov.get_children())
    for fila in c1:
        tabla_mov.insert("", tk.END, values=fila)
    con.close()


def insertarMov():
    con = conectar()
    if not con:
        return
    c1 = con.cursor()
    tipo = mov_tipo.get().lower()
    codigo = mov_prod.get()
    lote = mov_lote.get()
    cantidad = int(mov_cant.get())
    costo = float(mov_costo.get())
    fecha = mov_fecha.get()
    if tipo == "ingreso":
        c1.execute("""
            INSERT INTO existencias (exi_codigo_k, exi_lote, exi_cantidad)
            VALUES (%s, %s, %s)
        """, (codigo, lote, cantidad))
        con.commit()
    elif tipo == "salida":
        c1.execute("""
            SELECT exi_lote, exi_cantidad
            FROM existencias
            WHERE exi_codigo_k=%s
            ORDER BY exi_lote ASC
        """, (codigo,))
        lotes = c1.fetchall()
        cantidad_restante = cantidad
        for lote_bd, cant_bd in lotes:
            if cantidad_restante <= 0:
                break
            if cant_bd <= cantidad_restante:
                c1.execute("""
                    DELETE FROM existencias
                    WHERE exi_codigo_k=%s AND exi_lote=%s
                """, (codigo, lote_bd))
                cantidad_restante -= cant_bd
            else:
                nueva_cant = cant_bd - cantidad_restante
                c1.execute("""
                    UPDATE existencias
                    SET exi_cantidad=%s
                    WHERE exi_codigo_k=%s AND exi_lote=%s
                """, (nueva_cant, codigo, lote_bd))
                cantidad_restante = 0

        con.commit()

        if cantidad_restante > 0:
            messagebox.showerror("Error", "No hay suficiente producto para la salida.")
            con.close()
            return
    sql = """
    INSERT INTO movimientos 
    (MOV_CODIGO_K, MOV_MOVIMIENTO, MOV_FECHA, PRO_CODIGO_K, EXI_LOTE,
     MOV_COSTO, MOV_CANTIDAD, MOV_TOTAL)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """

    total = costo * cantidad
    datos = (mov_codigo.get(), mov_tipo.get(), fecha, codigo, lote,
             costo, cantidad, total)

    c1.execute(sql, datos)
    con.commit()

    STOCK_MINIMO = 10

    c1.execute("""
        SELECT SUM(exi_cantidad)
        FROM existencias
        WHERE exi_codigo_k=%s
    """, (codigo,))

    total_existencias = c1.fetchone()[0] or 0

    if total_existencias < STOCK_MINIMO:
        messagebox.showwarning(
            "⚠ Stock Mínimo",
            f"El producto {codigo} tiene solo {total_existencias} unidades.\n"
            f"Stock mínimo permitido: {STOCK_MINIMO}"
        )

    mostrarMov()
    con.close()

def eliminarMov():
    con = conectar()
    if not con: return
    c1 = con.cursor()
    c1.execute("DELETE FROM movimientos WHERE MOV_CODIGO_K=%s", (mov_codigo.get(),))
    con.commit()
    mostrarMov()
    con.close()

def buscarMov():
    con = conectar()
    if not con: return
    c1 = con.cursor()
    c1.execute("SELECT * FROM movimientos WHERE MOV_CODIGO_K=%s", (mov_codigo.get(),))
    tabla_mov.delete(*tabla_mov.get_children())
    for fila in c1:
        tabla_mov.insert("", tk.END, values=fila)
    con.close()

def actualizarMov():
    con = conectar()
    if not con: return
    c1 = con.cursor()
    sql = """
    UPDATE movimientos SET MOV_MOVIMIENTO=%s, MOV_FECHA=%s,
    PRO_CODIGO_K=%s, EXI_LOTE=%s, MOV_COSTO=%s, MOV_CANTIDAD=%s,
    MOV_TOTAL=%s WHERE MOV_CODIGO_K=%s
    """
    datos = (mov_tipo.get(), mov_fecha.get(), mov_prod.get(),
             mov_lote.get(), mov_costo.get(), mov_cant.get(),
             mov_total.get(), mov_codigo.get())
    c1.execute(sql, datos)
    con.commit()
    mostrarMov()
    con.close()

def generarM():
    #conexion base de datos
    con = conectar()
    c1 = con.cursor()
    #crear lista y diccionario
    valore = {}
    cc = []
    mm = []
    ff = []
    pp = []
    ll = []
    co = []
    ca = []
    tt = []
    #sentencia para seleccionar datos
    c1.execute("select *from movimientos")
    x = 1
    for fila in c1:
        cod,m,f,p,l,cos,can,t = fila
        cc.insert(x,cod)
        mm.insert(x,m)
        ff.insert(x,f)
        pp.insert(x, p)
        ll.insert(x, l)
        co.insert(x, cos)
        ca.insert(x, can)
        tt.insert(x, t)
        x = x+1
    print(cc,mm,ff,pp,ll,co,ca,tt)
    valore = {"codigo": cc,
             "movimiento": mm,
             "fecha": ff,
             "producto": pp,
             "lote": ll,
             "costo": co,
             "cantidad": ca,
             "total": tt}
    dataframe = pd.DataFrame(valore)
    dataframe.to_excel("./movimimenmtos.xlsx",
                       index=False)
    #Mostrar archivo
    os.system("start EXCEL.EXE movimientos.xlsx")
    dataframe.to_excel("./movimientos.xlsx",
                       index=False)

tk.Button(frame_movimientos, text="Mostrar", width=12, command=mostrarMov).place(x=30, y=380)
tk.Button(frame_movimientos, text="Insertar", width=12, command=insertarMov).place(x=150, y=380)
tk.Button(frame_movimientos, text="Eliminar", width=12, command=eliminarMov).place(x=270, y=380)
tk.Button(frame_movimientos, text="Buscar", width=12, command=buscarMov).place(x=390, y=380)
tk.Button(frame_movimientos, text="Actualizar", width=12, command=actualizarMov).place(x=510, y=380)
tk.Button(frame_movimientos, text="Reporte", width=12, command=generarM).place(x=650, y=100)

tk.Button(frame_movimientos, text="Volver al menú", width=15,
          command=lambda: mostrar_frame(frame_principal)).place(x=720, y=20)

tk.Button(
    frame_principal, text="Productos", bg="violet",
    font=("Colibri", 11, "bold"), width=20,
    command=lambda: mostrar_frame(frame_productos)
).pack(pady=10)

tk.Button(
    frame_principal, text="Existencias", bg="violet",
    font=("Colibri", 11, "bold"), width=20,
    command=lambda: mostrar_frame(frame_existencias)
).pack(pady=10)

tk.Button(
    frame_principal, text="Movimientos", bg="violet",
    font=("Colibri", 11, "bold"), width=20,
    command=lambda: mostrar_frame(frame_movimientos)
).pack(pady=10)

tk.Button(
    frame_principal, text="Volver al inicio",
    bg="yellow", font=("Colibri", 11, "bold"),
    command=lambda: mostrar_frame(frame_inicio)
).pack(pady=30)

mostrar_frame(frame_inicio)
ventana.mainloop()
