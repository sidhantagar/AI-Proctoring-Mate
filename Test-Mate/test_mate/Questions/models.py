from django.db import models
from django.contrib.auth.models import User


###############ANSWER##KEY#####################################################################



# Model for storing the Responses from the
class AnswerKey(models.Model):

    test_code = models.ForeignKey('ConfigCreation',on_delete=models.CASCADE)
    studentName = models.CharField(null=False,blank=False,max_length=50)
    studentId = models.CharField(null=False,blank=False,max_length=50)
    responseFile = models.FileField(null=True,blank=True)
    VideoFile = models.FileField(null=True,blank=True)

    def __str__(self):
        return self.studentName + " - files"

    class Meta:
        verbose_name = 'Submission'
        verbose_name_plural = 'Submissions'



######################CONFIG##CREATION################################################################################



# model for storing Question Configuration.

class ConfigCreation(models.Model):

    testCode = models.CharField(null=False,blank=False,max_length=10,primary_key=True)
    testCreator = models.ForeignKey(User,on_delete=models.CASCADE)

    dateCreated = models.CharField(null=False,blank=False,max_length=15)
    timeCreated = models.CharField(null=False,blank=False,max_length=15)

    quizName = models.CharField(null=True,blank=False,max_length=50)
    quizDescription = models.TextField(null=False,blank=False)
    idFormat = models.CharField(null=False,blank=False,max_length=15)

    scheduledDate = models.CharField(null=False,blank=False,max_length=20)
    scheduledTime = models.CharField(null=False,blank=False,max_length=20)

    allowCalculator = models.CharField(null=False,blank=True,max_length=50)
    keepQuestion = models.BooleanField(default=False,null=False,blank=True)


    shuffleQuestions = models.BooleanField(default=False,null=False,blank=False)
    shuffleOptions = models.BooleanField(default=False,null=False,blank=False)

    sectionCount = models.IntegerField(null=False,blank=False)

    questionCountSec_1 = models.IntegerField(null=False,blank=False)
    questionCountSec_2 = models.IntegerField(null=True,blank=True)
    questionCountSec_3 = models.IntegerField(null=True,blank=True)

    positivesPerQuestionSec_1 = models.IntegerField(null=False,blank=False)
    positivesPerQuestionSec_2 = models.IntegerField(null=True,blank=True)
    positivesPerQuestionSec_3 = models.IntegerField(null=True,blank=True)

    negativesPerQuestionSec_1 = models.IntegerField(null=False,blank=False)
    negativesPerQuestionSec_2 = models.IntegerField(null=True,blank=True)
    negativesPerQuestionSec_3 = models.IntegerField(null=True,blank=True)

    examDuration = models.IntegerField(null=False,blank=False)

    def __str__(self):
        return self.testCode + " - Config"

    class Meta:
        verbose_name = 'Question Configuration'
        verbose_name_plural = 'Question Configurations'



#########################QUESTION##MODEL##############################################################################



# models for storing questions for Configuration.

class QuestionModel(models.Model):

    test_code = models.ForeignKey('ConfigCreation',on_delete=models.CASCADE)

    sectionNumber = models.IntegerField(null=False,blank=False)
    questionNumber = models.IntegerField(null=False,blank=False)

    question = models.TextField(blank=False,null=False)

    option_1 = models.TextField(blank=False,null=False)
    option_2 = models.TextField(blank=False,null=False)
    option_3 = models.TextField(blank=False,null=False)
    option_4 = models.TextField(blank=False,null=False)

    isMultiCorrect = models.BooleanField(blank=False,null=True,default=False)

    ans_1 = models.BooleanField(blank=False,null=True,default=False)
    ans_2 = models.BooleanField(blank=False,null=True,default=False)
    ans_3 = models.BooleanField(blank=False,null=True,default=False)
    ans_4 = models.BooleanField(blank=False,null=True,default=False)

    def __str__(self):
        return self.test_code.testCode + '-Section-{}-Question-{}'.format(str(self.sectionNumber),str(self.questionNumber))

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
