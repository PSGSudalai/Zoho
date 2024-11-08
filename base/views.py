
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,  logout ,login as auth_login
from django.utils import timezone
from base.models import Lead ,Status
from django.utils.dateparse import parse_datetime
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Count

# Register
def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check for existing username, email, and password
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
        elif User.objects.filter(password=password).exists():
            messages.error(request, "Password already exists")
        else:
            # Create a new user and save
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=name  
            )
            user.save()
            login (request,user)
            messages.success(request, 'Registration successfully')
            return redirect('home')

    return render(request, 'register.html')

# Login

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)  # Ensure `username` is used if the default User model is used or modify if custom
        print(user)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Login Successful')
            return redirect('home')  
        else:
            messages.error(request, 'Invalid username or Password')
            return redirect('login')

    return render(request, 'index.html')

# logout
def logout(request):
    logout(request)
    return redirect('index')

#dashboard
def dashboard(request,lead_id=None):
    current_month = datetime.now().month
    current_year = datetime.now().year
    current_week = datetime.now().isocalendar()[1]

# Filter leads created in the current month and year
    monthly_lead = Lead.objects.filter(   #monthly lead for monhtly count
        created_at__month=current_month,
        created_at__year=current_year
    ).count()
    weekly_follow_up = Lead.objects.filter(follow_up__week=current_week)   # weekly follow up list
    total_lead = Lead.objects.all().count()   # Total lead count
    status_count = Lead.objects.filter(status__identity="Success").count()  #Status count
    leading = Lead.objects.all()[:5]   #Lead Data List
    lead_count = Lead.objects.all().count()   #Lead Data count
    leadweek = Lead.objects.filter(follow_up__week=current_week)

    follow_up = Lead.objects.filter(follow_up__year=current_year).count()
    lead = None
    if lead_id:
        lead = get_object_or_404(Lead, id=lead_id)  

    
    

# Weekly graph 
# Get the current month's lead count
    current_lead_count = Lead.objects.filter(
        created_at__week=current_week
    ).count()

    # Get the success status count for the current month
    success_count = Lead.objects.filter(
    created_at__week=current_week,
    status__identity='Success'  
    ).count()

    # Get previous month's data with correct referencing for ForeignKey
      

    
    # Prepare data arrays for JavaScript
    leadchart = [0,0,current_lead_count,0]
    leadStatus = [0,0,success_count, 0]

    #gender lead graph
    lead_male = Lead.objects.filter(gender='Male', created_at__week=current_week).count()
    lead_female = Lead.objects.filter(gender='Female', created_at__week=current_week).count()

    lead_gender_male = [0,0,lead_male,0]
    lead_gender_female = [0,0,lead_female,0]


#lead source
    source_social = Lead.objects.filter(source='Social media',created_at__year=current_year).count()
    source_job = Lead.objects.filter(source='Job portal',created_at__year=current_year).count()
    source_referral = Lead.objects.filter(source='Referral',created_at__year=current_year).count()



   

    content = {
        'total_lead': total_lead,
        'status_count': status_count,
        'monthly_lead': monthly_lead,
        'lead': lead,
        'leading': leading,
        'leadweek':leadweek,
        'leadStatus':leadStatus,
        'leadchart':leadchart,
        'weekly_follow_up':weekly_follow_up,
        'lead_count':lead_count,
        'lead_gender_female':lead_gender_female,
        'lead_gender_male':lead_gender_male,
        'source_referral':source_referral,
        'source_job':source_job,
        'source_social':source_social,
    }
    
    return render(request, 'dashboard.html', content)



#lead Table
def all_lead(request, lead_id=None):
    leads = Lead.objects.all().order_by("-created_at") 
    lead = None
    if lead_id:
        lead = get_object_or_404(Lead, id=lead_id)  # Safely get the lead or return a 404 if not found
    
    context = {
        'lead': lead,
        'leads': leads,  # Pass all leads to the template
    }
    
    return render(request, 'lead.html', context)







from django.shortcuts import redirect
from django.contrib import messages

