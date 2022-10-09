from app.bot.assets import Command, Callback


commands, callbacks = ([], [],)


def message(**kwargs):
    def with_args(handler):
        if 'names' in kwargs:
            if not isinstance(kwargs['names'], list):
                kwargs['names'] = [kwargs['names']]

            for name in kwargs['names']:
                commands.append(
                    Command(
                        name=name,
                        handler=handler,
                        dialog=kwargs['dialog'] if 'dialog' in kwargs else 'all',
                        admin=(kwargs['admin'] if 'admin' in kwargs else False),
                        with_args=(kwargs['with_args'] if 'with_args' in kwargs else False)
                    )
                )
        else:
            return False
    return with_args


def callback(**kwargs):
    def with_args(handler):
        if kwargs.keys() & {'name'}:
            callbacks.append(Callback(name=kwargs['name'], handler=handler, admin=(kwargs['admin'] if 'admin' in kwargs else False)))
        else:
            return False
    return with_args
