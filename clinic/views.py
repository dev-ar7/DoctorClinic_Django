from django import forms
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, query
from .forms import AppoinmentForm, UserForm, ConsultationForm
from .models import Appoinment, Consultation


# Create your views here.

def create_appoinment(request):
    if not request.user.is_authenticated():
        return render(request, 'clinic/login.html')
    else:
        form = AppoinmentForm(request.POST or None)
        if form.is_valid():
            appoinment = form.save(commit=False)
            appoinment.user = request.user
            appoinment.doctor = request.user
            # if file_type not in IMAGE_FILE_TYPES:
            #     context = {
            #         'appoinment': appoinment,
            #         'form': form,
            #     }
            #     return render(request, 'clinic/create_appoinment.html', context)
            appoinment.save()
            return render(request, 'clinic/detail.html', {'appoinment': appoinment})
        context = {
            'form': form,
        }
        return render(request, 'clinic/create_appoinment.html', context)


def create_consultation(request, appointment_id):
    form = ConsultationForm(request.POST or None)
    appointment = get_object_or_404(Appoinment, pk=appointment_id)
    if form.is_valid():
        appointments_consultation = appointment.consultation_set.all()
        for c in appointments_consultation:
            if c.doctor == form.claned_data.get('doctor'):
                context = {
                    'appointment': appointment,
                    'form': form,
                    'error_message': 'You Have Already Added The Apointment',
                }
                return render(request, 'clinic/create_consultation.html', context)
        consultation = form.save(commit=False)
        consultation.appointment = appointment
        consultation.save()
        return render(request, 'clinic/detail.html', {'appointment': appointment})
    context = {
        'appointment': appointment,
        'form': form,
    }
    return render(request, 'clinic/create_consultation.html', context)


def delete_appointment(request, appointment_id):
    appointment = Appoinment.objects.get(pk=appointment_id)
    appointment.delete()
    appointment = Appoinment.objects.filter(user=request.user)
    return render(request, 'clinic/index.html', {'appointment': appointment})


def delete_consultation(request, appointment_id, consultation_id):
    appointment = get_object_or_404(Appoinment, pk=appointment_id)
    consultation = Consultation.objects.get(pk=consultation_id)
    consultation.delete()
    return render(request, 'clinic/detail.html', {'appointment': appointment})


def detail(request, appointment_id):
    if not request.user.is_authnticated():
        return render(request, 'clinic/login.html')
    else:
        user = request.user
        appointment = get_object_or_404(Appoinment, pk=appointment_id)
        return render(request, 'clinic/detail.html', {'appointment': appointment, 'user': user})


def isdoctor(request, consultation_id):
    consultation = get_object_or_404(Consultation, pk=consultation_id)
    try:
        if consultation.is_doctor:
            consultation.is_doctor == False
        else:
            consultation.is_doctor == True
        consultation.save()
    except (KeyError, Consultation.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def favourite_appointment(request, appointment_id):
    appointment = get_object_or_404(Appoinment, pk=appointment_id)
    try:
        if appointment.is_doctor:
            appointment.is_doctor == False
        else:
            appointment.is_doctor == True
        appointment.save()
    except (KeyError, Appoinment.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'clinic/login.html')
    else:
        appointments = Appoinment.objects.filter(user=request.user)
        consultation_results = Consultation.objects.all()
        query = request.GET.get("q")
        if query:
            appointments = appointments.filter(
                Q(doctor_icontains=query) |
                Q(patient_name_icontains=query)
            ).distinct()
            consultation_results = consultation_results.filter(
                Q(doctor_icontains=query)
            ).distinct()
            return render(request, 'clinic/index.html', {
                'appointments': appointments,
                'consultations': consultation_results,
            })
        else:
            return render(request, 'clinic/index.html', {'appointments': appointments})


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        'form': form
    }
    return render(request, 'clinic/login.html', context)


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                appoinments = Appoinment.objects.filter(user=request.user)
                return render(request, 'clinic/index.html', context={'appoinments': appoinments})
            else:
                return render(request, 'clinic/login.htl', {'error_message': 'Your Account Has Been Disabled'})
        else:
            return render(request, 'clinic/login.html', {'error_message': 'Invalid LogIn! Please LogIn Again'})
    return render(request, 'clinic/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                appoinments = Appoinment.objects.filter(user=request.user)
                return render(request, 'clinic/index.html', {'appoinments': appoinments})
    context = {
        'form': form,
    }
    return render(request, 'clinic/register.html', context)


def consultations(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'clinic/login.html')
    else:
        try:
            consultation_id = []
            for appoinment in Appoinment.objects.filter(user=request.user):
                for consultation in appoinment.consultation_set.all():
                    consultation_id.append(consultation.pk)
            users_consultations = Consultation.objects.filter(
                pk_in=consultation_id)
            if filter_by == 'doctor':
                users_consultations = users_consultations.filter(
                    is_favourite=True)
        except Appoinment.DoesNotExist:
            users_consultations = []
        return render(request, 'clinic/consultations.html', {
            'consultation_list': users_consultations,
            'filter_by': filter_by,
        })
