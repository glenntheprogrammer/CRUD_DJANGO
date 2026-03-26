from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import UserForm

# PAGE
@login_required
def user_list_page(request):
    return render(request, 'users/list.html')


# LIST USERS (AJAX)
@login_required
def user_list_ajax(request):
    users = list(User.objects.all().values(
        'id',
        'username',
        'first_name',
        'last_name',
        'email',
        'is_staff',
        'is_active'
    ))

    return JsonResponse({
        "data": users
})

# GET SINGLE USER
@login_required
def user_get_ajax(request, pk):
    user = get_object_or_404(User, pk=pk)

    data = {
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "is_staff": user.is_staff,
        "is_active": user.is_active,
    }

    return JsonResponse(data)


# CREATE / UPDATE USER
@login_required
@require_POST
def user_save_ajax(request):

    user_id = request.POST.get("id")

    if user_id:
        user = get_object_or_404(User, pk=user_id)
    else:
        user = User()

    user.username = request.POST.get("username")
    user.first_name = request.POST.get("first_name")
    user.last_name = request.POST.get("last_name")
    user.email = request.POST.get("email")
    user.is_staff = request.POST.get("is_staff") == "true"
    user.is_active = request.POST.get("is_active") == "true"

    password = request.POST.get("password")
    if password:
        user.set_password(password)

    user.save()

    return JsonResponse({"status": "success"})


# DELETE USER
@login_required
@require_POST
def user_delete_ajax(request, pk):

    user = get_object_or_404(User, pk=pk)

    if request.user == user:
        return JsonResponse({"error": "You cannot delete yourself"}, status=400)

    user.delete()

    return JsonResponse({"status": "deleted"})