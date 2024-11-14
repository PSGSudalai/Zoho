
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,  logout ,login as auth_login
from django.utils import timezone
from base.models import Lead ,Status ,Assign
from django.db.models import Q
from django.utils import timezone
from datetime import date, datetime, timedelta
from django.db.models import Count
from django.utils.dateparse import parse_date
from django.db.models.functions import ExtractWeek, ExtractDay

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
    current_date = date.today()

    lead_overall_count = Lead.objects.count()
    user = Assign.objects.all().count()

    # Retrieve and parse date filters from GET request
   # Initial overall counts without any filters
   


    total_lead = Lead.objects.all().count()
    status_lead=Lead.objects.all().count()
    previous_status_lead=Lead.objects.all().count()
    # user =Lead.objects.filter(assign_to__assigned_to).count()
    lead_success_count = Lead.objects.filter(status__identity="Success").count()
    lead_pending_count = Lead.objects.filter(status__identity="Pending").count()
    lead_negotiation_count = Lead.objects.filter(status__identity="Negotiation").count()
    lead_follow_up_count = Lead.objects.filter(status__identity="Follow Up").count()
    lead_closed_count = Lead.objects.filter(status__identity="Closed").count()
    lead_whatsapp_count = Lead.objects.filter(source='Whatsapp').count()
    lead_referral_count = Lead.objects.filter(source='Referral').count()
    lead_job_count = Lead.objects.filter(source='Job portal').count()
    lead_social_count = Lead.objects.filter(source='Social media').count()
    

    # Retrieve and parse date filters from GET request
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    filter_type = request.GET.get('filter_type')
    # filter_month = request.GET.get('filter_month')
    # filter_year = request.GET.get('filter_year')

    if start_date:
        start_date = parse_date(start_date)
    if end_date:
        end_date = parse_date(end_date)

    # Create a QuerySet to filter by date range
    lead_filtered_queryset = Lead.objects.all()

    if start_date and end_date:
        lead_filtered_queryset = lead_filtered_queryset.filter(created_at__range=[start_date, end_date])
    elif start_date:
        lead_filtered_queryset = lead_filtered_queryset.filter(created_at__gte=start_date)
    elif end_date:
        lead_filtered_queryset = lead_filtered_queryset.filter(created_at__lte=end_date)

        

    # If date filters are applied, update the counts accordingly
    if start_date or end_date:
        total_lead=lead_filtered_queryset.all().count()
        previous_total_lead = lead_filtered_queryset.filter(created_at__lt=start_date).count()  # Adjust filter as needed

# Determine if the lead count has increased or decreased
        lead_trend = 'up' if total_lead > previous_total_lead else 'down'
        lead_success_count = lead_filtered_queryset.filter(status__identity="Success").count()
        lead_pending_count = lead_filtered_queryset.filter(status__identity="Pending").count()
        lead_negotiation_count = lead_filtered_queryset.filter(status__identity="Negotiation").count()
        lead_follow_up_count = lead_filtered_queryset.filter(status__identity="Follow Up").count()
        lead_closed_count = lead_filtered_queryset.filter(status__identity="Closed").count()
        lead_whatsapp_count = lead_filtered_queryset.filter(source='Whatsapp').count()
        lead_referral_count = lead_filtered_queryset.filter(source='Referral').count()
        lead_job_count = lead_filtered_queryset.filter(source='Job portal').count()
        lead_social_count = lead_filtered_queryset.filter(source='Social media').count()
    elif filter_type=="year":
        #year source count
        total_lead=Lead.objects.filter(created_at__year=current_year).count()
        lead_social_count = Lead.objects.filter(source='Social media',created_at__year=current_year).count()
        lead_job_count = Lead.objects.filter(source='Job portal',created_at__year=current_year).count()
        lead_referral_count = Lead.objects.filter(source='Referral',created_at__year=current_year).count()
        lead_whatsapp_count = Lead.objects.filter(source='Whatsapp',created_at__year=current_year).count()

        
        #Yearly Status count
        lead_success_count = Lead.objects.filter(status__identity="Success",created_at__year=current_year).count()  #Status count
        lead_closed_count =Lead.objects.filter(status__identity="Closed",created_at__year=current_year).count()
        lead_negotiation_count =Lead.objects.filter(status__identity="Negotation",created_at__year=current_year).count()
        lead_follow_up_count =Lead.objects.filter(status__identity="Follow Up",created_at__year=current_year).count()
        lead_pending_count =Lead.objects.filter(status__identity="Pending",created_at__year=current_year).count()

    elif filter_type=="month":
        #month source count
        total_lead=Lead.objects.filter(created_at__month=current_month).count()
        lead_social_count = Lead.objects.filter(source='Social media',created_at__month=current_month).count()
        lead_job_count = Lead.objects.filter(source='Job portal',created_at__month=current_month).count()
        lead_referral_count = Lead.objects.filter(source='Referral',created_at__month=current_month).count()
        lead_whatsapp_count = Lead.objects.filter(source='Whatsapp',created_at__month=current_month).count()
        
        #month Status Count
        lead_success_count = Lead.objects.filter(status__identity="Success",created_at__month=current_month).count()  #Status count
        lead_closed_count =Lead.objects.filter(status__identity="Closed",created_at__month=current_month).count()
        lead_negotiation_count =Lead.objects.filter(status__identity="Negotation",created_at__month=current_month).count()
        lead_follow_up_count =Lead.objects.filter(status__identity="Follow Up",created_at__month=current_month).count()
        lead_pending_count =Lead.objects.filter(status__identity="Pending",created_at__month=current_month).count()

    elif filter_type=="week":
        #week source count
        total_lead=Lead.objects.filter(created_at__week=current_week).count()
        lead_social_count = Lead.objects.filter(source='Social media',created_at__week=current_week).count()
        lead_job_count = Lead.objects.filter(source='Job portal',created_at__week=current_week).count()
        lead_referral_count = Lead.objects.filter(source='Referral',created_at__week=current_week).count()
        lead_whatsapp_count = Lead.objects.filter(source='Whatsapp',created_at__week=current_week).count()
        #Weekly Status Count
        lead_success_count = Lead.objects.filter(status__identity="Success",created_at__week=current_week).count()  #Status count
        lead_closed_count =Lead.objects.filter(status__identity="Closed",created_at__week=current_week).count()
        lead_negotiation_count =Lead.objects.filter(status__identity="Negotation",created_at__week=current_week).count()
        lead_follow_up_count =Lead.objects.filter(status__identity="Follow Up",created_at__week=current_week).count()
        lead_pending_count =Lead.objects.filter(status__identity="Pending",created_at__week=current_week).count()



            
        

