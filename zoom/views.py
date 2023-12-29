from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpResponseForbidden, HttpResponseRedirect, HttpResponseRedirect
from .forms import UserCreationForm, LoginForm
from django.contrib import messages
from .forms import SignupForm 
from .models import Department, LeaveType,Employee
from django.contrib.auth.models import User  # Add this import statement
from django import forms
from .models import Leave 
# Rest of your views.py code...

# Create your views here.

def adminclick_view(request):
    if request.user.is_authenticated:
        return redirect('admin-dashboard')
    return redirect('adminlogin')

def afterlogin_view(request):
        return redirect('admin-dashboard')
 
@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    return render(request,'admin/dashboard.html')
def admin_404(request):
    return HttpResponseNotFound('<h1>Page not found</h1>')
# signup page
def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            
            # Check if the entered email exists in the User model
            user_exists = User.objects.filter(email=email).exists()
            
            if not user_exists:
                # If the email doesn't exist, proceed with user registration
                user = User.objects.create_user(username=email, email=email, password=password)
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'This email already exists. Please use a different email.')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})
# login page
def index(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    login(request, user)
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Invalid email or password.')
            except User.DoesNotExist:
                messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()
    return render(request, 'index.html', {'form': form})


# logout page
def user_logout(request):
    logout(request)
    return redirect('index')
@login_required(login_url='/')
def dashboard(request):
    return render(request, 'dashboard.html')
@login_required(login_url='/')
def adddepartment(request):
    if request.method == 'POST':
        department_name = request.POST.get('departmentName')

        # Validate if department_name is not empty
        if department_name:
            Department.objects.create(department_name=department_name)
            messages.success(request, 'Department added successfully!')
            return redirect('adddepartment')  # Redirect to the same page after submission
        else:
            messages.error(request, 'Department name cannot be empty.')
    
    return render(request, 'admin/adddepartment.html')
@login_required(login_url='/')
def managedepartment(request):
    # Retrieve all departments from the database
    departments = Department.objects.all()

    # Pass the departments to the template context
    context = {'departments': departments}

    return render(request, 'admin/managedepartment.html', context)
@login_required(login_url='/')
def updatedepartment(request, department_id):
    # Retrieve the department object
    department = get_object_or_404(Department, id=department_id)

    if request.method == 'POST':
        # Update the department information based on the submitted form data
        department.department_name = request.POST.get('department_name')
        # Update other fields as needed

        # Save the changes
        department.save()

        # Redirect to the managedepartment view or any other desired page
        return redirect('managedepartment')

    # Pass the department to the template context
    context = {'department': department}

    return render(request, 'admin/updatedepartment.html', context)
def delete_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)

    if request.method == 'POST':
        department.delete()
        return redirect('managedepartment')

    return render(request, 'admin/managedepartment.html', {'department': department})
class LeaveTypeForm(forms.ModelForm):
    class Meta:
        model = LeaveType
        fields = ['name']

@login_required(login_url='/')
def add_leave_type(request):
    leave_types = LeaveType.objects.all()

    if request.method == 'POST':
        form = LeaveTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_leave_type')  # Redirect to a success page
    else:
        form = LeaveTypeForm()

    return render(request, 'admin/leave.html', {'leave_types': leave_types, 'form': form})
@login_required(login_url='/')
def manage_leave_type(request):
    leave_types = LeaveType.objects.all()
    return render(request, 'admin/manageleave.html',{'leave_types': leave_types})
@login_required(login_url='/')
def update_leave_type(request, leave_type_id):
    leave_type = get_object_or_404(LeaveType, pk=leave_type_id)

    if request.method == 'POST':
        name = request.POST.get('name')  # Adjust based on your model fields

        if name:
            leave_type.name = name
            leave_type.save()
            return redirect('manage_leave_type')  # Redirect to a success page

    return render(request, 'admin/updateleave.html', {'leave_type': leave_type})
@login_required(login_url='/')
def delete_leave_type(request, leave_type_id):
    leave_type = get_object_or_404(LeaveType, id=leave_type_id)

    if request.method == 'POST' and request.POST.get('method') == 'delete':
        leave_type.delete()
        return redirect('manage_leave_type')
    else:
        return HttpResponseNotAllowed(['POST'])

    return render(request, 'manageleave.html', {'leave_type': leave_type})

