class CopyDataModel():
    elem = None
    recursive = False
    copy_data = True
    models_list = ['']

    def __init__(self, *args, **kwargs):
        self.model = kwargs.get('model')
        self.elem = kwargs.get('elem')
        self.recursive = kwargs.get('recursive')
        self.copy_data = kwargs.get('copy_data')
        self.models_list = kwargs.get('models_list')
        self.valide_models = kwargs.get('valide_models')
        # super(CopyDataModel).__init__(self, *args, **kwargs)

    @staticmethod
    def recursive_search(self, model_parent=''):
        """
        Поиск зависимостей модели из списка models_list
        """
        result = []
        print(model_parent)
        for model in self.models_list:
            if model_parent == 'template':
                fields = model.objects.filter(tv=self.elem.pk)
            elif model_parent == 'resource':
                fields = model.objects.filter(tv_resource=self.elem.pk)
            elif model_parent == 'section':
                fields = model.objects.filter(tv_section=self.elem.pk)
            else:
                fields = []
            if len(fields) == 0:
                pass
            else:
                for field in fields:
                    result.append(field)
        return result

    def copy(self, *args, **kwargs):
        """
        Копируем сам элемент, и связанные с ним элементы из списка models_list
        """
        class_name = str(self.elem.__class__).split('.')[-1].split('\'>')[0].lower()
        print(class_name)
        if kwargs.get('elem', None) != None and kwargs.get('lists', None) != None:
            elem = kwargs['elem']
            
            for obj in kwargs['lists']:
                if class_name == 'template':
                    if obj.tv:
                        obj.tv = self.model.objects.get(pk=elem.pk)
                        obj.pk = None
                        obj.save()
                elif class_name == 'resource':
                    if obj.tv_resource:
                        obj.tv_resource = self.model.objects.get(pk=elem.pk)
                        obj.pk = None
                        obj.save()
                elif class_name == 'section':
                    if obj.tv_section:
                        obj.tv_section = self.model.objects.get(pk=elem.pk)
                        obj.pk = None
                        obj.save()
        else:
            lists = self.recursive_search(self, model_parent=class_name)
            # try:
            #     self.elem.name = f'{self.elem.name}_copy'
            # except AttributeError:
            #     # self.elem.pagetitle = f'{self.elem.pagetitle}_copy'
            
            old_name = self.elem.get_name()
                
            
            self.elem.pk = None
            self.elem.save()
            self.elem.change_name(new_name=f'{old_name}_copy')
            if self.recursive and len(lists) > 0:
                self.copy(
                    elem=self.elem,
                    lists=lists
                    )
            return self.elem.pk
        
    def delete(self, *args, **kwargs):
        class_name = str(self.elem.__class__).split('.')[-1].split('\'>')[0]
        if kwargs.get('elem', None) != None and kwargs.get('lists', None) != None:
            elem = kwargs['elem']
            for obj in kwargs['lists']:
                if obj.tv:
                    obj.delete()
        else:
            lists = self.recursive_search(self)
            if self.recursive and len(lists) > 0:
                self.delete(
                    elem=self.elem,
                    lists=lists
                    )
            self.elem.delete()




        # new_elem = model.objects.create()

