def mostrarAgregadas(agregadas):
    if(len(agregadas) > 0):
        print("\nMaterias agregadas:")
        for i in range(len(agregadas)):
            # Imprime solo el nombre y no la coordenada
            print("  - {}".format(agregadas[i][0]))
        print()
