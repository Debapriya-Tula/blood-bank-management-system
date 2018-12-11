from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect

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

def toportal(request):
    if request.method == "GET":
        togo = request.GET.get("togo")
        print(togo)
        dt = {'donor':0,'patient':0,'hospital':0}
        context={}
        if request.session.has_key('sess_id_user'):
            uc = request.session['sess_id_user']
            context['userp'] = uc.lstrip('bbms_user')
            dt['patient'] = 1
        if request.session.has_key('sess_id_donor'):
            dc = request.session['sess_id_donor']
            context['donor'] = dc.lstrip('bbms_donor')
            dt['donor'] = 1
        if request.session.has_key('sess_id_hospital'):
            hc = request.session['sess_id_hospital']
            print(hc)
            hc = hc.lstrip('bbms_')
            context['hospital'] = hc.lstrip('hospital')
            print('working',context['hospital'])
            dt['hospital'] = 1
        print(context)
        request.session['sess_togo']=togo
        if dt[togo]:
            return HttpResponseRedirect('/payments/bd_'+togo)
        else:
            return HttpResponseRedirect('/accounts/login')
