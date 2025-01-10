from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm

# Linear Search Function to filter students by name or marks
def search_students(students, search_query):
    filtered_students = []
    # Convert the search query to lowercase for case-insensitive comparison
    search_query = search_query.lower()
    
    for student in students:
        # Check if search query matches name or marks (starts with search term)
        if search_query in student.name.lower() or str(student.marks).startswith(search_query):
            filtered_students.append(student)
    
    return filtered_students

# View to display all students with sorting and searching by name/marks
def student_list(request):
    sort_order = request.GET.get('sort_order', 'desc')  # Default is descending order
    search_query = request.GET.get('search_query', '')  # Get search query

    # Fetch all students
    students = Student.objects.all()

    # If a search query exists, filter the students using the search function
    if search_query:
        students = search_students(students, search_query)

    # Apply sorting if necessary
    if sort_order == 'asc':
        students = students.order_by('marks')  # Ascending order
    else:
        students = students.order_by('-marks')  # Descending order
    
    return render(request, 'student_list.html', {'students': students, 'sort_order': sort_order, 'search_query': search_query})

# View to add a new student
def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            # Get the marks from the form
            marks = form.cleaned_data['marks']
            
            # Automatically assign grade based on marks
            if marks >= 90:
                grade = 'A+'
            elif marks >= 80:
                grade = 'A'
            elif marks >= 70:
                grade = 'B+'
            elif marks >= 60:
                grade = 'B'
            elif marks >= 50:
                grade = 'C+'
            elif marks > 40:
                grade = 'C'
            elif marks ==40:
                grade = 'P'
            else:
                grade = 'F'
            
            # Save the grade to the form before saving
            student = form.save(commit=False)  # Do not save to DB yet
            student.grade = grade  # Assign the grade
            student.save()  # Now save the student object with the grade

            return redirect('student_list')
    else:
        form = StudentForm()

    return render(request, 'add_student.html', {'form': form})

# View to edit a student record
def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'edit_student.html', {'form': form})

# View to delete a student record
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    return redirect('student_list')



def student_list(request):
    sort_order = request.GET.get('sort_order', 'desc')  # Default sorting order
    search_query = request.GET.get('search_query', '')  # Get search query if provided
    
    # Filter students by search query if provided
    if search_query:
        students = Student.objects.filter(name__icontains=search_query) | Student.objects.filter(marks__icontains=search_query)
    else:
        students = Student.objects.all()

    # Apply sorting
    if sort_order == 'asc':
        students = students.order_by('marks')
    else:
        students = students.order_by('-marks')

    return render(request, 'student_list.html', {'students': students, 'sort_order': sort_order, 'search_query': search_query})