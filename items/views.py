from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Item
from django.core.mail import send_mail  
from datetime import datetime

@login_required(login_url='login')
def additem(request):
    if request.method == 'POST':

        # check if the user is not setting an invalid start date and end date for the auction
        sdate = request.POST['s_date']
        edate = request.POST['e_date']
        now = datetime.now()
        now_str = now.strftime('%Y-%m-%d %H:%M:%S')

        if (edate >= sdate and sdate >= now_str):
            iname = request.POST['iname']
            prof = request.FILES['img']
            img1 = request.FILES.get('img1')
            img2 = request.FILES.get('img2')
            itag = request.POST['itag']
            disc = request.POST['disc']
            price = request.POST['iprice']
            location = request.POST['location']
            omail = request.user.email

            item = Item(ownermail=omail,start_date=sdate,end_date=edate,currentPrice=price,img1=img1,img2=img2,name=iname,profile=prof,tag=itag,description=disc,basePrice=price,location = location)
            item.save()
            return redirect("home")
        else:
            return render(request,"notification2.html")
    else:
        return render(request,'addItem.html')
    
    
@login_required(login_url='login')
def biditem(request):
    id=request.GET['id']
    item = Item.objects.get(id=id)
    lstatus="live"

    if item.status ==lstatus:
        return render(request,"biditem.html",{'item':item})
    else:
        return redirect("home")
    

# function to validate whether a bid was placed correctly and then to inform the seller

@login_required(login_url='login')
def successfullBid(request):

    value = request.GET.get('bidrs')
    iid = request.GET.get('iid')
    bidder = request.user
    bidderEmail = bidder.email

    item_obj = Item.objects.get(id=iid)

    itemOwnerEmail = item_obj.ownermail

    if bidderEmail == itemOwnerEmail:
        return render(request,"notification.html") # will give an error notification, as seller cannot bid on their own item
    else:
        mail = item_obj.ownermail
        subject = "The Dorm Room Dealer"  
        msg     = "Your item was bidded by "+ bidder.email + ", at Rs" + value + "."
        to      = mail  
        res     = send_mail(subject, msg, "notyourregularbidmaster@gmail.com", [to])

        Item.objects.filter(id=iid).update(currentPrice=value)
        Item.objects.filter(id=iid).update(highest_bidder=bidder.id)
        return redirect("home")
