class Libro:
    def __init__(self, titulo, autor):
        self.titulo = titulo
        self.autor = autor
        self.prev = None  # Apunta al libro anterior
        self.next = None  # Apunta al siguiente libro

class ListaDoble:
    def __init__(self):
        self.head = None  # Primer libro
        self.tail = None  # Último libro

    def agregar(self, titulo, autor):
        nuevo = Libro(titulo, autor)
        if not self.head:
            self.head = self.tail = nuevo
        else:
            self.tail.next = nuevo
            nuevo.prev = self.tail
            self.tail = nuevo

    def eliminar(self, titulo):
        actual = self.head
        while actual:
            if actual.titulo == titulo:
                if actual.prev:
                    actual.prev.next = actual.next
                else:
                    self.head = actual.next
                if actual.next:
                    actual.next.prev = actual.prev
                else:
                    self.tail = actual.prev
                break
            actual = actual.next

    def mostrar(self):
        print("Recorriendo hacia adelante:")
        actual = self.head
        while actual:
            print(f"{actual.titulo} - {actual.autor}")
            actual = actual.next

    def mostrar_inverso(self):
        print("Recorriendo hacia atrás:")
        actual = self.tail
        while actual:
            print(f"{actual.titulo} - {actual.autor}")
            actual = actual.prev

lista = ListaDoble()
lista.agregar("Cien años de soledad", "García Márquez")
lista.agregar("El Principito", "Saint-Exupéry")
lista.agregar("Don Quijote", "Cervantes")

lista.mostrar()
print()
lista.mostrar_inverso()

print("\nEliminamos 'El Principito':")
lista.eliminar("El Principito")
lista.mostrar()
print()
lista.mostrar_inverso()