from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView, ListView

from .forms import StaffRegisterForm, StaffUpdateForm
from .models import Staff


# Представление для просмотра всех сотрудников
class StaffListView(PermissionRequiredMixin, ListView):
    model = Staff
    ordering = '-last_name'
    template_name = 'staff/staff_list.html'
    context_object_name = 'staff'
    permission_required = ('staff.view_staff',)
    raise_exception = True
    paginate_by = 10

    def get_queryset(self):
        return Staff.objects.filter(is_active=True).order_by(self.ordering)


# Представление для просмотра всех уволенных сотрудников
class FiredListView(PermissionRequiredMixin, ListView):
    model = Staff
    ordering = '-last_name'
    template_name = 'staff/fired_list.html'
    context_object_name = 'fired'
    permission_required = ('staff.view_staff',)
    raise_exception = True
    paginate_by = 10

    def get_queryset(self):
        return Staff.objects.filter(is_active=False).order_by(self.ordering)


# Представление для регистрации работника
class StaffRegisterView(PermissionRequiredMixin, CreateView):
    model = Staff
    form_class = StaffRegisterForm
    template_name = 'staff/signup.html'
    permission_required = ('staff.add_staff',)
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = StaffRegisterForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.is_staff = True
            user.save()
            staff_group = Group.objects.get(name='staff')
            staff_group.user_set.add(user)
            return redirect('staff_list')
        else:
            return render(request, self.template_name, {'form': form})


class StaffUpdateView(PermissionRequiredMixin, UpdateView):
    model = Staff
    form_class = StaffUpdateForm
    template_name = 'staff/update.html'
    success_url = reverse_lazy('staff_list')
    permission_required = ('staff.change_staff',)
    raise_exception = True

    def get_permission_required(self):
        self.object = self.get_object()
        if not (
                self.request.user.email == self.object.email or
                self.request.user.is_superuser
        ):
            content = f'''
                <p style="font-size: 2em; font-weight: bold; font-family: Times New Roman;">403 Forbidden</p>
            '''
            return HttpResponse(content=content)
        if self.permission_required is None:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} is missing the "
                f"permission_required attribute. Define "
                f"{self.__class__.__name__}.permission_required, or override "
                f"{self.__class__.__name__}.get_permission_required()."
            )
        if isinstance(self.permission_required, str):
            perms = (self.permission_required,)
        else:
            perms = self.permission_required
        return perms


class StaffAccountView(PermissionRequiredMixin, TemplateView):
    template_name = 'staff/account.html'
    permission_required = ('staff.change_staff',)
    raise_exception = True

    def get_permission_required(self):
        if not (self.request.user.is_staff or self.request.user.is_superuser):
            content = f'''
                <p style="font-size: 2em; font-weight: bold; font-family: Times New Roman;">403 Forbidden</p>
            '''
            return HttpResponse(content=content)
        if self.permission_required is None:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} is missing the "
                f"permission_required attribute. Define "
                f"{self.__class__.__name__}.permission_required, or override "
                f"{self.__class__.__name__}.get_permission_required()."
            )
        if isinstance(self.permission_required, str):
            perms = (self.permission_required,)
        else:
            perms = self.permission_required
        return perms


class ManagementView(PermissionRequiredMixin, TemplateView):
    template_name = 'staff/management.html'
    permission_required = ('staff.change_staff', 'orders.view_order',)
    raise_exception = True

    def get_permission_required(self):
        if not (
                'management' in self.request.user.groups.all().values_list('name', flat=True) or
                self.request.user.is_superuser
        ):
            content = f'''
                <p style="font-size: 2em; font-weight: bold; font-family: Times New Roman;">403 Forbidden</p>
            '''
            return HttpResponse(content=content)
        if self.permission_required is None:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} is missing the "
                f"permission_required attribute. Define "
                f"{self.__class__.__name__}.permission_required, or override "
                f"{self.__class__.__name__}.get_permission_required()."
            )
        if isinstance(self.permission_required, str):
            perms = (self.permission_required,)
        else:
            perms = self.permission_required
        return perms


# Представление, делающее сотрудника активным
@permission_required('staff.change_staff', raise_exception=True)
def staff_restore_view(request, pk):
    # получаем сотрудника
    person = Staff.objects.get(id=pk)
    if not (
            'management' in request.user.groups.all().values_list('name', flat=True) or
            request.user.is_superuser
    ):
        content = f'''
            <p style="font-size: 2em; font-weight: bold; font-family: Times New Roman;">403 Forbidden</p>
        '''
        return HttpResponse(content=content)
    # меняем активность
    person.make_active()

    return redirect('fired_list')


# Представление, делающее сотрудника неактивным
@permission_required('staff.change_staff', raise_exception=True)
def staff_remove_view(request, pk):
    # получаем сотрудника
    person = Staff.objects.get(id=pk)
    if not (
            'management' in request.user.groups.all().values_list('name', flat=True) or
            request.user.is_superuser
    ):
        content = f'''
            <p style="font-size: 2em; font-weight: bold; font-family: Times New Roman;">403 Forbidden</p>
        '''
        return HttpResponse(content=content)
    # меняем активность
    person.make_inactive()

    return redirect('staff_list')
