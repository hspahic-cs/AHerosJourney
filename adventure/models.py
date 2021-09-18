from typing import Optional
from django.db.models.fields.related import ManyToManyField
from django.db import models

'''
Model Heirarchy: 
( ChoicePossibilities --> Choices --> Videos --> Chunk  ) 
'''

'''
Choice Model: 
A model to reperesent each choice in the show (Ex: LOH -> Leader Of Heroes, DRM -> Dream, etc.)

(field: Char)      choiceName          --> Name of the choice object needed to be chosen 
(field: ManyToOne) choicePossibilities --> A queryset of all possibilities for this particular choice
'''

class Choice(models.Model):
    choiceName = models.CharField(default="LOH", max_length=3)    

    def __str__(self):
        return self.choiceName

'''
Video Model: 
A model to represent each particular video in the show. The particular video to be sent is dependent on what *requiredChoices* the user has made.

(field: Char)       name             --> Name representing the particular video (Ex: 1a, 1b, etc.)
(field: ManyToMany) requriredChoices --> The names of the choices necessary to select the correct version of this video
'''

class Video(models.Model):
    name = models.CharField(default="Scene Name", max_length = 6)
    requiredChoices = ManyToManyField("Choice", blank=True)

    def __str__(self):
        requiredChoices_associated = ", ".join(str(choice) for choice in self.requiredChoices.all())
        return "{} | {}".format(self.name, requiredChoices_associated)


'''
Chunk Model:
A model to represent every collection of videos before a necessary choice.

(field: ManyToMany) requiredVidoes --> Collection of videos before the user makes their next choice.
(field: ManyToMany) nextChoice     --> The reference of the next *Choice* that follows this chunk.

Note: if nextChoice == null --> move to next scene
'''

class Chunk(models.Model):
    requiredVideos = ManyToManyField("Video")
    nextChoice = ManyToManyField("Choice")
    chunkNum = models.IntegerField(default=1)
    binaryChoice = models.BooleanField(blank=True, default=True);

    def __str__(self):
        chainedVideos = ", ".join(str(vid.name) for vid in self.requiredVideos.all())
        return "{} | {}".format(self.chunkNum, chainedVideos)

'''
ChoicePossibility Model:
A model to represent a possible choice the user can make for each *Choice* scene. (Ex: LOH may have (Hero1, Hero2, Hero3, etc.) as ChoicePossibility's)

(field: CharField) imgPath    --> Path to the image representation of *ChoicePossibility*
(field: CharField) optionName --> Name of the particular *ChoicePossibility* (Ex: "Hero1" or "Hero2")
(field: ManyToOne) containter --> Assigns each *ChoicePossibility* to a particular *Choice* to be referenced in the *Choice* model
'''

class ChoicePossibility(models.Model):
    imgPath = models.CharField(default="imgs/icons/", max_length=30)
    optionName = models.CharField(default="CHOICE NAME", max_length=40)
    container = models.ForeignKey(to=Choice, on_delete=models.CASCADE)

    def __str__(self):
        return self.optionName

