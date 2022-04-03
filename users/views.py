from django.shortcuts import render, get_object_or_404, redirect
from guest_chatRoom.models import GuestChatRoom

from users.models import CustomUser
from .forms import UserEditForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page


CACHE_TIME = 60 * 15 # setting cache time to 15 minutes

@cache_page(CACHE_TIME)
@login_required
def update_user_detail(request):
    user = request.user
    if request.method == "POST":
        # user_form = UserEditForm(instance=request.user, data=request.POST, files=request.FILES)
        user_form = UserEditForm(data=request.POST, files=request.FILES)
        if user_form.is_valid():
            # user_form.save()

            # ('image', 'first_name', 'last_name', 'country', 'age', 'occupation', 'birthday', 'mobile')
            user.image = user_form.cleaned_data["image"]
            user.first_name = user_form.cleaned_data["first_name"]
            user.last_name = user_form.cleaned_data["last_name"]
            user.country = user_form.cleaned_data["country"]
            user.age = user_form.cleaned_data["age"]
            user.occupation = user_form.cleaned_data["occupation"]
            user.birthday = user_form.cleaned_data["birthday"]
            user.mobile = user_form.cleaned_data["mobile"]
            user.save()

            return redirect('rooms:home')
    else:
        user_form = UserEditForm(instance=request.user, files=request.FILES)
    return render(request, 'users/edit_profile_form.html', {'user':user, 'user_form':user_form})


