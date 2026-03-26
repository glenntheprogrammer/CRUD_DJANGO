from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta


def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    failed_attempts = request.session.get('failed_attempts', 0)
    lock_time = request.session.get('lock_time')

    context = {}

    # Check if locked
    if lock_time:
        unlock_time = timezone.datetime.fromisoformat(lock_time)

        if timezone.now() < unlock_time:
            remaining = int((unlock_time - timezone.now()).total_seconds())
            context['locked'] = True
            context['remaining'] = remaining
            messages.error(request, f"Too many failed attempts. Try again in {remaining} seconds.")
            return render(request, "auth/login.html", context)
        else:
            request.session['failed_attempts'] = 0
            request.session['lock_time'] = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            request.session['failed_attempts'] = 0
            request.session['lock_time'] = None
            login(request, user)
            return redirect("dashboard")
        else:
            failed_attempts += 1
            request.session['failed_attempts'] = failed_attempts

            if failed_attempts >= 5:
                lock_until = timezone.now() + timedelta(minutes=1)
                request.session['lock_time'] = lock_until.isoformat()
                context['locked'] = True
                context['remaining'] = 60
                messages.error(request, "Too many failed attempts. Locked for 1 minute.")
            else:
                remaining_attempts = 5 - failed_attempts
                messages.error(request, f"Incorrect username or password. {remaining_attempts} attempts remaining.")

    return render(request, "auth/login.html", context)


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required(login_url='login')
def dashboard(request):
    return render(request, 'pages/dashboard.html')