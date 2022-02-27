from django.apps import AppConfig


# class AppConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'app'


class job(AppConfig):
    name = 'app'
    def ready(self):
        from scheduled_job import updater, job
        updater.start()
        # job.update()

        
