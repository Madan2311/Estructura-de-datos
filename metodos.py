from collections import deque


class Articulo:
    def __init__(self, id, nombre, categoria, existencias, precio_por_unidad, estado=0):
        self.id = id
        self.nombre = nombre
        self.categoria = categoria
        self.existencias = existencias
        self.precio_por_unidad = precio_por_unidad
        self.estado = estado  # 0 activo, 1 inactivo

    def activo(self):
        return self.estado == 0 and self.existencias > 0


class ClienteTurno:
    def __init__(self, cedula, nombre):
        self.cedula = cedula
        self.nombre = nombre


class VentaItem:
    def __init__(self, articulo_id, nombre, categoria, cantidad, precio_unitario):
        self.articulo_id = articulo_id
        self.nombre = nombre
        self.categoria = categoria
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario

    def subtotal(self):
        return round(self.cantidad * self.precio_unitario, 2)


class Venta:
    def __init__(self, cliente, items):
        self.cliente = cliente
        self.items = items

    def total(self):
        return round(sum(i.subtotal() for i in self.items), 2)


# --------- Validaciones muy básicas ---------
def es_texto_simple(valor):
    if not isinstance(valor, str):
        return False
    valor = valor.strip()
    if len(valor) < 2 or len(valor) > 60:
        return False
    permitidos = "abcdefghijklmnñopqrstuvwxyz áéíóú"
    for ch in valor:
        if ch.lower() not in permitidos:
            return False
    return True


def leer_entero_mayor_igual_cero(msg):
    while True:
        dato = input(msg).strip()
        if dato.isdigit():
            return int(dato)
        print("  -> Debe ser un número entero >= 0. Intente de nuevo.")


def leer_decimal_2(msg):
    while True:
        dato = input(msg).strip().replace(",", ".")
        try:
            v = float(dato)
            if v >= 0:
                return round(v, 2)
        except:
            pass
        print("  -> Debe ser un número decimal (ej: 1200 o 1200.50).")


def leer_texto_simple(msg):
    while True:
        t = input(msg).strip()
        if es_texto_simple(t):
            return t.title()
        print("  -> Solo letras y espacios (2-60).")


