import odoo
import json
import logging
_logger = logging.getLogger(__name__)

class MyPetAPIInherit(odoo.addons.mypet.controllers.main.MyPetAPI):
    # http://localhost:10014/foo
    @odoo.http.route()
    def foo_handler(self):
        return "New 'foo' API!"

    # http://localhost:10014/bar2
    @odoo.http.route('/bar2')
    def bar_handler(self):
        return json.dumps({
            "content": "New 'bar' API!"
        })

    # http://localhost:10014/pet/test-db-1/1
    @odoo.http.route()
    def pet_handler(self, dbname, id, **kw):
        _logger.warning("Pet handler called~")
        result = super(MyPetAPIInherit, self).pet_handler(dbname, id)
        _logger.warning("Post processing~")
        return result