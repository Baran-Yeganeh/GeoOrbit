from django.shortcuts import render

def mainPage(request):
    context={
        'name':'Baran'
        
    }
    return render(request,'main/firstPage.html',context)

def projectIntroduction(request):
    context={
        'name': 'introduce'
    }
    return render(request,'main/projectIntroduction.html',context)