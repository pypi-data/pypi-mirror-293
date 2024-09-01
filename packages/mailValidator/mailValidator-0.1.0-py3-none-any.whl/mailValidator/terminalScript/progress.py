import time

def animate_progress():
    dots = ''
    while True:
        print(f'\rLoading{dots}', end='')
        dots += '.'
        if len(dots) > 3:
            dots = ''
        time.sleep(0.5)
