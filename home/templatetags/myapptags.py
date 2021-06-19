from django import template
from django.db.models import Sum
from django.urls import reverse

from home.models import *

register = template.Library()

@register.simple_tag
def categoryTree():
    # for extending new categories in the future
    categories = {
        'book': {
            'title': 'Sách',
            'getChild': lambda : Theloaisach.objects.all(),
        },
        'electro': {
            'title': 'Điện tử',
            'getChild': lambda : Theloaidientu.objects.all(),
        },
        'clothes': {
            'title': 'Quần áo',
            'getChild': lambda : Theloaiquanao.objects.all(),
        }
    }

    menu = '<ul class="category-list" style="display: none">'

    for key, category in categories.items():
        menu += '\t<li class="dropdown side-dropdown">\n'
        menu += '\t\t<a class="dropdown-toggle" data-toggle="dropdown" aria-expanded="true">' + category['title'] + '<i class="fa fa-angle-right"></i></a>\n'
        menu += '\t\t\t<div class="custom-menu">\n'
        menu += '\t\t\t\t<ul class="list-links">\n'

        childCategories = category['getChild']()
        for child in childCategories:
            menu += '\t\t\t\t\t<li><a href="/home/category/' + key + '/' + str(child.id) +'">' + child.tentheloai + '</a></li>\n' 

        menu += '\t\t\t\t</ul>\n'
        menu += '\t\t\t</div>\n'
        menu += '\t\t</a>\n'
        menu += '\t</li>\n'

    menu += '</ul>'

    return menu