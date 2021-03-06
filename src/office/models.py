from django.db import models

from account import models as mod


class ClassRoutine(models.Model):
    school = models.ForeignKey(mod.School, on_delete=models.CASCADE)
    classes = models.ForeignKey(mod.Class, on_delete=models.CASCADE)
    section = models.ForeignKey(mod.Section, on_delete=models.CASCADE)
    subject = models.ForeignKey(mod.Subject, on_delete=models.CASCADE)

    day = models.CharField(max_length=30, null=True, blank=True)
    period = models.IntegerField(null=True, blank=True)
    start_hour = models.TimeField(null=True, blank=True)
    end_hour = models.TimeField(null=True, blank=True)

    def __str__(self):
        return str(self.day) + "-" + str(self.period)


class ExamRoutine(models.Model):
    school = models.ForeignKey(mod.School, on_delete=models.CASCADE)
    classes = models.ForeignKey(mod.Class, on_delete=models.CASCADE)
    subject = models.ForeignKey(mod.Subject, on_delete=models.CASCADE)

    exam_name = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    start_hour = models.TimeField(null=True, blank=True)
    end_hour = models.TimeField(null=True, blank=True)

    def __str__(self):
        return str(self.school) + "-" + str(self.classes.name) + "-" + str(self.date)


#office notice model
class Notice(models.Model):
    school = models.ForeignKey(mod.School, on_delete=models.CASCADE)
    classes = models.ForeignKey(mod.Class, on_delete=models.CASCADE)
    user = models.ForeignKey(mod.UserProfile, on_delete=models.CASCADE)

    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.school.name) + "-" + str(self.classes.name) + "-" + str(self.user.username)


#gallary image upload model
class GallaryImage(models.Model):
    school = models.ForeignKey(mod.School, on_delete=models.CASCADE)
    user = models.ForeignKey(mod.UserProfile, on_delete=models.CASCADE)

    description = models.TextField(max_length=1000, null=True, blank=True)
    image = models.ImageField(upload_to='school/gallary/', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.school.name) + "-" + str(self.user.username)

    def delete(self, *args, **kwargs):
        storage, path = self.image.storage, self.image.path
        super(GallaryImage, self).delete(*args, **kwargs)
        storage.delete(path)


#gallary video upload model
class GallaryVideo(models.Model):
    school = models.ForeignKey(mod.School, on_delete=models.CASCADE)
    user = models.ForeignKey(mod.UserProfile, on_delete=models.CASCADE)

    description = models.TextField(max_length=1000, null=True, blank=True)
    video = models.CharField(max_length=255, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.school.name) + "-" + str(self.user.username)



#class room module
class Classroom(models.Model):
    school = models.ForeignKey(mod.School, on_delete=models.CASCADE)
    classes = models.ForeignKey(mod.Class, on_delete=models.CASCADE)
    section = models.ForeignKey(mod.Section, on_delete=models.CASCADE)

    room = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)


    def __str__(self):
        return str(self.school.name) + "-" + str(self.classes.name) + "-" + str(self.section.name) + "-" + str(self.room)


#event create
class Event(models.Model):
    school = models.ForeignKey(mod.School, on_delete=models.CASCADE)
    user = models.ForeignKey(mod.UserProfile, on_delete=models.CASCADE)

    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.school.name) + "-" + str(self.user.username) + ":" + str(self.id)


#expense catagory
class ExpenseCatagory(models.Model):
    school = models.ForeignKey(mod.School, on_delete=models.CASCADE)
    user = models.ForeignKey(mod.UserProfile, on_delete=None)

    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)


    def __str__(self):
        return str(self.school.name) + "-" + str(self.user.username) + "-" + str(self.name)



#expense entry
class Expense(models.Model):
    school = models.ForeignKey(mod.School, on_delete=models.CASCADE)
    catagory = models.ForeignKey(ExpenseCatagory, on_delete=None)
    user = models.ForeignKey(mod.UserProfile, on_delete=None)

    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    method = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateField(null=True, blank=True)


    def __str__(self):
        return str(self.school.name) + "-" + str(self.catagory.name) + "-" + str(self.user.username)


#bus
class Bus(models.Model):
    school = models.ForeignKey(mod.School, on_delete=models.CASCADE)

    name = models.CharField(max_length=255, blank=True, null=True)
    bus_route = models.CharField(max_length=255, null=True, blank=True)
    driver_name = models.CharField(max_length=255, null=True, blank=True)
    driver_phone = models.CharField(max_length=255, null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)

    def __str__(self):
        return str(self.school.name) + "-" + str(self.name) + ":" + str(self.bus_route)



#payment
class Payment(models.Model):
    school = models.ForeignKey(mod.School, on_delete=models.CASCADE)
    classes = models.ForeignKey(mod.Class, on_delete=models.CASCADE)
    section = models.ForeignKey(mod.Section, on_delete=models.CASCADE)
    user = models.ForeignKey(mod.UserProfile, on_delete=None, related_name='receiver')
    student = models.ForeignKey(mod.UserProfile, on_delete=None, related_name='payer')

    #payment type will be exam/monthly fee
    payment_type = models.CharField(max_length=255, null=True, blank=True)

    #payment_as will be :
    #if monthly then month name like: january, february etc
    #if exam then : 1st_term, 2nd_term etc
    payment_as = models.CharField(max_length=255, null=True, blank=True)
    month = models.CharField(max_length=255, null=True, blank=True)

    total = models.FloatField(null=True, blank=True)
    paid_amount = models.FloatField(null=True, blank=True)

    payment_status = models.CharField(max_length=255, null=True, blank=True)
    payment_method = models.CharField(max_length=255, null=True, blank=True)

    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.school.name) + "-" + str(self.classes.name) + "-" + str(self.student.username)



