# For dead code

########################################################################################################################
# FROM views.py
'''
def surveycompletion(request):
    survey_Id = request.session.get('survey_Id')
    #questions = Question.objects.filter(question_survey_Id=surveyid)

    #mclist = MCQuestion.objects.filter(question_survey_Id=survey_Id)
    #telist = TEQuestion.objects.filter(question_survey_Id=survey_Id)
    #cblist = CBQuestion.objects.filter(question_survey_Id=survey_Id)

    # Still need to get cross-Question table querying
    # for q in questions:
    #     qid = q.question_Id
    #
    #     if q.question_type == 'MC':
    #         qq = MCQuestion.objects.filter(question_Id=qid)
    #         mclist.append(qq)
    #
    #     if q.question_type == 'TE':
    #         qq = MCQuestion.objects.filter(question_Id=qid)
    #         telist.append(qq)
    #
    #     if q.question_type == 'CB':
    #         qq = MCQuestion.objects.filter(question_Id=qid)
    #         cblist.append(qq)
    #context = {'survey_Id': survey_Id, 'mclist': mclist, 'telist': telist, 'cblist': cblist}
    context = {'survey_Id': survey_Id}

    return render(
        request,
        'survey-completion.html',
        context
    )
'''

'''
# prints list of all survey objects
def index(request):
    user_surveys = Survey.objects.filter(creator_Id=request.user)

    if request.method == 'POST':
        form = SurveyForm(request.POST)

        if form.is_valid():
            survey = form.save(commit=False)
            survey.survey_Id = uuid.uuid4()
            survey.save()
            # return redirect(reverse('surveys:add_survey'))
            return redirect(reverse('surveys:detail', kwargs={'survey_Id': survey.survey_Id}))

    else:
        form = SurveyForm()

    return render(request, 'surveys/index.html', {'user_surveys': user_surveys})
'''

'''
# page of specific survey listing its questions
def detail(request, survey_Id):
    survey = get_object_or_404(Survey, survey_Id=survey_Id)

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            QUESTIONPAGES = {
                'MC': 'multiplechoice.html',
                'TE': 'textentry.html',
                'CB': 'checkbox.html',
            }
            nextpage = '/surveys/'

            question = form.save(commit=False)
            question.question_Id = uuid.uuid4()
            question.question_type = request.POST.get('question_type')
            # question.question_survey_Id = request.POST.get('question_survey_Id')
            type = request.POST.get('question_type')
            nextpage += QUESTIONPAGES[type]
            question.save()  # save to DB
            # return HttpResponseRedirect(nextpage)

            #if type is 'MC':
            #    return redirect(reverse('surveys:multiplechoice', kwargs={'survey_Id': survey.survey_Id}))
            #elif type is 'TE':
            #    return redirect(reverse('surveys:textentry', kwargs={'survey_Id': survey.survey_Id}))
            #else:
            #    return redirect(reverse('surveys:checkbox', kwargs={'survey_Id': survey.survey_Id}))


        # else:
        #    print(form.errors, len(form.errors))
    else:
        form = QuestionForm()

    # return render(request, 'surveys/add_question.html', {'survey': survey_Id})
    return render(request, 'surveys/detail.html', {'survey': survey})
'''

'''
def add_question(request, survey_Id):
    QUESTIONPAGES = {
        'MC': 'multiplechoice.html',
        'TE': 'textentry.html',
        'CB': 'checkbox.html',
    }
    nextpage = '/surveys/'

    question_form = QuestionForm()

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            # owningsurvey = request.
            # set_survey_foreign_key(owningsurvey)
            # https://chriskief.com/2013/05/24/django-form-wizard-and-getting-data-from-previous-steps/
            # https://docs.djangoproject.com/en/1.7/ref/contrib/formtools/form-wizard/
            question = form.save(commit=False)
            question.question_Id = uuid.uuid4()
            question.question_survey_Id = survey_Id

            nextpage += QUESTIONPAGES[request.POST.get('question_type')]
            question.save()  # save to DB
            # return HttpResponseRedirect(nextpage)
            return redirect(reverse('surveys:detail', args=(survey.survey_Id)))
    else:
        form = QuestionForm()

    return render(request, 'surveys/add_question.html', {'survey': survey_Id})


def new_question(request, survey_Id):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.set(question_survey_Id=survey_Id)
            nextpage += QUESTIONPAGES[request.POST.get('question_type')]
            question.save()  # save to DB
            return redirect(reverse('surveys:detail', args=(survey.survey_Id,)))
    else:
        form = QuestionForm()

    return render(request('add_question.html', context={'survey': survey.survey_Id, 'form': form}))


def delete_question(request, survey_Id):
    survey = get_object_or_404(Survey, survey_Id=survey_Id)
    # question = None
    try:
        # question = request.POST.get('question')
        question = survey.question_set.get(question_Id=request.POST['question_Id'])
    except (KeyError, Question.DoesNotExist):
        return render(request, 'surveys/detail.html', {
            'question': question,
            'error_message': "You did not select a valid question",
        })
    else:
        question.delete()
    return render(request, 'surveys/detail.html', {'survey': survey})


def delete_survey(request, survey_Id):
    survey = get_object_or_404(Survey, survey_Id=survey_Id)
    survey.delete()
    user_surveys = Survey.objects.filter(creator_Id=request.user)
    return render(request, 'surveys/index.html', {'user_surveys': user_surveys})
'''

'''
def multiplechoice(request, survey_Id):
    #return render(request('multiplechoice.html', context={'survey': survey.survey_Id, 'form': form}))
    return redirect(reverse('surveys:multiplechoice', args=(survey.survey_Id,)))

def textentry(request, survey_Id):
    return render(request('textentry.html', context={'survey': survey.survey_Id, 'form': form}))

def checkbox(request, survey_Id):
    return render(request('checkbox.html', context={'survey': survey.survey_Id, 'form': form}))
'''
########################################################################################################################

