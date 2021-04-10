from django.db import models
from django.contrib.auth.models import User
from Questions.models import *


################################################################################



# Student model to store the student's records in the db.

class Student(models.Model):

    test_code = models.ForeignKey(ConfigCreation,on_delete=models.CASCADE)

    studentName = models.CharField(null=False,blank=False,max_length=50)
    studentId = models.CharField(null=False,blank=False,max_length=50)

    Response = models.OneToOneField(AnswerKey,on_delete=models.CASCADE)

    section1_marks = models.IntegerField(null=True,blank=True)
    section2_marks = models.IntegerField(null=True,blank=True)
    section3_marks = models.IntegerField(null=True,blank=True)
    total_marks = models.IntegerField(null=True,blank=True)

    section1_total = models.IntegerField(null=True,blank=True)
    section2_total = models.IntegerField(null=True,blank=True)
    section3_total = models.IntegerField(null=True,blank=True)
    overall_total = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return self.studentName

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Student Profiles'




###################################################################################




# Section metrics to store the Metrics of the section of indivisual Test Code.

class SectionMetrics(models.Model):

    test_code = models.OneToOneField(ConfigCreation,on_delete=models.CASCADE)

    # solved = Attempted.

    section1_attempted = models.IntegerField(null=True,blank=True)
    section1_correct = models.IntegerField(null=True,blank=True)
    section1_incorrect = models.IntegerField(null=True,blank=True)


    section2_attempted = models.IntegerField(null=True,blank=True)
    section2_correct = models.IntegerField(null=True,blank=True)
    section2_incorrect = models.IntegerField(null=True,blank=True)


    section3_attempted = models.IntegerField(null=True,blank=True)
    section3_correct = models.IntegerField(null=True,blank=True)
    section3_incorrect = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return self.test_code.quizName

    class Meta:
        verbose_name = 'Section Metric'
        verbose_name_plural = 'Section Metrics'
