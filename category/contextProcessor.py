from category.models import Category

def menuList(request):
    link = Category.objects.all()
    return {'link': link}