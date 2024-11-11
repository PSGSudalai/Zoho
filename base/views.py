
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
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

        # Apply date filters if provided
    if start_date:
        start_date = parse_date(start_date)
    if end_date:
        end_date = parse_date(end_date)

    if start_date and end_date:
        lead_queryset = lead_queryset.filter(created_at__range=[start_date, end_date])
    elif start_date:
        lead_queryset = lead_queryset.filter(created_at__gte=start_date)
    elif end_date:
        lead_queryset = lead_queryset.filter(created_at__lte=end_date)

    # Get the count after applying filters
    # lead_count = lead_queryset.count()

    user = Assign.objects.all().count()

# Filter leads created in the current month and year
    monthly_lead = Lead.objects.filter(   #monthly lead for monhtly count
        created_at__month=current_month,
        created_at__year=current_year
    ).count()
    weekly_follow_up = Lead.objects.filter(follow_up__week=current_week)   # weekly follow up list
    total_lead = Lead.objects.all().count()   # Total lead count
    leading = Lead.objects.all()[:5]   #Lead Data List
    lead_count = Lead.objects.all().count()   #Lead Data count
    leadweek = Lead.objects.filter(follow_up__week=current_week)

        # Count statuses for overall metrics
        status_count = Lead.objects.filter(status__identity="Success").count()
        closed_lead = Lead.objects.filter(status__identity="Closed").count()
        negotiation_lead = Lead.objects.filter(status__identity="Negotiation").count()
        follow_up_lead = Lead.objects.filter(status__identity="Follow Up").count()
        pending_lead = Lead.objects.filter(status__identity="Pending").count()

        # Count sources for overall metrics
        source = Lead.objects.filter(source="Referral").count()
        social = Lead.objects.filter(source="Social media").count()

        # Weekly metrics for leads, success status, and gender distribution
        current_lead_count = Lead.objects.filter(created_at__week=current_week).count()
        success_count = Lead.objects.filter(created_at__week=current_week, status__identity='Success').count()
        lead_male = Lead.objects.filter(gender='Male', created_at__week=current_week).count()
        lead_female = Lead.objects.filter(gender='Female', created_at__week=current_week).count()

        # Prepare arrays for JavaScript usage
        leadchart = [0, 0, current_lead_count, 0]
        leadStatus = [0, 0, success_count, 0]
        lead_gender_male = [0, 0, lead_male, 0]
        lead_gender_female = [0, 0, lead_female, 0]

        # Yearly and weekly source counts
        source_social = Lead.objects.filter(source='Social media', created_at__year=current_year).count()
        source_job = Lead.objects.filter(source='Job portal', created_at__year=current_year).count()
        source_referral = Lead.objects.filter(source='Referral', created_at__year=current_year).count()
        source_whatsapp = Lead.objects.filter(source='Whatsapp', created_at__year=current_year).count()

        week_social = Lead.objects.filter(source='Social media', created_at__week=current_week).count()
        week_job = Lead.objects.filter(source='Job portal', created_at__week=current_week).count()
        week_referral = Lead.objects.filter(source='Referral', created_at__week=current_week).count()
        week_whatsapp = Lead.objects.filter(source='Whatsapp', created_at__week=current_week).count()

        # Yearly and weekly status counts
        year_success = Lead.objects.filter(status__identity="Success", created_at__year=current_year).count()
        year_closed = Lead.objects.filter(status__identity="Closed", created_at__year=current_year).count()
        year_negotiation = Lead.objects.filter(status__identity="Negotiation", created_at__year=current_year).count()
        year_follow_up = Lead.objects.filter(status__identity="Follow Up", created_at__year=current_year).count()
        year_pending = Lead.objects.filter(status__identity="Pending", created_at__year=current_year).count()

        week_success = Lead.objects.filter(status__identity="Success", created_at__week=current_week).count()
        week_closed = Lead.objects.filter(status__identity="Closed", created_at__week=current_week).count()
        week_negotiation = Lead.objects.filter(status__identity="Negotiation", created_at__week=current_week).count()
        week_follow_up = Lead.objects.filter(status__identity="Follow Up", created_at__week=current_week).count()
        week_pending = Lead.objects.filter(status__identity="Pending", created_at__week=current_week).count()


    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        lead_date = Lead.objects.filter(created_at__range=(start_date, end_date))
    else:
        lead_date = Lead.objects.all()


    

    # Filter sources and statuses
    lead_queryset = Lead.objects.filter(
        source__in=['Social media', 'Whatsapp', 'Referral', 'Job portal'],
        status__identity__in=["Pending", "Follow Up", "Negotation", "Closed", "Success"]
    )




   

    content = {
        'user':user,
        'lead_count': lead_count,
        'source':source,
        'social':social,
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
        'closed_lead':closed_lead,
        'pending_lead':pending_lead,
        'follow_up_lead':follow_up_lead,
        'negotiation_lead':negotiation_lead,
        'source_whatsapp':source_whatsapp,
        'week_success':week_success,
        'week_closed':week_closed,
        'week_negotiation':week_negotiation,
        'week_follow_up':week_follow_up,
        'week_pending':week_pending,
        'year_success':year_success,
        'year_closed':year_closed,
        'year_negotiation':year_negotiation,
        'year_follow_up':year_follow_up,
        'year_pending':year_pending,
        'week_whatsapp':week_whatsapp,
        'week_referral':week_referral,
        'week_job':week_job,
        'week_social':week_social,
        'lead_date':lead_date,
        # fiter chart
        # 'source_social': source_social,
        # 'source_referral': source_referral,
        # 'source_whatsapp': source_whatsapp,
        # 'source_job': source_job,
        # 'total_lead': total_lead,
        # 'status_count': success_lead,
        # 'negotiation_lead': negotiation_lead,
        # 'follow_up_lead': follow_up_lead,
        # 'pending_lead': pending_lead,
        # 'closed_lead': closed_lead,


    }
    
    return render(request, 'dashboard.html', content)


