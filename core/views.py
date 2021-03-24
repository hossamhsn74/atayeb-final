from django.shortcuts import render, redirect

from .models import (AboutUsCard, AboutUsParagraph, ContactParagraph,
                     ContactSideParagraph, FaqQuestionBanner, FaqShortBanner,
                     SiteIdentity, ContactLocation, ContactMessages, NewsLetterEmail)


def HomePageView(request):
    context = {}

    # site_identity = SiteIdentity.objects.filter(user=request.user)[:1]
    # print(type([site_identity[0]]))
    # item = site_identity[0]
    # if site_identity != None:
    #     print(item.title)
    #     context['identity'] = item
    # else:
    #     pass

    print("context", context)
    return render(request, 'core/home.html', context)


def FaqPageView(request):
    context = {}
    context['shortbanners'] = FaqShortBanner.objects.all()
    context['questions'] = FaqQuestionBanner.objects.all()
    return render(request, 'core/faq.html', context)


def AboutUsPageView(request):
    context = {}
    context['paragraphs'] = AboutUsParagraph.objects.all()
    context['cards'] = AboutUsCard.objects.all()
    return render(request, 'core/about.html', context)


def ContacUsView(request):
    context = {}
    context['paragraphs'] = ContactParagraph.objects.all()
    context['side_paragraphs'] = ContactSideParagraph.objects.all()
    context['location'] = ContactLocation.objects.all()[:1]
    return render(request, 'core/contact.html', context)


def SendContactMessageView(request):
    address = request.POST['address']
    email = request.POST['email']
    message = request.POST['message']
    ContactMessages.objects.create(
        email=email, address=address, message=message)
    return redirect("core:home")


def NewsLetterSubscribe(request):
    email = request.POST['EMAIL']
    NewsLetterEmail.objects.create(email=email)
    return redirect("core:home")
