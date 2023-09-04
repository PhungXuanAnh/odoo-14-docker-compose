# -*- coding: utf-8 -*-
"""
class inheritance
thêm field, chỉnh sửa field, chỉnh sửa phương thức trong model đã có; 
tổ chức database lưu trữ chung một bảng với model gốc.
"""
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

class MyPetPlus(models.Model):
    _name = "my.pet"
    _inherit = "my.pet"
    _description = "Extend mypet model"

    # add new field
    toy = fields.Char('Pet Toy', required=False)
    
    # modify old fields
    age = fields.Integer('Pet Age', default=2) # change default age from 1 to 2
    gender = fields.Selection(selection_add=[('sterilization', 'Sterilization')]) # add one more selection
