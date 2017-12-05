from crudbuilder.abstract import BaseCrudBuilder

from youth.models import ChurchGoer


class Roll_A_Dex(BaseCrudBuilder):
    model = ChurchGoer
    search_fields = ['first_name', 'middle_name', 'maiden_name', 'nickname', 'birthday', 'school', 'gender']
    tables2_fields = ('first_name', 'middle_name', 'maiden_name', 'nickname', 'birthday')
    tables2_css_class = "table table-bordered table-condensed"
    tables2_pagination = 20  # default is 10
    login_required=True
    permission_required=True


        # permissions = {
        #     'list': 'example.person_list',
        #     'create': 'example.person_create'
        # }
        # createupdate_forms = {
        #     'create': PersonCreateForm,
        #     'update': PersonUpdateForm
        # }