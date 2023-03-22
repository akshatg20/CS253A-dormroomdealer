from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from items.models import Item
from .models import Detail
from django.core.mail import send_mail
from datetime import datetime
from django.utils import timezone
import datetime
from django.core.paginator import Paginator

# function to implement the login facility
def login(request):
    if request.method == 'POST':
        username = request.POST.get('un','')
        pwd = request.POST.get('pa','')
        user = auth.authenticate(username=username,password=pwd)

        if user == None:
            messages.info(request,"Invalid Username/Password")
            return redirect('login')
        else:
            auth.login(request,user)
            return redirect("home")
            
    else:
        return render(request,'login.html')

# function to implement the registration utility for a new user
def register(request):
    if request.method == 'POST':
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        username = request.POST['username']
        mail = request.POST['email']
        p1 = request.POST['p1']
        p2 = request.POST['p2']

        contact = request.POST['contact']
        if p1 == p2:
            if User.objects.filter(email=mail).exists():
                messages.info(request,"User with this Email already exits")
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request,"Username Taken")
                return redirect('register')
            else:
                user = User.objects.create_user(first_name=firstname,last_name=lastname,email=mail,password=p1,username=username)
                user.save()
                obj = Detail(username=username,contact=contact)
                obj.save()
                subject = "The Dorm Room Dealer"  
                msg     = "Succesfull Registration!"
                to      = mail  
                res     = send_mail(subject, msg, "notyourregularbidmaster@gmail.com'", [to])
                if res == 1:
                    return redirect('/')
                else:
                    messages.info(request,"Error")
                return redirect('/')
        else:
            messages.info(request,"Password does not match")
            return redirect('register')
    else:
        return render(request,'register.html')

# logout function    
def logout(request):
    auth.logout(request)
    return redirect("login") 

# function to logout from the items
def ilogout(request):
    auth.logout(request)
    return redirect("login") 

# function to implement the user information dashboard
@login_required(login_url='login')
def myprofile(request):
    bidder = request.user
    details = bidder
    username = details.username

    obj = Detail.objects.filter(username=username)
    contact = ""
    for i in obj:
        contact = i.contact
    return render(request,"myprofile.html",{"details":details,"contact":contact})

# helper function to update the current status of items on the application
@login_required(login_url='login')
def productStatus(request):

    item = Item.objects.all()
    for i in item:
        try:
            highest_bidder = i.highest_bidder
            if highest_bidder is not None and i.status == "live":
                i.sold = "Bidded"
                i.save()
            elif highest_bidder is not None and i.status == "past":
                i.sold = "Sold"    
                i.save()
            elif i.status == "future":
                i.sold = "Yet to be auctioned"
                i.save()
            else:
                i.sold = "Unsold"
                i.save()
        except:
            pass

# helper function to send mails
@login_required(login_url='login')
def sendMail(request):
    now = timezone.now()
    item = Item.objects.filter(end_date = now ).filter(sold="sold").filter(sendwinmail="notSent")
    for i in item :
        try:
            # Selecting the attributes of the auction winner

            winnerID = i.highest_bidder
            user_obj = User.objects.get(id = winnerID)
            winnerEmail = user_obj.email
            winnerUsername = user_obj.username          
            #-----------------------------------------------------------
            obj = Detail.objects.get(username=winnerUsername)
            winnerContact = obj.contact
            
            itemMail = i.ownermail
            itemUserobj = User.objects.get(email=itemMail)
            itemUser = itemUserobj.username

            obj2 = Detail.objects.get(username=itemUser)
            itemContact = obj2.contact
            #-------------------------------------------------------------

            # Mail sent to the highest bidder
            subject = "The Dorm Room Dealer"  
            msg     = "You have successfuly purchased " + i.name + "'s. Email-id of the seller is " + i.ownermail + ". You can contact the seller for further informations at " + itemContact + "."
            to      = winnerEmail  
            res     = send_mail(subject, msg, "notyourregularbidmaster@gmail.com", [to])
            if res == 1:
                print ("Mail sent")
            else:
                print("Error. Mail not sent.")
            
            # Mail sent to the seller
            subject = "The Dorm Room Dealer"  
            msg     = "Your item " + i.name + "'s higgest bidder's email id is "+ winnerEmail + " . You can contact them for further informations at " + winnerContact + "."
            to      = i.ownermail  
            res     = send_mail(subject, msg, "notyourregularbidmaster@gmail.com", [to])
            if res ==1:
                print ("Mail sent")
            else:
                print("Error. Mail not sent.")
            i.sendwinmail="sent"
            i.save()
        except:
            pass

