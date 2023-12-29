from django.urls import path,include
from zoom import views
from django.contrib.auth.views import LogoutView,LoginView
from zoom.views import index, adminclick_view, admin_dashboard_view, admin_404, updatedepartment, delete_department,update_leave_type,delete_leave_type,employee_type,update_employee,view_employee_details,profile_type,leave_request,approve_leave,reject_leave
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index , name='index'),
     # add these lines
    path('adminclick', views.adminclick_view),
    path('adminlogin', LoginView.as_view(template_name='admin/login.html'),name='adminlogin'),
    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin-dashboard', admin_dashboard_view, name='admin-dashboard'),
    path('admin/404', admin_404),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('adddepartment/',views.adddepartment, name='adddepartment'),
    path('managedepartment/',views.managedepartment, name='managedepartment'),
   path('updatedepartment/<int:department_id>/', updatedepartment, name='updatedepartment'),
   path('delete_department/<int:department_id>/', delete_department, name='delete_department'),
  path('add_leave_type/', views.add_leave_type, name='add_leave_type'),
  path('manage_leave_type/', views.manage_leave_type, name='manage_leave_type'),
    path('update_leave_type/<int:leave_type_id>/', update_leave_type, name='update_leave_type'),
     path('leave_type/delete/<int:leave_type_id>/', delete_leave_type, name='delete_leave_type'),
   path('employee_type/',views.employee_type, name='employee_type'),
    
    path('view_employee_type/', views.view_employee_type, name='view_employee_type'),
   path('update_employee/<int:employee_id>/', update_employee, name='update_employee'),
 path('view_employee_details/<int:employee_id>/', view_employee_details, name='view_employee_details'),
path('profile_type',views.profile_type,name='profile_type'),
path('add_leave/', views.add_leave, name='add_leave'),
path('leave_history/',views.leave_history, name='leave_history'),
 path('leave_request/', leave_request, name='leave_request'),
    path('approve_leave/<int:leave_id>/', approve_leave, name='approve_leave'),
    path('reject_leave/<int:leave_id>/', reject_leave, name='reject_leave'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
