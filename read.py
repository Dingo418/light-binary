import cv2
from argparse import ArgumentParser

def click_function(event, x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global global_x, global_y, collection
        global_x = x
        global_y = y
        collection = True

def what_colour(r,g,b):
    if r > 245-sens and g < 10+sens and b < 10+sens:
        return "1"
    elif r < 10+sens and g < 10+sens and b > 245-sens:
        return "0"
    else:
        return "|"

def format(string):
    if string == "":
        return "NO INFO GIVEN"

    # Removing consecutive repeating bits
    format = "" 
    current_bit = string[0]
    current_count = 0
    for i in range(len(string)):
        if string[i] == current_bit:
            current_count += 1
        else:
            if current_count >= fuzzy:
                format += current_bit
            current_bit, current_count = string[i], 1
    if current_count >= fuzzy:
        format += current_bit

    # Removing "|"
    stripped = format.replace("|", "")

    # Adding space every 8 bits
    formatted_binary = ' '.join(stripped[i:i+8] for i in range(0, len(stripped), 8) )

    # Converting 8-bit binary to uefi
    text = "".join(chr(int(byte, 2)) for byte in formatted_binary.split())

    print("\n\n\n\n\n\n\n\n")
    print("Binary: ", formatted_binary)  
    print("Text: ", text)

def webcam(camera_id):
    raw = ""
    collection,raw = False, ""
    vid = cv2.VideoCapture(camera_id)
    print("Camera's up")

    while True: 
        _, frame = vid.read()        
        cv2.imshow("image", frame)
        cv2.setMouseCallback('image',click_function) 
        
        b,g,r = frame[global_y,global_x]
        
        if collection:
            bit = what_colour(r, g, b)
            print(bit,end="")
            raw += bit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()
    format(raw)

def analyze_file(file_location):
    raw = ""
    global collection
    collection = False
    #Get first frame
    video = cv2.VideoCapture(file_location)
    video.set(cv2.CAP_PROP_POS_FRAMES, 0)
    ret, img = video.read() 
 
    while True:
        cv2.imshow("image", img)
        cv2.setMouseCallback("image", click_function)
        if cv2.waitKey(1) & 0xFF == ord("q") or collection:
            break

    # close the windowy
    cv2.destroyAllWindows()

    video = cv2.VideoCapture(file_location)
    success, img = video.read()

    while success:
        b,g,r = img[global_y,global_x]        
        bit = what_colour(r, g, b)
        print(bit,end="")
        raw += bit
        # read next frame
        success, img = video.read()
    format(raw)

def main():
    parser = ArgumentParser(description="Light Binary for Reading light")

    parser.add_argument("-c","--camera", 
                        action="store", default=0, choices=("0","1","2","3"),
                        help="Different camera"
                        )
    parser.add_argument("-f","--file", 
                        action="store", default=None,
                        help="video file address file."
                        )
    parser.add_argument("-rgb", 
                        action="store", default=90,
                        help="RGB Senstivity"
                        )
    parser.add_argument("-sens", "-senstivity",
                        action="store", default=1,
                        help="senstivity gets rid of single bit pickups. If you got a good camera you can go to 0")
    args = parser.parse_args()

    try:
        global sens,fuzzy,raw
        sens = int(args.rgb)
        fuzzy = int(args.sens)
        raw = ""
    except:
        print("failed")
        exit()

    if args.file != None:
        analyze_file(args.file)
    else:
        webcam(int(args.camera))

if __name__ == "__main__":
    main()