# --------- Clase principal ---------
class Supermercado:
    def __init__(self, nombre):
        self.nombre = nombre
        self.turnos = deque()  # COLA (FIFO) optimizada con deque
        self.atendidos = []  # lista de clientes atendidos
        self.inventario = []  # lista de Articulo
        self.ventas_del_dia = []  # lista de Venta
        self._siguiente_id = 1  # ID autoincremental
        self.categorias = []  # columnas de la "matriz"
        self.matriz_cat = []  # filas por venta

    # ---- HU00004 Inventario ----
    def agregar_articulo(self):
        nombre = leer_texto_simple("  Nombre: ")
        categoria = leer_texto_simple("  Categoría: ")
        exist = leer_entero_mayor_igual_cero("  Existencias: ")
        precio = leer_decimal_2("  Precio por unidad: ")
        art = Articulo(self._siguiente_id, nombre, categoria, exist, precio, 0)
        self.inventario.append(art)
        self._siguiente_id += 1
        if categoria not in self.categorias:
            self.categorias.append(categoria)
        print(f"✔ Agregado: {art.nombre} (ID {art.id})")

    def dar_de_baja(self):
        art_id = leer_entero_mayor_igual_cero("  ID a dar de baja: ")
        for art in self.inventario:
            if art.id == art_id:
                art.estado = 1
                print(f"✔ Artículo {art.id} dado de baja (inactivo).")
                return
        print("  -> No se encontró ese artículo.")

    def listar_inventario(self):
        print("\nINVENTARIO")
        print(
            "ID | Nombre               | Categoría        | Stock | Precio   | Estado"
        )
        print(
            "-- | -------------------- | ---------------- | ----- | -------- | ------"
        )
        for art in self.inventario:
            estado = "Activo" if art.estado == 0 else "Inactivo"
            print(
                f"{str(art.id).ljust(2)} | {art.nombre.ljust(20)} | {art.categoria.ljust(16)} | "
                f"{str(art.existencias).rjust(5)} | {str(f'{art.precio_por_unidad:.2f}').rjust(8)} | {estado}"
            )

    def buscar_articulo(self, articulo_id):
        for art in self.inventario:
            if art.id == articulo_id:
                return art
        return None

    # ---- HU00001 Turnos ----
    def tomar_turno(self):
        cedula = input("  Cédula (solo números): ").strip()
        if not cedula.isdigit():
            print("  -> Debe ser solo números.")
            return
        nombre = leer_texto_simple("  Nombre: ")
        cliente = ClienteTurno(cedula, nombre)
        self.turnos.append(cliente)  # encola
        print(f"✔ Turno tomado por {nombre} (CC {cedula}).")

    def ver_turnos(self):
        if len(self.turnos) == 0:
            print("No hay turnos pendientes.")
            return
        print("\nTURNOS PENDIENTES (orden de llegada)")
        for i, c in enumerate(self.turnos, start=1):
            print(f"{i}. {c.nombre} (CC {c.cedula})")

    # ---- HU00002 Caja ----
    def atender_siguiente(self):
        if len(self.turnos) == 0:
            print("No hay turnos para atender.")
            return
        cliente = self.turnos.popleft()  # desencola con deque
        print(f"\nAtendiendo a: {cliente.nombre} (CC {cliente.cedula})")

        carrito = []  # lista de VentaItem
        pila_descartes = []  # PILA LIFO para último descartado

        def ver_carrito():
            print("\nCARRITO ACTUAL")
            if len(carrito) == 0:
                print("  (vacío)")
                return
            print("ID  | Artículo             | Cat.       | Cant | P.Unit  | Subtotal")
            print("----|----------------------|------------|------|---------|---------")
            for it in carrito:
                print(
                    f"{str(it.articulo_id).ljust(4)}| {it.nombre.ljust(20)} | "
                    f"{it.categoria.ljust(10)} | {str(it.cantidad).rjust(4)} | "
                    f"{str(f'{it.precio_unitario:.2f}').rjust(7)} | "
                    f"{str(f'{it.subtotal():.2f}').rjust(7)}"
                )
            total = sum(i.subtotal() for i in carrito)
            print(f"TOTAL: {total:.2f}")

        while True:
            print(
                "\n[1] Agregar artículo  [2] Descartar último  [3] Ver carrito  [4] Finalizar compra  [5] Salir sin comprar"
            )
            op = input("Elija opción: ").strip()

            if op == "1":
                art_id = leer_entero_mayor_igual_cero("  ID artículo: ")
                art = self.buscar_articulo(art_id)
                if art is None:
                    print("  -> No existe ese artículo.")
                    continue
                if not art.activo():
                    print("  -> Artículo inactivo o sin stock.")
                    continue
                cant = leer_entero_mayor_igual_cero("  Cantidad: ")
                if cant <= 0:
                    print("  -> La cantidad debe ser > 0.")
                    continue
                if cant > art.existencias:
                    print(f"  -> Stock insuficiente. Disponible: {art.existencias}.")
                    continue
                item = VentaItem(
                    art.id, art.nombre, art.categoria, cant, art.precio_por_unidad
                )
                carrito.append(item)
                print(f"  ✔ Agregado {cant} x {art.nombre}")

            elif op == "2":
                if len(carrito) > 0:
                    eliminado = carrito.pop()
                    pila_descartes.append(eliminado)
                    print(f"  ↩ Descartado: {eliminado.cantidad} x {eliminado.nombre}")
                else:
                    print("  -> No hay nada para descartar.")

            elif op == "3":
                ver_carrito()

            elif op == "4":
                if len(carrito) == 0:
                    print("  -> Carrito vacío, no se puede finalizar.")
                    continue
                venta = Venta(cliente, carrito[:])
                # Descontar inventario
                for it in carrito:
                    art = self.buscar_articulo(it.articulo_id)
                    if art is not None:
                        art.existencias -= it.cantidad
                self.ventas_del_dia.append(venta)
                self.atendidos.append(cliente)
                # Actualizar "matriz" por categoría
                fila = [0.0 for _ in self.categorias]
                for it in carrito:
                    cat = it.categoria
                    if cat not in self.categorias:
                        self.categorias.append(cat)
                        # expandir filas previas con 0
                        for row in self.matriz_cat:
                            row.append(0.0)
                        fila.append(0.0)
                    idx = self.categorias.index(cat)
                    fila[idx] += it.subtotal()
                self.matriz_cat.append(fila)

                print(f"  ✔ Venta registrada. TOTAL = {venta.total():.2f}")
                return  # termina atención

            elif op == "5":
                print("  -> Cliente se retira sin comprar.")
                self.atendidos.append(cliente)
                return
            else:
                print("  -> Opción inválida.")

    # ---- HU00003 Estado ----
    def ver_estado(self):
        print("\nESTADO DE LA COLA Y VENTAS")
        print(f"Pendientes: {len(self.turnos)}")
        print(f"Atendidos:  {len(self.atendidos)}")
        total_dia = 0.0
        for v in self.ventas_del_dia:
            total_dia += v.total()
        print(f"Ventas del día (TOTAL): {total_dia:.2f}")

        if len(self.ventas_del_dia) > 0 and len(self.categorias) > 0:
            print("\nMATRIZ VENTAS x CATEGORÍA (cada fila = una venta)")
            cab = "      | " + " | ".join(cat.center(10) for cat in self.categorias)
            print(cab)
            print("-" * (8 + 13 * len(self.categorias)))
            for i, fila in enumerate(self.matriz_cat, start=1):
                valores = " | ".join(str(f"{v:.2f}").rjust(10) for v in fila)
                print(f"Venta {str(i).rjust(2)} | {valores}")
