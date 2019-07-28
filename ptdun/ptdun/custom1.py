# -*- coding: utf-8 -*-
# Copyright (c) 2015, jonathan and Contributors
# See license.txt
from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt, cstr
from frappe.desk.reportview import get_match_cond, get_filters_cond
from frappe.utils import nowdate

# test_records = frappe.get_test_records('testdoctype')

def set_purchase_receipt_per_billed(self, method):
	if self.docstatus == 1 or self.docstatus == 2:
		for d in self.items:
			if d.purchase_receipt:
				ref_doc_qty = flt(frappe.db.sql("""select ifnull(sum(qty), 0) from `tabPurchase Receipt Item`
				where parent=%s""", (d.purchase_receipt))[0][0])
				print 'ref_doc_qty=' + cstr(ref_doc_qty)
	
				billed_qty = flt(frappe.db.sql("""SELECT ifnull(sum(qty), 0) as billed_qty FROM `tabPurchase Invoice` si INNER JOIN `tabPurchase Invoice Item` it 
						ON si.name=it.parent where si.docstatus=1 and it.purchase_receipt=%s and si.name=%s""", (d.purchase_receipt, self.name))[0][0])
				#billed_qty = 100
				print 'billed_qty=' + cstr(billed_qty)

				per_billed = ((ref_doc_qty if billed_qty > ref_doc_qty else billed_qty)\
					/ ref_doc_qty)*100
				print 'per_billed=' + cstr(per_billed)

				doc = frappe.get_doc("Purchase Receipt", d.purchase_receipt)

				#frappe.throw(_("doc.per_billed = {0} per_billed = {1}").format(doc.per_billed, per_billed))

				if doc.per_billed < 100:
					doc.db_set("per_billed", "100")
					doc.set_status(update=True)

				if self.docstatus == 2:
					doc.db_set("per_billed", "0")
					doc.set_status(update=True)
@frappe.whitelist()
def set_per_billed_in_so_dn(doc, method):
	if doc.is_return:
		dn = ""
		for d in doc.items:
			if dn != d.delivery_note:
				dn = d.delivery_note
			else:
				continue
			if d.delivery_note and doc.is_return and doc.docstatus == 1:
				del_note = frappe.get_doc("Delivery Note",d.delivery_note)
				if not del_note.return_status and (0 < del_note.per_billed < 100.0):
					del_note.db_set("return_status", "To Return")

			elif d.delivery_note and doc.is_return and doc.docstatus == 2:
				ref_dn = frappe.get_doc("Delivery Note",d.delivery_note)

				ref_dn_qty = flt(frappe.db.sql("""select ifnull(sum(qty), 0) from `tabDelivery Note Item`
					where parent=%s""", (d.delivery_note))[0][0])

				return_dn_qty = flt(frappe.db.sql("""select ifnull(sum(it.qty), 0) from `tabDelivery Note` dln 
					INNER JOIN `tabDelivery Note Item` it 
					ON dln.name=it.parent where dln.docstatus=1 and dln.is_return and dln.return_against=%s""", (ref_dn.name))[0][0])
				if return_dn_qty:
					ref_dn_qty += return_dn_qty

				billed_qty = flt(frappe.db.sql("""SELECT ifnull(sum(qty), 0) as billed_qty FROM `tabSales Invoice` si INNER JOIN `tabSales Invoice Item` it 
					ON si.name=it.parent where si.docstatus=1 and it.delivery_note=%s and si.is_return != 1""", (d.delivery_note))[0][0])

				per_billed = ((ref_dn_qty if billed_qty > ref_dn_qty else billed_qty)/ ref_dn_qty)*100
		
				if (0 <= ref_dn.per_billed < 100.0) and per_billed >= 100.0 and doc.docstatus == 2:
					ref_dn.db_set("per_billed", "100")
					ref_dn.set_status(update=True)

					if ref_dn.return_status != "":
						ref_dn.db_set("return_status", "")
	elif doc.docstatus == 1:
		dn = ""
		so = ""
		for d in doc.items:
			if dn != d.delivery_note:
				dn = d.delivery_note
			else:
				continue

			if d.delivery_note:
				ref_dn = frappe.get_doc("Delivery Note",d.delivery_note)
				#frappe.msgprint(cstr(ref_dn.per_billed))
				if ref_dn.per_billed >= 100.0:
					continue

				ref_dn_qty = flt(frappe.db.sql("""select ifnull(sum(qty), 0) from `tabDelivery Note Item`
					where parent=%s""", (d.delivery_note))[0][0])

				return_dn_qty = flt(frappe.db.sql("""select ifnull(sum(it.qty), 0) from `tabDelivery Note` dln 
					INNER JOIN `tabDelivery Note Item` it 
					ON dln.name=it.parent where dln.docstatus=1 and dln.is_return and dln.return_against=%s""", (ref_dn.name))[0][0])
				if return_dn_qty:
					ref_dn_qty += return_dn_qty

				billed_qty = flt(frappe.db.sql("""SELECT ifnull(sum(qty), 0) as billed_qty FROM `tabSales Invoice` si INNER JOIN `tabSales Invoice Item` it 
					ON si.name=it.parent where si.docstatus=1 and it.delivery_note=%s and si.is_return != 1""", (d.delivery_note))[0][0])

				per_billed = ((ref_dn_qty if billed_qty > ref_dn_qty else billed_qty)/ ref_dn_qty)*100
				#frappe.msgprint(cstr(per_billed))
		
				if (0 <= ref_dn.per_billed < 100.0) and per_billed >= 100.0 and doc.docstatus == 1:
					ref_dn.db_set("per_billed", "100")
					ref_dn.db_set("return_status", "")
					ref_dn.set_status(update=True)
		for d in doc.items:
			if so != d.sales_order:
				so = d.sales_order
			else:
				continue

			if d.sales_order:
				ref_so = frappe.get_doc("Sales Order",d.sales_order)
				if ref_so.per_billed >= 100.0:
					continue

				ref_so_qty = flt(frappe.db.sql("""select ifnull(sum(qty)-sum(returned_qty), 0) from `tabSales Order Item`
					where parent=%s""", (d.sales_order))[0][0])

				billed_qty = flt(frappe.db.sql("""SELECT ifnull(sum(qty), 0) as billed_qty FROM `tabSales Invoice` si INNER JOIN `tabSales Invoice Item` it 
					ON si.name=it.parent where si.docstatus=1 and it.sales_order=%s and si.is_return != 1""", (d.sales_order))[0][0])

				per_billed = ((ref_so_qty if billed_qty > ref_so_qty else billed_qty)/ ref_so_qty if ref_so_qty else 1.0)*100
		
				if (0 <= ref_so.per_billed < 100.0) and per_billed >= 100.0 and doc.docstatus == 1:
					ref_so.db_set("per_billed", "100")
					ref_so.set_status(update=True)

