import src

if __name__ == '__main__':
    WiBeee = src.WiBeee('192.168.1.145')
    while True:
        print(WiBeee.power())

