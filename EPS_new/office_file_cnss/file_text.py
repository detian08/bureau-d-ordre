import xlwt

from xlsxwriter.workbook import Workbook

from cStringIO import StringIO
import calendar

# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import base64
from openerp import models, fields, api, _
import time
from datetime import datetime
from openerp.osv import  osv


class inventory_txt_extended(models.Model):

	_name= "txt.extended"

	excel_file = fields.Binary('Telecharger teledeclaration CNSS')

	file_name = fields.Char('txt File', size=64)
	trimestre = fields.Selection([('1', 'T01'),('2','T02'),('3','T03'),('4','T04')], 'Trimestre', required=True, )
	yearr = fields.Selection([(num, str(num)) for num in range(((datetime.now().year)-4), ((datetime.now().year)+1) )] , 'Annee', required=True,) 


	def print_excel_report(self, cr, uid, ids, context=None):

	    month= datetime.now().month
	    y= datetime.now().year
	    wizard=self.browse(cr, uid, ids)
	    i=0
	    s1=0
	    s2=0
	    s3=0
	    n=1
	    page=1
	    j=int(wizard.trimestre)
	    year=int(wizard.yearr)
	    mois=(2*j)+(j+(-2))#1er mois de chaque trimestre
	    if ((month < mois) and (year==y)):
			raise osv.except_osv(('Trimestre errone'), ('Vous devez choisir un trimestre deja depasse ou en cours '))

	    filename = "DS12345678990006.12016.txt"
	    # Open a file
	    fo = open("foo.txt", "wb+")
	    #fo.write( "Python is a great language.\nYeah its great!!\n")
	    #fo.write( "\n")#retour a la ligne
	    #dataaaa=fo.read()
	    # s.upper() ==> s en majuscule
	    nom="Marwa mazhoud romdhan"
	    employee_ids=self.pool.get('hr.employee').search(cr, uid, [('slip_ids','!=','')])
	    employee_objs=self.pool.get('hr.employee').browse(cr, uid, employee_ids)
	    print "x1111****************",employee_objs
	    if employee_objs:
			for employee in employee_objs:
			        s1=0
    				s2=0
	    			s3=0
				## Fiche de paie 1
				from_date1=datetime(year,mois,1)
				print "from_date1mmmmmmmmmmmmmm",from_date1
				to_date1=datetime(year,mois,calendar.monthrange(year,mois)[1])


				payslip_ids1 = self.pool.get('hr.payslip').search(cr, uid, [('date_from','=',from_date1),('date_to','=',to_date1),('employee_id','=',employee.id)])
				payslip_objs1 = self.pool.get('hr.payslip').browse(cr, uid, payslip_ids1)

				## Fiche de paie 2
				from_date2=datetime(year,mois+1,1)
				to_date2=datetime(year,mois+1,calendar.monthrange(year,mois+1)[1])#

				payslip_ids2 = self.pool.get('hr.payslip').search(cr, uid, [('date_from','=',from_date2),('date_to','=',to_date2),('employee_id','=',employee.id)])
				payslip_objs2 = self.pool.get('hr.payslip').browse(cr, uid, payslip_ids2)

				## Fiche de paie 3
				from_date3=datetime(year,mois+2,1)
				to_date3=datetime(year,mois+2,calendar.monthrange(year,mois+2)[1])#

				payslip_ids3 = self.pool.get('hr.payslip').search(cr, uid, [('date_from','=',from_date3),('date_to','=',to_date3),('employee_id','=',employee.id)])
				payslip_objs3 = self.pool.get('hr.payslip').browse(cr, uid, payslip_ids3)
				if payslip_objs1:
					for pay1 in payslip_objs1:
						if pay1.contract_id.type_id.name != "SIVP":
							hr_payslip_line_ids = self.pool.get('hr.payslip.line').search(cr, uid, [('slip_id', '=', pay1.id)])
							hr_payslip_line_obj = self.pool.get('hr.payslip.line').browse(cr,uid,hr_payslip_line_ids)

							for hr_payslip_line in hr_payslip_line_obj :
								if hr_payslip_line.code=='BRUT' :
									s1=hr_payslip_line.total
				if payslip_objs2:
					for pay2 in payslip_objs2:
						if pay2.contract_id.type_id.name != "SIVP":
							hr_payslip_line_ids = self.pool.get('hr.payslip.line').search(cr, uid, [('slip_id', '=', pay2.id)])
							hr_payslip_line_obj = self.pool.get('hr.payslip.line').browse(cr,uid,hr_payslip_line_ids)

							for hr_payslip_line in hr_payslip_line_obj :
								if hr_payslip_line.code=='BRUT' :
									s2=hr_payslip_line.total

				if payslip_objs3:
					for pay3 in payslip_objs3:
						if pay3.contract_id.type_id.name != "SIVP":
							hr_payslip_line_ids = self.pool.get('hr.payslip.line').search(cr, uid, [('slip_id', '=', pay3.id)])
							hr_payslip_line_obj = self.pool.get('hr.payslip.line').browse(cr,uid,hr_payslip_line_ids)

							for hr_payslip_line in hr_payslip_line_obj :
								if hr_payslip_line.code=='BRUT' :
									s3=hr_payslip_line.total				
				s=int((s1+s2+s3)*1000)
				if (s>0):
					print "employee***************",employee.name
					i+=1
					if i==((12*n)+1):
						page+=1
						i=1

					num_ligne=str(i)
					print 'num ligne***********', num_ligne
					if i<10 :
						num_ligne='0'+str(i)

					num_page=str(page)
					print 'num page***********', num_page
					while(len(num_page)<3):
						num_page='0'+num_page
					fo.write( "00345678")#Matricle employeur 8 carac
					fo.write( "99")#cle employeur 2 carac
					fo.write( "0006")#code d'exploi 4 carac
					fo.write( wizard.trimestre)#trimestre 1 carac
					fo.write( str(year))#annee 4 carac	
					fo.write( num_page)#num page 3 carac
					fo.write( num_ligne)#num ligne 2 carac
					##fo.write( "98765432")#Matricle assure 8 carac
					#fo.write( "11")#cle assure 2 carac
					if employee.matricule_cnss:
						fo.write(str(employee.matricule_cnss))
					else:				
						fo.write("0000000000")
				
					nom=employee.name
					while(len(nom)<60):
						nom+=' '
					fo.write(nom)#nom assure 60 carac :len( str )

					fo.write( str(employee.num_cin))#CARTE D'IDENTITE 8 carac


					#s=int((s1+s2+s3)*1000)
					salaire=str(s)
					while(len(salaire)<10):
						salaire='0'+salaire
					print "salaiiiire ************====",salaire
					fo.write( salaire)#salaire 10 carac
					fo.write( "          ")#zone vierge 10 carac
					fo.write( "\n")#retour a la ligne
					dataaaa=fo.read()
	    else :
	    	fo.write( " ")
	    	dataaaa=fo.read()
		# Close opend file
		
	    with open("foo.txt") as file:
		
		
			data = file.read()
			#print "dataaaaaa=",data
			#print "len( data )=======",len( data )

	    export_id = self.pool.get('txt.extended').create(cr, uid, {'excel_file': base64.encodestring(data), 'file_name': filename,'trimestre':wizard.trimestre}, context=context)


	    position = fo.tell()
	    print "Current file position : ", position
	    fo.close()		
	    return{

			'view_mode': 'form',

			'res_id': export_id,

			'res_model': 'txt.extended',

			'view_type': 'form',

			'type': 'ir.actions.act_window',

			'context': context,

			'target': 'new',

	    }

