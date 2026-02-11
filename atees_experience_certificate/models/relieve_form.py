from odoo import models, fields, api

class RelieveForm(models.Model):
    _name = 'relieve.form'
    _description = "Relive Form"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'employee_id'


    department_id = fields.Many2one('hr.department', string="Department")
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True, readonly=True, default=lambda self: self._get_current_employee())
    join_date = fields.Date(string="Joining Date")
    terminate_date = fields.Date(string="Terminate Date")
    job_id = fields.Many2one('hr.job', string="Job Title")
    head_dept = fields.Char(string="Head Of Department")
    head_dept_id = fields.Many2one('hr.employee', string="Head Of Department")
    state = fields.Selection([('draft', 'Request'),('department', 'Head Approved'),('admin','Admin Approved'),('hr','HR Approved'),('cancel', 'Cancel')])
    department_head_id = fields.Many2one('hr.employee', string="Department Head")
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)

    # return property items
    laptop = fields.Boolean(string="Laptop")
    mobile = fields.Boolean(string="Mobile")
    sim = fields.Boolean(string="SIM")
    id_card = fields.Boolean(string="Id Card")
    connectors = fields.Boolean(string="Connectors")
    devices = fields.Boolean(string="Devices")
    credentials = fields.Boolean(string="Credentials")
    credentials_of_office = fields.Boolean(string="Credentials of Office")
    credentials_of_client = fields.Boolean(string="Credentials of Clients")
    flock = fields.Boolean(string="Flock")
    gmail = fields.Boolean(string="Gmail")
    erp = fields.Boolean(string="ERP")
    social_media = fields.Boolean(string="Social Media")
    server = fields.Boolean(string="Server")
    headset = fields.Boolean(string="Headset")
    tab = fields.Boolean(string="Tab")
    others = fields.Char(string="Others")



    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        if self.employee_id:
            self.department_id = self.employee_id.department_id.id
            self.job_id = self.employee_id.job_id.id
            self.head_dept_id = self.employee_id.parent_id.id




    def _get_current_employee(self):
        employee = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
        return employee.id



    # employee request
    def relieve_request(self):
        self.state = 'draft'

    #     request approved and rejected by the dept head

    def head_approved(self):
        # Get the current user's name
        current_user = self.env.user.name
        # Update state
        self.state = 'department'
        # Post message in chatter
        self.message_post(
            body=f"Department Head {current_user} approved the relieve request for employee {self.employee_id.name}.",
            subject="Relieve Request Approved by Department Head"
        )

    def reject_request_head(self):
        """ Set state to 'cancel' when the request is rejected """
        self.state = 'cancel'
        current_user = self.env.user.name
        self.message_post(
            body=f"Department Head {current_user} rejected the relieve request for employee {self.employee_id.name}.",
            subject="Relieve Request Rejected by Department Head"
        )



    # request approved or rejected by the admin

    def admin_approved(self):
        self.state = 'admin'
        current_user = self.env.user.name
        self.message_post(
            body=f"Admin {current_user} approved the relieve request for employee {self.employee_id.name}.",
            subject="Relieve Request Approved by Admin"
        )

    def reject_request_admin(self):
        """ Set state to 'cancel' when the request is rejected """
        self.state = 'cancel'
        current_user = self.env.user.name
        self.message_post(
            body=f"Admin {current_user} rejected the relieve request for employee {self.employee_id.name}.",
            subject="Relieve Request Rejected by Admin"
        )

    #     request is approved or rejected by the hr

    def hr_approved(self):
        self.state = 'hr'
        current_user = self.env.user.name
        self.message_post(
            body=f"HR {current_user} approved the relieve request for employee {self.employee_id.name}.",
            subject="Relieve Request Approved by HR"
        )


    def reject_request_hr(self):
        """ Set state to 'cancel' when the request is rejected """
        self.state = 'cancel'
        current_user = self.env.user.name
        self.message_post(
            body=f"HR {current_user} rejected the relieve request for employee {self.employee_id.name}.",
            subject="Relieve Request Rejected by HR"
        )


