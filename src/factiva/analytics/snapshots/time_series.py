"""
  Classes to interact with the Snapshot Analytics (TimeSeries) endpoint
"""
from io import StringIO
import time
import pandas as pd
from typing import Any, Optional
from .base import SnapshotBase, SnapshotBaseQuery, SnapshotBaseJobResponse
from ..common import log, const, tools, req


class SnapshotTimeSeriesJobReponse(SnapshotBaseJobResponse):
    """
    Snapshot Explain Job Response class. Essentially contains the volume
    of estimate documents.

    Attributes
    ----------
    job_id : str
        Explain Job ID with a format like ``abcd1234-ab12-ab12-ab12-abcdef123456``.
    job_link : str
        Unique URL referring to the job instance
    job_state : str
        Latest known job status. Value is self-explanatory.
    data : pandas.DataFrame
        Obtained Time-Series data from job execution
    errors : list[dict]
        Job execution errors returned by the API

    """

    _data : Optional[pd.DataFrame] = None
    _download_link : Optional[str] = None
    _errors : Optional[list[dict]] = None
    # Override inherited properties with private variables
    _job_id: Optional[str] = None
    _job_link: Optional[str] = None
    _job_state: Optional[str] = None
    # Consider adding calculated values for start/end date and the number
    # of records


    def __init__(self, job_id: Optional[str] = None) -> None:
        # Initialize private variables directly to avoid property conflicts
        # Initialize using private variables first
        self._job_id = None
        self._job_link = None  
        self._job_state = None
        
        # Then use property setter for validation if job_id is provided
        if job_id is not None:
            self.job_id = job_id  # type: ignore[misc]


    def __repr__(self):
        return super().__repr__()


    def __str__(self, detailed=True, prefix='  ├─', root_prefix=''):
        ret_val = super().__str__(detailed, prefix, root_prefix)
        if self.download_link:
            ret_val += f"{prefix}download_link: {tools.print_property(self.download_link[0:20] + '...' + self.download_link[-20:])}"
        else:
            ret_val += f"{prefix}download_link: <NotSet>"
        ret_val += f"\n{prefix}data: {tools.print_property(self.data)}"
        if self.errors:
            ret_val += f"\n{prefix.replace('├', '└')}errors: [{len(self.errors)}]"
            err_list = [f"\n{prefix[0:-1]}  |-{err['title']}: {err['detail']}" for err in self.errors]
            for err in err_list:
                ret_val += err
        else:
            ret_val += f"\n{prefix.replace('├', '└')}errors: <NoErrors>"
        return ret_val


    # Getter and Setter methods
    @property
    def data(self) -> Optional[pd.DataFrame]:
        """Get the data DataFrame."""
        return self._data

    @data.setter
    def data(self, value: Optional[pd.DataFrame]) -> None:
        """Set the data DataFrame."""
        self._data = value

    @property
    def download_link(self) -> Optional[str]:
        """Get the download link."""
        return self._download_link

    @download_link.setter
    def download_link(self, value: Optional[str]) -> None:
        """Set the download link."""
        self._download_link = value

    @property
    def errors(self) -> Optional[list[dict]]:
        """Get the errors list."""
        return self._errors

    @errors.setter
    def errors(self, value: Optional[list[dict]]) -> None:
        """Set the errors list."""
        self._errors = value

    # Override inherited properties from base class
    @property
    def job_id(self) -> Optional[str]:
        """Get the job ID."""
        return self._job_id

    @job_id.setter
    def job_id(self, value: Optional[str]) -> None:
        """Set the job ID with TimeSeries-specific validation.
        
        TimeSeries job IDs should follow the format: abcd1234-ab12-ab12-ab12-abcdef123456
        """
        if value is None:
            raise ValueError("Job ID cannot be None")
        
        tools.validate_type(value, str, "Job ID must be a string")
        
        # Validate UUID format for TimeSeries jobs (36 characters with hyphens)
        if len(value) != 36 or value.count('-') != 4:
            raise ValueError("TimeSeries job ID must be in UUID format (e.g., abcd1234-ab12-ab12-ab12-abcdef123456)")
        
        # Additional validation: check if it matches UUID pattern
        import re
        uuid_pattern = r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$'
        if not re.match(uuid_pattern, value.lower()):
            raise ValueError("TimeSeries job ID must be a valid UUID format")
            
        self._job_id = value

    @property
    def job_link(self) -> Optional[str]:
        """Get the job link."""
        return self._job_link

    @job_link.setter
    def job_link(self, value: Optional[str]) -> None:  # type: ignore[misc]
        """Set the job link with validation."""
        if value is not None:
            tools.validate_type(value, str, "Job link must be a string")
        self._job_link = value

    @property
    def job_state(self) -> Optional[str]:
        """Get the job state."""
        return self._job_state

    @job_state.setter
    def job_state(self, value: Optional[str]) -> None:  # type: ignore[misc]
        """Set the job state with validation."""
        if value is not None:
            tools.validate_type(value, str, "Job state must be a string")
            # Validate against expected job states from constants
            expected_states = [const.API_JOB_DONE_STATE, const.API_JOB_FAILED_STATE] + const.API_JOB_EXPECTED_STATES
            if hasattr(const, 'API_JOB_EXPECTED_STATES') and value not in expected_states:
                # Allow setting even if not in expected states for flexibility
                pass
        self._job_state = value



