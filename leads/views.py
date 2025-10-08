import logging
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from agents.mixins import OrganisorAndLoginRequiredMixin
from leads import models
from leads import forms
from django.utils import timezone

logger = logging.getLogger(__name__)


class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = forms.CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")

class LandingPageView(generic.TemplateView):
    template_name = "landing.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard")
        return super().dispatch(request, *args, **kwargs)


class DashboardView(OrganisorAndLoginRequiredMixin, generic.TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        organisation = user.userprofile  
        total_lead_count = models.Lead.objects.filter(organisation=organisation).count()

        thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
        total_in_past30 = models.Lead.objects.filter(
            organisation=organisation,
            date_added__gte=thirty_days_ago).count()
        

        converted_category, created = models.Category.objects.get_or_create(
            name="Converted",
            organisation=organisation  
        )

        converted_in_past30 = models.Lead.objects.filter(
            organisation=organisation,
            category=converted_category,
            converted_date__gte=thirty_days_ago).count()
        

        context.update({
            "total_lead_count": total_lead_count,
            "total_in_past30": total_in_past30,
            "converted_in_past30": converted_in_past30
        })

        return context

def landing_page(request):
    return render(request, "landing.html")


class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/lead_list.html"
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = models.Lead.objects.filter(
                organisation=user.userprofile, 
                agent__isnull=False
            )
        else:
            queryset = models.Lead.objects.filter(
                organisation=user.agent.organisation, 
                agent__isnull=False
            )
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            queryset = models.Lead.objects.filter(
                organisation=user.userprofile, 
                agent__isnull=True
            )
            context.update({
                "unassigned_leads": queryset
            })
        return context
class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/lead_detail.html"
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = models.Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = models.Lead.objects.filter(organisation=user.agent.organisation)
            queryset = queryset.filter(agent__user=user)
        return queryset

class LeadCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "leads/lead_create.html"
    form_class = forms.LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.organisation = self.request.user.userprofile
        lead.save()
        send_mail(
            subject="A lead has been created",
            message="Go to the site to see the new lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        messages.success(self.request, "You have successfully created a lead")
        return super(LeadCreateView, self).form_valid(form)


class LeadUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_update.html"
    form_class = forms.LeadModelForm

    def get_queryset(self):
        user = self.request.user
        return models.Lead.objects.filter(organisation=user.userprofile)

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        form.save()
        messages.info(self.request, "You have successfully updated this lead")
        return super(LeadUpdateView, self).form_valid(form)

class LeadDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "leads/lead_delete.html"
    def get_success_url(self):
        return reverse("leads:lead-list")
    def get_queryset(self):
        user = self.request.user
        return models.Lead.objects.filter(organisation=user.userprofile)

class AssignAgentView(OrganisorAndLoginRequiredMixin, generic.FormView):
    template_name = "leads/assign_agent.html"
    form_class = forms.AssignAgentForm
    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs
        
    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = models.Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)

class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/category_list.html"
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_organisor:
            queryset = models.Lead.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = models.Lead.objects.filter(
                organisation=user.agent.organisation
            )

        context.update({
            "unassigned_lead_count": queryset.filter(category__isnull=True).count()
        })
        return context

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = models.Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = models.Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset

class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/category_detail.html"
    context_object_name = "category"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = models.Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = models.Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset


class CategoryCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "leads/category_create.html"
    form_class = forms.CategoryModelForm

    def get_success_url(self):
        return reverse("leads:category-list")

    def form_valid(self, form):
        category = form.save(commit=False)
        category.organisation = self.request.user.userprofile
        category.save()
        return super(CategoryCreateView, self).form_valid(form)


class CategoryUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "leads/category_update.html"
    form_class = forms.CategoryModelForm

    def get_success_url(self):
        return reverse("leads:category-list")

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = models.Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = models.Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset

class CategoryDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "leads/category_delete.html"

    def get_success_url(self):
        return reverse("leads:category-list")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = models.Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = models.Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset


class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_category_update.html"
    form_class = forms.LeadCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = models.Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = models.Lead.objects.filter(organisation=user.agent.organisation)
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk": self.get_object().id})

    def form_valid(self, form):
        lead_before_update = self.get_object()
        instance = form.save(commit=False)
        
        converted_category = models.Category.objects.get(name="Converted")
        if form.cleaned_data["category"] == converted_category:
            if lead_before_update.category != converted_category:
                instance.converted_date = timezone.now()
        instance.save()
        return super(LeadCategoryUpdateView, self).form_valid(form)


class FollowUpCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "leads/followup_create.html"
    form_class = forms.FollowUpModelForm

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk": self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
        context = super(FollowUpCreateView, self).get_context_data(**kwargs)
        context.update({
            "lead": models.Lead.objects.get(pk=self.kwargs["pk"])
        })
        return context

    def form_valid(self, form):
        lead = models.Lead.objects.get(pk=self.kwargs["pk"])
        followup = form.save(commit=False)
        followup.lead = lead
        followup.save()
        return super(FollowUpCreateView, self).form_valid(form)

class FollowUpUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "leads/followup_update.html"
    form_class = forms.FollowUpModelForm

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = forms.FollowUp.objects.filter(lead__organisation=user.userprofile)
        else:
            queryset = forms.FollowUp.objects.filter(lead__organisation=user.agent.organisation)
            queryset = queryset.filter(lead__agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk": self.get_object().lead.id})


class FollowUpDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "leads/followup_delete.html"

    def get_success_url(self):
        
        followup = models.FollowUp.objects.get(id=self.kwargs["pk"])
        return reverse("leads:lead-detail", kwargs={"pk": followup.lead.pk})

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = models.FollowUp.objects.filter(lead__organisation=user.userprofile)
        else:
            queryset = models.FollowUp.objects.filter(lead__organisation=user.agent.organisation)
            queryset = queryset.filter(lead__agent__user=user)
        return queryset

