# from typing_extensions import Required
from django.db.models.fields import AutoField
from adventure.forms import ChoiceForm
from django.http.response import Http404
from django.shortcuts import render, redirect

from .models import ChoicePossibility, Chunk, Choice
from .forms import ChoiceForm

# Create your views here.
# Check url paths in "TheHeroesJourney/TheHeroesJourney/urls.py"

'''
home view:
Intro page to the show 
'''
def home(request):
    return render(request, 'home.html', {})

'''
crossroads view: 
View which displays all the videos in each *Chunk* model

(int) chunk_id --> id of the current chunk
'''
def crossroads(request, chunk_id):
    
    # Checks if Chunk with chunk_id exists, else throws error
    if(chunk_id == 10):
        if(request.COOKIES.get("WCH") == "Sneak"):
            chunk = Chunk.objects.filter(chunkNum = chunk_id).get(binaryChoice = False)
        else:
            chunk = Chunk.objects.filter(chunkNum = chunk_id).get(binaryChoice = True)        
        
    elif(chunk_id == 11):
        if(request.COOKIES.get("TOK") == "Kraken"):
            chunk = Chunk.objects.filter(chunkNum = chunk_id).get(binaryChoice = True)
        else:
            chunk = Chunk.objects.filter(chunkNum = chunk_id).get(binaryChoice = False)    

    else:
        try: 
            chunk = Chunk.objects.get(chunkNum = chunk_id)
        except:
            raise Http404("Something went wrong!")

    # Variable that will hold str filepaths for each video in chunk 
    filePaths = []
    
    # Constructs filepath based on *Video* model fields
    for video in chunk.requiredVideos.all():
        
        # Particular Scene
        if(chunk_id < 12):
            scene = "S" + video.name[0] + "/"
        else:
            scene = "S" + video.name[0] + video.name[1] + "/"
            
        # NOTE: imgPath is for the first scene of each video, to prevent breaks between the videos

        # If *Video* has choices --> get every value of each *Choice* & combine them into single string
        # Combine all parts of vid & img path, to reference particular video (Ex: "videos/S1/1e/Norrun.mp4" since LOH is a requiredChoice)
        if(video.requiredChoices.all()):
            currentChoice = ""
            for choice in video.requiredChoices.all().order_by('choiceName'):
                currentChoice += request.COOKIES.get(choice.choiceName)

            # Video Reference to 2n
            if(video.name == "2n"):
                if(request.COOKIES.get('CPV') == "Freddick"):
                    if(request.COOKIES.get('SOC') == "Summit"):
                        vidPath = ("videos/S2/2n/2n2.mp4")
                        imgPath = ("imgPath/S2/2n/2n2.png")
                    else:
                        vidPath = ("videos/S2/2n/2n4.mp4")
                        imgPath = ("imgPath/S2/2n/2n4.png")
                else: 
                    if(request.COOKIES.get('CPV') == "Summit"):
                        vidPath = ("videos/S2/2n/2n1.mp4")
                        imgPath = ("imgPath/S2/2n/2n1.png")
                    else:
                        vidPath = ("videos/S2/2n/2n3.mp4")
                        imgPath = ("imgPath/S2/2n/2n3.png")

            elif(video.name == "5e"):
                if(request.COOKIES.get('DRM') == "Aquayna"):
                    vidPath = ("videos/S5/5e/Aquayna.mp4")
                    imgPath = ("imgPath/S5/5e/Aquayna.png")

                else:
                    vidPath = ("videos/S5/5e/Norrun.mp4")
                    imgPath = ("imgPath/S5/5e/Norrun.png")

            else: 
                vidPath = ("videos/" + scene + video.name + "/" + currentChoice + ".mp4")
                imgPath = ("imgs/" +  scene + video.name + "/" + currentChoice + ".jpg")

        # If no choices, just reference direct video & image of *Video*
        else:
            imgPath = ("imgs/" + scene + video.name + ".jpg")
            vidPath = ("videos/" + scene + video.name + ".mp4")

        # Adds paths as a tuple to filePaths
        filePaths.append((vidPath, imgPath)) 
    
    # Gets the choice after *Chunk* using (nextChoice field) --> must do for loop b/c nextChoice is ManyToManyField but will always only have 1 choice\
    for choice in chunk.nextChoice.all():
        nextChoice = choice.choiceName 

    # Renders site with all necessary variables 
    return render(request, 'crossroads.html', {'filePaths': filePaths, 'nextChoice': nextChoice, 'chunk_id': chunk_id,})

'''
choice view: 
View that renders ChoicePossibilities into a form, to be selected by user

(int) chunk_id    --> id of following chunk
(str) choice_name --> name of the choice to be selected
'''
def choice(request, chunk_id, choice_name):
    #Gets a reference to every *ChoicePossibility* in *Choice* 
    choicePossibilities = Choice.objects.get(choiceName=choice_name).choicepossibility_set.all()
    numChoices = choicePossibilities.count()

    #If form is submitted --> redirect the site to the next chunk, and set user's cookie for the *Choice* to their selected *ChoicePossibility*
    if request.method == "POST":
        response = redirect('crossroads', chunk_id=chunk_id)
        response.set_cookie(choice_name, request.POST['path'])
        return response

    #Else keep rendering the form with necessary variables
    return render(request, 'choice.html', {"chunk_id": chunk_id, "choice_name": choice_name, "choicePossibilities": choicePossibilities, 'numChoices': numChoices})
 
def ending(request):
    return render(request, 'ending.html')

def reward(request):
    CPLReward = False;
    MRLReward = False;

    CPL = request.COOKIES.get("CPL")
    END = request.COOKIES.get("END")

    if((CPL == "R&F" and END == "Freddick") or (CPL == "A&F" and END == "Hayson") or (CPL == "R&H" and END == "Farfrum") or (CPL == "A&H" and END == "Pacrod")
            or (CPL == "A&H" and END == "Norrun") or  (CPL == "R&H" and END == "Aquayna") or (CPL == "A&F" and END == "Reyla") or (CPL == "R&H" and END == "Iyew")):
        CPLReward = True
    
    if(request.COOKIES.get("MRL") == "Divided"):
        MRLReward = True
        
    return render(request, 'reward.html', {"CPLReward" : CPLReward, "MRLReward" : MRLReward})
