from django.shortcuts import render
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
import datetime
from django.utils.translation import get_language, activate
from django.template.defaultfilters import date

from .models import *


# Create your views here.



class GetAllMasterView(APIView):

    def post(self, request, *args, **kwargs):
        idfirma = request.data['idfirma']
        client = Master.objects.filter(active=True, firma_id=idfirma)
        spisok = []
        for mst in client:
            op = {}
            op['text'] = mst.fio
            op['value'] = mst.id
            spisok.append(op)

        problem = Problem.objects.filter(firma_id=idfirma)
        prob = []
        for mst in problem:
            op = {}
            op['text'] = mst.type
            op['value'] = mst.id
            prob.append(op)

        proritet = Prioritet.objects.all()
        prior = []
        for mst in proritet:
            op = {}
            op['text'] = mst.type
            op['value'] = mst.id
            prior.append(op)

        client = Client.objects.filter(firma_id=idfirma)
        cli = []
        for mst in client:
            op = {}
            op['text'] = mst.company
            op['value'] = mst.id
            cli.append(op)

        status = Status.objects.all()
        stat = []
        for mst in status:
            op = {}
            op['text'] = mst.type
            op['value'] = mst.id
            stat.append(op)

        return Response({'master': spisok, 'problem':prob, 'prioritet':prior, 'client':cli, 'status':stat})


class GetSpecView(APIView):

    def post(self, request, *args, **kwargs):
        idfirma = request.data['idfirma']
        special = Spec.objects.filter(firma_id=idfirma)
        stat = []
        for mst in special:
            op = {}
            op['text'] = mst.type
            op['value'] = mst.id
            stat.append(op)

        return Response({'spec': stat})


# class GetSpecView(APIView):
#
#     def get(self, request):
#         special = Spec.objects.all()
#         stat = []
#         for mst in special:
#             op = {}
#             op['text'] = mst.type
#             op['value'] = mst.id
#             stat.append(op)
#
#         return Response({'spec': stat})




class AddReqView(APIView):

    def post(self, request, *args, **kwargs):
        ok = 1
        dat = request.data['date']
        client = request.data['client']
        master = request.data['master']
        theme = request.data['theme']
        problem = request.data['problem']
        prioritet = request.data['prioritet']
        desc = request.data['description']
        idfirma = request.data['idfirma']

        date = datetime.datetime.strptime(dat, "%Y-%m-%d").date()
        ok=1
        a= Request(tema=theme,firma_id = idfirma, problem_id=problem, master_id=master, prioritet_id=prioritet, client_id=client, description=desc, datetask=date, daterun=date, status_id=1)
        a.save()


        return Response({'ok': ok})


class FindreqView(APIView):

    def post(self, request, *args, **kwargs):
        ok = 1
        req = request.data['nomreq']
        idfirma=request.data['idfirma']
        rq = Request.objects.get(id=req, firma_id=idfirma)
        op = {}
        op['theme'] = rq.tema
        op['client'] = rq.client.company
        op['contact'] = rq.client.contactfio
        op['flat'] = rq.client.flat+' каб. '+rq.client.cabinet
        op['description']=rq.description

        op['master'] = rq.master.id
        op['prioritet'] = rq.prioritet.id
        op['status'] = rq.status.id
        if rq.daterun.month<10:
            month='0'+str(rq.daterun.month)
        else:
            month = str(rq.daterun.month)
        if rq.daterun.day < 10:
            day = '0' + str(rq.daterun.day)
        else:
            day = str(rq.daterun.day)
        op['daterun'] = str(rq.daterun.year)+'-'+month+'-'+day
        op['datetask'] = str(rq.daterun.day)+'-'+str(rq.daterun.month)+'-'+str(rq.daterun.year)

        return Response({'headers': op})


class EditreqView(APIView):

    def post(self, request, *args, **kwargs):
        ok = 1
        id = request.data['nomreq']
        idfirma = request.data['idfirma']
        daterun = request.data['daterun']
        date = datetime.datetime.strptime(daterun, "%Y-%m-%d").date()
        status = request.data['status']
        master = request.data['master']
        prioritet = request.data['prioritet']
        Request.objects.filter(id=id, firma_id=idfirma).update(daterun=date, status_id=status, master_id=master, prioritet_id=prioritet)

        return Response({'ok': 1})


