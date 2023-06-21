from django.shortcuts import render, redirect
from django.contrib import auth
from .models import User
from django.core.files.storage import default_storage


def signup(request):
    if request.method == 'POST':
        if User.objects.filter(username=request.POST.get("username")).exists():
            return render(request, "signup.html", {"message": "이미 존재하는 회원입니다."})
        else:
            profile_image = request.FILES.get('profile_image')
            if profile_image:
                file_path = default_storage.save('profile_images/' + profile_image.name, profile_image)
            else:
                file_path = 'profile_images/person.png'

            user = User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password'],
                first_name=request.POST['name'][0],
                last_name=request.POST['name'][1:],
                profile_image=file_path
            )
            auth.login(request, user)
            return redirect('/')

    else:
        return render(request, 'account/signup.html')


def profile(request):
    user = request.user
    recently_viewed_products = user.recently_viewed_products.all()[:5]  # 최근 조회한 제품 목록 (상위 5개)
    liked_products = user.liked_products.all()  # 사용자가 좋아요를 누른 제품들

    context = {
        'user': user,
        'recently_viewed_products': recently_viewed_products,
        'liked_products': liked_products,
    }
    return render(request, 'account/profile.html', context)
def user_update(request):
    if request.method == "POST":
        profile_image = request.FILES.get('profile_image')
        if profile_image:
            file_path = default_storage.save('profile_images/' + profile_image.name, profile_image)
        else:
            file_path = request.user.profile_image
        print(file_path)
        user = request.user
        user.first_name = request.POST.get("name")[0]
        user.last_name = request.POST.get("name")[1:]
        user.profile_image = file_path
        user.save()
        auth.login(request, user)
        return redirect("/")
    else:
        return render(request, "account/profile.html")


def user_delete(request):
    if request.user.is_authenticated:
        request.user.delete()
        auth.logout(request)
    return redirect("/")
