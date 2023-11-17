import pygetwindow

def main():
    # Obtém todas as janelas ativas
    windows = pygetwindow.getWindowsWithTitle("")

    # Imprime o nome e o classname de cada janela
    for window in windows:
        print("Nome:", window)
        print("Classname:", window.className)

if __name__ == "__main__":
    main()


