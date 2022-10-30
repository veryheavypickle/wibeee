import src

if __name__ == '__main__':
    WiBeee = src.WiBeee("192.168.1.145")
    status = WiBeee.getStatus()
    for stat in status:
        print("{0}: {1}".format(stat, status[stat]))

    print("")
    print(status["fase1_p_activa"])

