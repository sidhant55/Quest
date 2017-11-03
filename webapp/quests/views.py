from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings

from rest_framework.decorators import api_view

from .serializers import QuestsSerializer
from .forms import Registerkey,Postone,Deleteone,Updateone, Getlist, Getone, Forgotkey
from .models import user

import os



"""View to return home page"""
@api_view(['GET'])
def HomePage(request):
    return render(request, "index.html")


"""Returns django form to save user's credential"""
@api_view(['GET'])
def RegisterKey(request):
    form=Registerkey()
    return render(request,'register.html',{'form': form})


"""Returns django form to post one image on file system"""
@api_view(['GET'])
def PostOne(request):
    form = Postone()
    return render(request,'postone.html',{'form':form})


"""Returns django form to get all images associated with the provided access key"""
@api_view(['GET'])
def GetList(request):
    form=Getlist()
    return render(request, 'getlist.html', {'form': form})


"""Returns django form to get one image"""
@api_view(['GET'])
def GetOne(request):
    form=Getone()
    return render(request,'getone.html',{'form':form})


"""Returns django form to delete one image"""
@api_view(['GET'])
def DeleteOne(request):
    form=Deleteone()
    return render(request, 'deleteone.html', {'form': form})


"""Returns django form to update one image"""
@api_view(['GET'])
def UpdateOne(request):
    form=Updateone()
    return render(request, 'updateone.html', {'form': form})


"""Returns django form to handle forget key request"""
@api_view(['GET'])
def ForgotKey(request):
    form=Forgotkey()
    return render(request, 'forgotkey.html', {'form': form})


"""View to save users credential to db"""
@api_view(['POST'])
def Sign(request):
    #accepting parameters, converting data into json format and saving to the db
    name = request.POST['name']
    key = request.POST['key']
    email=request.POST['email']
    js = {'name': name, 'key': key,'email':email}
    serial = QuestsSerializer(data=js)
    if (serial.is_valid()):
        print(serial)
        serial.save()
        return render(request,'index.html')
    return Response(status=status.HTTP_400_BAD_REQUEST)


"""As per the instrunction of the api specs, detail function handles thre request,
    GET   : dispaly one image,
    DELETE: delete one image,
    PATCH : update one image
"""
@api_view(['GET','DELETE','PATCH'])
def Detail(request):
    #dispaly one image
    if (request.method=='GET'):
        key = request.GET['key']
        img_name = request.GET['image']
        try:
            obj = user.objects.filter(key=key).values('name')
            #framing folder name eg: (user's name)_(user's key)
            folder = "tmp/"+obj[0]['name'] + "_" + key
            arr = []
            #getting to the targeted image
            arr.append(folder + "/" + img_name)
            return render(request, 'display.html', {'arr': arr})
        except BaseException as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    #delete one image
    elif (request.method=='DELETE'):
        key = request.POST['key']
        img = request.FILES['image']
        img_name = img.name
        try:
            obj = user.objects.filter(key=key).values('name')
            # framing folder name eg: (user's name)_(user's key)
            dir_path = "tmp/"+obj[0]['name'] + "_" + key+ "/" + img_name
            os.remove(dir_path)
        except BaseException as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)

    #update one image
    elif (request.method=='PATCH'):
        key = request.POST['key']
        img = request.FILES['image']
        img_name = img.name
        try:
            obj = user.objects.filter(key=key).values('name')
            # framing folder name eg: (user's name)_(user's key)
            dir_path = "tmp/" + obj[0]['name'] + "_" + key
            img_list = os.listdir(dir_path)
            f = open(dir_path + "/" + img_name, 'wb')
        except BaseException as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        flag = 0
        #if existing image name matches with the given image name, update with the given image name
        for i in range(len(img_list)):
            if (img_list[i] == img_name):
                flag = 1
                break
        print(flag)
        if (flag == 0):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        for chunk in img.chunks():
            f.write(chunk)
        return Response(status=status.HTTP_200_OK)


"""As per the instrunction of the api specs, list function handles thre request,
    GET   : dispaly all image,
    POST  : save one image
"""
@api_view(['GET','POST'])
def List(request):
    #dispaly all image
    if (request.method=='GET'):
        key=request.GET['key']
        try:
            obj = user.objects.filter(key=key).values('name')
            # framing folder name eg: (user's name)_(user's key)
            folder = "tmp/" + obj[0]['name'] + "_" + key
            dir_path = (folder)
            img_list = os.listdir(dir_path)
            arr = []
            #store location of the entire images inside directory dir_path
            for i in range(len(img_list)):
                arr.append(folder + "/" + img_list[i])
            return render(request, 'display.html', {'arr': arr})
        except BaseException as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    #save one image
    elif (request.method=='POST'):
        key=request.POST['key']
        img = request.FILES['image']
        img_name = img.name
        try:
            obj = user.objects.filter(key=key).values('name')
            folder = obj[0]['name'] + "_" + key
            dir_path = ("tmp/" + folder)
        except BaseException as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            os.mkdir(dir_path)
        except OSError as e:
            print(e)
        f = open(dir_path + "/" + img_name, 'wb')
        for chunk in img.chunks():
            f.write(chunk)
        return Response(status=status.HTTP_200_OK)


"""Its a repeat function to delete an image via django forms
    used this function because i was not able to send DELETE request from form"""
@api_view(['POST'])
def Delete(request):
    key = request.POST['key']
    image = request.FILES['image']
    img = image.name
    try:
        obj = user.objects.filter(key=key).values('name')
        folder = obj[0]['name'] + "_" + key
        dir_path = ("tmp/" + folder)
        img_list = os.listdir(dir_path)
        dir_path = dir_path + "/" + img
        print(dir_path, img_list, img, len(img_list))
        os.remove(dir_path)
    except BaseException as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)


"""Its a repeat function to update an image via django forms
    used this function because i was not able to send PATCH request from form"""
@api_view(['POST'])
def Patch(request):
    key = request.POST['key']
    img = request.FILES['image']
    img_name = img.name
    try:
        obj = user.objects.filter(key=key).values('name')
        folder = obj[0]['name'] + "_" + key
        dir_path = ("tmp/" + folder)
        img_list = os.listdir(dir_path)
        f = open(dir_path + "/" + img_name, 'wb')
    except BaseException as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    flag = 0
    for i in range(len(img_list)):
        if (img_list[i] == img_name):
            flag = 1
            break
    print(flag)
    if (flag == 0):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    for chunk in img.chunks():
        f.write(chunk)
    return Response(status=status.HTTP_200_OK)


"""An end point to access key, This function sends the access key to the user's email address"""
@api_view(['POST'])
def MailKey(request):
    email=request.POST['email']
    print(email)
    try:
        obj = user.objects.filter(email=email)
        ema=obj[0].email
        key=obj[0].key
        send_mail(
            'Access Key',
            'your access key is '+key,
            settings.EMAIL_HOST_USER,
            [ema],
            fail_silently=True
        )

    except BaseException as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)