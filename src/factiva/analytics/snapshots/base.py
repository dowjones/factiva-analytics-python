from typing import Optional
from ..auth import UserKey
from ..common import tools, config


class SnapshotBaseJobResponse():
    job_id: Optional[str] = None
    job_link: Optional[str] = None
    job_state: Optional[str] = None


    def __init__(self, job_id: Optional[str] = None) -> None:
        self.job_id = job_id


    def __repr__(self):
        return self.__str__()


    def __str__(self, detailed=True, prefix='  |-', root_prefix=''):
        ret_val = f"{root_prefix}<'factiva.analytics.{str(self.__class__).split('.')[-1]}\n"
        if self.job_id and len(self.job_id) >= 40:
            ret_val += f"{prefix}job_id: {tools.mask_string(self.job_id, 10)}\n"
        else:
            ret_val += f"{prefix}job_id: {tools.print_property(self.job_id)}\n"
        if self.job_link:
            ret_val += f"{prefix}job_link: {tools.print_property(self.job_link[0:20] + '...' + self.job_link[-10:])}\n"
        else:
            ret_val += f"{prefix}job_link: <NotSet>\n"
        ret_val += f"{prefix}job_state: {tools.print_property(self.job_state)}\n"
        return ret_val



class SnapshotBaseQuery():
    where: Optional[str] = None
    includes: Optional[dict] = None
    include_lists: Optional[dict] = None
    excludes: Optional[dict] = None
    exclude_lists: Optional[dict] = None

    # TODO: Consider implementing a SQL validation functionality to ensure 
    # fields are valid. There's sample projects doing something similar.
    # https://github.com/David-Wobrock/sqlvalidator


    def __init__(
        self,
        where=None,
        includes: Optional[dict] = None,
        include_lists: Optional[dict] = None,
        excludes: Optional[dict] = None,
        exclude_lists: Optional[dict] = None
    ):
        if isinstance(where, str):
            self.where = where
        elif config.load_environment_value('FACTIVA_WHERE', '') != '':
            self.where = config.load_environment_value('FACTIVA_WHERE')
        else:
            raise ValueError("Where value not provided and env variable FACTIVA_WHERE not set.")

        # TODO: Create a validation method that checks the dict structure as key: [list]
        # for all properties below. Additionally, keys must be in a predefined column
        # dictionary.
        if includes:
            self.includes = tools.parse_field(includes, 'includes')

        if include_lists:  # TODO: Validate data structure
            self.include_lists = tools.parse_field(include_lists, 'includes')

        if excludes:
            self.excludes = tools.parse_field(excludes, 'excludes')

        if exclude_lists:  # TODO: Validate data structure
            self.exclude_lists = tools.parse_field(exclude_lists, 'excludes')


    def get_payload(self) -> dict:
        from typing import Any, Dict
        
        query_dict: Dict[str, Any] = {
            "query": {
                "where": self.where
            }
        }

        if self.includes:
            query_dict["query"]["includes"] = self.includes

        if self.excludes:
            query_dict["query"]["excludes"] = self.excludes

        if self.include_lists:
            query_dict["query"]["includesList"] = self.include_lists

        if self.exclude_lists:
            query_dict["query"]["excludesList"] = self.exclude_lists

        return query_dict


    def __repr__(self):
        return self.__str__()


    def __str__(self, detailed=True, prefix='  ├─', root_prefix=''):
        ret_val = f"{root_prefix}<'factiva.analytics.{str(self.__class__).split('.')[-1]}\n"
        ret_val += f"{prefix}where: "
        if self.where:
            ret_val += (self.where[:77] + '...') if len(self.where) > 80 else self.where
        else:
            ret_val += "<NotSet>"
        # if detailed:
        ret_val += f"\n{prefix}includes: "
        ret_val += f"\n{prefix.replace('├', '│')[0:-1]}  └─{len(self.includes)} conditions" if self.includes else "<NotSet>"
        ret_val += f"\n{prefix}excludes: "
        ret_val += f"\n{prefix.replace('├', '│')[0:-1]}  └─{len(self.excludes)} conditions" if self.excludes else "<NotSet>"
        ret_val += f"\n{prefix}include_lists: "
        ret_val += f"\n{prefix.replace('├', '│')[0:-1]}  └─{len(self.include_lists)} conditions" if self.include_lists else "<NotSet>"
        ret_val += f"\n{prefix}exclude_lists: "
        ret_val += f"\n{prefix.replace('├', '│')[0:-1]}  └─{len(self.exclude_lists)} conditions" if self.exclude_lists else "<NotSet>"
        # else:
        #     ret_val += f"\n{prefix.replace('├', '└')}..."
        return ret_val



class SnapshotBase():

    __JOB_BASE_URL = None
    __SUBMIT_URL = None
    __GETINFO_URL = None
    __GETLIST_URL = None
    __log = None

    user_key: Optional[UserKey] = None
    job_response: Optional[SnapshotBaseJobResponse] = None
    query: Optional[SnapshotBaseQuery] = None

    def __init__(
        self,
        user_key=None,
        query=None,
        job_id=None
    ) -> None:
        if isinstance(user_key, UserKey):
            self.user_key = user_key
        else:
            self.user_key = UserKey(user_key)

        if query and job_id:
            raise ValueError("The query and job_id parameters cannot be assigned simultaneously")

        # if (not query) and (not job_id):
        #     raise ValueError("Paramters query or job id are required")


    def submit_job(self, payload=None) -> bool:  # TODO: NEXT!
        return True


    def get_job_response_base(self) -> bool:
        return True


    def __repr__(self):
        return self.__str__()


    def __str__(self, detailed=True, prefix='  ├─', root_prefix=''):
        ret_val = f"{root_prefix}<'factiva.analytics.{str(self.__class__).split('.')[-1]}\n"
        ret_val += f"{prefix}user_key: {str(self.user_key)}\n"
        if self.query:
            ret_val += f"{prefix}query: {self.query.__str__(detailed=False, prefix='  │  ├─')}\n"
        else:
            ret_val += f"{prefix}query: <NotRetrieved>\n"
        if self.job_response:
            ret_val += f"{prefix}job_response: {self.job_response.__str__(detailed=False, prefix='  │  ├─')}"
        else:
            ret_val += f"{prefix}job_response: <NotSubmitted>"
        return ret_val