# Return or pass these counts as needed


    

# Filter leads created in the current month and year
    monthly_lead = Lead.objects.filter(   #monthly lead for monhtly count
        created_at__month=current_month,
        created_at__year=current_year
    ).count()
    if request.user.is_superuser:
        weekly_follow_up = Lead.objects.filter(follow_up__week=current_week)
    else:
        weekly_follow_up = Lead.objects.filter(follow_up__week=current_week, user=request.user)
        
    
    if request.user.is_superuser:
        leading = Lead.objects.all().order_by("-created_at")[:5]
    else:
        leading = Lead.objects.filter(user=request.user).order_by("-created_at")[:5]
    lead_count = Lead.objects.all().count()   #Lead Data count
    leadweek = Lead.objects.filter(follow_up__week=current_week)

   

    lead = None
    if lead_id:
        lead = get_object_or_404(Lead, id=lead_id)  

    leadchart = [0, 0, 0, 0]
    leadStatus = [0, 0, 0, 0]

    # Get the week number for the first day of the month
    first_day_of_month = date(current_year, current_month, 1)
    first_week_number = first_day_of_month.isocalendar()[1]  # Extract the week number directly

    # Get the total number of leads per week
    weekly_lead_counts = Lead.objects.filter(
        created_at__month=current_month,
        created_at__year=current_year
    ).annotate(
        week=ExtractWeek('created_at')
    ).values(
        'week'
    ).annotate(
        count=Count('id')
    ).order_by('week')

    # Populate leadchart array for the corresponding week
    for entry in weekly_lead_counts:
        week_index = entry['week'] - first_week_number  # Calculate week index based on the first week of the month
        if 0 <= week_index < 4:  # Ensure the week falls within the 4-week range of the month
            leadchart[week_index] = entry['count']

    # Get the number of successful leads per week
    weekly_success_counts = Lead.objects.filter(
        status__identity="Success",
        created_at__month=current_month,
        created_at__year=current_year
    ).annotate(
        week=ExtractWeek('created_at')
    ).values(
        'week'
    ).annotate(
        count=Count('id')
    ).order_by('week')

    # Populate leadStatus array for the corresponding week
    for entry in weekly_success_counts:
        week_index = entry['week'] - first_week_number  # Align with the first week of the month
        if 0 <= week_index < 4:  # Ensure within the 4-week range
            leadStatus[week_index] = entry['count']


    #gender lead graph
    lead_male = Lead.objects.filter(gender='Male', created_at__week=current_week).count()
    lead_female = Lead.objects.filter(gender='Female', created_at__week=current_week).count()

    lead_gender_male = [0,0,lead_male,0]
    lead_gender_female = [0,0,lead_female,0]
    user_has_permission = request.user.is_superuser or request.user in [lead.user for lead in leading]
    
    content = {
        'user_has_permission': user_has_permission,
        
        # 'today_date': today_date,
        'status_lead':status_lead,
        'user':user,
        'lead_count': lead_count,
        'lead_overall_count': lead_overall_count,
        'lead_success_count': lead_success_count,
        'lead_pending_count': lead_pending_count,
        'lead_negotiation_count': lead_negotiation_count,
        'lead_follow_up_count': lead_follow_up_count,
        'lead_closed_count': lead_closed_count,
        'lead_whatsapp_count': lead_whatsapp_count,
        'lead_referral_count': lead_referral_count,
        'lead_job_count': lead_job_count,
        'lead_social_count': lead_social_count,
        'total_lead': total_lead,
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
        


    }
    
    return render(request, 'dashboard.html', content)