class ReqView(APIView):


    def post(self, request, *args, **kwargs):
        ok=1
        idfirma = request.data['idfirma']
        filter =  request.data['filter']
        if filter == "":
            req = Request.objects.filter(firma_id=idfirma).order_by('-datetask')
        else:
            req = Request.objects.filter(firma_id=idfirma, status_id=filter).order_by('-datetask')
        ok = 1
        all_new = 0
        all_work = 0
        all_done = 0
        spisok = []
        i=1
        for rq in req:
            if rq.status.id == 1:
                all_new += 1
            if rq.status.id == 2:
                all_work += 1
            if rq.status.id == 3:
                all_done += 1
            op = {}
            op['number'] =i
            i+=1
            if rq.status.id == 1:
                status = rq.status.type
            if rq.status.id == 2:
                status = rq.status.type
            if rq.status.id == 3:
                status = rq.status.type

            op['datetask'] = rq.datetask.strftime('%d-%m-%Y')
            op['theme'] = rq.tema
            op['client'] = rq.client.company
            op['contact'] = rq.client.contactfio
            op['priority'] = rq.prioritet.type
            op['status'] = status
            op['id'] = rq.id
            spisok.append(op)



        return Response({'headers': spisok, 'all_new':all_new, 'all_work':all_work, 'all_done':all_done})

#------------ Employee ---------------------------------------------------------


class GetAllEmplyeesView(APIView):

    def post(self, request, *args, **kwargs):
        ok=1
        idfirma = request.data['idfirma']
        client = Master.objects.filter(firma_id=idfirma)
        spisok = []
        today=datetime.datetime.today()
        i=1
        for mst in client:
            op = {}
            op['number'] = i
            op['employee'] = mst.fio
            op['specialization'] = mst.spec.type
            op['telephone'] = mst.phone
            if mst.active == True:
                a = Request.objects.filter(daterun=today, master=mst,firma_id=idfirma)
                if len(a)>0:
                    status = a[0].status.id
                    if status <3:
                        op['emstatus'] = 'В работе'
                    else:
                        op['emstatus'] = 'Свободен'
                else:
                    op['emstatus'] = 'Свободен'
            else:
                op['emstatus'] = 'Уволен'
            op['role'] = 'Специалист'
            op['url'] = '/editemployees/'+str(mst.id)
            op['id'] = mst.id
            spisok.append(op)

        return Response({'headers': spisok})




class FindmployeeView(APIView):

    def post(self, request, *args, **kwargs):
        ok = 1
        id = request.data['nomreq']
        idfirma = request.data['idfirma']
        mst = Master.objects.get(id=id, firma_id=idfirma)
        op = {}
        op['fio'] = mst.fio
        op['phone'] = mst.phone
        op['adress'] = mst.adress
        op['desc'] = mst.description
        op['spec'] = mst.spec_id
        op['active'] = mst.active


        return Response({'headers': op})


class EditmployeeView(APIView):

    def post(self, request, *args, **kwargs):
        ok = 1
        id = request.data['nomreq']
        fio = request.data['fio']
        phone = request.data['phone']
        spec = request.data['spec']
        adress = request.data['adress']
        desc = request.data['desc']

        Master.objects.filter(id=id).update(fio=fio, phone=phone, spec_id=spec, adress=adress, description=desc)



        return Response({'ok': 1})


class AddmployeeView(APIView):

    def post(self, request, *args, **kwargs):
        ok = 1
        idfirma = request.data['idfirma']
        fio = request.data['fio']
        phone = request.data['phone']
        spec = request.data['spec']
        adress = request.data['adress']
        desc = request.data['desc']

        a =Master(firma_id=idfirma, fio=fio, phone=phone, spec_id=spec, adress=adress, description=desc)
        a.save()



        return Response({'ok': 1})


class DelemployeeView(APIView):

    def post(self, request, *args, **kwargs):
        ok = 1
        id = request.data['id']
        Master.objects.filter(id=id).update(active=0)


        return Response({'ok': 1})


#   ----------------   Company  ---------------------------------------


