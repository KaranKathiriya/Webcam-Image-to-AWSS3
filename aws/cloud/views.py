from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
import cv2
import boto3
from botocore.exceptions import NoCredentialsError
import os
from django.contrib import messages

ACCESS_KEY = ''
SECRET_KEY = ''
count = 0
flag = 0


def home(request):
    return render(request, "index.html")


def capture_img(request):
    global count
    global ACCESS_KEY
    global SECRET_KEY
    global flag
    if request.method == 'POST' and flag == 0:
        flag = 1
        name = request.POST['filename']
        filename = name + ".jpg"
        ACCESS_KEY = request.POST['ak']
        SECRET_KEY = request.POST['sk']
        bucket = request.POST['bk']
        if ACCESS_KEY != "" and SECRET_KEY != "" and bucket != "" and filename != "":
            key = cv2.waitKey(1)
            webcam = cv2.VideoCapture(0)
            while True:
                try:
                    check, frame = webcam.read()
                    print(check)  # prints true as long as the webcam is running
                    print(frame)  # prints matrix values of each framecd
                    cv2.imshow("Capturing", frame)
                    key = cv2.waitKey(1)
                    if key == ord('s'):
                        cv2.imwrite(filename, img=frame)
                        webcam.release()
                        img_new = cv2.imread(filename)
                        img_new = cv2.imshow("Captured Image", img_new)
                        cv2.waitKey(1650)
                        cv2.destroyAllWindows()

                        break
                    elif key == ord('q'):
                        print("Turning off camera.")
                        webcam.release()
                        print("Camera off.")
                        print("Program ended.")
                        cv2.destroyAllWindows()
                        break

                except(KeyboardInterrupt):
                    print("Turning off camera.")
                    webcam.release()
                    print("Camera off.")
                    print("Program ended.")
                    cv2.destroyAllWindows()
                    break
            local_file = filename
            #bucket = bucket_name
            s3_file = filename
            s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                              aws_secret_access_key=SECRET_KEY)

            try:
                s3.upload_file(local_file, bucket, s3_file)
                print("Upload Successful")
                os.remove(local_file)
                messages.info(request, 'Image Uploaded successfully')
            except FileNotFoundError:
                print("The file was not found")
                messages.info(request, 'Please Capture an Image to upload')
                # return render(request, 'index.html')
            except NoCredentialsError:
                print("Credentials not available")
                os.remove(local_file)
                messages.info(
                    request, 'Please Check ACCESS KEY and SECRET KEY')
                # return render(request, 'index.html')
            except:
                os.remove(local_file)
                messages.info(
                    request, 'Please Check ACCESS KEY and SECRET KEY')

            filename = ""
            ACCESS_KEY = ""
            SECRET_KEY = ""
            bucket = ""
            return render(request, 'index.html')
    else:
        messages.info(request, 'Please fill all the details')
        return render(request, 'index.html')
