from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
import cv2
import boto3
from botocore.exceptions import NoCredentialsError
import os
#ACCESS_KEY = 'AKIAWZWHC4N22ZGNBSZ3'
#SECRET_KEY = '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'
count = 0


def home(request):
    return render(request, "index.html")


def capture_img(request):
    global count
    global ACCESS_KEY
    global SECRET_KEY
    if request.method == 'POST':
        name = request.POST['name']
        filename = name + ".jpg"
        ACCESS_KEY = request.POST['ak']
        SECRET_KEY = request.POST['sk']
    else:
        count = count + 1
        filename = "cloud" + str(count) + ".jpg"
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
    uploaded = upload_img(filename)
    print(uploaded)
    if uploaded == True:
        return HttpResponse("<h1>Image Uploaded Successfully</h1>")
    else:
        return HttpResponse("<h1>Please Check ACCESS KEY and SECRET KEY</h1>")


def upload_img(filename):
    local_file = filename
    bucket = "cloud-a-thon"
    s3_file = filename
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        os.remove(local_file)
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False
    except:
        return False


@csrf_exempt
def save_image(request):
    if request.POST:
        # save it somewhere
        f = open('/static/user/save_image/someimage.jpg', 'wb')
        f.write(request.raw_post_data)
        f.close()
        # return the URL
        return HttpResponse('http://localhost:8080/site_media/webcamimages/someimage.jpg')
    else:
        return HttpResponse('no data')
