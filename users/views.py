from django.shortcuts import render, get_object_or_404, redirect
from guest_chatRoom.models import GuestChatRoom

from users.models import CustomUser
from .forms import UserEditForm
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def update_user_detail(request):
    user = request.user
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST, files=request.FILES)
        if user_form.is_valid():
            user_form.save()
            return redirect('rooms:home')
    else:
        user_form = UserEditForm(instance=request.user, files=request.FILES)
    return render(request, 'users/edit_profile_form.html', {'user':user, 'user_form':user_form})


