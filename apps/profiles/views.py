from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Profile


# PAGE
def list_page(request):
    return render(request, 'profiles/list.html')


# AJAX LIST
def list_ajax(request):
    profiles = list(Profile.get_all_records())
    return JsonResponse({"data": profiles})


# AJAX GET
def get_ajax(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    return JsonResponse({
        "id": profile.id,
        "name": profile.name,
        "address": profile.address,
        "bday": profile.bday,
    })


# AJAX SAVE (CREATE + UPDATE)
def save_ajax(request):
    if request.method == "POST":
        pk = request.POST.get("id")

        if pk:
            profile = Profile.objects.get(pk=pk)
        else:
            profile = Profile()

        profile.name = request.POST.get("name")
        profile.address = request.POST.get("address")
        profile.bday = request.POST.get("bday")
        profile.save()

        return JsonResponse({"success": True})


# AJAX DELETE
def delete_ajax(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    profile.delete()
    return JsonResponse({"success": True})