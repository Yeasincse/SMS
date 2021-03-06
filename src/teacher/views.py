from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db.models import Q
import datetime
from django.http import JsonResponse

from account import models
from . import models as teacher_model
from . import forms


#student dashboard access permission mixin
class TeacherPermissionMixin(object):
    def has_permissions(self, request):
        return request.user.member_type.name == 'teacher'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not self.has_permissions(request):
                return redirect('account:login')
            return super(TeacherPermissionMixin, self).dispatch(
                request, *args, **kwargs)
        else:
            return redirect('account:login')



#teacher dashboard
class Home(TeacherPermissionMixin, View):
    template_name = 'teacher/index.html'

    def get(self, request):
        return render(request, self.template_name)



#class list for attendance
class AttendanceClassList(TeacherPermissionMixin, View):
    template_name = 'teacher/attendance-class-list.html'

    def get(self, request):

        classes = models.Class.objects.filter(Q(school=request.user.school)).all()
        count = models.Class.objects.filter(Q(school=request.user.school)).count()

        variables = {
            'classes': classes,
            'count': count,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass



#attendance section list
class AttendanceSectionList(TeacherPermissionMixin, View):
    template_name = 'teacher/attendance-section-list.html'

    def get(self, request, classes):

        sections = models.Section.objects.filter(Q(school=request.user.school) & Q(classes__name=classes)).all()
        count = models.Section.objects.filter(Q(school=request.user.school) & Q(classes__name=classes)).count()


        variables = {
            'sections': sections,
            'count': count,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass




#attendance subject list
class AttendanceSubjectList(TeacherPermissionMixin, View):
    template_name = 'teacher/attendance-subject-list.html'

    def get(self, request, classes, section):

        subjects = models.Subject.objects.filter(Q(school=request.user.school) & Q(classes__name=classes)).all()
        count = models.Subject.objects.filter(Q(school=request.user.school) & Q(classes__name=classes)).count()


        variables = {
            'subjects': subjects,
            'count': count,
            'section': section,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass



#attendance subject wise
class AttendanceSubjectAll(TeacherPermissionMixin, View):
    template_name = 'teacher/attendance-list.html'

    def get(self, request, classes, section, subject_id):

        now = datetime.datetime.now()

        attendance_lists = teacher_model.Attendence.objects.filter(Q(school=request.user.school) & Q(classes__name=classes) & Q(section__name=section) & Q(subject__id=subject_id)).order_by('-id').all()
        count = teacher_model.Attendence.objects.filter(Q(school=request.user.school) & Q(classes__name=classes) & Q(section__name=section) & Q(subject__id=subject_id)).count()


        variables = {
            'attendance_lists': attendance_lists,
            'count': count,
            'now': now.date,
            'subject_id': subject_id,
            'classes': classes,
            'section': section,
        }

        return render(request, self.template_name, variables)

    def post(self, request, classes, section, subject_id):
        now = datetime.datetime.now()

        attendance_lists = teacher_model.Attendence.objects.filter(Q(school=request.user.school) & Q(classes__name=classes) & Q(section__name=section) & Q(subject__id=subject_id)).all()
        count = teacher_model.Attendence.objects.filter(Q(school=request.user.school) & Q(classes__name=classes) & Q(section__name=section) & Q(subject__id=subject_id)).count()

        if request.POST.get('take_attendance') == 'take_attendance':
            get_object_or_404(models.Subject, pk=subject_id)

            class_obj = models.Class.objects.get(Q(school=request.user.school) & Q(name=classes))
            section_obj = models.Section.objects.get(Q(school=request.user.school) & Q(classes=class_obj) & Q(name=section))
            subject_obj = models.Subject.objects.get(Q(school=request.user.school) & Q(classes=class_obj) & Q(pk=subject_id))

            attendance = teacher_model.Attendence(school=request.user.school, classes=class_obj, section=section_obj, subject=subject_obj, teachers=request.user)
            attendance.save()

            return redirect('teacher:attendance-create', classes=classes, section=section, attendance_id=attendance.id)

        variables = {
            'attendance_lists': attendance_lists,
            'count': count,
            'now': now.date,
        }

        return render(request, self.template_name, variables)


#attendance create
class AttendanceCreate(TeacherPermissionMixin, View):
    template_name = 'teacher/attendance-create.html'

    def get(self, request, classes, section, attendance_id):
        get_object_or_404(teacher_model.Attendence, pk=attendance_id)
        now = datetime.datetime.now()

        students = models.UserProfile.objects.filter(Q(school=request.user.school) & Q(classes__name=classes) & Q(section__name=section)).order_by('student__roll').all()
        count = models.UserProfile.objects.filter(Q(school=request.user.school) & Q(classes__name=classes) & Q(section__name=section)).count()

        attendances = teacher_model.Attendence.objects.get(id=attendance_id)
        present_lists = attendances.students.all()


        variables = {
            'now': now.date,
            'students': students,
            'count': count,
            'attendance_id': attendance_id,
            'present_lists': present_lists,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass



#attendance subject wise statistics
class AttendanceSubjectWiseStatistics(TeacherPermissionMixin, View):
    template_name = 'teacher/attendance-subject-wise-statistics.html'

    def get(self, request, classes, section, subject_id):

        subjects = models.Subject.objects.get(Q(school=request.user.school) & Q(classes__name=classes) & Q(id=subject_id))

        total_class = teacher_model.Attendence.objects.filter(Q(school=request.user.school) & Q(classes__name=classes) & Q(section__name=section) & Q(subject__id=subject_id)).count()
        attendance_obj = teacher_model.Attendence.objects.filter(Q(school=request.user.school) & Q(classes__name=classes) & Q(section__name=section) & Q(subject__id=subject_id)).all()


        students = models.UserProfile.objects.filter(Q(school=request.user.school) & Q(classes__name=classes) & Q(section__name=section)).order_by('student__roll').all()
        total_student = models.UserProfile.objects.filter(Q(school=request.user.school) & Q(classes__name=classes) & Q(section__name=section)).count()

        present_count_list = []
        for student in students:
            count = 0
            for attendance in attendance_obj:
                present_students_obj = attendance.students.all()

                if student in present_students_obj:
                    count = count + 1

            present_count_list.append(count)

        zipped = zip(students, present_count_list)

        variables = {
            'subjects': subjects,
            'section': section,
            'total_class': total_class,
            'classes': classes,
            'section': section,
            'zipped': zipped,
            'total_student': total_student,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass


#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::start take exam and exam marks:::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


#attendance subject wise statistics
class ExamAndMarksHome(TeacherPermissionMixin, View):
    template_name = 'teacher/exam-and-marks-home.html'

    def get(self, request):

        variables = {

        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass


#class list for Exam and marks
class ExamAndMarksClassList(TeacherPermissionMixin, View):
    template_name = 'teacher/exam-and-marks-class-list.html'

    def get(self, request):

        classes = models.Class.objects.filter(Q(school=request.user.school)).all()
        count = models.Class.objects.filter(Q(school=request.user.school)).count()

        variables = {
            'classes': classes,
            'count': count,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass


#exam and marks section list
class ExamAndMarksSectionList(TeacherPermissionMixin, View):
    template_name = 'teacher/exam-and-marks-section-list.html'

    def get(self, request, classes):

        sections = models.Section.objects.filter(Q(school=request.user.school) & Q(classes__name=classes)).all()
        count = models.Section.objects.filter(Q(school=request.user.school) & Q(classes__name=classes)).count()


        variables = {
            'sections': sections,
            'count': count,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass


#exam and marks subject list
class ExamAndMarksSubjectList(TeacherPermissionMixin, View):
    template_name = 'teacher/exam-and-marks-subject-list.html'

    def get(self, request, classes, section):

        subjects = models.Subject.objects.filter(Q(school=request.user.school) & Q(classes__name=classes)).all()
        count = models.Subject.objects.filter(Q(school=request.user.school) & Q(classes__name=classes)).count()


        variables = {
            'subjects': subjects,
            'count': count,
            'section': section,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass



#exam and marks subject wise
class ExamAndMarksSubjectAllExam(TeacherPermissionMixin, View):
    template_name = 'teacher/class-test-exam-time-list.html'

    def get(self, request, classes, section, subject_id):

        exam_lists = teacher_model.ClassTestExamTime.objects.filter(Q(school=request.user.school) & Q(classes__name=classes) & Q(section__name=section) & Q(subject__id=subject_id)).order_by('date').all()
        count = teacher_model.ClassTestExamTime.objects.filter(Q(school=request.user.school) & Q(classes__name=classes) & Q(section__name=section) & Q(subject__id=subject_id)).count()


        variables = {
            'exam_lists': exam_lists,
            'count': count,
            'subject_id': subject_id,
            'classes': classes,
            'section': section,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass


#create class test exam routine
class ExamAndMarksExamCreate(TeacherPermissionMixin, View):
    template_name = 'teacher/class-test-exam-time-create.html'

    def get(self, request, classes, section, subject_id):

        exam_routine_form = forms.ClassTestExamTimeForm()

        variables = {
            'exam_routine_form': exam_routine_form,
        }

        return render(request, self.template_name, variables)

    def post(self, request, classes, section, subject_id):
        exam_routine_form = forms.ClassTestExamTimeForm(request.POST or None)

        if exam_routine_form.is_valid():
            deploy = exam_routine_form.deploy(request, classes, section, subject_id)

        variables = {
            'exam_routine_form': exam_routine_form,
        }

        return render(request, self.template_name, variables)



#edit class test exam routine
class ExamAndMarksExamEdit(TeacherPermissionMixin, View):
    template_name = 'teacher/class-test-exam-time-edit.html'

    def get(self, request, pk):
        get_object_or_404(teacher_model.ClassTestExamTime, pk=pk)

        exam_routine_edit_form = forms.EditClassTestExamTimeForm(instance=teacher_model.ClassTestExamTime.objects.get(Q(school=request.user.school) & Q(pk=pk)))

        variables = {
            'exam_routine_edit_form': exam_routine_edit_form,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        get_object_or_404(teacher_model.ClassTestExamTime, pk=pk)

        exam_routine_edit_form = forms.EditClassTestExamTimeForm(request.POST or None, instance=teacher_model.ClassTestExamTime.objects.get(Q(school=request.user.school) & Q(pk=pk)))

        if exam_routine_edit_form.is_valid():
            exam_routine_edit_form.save()

        variables = {
            'exam_routine_edit_form': exam_routine_edit_form,
        }

        return render(request, self.template_name, variables)



#exam delete
class ExamAndMarksExamDelete(TeacherPermissionMixin, View):
    template_name = 'teacher/class-test-exam-time-delete.html'

    def get(self, request, pk):
        get_object_or_404(teacher_model.ClassTestExamTime, pk=pk)

        exam_obj = teacher_model.ClassTestExamTime.objects.filter(Q(pk=pk) & Q(school=request.user.school))

        viewable_exam = False
        if exam_obj:
            viewable_exam = exam_obj

        variables = {
            'viewable_exam': viewable_exam,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        get_object_or_404(teacher_model.ClassTestExamTime, pk=pk)

        exam_obj = teacher_model.ClassTestExamTime.objects.filter(Q(pk=pk) & Q(school=request.user.school))

        viewable_exam = False
        if exam_obj:
            viewable_exam = exam_obj

            if request.POST.get('yes') == 'yes':
                exam_id = request.POST.get('exam_id')

                exam_obj = teacher_model.ClassTestExamTime.objects.get(id=exam_id)
                exam_obj.delete()

                return redirect('teacher:exam-and-marks-class-list')

            elif request.POST.get('no') == 'no':
                return redirect('teacher:exam-and-marks-class-list')

        variables = {
            'viewable_exam': viewable_exam,
        }

        return render(request, self.template_name, variables)



#publish marks student wise
class ExamAndMarksExamStudent(TeacherPermissionMixin, View):
    template_name = 'teacher/class-test-exam-marks-student.html'

    def get(self, request, classes, section, subject_id, exam_id):

        exam_marks_form = forms.ClassTestExamMarkForm(request=request, classes=classes, section=section, subject=subject_id, exam=exam_id)

        students = models.UserProfile.objects.filter(Q(school=request.user.school) & Q(classes__name=classes) & Q(section__name=section)).order_by('student__roll').all()

        variables = {
            'students': students,
            'exam_marks_form': exam_marks_form,
        }

        return render(request, self.template_name, variables)

    def post(self, request, classes, section, subject_id, exam_id):
        exam_marks_form = forms.ClassTestExamMarkForm(request.POST or None, request=request, classes=classes, section=section, subject=subject_id, exam=exam_id)

        students = models.UserProfile.objects.filter(Q(school=request.user.school) & Q(classes__name=classes) & Q(section__name=section)).order_by('student__roll').all()

        if exam_marks_form.is_valid():
            exam_marks_form.deploy()

        variables = {
            'students': students,
            'exam_marks_form': exam_marks_form,
        }

        return render(request, self.template_name, variables)




#exam and marks view
class ExamAndMarksView(TeacherPermissionMixin, View):
    template_name = 'teacher/class-test-exam-mark-view.html'

    def get(self, request, exam_id):

        exam_lists = teacher_model.ClassTestExamMark.objects.filter(Q(school=request.user.school) & Q(exam__id=exam_id)).order_by('student__student__roll').all()

        variables = {
            'exam_lists': exam_lists,
        }

        return render(request, self.template_name, variables)

    def post(self, request, exam_id):
        pass



#edit class test exam mark
class ExamAndMarksEdit(TeacherPermissionMixin, View):
    template_name = 'teacher/class-test-exam-mark-edit.html'

    def get(self, request, pk):
        get_object_or_404(teacher_model.ClassTestExamMark, pk=pk)

        exam_mark_obj = teacher_model.ClassTestExamMark.objects.filter(Q(pk=pk) & Q(school=request.user.school))

        exam_teacher = None
        for exam in exam_mark_obj:
            exam_teacher = exam.teachers


        exam_mark_edit_form = None
        if exam_teacher == request.user:
            exam_mark_edit_form = forms.EditClassTestExamMarkForm(instance=teacher_model.ClassTestExamMark.objects.get(Q(school=request.user.school) & Q(pk=pk)))


        variables = {
            'exam_mark_edit_form': exam_mark_edit_form,
            'pk': pk,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        get_object_or_404(teacher_model.ClassTestExamMark, pk=pk)

        exam_mark_obj = teacher_model.ClassTestExamMark.objects.filter(Q(pk=pk) & Q(school=request.user.school))

        exam_teacher = None
        for exam in exam_mark_obj:
            exam_teacher = exam.teachers


        exam_mark_edit_form = None
        if exam_teacher == request.user:
            exam_mark_edit_form = forms.EditClassTestExamMarkForm(request.POST or None, instance=teacher_model.ClassTestExamMark.objects.get(Q(school=request.user.school) & Q(pk=pk)))

            if exam_mark_edit_form.is_valid():
                exam_mark_edit_form.save()

        variables = {
            'exam_mark_edit_form': exam_mark_edit_form,
            'pk': pk,
        }


        return render(request, self.template_name, variables)




#exam delete
class ExamAndMarksDelete(TeacherPermissionMixin, View):
    template_name = 'teacher/class-test-exam-time-delete.html'

    def get(self, request, pk):
        get_object_or_404(teacher_model.ClassTestExamMark, pk=pk)

        exam_obj = teacher_model.ClassTestExamMark.objects.filter(Q(pk=pk) & Q(school=request.user.school) & Q(teachers=request.user))

        viewable_exam = False
        if exam_obj:
            viewable_exam = exam_obj

        variables = {
            'viewable_exam': viewable_exam,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        get_object_or_404(teacher_model.ClassTestExamMark, pk=pk)

        exam_obj = teacher_model.ClassTestExamMark.objects.filter(Q(pk=pk) & Q(school=request.user.school) & Q(teachers=request.user))

        viewable_exam = False
        if exam_obj:
            viewable_exam = exam_obj

            if request.POST.get('yes') == 'yes':
                exam_id = request.POST.get('exam_id')

                exam_obj = teacher_model.ClassTestExamMark.objects.get(id=exam_id)
                exam_obj.delete()

                return redirect('teacher:exam-and-marks-class-list')

            elif request.POST.get('no') == 'no':
                return redirect('teacher:exam-and-marks-class-list')

        variables = {
            'viewable_exam': viewable_exam,
        }

        return render(request, self.template_name, variables)




#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::end take exam and exam marks::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::




#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::api view::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

class AttendanceAPIPresent(TeacherPermissionMixin, View):
    def get(self, request):

        message = False

        if request.user.is_authenticated:
            if request.GET.get('student') and request.GET.get('attendance_id'):
                stu_username = request.GET.get('student')
                attendance_id = request.GET.get('attendance_id')
                status = request.GET.get('status')

                student_obj = get_object_or_404(models.UserProfile, username=stu_username)
                attendance_obj = get_object_or_404(teacher_model.Attendence, id=attendance_id)

                #present for student when checked
                if status == 'take_present':
                    if student_obj and attendance_obj:
                        stu_exists_in_present = attendance_obj.students.filter(username=stu_username).exists()

                        if not stu_exists_in_present:

                            student_obj = models.UserProfile.objects.get(username=stu_username)

                            teacher_model.Attendence.addStudent(request.user, student_obj, attendance_id)

                            message = "present"
                        else:
                            message = "allready present count"
                    else:
                        message = 'both not found'

                #delete present for student when unchecked
                elif status == 'take_absent':
                    if student_obj and attendance_obj:
                        stu_exists_in_present = attendance_obj.students.filter(username=stu_username).exists()

                        if stu_exists_in_present:

                            student_obj = models.UserProfile.objects.get(username=stu_username)

                            teacher_model.Attendence.removeStudent(request.user, student_obj, attendance_id)

                            message = "remove present"
                        else:
                            message = "student not found in present"
                    else:
                        message = 'both not found'
        else:
            message = 'not authenticated'

        x = {
            'message': message,
        }

        return JsonResponse(x)
