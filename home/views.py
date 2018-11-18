from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

def index(request):
    context = {}
#    print(request.session['sess_id_user'])
    if request.session.has_key('sess_id_user'):
        print("has user")
        uc = request.session['sess_id_user']
        context['userp'] = uc.split('_')[2]
    if request.session.has_key('sess_id_donor'):
        print("has donor")
        dc = request.session['sess_id_donor']
        context['donor'] = uc.split('_')[2]
    if request.session.has_key('sess_id_hospital'):
        print("has hospital")
        hc = request.session['sess_id_hospital']
        context['hospital'] = uc.split('_')[2]
    template = loader.get_template('base.html')
    print(context)
    return HttpResponse(template.render(context,request))