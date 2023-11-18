from threading import Thread
import PySimpleGUI as sg
from datetime import datetime, timedelta
import os
import time
import sys


#--------- layout da janela do timer---------#
sg.theme('black')
column = [
    [
        sg.Text("00:00", size=(None, 1), key='-OUT-', justification='center')
    ]
]

layout_timer = [
    [sg.VPush()],
    [sg.Push(), sg.Column(column, justification='center'), sg.Push()],
    [sg.VPush()]
]
#----------layout do programador-------------#

sg.theme('SystemDefaultForReal')
horas = list(range(0,24))
minutos = list(range(0,60, 1))
layout_prompt = [
    [sg.Text("Programar timer da reunião")],
    [sg.Text("Hora de início", font='_ 12')],
    [sg.Spin(horas, 19, readonly=True, key="-hour-"), sg.Spin(minutos, 30, readonly=True, key="-min-")],
    [sg.Text("Tempo do timer", font='_ 12')],
    [sg.Spin(list(range(1, 21)), 5, readonly=True, key="-time-")],
    [sg.Button("Cancelar", font='_ 12', key="-cancel-"), sg.HSeparator(), sg.Button("Programar", font='_ 12', key="-set-")]
]

#----------layout do gerenciador do timer-------------#

sg.theme('SystemDefaultForReal')
layout_manager = [
    [sg.Text("Timer rodando")],
    [sg.Text("Favor voltar o JW para o primeiro plano após o timer", font="_ 11")],
    [sg.Button("Fechar timer", key="-close-")]
]

def timedelta_formatter(td):                             
    td_sec = td.seconds
    minute_count, second_count = divmod(divmod(td_sec, 3600)[1], 60)
    fmt = f"{minute_count:02d}:{second_count:02d}"
    return fmt


def update_time(window, total_seconds):
    #window.keep_on_top_set()
    os.system('nircmd win activate title "Timer count"')
    os.system('nircmd win max title "Timer count"')
    # checagem do tempo
    while total_seconds > 0:
 
        # Timer é o tempo restante formatado
        timer = timedelta_formatter(timedelta(seconds = total_seconds))

        # mostra o tempo restante
        window['-OUT-'].update(timer)
        window.bring_to_front()

        # dá uma pausa de 1 segundo
        time.sleep(1)
        total_seconds -= 1
    
    print("tempo")
    return


#def foreground( hwnd, ctx ):
#    if win32gui.IsWindowVisible( hwnd ):
#        nome = win32gui.GetWindowText(hwnd).strip().lower()
#        if  nome == "timer screen" or nome == "title not seen":
#            win32gui.SetForegroundWindow(hwnd)
#        #print ( hex( hwnd ), win32gui.GetWindowText( hwnd ) )


def countdown(m):
 
    # Calcula o tempo total em segundos
    total_seconds =  m * 60
    
    #cria a janela do gerenciardor
    sg.theme('SystemDefaultForReal')
    window_m = sg.Window('Gerenciador do timer', layout_manager, font='_ 16', finalize=True)

    # cria a janela do timer
    screen_size = sg.Window.get_screen_size()
    sg.theme('black')
    window_t = sg.Window('Timer count', layout_timer, location=(screen_size[0],0), no_titlebar=True,
                   keep_on_top=True, font='_ 96', finalize=True)
    window_t.Maximize() 
    
    # move a janela para frente
    #win32gui.EnumWindows(foreground, None)
    
    #cria nova thread para paralelismo
    timer = Thread(target=update_time, args=[window_t, total_seconds])
    timer.start()
    window_t.keep_on_top_set()
    while True:
         # lê os eventos da janela
        event_m, value_m = window_m.read(timeout=100)
        event_t, values_t = window_t.read(timeout=100)
        if event_m == sg.WIN_CLOSED or event_m == "-close-" or event_t == sg.WIN_CLOSED or not timer.is_alive():
            break
    
    window_t.close()
    window_m.close()

    print("fechou")
    sys.exit()


def prompt_time():
    sg.theme('SystemDefaultForReal')
    window = sg.Window('Timer', layout_prompt, font='_ 16', finalize=True)

    while True:
         # lê os eventos da janela
        event, values = window.read(timeout=100)
        if event == sg.WIN_CLOSED or event == 'Exit' or event == "-cancel-":
            break
        
        if event == "-set-":
            print(values["-hour-"], " : ", values["-min-"])
            dt = datetime.now()
            start_time = (dt.replace(hour=values["-hour-"], minute=values["-min-"]) - timedelta(minutes=values["-time-"]))
            print(start_time)

            if dt.hour > start_time.hour or (dt.hour >= start_time.hour and dt.minute >= start_time.minute):
                sg.popup("O tempo já passou", title="timeout")
                continue
            
            window.close()
            return start_time, values["-time-"], f"{values['-hour-']:02d}:{values['-min-']:02d}"
    
    return False


def alarm(timer: datetime, minutes):
    while True:
        now = datetime.now().strftime("%H:%M")
        timerstr = timer.strftime("%H:%M")
        timer_arr = timerstr.split(":")
        now_arr = now.split(":")

        if int(timer_arr[0]) > int(now_arr[0]):
            time.sleep(300)
            continue
        elif int(timer_arr[1]) - int(now_arr[1]) > 10:
            time.sleep(600)
            continue
        elif int(timer_arr[1]) - int(now_arr[1]) > 5:
            time.sleep(300)
            continue
        elif int(timer_arr[1]) - int(now_arr[1]) > 1:
            time.sleep(60)
            continue
        

        if timerstr == now:
            print("start Timer")
            countdown(minutes)
            break
        
        if int(now_arr[0]) > int(timer_arr[0]) or (int(now_arr[0]) >= int(timer_arr[0]) and int(now_arr[1]) >= int(timer_arr[1])):
            print("já passou")
            sg.popup("O tempo já passou", title="timeout")
            return
        time.sleep(1)


#countdown(0.1)
timer_info = prompt_time()

if timer_info:
    sg.popup_auto_close(f"timer programado para começar às \n{timer_info[0].strftime('%H:%M')}\nE terminar às\n{timer_info[2]}")
    alarm(timer_info[0], timer_info[1])



