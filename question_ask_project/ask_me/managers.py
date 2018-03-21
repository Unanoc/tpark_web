# from django.db import models
#
#
#
# class QuestionManager(models.Model):
#
#     def get_hot(self):
#         return self.all().order_by('rating').reverse()
#
#     def get_new(self):
#         return self.all().order_by('date').reverse()
#
#     def get_by_id(self, question_id):
#         return self.all().filter(id=question_id)
#
#
# class AnswerManager(models.Model):
#
#     def get_answers(self):
#         return self.all().order_by('date').reverse()
#
#
# class TagManager(models.Model):
#     def get_by_tag(self, tag_name):
#         return self.filter(title=tag_name).first().questions.all().order_by('date').reverse()