@frappe.whitelist()
def set_per_delivered_in_so(self, method):
	if not self.is_return:
		return
	elif not self.no_replacement:
		return

	ref_dn = frappe.get_doc(self.doctype,self.return_against)
	per_delivered = 100.0

	if self.docstatus == 1 or self.docstatus == 2:
		so = ""
		for d in self.items:
			if d.against_sales_order: #get ref sales order
				if so != d.against_sales_order:
					so = d.against_sales_order
				else:
					continue

				ref_so = frappe.get_doc("Sales Order", d.against_sales_order)

				#for so_item in ref_so.items:
				#	if so_item.qty != so_item.delivered_qty + so_item.returned_qty:
				#		per_delivered = ref_so.per_delivered

				so_qty = flt(frappe.db.sql("""select ifnull(sum(qty)-sum(returned_qty), 0) from `tabSales Order Item`
					where parent=%s""", (ref_so.name))[0][0])

				delivered_qty = flt(frappe.db.sql("""SELECT ifnull(sum(qty), 0) as delivered_qty FROM `tabDelivery Note` si INNER JOIN `tabDelivery Note Item` it 
					ON si.name=it.parent where si.docstatus=1 and it.against_sales_order=%s and si.is_return != 1""", (ref_so.name))[0][0])

				per_delivered = ((so_qty if delivered_qty > so_qty else delivered_qty)/ so_qty if so_qty else 1.0)*100

				if per_delivered >= 100.0:
					ref_so.db_set("per_delivered", "100")
					ref_so.set_status(update=True)

				billed_qty = flt(frappe.db.sql("""SELECT ifnull(sum(qty), 0) as billed_qty FROM `tabSales Invoice` si INNER JOIN `tabSales Invoice Item` it 
					ON si.name=it.parent where si.docstatus=1 and it.sales_order=%s and si.is_return != 1""", (ref_so.name))[0][0])

				per_billed = ((so_qty if billed_qty > so_qty else billed_qty)/ so_qty if so_qty else 1.0)*100
		
				if (0 <= ref_so.per_billed < 100.0) and per_billed <= 100.0 and self.docstatus == 2:
					ref_so.db_set("per_billed", per_billed)
					ref_so.set_status(update=True)



		ref_dn_qty = flt(frappe.db.sql("""select ifnull(sum(qty), 0) from `tabDelivery Note Item`
		where parent=%s""", (ref_dn.name))[0][0])
		#print 'ref_dn_qty=' + cstr(ref_dn_qty)

		billed_qty = flt(frappe.db.sql("""SELECT ifnull(sum(qty), 0) as billed_qty FROM `tabSales Invoice` si INNER JOIN `tabSales Invoice Item` it 
				ON si.name=it.parent where si.docstatus=1 and it.delivery_note=%s and si.is_return != 1""", (ref_dn.name))[0][0])
		#billed_qty = 100
		#print 'billed_qty=' + cstr(billed_qty)

		per_billed = ((ref_dn_qty if billed_qty > ref_dn_qty else billed_qty)/ ref_dn_qty if ref_dn_qty else 1.0)*100
		#print 'per_billed=' + cstr(per_billed)

		#frappe.msgprint(_("billed_qty = {0}, pref_dn_qty = {1}, per_billed = {2}").format(billed_qty, ref_dn_qty, per_billed))

		if (0 <= ref_dn.per_billed < 100.0) and per_billed >= 100.0:
			ref_dn.db_set("per_billed", "100")
			ref_dn.db_set("return_status", "")
			self.db_set("return_status", "")
			ref_dn.set_status(update=True)
		

