import logging
import magic

from . import wrapper

from .conf import settings

logger = logging.getLogger(__name__)

class Mime(wrapper.Wrapper):
    def __init__(self, filepath):
        super().__init__(exec_name=settings.BINARY_FILE)
        self.filepath = filepath
        self.mime_magic = magic.Magic(mime=True)
        
    def get_cmd(self):
        cmd = super().get_cmd()

        cmd.extend(['--mime-type'])
        cmd.extend(['-b'])
        cmd.extend([self.filepath])

        return cmd

    def is_tiff(self):
        return self.guess() == 'image/tiff'

    def is_pdf(self):
        return self.guess() == 'application/pdf'

    def is_image(self):
        """
        Returns true if MIME type is one of following:
            * image/png
            * image/jpg
        """
        return self.guess() in ('image/png', 'image/jpg', 'image/jpeg')

    def guess(self):
        fvv=open(self.filepath ,'rb').read()
        return self.mime_magic.from_buffer(fvv)

    def __str__(self):

        mime_type = self.guess()
        return f"Mime({self.filepath}, {mime_type})"
