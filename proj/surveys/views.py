from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Survey, Question, MCQuestion, TEQuestion, CBQuestion, ResponseTE
from .forms import QuestionForm, MCQuestionForm, TEQuestionForm, CBQuestionForm, SurveyForm, TakeSurveyForm
from django.urls import reverse, resolve
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

import json
import uuid
from json import JSONEncoder


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)


# Create your views here.
def home(request):
    return render(
        request,
        'home.html',
        context={})


@login_required
def index(request):
    num_users = User.objects.all().count()
    surveys = Survey.objects.filter(creator_Id=request.user.pk)
    creator = User.objects.get(username=request.user.username)
    survey_list = Survey.objects.filter(creator_Id=creator)
    form = SurveyForm(initial={'creator_Id': request.user.pk})

    if request.method == 'POST':
        if 'remove' in request.POST:
            try:
                s = Survey.objects.get(survey_Id=request.POST['remove'])
            except:
                s = None
            if s: s.delete()
        else:
            form = SurveyForm(request.POST)
            if form.is_valid():
                s = form.save(commit=False)
                s.survey_Id = uuid.uuid4()
                s.save()

    return render(
        request,
        'index.html',
        context={'form': form, 'num_users': num_users, 'surveys': surveys, 'userID': creator})

# No longer using any login view functions
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        # form2 = UserForm(request.POST) ###

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')

            user = authenticate(username=username, password=raw_password)
            # form2.fields['user_Id'] = request.user ### this gives username, not UUID
            login(request, user)
            return redirect(reverse('surveys:index'))
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


### VIEWS FOR SURVEY MAKING ###
@login_required
def editsurvey(request, survey_Id):
    #s = None
    #if 'id' in request.GET: request.session['survey'] = request.GET['id']
    #if 'survey' in request.session:
    if not survey_Id:
        #try:
            #sid = request.session['survey']
        #    s = Survey.objects.get(survey_Id=survey_Id)
        #except:
        return HttpResponseRedirect('/surveys')

    #else: return HttpResponseRedirect('/surveys')

    if request.method == 'POST' and 'remove' in request.POST:
        # try:
        #     MCQuestion.objects.get(question_Id=request.POST['remove']).delete()
        # except:
        #     pass
        try:
            #TEQuestion.objects.get(question_Id=request.POST['remove']).delete()
            #question = get_object_or_404(Survey, survey_Id=survey_Id)
            question = Question.objects.get(question_Id=request.POST['remove'])
            question.delete()
        except:
            pass
        # try:
        #     CBQuestion.objects.get(question_Id=request.POST['remove']).delete()
        # except:
        #     pass

    return render(
        request,
        'edit.html',
        context={
            'survey_Id': survey_Id,
            'mcquestions': MCQuestion.objects.filter(question_survey_Id=survey_Id),
            'tequestions': TEQuestion.objects.filter(question_survey_Id=survey_Id),
            'cbquestions': CBQuestion.objects.filter(question_survey_Id=survey_Id),
        }
    )


def newquestion(request):
    QUESTIONPAGES = {
        'MC': 'multiplechoice.html',
        'TE': 'textentry.html',
        'CB': 'checkbox.html',
    }
    nextpage = '/surveys/'

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            # owningsurvey = request.
            # set_survey_foreign_key(owningsurvey)
            # https://chriskief.com/2013/05/24/django-form-wizard-and-getting-data-from-previous-steps/
            # https://docs.djangoproject.com/en/1.7/ref/contrib/formtools/form-wizard/

            nextpage += QUESTIONPAGES[request.POST.get('question_type')]
            form.save()  # save to DB
            return HttpResponseRedirect(nextpage)
    else:
        form = QuestionForm()

    return render(
        request,
        'newquestion.html',
        context={'form': form},
    )


@login_required
def multiplechoice(request, survey_Id):
    if request.method == 'POST':
        form = MCQuestionForm(request.POST)
        if form.is_valid():
            survey = get_object_or_404(Survey, survey_Id=survey_Id)
            q = form.save(commit=False)
            q.question_Id = uuid.uuid4()
            q.question_survey_Id = survey
            q.save()
            return redirect(reverse('surveys:editsurvey', args=(survey.survey_Id,)))
    else:
        form = MCQuestionForm(initial={'question_survey_Id': survey_Id})

    return render(
        request,
        'multiplechoice.html',
        context={'form': form},
    )


@login_required
def textentry(request, survey_Id):
    if request.method == 'POST':
        form = TEQuestionForm(request.POST)
        if form.is_valid():
            survey = get_object_or_404(Survey, survey_Id=survey_Id)
            q = form.save(commit=False)
            q.question_Id = uuid.uuid4()
            q.question_survey_Id = survey
            q.save()
            return redirect(reverse('surveys:editsurvey', args=(survey.survey_Id,)))

    else:
        form = TEQuestionForm(initial={'question_survey_Id': survey_Id})

    return render(
        request,
        'textentry.html',
        context={'form': form},
    )


@login_required
def checkbox(request, survey_Id):
    if request.method == 'POST':
        form = CBQuestionForm(request.POST)
        if form.is_valid():
            survey = get_object_or_404(Survey, survey_Id=survey_Id)
            q = form.save(commit=False)
            q.question_Id = uuid.uuid4()
            q.question_survey_Id = survey
            q.save()
            return redirect(reverse('surveys:editsurvey', args=(survey.survey_Id,)))
    else:
        form = CBQuestionForm(initial={'question_survey_Id': survey_Id})

    return render(
        request,
        'checkbox.html',
        context={'form': form},
    )


### VIEWS FOR SURVEY TAKING ###
@login_required
def takesurvey(request):
    if request.method == 'POST':
        form = TakeSurveyForm(request.POST, user=request.user)
        if form.is_valid():
            request.session['survey_to_take'] = getattr(form.cleaned_data.get('survey_to_take'), 'survey_Id').hex
            return HttpResponseRedirect('/surveys/survey-completion')
    else:
        form = TakeSurveyForm(user=request.user)
    return render(
        request,
        'takesurvey.html',
        {'form': form}
    )


@login_required
def surveycompletion(request):
    surveyid = request.session.get('survey_to_take')
    questions = Question.objects.filter(question_survey_Id=surveyid)
    mcquestions = MCQuestion.objects.filter(question_survey_Id=surveyid)
    tequestions = TEQuestion.objects.filter(question_survey_Id=surveyid)
    cbquestions = CBQuestion.objects.filter(question_survey_Id=surveyid)
    print(surveyid)
    mclist = []
    telist = []
    cblist = []
    qlist = []
    # Still need to get cross-Question table querying
    for q in questions:
        print(q.questionID)
        qlist.append(q)
    for q in mcquestions:
        qlist.append(q)
    for q in tequestions:
        qlist.append(q)
    for q in cbquestions:
        qlist.append(q)

    for q in qlist:
        print("questionID: ", end="")
        print(q.question_Id, "\n", end="")
        print("     question text: ", end="")
        print(q.question_text)
    if q in mcquestions:
        print("----MC----")
    elif q in tequestions:
        print("----TE----")
    elif q in cbquestions:
        print("----CB---")

    return render(request,
                  'survey-completion.html',
                  {'surveyid': surveyid, 'allQ': qlist, 'mclist': mcquestions, 'telist': tequestions,
                   'cblist': cbquestions}
                  )
