import time


def getData_ca(ser):
    try:
        while True:
            ca = None
            if ser.in_waiting > 0:  
                line1 = ser.readline().decode('latin-1').rstrip()
                line2 = ser.readline().decode('latin-1').rstrip()
                line3 = ser.readline().decode('latin-1').rstrip()
                line4 = ser.readline().decode('latin-1').rstrip()
                line5 = ser.readline().decode('latin-1').rstrip()


                # print(type(line1))
                # print(type(line2))
                # print(type(line3))
                # print(type(line4))
                # print(type(line5))

                if line1.startswith("ca") and len(line1) > 4:
                    ca = line1
                elif line2.startswith("ca") and len(line2) > 4:
                    ca = line2
                elif line3.startswith("ca") and len(line3) > 4:
                    ca = line3
                elif line4.startswith("ca") and len(line4) > 4:
                    ca = line4
                elif line5.startswith("ca") and len(line5) > 4:
                    ca = line5
                else:
                    ca = None

                # print(type(ca))
                # print(len(ca))

                # print(temps)
                # print(ca)
                return ca


            # print("Nope")
            return None
            
    except Exception as error:
        print(f"Error: {error}")

def getData_temps(ser):
    try:
        while True:
            temps = None
            if ser.in_waiting > 0:
                line1 = ser.readline().decode('latin-1').rstrip()
                line2 = ser.readline().decode('latin-1').rstrip()
                line3 = ser.readline().decode('latin-1').rstrip()
                line4 = ser.readline().decode('latin-1').rstrip()
                line5 = ser.readline().decode('latin-1').rstrip()

                if line1.startswith("temps"):
                    temps = line1
                elif line2.startswith("temps"):
                    temps = line2
                elif line3.startswith("temps"):
                    temps = line3
                elif line4.startswith("temps"):
                    temps = line4
                elif line5.startswith("temps"):
                    temps = line5
                else:
                    temps = None

                # print(temps)
                # print(ca)
                return temps


            # print("Nope")
            return None
            
    except Exception as error:
        print(f"Error: {error}")

def getData_bp(ser):
    try:
        while True:
            BP = None
            if ser.in_waiting > 0:
                line1 = ser.readline().decode('latin-1').rstrip()
                line2 = ser.readline().decode('latin-1').rstrip()
                line3 = ser.readline().decode('latin-1').rstrip()
                line4 = ser.readline().decode('latin-1').rstrip()
                line5 = ser.readline().decode('latin-1').rstrip()

                if line1.startswith("bp"):
                    BP = line1
                elif line2.startswith("bp"):
                    BP = line2
                elif line3.startswith("bp"):
                    BP = line3
                elif line4.startswith("bp"):
                    BP = line4
                elif line5.startswith("bp"):
                    BP = line5
                else:
                    BP = None

                # print(temps)
                # print(ca)
                return BP

            return None
            
    except Exception as error:
        print(f"Error: {error}")

# while True:
#     print(getData())
#     print("Done")

