from django.shortcuts import render, redirect
from .models import Student, Subject, Question , Result
def home(request):
    return render(request, "index.html")

def register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        Student.objects.create(
            name=name,
            email=email,
            phone=phone,
            password=password
        )

        return redirect("studentlogin")

    return render(request, "register.html")

def studentlogin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            student = Student.objects.get(email=email, password=password)
            request.session["student_id"] = student.id
            return redirect("studentdashboard")
        except Student.DoesNotExist:
            return render(request, "studentlogin.html", {
                "error": "Invalid Email or Password"
            })

    return render(request, "studentlogin.html")

def studentdashboard(request):
    return render(request, "studentdashboard.html")

def adminlogin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username == "admin" and password == "admin123":
            request.session["admin_logged_in"] = True
            return redirect("admindashboard")
        else:
            return render(request, "adminlogin.html", {
                "error": "Invalid Username or Password"
            })
    return render(request, "adminlogin.html")

def admindashboard(request):
    students = Student.objects.all()
    subjects = Subject.objects.all()
    questions = Question.objects.all()
    results = Result.objects.all()

    context = {
        "students": students,
        "subjects": subjects,
        "questions": questions,
        "results": results,
    }

    return render(request, "admindashboard.html", context)

def start_exam(request):
    questions = Question.objects.all()

    if request.method == "POST":
        score = 0

        for q in questions:
            answer = request.POST.get(f"q{q.id}")

            if answer == q.answer:
                score += 1

        request.session["score"] = score

        student_id = request.session.get("student_id")
        
        if student_id:
            student= Student.objects.get(id=student_id)
            if questions.exists():
                subject= questions.first().subject

        Result.objects.create(
            student=student,
            subject=subject,
            score=score
        )

        return redirect("result")

    return render(request, "startexam.html", {"questions": questions})

def result(request):
    score = request.session.get("score", 0)

    return render(request, "result.html", {
        "score": score
    })

def profile(request):
    student_id = request.session.get("student_id")

    if student_id:
        student = Student.objects.get(id=student_id)
        return render(request, "profile.html", {
            "student": student
        })

    return redirect("studentlogin")

def logout(request):
    request.session.flush()
    return redirect("studentlogin")

def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, "subject_list.html", {"subjects": subjects})


def subject_exam(request, subject_id):
    subject = Subject.objects.get(id=subject_id)
    questions = Question.objects.filter(subject=subject)

    if request.method == "POST":
        score = 0

        for question in questions:
            selected = request.POST.get(str(question.id))

            if selected == question.answer:
                score += 1

        student = Student.objects.get(id=request.session["student_id"])

        Result.objects.create(
            student=student,
            subject=subject,
            score=score
        )

        return render(request, "result.html", {
            "score": score,
            "total": questions.count()
        })

    return render(request, "subject_exam.html", {
        "subject": subject,
        "questions": questions
    })

def my_results(request):
    student = Student.objects.get(id=request.session["student_id"])
    results = Result.objects.filter(student=student)

    return render(request, "my_results.html", {
        "results": results
    })

def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, "subject_list.html", {"subjects": subjects})

def add_subject(request):
    if request.method == "POST":
        subject_name = request.POST.get("subject_name")
        Subject.objects.create(subject_name=subject_name)
        return redirect("admindashboard")

    return render(request, "add_subject.html")

def subject_exam(request, subject_id):
    subject = Subject.objects.get(id=subject_id)
    questions = Question.objects.filter(subject=subject)

    if request.method == "POST":
        score = 0

        for question in questions:
            selected = request.POST.get(str(question.id))

            if selected == question.answer:
                score += 1

        student = Student.objects.get(id=request.session["student_id"])

        Result.objects.create(
            student=student,
            subject=subject,
            score=score
        )

        return render(request, "result.html", {
            "score": score,
            "total": questions.count()
        })

    return render(request, "subject_exam.html", {
        "subject": subject,
        "questions": questions
    })

def my_results(request):
    student = Student.objects.get(id=request.session["student_id"])
    results = Result.objects.filter(student=student)

    return render(request, "my_results.html", {
        "results": results
    })

def logout(request):
    request.session.flush()
    return redirect("studentlogin")

def add_question(request):
    subjects = Subject.objects.all()

    if request.method == "POST":
        subject_id = request.POST.get("subject")
        question_text = request.POST.get("question")
        option1 = request.POST.get("option1")
        option2 = request.POST.get("option2")
        option3 = request.POST.get("option3")
        option4 = request.POST.get("option4")
        answer = request.POST.get("answer")

        subject = Subject.objects.get(id=subject_id)

        Question.objects.create(
            subject=subject,
            question=question_text,
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            answer=answer
        )

        return redirect("admindashboard")

    return render(request, "add_question.html", {"subjects": subjects})

def add_student(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        Student.objects.create(
            name=name,
            email=email,
            phone=phone,
            password=password
        )

        return redirect("admindashboard")

    return render(request, "add_student.html")