# function to implement the home page of the application, which will show the live bids
@login_required(login_url='login')
def home(request):

    # creating a category search on the top of the home page
    if request.method == "POST":
        category = request.POST.get('category')
    else:    
        category = "All categories"

    items = Item.objects.all()
    today = timezone.now()
    
    # assigning status to each product
    for i in items:

        # if item start_date not mentioned , we take today as the default value
        i.start_date = i.start_date or today                       
        # if item end_date not mentioned, we take tomorrow as the default value
        i.end_date = i.end_date or today + datetime.timedelta(days=1)  

        if(today < i.start_date):
            i.status = "future"
        elif (i.start_date <= today < i.end_date and i.status != "past"):
            i.status = "live"
        else:
            i.status = "past"

        i.save()

    productStatus(request)
    sendMail(request)

    if category != "All categories" and category != None:
        items = Item.objects.filter(status="live").filter(tag=category)
    else:
        items = Item.objects.filter(status="live")

    # paginating
    paginator = Paginator(items, 6) # Show 6 products per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)    

    # adding future auctions
    itemsfuture = Item.objects.filter(status="future")

    return render(request,"home.html",{'page_obj': page_obj, 'items': itemsfuture})


# This function mainains a log of the user's history with the application
@login_required(login_url='login')
def dashboard(request):

    # Checking if seller stopped the auction beforehand
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
    else:
        item_id = None

    if item_id is not None:
        item = Item.objects.get(id=item_id)
        item.status = "past"
        item.save()

    # Select the bidder attributes to send the mail in case the auction was stopped beforehand

        try:

            winnerID = item.highest_bidder
            user_obj = User.objects.get(id=winnerID)
            winnerEmail = user_obj.email
            winnerUsername = user_obj.username

            # -----------------------------------------------------------
            obj = Detail.objects.get(username=winnerUsername)
            winnerContact = obj.contact

            itemMail = item.ownermail
            itemUserobj = User.objects.get(email=itemMail)
            itemUser = itemUserobj.username

            obj2 = Detail.objects.get(username=itemUser)
            itemContact = obj2.contact

            # -------------------------------------------------------------
            # Mail sent to the highest bidder

            subject = "The Dorm Room Dealer"  
            msg     = "You have successfuly purchased " +item.name+"'s. Email-id of the seller is "+item.ownermail+". You can contact the seller for further informations at " +itemContact+ "."
            to      = winnerEmail  
            res     = send_mail(subject, msg, "notyourregularbidmaster@gmail.com", [to])
            if res ==1:
                print ("Mail sent")
            else:
                print("Error. Mail not sent.")

            # Mail sent to the seller

            subject = "The Dorm Room Dealer"  
            msg     = "Your item "+item.name+"'s higgest bidder's email id is "+winnerEmail+" . You can contact them for further informations at "+winnerContact +"."
            to      = item.ownermail  
            res     = send_mail(subject, msg, "notyourregularbidmaster@gmail.com", [to])
            if res == 1:
                print ("Mail sent")
            else:
                print("Error. Mail not sent.")
            item.sendwinmail = "sent"
            item.save()
        except:
            pass


    # Setting up the user information 

    bidder = request.user
    details = bidder
    username = details.username

    obj3 = Detail.objects.filter(username=username)
    contact = ""
    for i in obj3:
        contact = i.contact


    # Setting up the user items history information
    user = request.user
    mail = user.email
    id = user.id
    item_obj = Item.objects.filter(highest_bidder = id)

    biddeditem = item_obj

    pitem = Item.objects.filter(ownermail = mail).filter(status="past")
    litem = Item.objects.filter(ownermail = mail).filter(status="live")
    fitem = Item.objects.filter(ownermail = mail).filter(status="future")
    return render(request, "dashboard.html", {'pitem': pitem, 'litem': litem, 'fitem': fitem, "biddeditem": biddeditem, "details":details,"contact":contact})

