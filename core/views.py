from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.models import User
from core.forms import UserForm

#  --------------------------HOME-----------------------------#


class dashboard(LoginRequiredMixin, TemplateView):

    template_name = 'dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

#  ---------------------------LOGIN---------------------------#


class Login(LoginView):
    template_name = 'login/views/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)


#  ---------------------------USER MODEL---------------------------#
# ------------------------VIEWS------------------------------#

class ListUser(LoginRequiredMixin, ListView):

    model = User
    template_name = 'users/views/ListUser.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        create_forms = {
            'form1': {'button_create': reverse_lazy('CreateUser'),
                      'text': 'Crear Nuevo Usuario'},
        }
        context['create_forms'] = create_forms
        return context


# ------------------------FUNCTIONS------------------------------#

class CreateUser(LoginRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'users/functions/CreateUser.html'
    success_url = reverse_lazy('ListUser')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'create'
        context['success_url'] = self.success_url
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'create':
                form = self.get_form()
                data = form.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

# ------------------------FUNCTIONS------------------------------#


class EditUser(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'users/functions/CreateUser.html'
    success_url = reverse_lazy('ListUser')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'edit'
        context['success_url'] = self.success_url
        return context

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)


class DeleteUser(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'users/functions/DeleteUser.html'
    success_url = reverse_lazy('ListUser')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
