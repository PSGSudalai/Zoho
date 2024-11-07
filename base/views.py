
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,  logout ,login 
from django.utils import timezone
from base.models import Lead ,Status
from django.utils.dateparse import parse_datetime
from django.db.models import Q
from django.utils import timezone


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
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Login Successful')
            return redirect('lead')
        else:
            messages.error(request, 'Invalid Email or Password')
            return redirect('login')

    return render(request, 'index.html')

# logout
def logout(request):
    logout(request)
    return redirect('index')

#dashboard
def dashboard(request):
    total_lead = Lead.objects.all().count()  # Total number of leads
    lead_status = Lead.objects.filter(is_lead=True).count()  # Number of leads with is_lead=True

    # Count of leads where the status is "Success"
    status_count = Lead.objects.filter(status__identity="Success").count()

    content = {
        'total_lead': total_lead,
        'lead_status': lead_status,
        'status_count': status_count
    }
    
    return render(request, 'dashboard.html', content)



#lead Table
def all_lead(request, lead_id=None):
    leads = Lead.objects.all()
    statuses = Status.objects.all()  # Get all status objects from the database
      # Get all lead objects

    # Check if you're editing an existing lead
    lead = None
    if lead_id:
        lead = get_object_or_404(Lead, id=lead_id)  # Safely get the lead or return a 404 if not found
    
    context = {
        'lead': lead,
        'statuses': statuses,
        'leads': leads,  # Pass all leads to the template
    }
    
    return render(request, 'lead.html', context)


# def status(request):
#     statuses = Status.objects.all()  
#     lead = None  # Replace with actual lead object if editing an existing lead

#     # If you're editing an existing lead, fetch the lead and pass it in the context
#     if 'lead_id' in request.GET:  # Example condition for fetching a lead
#         lead = Lead.objects.get(id=request.GET['lead_id'])
#     return render(request, 'add-lead.html', {'statuses': statuses})


# #add Status
def add_status(request):
    if request.method == 'POST':
        status_name = request.POST.get('identity', '').strip()
        
        # Check if the input is valid and not empty
        if status_name:
            if not Status.objects.filter(identity=status_name).exists():
                new_status = Status(identity=status_name)
                new_status.save()
                messages.success(request, "Added successfully")
            else:
                messages.warning(request, "Status with this identity already exists")
        else:
            messages.error(request, "Status name cannot be empty")
        
        return redirect('add_status')
    
    return render(request, 'add-lead.html')


#add Lead
def add_lead(request):
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
        status_id = request.POST.get('status') 
        is_lead = False 
        status = Status.objects.get(id=status_id)  
        if status.identity == 'Active': 
            is_lead = True
        
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
            college_name=college,
            status=status,  # Ensure status is set
            is_lead=is_lead,  # Set is_lead based on condition
            follow_up=follow_up,  # Follow-up date (optional)
        )

        messages.success(request, 'New lead added successfully.')
        return redirect('lead')  # Redirect to the list or another view
    
    return render(request, 'add-lead.html')

#delete lead
def delete_lead(request,pk):
    del_lead = Lead.objects.get(id=pk)
    del_lead.delete()
    messages.success(request,"Deleted Successfully")
    return redirect('lead')



#edit lead
def edit_lead(request, lead_id):
    lead = get_object_or_404(Lead, pk=lead_id)
    if request.method == 'POST':
        # Handle the POST request to update the lead
        lead.name = request.POST.get('name')
        lead.email = request.POST.get('email')
        lead.address = request.POST.get('address')
        lead.city = request.POST.get('city')
        lead.phone = request.POST.get('phone')
        lead.passout = request.POST.get('passout')
        lead.gender = request.POST.get('gender')
        lead.college_name = request.POST.get('college_name')
        lead.status = request.POST.get('status')
        lead.is_lead = request.POST.get('is_lead') == 'on'
        lead.tech_field = request.POST.get('tech_field')
        lead.created_at = request.POST.get('created_at')
        lead.follow_up = request.POST.get('follow_up')
        lead.save()
        return redirect('lead')  # Redirect to the lead list page or wherever you want after saving

    return render(request, 'edit.html', {'lead': lead})