class SnapshotTimeSeriesQuery(SnapshotBaseQuery):
    """
    Snapshot Query for TimeSeries operations class. Used only in the context of
    SnapshotTimeSeries.

    Attributes
    ----------
    where : str
        User representation for service authentication
    includes : dict
        Dictionary with a fixed list of codes to include
    includes_list : dict
        Dictionary with references to Lists for inclusion
    excludes : dict
        Dictionary with a fixed list of codes to exclude
    excludes_list : dict
        Dictionary with references to Lists for inclusion
    frequency : str
        Time unit used to aggregate values in the time-series calculation
    date_field : str
        Schema date-time field used to calculate the time-series dataset
    group_dimension : str
        Field name to break-down aggregates per time period unit
    top : str
        Max entries per group_dimension per time period unit
    """

    _frequency : str = const.API_MONTH_PERIOD
    _date_field : str = const.API_PUBLICATION_DATETIME_FIELD
    _group_dimension : list[Any] | str
    _top : Optional[int] = None

    def __init__(self,
                where=None,
                includes: Optional[dict] = None,
                include_lists: Optional[dict] = None,
                excludes: Optional[dict] = None,
                exclude_lists: Optional[dict] = None,
                group_dimension: Optional[list[Any] | str] = None,
                frequency: str = const.API_MONTH_PERIOD,
                date_field:str = const.API_PUBLICATION_DATETIME_FIELD,
                top: int = 10):
        """
        Class constructor
        
        Parameters
        ----------
        where : str
            String containing the query WHERE statement.
        includes : dict, optional
            Collection of bulk values to be added to the selection criteria.
            Python dictionary with the format ``{column_name1: ['value1', 'value2, ...],
            column_name2: ['value1', 'value2', ...]}``.
        excludes : dict, optional
            Collection of bulk values to be removed from the selection criteria.
            Python dictionary with the format ``{column_name1: ['value1', 'value2, ...],
            column_name2: ['value1', 'value2', ...]}``.
        include_lists : dict, optional
            Collection of column-List values to be added to the selection crieria
            Python dictionary with the format ``{column_name1: ['listID1', 'listID2, ...],
            column_name2: ['listID1', 'listID2', ...]}``.
        exclude_lists : dict, optional
            Collection of bulk values to be removed from the selection criteria.
            Python dictionary with the format ``{column_name1: ['ListID1', 'listID2, ...],
            column_name2: ['listID1', 'listID2', ...]}``.
        frequency : str, optional (default: 'MONTH')
            Date part to be used to group subtotals in the time-series dataset. Allowed values
            are ``DAY``, ``MONTH`` (default) and ``YEAR``.
        date_field : str, optional (default: 'publication_datetime')
            Timestamp column that will be used to calculate the time-series dataset. It can be
            any of the three values: ``publication_datetime`` (default), ``modification_datetime``,
            and ``ingestion_datetime``.
        group_dimension : str, optional (default: 'source_code')
            Field name that will be used to break-down subtotals for each period. Allowed values are one of the following:
            ``['source_code', 'subject_codes', 
            'region_codes', 'industry_codes', 'company_codes', 'person_codes', 'company_codes_about', 
            'company_codes_relevance', 'company_codes_cusip', 'company_codes_isin', 
            'company_codes_sedol', 'company_codes_ticker', 'company_codes_about_cusip', 
            'company_codes_about_isin', 'company_codes_about_sedol', 'company_codes_about_ticker', 
            'company_codes_relevance_cusip', 'company_codes_relevance_isin', 
            'company_codes_relevance_sedol', 'company_codes_relevance_ticker']``
        top : int, optional
            Limits the dataset to return only the top X values for the dimension passed in the
            ``group_dimension`` parameter. Default 10. Can be set to -1 to return all values.
        """
        super().__init__(
            where,
            includes if includes is not None else {},
            include_lists if include_lists is not None else {},
            excludes if excludes is not None else {},
            exclude_lists if exclude_lists is not None else {}
        )

        # Use property setters for validation
        self.frequency = frequency
        self.date_field = date_field
        self.group_dimension = group_dimension
        self.top = top


    def get_payload(self) -> dict:
        """
        Create the basic request payload to be used within Snapshots Explain API
        request.

        Returns
        -------
        dict
            Dictionary containing non-null query attributes.

        """
        payload = super().get_payload()

        payload["query"].update({"frequency": self.frequency})
        payload["query"].update({"date_field": self.date_field})

        if(self.group_dimension):
            payload["query"].update(
                {"group_dimensions": [self.group_dimension]})

        payload["query"].update({"top": self.top})

        return payload


    def __repr__(self):
        return super().__repr__()


    def __str__(self, detailed=True, prefix='  ├─', root_prefix=''):
        ret_val = super().__str__(detailed, prefix, root_prefix)
        ret_val = ret_val.replace('└─ex', '├─ex')
        ret_val += f"\n{prefix}frequency: {tools.print_property(self.frequency)}"
        ret_val += f"\n{prefix}date_field: {tools.print_property(self.date_field)}"
        ret_val += f"\n{prefix}group_dimension: {tools.print_property(self.group_dimension)}"
        ret_val += f"\n{prefix[0:-2]}└─top: {tools.print_property(self.top)}"
        return ret_val


    # Getter and Setter methods
    @property
    def frequency(self) -> str:
        """Get the frequency value."""
        return self._frequency

    @frequency.setter
    def frequency(self, value: str) -> None:
        """Set the frequency value with validation."""
        tools.validate_type(value, str, "Unexpected value for frequency")
        value = value.upper().strip()
        tools.validate_field_options(value, const.API_DATETIME_PERIODS)
        self._frequency = value

    @property
    def date_field(self) -> str:
        """Get the date_field value."""
        return self._date_field

    @date_field.setter
    def date_field(self, value: str) -> None:
        """Set the date_field value with validation."""
        tools.validate_type(value, str, "Unexpected value for date_field")
        value = value.lower().strip()
        tools.validate_field_options(value, const.API_DATETIME_FIELDS)
        self._date_field = value

    @property
    def group_dimension(self) -> list[Any] | str:
        """Get the group_dimension value."""
        return self._group_dimension

    @group_dimension.setter
    def group_dimension(self, value: Optional[list[Any] | str]) -> None:
        """Set the group_dimension value with validation.
        
        If value is a string, sets it directly.
        If value is a list/array, sets only the first value.
        """
        if value:
            # Handle string case
            if isinstance(value, str):
                if value in const.API_GROUP_DIMENSIONS_FIELDS:
                    self._group_dimension = value
                else:
                    raise ValueError('Group dimension is not valid')
            # Handle list/array case - use first value
            elif isinstance(value, (list, tuple)) and len(value) > 0:
                first_value = value[0]
                if isinstance(first_value, str) and first_value in const.API_GROUP_DIMENSIONS_FIELDS:
                    self._group_dimension = first_value
                else:
                    raise ValueError('Group dimension is not valid')
            else:
                raise ValueError('Group dimension must be a string or non-empty list/array')
        else:
            self._group_dimension = []

    @property
    def top(self) -> Optional[int]:
        """Get the top value."""
        return self._top

    @top.setter
    def top(self, value: int) -> None:
        """Set the top value with validation."""
        tools.validate_type(value, int, "Unexpected value for top")
        if value >= -1:
            self._top = value
        else:
            raise ValueError('Top value must be an ingeger greater than or equal to -1')



