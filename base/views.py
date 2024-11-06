
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,  logout ,login as auth_login
from django.utils import timezone
from base.models import Lead ,Status
from django.utils.dateparse import parse_datetime
from django.db.models import Q


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
            auth_login (request,user)
            messages.success(request, 'Registration successfully')
            return redirect('home')

    return render(request, 'register.html')

# Login
def login(request):
    if request.method =='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request,email=email,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'Login Successfully')
            return redirect("home")
        else:
            messages.error(request,'Invalid Email and password')
            return redirect('login')
    return render(request,'login.html')

# logout
def logout(request):
    logout(request)
    return redirect('home')

#dashboard
def dashboard(request):
    
    return render(request, 'dashboard.html')



#lead Table
def all_lead(request):
    search_query = request.GET.get("search", "")
    if search_query:
        lead = Lead.objects.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(address__icontains=search_query) |
            Q(status__identity__icontains=search_query)  
        ).distinct()
    else:
        lead = Lead.objects.all()
    context = {'lead': lead, 'search_query': search_query}
    return render(request, 'data.html', context)





#add Status
def add_status(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        
        # Check if status is provided
        if status:
            new_status = Status(identity=status)
            new_status.save()
            messages.success(request, 'Status added successfully.')
            return redirect('add-status')
        else:
            messages.error(request, 'Please enter a status.')

    return render(request, 'status.html')

#add Lead
def add_lead(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        gender=request.POST.get('gender')
        passout=request.POST.get('passout')
        college=request.POST.get('college_name')
        tech =request.POST.get('tech_field')
        status_name = request.POST.get('status')
        is_lead = request.POST.get('is_lead') == 'on'
        created_at = request.POST.get('created_at')
        follow_up = request.POST.get('follow_up')

        status, created = Status.objects.get_or_create(identity=status_name)
        Lead.objects.create(
            name=name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            status=status,
            gender=gender,
            passout=passout,
            tech_field=tech,
            college_name=college,
            is_lead=is_lead,
            created_at=created_at,
            follow_up=follow_up,
        )

        messages.success(request, 'New lead added successfully.')
        return redirect('lead') 
    return render(request, 'lead.html')


#delete lead
def delete_lead(request,pk):
    del_lead = Lead.objects.get(id=pk)
    del_lead.delete()
    messages.success(request,"Deleted Successfully")
    return redirect('lead')



#edit lead
def edit_lead(request, pk):
    # Retrieve the specific lead or return 404 if not found
    lead = get_object_or_404(Lead, id=pk)

    if request.method == 'POST':
        # Update the lead data with the posted form values
        lead.name = request.POST.get('name')
        lead.email = request.POST.get('email')
        lead.phone = request.POST.get('phone')
        lead.address = request.POST.get('address')
        lead.city = request.POST.get('city')
        lead.gender = request.POST.get('gender')
        lead.passout = request.POST.get('passout')
        lead.college_name = request.POST.get('college_name')
        lead.tech_field = request.POST.get('tech_field')
        lead.is_lead = request.POST.get('is_lead') == 'on'
        lead.created_at = request.POST.get('created_at')
        lead.follow_up = request.POST.get('follow_up')
        
        # Retrieve or create the status
        status_name = request.POST.get('status')
        status, created = Status.objects.get_or_create(identity=status_name)
        lead.status = status
        
        # Save the updated lead information
        lead.save()

        messages.success(request, 'Lead updated successfully.')
        return redirect(('lead'))  # Redirect to the lead list

    context = {'lead': lead}
    return render(request, 'lead.html', context)


#report


