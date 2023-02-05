import time
import turtle
from argparse import ArgumentParser


def splash(pause, wait, message):
    wn=turtle.Screen()
    wn.setup(width=1.0, height=1.0)
    data_in_binary = ""
    wn.bgcolor("green")
    time.sleep(wait)
    time1 = time.time()
    for letter in message:
        for bit in format(ord(letter), '#010b')[2:]:
            if bit == "1":
                wn.bgcolor("red")
                data_in_binary += "1"
                time.sleep(pause)
            else:
                wn.bgcolor("blue")
                data_in_binary += "0"
                time.sleep(pause)
            end_time = time.time() 
            wn.bgcolor("green")
            time.sleep(pause)
    print(data_in_binary)
    print("time elapsed: ",end_time-time1)
    print("bits: ", len(message)*8)
    wn.bgcolor("green")
    time.sleep(wait)

def main():
    parser = ArgumentParser(description="Light Binary Project Screen")
    

    parser.add_argument("-m","--message", 
                        action="store", default="testing123,",
                        help="The message. The default is testing123"
                        )
    parser.add_argument("-s","--speed", 
                        action="store", default=0.2,
                        help="Pause between flashes of colour."
                        )
    parser.add_argument("-w","--wait", 
                        action="store", default=10,
                        help="Wait period before and after flashes."
                        )


    args = parser.parse_args()
    try:
        speed = float(args.speed)
        wait = float(args.wait)
    except:
        print("Please put a float for speed")
        exit()
    
    
    splash(speed, wait, args.message)

if __name__ == "__main__":
    main()




