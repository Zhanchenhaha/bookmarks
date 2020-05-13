from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from account.forms import LoginForm


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
