"""
Simple Flask web site 
"""

import flask
from flask import request  # Data from a submitted form
from flask import url_for
from flask import jsonify # For AJAX transactions

import json
import logging
import argparse  # For the vocabulary list
import sys

# Our own modules
from letterbag import LetterBag
from vocab import Vocab
from jumble import jumbled

###
# Globals
###
app = flask.Flask(__name__)
import CONFIG
app.secret_key = CONFIG.secret_key  # Should allow using session variables

#
# One shared 'Vocab' object, read-only after initialization,
# shared by all threads and instances.  Otherwise we would have to
# store it in the browser and transmit it on each request/response cycle, 
# or else read it from the file on each request/responce cycle,
# neither of which would be suitable for responding keystroke by keystroke.

WORDS = Vocab( CONFIG.vocab )

###
# Pages
###

@app.route("/")
@app.route("/index")
def index():
  flask.g.vocab = WORDS.as_list();
  flask.session["target_count"] = min( len(flask.g.vocab), CONFIG.success_at_count )
  flask.session["jumble"] = jumbled(flask.g.vocab, flask.session["target_count"])
  flask.session["matches"] = [ ]
  app.logger.debug("Session variables have been set")
  assert flask.session["matches"] == [ ]
  assert flask.session["target_count"] > 0
  app.logger.debug("At least one seems to be set correctly")
  return flask.render_template('vocab.html')


@app.route("/success")
def success():
  return flask.render_template('success.html')

#######################
# AJAX request handlers 
#   These return JSON, rather than rendering pages. 
#######################
@app.route("/_auto_check")
def auto_check():
  """
  User has entered new input, check for
  the input in the jumble and vocabulary list.
  Respond depending on whether the word is in the
  vocab list, made from jumbled letters and not an
  already found word.
  """
  text = request.args.get("text", type=str)
  jumble = flask.session["jumble"]
  matches = flask.session.get("matches", []) # Default to empty list
  in_jumble = LetterBag(jumble).contains(text) #can text be formed from jumble
  matched = WORDS.has(text) #is text in the word list
  already_found = text in matches #has text already been found

  ## Respond appropriately 
  if matched and in_jumble and not already_found:
    ## they found a new word
    new_word = True
    matches.append(text) #add word to list of matches
    flask.session["matches"] = matches
  else:
    ## they didn't find a new word
    new_word = False
  
  done = len(matches) >= flask.session["target_count"] #should the game end 
  rslt = { "found_word": new_word, "already_found": already_found, "in_jumble": in_jumble, "done": done }   
  return jsonify(result=rslt)


#######################
# Form handler.  
# currently unused, it was replaced
# by a json request handler
#######################
@app.route("/_check", methods = ["POST"])
def check():
  """
  User has submitted the form with a word ('attempt')
  that should be formed from the jumble and on the
  vocabulary list.  We respond depending on whether
  the word is on the vocab list (therefore correctly spelled),
  made only from the jumble letters, and not a word they
  already found.
  """
  app.logger.debug("Entering check")

  ## The data we need, from form and from cookie
  text = request.form["attempt"]
  ## for AJAX: text = request.args.get("text", type=str)
  jumble = flask.session["jumble"]
  matches = flask.session.get("matches", []) # Default to empty list

  ## Is it good? 
  in_jumble = LetterBag(jumble).contains(text)
  matched = WORDS.has(text)

  ## Respond appropriately 
  if matched and in_jumble and not (text in matches):
    ## Cool, they found a new word
    matches.append(text)
    flask.session["matches"] = matches
  elif text in matches:
    flask.flash("You already found {}".format(text))
  elif not matched:
    flask.flash("{} isn't in the list of words".format(text))
  elif not in_jumble:
    flask.flash('"{}" can\'t be made from the letters {}'.format(text,jumble))
  else:
    app.logger.debug("This case shouldn't happen!")
    assert False  # Raises AssertionError

  ## Choose page:  Solved enough, or keep going? 
  if len(matches) >= flask.session["target_count"]:
    return flask.redirect(url_for("success"))
  else:
    return flask.redirect(url_for("keep_going"))


#################
# Functions used within the templates
#################

@app.template_filter( 'filt' )
def format_filt( something ):
    """
    Example of a filter that can be used within
    the Jinja2 code
    """
    return "Not what you asked for"
  
###################
#   Error handlers
###################
@app.errorhandler(404)
def error_404(e):
  app.logger.warning("++ 404 error: {}".format(e))
  return render_template('404.html'), 404

@app.errorhandler(500)
def error_500(e):
   app.logger.warning("++ 500 error: {}".format(e))
   assert app.debug == False #  I want to invoke the debugger
   return render_template('500.html'), 500

@app.errorhandler(403)
def error_403(e):
  app.logger.warning("++ 403 error: {}".format(e))
  return render_template('403.html'), 403



#############

# Set up to run from cgi-bin script, from
# gunicorn, or stand-alone.
#

if __name__ == "__main__":
    # Standalone. 
    app.debug = True
    app.logger.setLevel(logging.DEBUG)
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
else:
    # Running from cgi-bin or from gunicorn WSGI server, 
    # which makes the call to app.run.  Gunicorn may invoke more than
    # one instance for concurrent service.
    #FIXME:  Debug cgi interface 
    app.debug=False

