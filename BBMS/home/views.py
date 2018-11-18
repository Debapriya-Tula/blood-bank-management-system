from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

def index(request):
    context = {}
#    print(request.session['sess_id_user'])

    if request.session.has_key('sess_id_user'):
        uc = request.session['sess_id_user']
        context['userp'] = uc.lstrip('bbms_user')

    if request.session.has_key('sess_id_donor'):
        dc = request.session['sess_id_donor']
        context['donor'] = dc.lstrip('bbms_donor')

    if request.session.has_key('sess_id_hospital'):
        hc = request.session['sess_id_hospital']
        print(hc)
        hc = hc.lstrip('bbms_')
        context['hospital'] = hc.lstrip('hospital')
        print('working',context['hospital'])
    template = loader.get_template('main.html')
    return HttpResponse(template.render(context,request))