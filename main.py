from threading import Thread
import PySimpleGUI as sg
import datetime
import time
import sys


sg.theme('black')

#--------- layout da janela do timer---------#
column = [
    [
        sg.Text(size=(None, 1), key='-OUT-', justification='center')
    ]
]

layout_timer = [
    [sg.VPush()],
    [sg.Push(), sg.Column(column, justification='center'), sg.Push()],
    [sg.VPush()]
]
#-------------------------------------------#

layout_prompt = [
    [sg.Text("Programar timer da reunião")],
]

def update_time(window, total_seconds):
    # checagem do tempo
    while total_seconds > 0:
 
        # Timer é o tempo restante formatado
        timer = datetime.timedelta(seconds = total_seconds)

        # mostra o tempo restante
        window['-OUT-'].update(timer)

        # dá uma pausa de 1 segundo
        time.sleep(1)
        total_seconds -= 1
    
    print("tempo")
    return


def countdown(h, m, s):
 
    # Calcula o tempo total em segundos
    total_seconds = h * 3600 + m * 60 + s
 
    # cria a janela
    window = sg.Window('Title not seen', layout_timer, location=(-500,0), no_titlebar=True, margins=(0, 0), element_padding=(0, 0), right_click_menu=sg.MENU_RIGHT_CLICK_EXIT,
                   keep_on_top=True, font='_ 72', finalize=True)
    window.Maximize()

    #cria nova thread para paralelismo
    timer = Thread(target=update_time, args=[window, total_seconds])
    timer.start()

    while True:
         # lê os eventos da janela
        event, values = window.read(timeout=100)
        if event == sg.WIN_CLOSED or event == 'Exit' or not timer.is_alive():
            break

    window.close()

    print("fechou")


def prompt_time():
    window = sg.Window('Timer', layout_prompt, font='_ 25', finalize=True)


prompt_time()


