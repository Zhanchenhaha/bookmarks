from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render
from .models import Profile

# Create your views here.
from account.forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm


def user_login(request):
    # 判断http请求方式
    if request.method == "POST":
        # 实例化表单对象
        form = LoginForm(request.POST)
        # 判断表单内容是否是有效的
        if form.is_valid():
            # 维护表单数据格式
            cd = form.cleaned_data
            # 验证提交的证书是否是有效的
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Authenticated successfully")
                else:
                    return HttpResponse("Disable templates")
            else:
                return HttpResponse("Invalid login")

    else:
        form = LoginForm()

    return render(request, "account/login.html", {'form': form})


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # 建立新数据对象但不写入数据库
            new_user = user_form.save(commit=False)
            # 设置密码
            new_user.set_password(user_form.cleaned_data['password'])
            # 保存User对象
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
    try:
        profile = request.user.profile
    except ObjectDoesNotExist:
        profile = Profile(user=request.user)
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(isinstance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form':  profile_form})