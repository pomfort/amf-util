import click


class Context(object):
    """
    Context is a custom object intended to wrap root runtime configurations...
    most of which are provided upon CLI invocation via options.
    """
    def __init__(self):
        self.sys_username = None
        self.filepath = None
        self.schemapath = None
        self.rootpath = None
        self.compact = False
        self.ctl_root_path = None
        self.verbose = None

    def load_args(self, **kwargs):
        """
        sets all context properties based on the values contained in the kwargs.
        intended to be called directly with the arguments and options provided to the cli upon invocation.
        :param kwargs: all arguments/options from the cli passed along as key-word-arguments.
        :return: none
        """
        self.filepath = kwargs.get('filepath')
        self.schemapath = kwargs.get('schemapath')
        self.rootpath = kwargs.get('rootpath')
        self.compact = kwargs.get('compact')
        self.ctl_root_path = kwargs.get('ctlrootpath')
        self.verbose = kwargs.get('verbose')


"""
this is a custom decorator that we use instead of the default pass_context that click provides so that our 
custom context gets injected.
"""
pass_context = click.make_pass_decorator(Context, ensure=True)
