import xmlrpc.client

ODOO_BACKEND = 'http://localhost:10014'
ODOO_DB = 'test-db-1'
ODOO_USER = 'xa@mail.com'
ODOO_PASS = '1234'

def my_print(data_list, title=''):
    if title:
        print(title)
    for line in data_list:
        print('-', line)


# https://www.odoo.com/documentation/13.0/webservices/odoo.html
class XMLRPC_API():
    def __init__(self, url, db, username='admin', password='admin'):
        self.url = url
        self.db = db
        self.username = username
        self.password = password
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(self.url))
        self.uid = common.authenticate(self.db, self.username, self.password, {})
        self.models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
        pass

    # get fields names of the model
    def get_fields(self, model_name, required=False):
        data = self.models.execute_kw(self.db, 
            self.uid, 
            self.password, 
            model_name, 
            'fields_get',
            [], {'attributes': ['string', 'type', 'required', 'readonly']})
        
        if required:
            key_list = list(data.keys())
            for k in key_list:
                if not data[k].get('required', False):
                    data.pop(k)
                pass
        return data

    def search(self, model_name, conditions=[()]):
        return self.models.execute_kw(self.db, self.uid, self.password,
            model_name, 
            'search',
            [conditions])  

    # Create
    def create(self, model_name, data_dict):
        """
        Eg.
            model_name: 'res.users'
            data_dict: { 'name': "Minh", 'age': 27 }
        """
        id = self.models.execute_kw(self.db, self.uid, self.password, model_name, 'create', [data_dict])
        return id

    # Read
    def read(self, model_name, conditions=[()], params={}):
        """
        Eg.
            model_name: 'res.users'
            conditions: [('id', '>', 1)]
            params: {'fields': ['name', 'country_id', 'comment'], 'limit': 5}
        """
        return self.models.execute_kw(self.db, self.uid, self.password,
            model_name, 
            'search_read',
            [conditions],
            params)       
    
    # Update
    def update(self, model_name, id_list, new_data_dict):
        """
        Eg.
            model_name: 'res.users'
            id_list: [7]
            new_data_dict: { 'name': "Newer partner", 'age': 27 }
        """
        self.models.execute_kw(self.db, 
            self.uid, 
            self.password, 
            model_name, 
            'write', 
            [id_list, new_data_dict])

    # Delete
    def delete(self, model_name, id_list):
        self.models.execute_kw(self.db, self.uid, self.password, model_name, 'unlink', [id_list])
        pass

    # Soft delete
    def soft_delete(self, model_name, id_list):
        self.update(model_name, id_list, {
            'active': False,
        })

    # Aug 01, 2019
    def call(self, model_name, method, params=[]):
        return self.models.execute_kw(self.db, self.uid, self.password, model_name, method, params)

    def call2(self, model_name, method, param1, param2):
        return self.models.execute_kw(self.db, self.uid, self.password, model_name, method, param1, param2)

def main():
    client = XMLRPC_API(url=ODOO_BACKEND, db=ODOO_DB, username=ODOO_USER, password=ODOO_PASS)

    # list vendor accounts
    my_print(client.read(model_name='my.pet', 
        conditions=[('id', '>=', 1)], 
        params={ 'fields': ['name', 'nickname'], }), title='Read My Pet')
    
    my_print(client.call2(model_name="my.pet", method="search_read", param1=[[('id', '>=', 1)]], param2={}), title='General Call')

    client.create(model_name="my.pet", data_dict={"name": "Minh", "nickname": "Kyz"})
    print("Created new pet")

    client.update(model_name="my.pet", id_list=[1], new_data_dict={"name": "Kitte", "nickname": "Sugar Baby"})
    print("Update new pet")


if __name__ == '__main__':
    main()
