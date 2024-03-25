import pysftp

class PsftpConnection(pysftp.Connection):
    def __init__(self, *args, **kwargs):
        try:
            if kwargs.get('cnopts') is None:
                kwargs['cnopts'] = pysftp.CnOpts()
        except pysftp.HostKeysException as e:
            self._init_error = True
        else:
            self._init_error = False
        
        self._sftp_live = False
        self._transport = None

        super().__init__(*args, **kwargs)


    def __del__(self):
        if not self._init_error:
            self.close()
