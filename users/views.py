from django.shortcuts import render, get_object_or_404, redirect
from .forms import UserEditForm
from django.contrib.auth.decorators import login_required
# Create your views here.

login_required
def update_user_detail(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('rooms:home')
    else:
        user_form = UserEditForm(instance=request.user)
    return render(request, 'users/profile-form.html', {'user_form':user_form})





# def update_profile(request):
#     user = request.user
#     # user = get_object_or_404(Profile, id=user.id)
#     if request.method == "POST":
#         form = ProfileForm(request.POST)
#         if form.is_valid():
#             profile = form.save(commit=False)
#             profile.user = user
#             profile.first_name = form.cleaned_data.get('first_name')
#             profile.last_name = form.cleaned_data.get('last_name')
#             profile.save()
#             user.first_name = profile.first_name
#             user.last_name = profile.last_name
#             user.save()
            
#             return redirect('rooms:home')
#     else:
#         form = ProfileForm()
#     return render(request, 'users/profile-form.html', {'form':form})