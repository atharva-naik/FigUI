import imap_tools
from enum import Enum, auto
from typing import Union, List
try:
    from FigUI.subSystem.Email.user import UserModel
except ImportError:
    from .user import UserModel


class Inbox(Enum):
    All = auto()
    Junk = auto()
    Sent = auto()
    Trash = auto()
    Drafts = auto()
    Flagged = auto()
    Noselect = auto()
    Important = auto()
    HasChildren = auto()
    HasNoChildren = auto()

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name


class IMapMailHandler:
    def __init__(self, imap_url):
        self.imap_url = imap_url 
        self.mail_box = imap_tools.MailBox(self.imap_url) 

    def login(self, user: Union[UserModel, str], pswd: str):
        '''return True if login was successfull.'''
        if isinstance(user, UserModel):
            self.mail_box.login(user.email, user.password)
        elif isinstance(user, str):
            self.mail_box.login(user, pswd)
        return True

    def logout(self):
        self.mail_box.logout()

    def folders(self, 
                root: Union[None, str]=None, 
                as_dicts: bool=False,
                select: List[Inbox]=[Inbox.HasNoChildren],
                reject: List[Inbox]=[Inbox.Noselect]):
        '''list all the folders.'''
        if root is None:
            folderList = [f for f in self.mail_box.folder.list()]
        else:
            folderList = [f for f in self.mail_box.folder.list(root)]
        select = [str(s) for s in select]
        reject = [str(r) for r in reject]
        # apply flags.
        filtList = []
        for folder in folderList:
            accept = False
            # accept if flag is present in the select list.
            for flag in folder.flags:
                if flag[1:] in select: 
                    accept = True; break
            # reject if flag is present in the reject list. This takes precedence over the select list.
            for flag in folder.flags:
                if flag[1:] in reject: 
                    accept = False; break
            if accept: filtList.append(folder)
        if not as_dicts:
            return filtList
        # convert to list of dictionaries.
        dictRecords = []
        for folder in filtList:
            record = {}
            record["name"] = folder.name
            record["delim"] = folder.delim
            record["flags"] = [f[1:] for f in list(folder.flags)]
            dictRecords.append(record)

        return dictRecords
    # def folderTree(self, root=None):
    #     folders = self.folders(root)
    def __iter__(self):
        for msg in self.mail_box.fetch(imap_tools.AND(all=True)):
            yield msg


if __name__ == "__main__":
    pass