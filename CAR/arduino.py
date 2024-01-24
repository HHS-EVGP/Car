# Last updated on 1/23/2024

def getData(ser):
    try:
        ca = "CA,None,None,None,None,None,,"
        bp = "bp,None"
        temps = "temps,None,None"
        data = "data,None"
        throttle = "throttle,None"
        motorTemps = "motor,None"
        
        if ser.in_waiting > 0:  
            line1 = ser.readline().decode('latin-1').rstrip()
            line2 = ser.readline().decode('latin-1').rstrip()
            line3 = ser.readline().decode('latin-1').rstrip()
            line4 = ser.readline().decode('latin-1').rstrip()
            line5 = ser.readline().decode('latin-1').rstrip()

            if line1.startswith("CA") and len(line1) > 4:
                ca = line1
            elif line2.startswith("CA") and len(line2) > 4:
                ca = line2
            elif line3.startswith("CA") and len(line3) > 4:
                ca = line3
            elif line4.startswith("CA") and len(line4) > 4:
                ca = line4
            elif line5.startswith("CA") and len(line5) > 4:
                ca = line5

            if line1.startswith("BP") and len(line1) > 3:
                bp = line1
            elif line2.startswith("BP") and len(line2) > 3:
                bp = line2
            elif line3.startswith("BP") and len(line3) > 3:
                bp = line3
            elif line4.startswith("BP") and len(line4) > 3:
                bp = line4
            elif line5.startswith("BP") and len(line5) > 3:
                bp = line5

            if line1.startswith("temps") and len(line1) > 4:
                temps = line1
            elif line2.startswith("temps") and len(line2) > 4:
                temps = line2
            elif line3.startswith("temps") and len(line3) > 4:
                temps = line3
            elif line4.startswith("temps") and len(line4) > 4:
                temps = line4
            elif line5.startswith("temps") and len(line5) > 4:
                temps = line5

            if line1.startswith("motor") and len(line1) > 4:
                motorTemps = line1
            elif line2.startswith("motor") and len(line2) > 4:
                motorTemps = line2
            elif line3.startswith("motor") and len(line3) > 4:
                motorTemps = line3
            elif line4.startswith("motor") and len(line4) > 4:
                motorTemps = line4
            elif line5.startswith("motor") and len(line5) > 4:
                motorTemps = line5

            if line1.startswith("throttle") and len(line1) > 4:
                throttle = line1
            elif line2.startswith("throttle") and len(line2) > 4:
                throttle = line2
            elif line3.startswith("throttle") and len(line3) > 4:
                throttle = line3
            elif line4.startswith("throttle") and len(line4) > 4:
                throttle = line4
            elif line5.startswith("throttle") and len(line5) > 4:
                throttle = line5

            data = f"{ca}|{bp}|{temps}|{motorTemps}|{throttle}"
            
        return data
            
    except Exception as error:
        print(f"Error: {error}")
        return "None - Fail"
