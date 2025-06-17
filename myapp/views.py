from django.shortcuts import render, redirect
from django.http import HttpResponse
from myapp.models import *
from django.forms.models import model_to_dict
from django.db.models import Q
from django.core.paginator import Paginator  #分頁器,目前寫在INDEX裡

def search_list(request):
    if 'cName' in request.GET:
        cName = request.GET["cName"]
        print(cName)
        #resultList = students.objects.filter(cName=cName)
        resultList = students.objects.filter(cName__contains=cName) #更好的語法,只要是關鍵字就可以找到_contains=

    else:
        resultList = students.objects.all()
    
    errorMassage=""
    if not resultList:
        errorMassage="無此資料"

    #檢查看看有沒有資料用的迴圈
    # for data in resultList:
    #     print(model_to_dict(data))
    #return HttpResponse("HeLlo")

    return render(request, "search_list.html" , locals())

def index(request):
    if 'site_search' in request.GET:
        site_search = request.GET["site_search"]
        site_search = site_search.strip()
        #print(site_search)
        #一個關鍵字,搜尋一個欄位
        #reultList = students.objects.filter(cName__contains=site_search)
        #----------------------------------------
        #一個關鍵字,搜尋多欄位(Q表逹示,要import Q)
        reultList = students.objects.filter(
            Q(cName__contains=site_search)|
            Q(cBirthday__contains=site_search)|
            Q(cEmail__contains=site_search)|
            Q(cPhone__contains=site_search)|
            Q(cAddr__contains=site_search))
            
        #----------------------------------------
        #多個關鍵字,搜尋多欄位
        keywords = site_search.split() #切割
        print(keywords)
        #reultList = []
        q_object = Q()
        for keywork in keywords:
            q_object.add(Q(cName__contains=keywork),Q.OR)
            q_object.add(Q(cBirthday__contains=keywork),Q.OR)
            q_object.add(Q(cEmail__contains=keywork),Q.OR)
            q_object.add(Q(cPhone__contains=keywork),Q.OR)
            q_object.add(Q(cAddr__contains=keywork),Q.OR)
        resultList = students.objects.filter(q_object)

    else:
        resultList = students.objects.all().order_by("cID")
    dataCount = len(resultList)  #顯示筆數
    status = True
    errormessage = ""
    if not resultList:
        status = False
        errormessage = "無此資料"

    #分頁設定,每頁3筆資料
    paginator = Paginator(resultList, 1)  #(資料來源,每頁數量)
    page_number = request.GET.get("page")  #自訂變數名稱
    page_obj = paginator.get_page(page_number)  #get_page()根據上方訂義取得(自訂變數名稱的資料)
    #page_obj 包含該頁資料的物件
    #page_obj.object_list:該頁資料
    #page_obj.has_next(下一頁), page_obj.has_previous (上一頁)-->是否有下一頁或上一頁
    #page_obj.next_page_number, page_obj.previous_page_number #上一頁,下一頁
    #page_obj.number 目前頁碼
    #page_obj.paginator.num_pages:總頁數(最後一頁頁)
    #page_obj.paginator.page_range(這個寫在html的for迴圈裡可顯示頁碼)



        # print(dataCount)
        # #return HttpResponse("HeLlo")
    return render(request, "index.html" , locals())

def edit(request,id=None):
    print(f"id={id}")
    if request.method == "POST":
        cName = request.POST["cName"]
        cSex =request.POST["cSex"]
        cBirthday =request.POST["cBirthday"]
        cEmail =request.POST["cEmail"]
        cPhone =request.POST["cPhone"]
        cAddr =request.POST["cAddr"]   #以上是post收到資料,再次定義給變數
        print(f"cName={cName},cSex={cSex},cBirthday={cBirthday},cEmail={cEmail},cPhone={cPhone},cAddr={cAddr}")
        #ORM
        update = students.objects.get(cID=id)   #以下是更新至資料庫的動作
        update.cName = cName
        update.cSex = cSex
        update.cBirthday = cBirthday
        update.cEmail = cEmail
        update.cPhone = cPhone
        update.cAddr = cAddr
        update.save()
        return redirect("/index/") #更新完回首頁
        #return HttpResponse(f"HeLlo{cName}己更新完成")
    else:
        obj_data = students.objects.get(cID=id)
        print(model_to_dict(obj_data))
        return render(request, "edit.html",locals())