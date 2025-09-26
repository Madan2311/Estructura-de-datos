from metodos import Supermercado

supermercado = Supermercado("Akira Toriyama")

while True:
    print("\n=== SUPERMERCADO AKIRA TORIYAMA ===")
    print("1) HU00001 - Tomar turno")
    print("2) HU00001 - Ver turnos pendientes")
    print("3) HU00002 - Caja (atender siguiente)")
    print("4) HU00003 - Ver estado cola/ventas")
    print("5) HU00004 - Ver inventario")
    print("6) HU00004 - Agregar artículo")
    print("7) HU00004 - Dar de baja artículo")
    print("8) Salir")
    opcion = input("Seleccione opción: ").strip()

    match opcion:
        case "1":
            supermercado.tomar_turno()
        case "2":
            supermercado.ver_turnos()
        case "3":
            supermercado.atender_siguiente()
        case "4":
            supermercado.ver_estado()
        case "5":
            supermercado.listar_inventario()
        case "6":
            supermercado.agregar_articulo()
        case "7":
            supermercado.dar_de_baja()
        case "8":
            print("Saliendo... ¡gracias!")
            break
        case _:
            print("Opción inválida")
