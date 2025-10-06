from django.shortcuts import render
from rest_framework import generics
from .models import Lead,Agent
# Create your views here.

# class LeadsView(generics.ListAPIView):
#     template_name = 'leads/lead_list.html'
#     context_object_name = 'leads'

#     def get_queryset(self):
#         queryset = Lead.objects.all()

#         return queryset
def lead_list(request):
    leads = Lead.objects.all()
    context = {
        "leads":leads
    }
    return render(request,"leads/lead_list.html",context)