#lead Table
def all_lead(request, lead_id=None):
    # Get all leads and order them by creation date
    leads = Lead.objects.all().order_by("-created_at")
    
    
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
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
    
    # Apply city filter if provided
    elif city:
        leads = Lead.objects.filter(city=city)
    
    # Apply source filter if provided
    elif source:
        leads = Lead.objects.filter(source=source)
    
    # Apply tech field filter if provided
    elif tech:
        leads = Lead.objects.filter(tech_field=tech)
    # Apply tech field filter if provided
    elif gender:
        leads = Lead.objects.filter(gender=gender)

    # Get a specific lead if an ID is provided
    lead = None
    if lead_id:
        lead = get_object_or_404(Lead, id=lead_id)

    context = {
        'lead': lead,
        'leads': leads,  # Pass filtered or all leads to the template
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

def add_assign(request):
    assign = Assign.objects.all()
    
    if request.method == 'POST':
        # Get the value from the POST data and trim whitespace
        assign_to = request.POST.get('assigned_to', '').strip()
        
        if assign_to:
            if not Assign.objects.filter(assign_to=assign_to).exists():
                new_assign = Assign(assign_to=assign_to)
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
        assign_id = request.POST.get('assign_to')
        is_lead = False

        try:
            status = Status.objects.get(id=status_id)
        except (Status.DoesNotExist, ValueError):
            status = None
        
        # If the status is 'Active', mark as lead
        if status and status.identity == 'Active': 
            is_lead = True

        try:
            assign = Assign.objects.get(id=assign_id)
        except(Assign.DoesNotExist,ValueError):
            assign = None

        # Check if the follow-up date is provided; if not, set it to None
        follow_up = request.POST.get('follow_up') or None

        # Create the new Lead object
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
            assign_to=assign  # This will be None if not provided
        )

        messages.success(request, 'New lead added successfully.')
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
        
        status_id = request.POST.get('status')
        if status_id:
            lead.status = Status.objects.get(id=status_id)

        lead.is_lead = 'is_lead' in request.POST

        lead.save()
        messages.success(request, 'Lead updated successfully.')
        return redirect('lead')  
    
    context = {
        'lead': lead,
        'statuses': statuses,
    }

    return render(request, 'edit.html', context)