def add_status(request):
    statuses = Status.objects.all()
    if request.method == 'POST':
        status_name = request.POST.get('identity', '').strip()
        if status_name:
            if not Status.objects.filter(identity=status_name).exists():
                new_status = Status(identity=status_name)
                new_status.save()
                messages.success(request, "Status added successfully.")
            else:
                messages.warning(request, "Status with this identity already exists.")
        else:
            messages.error(request, "Status name cannot be empty.")
        return redirect(request.META.get('HTTP_REFERER', 'default-page-url'))
    return render(request, 'add-lead.html', {'statuses': statuses})



#add Lead
# def add_lead(request):
#     statuses = Status.objects.all()
#     if request.method == 'POST':
#         # Collect data from the form
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         address = request.POST.get('address')
#         city = request.POST.get('city')
#         gender = request.POST.get('gender')
#         passout = request.POST.get('passout')
#         college = request.POST.get('college_name')
#         tech = request.POST.get('tech_field')
#         source = request.POST.get('source')
#         status_id = request.POST.get('status') 
#         is_lead = False 
#         status = Status.objects.get(id=status_id)  
#         if status.identity == 'Active': 
#             is_lead = True
        
#         follow_up = request.POST.get('follow_up') or None
        
#         # Create the new Lead object
#         Lead.objects.create(
#             name=name,
#             email=email,
#             phone=phone,
#             address=address,
#             city=city,
#             gender=gender,
#             passout=passout,
#             tech_field=tech,
#             source=source,
#             college_name=college,
#             status=status,  
#             is_lead=is_lead,  
#             follow_up=follow_up, 
#         )

#         messages.success(request, 'New lead added successfully.')
#         return redirect('lead')
    
#     return render(request, 'add-lead.html', {'statuses': statuses})


def add_lead(request):
    statuses = Status.objects.all()

    if request.method == 'POST':
        # Collect data from the form
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        gender = request.POST.get('gender')
        passout = request.POST.get('passout')
        college = request.POST.get('college_name')
        tech = request.POST.get('tech_field')
        source = request.POST.get('source')  # Get the selected source
        status_id = request.POST.get('status')
        follow_up = request.POST.get('follow_up') or None

        # Ensure all required fields are provided
        if not name or not email or not phone or not city or not gender or not source or not status_id:
            messages.error(request, 'Please fill in all required fields.')
            
        is_lead = False

        # Fetch the status based on the provided status_id
        try:
            status = Status.objects.get(id=status_id)
        except Status.DoesNotExist:
            status = None
            messages.error(request, 'Invalid status selected.')
            return redirect('add_status')

        # If the status is 'Active', mark as lead
        if status and status.identity == 'Active':
            is_lead = True

        # Create the new Lead object
        try:
            Lead.objects.create(
                name=name,
                email=email,
                phone=phone,
                address=address,
                city=city,
                gender=gender,
                passout=passout,
                tech_field=tech,
                source=source,
                college_name=college,
                status=status,
                is_lead=is_lead,
                follow_up=follow_up,
            )
            messages.success(request, 'New lead added successfully.')
        except Exception as e:
            messages.error(request, f'Error adding lead: {str(e)}')

        return redirect('lead')  # Replace with your appropriate redirect URL or view name

    return render(request, 'add-lead.html', {'statuses': statuses})

#delete lead
def delete_lead(request,pk):
    del_lead = Lead.objects.get(id=pk)
    del_lead.delete()
    messages.success(request,"Deleted Successfully")
    return redirect('lead')



#edit lead
def edit_lead(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    statuses = Status.objects.all()

    if request.method == 'POST':
        # Update the lead instance with form data
        lead.name = request.POST.get('name')
        lead.email = request.POST.get('email')
        lead.phone = request.POST.get('phone')
        lead.address = request.POST.get('address')
        lead.city = request.POST.get('city')
        lead.gender = request.POST.get('gender')
        lead.passout = request.POST.get('passout')
        lead.college_name = request.POST.get('college_name')
        lead.source = request.POST.get('source')
        lead.tech_field = request.POST.get('tech_field')
        lead.follow_up = request.POST.get('follow_up')

        # Get the status as a ForeignKey object
        status_id = request.POST.get('status')
        if status_id:
            lead.status = Status.objects.get(id=status_id)

        lead.is_lead = 'is_lead' in request.POST

        lead.save()
        messages.success(request, 'Lead updated successfully.')
        return redirect('lead')  # Replace 'lead' with the appropriate name of your leads list page

    context = {
        'lead': lead,
        'statuses': statuses,
    }

    return render(request, 'edit.html', context)