class SnapshotTimeSeries(SnapshotBase):
    """
    Main class to interact with the Time Series service from Factiva Analytics.

    Attributes
    ----------
    user_key : UserKey
        User representation for service authentication
    query : SnapshotExtractionQuery
        Query object tailored for Extraction operations
    job_response : SnapshotExtractionJobReponse
        Object containing job status and execution details

    """

    from typing import Optional

    query : Optional[SnapshotTimeSeriesQuery] = None
    job_response : Optional[SnapshotTimeSeriesJobReponse] = None

    def __init__(
        self,
        job_id=None,
        user_key=None,
        query: Optional[SnapshotBaseQuery] = None
    ):
        super().__init__(user_key=user_key, query=query, job_id=job_id)
        self.__log = log.get_factiva_logger()
        self.__JOB_BASE_URL = f"{const.API_HOST}{const.API_ANALYTICS_BASEPATH}"

        if job_id:
            self.__log.info(f"Creating SnapshotTimeSeries instance with JobID {job_id}")
            self.job_response = SnapshotTimeSeriesJobReponse(job_id)
            self.get_job_response()
        elif query:
            if isinstance(query, SnapshotTimeSeriesQuery):
                self.query = query
            elif isinstance(query, str):
                self.query = SnapshotTimeSeriesQuery(query)
            else:
                raise ValueError('Unexpected query type')
        else:
            self.query = SnapshotTimeSeriesQuery()  # type: ignore[assignment]
        self.__log.info('SnapshotExtraction created OK')



    @log.factiva_logger
    def submit_job(self, payload=None):
        """
        Performs a POST request to the API using the assigned query to start
        a TimeSeries job.

        If the job is initiated succesfully, results are assigned to the ``job_response``
        object. Otherwise any HTTP error will raise an exception.

        Returns
        -------
        bool
            True if the submission was successful. An Exception otherwise.

        """
        self.__log.info('submit_job Start')
        if not self.query:
            raise ValueError('A query is needed to submit an Explain Job')

        if not self.user_key:
            raise ValueError('User key is required for API requests')
            
        headers_dict = {
                'user-key': self.user_key.key,
                'Content-Type': 'application/json'
            }
        
        submit_url = f"{self.__JOB_BASE_URL}"
        submit_payload = self.query.get_payload()

        response = req.api_send_request(method='POST', endpoint_url=submit_url, headers=headers_dict, payload=submit_payload)

        if response.status_code == 201:
            response_data = response.json()
            self.job_response = SnapshotTimeSeriesJobReponse(response_data["data"]["id"])  # type: ignore[assignment]
            self.job_response.job_state = response_data['data']['attributes']['current_state']
            self.job_response.job_link = response_data['links']['self']
            if 'errors' in response_data.keys():
                self.job_response.errors = response_data['errors']
        elif response.status_code == 400:
            raise ValueError(f"Invalid Query [{response.text}]")
        else:
            raise RuntimeError(f"API request returned an unexpected HTTP status, with content [{response.text}]")
        self.__log.info('submit_job End')
        return True


    @log.factiva_logger
    def get_job_response(self) -> bool:
        """
        Performs a request to the API using the job ID to get its status.

        If the job has been completed, results are assigned to the ``job_response`` object.

        Returns
        -------
        bool
            True if the get request was successful. An Exception otherwise.

        """
        self.__log.info('get_job_response Start')

        if (not self.job_response):
            raise RuntimeError('Job has not yet been submitted or Job ID was not set')

        if not self.user_key:
            raise ValueError('User key is required for API requests')
            
        headers_dict = {
            'user-key': self.user_key.key,
            'Content-Type': 'application/json'
        }

        self.__log.info(f"Requesting Analytics Job info for ID {self.job_response.job_id}")
        getinfo_url = f"{self.__JOB_BASE_URL}/{self.job_response.job_id}"
        response = req.api_send_request(method='GET', endpoint_url=getinfo_url, headers=headers_dict)

        if response.status_code == 422:
            headers_dict.update(
                {'X-API-VERSION': '2.0'}
            )
            self.__log.info(f"Retrying get Analytics Job info with X-API-VERSION 2.0 info for ID {self.job_response.job_id}")
            response = req.api_send_request(method='GET', endpoint_url=getinfo_url, headers=headers_dict)

        if response.status_code == 200:
            self.__log.info(f"Job ID {self.job_response.job_id} info retrieved successfully")
            response_data = response.json()
            self.job_response.job_state = response_data['data']['attributes']['current_state']
            self.job_response.job_link = response_data['links']['self']
            if self.job_response.job_state == const.API_JOB_DONE_STATE:
                if 'results' in response_data['data']['attributes'].keys():
                    self.job_response.data = pd.DataFrame(response_data['data']['attributes']['results'])
                else:
                    self.job_response.download_link = response_data['data']['attributes']['download_link']
            if 'errors' in response_data.keys():
                self.job_response.errors = response_data['errors']
        elif response.status_code == 404:
            raise RuntimeError('Job ID does not exist.')
        elif response.status_code == 400:
            detail = response.json()['errors'][0]['detail']
            raise ValueError(f"Bad Request: {detail}")
        else:
            raise RuntimeError(f"API request returned an unexpected HTTP status, with content [{response.text}]")
        if self.job_response.download_link:
            self.__log.info(f"Downloading TimeSeries response file from {self.job_response.download_link.split('/')[-1]}")
            response = req.api_send_request(method='GET', endpoint_url=self.job_response.download_link, headers=headers_dict)
            if response.status_code == 200:
                decoded_response = response.content.decode('utf-8')
                jsonl_io = StringIO(decoded_response)
                self.job_response.data = pd.read_json(jsonl_io, lines=True)
            else:
                raise RuntimeError(f"TimeSeries results file download error: [{response.text}]")
        self.__log.info('get_job_response End')
        return True


    def process_job(self):  # TODO: Implement Retries if a 500 or timeout is returned during the active wait
        """
        Submit a new job to be processed, wait until the job is completed
        and then retrieves the job results.

        Returns
        -------
        bool
            True if the explain processing was successful. An Exception
            otherwise.

        """
        self.__log.info('process_job Start')
        self.submit_job()
        self.get_job_response()

        if not self.job_response:
            raise RuntimeError('Job response is not available')
            
        while not (self.job_response.job_state in
                    [const.API_JOB_DONE_STATE,
                     const.API_JOB_FAILED_STATE]
                  ):
            if self.job_response.job_state not in const.API_JOB_EXPECTED_STATES:
                raise RuntimeError('Unexpected job state')
            # if self.job_response.job_state == const.API_JOB_FAILED_STATE:
            #     raise Exception('Job failed')
            time.sleep(const.API_JOB_ACTIVE_WAIT_SPACING)
            self.get_job_response()
        
        self.__log.info('process_job End')
        return True


    def __repr__(self):
        return super().__repr__()


    def __str__(self, detailed=True, prefix='  ├─', root_prefix=''):
        ret_val = super().__str__(detailed, prefix, root_prefix)
        ret_val = ret_val.replace('├─job_response', '└─job_response')
        return ret_val
