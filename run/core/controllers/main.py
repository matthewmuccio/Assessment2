#!/usr/bin/env python3


from flask import abort, Blueprint, redirect, render_template, request, session, url_for

from core.models import model


controller = Blueprint("main", __name__, url_prefix="/")

# Shows the feed page (if user is in session), or the signup page (if user is not in session).
@controller.route("/", methods=["GET", "POST"])
def show_main():
	# Feed page (in session - user signed in)
	if "username" in session:
		# GET request
		if request.method == "GET":
			return render_template("feed.html", \
									username=session["username"], \
									first_name=session["first_name"], \
									last_name=session["last_name"],
									num_posts=model.get_num_posts(session["username"]), \
									num_reposts=model.get_num_reposts(session["username"]), \
									posts=model.get_all_posts(), \
									title="Feed")
		# POST request
		else:
			# Clicking post button.
			if "post-button" in request.form:
				content = request.form["content"]
				# If the post is greater than 280 characters or has 0 characters (it is invalid).
				if len(content) > 280 or len(content) == 0:
					return render_template("feed.html", \
										username=session["username"], \
										first_name=session["first_name"], \
										last_name=session["last_name"],
										num_posts=model.get_num_posts(session["username"]), \
										num_reposts=model.get_num_reposts(session["username"]), \
										posts=model.get_all_posts(), \
										content=content, \
										error="e", \
										title="Feed")
				# If the post is fewer than 280 characters (it is valid).
				else:
					model.add_new_post(session["username"], content)
					return render_template("feed.html", \
											username=session["username"], \
											first_name=session["first_name"], \
											last_name=session["last_name"],
											num_posts=model.get_num_posts(session["username"]), \
											num_reposts=model.get_num_reposts(session["username"]), \
											posts=model.get_all_posts(), \
											title="Feed")
			# Clicking repost button.
			elif "repost-button" in request.form:
				post_id = request.form["post-id"]
				model.add_new_repost(session["username"], post_id)
				return render_template("feed.html", \
											username=session["username"], \
											first_name=session["first_name"], \
											last_name=session["last_name"],
											num_posts=model.get_num_posts(session["username"]), \
											num_reposts=model.get_num_reposts(session["username"]), \
											posts=model.get_all_posts(), \
											title="Feed")
	# Signup page (out of session - user not signed in)
	else:
		# GET request
		if request.method == "GET":
			return render_template("signup.html")
		# POST request
		else:
			# Accesses current form data (data transmitted in a POST request).
			username = request.form["username"]
			first_name = request.form["first-name"]
			last_name = request.form["last-name"]
			password1 = request.form["password1"]
			password2 = request.form["password2"]
			# If the passwords the user entered match.
			if password1 == password2:
				# Attempts to create an account with the entered username and password.
				response = model.create_account(username, password1, first_name, last_name)
				# If the user's account has been successfully created.
				if "Success" in response:
					session["username"] = username
					session["first_name"] = first_name
					session["last_name"] = last_name
					return render_template("feed.html", \
											username=username, \
											first_name=first_name, \
											last_name=last_name, \
											num_posts=model.get_num_posts(session["username"]), \
											num_reposts=model.get_num_reposts(session["username"]), \
											title="Feed")
				# If there was an issue creating the account (username already exists, account already exists, or username was invalid).
				else:
					return render_template("signup.html", response=response)
			# If the passowrds the user entered do not match.
			else:
				return render_template("signup.html", response=["Passwords did not match."])

# Handles signing out the user and removing them from the session.
@controller.route("/signout", methods=["GET"])
def signout():
	# In session (user signed in)
	if "username" in session:
		session.pop("username", None)
		session.pop("first_name", None)
		session.pop("last_name", None)
		return redirect(url_for("main.show_main"))
	# Out of session (user not signed in)
	else:
		return redirect(url_for("main.show_main"))

@controller.route("/base", methods=["GET"])
def show_base():
	return render_template("base.html", \
								username=session["username"], \
								first_name=session["first_name"], \
								last_name=session["last_name"],
								num_posts=model.get_num_posts(session["username"]), \
								num_reposts=model.get_num_reposts(session["username"]), \
								title="Base")

# Handles page requests for non-existent pages (404 errors).
@controller.route("/<path:path>", methods=["GET"])
def show_404(path):
	if "username" in session:
		return redirect(url_for("main.show_main"))
	else:
		abort(404)

@controller.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404