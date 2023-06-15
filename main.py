import cv2
import time
import pygsheets
def start_again():
    cam_test()

import easyocr
def extract_numberplate(image):
    reader = easyocr.Reader(['en'])
    try:
        output = reader.readtext('plates/'+image)
        numberplate=output[0][1]
        words = numberplate.split()  # Split the string into a list of words
        numberplate = "".join(words)
        print(numberplate)
        return numberplate
    except IndexError as e:
            print("Image is not Clear")    
    except Exception as e:
            print(e)

    

def excel_sheet(numberplate):
    ts=0
    ts=time.gmtime()
    times=time.strftime("%H:%M", ts)
    # time_now=int(times[0:2])*60+int(times[3:6])
    print(times)
    cell=None
    gc = pygsheets.authorize(service_file='model/number_plate.json')
    sh = gc.open('ocr')
    wks = sh.worksheet('title', 'Sheet1')  
    # search_column = 'License'
    search_value = numberplate
    cell = sh.find(search_value, matchEntireCell=True)
    print(cell)
    isEmpty = True
    for array in cell:
         if len(array) > 0:
            isEmpty = False
            break
    if isEmpty:
         print("STOP")
         
    else:
        print("CELL HAS somethig")

    if(isEmpty==False):
        cell=str(cell[0][-1])
        cell=cell[7:9]
        print(cell)
    #new entry
    if(isEmpty):
        wks.append_table(values=[numberplate, times, 'NULL', 'NULL'])

    elif(isEmpty==False):
    #entry with entry time only
        value=wks.cell((int(cell),3)).value
        if(value == 'NULL'):
            wks.update_value('C'+cell, times)
            intime=str(wks.cell((int(cell),2)).value)
            intime=int(intime[0:2])*60+int(intime[3:6])
            outtime=str(wks.cell((int(cell),3)).value)
            outtime=int(outtime[0:2])*60+int(outtime[3:6])
            cost=(outtime-intime)*0.33
            wks.update_value('D'+cell, "₹"+str(cost))
        else:
            #entry with entry time and exit time
            wks.append_table(values=[numberplate, times, "NULL", "NULL"])

def cam_test():
    harcascade = "model/haarcascade_russian_plate_number.xml"
    link= 'http://192.168.137.134:1100/video'
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 270)
    min_area = 500
    count = 0
    destroy =1
    completed = 0
    img_roi = 0

    while not completed:
        success, img = cap.read()
        sound =0
        plate_cascade = cv2.CascadeClassifier(harcascade)
        img_gray = cv2.cvtColor(img, cv2.IMREAD_GRAYSCALE)

        plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)

        for (x,y,w,h) in plates:
            area = w * h

            if area > min_area:
                cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
                cv2.putText(img, "Number Plate", (x,y-5), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)

                img_roi = img[y: y+h, x:x+w]
                cv2.imshow("Car Number Plates", img_roi)
                if count<20:
                    if img_roi.all != 0:
                        cv2.imwrite("plates/img" + str(count) + ".png", img_roi)
                        count+=1
                        print(count)
                        img_roi = None

        if destroy:
            cv2.imshow("Result", img)
        if count ==20:
            cv2.destroyAllWindows()
            destroy=0

        if cv2.waitKey(1) & 0xFF == ord('q') | count==20:
                cv2.destroyAllWindows()
                destroy=0
                print("Video Window is Closed")
        i=19
        array_numberplate=[]
        while not destroy:
            if i> 0:
                print('img'+str(i)+'.png')
                number_plate=extract_numberplate('img'+str(i)+'.png')
                array_numberplate.append(number_plate)
                print(array_numberplate)

                # bus_info=excel_sheet(str(number_plate))

                i-=1
                if(i==0):
                    counts = {}
                    for element in array_numberplate:
                        if str(element) in counts and element !='None':
                            if str(element)=='None':
                                 continue
                            else:
                                counts[element] += 1
                        else:
                            if str(element)=='None':
                                 continue
                            else:
                                 counts[element] = 1

                    number_plate = max(counts, key=counts.get)
                    max_occurrence = counts[number_plate]
                    print('The Value '+str(number_plate)+' Occured '+str(max_occurrence)+' times')
                    excel_sheet(number_plate)
                    start_again()

if __name__ == '__main__':
    cam_test()                