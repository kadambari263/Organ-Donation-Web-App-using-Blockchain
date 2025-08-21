from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from home.model.auth import HospitalProfile
from django.contrib import messages




@login_required
def profile_view(request):
    user = request.user
    profile = HospitalProfile.objects.filter(user=user).first()
    print(f"Logged in user: {user.username}")
    print(f"Profile found: {profile}")
    if profile:
        print(f"Hospital name: {profile.hospital_name}")
    else:
        print("No profile found for this user")
    return render(request, 'other/profile.html', {
        'user': user,
        'profile': profile,
    })

@login_required
def edit_profile_view(request):
    profile, _ = HospitalProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile.hospital_name = request.POST.get('hospital_name', '')
        profile.branch_name = request.POST.get('branch_name', '')
        profile.address = request.POST.get('address', '')
        profile.mobile_number = request.POST.get('mobile_number', '')
        profile.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')

    context = {
        'hospital_name': profile.hospital_name,
        'branch_name': profile.branch_name,
        'address': profile.address,
        'mobile_number': profile.mobile_number,
    }
    return render(request, 'other/edit_profile.html', context)