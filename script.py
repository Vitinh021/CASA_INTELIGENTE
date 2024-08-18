import cv2
import face_recognition as fr
import speech_recognition as sr
import serial
import serial.tools.list_ports
import os

try:
    arduino = serial.Serial('COM3', 9600, timeout=1)
except serial.SerialException as e:
    print(f"Erro ao tentar se conectar ao Arduino: {e}")
except Exception as e:
    print(f"Um erro inesperado ocorreu: {e}")

caminho = 'exemplo.jpg' # Definir a imagem base de reconhecimento

recognizer = sr.Recognizer()
if not os.path.exists(caminho):
    print(f"O arquivo '{caminho}' não foi encontrado.")

def ativarReconhecimento():
    foto = fr.load_image_file(caminho) 
    foto = cv2.cvtColor(foto,cv2.COLOR_BGR2RGB)
    faceLoc = fr.face_locations(foto)[0]
    cv2.rectangle(foto,(faceLoc[3],faceLoc[0]),(faceLoc[1],faceLoc[2]),(0,255,0),2)
    encodeFoto = fr.face_encodings(foto)[0]

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("nao abriu")
        exit()

    while True:
        ret, frame = cap.read()

        if not ret:
            print("nao tem frame")
            break

        # Convertendo o frame para escala de cinza
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detectando rostos no frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Desenhando retângulos ao redor dos rostos detectados
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.imwrite('rosto_detectado.jpg', frame)
            rosto = fr.load_image_file('rosto_detectado.jpg')
            rosto = cv2.cvtColor(rosto,cv2.COLOR_BGR2RGB)
            if len(fr.face_encodings(rosto)) > 0:
                encodeRosto = fr.face_encodings(rosto)[0]
                comparacao = fr.compare_faces([encodeFoto],encodeRosto)
                if(comparacao[0] == True):
                    arduino.write(b'1') 
                elif(comparacao[0] == False):
                    arduino.write(b'2')

        windowName = "imagem"
        cv2.imshow(windowName, frame)

        k = cv2.waitKey(1)
        if k == ord('q'):
            break

        if cv2.getWindowProperty(windowName, cv2.WND_PROP_VISIBLE) < 1:
            break

    cv2.destroyAllWindows()
    cap.release()

def ativarSala():
    arduino.write(b"3")

def desativarSala():
    arduino.write(b"4")

def ativarAcademia():
    arduino.write(b"5")

def desativarAcademia():
    arduino.write(b"6")

def ativarQuarto():
    arduino.write(b"C")

def desativarQuarto():
    arduino.write(b"D")

def ativarCozinha():
    arduino.write(b"7")

def desativarCozinha():
    arduino.write(b"8")

def ativarAlarme():
    arduino.write(b"9")

def desativarAlarme():
    arduino.write(b"0")

while True:
    # Usa o microfone como fonte de áudio
    with sr.Microphone() as source:
        print("Ajustando o nível de ruído...") 
        recognizer.adjust_for_ambient_noise(source)
        print("Diga algo...")
        audio = recognizer.listen(source)

    # Tenta reconhecer o áudio usando o Google Web Speech API
    try:
        print("Você disse: " + recognizer.recognize_google(audio, language="pt-BR"))
        comando = recognizer.recognize_google(audio, language="pt-BR")

        if(comando.lower() == "ativar reconhecimento"):
            ativarReconhecimento()

        if(comando.lower() == "ativar sala"):
           ativarSala()

        if(comando.lower() == "desativar sala"):
           desativarSala()

        if(comando.lower() == "ativar quarto"):
           ativarQuarto()

        if(comando.lower() == "desativar quarto"):
           desativarQuarto()

        if(comando.lower() == "ativar cozinha"):
           ativarCozinha()

        if(comando.lower() == "desativar cozinha"):
           desativarCozinha()
                
        if(comando.lower() == "ativar alarme"):
           ativarAlarme()
        
        if(comando.lower() == "desativar alarme"):
           desativarAlarme()

        if(comando.lower() == "ativar academia"):
           ativarAcademia()

        if(comando.lower() == "desativar academia"):
           desativarAcademia()

    except sr.UnknownValueError:
        print("NÃO ENTENDI, REPITA")
    except sr.RequestError as e:
        print("Não foi possível requisitar resultados do Google Speech Recognition; {0}".format(e))
