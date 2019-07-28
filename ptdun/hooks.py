# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "ptdun"
app_title = "ptdun"
app_publisher = "jonathan"
app_description = "ptdun"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "jof2jc@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/ptdun/css/ptdun.css"
# app_include_js = "/assets/ptdun/js/ptdun.js"

# include js, css files in header of web template
# web_include_css = "/assets/ptdun/css/ptdun.css"
# web_include_js = "/assets/ptdun/js/ptdun.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

fixtures = [  
		{
			"doctype": "Custom Field",
		        "filters": {
        				"dt": ["in", ["Journal Entry"]],
				        "fieldname": ["in", ["expenses","sc_expenses","cash_bank_account"]]
        		}
    		}
]
# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "ptdun.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "ptdun.install.before_install"
# after_install = "ptdun.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "ptdun.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }
doc_events = {
    "Sales Invoice": {
	"on_submit": "ptdun.ptdun.custom1.set_per_billed_in_so_dn",
	"on_cancel": "ptdun.ptdun.custom1.set_per_billed_in_so_dn"
    },
    "Delivery Note": {
	"on_submit": "ptdun.ptdun.custom1.set_per_delivered_in_so",
	"on_cancel": "ptdun.ptdun.custom1.set_per_delivered_in_so"
    }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"ptdun.tasks.all"
# 	],
# 	"daily": [
# 		"ptdun.tasks.daily"
# 	],
# 	"hourly": [
# 		"ptdun.tasks.hourly"
# 	],
# 	"weekly": [
# 		"ptdun.tasks.weekly"
# 	]
# 	"monthly": [
# 		"ptdun.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "ptdun.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "ptdun.event.get_events"
# }

