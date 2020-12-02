#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from myTools_Linux import *
import platform

from django.contrib import admin
# # Register your models here.
# from test2 import models
#
# class PersonAdmin(admin.ModelAdmin):
#     list_display = ('name', 'age')
#
# # admin.site.register([models.Blog,models.Author,models.Entry])
# admin.site.register(models.Person,PersonAdmin)

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test2.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

'''
凡是views中用了wrapper的，都会被映射到urls.py文件中。
'''
#在url.py文件中注册接口
def register_api():
    content=readfile('test2/views.py')
    print()
    names_funcs=re.findall('''\n@[a-z,A-Z,_]*?wrapper\('(.+?)'\)\s*?def ([a-z,A-Z,_,0-9]+)''',content)
    content2=readfile('test2/urls.py')
    '''urlpatterns = [
    path('admin', admin.site.urls),
    path('test', views.test),
    path('quant_api', views.quant_api),
    url(r'^$', views.index, name='index'),
]'''
    string="urlpatterns = [\npath('admin', admin.site.urls),"
    for arr in names_funcs:
        name=arr[0]
        func=arr[1]
        string+="\npath('py_x2/%s', views.%s),"%(name,func)
    string+='\n]'
    content2=replace_by_reg2(r'urlpatterns = \[[\s\S]+?\]',string,content2)
    writefile(content2,'test2/urls.py')

def convert_cloud_py():
    cloud_file=r'C:\Important_Storage\Python_Projects\win10_projects\a91_server\cloud.py'
    target_file=r'cloud_converted.py'
    content=readfile(cloud_file)
    def tmp(string):
        name=re.findall("define\('(.+)'\)",string)[0]
        return f"@wrapper('{name}')"
    content=replace_by_reg2("@engine\.define\('.+'\)\s*@handle_error_wrapper",tmp,content)
    writefile(content,target_file)


if __name__ == '__main__':
    #转cloud.py
    main()

