class routerRecibosNomina(object):
    """
    A router to control all database operations on models in the application.
    """
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'recibos_nom':
            return 'recibos_nom'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'recibos_nom':
            return 'recibos_nom'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'recibos_nom' or \
            obj2._meta.app_label == 'recibos_nom':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'recibos_nom':
            return db == 'recibos_nom'
        return None
