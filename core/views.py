from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from django.conf import settings
from django.views.generic import View, ListView, DetailView, TemplateView
from .models import Project, Instagram
from .forms import ContactForm


# ---------------------------------------------------------------------------- #
class HomePageView(View):
    def get(self, *args, **kwargs):
        posts = Instagram.objects.all()
        projects = Project.objects.all()
        form = ContactForm()
        context = {
            "posts": posts,
            "projects": projects,
            "form": form
        }
        return render(self.request, 'home.html', context, status=200)

    def post(self, *args, **kwargs):
        form = ContactForm(self.request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = f"{name} ({email} says: {form.cleaned_data['message']}"
            try:
                send_mail(subject, message, email, ['jharriswebdev@gmail.com'])
                messages.success(self.request, "Your message has been sent. I'll get back to you ASAP!")
                return redirect("core:home")
            except BadHeaderError:
                messages.warning(self.request, "Invalid header found. Try again or connect with me on social media.")
                return redirect("core:home")
            except Exception as e:
                messages.warning(self.request, "Something went wrong. Please try again or connect with me on social media.")
                print(e)
                return redirect("core:home")
            