import os

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required

import misaka as m
from markdown import Markdown


CORRECT_DEMANDS = {
  1: 90,
  2: 100, 
  3: 205
}


def render_md(request, mdfilepath, context=None):
  if not context:
    context = {}
  content = ""
  print os.path.abspath(".")
  with file(mdfilepath, "r") as f:
    s = f.read()
    content = m.html(s)
    #m = Markdown()
    #content = m.convert(s)
  context['content'] = content
  return render(request, "home/md_template.html", context)

def render_page(request, pagename, context=None):
  htmlfilepath = "./templates/home/%s.html" % pagename
  print htmlfilepath
  if os.path.exists(htmlfilepath):
    return render_to_response(
        'home/%s.html'%pagename, 
        context_instance=RequestContext(request))

  mdfilepath = "./templates/home/%s.md" % pagename
  print mdfilepath
  return render_md(request, mdfilepath, context)

def index(request):
  return page(request, "index")

def page(request, pagename=None):
  try:
    return render_page(request, pagename)
  except Exception as e:
    return error(request, 'Could not find page', str(e))

# This should be a context manager
def error(request, title='There was an error', msg=""):
  context = {'title': 'There was an error',  'message': msg }
  return render(request, "error.html", context)


def info(request):
  return render_md(request, "./templates/home/info.md")

def prediction(request):
  return render_md(request, "./templates/home/prediction.md")

def visualization(request):
  return render_md(request, "./templates/home/visualization.md")

@login_required
def submit(request):
  if request.method == 'POST':
    uid = request.POST.get('uid', None)
    submission = request.POST.get('submission', None)
    demands = parse(submission)
    score = compute_score(demands)

    # TODO: store the score
  return render(request, "home/index_template.html", {'content': score})

def compute_score(demands):
  sqerrs = []
  for key in CORRECT_DEMANDS:
    trueval = CORRECT_DEMANDS[key]
    if key in  demands:
      estval = demands[key]
      sqerrs.append(float(trueval - estval) ** 2)

  return sum(sqerrs) ** 0.5

def parse(submission=""):
  """
  ARGS:
  submission is as string

  RETURN:
  dictionary of location -> demand number 
  """
  demands = {}
  try:
    lines = submission.split("\n")
    for line in lines:
      line = line.strip()
      if not line: continue
      tokens = line.split(" ")
      locid = int(tokens[0])
      demand = int(tokens[1])
      demands[locid] = demand
    return demands
  except:
    return {}
