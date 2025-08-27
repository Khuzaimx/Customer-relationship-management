from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from .forms import AddRecordForm
from .models import Record 

# Create your views here.
def home(request):
    records=Record.objects.all()
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user=authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "you have been successfully logged in")
            return redirect('home')
        else:
            messages.success(request, "Error logging you in")
            return redirect('home')
    else:    
        return render(request, 'website/home.html', {'records' : records})
    print(records)

def login_user(request):
    pass

def logout_user(request):
    logout(request)
    messages.success(request, "Logged out!")
    return redirect('home')

def register_user(request):
    if request.method=='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have signed up succcesfuly")
            return redirect('home')
    else:    
        form=SignUpForm()
        return render(request, 'website/register.html', {'form' : form})
    return render(request, 'website/register.html', {'form' : form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record=Record.objects.get(id=pk)
        return render(request, 'website/record.html', {'customer_record' : customer_record})
    else:
        messages.success(request, "You must be logged in to access records")
        return redirect('home')
    
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it=Record.objects.get(id=pk)    
        delete_it.delete()
        messages.success(request, "Record deleted successfuly")
        return redirect('home')
    else:
        messages.success(request, "Record deleted successfuly")
        return redirect('home')
    
def add_record(request):
      form = AddRecordForm(request.POST or None) 
      if request.user.is_authenticated:
          if request.method=='POST':
              if form.is_valid():
                  record=form.save()
                  messages.success(request, "Record added successfully") 
                  return redirect('home')
          return render(request, 'website/add_record.html', {'form' : form})  
      else:
          messages.success(request, "You must be logged in to update records")  

def update_record(request, pk):
    if request.user.is_authenticated:
        current_record=Record.objects.get(id=pk)
        form=AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record has been uploaded")
            return redirect('home')  
        return render(request, 'website/update_record.html', {'form' : form})    
    else:
        messages.success(request, "You must be logged in to update record")
        return redirect('home')




    



        
    