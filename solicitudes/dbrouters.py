class postgresqlRouter(object):
    """
    A router to control all database operations on models in the application.
    """
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'solicitudes':
            return 'solicitudes'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'solicitudes':
            return 'solicitudes'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'solicitudes' or \
            obj2._meta.app_label == 'solicitudes':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'solicitudes':
            return db == 'solicitudes'
        return None