class GetAllFirmView(APIView):

    def post(self, request, *args, **kwargs):
        ok = 1
        idfirma = request.data['idfirma']
        client = Client.objects.filter(firma_id=idfirma)
        spisok = []
        i = 1
        for mst in client:
            op = {}
            op['number'] = i
            op['company'] = mst.company
            op['manager'] = mst.contactfio
            op['telephone'] = mst.phone
            op['floor'] = mst.flat
            op['office'] = mst.cabinet
            op['position'] =''
            op['url'] = '/editcompanies/' + str(mst.id)
            op['id'] = mst.id
            spisok.append(op)

        return Response({'headers': spisok})


class FindFirmView(APIView):

    def post(self, request, *args, **kwargs):
        ok = 1
        id = request.data['nomreq']
        idfirma = request.data['idfirma']
        mst = Client.objects.get(id=id, firma_id=idfirma)
        op = {}
        op['name'] = mst.company
        op['contact'] = mst.contactfio
        op['phone'] = mst.phone
        op['datein'] = mst.date_in
        op['flat'] = mst.flat
        op['office'] = mst.cabinet
        op['desc'] = mst.description


        return Response({'headers': op})


class EditFirmView(APIView):

    def post(self, request, *args, **kwargs):
        ok = 1
        id = request.data['nomreq']
        name = request.data['name']
        contact = request.data['contact']
        phone = request.data['phone']
        datein = request.data['datein']
        flat = request.data['flat']
        office = request.data['office']
        desc = request.data['desc']
        idfirma = request.data['idfirma']


        Client.objects.filter(id=id, firma_id=idfirma).update(company=name, phone=phone, contactfio=contact, date_in=datein, description=desc, flat = flat, cabinet=office)

        return Response({'ok': 1})

class AddFirmView(APIView):

    def post(self, request, *args, **kwargs):
        ok = 1

        name = request.data['name']
        contact = request.data['contact']
        phone = request.data['phone']
        datein = request.data['datein']
        flat = request.data['flat']
        office = request.data['office']
        desc = request.data['desc']
        idfirma = request.data['idfirma']


        a= Client(firma_id=idfirma, company=name, phone=phone, contactfio=contact, date_in=datein, description=desc, flat = flat, cabinet=office)
        a.save()



        return Response({'ok': 1})


class DelFirmView(APIView):

    def post(self, request, *args, **kwargs):
        ok = 1
        id = request.data['id']

        Client.objects.filter(id=id).update(active = 0)

        return Response({'ok': 1})


#   ----------     ANALITICA    ------------------------------------------------------------------


class AllStatchartView(APIView):

    def post(self, request, *args, **kwargs):

        # if request.user.is_authenticated  == False :
        #     return render(request, 'login.html')
        id = request.data['idfirma']
        req = Request.objects.filter(firma_id=id)
        all=0
        all_new = 0
        all_work = 0
        all_done = 0
        santehnika=0
        electrica=0
        teplo=0
        ohrana=0
        uborka=0
        for rq in req:
            all+=1
            if rq.status.id == 1:
                all_new += 1
            if rq.status.id == 2:
                all_work += 1
            if rq.status.id == 3:
                all_done += 1

        return Response({ 'all':all, 'all_new':all_new, 'all_work':all_work, 'all_done':all_done})


