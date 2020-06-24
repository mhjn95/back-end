from django.shortcuts import render,redirect
from .models import Contact
from django.contrib.auth.models import User,auth
from django.core.mail import send_mail
from django.contrib import messages
# Create your views here.
def contact(request):
    if request.method == 'POST':
        # print('HELL YES')
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']
        fn = name.split(' ')[0]


        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id,user_id=user_id)
            if has_contacted:
                messages.error(request,'You have already made an inquiry for this home')
                return redirect('/listings/'+listing_id)




        contact = Contact(listing=listing,listing_id=listing_id,name=name,email=email,phone=phone,message=message,user_id=user_id)
        contact.save()
        send_mail(
            'Property Listing Inquiry',
            'Thank you '+fn+ ' for showing interest in ' + listing + '.Sign into the admin panel for more info.',
            '',#the mail through which you wanna send ,mentioned in settings.py
            [email],
            fail_silently = False
        )
        messages.success(request,'Your inquiry will be attended shortly !')
        return redirect('/listings/'+listing_id)
