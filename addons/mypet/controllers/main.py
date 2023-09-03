import odoo
import logging
import json

_logger = logging.getLogger(__name__)

class MyPetAPI(odoo.http.Controller):
    # http://localhost:10014/foo
    @odoo.http.route('/foo', auth='public') # or public or none
    def foo_handler(self):
        return "Welcome to 'foo' API!"

    # http://localhost:10014/bar
    @odoo.http.route('/bar', auth='public')
    def bar_handler(self):
        return json.dumps({
            "content": "Welcome to 'bar' API! haha "
        })
    
    # http://localhost:10014/pet/test-db-1/0
    # http://localhost:10014/pet/test-db-1/1
    # http://localhost:10014/pet/test-db-1/2
    # http://localhost:10014/pet/noexist_db/1
    @odoo.http.route(['/pet/<dbname>/<id>'], type='http', auth="none", sitemap=False, cors='*', csrf=False)
    def pet_handler(self, dbname, id, **kw):
        model_name = "my.pet"
        try:
            registry = odoo.modules.registry.Registry(dbname)
            with odoo.api.Environment.manage(), registry.cursor() as cr:
                env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
                rec = env[model_name].search([('id', '=', int(id))], limit=1)
                response = {
                    "status": "ok",
                    "content": {
                        "name": rec.name,
                        "nickname": rec.nickname,
                        "description": rec.description,
                        "age": rec.age,
                        "weight": rec.weight,
                        "dob": rec.dob.strftime('%d/%m/%Y'),
                        "gender": rec.gender,
                    }
                }
        except Exception:
            response = {
                "status": "error",
                "content": "not found"
            }
        return json.dumps(response)