#lead Table
def all_lead(request, lead_id=None):

    current_month = datetime.now().month
    current_year = datetime.now().year
    current_week = datetime.now().isocalendar()[1]
    # Get all leads and order them by creation date
    if request.user.is_superuser:
        leads = Lead.objects.all().order_by("-created_at")
    else:
        leads = Lead.objects.filter(user=request.user).order_by("-created_at")
    
    
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    filter_type=request.GET.get('filter_type')
    city = request.GET.get('city')
    source = request.GET.get('source')
    tech = request.GET.get('tech_field')
    gender = request.GET.get('gender')


    if start_date:
        start_date = parse_date(start_date)
    if end_date:
        end_date = parse_date(end_date)

    if start_date and end_date:
        leads = Lead.objects.filter(created_at__range=[start_date, end_date])
    elif start_date:
        leads = Lead.objects.filter(created_at__gte=start_date)
    elif end_date:
        leads = Lead.objects.filter(created_at__lte=end_date)
    elif filter_type=="week":
        leads = Lead.objects.filter(created_at__week=current_week)
    elif filter_type=="month":
        leads = Lead.objects.filter(created_at__month=current_month)
    elif filter_type=="year":
        leads = Lead.objects.filter(created_at__year=current_year)
    
    
    elif city:
        leads = Lead.objects.filter(city=city)
    
    elif source:
        leads = Lead.objects.filter(source=source)
    
    # Apply tech field filter if provided
    elif tech:
        leads = Lead.objects.filter(tech_field=tech)

    elif gender:
        leads = Lead.objects.filter(gender=gender)

    lead = None
    if lead_id:
        lead = get_object_or_404(Lead, id=lead_id)

    context = {
        'lead': lead,
        'leads': leads,  # Pass filtered or all leads to the template
    }
    
    return render(request, 'lead.html', context)








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

def add_assign(request):
    assign = Assign.objects.all()
    
    if request.method == 'POST':
        # Get the value from the POST data and trim whitespace
        assign_to = request.POST.get('assign_to', '').strip()
        
        if assign_to:
            if not Assign.objects.filter(assigned_to=assign_to).exists():
                new_assign = Assign(assigned_to=assign_to)
                new_assign.save()
                messages.success(request, "Assignment added successfully.")
            else:
                messages.warning(request, "An assignment with this user already exists.")
        else:
            messages.error(request, "Assignment name cannot be empty.")
        
        return redirect(request.META.get('HTTP_REFERER', 'default-page-url'))
    
    return render(request, 'add-lead.html', {'assign': assign})




#add Lead


def add_lead(request):
    statuses = Status.objects.all()
    assigns = Assign.objects.all()
    users =User.objects.all()
    

    if request.method == 'POST':
        # Collect data from the form
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        gender = request.POST.get('gender')
        passout = request.POST.get('passout')
        college = request.POST.get('college_name')
        tech = request.POST.get('tech_field')
        source = request.POST.get('source')
        status_id = request.POST.get('status')
        assign_id = request.POST.get('assign_to')
        user_id = request.POST.get('user')
        is_lead = False

        try:
            status = Status.objects.get(id=status_id)
        except (Status.DoesNotExist, ValueError):
            status = None

        if status and status.identity == 'Active':
            is_lead = True

        try:
            assign = Assign.objects.get(id=assign_id)
        except (Assign.DoesNotExist, ValueError):
            assign = None
        try:
            user = User.objects.get(id=user_id)
        except (User.DoesNotExist, ValueError):
            user = None

        follow_up = request.POST.get('follow_up') or None
        email = request.POST.get('email') or None

        # Check if a lead with the same phone number already exists
        if Lead.objects.filter(phone=phone).exists():
            phone_error = 'A lead with this phone number already exists.'
            return render(request, 'add-lead.html', {
                'statuses': statuses,
                'assigns': assigns,
                'users':users,
                'phone_error': phone_error
            })

        # Create the new Lead object if validation passes
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
            assign_to=assign,
            user=user,
        )

        messages.success(request, 'New lead added successfully.')
        return redirect('lead')

    return render(request, 'add-lead.html', {'statuses': statuses, 'assigns': assigns,'users':users})





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
    assigns = Assign.objects.all()

    if request.method == 'POST':
        # Update lead instance with form data
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

        # Allow empty follow-up date
        lead.follow_up = request.POST.get('follow_up') or None
        lead.email = request.POST.get('email') or None
        
        status_id = request.POST.get('status')
        if status_id:
            lead.status = Status.objects.get(id=status_id)
        assign_id = request.POST.get('assign_to')
        if assign_id:
            lead.assign_to = Assign.objects.get(id=assign_id)

        lead.is_lead = 'is_lead' in request.POST

        lead.save()
        messages.success(request, 'Lead updated successfully.')
        return redirect('lead')  
    
    context = {
        'lead': lead,
        'statuses': statuses,
        'assigns': assigns,
    }

    return render(request, 'edit.html', context)

