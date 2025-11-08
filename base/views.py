from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from .models import GymPlan, Member, SupportMessage, Trainer



def login_view(request):
    plans = GymPlan.objects.all()

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            member = Member.objects.get(email=email)
            if check_password(password, member.password) or member.password == password:
                request.session['member_id'] = member.id
                request.session['member_name'] = member.name
                return redirect('dashboard')
            else:
                messages.error(request, "Incorrect password.")
        except Member.DoesNotExist:
            messages.error(request, "No account found with that email.")

    return render(request, 'home.html', {'plans': plans})


def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        membership = request.POST.get('membership')
        time = request.POST.get('time')
        profile_pic = request.FILES.get('profile_pic')


        if password != confirm_password:
            messages.error(request, 'passwords do not match!')
            return render(request, 'register.html')


        if Member.objects.filter(email=email).exists():
            messages.error(request, 'This email is already registered!')
            return render(request, 'register.html')


        hashed_password = make_password(password)


        Member.objects.create(
            name=name,
            email=email,
            phone=phone,
            password=hashed_password,
            membership=membership,
            preferred_time=time,
            profile_pic=profile_pic
        )

        messages.success(request, "Registration Succesgull !login!.")
        return redirect('login')

    return render(request, 'register.html')


def payment_view(request):
    member_id = request.session.get('member_id')
    if not member_id:
        return redirect('login')

    member = Member.objects.get(id=member_id)

    plan_prices = {
        'GOLD': {'price': 800, 'duration': 28},
        'PLATINUM': {'price': 1200, 'duration': 30},
        'IRON': {'price': 2000, 'duration': 35},
    }

    plan_info = plan_prices.get(member.membership, {'price': 0, 'duration': 0})

    if request.method == "POST":
        member.payment_confirmed = True
        member.start_date = timezone.now().date()
        member.save()
        return redirect('dashboard')

    return render(request, 'payment.html', {'member': member, 'plan_info': plan_info})


def dashboard(request):
    member_id = request.session.get('member_id')
    if not member_id:
        return redirect('login')

    member = Member.objects.get(id=member_id)

    support_messages = (
        SupportMessage.objects.filter(member=member)
        | SupportMessage.objects.filter(email=member.email)
    ).order_by('-created_at')

    return render(request, 'dashboard.html', {
        'member': member,
        'messages': support_messages
    })


def support(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        member = None
        if request.session.get("member_id"):
            member = Member.objects.get(id=request.session["member_id"])

        SupportMessage.objects.create(
            name=name,
            email=email,
            message=message,
            member=member
        )

        return render(request, "support.html", {"success": True})

    return render(request, "support.html")


def about(request):
    return render(request, 'about.html')


def logout_view(request):
    request.session.flush()
    messages.success(request, "Logged out successfully.")
    return redirect('login')

# -------------------- TRAINER SECTION --------------------

def trainer_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        specialization = request.POST.get('specialization')
        experience = request.POST.get('experience')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'trainer_register.html')

        if Trainer.objects.filter(email=email).exists():
            messages.error(request, "A trainer with this email already exists.")
            return render(request, 'trainer_register.html')

        hashed_password = make_password(password)

        Trainer.objects.create(
            name=name,
            email=email,
            password=hashed_password,
            phone=phone,
            specialization=specialization,
            experience=experience
        )

        messages.success(request, "Trainer registered successfully! Please wait for admin approval before logging in.")

        return redirect('trainer_login')

    return render(request, 'trainer_register.html')


def trainer_login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        if not email or not password:
            return render(request, 'trainer_login.html', {'error': 'Please enter both email and password.'})

        try:
            trainer = Trainer.objects.get(email=email)

            # Check if approved
            if not trainer.is_approved:
                return render(request, 'trainer_login.html', {
                    'error': 'Your account is pending admin approval. Please wait.'
                })

            if check_password(password, trainer.password) or trainer.password == password:
                return redirect('trainer_dashboard', trainer_id=trainer.id)
            else:
                return render(request, 'trainer_login.html', {'error': 'Invalid password'})

        except Trainer.DoesNotExist:
            return render(request, 'trainer_login.html', {'error': 'Invalid email'})

    return render(request, 'trainer_login.html')



def trainer_dashboard(request, trainer_id):
    trainer = Trainer.objects.get(id=trainer_id)
    members = Member.objects.all().order_by('-start_date')
    return render(request, 'trainer_dashboard.html', {
        'trainer': trainer,
        'members': members
    })

def locate(request):
    return render(request, 'locate.html')