class RequestchartView(APIView):

    def post(self, request, *args, **kwargs):

        # if request.user.is_authenticated  == False :
        #     return render(request, 'login.html')
        id = request.data['idfirma']
        req = Request.objects.filter(firma_id=id)
        #req = Request.objects.all()
        all=0
        all_new = 0
        all_work = 0
        all_done = 0
        santehnika=0
        electrica=0
        teplo=0
        ohrana=0
        uborka=0
        for rq in req:
            all+=1
            if rq.status.id == 1:
                all_new += 1
            if rq.status.id == 2:
                all_work += 1
            if rq.status.id == 3:
                all_done += 1
            if rq.problem_id == 1:
                santehnika+=1
            if rq.problem_id == 2:
                electrica+=1
            if rq.problem_id == 4:
                teplo+=1
            if rq.problem_id == 5:
                ohrana+=1
            if rq.problem_id == 3:
                uborka+=1

        ok = 1
        req = Request.objects.filter(firma_id=id).order_by('datetask')
        count_month={}
        count_month_done = {}
        # for i in range(1, 7):
        #     count_month_done[i] = 0

        count_month_notdone = {}
        # for i in range(1, 7):
        #     count_month_notdone[i] = 0
        for rq in req:
            ok=1
            month=rq.datetask.month
            try:
                count_month[month]+=1
            except:
                count_month[month] = 1
                count_month_notdone[month] = 0
                count_month_done[month] = 0

            if rq.status.id == 1:
                try:
                    count_month_notdone[month] += 1
                except:
                    count_month_notdone[month] = 1
            if rq.status.id == 2:
                try:
                    count_month_notdone[month] += 1
                except:
                    count_month_notdone[month] = 1
            if rq.status.id == 3:
                try:
                    count_month_done[month] += 1
                except:
                    count_month_done[month] = 1

        ok=1
        activate('ru')
        #name_months=['Январь', '','','','','','','','','']
        name_months =[]
        now = datetime.date.today().replace(day=1)
        month=date(now, 'F')
        name_months.append(month)
        for i in range(1,7):
            ok=1
            now = now.replace(day=1) - datetime.timedelta(days=1)
            month = date(now, 'F')
            name_months.append(month)
        name_months.reverse()
        name_months_text='['
        for nm in name_months:
            name_months_text+="'"+nm+"',"
        name_months_text+=']'
        ok=1
        all_count=[]
        for key,item in count_month.items():
            ok=1
            all_count.append(item)
        all_count_done = []
        for key, item in count_month_done.items():
            ok = 1
            all_count_done.append(item)
        all_count_notdone = []
        for key, item in count_month_notdone.items():
            ok = 1
            all_count_notdone.append(item)

        ok=1

        return Response({'name_months': name_months, 'all_count':all_count,'all_count_done':all_count_done,'all_count_notdone':all_count_notdone})
        # return Response( {'name_months':name_months,'all_count':all_count,'all_count_done':all_count_done,'all_count_notdone':all_count_notdone,
        #                                              'all':all,'reqs': req, 'all_new':all_new, 'all_work':all_work, 'all_done':all_done,
        #                                              'santehnika': santehnika,'electrica':electrica,'teplo':teplo,'uborka':uborka,'ohrana':ohrana } )



class SpecchartView(APIView):

    def post(self, request, *args, **kwargs):

        # if request.user.is_authenticated  == False :
        #     return render(request, 'login.html')
        id = request.data['idfirma']
        req = Request.objects.filter(firma_id=id)

        all=0
        all_new = 0
        all_work = 0
        all_done = 0
        santehnika=0
        electrica=0
        teplo=0
        ohrana=0
        uborka=0
        for rq in req:
            if rq.problem_id == 1:
                santehnika+=1
            if rq.problem_id == 2:
                electrica+=1
            if rq.problem_id == 4:
                teplo+=1
            if rq.problem_id == 5:
                ohrana+=1
            if rq.problem_id == 3:
                uborka+=1

        data=[]
        data.append(santehnika)
        data.append(electrica)
        data.append(uborka)
        data.append(ohrana)
        data.append(teplo)

        return Response({'data': data})
        # return Response( {'name_months':name_months,'all_count':all_count,'all_count_done':all_count_done,'all_count_notdone':all_count_notdone,
        #                                              'all':all,'reqs': req, 'all_new':all_new, 'all_work':all_work, 'all_done':all_done,
        #                                              'santehnika': santehnika,'electrica':electrica,'teplo':teplo,'uborka':uborka,'ohrana':ohrana } )


#----------------------SPEC  ---------------------------

class EditSpecView(APIView):

    def post(self, request, *args, **kwargs):
        ok = 1
        id = request.data['idfirma']
        spec_s = request.data['spec']

        spec = Spec.objects.filter(firma_id=id)
        for sp in spec:
            ok=0
            try:
                for sp2 in spec_s:
                    if sp.id == sp2['value']:
                        ok=1
                        break
                if ok == 0:
                    #  Delete from base Spec
                    Spec.objects.filter(id=sp.id,firma_id=id).delete()
                    p=1
            except:
                #  Delete from base Spec
                Spec.objects.filter(id=sp.id,firma_id=id).delete()
                pass

        #  Add New Spec
        for sp2 in spec_s:
            try:
                s = sp2['value']
            except:
                #add new spec
                s = sp2
                a = Spec(type=s)
                a.save()
                pass

        return Response({'ok': 1})