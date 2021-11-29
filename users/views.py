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


