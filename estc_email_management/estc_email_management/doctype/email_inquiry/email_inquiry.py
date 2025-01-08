# Copyright (c) 2025, Tes Pheakdey and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today

class EmailInquiry(Document):
	def validate(self):
		self.ip_address =  frappe.local.request_ip 
		
	def after_insert(self):
		# check email count
		sql = "select count(name) as total from `tabEmail Inquiry` where date(send_date)=date(%(date)s) and website_domain=%(website_domain)s"
		data = frappe.db.sql(sql,{"website_domain":self.website_domain,"date":today()},as_dict=1)
		if data:
			if data[0].get("total",0)<=frappe.get_cached_value("Website Domain",self.website_domain,"limit_email_send_per_day"):
				self.submit()
			else:
				frappe.msgprint("This website domain is reach daily limit")
	