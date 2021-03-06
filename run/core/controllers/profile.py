#!/usr/bin/env python3


from flask import abort, Blueprint, redirect, render_template, request, session, url_for

from core.models import model


controller = Blueprint("profile", __name__, url_prefix="/profile")

@controller.route("/", methods=["GET"])
def show_profile():
    # In session (user signed in)
    if "username" in session:
        return render_template("profile.html", \
                                username=session["username"], \
                                first_name=session["first_name"], \
                                last_name=session["last_name"], \
                                num_posts=model.get_num_posts(session["username"]), \
								num_reposts=model.get_num_reposts(session["username"]), \
                                posts=model.get_posts(session["username"]), \
                                reposts=model.get_reposts(session["username"]), \
                                title="Profile")
    # Out of session (user not signed in)
    else:
        return redirect(url_for("main.show_main"))