@login_required(login_url='/')
def employee_type(request):
    if request.method == 'POST':
        emp_id = request.POST.get('empId')
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        department_id = request.POST.get('department')
        mobile = request.POST.get('mobile')
        state = request.POST.get('state')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        country = request.POST.get('country')
        city = request.POST.get('city')
        joining_date = request.POST.get('joiningDate')
        address = request.POST.get('address')
        password = request.POST.get('password')  # Assuming you have a password field in your form

        # Handle the file upload separately if needed
        photo = request.FILES.get('photo', None)

        # Check if the entered email exists in the User model
        user_exists = User.objects.filter(email=email).exists()

        if not user_exists:
            try:
                department = Department.objects.get(id=department_id)
                employee_instance = Employee(
                    empId=emp_id,
                    firstName=first_name,
                    lastName=last_name,
                    department=department,
                    mobile=mobile,
                    state=state,
                    dob=dob,
                    email=email,
                    country=country,
                    city=city,
                    joiningDate=joining_date,
                    address=address,
                    photo=photo  # Handle this according to your model field
                )
                employee_instance.save()

                # Proceed with user registration
                user = User.objects.create_user(username=email, email=email, password=password)
                login(request, user)

                messages.success(request, 'Employee added successfully.')
                return redirect('employee_type')  # Redirect to the same page or another view
            except Department.DoesNotExist:
                messages.error(request, 'Department does not exist.')
                # Handle the error as needed
        else:
            messages.error(request, 'This email already exists. Please use a different email.')

    # Handle GET request or form validation errors
    departments = Department.objects.all()
    return render(request, 'admin/employee.html', {'departments': departments})

@login_required(login_url='/')
def view_employee_type(request):
    employees = Employee.objects.all()
    return render(request, 'admin/viewemployee.html', {'employees': employees})
@login_required(login_url='/')
def update_employee(request, employee_id):
    # Retrieve the employee object based on the employee_id
    employee = get_object_or_404(Employee, id=employee_id)

    if request.method == 'POST':
        # If the form is submitted, process the form data
        employee.empId = request.POST.get('empId')
        employee.firstName = request.POST.get('firstName')
        employee.lastName = request.POST.get('lastName')
        employee.department_id = request.POST.get('department')
        employee.mobile = request.POST.get('mobile')
        employee.state = request.POST.get('state')
        employee.dob = request.POST.get('dob')
        employee.email = request.POST.get('email')
        employee.country = request.POST.get('country')
        employee.city = request.POST.get('city')
        employee.joiningDate = request.POST.get('joiningDate')
        employee.address = request.POST.get('address')

        # Handle the file upload separately if needed
        photo = request.FILES.get('photo', None)
        if photo:
            employee.photo = photo

        try:
            department_id = request.POST.get('department')
            department = Department.objects.get(id=department_id)
            employee.department = department

            employee.save()

            messages.success(request, 'Employee updated successfully.')
            return redirect('view_employee_type')  # Redirect to the employee list or another view
        except Department.DoesNotExist:
            messages.error(request, 'Department does not exist.')
            # Handle the error as needed

    # Handle GET request or form validation errors
    departments = Department.objects.all()
    return render(request, 'admin/updateemployee.html', {'employee': employee, 'departments': departments})
@login_required(login_url='/')
def view_employee_details(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    return render(request, 'admin/viewemployeedetails.html', {'employee': employee})


@login_required(login_url='/')
def profile_type(request):
    try:
        employee = Employee.objects.get(email=request.user.email)
        context = {
            'employee': employee,
        }
        return render(request, 'profile.html', context)
    except Employee.DoesNotExist:
        # Handle the case where the Employee record does not exist
        # This might happen if the user is not properly associated with an Employee
        return render(request, 'profile.html', {})

@login_required(login_url='/')
def add_leave(request):
    if request.method == 'POST':
        leave_type = request.POST.get('leave_type')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        description = request.POST.get('description')

        # Create a new Leave object and associate it with the logged-in employee
        leave = Leave(leave_type=leave_type, start_date=start_date, end_date=end_date, description=description, employee=request.user)
        leave.save()

        messages.success(request, 'Leave added successfully!')
        return redirect('leave_history')  # Redirect to the leave history page

    return render(request, 'addleave.html')

@login_required(login_url='/')
def leave_history(request):
    # Retrieve leave history for the logged-in employee
    leave_history = Leave.objects.filter(employee=request.user)

    return render(request, 'leavehistory.html', {'leave_history': leave_history})
@login_required(login_url='/')
def leave_request(request):
    # Retrieve all leaves added by any employee
    all_leaves = Leave.objects.all()

    return render(request, 'admin/leaverequest.html', {'all_leaves': all_leaves})

@login_required(login_url='/')
def approve_leave(request, leave_id):
    leave = Leave.objects.get(pk=leave_id)
    leave.status = 'approved'
    leave.save()
    messages.success(request, f'Leave request for {leave.employee.username} has been approved.')
    return redirect('leave_request')

@login_required(login_url='/')
def reject_leave(request, leave_id):
    leave = Leave.objects.get(pk=leave_id)
    leave.status = 'rejected'
    leave.save()
    messages.success(request, f'Leave request for {leave.employee.username} has been rejected.')
    return redirect('leave_request')