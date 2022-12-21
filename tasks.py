from invoke import task


@task
def manage(context, command, watchers=()):
    return context.run(" ".join(["python", "manage.py"] + [command]),
                       watchers=watchers)


@task
def run(context):
    manage(
        context,
        "runserver_plus 0.0.0.0:8000 --reloader-type stat",
    )
