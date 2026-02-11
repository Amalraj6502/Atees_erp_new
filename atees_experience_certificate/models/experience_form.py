from odoo import models, fields, api
from datetime import date


class ExperienceCertificate(models.Model):
    _name = 'experience.certificate'
    _description = 'Certificate for the employees'
    _inherit = ['mail.thread']

    name = fields.Char(string="Reference Number", readonly=True, copy=False)
    new_name = fields.Char(string="Reference Number")
    title = fields.Char(string="Title")
    partner_title_id = fields.Many2one(
        'res.partner.title',
        string="Title"
    )
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True)
    company_ids = fields.Many2many(
        'res.company',
        string="Allowed Companies",
        default=lambda self: self.env.user.company_ids
    )

    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)



    job_title_id = fields.Many2one('hr.job', string="Job Title")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], string="Gender")
    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")
    created_on = fields.Date(string="Created Date", default=fields.Date.today)
    period = fields.Char(string="Period", compute='_compute_period', store=True)
    salary = fields.Monetary(string="Salary", currency_field='currency_id')
    rating = fields.Integer(string='Rating', default=0)
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
    )

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        """Auto-fill job title, from_date and to_date from HR Contract when employee selected."""
        for rec in self:

            if rec.employee_id:
                # Set job title from employee record
                rec.job_title_id = rec.employee_id.job_id.id
                rec.gender = rec.employee_id.gender if hasattr(rec.employee_id, 'gender') else False

                # Find latest active or most recent contract for this employee
                contract = self.env['hr.contract'].search([
                    ('employee_id', '=', rec.employee_id.id)
                ], order='date_start desc', limit=1)

                # Fill From/To dates from the contract (if found)
                rec.from_date = contract.date_start or False
                rec.to_date = contract.date_end or False
                rec.salary = contract.wage or False
            else:
                rec.job_title_id = False
                rec.from_date = False
                rec.to_date = False

    @api.depends('from_date', 'to_date')
    def _compute_period(self):
        for rec in self:
            if rec.from_date and rec.to_date:
                rec.period = f"Since {rec.from_date.strftime('%d.%m.%Y')} to {rec.to_date.strftime('%d.%m.%Y')}"
            elif rec.from_date:
                rec.period = f"Since {rec.from_date.strftime('%d.%m.%Y')}"
            else:
                rec.period = ''

    @api.model
    def create(self, vals):
        vals = self._assign_sequence(vals)
        return super(ExperienceCertificate, self).create(vals)

    @api.onchange('employee_id')
    def _onchange_employee_id_sequence(self):
        for rec in self:
            vals = {'employee_id': rec.employee_id.id}
            seq_vals = self._assign_sequence(vals)
            rec.name = seq_vals.get('name')

    def _assign_sequence(self, vals):
        """Generate company-specific sequence dynamically"""
        company = self.env.company
        if vals.get('employee_id'):
            employee = self.env['hr.employee'].browse(vals['employee_id'])
            company = employee.company_id or self.env.company

        vals['company_id'] = company.id

        company_code = (company.name or 'COMP').upper()
        padding = 4

        # Search for the last certificate of this company
        last_cert = self.env['experience.certificate'].sudo().search(
            [('company_id', '=', company.id)],
            order='id desc', limit=1
        )

        if last_cert and last_cert.name:
            # Extract last number from last certificate name
            try:
                last_number = int(last_cert.name.split('/')[-1])
            except ValueError:
                last_number = 0
        else:
            last_number = 0

        next_number = last_number + 1

        # Build certificate name
        vals['name'] = f"{company_code}/EXPC/{str(next_number).zfill(padding)}"
        return vals




