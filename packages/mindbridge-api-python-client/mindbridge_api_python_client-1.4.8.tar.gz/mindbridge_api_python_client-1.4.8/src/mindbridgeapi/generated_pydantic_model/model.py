#
#  Copyright MindBridge Analytics Inc. all rights reserved.
#
#  This material is confidential and may not be copied, distributed,
#  reversed engineered, decompiled or otherwise disseminated without
#  the prior written consent of MindBridge Analytics Inc.
#

from __future__ import annotations
from datetime import date
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, RootModel
from typing_extensions import Annotated


class Type(str, Enum):
    """
    The type of account group error.
    """

    ERROR_INVALID_INDUSTRY_TAG = "ERROR_INVALID_INDUSTRY_TAG"
    ERROR_LOWEST_LEVEL_WITH_NO_MAC = "ERROR_LOWEST_LEVEL_WITH_NO_MAC"
    ERROR_LOWEST_LEVEL_WITHOUT_LEVEL_4_MAC = "ERROR_LOWEST_LEVEL_WITHOUT_LEVEL_4_MAC"
    ERROR_INCONSISTENT_SHEET_HIERARCHY = "ERROR_INCONSISTENT_SHEET_HIERARCHY"


class ApiAccountGroupErrorRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    arguments: Annotated[
        Optional[List[str]],
        Field(
            None,
            description="A list of values relevant to the type of account group error.",
        ),
    ]
    type: Annotated[
        Optional[Type], Field(None, description="The type of account group error.")
    ]


class ApiAccountGroupRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    account_grouping_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="accountGroupingId",
            description="The unique identifier for the account grouping that the account group belongs to.",
        ),
    ]
    account_tags: Annotated[
        Optional[List[str]],
        Field(
            None,
            alias="accountTags",
            description="A list of account tags assigned to this account group.",
        ),
    ]
    code: Annotated[
        Optional[str],
        Field(None, description="The account code for this account group."),
    ]
    description: Annotated[
        Optional[Dict[str, str]],
        Field(
            None,
            description="A description of the account code for this account group.",
        ),
    ]
    errors: Annotated[
        Optional[List[ApiAccountGroupErrorRead]],
        Field(None, description="A list of errors associated with this account group."),
    ]
    hierarchy: Annotated[
        Optional[List[str]],
        Field(None, description="A list of the parent codes for this account group."),
    ]
    id: Annotated[
        Optional[str], Field(None, description="The unique object identifier.")
    ]
    industry_tags: Annotated[
        Optional[List[str]],
        Field(
            None,
            alias="industryTags",
            description="A list of industry tags assigned to this account group.",
        ),
    ]
    lowest_level: Annotated[Optional[bool], Field(None, alias="lowestLevel")]
    mac_code: Annotated[
        Optional[str],
        Field(
            None,
            alias="macCode",
            description="The MAC code mapped to this account group.",
        ),
    ]
    order_index: Annotated[
        Optional[int],
        Field(
            None,
            alias="orderIndex",
            description="The order in which this account group is displayed, relative to other account groups with the same parent.",
        ),
    ]
    parent_code: Annotated[
        Optional[str],
        Field(
            None,
            alias="parentCode",
            description="The parent code for this account group.",
        ),
    ]
    published_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="publishedDate",
            description="The date this account group was published. If not set, this account group is not published.\n\nPublished account groups cannot be updated.",
        ),
    ]


class ApiAccountGroupUpdate(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    account_tags: Annotated[
        Optional[List[str]],
        Field(
            None,
            alias="accountTags",
            description="A list of account tags assigned to this account group.",
        ),
    ]
    industry_tags: Annotated[
        Optional[List[str]],
        Field(
            None,
            alias="industryTags",
            description="A list of industry tags assigned to this account group.",
        ),
    ]
    mac_code: Annotated[
        Optional[str],
        Field(
            None,
            alias="macCode",
            description="The MAC code mapped to this account group.",
        ),
    ]


class PublishStatus(str, Enum):
    """
    The current status of the account grouping.
    """

    DRAFT = "DRAFT"
    UNPUBLISHED_CHANGES = "UNPUBLISHED_CHANGES"
    PUBLISHED = "PUBLISHED"


class ApiAccountGroupingUpdate(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    archived: Annotated[
        Optional[bool],
        Field(None, description="When `true`, the account grouping is archived."),
    ]
    name: Annotated[
        Optional[Dict[str, str]],
        Field(None, description="The name of the account grouping."),
    ]
    publish_status: Annotated[
        Optional[PublishStatus],
        Field(
            None,
            alias="publishStatus",
            description="The current status of the account grouping.",
        ),
    ]
    version: Annotated[
        Optional[int],
        Field(
            None, description="The data integrity version, to ensure data consistency."
        ),
    ]


class Frequency(str, Enum):
    """
    The frequency with which your client's financial data is reported.
    """

    ANNUAL = "ANNUAL"
    SEMI_ANNUAL = "SEMI_ANNUAL"
    QUARTERLY = "QUARTERLY"
    MONTHLY = "MONTHLY"
    THIRTEEN_PERIODS = "THIRTEEN_PERIODS"


class ApiAccountingPeriodCreateOnly(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    fiscal_start_day: Annotated[
        Optional[int],
        Field(
            None,
            alias="fiscalStartDay",
            description="The date of the month that the fiscal period begins.",
        ),
    ]
    fiscal_start_month: Annotated[
        Optional[int],
        Field(
            None,
            alias="fiscalStartMonth",
            description="The month that the fiscal period begins.",
        ),
    ]
    frequency: Annotated[
        Optional[Frequency],
        Field(
            None,
            description="The frequency with which your client's financial data is reported.",
        ),
    ]


class ApiAccountingPeriodRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    fiscal_start_day: Annotated[
        Optional[int],
        Field(
            None,
            alias="fiscalStartDay",
            description="The date of the month that the fiscal period begins.",
        ),
    ]
    fiscal_start_month: Annotated[
        Optional[int],
        Field(
            None,
            alias="fiscalStartMonth",
            description="The month that the fiscal period begins.",
        ),
    ]
    frequency: Annotated[
        Optional[Frequency],
        Field(
            None,
            description="The frequency with which your client's financial data is reported.",
        ),
    ]


class ApiAccountingPeriodUpdate(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    fiscal_start_day: Annotated[
        Optional[int],
        Field(
            None,
            alias="fiscalStartDay",
            description="The date of the month that the fiscal period begins.",
        ),
    ]
    fiscal_start_month: Annotated[
        Optional[int],
        Field(
            None,
            alias="fiscalStartMonth",
            description="The month that the fiscal period begins.",
        ),
    ]
    frequency: Annotated[
        Optional[Frequency],
        Field(
            None,
            description="The frequency with which your client's financial data is reported.",
        ),
    ]


class ApiAmbiguousColumnRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    ambiguous_formats: Annotated[
        Optional[List[str]],
        Field(
            None,
            alias="ambiguousFormats",
            description="A list of ambiguous formats detected.",
        ),
    ]
    position: Annotated[
        Optional[int],
        Field(None, description="The position of the column with the resolution."),
    ]
    selected_format: Annotated[
        Optional[str],
        Field(
            None,
            alias="selectedFormat",
            description="The data format to be used in case of ambiguity.",
        ),
    ]


class ApiAmbiguousColumnUpdate(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    position: Annotated[
        Optional[int],
        Field(None, description="The position of the column with the resolution."),
    ]
    selected_format: Annotated[
        Optional[str],
        Field(
            None,
            alias="selectedFormat",
            description="The data format to be used in case of ambiguity.",
        ),
    ]


class ApiAnalysisImportantColumnRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    column_name: Annotated[
        Optional[str],
        Field(
            None,
            alias="columnName",
            description="The name of the column as it appears in the imported file.",
        ),
    ]
    field: Annotated[
        Optional[str],
        Field(None, description="The name of the additional data column."),
    ]


class ApiAnalysisPeriodGapRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    analysis_period_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="analysisPeriodId",
            description="Identifies the analysis period.",
        ),
    ]
    days: Annotated[
        Optional[int],
        Field(None, description="The number of days between two analysis periods."),
    ]
    previous_analysis_period_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="previousAnalysisPeriodId",
            description="Identifies the previous analysis period relevant to the current analysis period.",
        ),
    ]


class ApiAnalysisPeriodCreateOnly(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    end_date: Annotated[
        Optional[date],
        Field(
            None,
            alias="endDate",
            description="The last day of the period under analysis.",
        ),
    ]
    interim_as_at_date: Annotated[
        Optional[date],
        Field(
            None,
            alias="interimAsAtDate",
            description="The last day of the interim period under analysis.",
        ),
    ]
    start_date: Annotated[
        Optional[date],
        Field(
            None,
            alias="startDate",
            description="The first day of the period under analysis.",
        ),
    ]


class ApiAnalysisPeriodRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    end_date: Annotated[
        Optional[date],
        Field(
            None,
            alias="endDate",
            description="The last day of the period under analysis.",
        ),
    ]
    id: Annotated[
        Optional[str], Field(None, description="The unique object identifier.")
    ]
    interim_as_at_date: Annotated[
        Optional[date],
        Field(
            None,
            alias="interimAsAtDate",
            description="The last day of the interim period under analysis.",
        ),
    ]
    start_date: Annotated[
        Optional[date],
        Field(
            None,
            alias="startDate",
            description="The first day of the period under analysis.",
        ),
    ]


class ApiAnalysisPeriodUpdate(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    end_date: Annotated[
        Optional[date],
        Field(
            None,
            alias="endDate",
            description="The last day of the period under analysis.",
        ),
    ]
    id: Annotated[
        Optional[str], Field(None, description="The unique object identifier.")
    ]
    interim_as_at_date: Annotated[
        Optional[date],
        Field(
            None,
            alias="interimAsAtDate",
            description="The last day of the interim period under analysis.",
        ),
    ]
    start_date: Annotated[
        Optional[date],
        Field(
            None,
            alias="startDate",
            description="The first day of the period under analysis.",
        ),
    ]


class Status(str, Enum):
    """
    The current state of the analysis source.
    """

    IMPORTING = "IMPORTING"
    UPLOADING = "UPLOADING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"


class ApiAnalysisSourceStatusRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    analysis_source_type_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="analysisSourceTypeId",
            description="Identifies the analysis source type.",
        ),
    ]
    period_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="periodId",
            description="Identifies the analysis period within the analysis.",
        ),
    ]
    source_id: Annotated[
        Optional[str],
        Field(
            None, alias="sourceId", description="Identifies the analysis source object."
        ),
    ]
    status: Annotated[
        Optional[Status],
        Field(None, description="The current state of the analysis source."),
    ]


class Feature(str, Enum):
    FORMAT_DETECTION = "FORMAT_DETECTION"
    DATA_VALIDATION = "DATA_VALIDATION"
    COLUMN_MAPPING = "COLUMN_MAPPING"
    EFFECTIVE_DATE_METRICS = "EFFECTIVE_DATE_METRICS"
    TRANSACTION_ID_SELECTION = "TRANSACTION_ID_SELECTION"
    PARSE = "PARSE"
    CONFIRM_SETTINGS = "CONFIRM_SETTINGS"
    REVIEW_FUNDS = "REVIEW_FUNDS"


class TargetWorkflowState(str, Enum):
    """
    The state that the current workflow will advance to.
    """

    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"
    STARTED = "STARTED"
    DETECTING_FORMAT = "DETECTING_FORMAT"
    ANALYZING_COLUMNS = "ANALYZING_COLUMNS"
    CHECKING_INTEGRITY = "CHECKING_INTEGRITY"
    PARSING = "PARSING"
    ANALYZING_EFFECTIVE_DATE_METRICS = "ANALYZING_EFFECTIVE_DATE_METRICS"
    FORMAT_DETECTION_COMPLETED = "FORMAT_DETECTION_COMPLETED"
    COLUMN_MAPPINGS_CONFIRMED = "COLUMN_MAPPINGS_CONFIRMED"
    SETTINGS_CONFIRMED = "SETTINGS_CONFIRMED"
    ANALYSIS_PERIOD_SELECTED = "ANALYSIS_PERIOD_SELECTED"
    FUNDS_REVIEWED = "FUNDS_REVIEWED"
    RUNNING = "RUNNING"
    UNPACK_COMPLETE = "UNPACK_COMPLETE"
    UPLOADED = "UPLOADED"
    FORMAT_DETECTED = "FORMAT_DETECTED"
    COLUMNS_ANALYZED = "COLUMNS_ANALYZED"
    INTEGRITY_CHECKED = "INTEGRITY_CHECKED"
    PARSED = "PARSED"
    AUTHENTICATED = "AUTHENTICATED"
    CONFIGURED = "CONFIGURED"
    EFFECTIVE_DATE_METRICS_ANALYZED = "EFFECTIVE_DATE_METRICS_ANALYZED"
    DATA_VALIDATION_CONFIRMED = "DATA_VALIDATION_CONFIRMED"


class DetectedFormat(str, Enum):
    """
    The data format that MindBridge detected.
    """

    QUICKBOOKS_JOURNAL = "QUICKBOOKS_JOURNAL"
    QUICKBOOKS_JOURNAL_2024 = "QUICKBOOKS_JOURNAL_2024"
    QUICKBOOKS_TRANSACTION_DETAIL_BY_ACCOUNT = (
        "QUICKBOOKS_TRANSACTION_DETAIL_BY_ACCOUNT"
    )
    SAGE50_LEDGER = "SAGE50_LEDGER"
    SAGE50_TRANSACTIONS = "SAGE50_TRANSACTIONS"
    CCH_ACCOUNT_LIST = "CCH_ACCOUNT_LIST"


class WorkflowState(str, Enum):
    """
    The current state of the workflow.
    """

    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"
    STARTED = "STARTED"
    DETECTING_FORMAT = "DETECTING_FORMAT"
    ANALYZING_COLUMNS = "ANALYZING_COLUMNS"
    CHECKING_INTEGRITY = "CHECKING_INTEGRITY"
    PARSING = "PARSING"
    ANALYZING_EFFECTIVE_DATE_METRICS = "ANALYZING_EFFECTIVE_DATE_METRICS"
    FORMAT_DETECTION_COMPLETED = "FORMAT_DETECTION_COMPLETED"
    COLUMN_MAPPINGS_CONFIRMED = "COLUMN_MAPPINGS_CONFIRMED"
    SETTINGS_CONFIRMED = "SETTINGS_CONFIRMED"
    ANALYSIS_PERIOD_SELECTED = "ANALYSIS_PERIOD_SELECTED"
    FUNDS_REVIEWED = "FUNDS_REVIEWED"
    RUNNING = "RUNNING"
    UNPACK_COMPLETE = "UNPACK_COMPLETE"
    UPLOADED = "UPLOADED"
    FORMAT_DETECTED = "FORMAT_DETECTED"
    COLUMNS_ANALYZED = "COLUMNS_ANALYZED"
    INTEGRITY_CHECKED = "INTEGRITY_CHECKED"
    PARSED = "PARSED"
    AUTHENTICATED = "AUTHENTICATED"
    CONFIGURED = "CONFIGURED"
    EFFECTIVE_DATE_METRICS_ANALYZED = "EFFECTIVE_DATE_METRICS_ANALYZED"
    DATA_VALIDATION_CONFIRMED = "DATA_VALIDATION_CONFIRMED"


class PreflightError(str, Enum):
    IN_PROGRESS = "IN_PROGRESS"
    NOT_READY = "NOT_READY"
    ARCHIVED = "ARCHIVED"
    REQUIRED_FILES_MISSING = "REQUIRED_FILES_MISSING"
    SOURCES_NOT_READY = "SOURCES_NOT_READY"
    SOURCE_ERROR = "SOURCE_ERROR"
    UNVERIFIED_ACCOUNT_MAPPINGS = "UNVERIFIED_ACCOUNT_MAPPINGS"
    ANALYSIS_PERIOD_OVERLAP = "ANALYSIS_PERIOD_OVERLAP"
    SOURCE_WARNINGS_PRESENT = "SOURCE_WARNINGS_PRESENT"


class Status1(str, Enum):
    """
    The current state of the analysis.
    """

    NOT_STARTED = "NOT_STARTED"
    IMPORTING_FILE = "IMPORTING_FILE"
    PREPARING_DATA = "PREPARING_DATA"
    PROCESSING = "PROCESSING"
    CONSOLIDATING_RESULTS = "CONSOLIDATING_RESULTS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class ApiAnalysisStatusRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    analysis_id: Annotated[
        Optional[str],
        Field(
            None, alias="analysisId", description="Identifies the associated analysis."
        ),
    ]
    analysis_type_id: Annotated[
        Optional[str],
        Field(
            None, alias="analysisTypeId", description="Identifies the type of analysis."
        ),
    ]
    available_features: Annotated[
        Optional[Dict[str, bool]],
        Field(
            None,
            alias="availableFeatures",
            description="Details about the various analysis capabilities available in MindBridge. [Learn more](https://support.mindbridge.ai/hc/en-us/articles/360056395234)",
        ),
    ]
    inferred_account_mapping_count: Annotated[
        Optional[int],
        Field(
            None,
            alias="inferredAccountMappingCount",
            description="The number of inferred account mapping; this can be considered a warning on partial matches.",
        ),
    ]
    mapped_account_mapping_count: Annotated[
        Optional[int],
        Field(
            None,
            alias="mappedAccountMappingCount",
            description="The number of mapped accounts.",
        ),
    ]
    preflight_errors: Annotated[
        Optional[List[PreflightError]],
        Field(
            None,
            alias="preflightErrors",
            description="The errors that occurred before the analysis was run.",
        ),
    ]
    re_run_ready: Annotated[
        Optional[bool],
        Field(
            None,
            alias="reRunReady",
            description="Indicates whether or not the analysis is ready to be run again.",
        ),
    ]
    ready: Annotated[
        Optional[bool],
        Field(
            None,
            description="Indicates whether or not the analysis is ready to be run.",
        ),
    ]
    source_statuses: Annotated[
        Optional[List[ApiAnalysisSourceStatusRead]],
        Field(
            None,
            alias="sourceStatuses",
            description="Details about the state of each analysis source.",
        ),
    ]
    status: Annotated[
        Optional[Status1], Field(None, description="The current state of the analysis.")
    ]
    unmapped_account_mapping_count: Annotated[
        Optional[int],
        Field(
            None,
            alias="unmappedAccountMappingCount",
            description="The number of unmapped accounts.",
        ),
    ]


class ApiAnalysisCreateOnly(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    analysis_periods: Annotated[
        Optional[List[ApiAnalysisPeriodCreateOnly]],
        Field(
            None,
            alias="analysisPeriods",
            description="Details about the specific analysis periods under audit.",
        ),
    ]
    analysis_type_id: Annotated[
        Optional[str],
        Field(
            None, alias="analysisTypeId", description="Identifies the type of analysis."
        ),
    ]
    currency_code: Annotated[
        Optional[str],
        Field(
            None,
            alias="currencyCode",
            description="The currency to be displayed across the analysis results.",
        ),
    ]
    engagement_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="engagementId",
            description="Identifies the associated engagement.",
        ),
    ]
    interim: Annotated[
        Optional[bool],
        Field(
            None,
            description="Indicates whether or not the analysis is using an interim time frame.",
        ),
    ]
    name: Annotated[
        Optional[str],
        Field(
            None, description="The name of the analysis.", max_length=80, min_length=0
        ),
    ]
    periodic: Annotated[
        Optional[bool],
        Field(
            None,
            description="Indicates whether or not the analysis is using a periodic time frame.",
        ),
    ]


class ApiAnalysisUpdate(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    analysis_periods: Annotated[
        Optional[List[ApiAnalysisPeriodUpdate]],
        Field(
            None,
            alias="analysisPeriods",
            description="Details about the specific analysis periods under audit.",
        ),
    ]
    archived: Annotated[
        Optional[bool],
        Field(
            None, description="Indicates whether or not the analysis has been archived."
        ),
    ]
    currency_code: Annotated[
        Optional[str],
        Field(
            None,
            alias="currencyCode",
            description="The currency to be displayed across the analysis results.",
        ),
    ]
    name: Annotated[
        Optional[str],
        Field(
            None, description="The name of the analysis.", max_length=80, min_length=0
        ),
    ]
    version: Annotated[
        Optional[int],
        Field(
            None,
            description="Indicates the data integrity version to ensure data consistency.",
        ),
    ]


class Permission(str, Enum):
    API_ORGANIZATIONS_READ = "api.organizations.read"
    API_ORGANIZATIONS_WRITE = "api.organizations.write"
    API_ORGANIZATIONS_DELETE = "api.organizations.delete"
    API_ENGAGEMENTS_READ = "api.engagements.read"
    API_ENGAGEMENTS_WRITE = "api.engagements.write"
    API_ENGAGEMENTS_DELETE = "api.engagements.delete"
    API_ANALYSES_READ = "api.analyses.read"
    API_ANALYSES_WRITE = "api.analyses.write"
    API_ANALYSES_DELETE = "api.analyses.delete"
    API_ANALYSES_RUN = "api.analyses.run"
    API_ANALYSIS_SOURCES_READ = "api.analysis-sources.read"
    API_ANALYSIS_SOURCES_WRITE = "api.analysis-sources.write"
    API_ANALYSIS_SOURCES_DELETE = "api.analysis-sources.delete"
    API_FILE_MANAGER_READ = "api.file-manager.read"
    API_FILE_MANAGER_WRITE = "api.file-manager.write"
    API_FILE_MANAGER_DELETE = "api.file-manager.delete"
    API_LIBRARIES_READ = "api.libraries.read"
    API_LIBRARIES_WRITE = "api.libraries.write"
    API_LIBRARIES_DELETE = "api.libraries.delete"
    API_ACCOUNT_GROUPINGS_READ = "api.account-groupings.read"
    API_ACCOUNT_GROUPINGS_WRITE = "api.account-groupings.write"
    API_ACCOUNT_GROUPINGS_DELETE = "api.account-groupings.delete"
    API_ENGAGEMENT_ACCOUNT_GROUPINGS_READ = "api.engagement-account-groupings.read"
    API_ENGAGEMENT_ACCOUNT_GROUPINGS_WRITE = "api.engagement-account-groupings.write"
    API_ENGAGEMENT_ACCOUNT_GROUPINGS_DELETE = "api.engagement-account-groupings.delete"
    API_USERS_READ = "api.users.read"
    API_USERS_WRITE = "api.users.write"
    API_USERS_DELETE = "api.users.delete"
    API_DATA_TABLES_READ = "api.data-tables.read"
    API_API_TOKENS_READ = "api.api-tokens.read"
    API_API_TOKENS_WRITE = "api.api-tokens.write"
    API_API_TOKENS_DELETE = "api.api-tokens.delete"
    API_TASKS_READ = "api.tasks.read"
    API_TASKS_WRITE = "api.tasks.write"
    API_TASKS_DELETE = "api.tasks.delete"
    API_ADMIN_REPORTS_RUN = "api.admin-reports.run"
    API_ANALYSIS_TYPES_READ = "api.analysis-types.read"
    API_ANALYSIS_SOURCE_TYPES_READ = "api.analysis-source-types.read"
    SCIM_USER_READ = "scim.user.read"
    SCIM_USER_WRITE = "scim.user.write"
    SCIM_USER_DELETE = "scim.user.delete"
    SCIM_USER_SCHEMA = "scim.user.schema"


class ApiApiTokenCreateOnly(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    allowed_addresses: Annotated[
        Optional[List[str]],
        Field(
            None,
            alias="allowedAddresses",
            description="Indicates the set of addresses that are allowed to use this token. If empty, any address may use it.",
        ),
    ]
    expiry: Annotated[
        Optional[AwareDatetime],
        Field(None, description="The day on which the API token expires."),
    ]
    name: Annotated[
        Optional[str],
        Field(
            None,
            description="The token record’s name. This will also be used as the API Token User’s name.",
        ),
    ]
    permissions: Annotated[
        Optional[List[Permission]],
        Field(
            None,
            description="The set of permissions that inform which endpoints this token is authorized to access.",
        ),
    ]


class ApiApiTokenUpdate(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    name: Annotated[
        Optional[str],
        Field(
            None,
            description="The token record’s name. This will also be used as the API Token User’s name.",
        ),
    ]
    version: Annotated[
        Optional[int],
        Field(
            None,
            description="Indicates the data integrity version to ensure data consistency.",
        ),
    ]


class EntityType(str, Enum):
    """
    Identifies the entity type used in the job.
    """

    ORGANIZATION = "ORGANIZATION"
    ENGAGEMENT = "ENGAGEMENT"
    ANALYSIS = "ANALYSIS"
    ANALYSIS_SOURCE = "ANALYSIS_SOURCE"
    FILE_RESULT = "FILE_RESULT"
    GDPDU_UNPACK_JOB = "GDPDU_UNPACK_JOB"
    ACCOUNT_GROUPING = "ACCOUNT_GROUPING"
    ENGAGEMENT_ACCOUNT_GROUPING = "ENGAGEMENT_ACCOUNT_GROUPING"


class Status2(str, Enum):
    """
    Indicates the current state of the job.
    """

    IN_PROGRESS = "IN_PROGRESS"
    COMPLETE = "COMPLETE"
    ERROR = "ERROR"


class Type1(str, Enum):
    """
    Indicates the type of job being run.
    """

    ANALYSIS_RUN = "ANALYSIS_RUN"
    ANALYSIS_SOURCE_INGESTION = "ANALYSIS_SOURCE_INGESTION"
    ADMIN_REPORT = "ADMIN_REPORT"
    DATA_TABLE_EXPORT = "DATA_TABLE_EXPORT"
    ANALYSIS_ROLL_FORWARD = "ANALYSIS_ROLL_FORWARD"
    GDPDU_UNPACK_JOB = "GDPDU_UNPACK_JOB"
    ACCOUNT_GROUPING_EXPORT = "ACCOUNT_GROUPING_EXPORT"


class State(str, Enum):
    PASS_ = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"


class ApiChunkedFilePart(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    offset: Annotated[
        Optional[int],
        Field(
            None,
            description="Indicates the start position of the file part in the chunked file.",
            ge=0,
        ),
    ]
    size: Annotated[
        Optional[int], Field(None, description="The size of the file part.", ge=0)
    ]


class ApiChunkedFilePartRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    offset: Annotated[
        Optional[int],
        Field(
            None,
            description="Indicates the start position of the file part in the chunked file.",
            ge=0,
        ),
    ]
    size: Annotated[
        Optional[int], Field(None, description="The size of the file part.", ge=0)
    ]


class ApiChunkedFileCreateOnly(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    name: Annotated[
        Optional[str], Field(None, description="The name of the chunked file.")
    ]
    size: Annotated[
        Optional[int], Field(None, description="The size of the chunked file.", ge=0)
    ]


class ApiColumnDateTimeFormatRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    custom_format_pattern: Annotated[
        Optional[str], Field(None, alias="customFormatPattern")
    ]
    sample_converted_values: Annotated[
        Optional[List[AwareDatetime]], Field(None, alias="sampleConvertedValues")
    ]
    sample_raw_values: Annotated[
        Optional[List[str]], Field(None, alias="sampleRawValues")
    ]
    selected: Optional[bool] = None


class Type3(str, Enum):
    """
    The type of data this column accepts.
    """

    TEXT = "TEXT"
    NUMBER = "NUMBER"
    DATE = "DATE"
    UNKNOWN = "UNKNOWN"
    FLOAT64 = "FLOAT64"


class ApiColumnDefinitionRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    allow_blanks: Annotated[
        Optional[bool],
        Field(
            None,
            alias="allowBlanks",
            description="Indicates whether or not this column allows the source column to contain blank values.",
        ),
    ]
    alternative_mappings: Annotated[
        Optional[List[str]],
        Field(
            None,
            alias="alternativeMappings",
            description="A list of alternative mappings, identified by their `mindbridgeFieldName`. If all of the alternatives are mapped, then this mapping’s `required` constraint is considered satisfied. \n\n**Note**: This column may not be mapped if any alternative is also mapped.",
        ),
    ]
    mindbridge_field_name: Annotated[
        Optional[str],
        Field(
            None,
            alias="mindbridgeFieldName",
            description="The internal name of the analysis source type’s column.",
        ),
    ]
    mindbridge_field_name_for_non_mac_groupings: Annotated[
        Optional[str],
        Field(
            None,
            alias="mindbridgeFieldNameForNonMacGroupings",
            description="The alternative column name when a non-MAC based account grouping is used.",
        ),
    ]
    required: Annotated[
        Optional[bool],
        Field(None, description="Indicates whether or not this column is required."),
    ]
    required_for_non_mac_groupings: Annotated[
        Optional[bool],
        Field(
            None,
            alias="requiredForNonMacGroupings",
            description="Indicates whether or not this column is required when using a non-MAC based account grouping.",
        ),
    ]
    type: Annotated[
        Optional[Type3],
        Field(None, description="The type of data this column accepts."),
    ]


class MappingType(str, Enum):
    """
    The method used to map the column.
    """

    AUTO = "AUTO"
    NOT_MAPPED = "NOT_MAPPED"
    MANUAL = "MANUAL"


class ApiColumnMappingRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    additional_column_name: Annotated[
        Optional[str],
        Field(
            None,
            alias="additionalColumnName",
            description="Additional columns of data that were added to the analysis.",
        ),
    ]
    field: Annotated[Optional[str], Field(None, description="The column name.")]
    mapping_type: Annotated[
        Optional[MappingType],
        Field(
            None, alias="mappingType", description="The method used to map the column."
        ),
    ]
    mindbridge_field: Annotated[
        Optional[str],
        Field(
            None,
            alias="mindbridgeField",
            description="The MindBridge field that the data column was mapped to.",
        ),
    ]
    position: Annotated[
        Optional[int], Field(None, description="The position of the column mapping.")
    ]


class ApiColumnMappingUpdate(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    additional_column_name: Annotated[
        Optional[str],
        Field(
            None,
            alias="additionalColumnName",
            description="Additional columns of data that were added to the analysis.",
        ),
    ]
    mindbridge_field: Annotated[
        Optional[str],
        Field(
            None,
            alias="mindbridgeField",
            description="The MindBridge field that the data column was mapped to.",
        ),
    ]
    position: Annotated[
        Optional[int], Field(None, description="The position of the column mapping.")
    ]


class ApiCsvConfiguration(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    delimiter: Annotated[
        Optional[str],
        Field(None, description="The character used to separate entries."),
    ]
    quote: Annotated[
        Optional[str],
        Field(None, description="The character used to encapsulate an entry."),
    ]
    quote_escape: Annotated[
        Optional[str],
        Field(
            None,
            alias="quoteEscape",
            description="The character used to escape the quote character.",
        ),
    ]
    quote_escape_escape: Annotated[
        Optional[str],
        Field(
            None,
            alias="quoteEscapeEscape",
            description="The character used to escape the quote escape character.",
        ),
    ]


class ApiCurrencyFormatRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    ambiguous_delimiters: Annotated[
        Optional[List[str]], Field(None, alias="ambiguousDelimiters")
    ]
    decimal_character: Annotated[Optional[str], Field(None, alias="decimalCharacter")]
    example: Optional[str] = None
    non_decimal_delimiters: Annotated[
        Optional[List[str]], Field(None, alias="nonDecimalDelimiters")
    ]


class ApiDataPreviewRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    column: Optional[int] = None
    data: Optional[str] = None
    row: Optional[int] = None


class Type4(str, Enum):
    """
    The type of data found in the column.
    """

    STRING = "STRING"
    DATE = "DATE"
    DATE_TIME = "DATE_TIME"
    BOOLEAN = "BOOLEAN"
    INT16 = "INT16"
    INT32 = "INT32"
    INT64 = "INT64"
    FLOAT32 = "FLOAT32"
    FLOAT64 = "FLOAT64"
    MONEY_100 = "MONEY_100"
    PERCENTAGE_FIXED_POINT = "PERCENTAGE_FIXED_POINT"
    ARRAY_STRINGS = "ARRAY_STRINGS"
    KEYWORD_SEARCH = "KEYWORD_SEARCH"
    OBJECTID = "OBJECTID"
    BOOLEAN_FLAGS = "BOOLEAN_FLAGS"
    MAP_SCALARS = "MAP_SCALARS"
    LEGACY_ACCOUNT_TAG_EFFECTS = "LEGACY_ACCOUNT_TAG_EFFECTS"


class ApiDataTableColumnRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    case_insensitive_prefix_search: Annotated[
        Optional[bool],
        Field(
            None,
            alias="caseInsensitivePrefixSearch",
            description="Indicates whether or not a case insensitive search can be performed on a prefix.",
        ),
    ]
    case_insensitive_substring_search: Annotated[
        Optional[bool],
        Field(
            None,
            alias="caseInsensitiveSubstringSearch",
            description="Indicates whether or not a case insensitive search can be performed on a substring.",
        ),
    ]
    contains_search: Annotated[
        Optional[bool],
        Field(
            None,
            alias="containsSearch",
            description="Indicates whether or not a value-based search can be performed.",
        ),
    ]
    equality_search: Annotated[
        Optional[bool],
        Field(
            None,
            alias="equalitySearch",
            description="Indicates whether or not a search can be performed based on two equal operands.",
        ),
    ]
    field: Annotated[Optional[str], Field(None, description="The column name.")]
    filter_only: Annotated[
        Optional[bool],
        Field(
            None,
            alias="filterOnly",
            description="Indicates whether a field can only be used as part of a filter.",
        ),
    ]
    keyword_search: Annotated[
        Optional[bool],
        Field(
            None,
            alias="keywordSearch",
            description="Indicates whether or not a keyword search can be performed.",
        ),
    ]
    nullable: Annotated[
        Optional[bool],
        Field(None, description="Indicates whether or not NULL values are allowed."),
    ]
    original_name: Annotated[
        Optional[str],
        Field(
            None,
            alias="originalName",
            description="The original field name entered by the user (from the original input file, risk score name, etc.)",
        ),
    ]
    range_search: Annotated[
        Optional[bool],
        Field(
            None,
            alias="rangeSearch",
            description="Indicates whether or not a search can be performed on a value-based comparison.",
        ),
    ]
    sortable: Annotated[
        Optional[bool],
        Field(
            None,
            description="Indicates whether or not the data table can be sorted by this column.",
        ),
    ]
    type: Annotated[
        Optional[Type4],
        Field(None, description="The type of data found in the column."),
    ]


class ApiDataTablePage(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    content: Optional[List[Dict[str, Dict[str, Any]]]] = None


class Direction(str, Enum):
    """
    How the column will be sorted.
    """

    ASC = "ASC"
    DESC = "DESC"


class ApiDataTableQuerySortOrder(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    direction: Annotated[
        Optional[Direction], Field(None, description="How the column will be sorted.")
    ]
    field: Annotated[Optional[str], Field(None, description="The data table column.")]


class ApiDataTableQuerySortOrderRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    direction: Annotated[
        Optional[Direction], Field(None, description="How the column will be sorted.")
    ]
    field: Annotated[Optional[str], Field(None, description="The data table column.")]


class ApiDataTableRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    analysis_id: Annotated[
        Optional[str],
        Field(
            None, alias="analysisId", description="Identifies the associated analysis."
        ),
    ]
    columns: Annotated[
        Optional[List[ApiDataTableColumnRead]],
        Field(None, description="Details about the data table columns."),
    ]
    engagement_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="engagementId",
            description="Identifies the associated engagement.",
        ),
    ]
    id: Annotated[
        Optional[str], Field(None, description="The unique object identifier.")
    ]
    logical_name: Annotated[
        Optional[str],
        Field(None, alias="logicalName", description="The name of the data table."),
    ]
    type: Annotated[Optional[str], Field(None, description="The type of data table.")]


class DetectedType(str, Enum):
    TEXT = "TEXT"
    NUMBER = "NUMBER"
    DATE = "DATE"
    UNKNOWN = "UNKNOWN"
    FLOAT64 = "FLOAT64"


class DominantType(str, Enum):
    TEXT = "TEXT"
    NUMBER = "NUMBER"
    DATE = "DATE"
    UNKNOWN = "UNKNOWN"
    FLOAT64 = "FLOAT64"


class ApiDensityMetricsRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    blanks: Optional[int] = None
    count: Optional[int] = None
    data_previews: Annotated[
        Optional[List[ApiDataPreviewRead]], Field(None, alias="dataPreviews")
    ]
    density: Optional[float] = None
    state: Optional[State] = None


class ApiDistinctValueMetricsRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    count: Optional[int] = None
    data_previews: Annotated[
        Optional[List[ApiDataPreviewRead]], Field(None, alias="dataPreviews")
    ]
    state: Optional[State] = None


class PeriodType(str, Enum):
    """
    Indicates the time period by which the histogram has been broken down.
    """

    DAY = "DAY"
    WEEK = "WEEK"
    MONTH = "MONTH"


class ApiEffectiveDateMetricsRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    credits_in_period: Annotated[
        Optional[int],
        Field(
            None,
            alias="creditsInPeriod",
            description="The total credit amount that occurred within the source period’s date range.",
        ),
    ]
    debits_in_period: Annotated[
        Optional[int],
        Field(
            None,
            alias="debitsInPeriod",
            description="The total debit amount that occurred within the source period’s date range.",
        ),
    ]
    entries_in_period: Annotated[
        Optional[int],
        Field(
            None,
            alias="entriesInPeriod",
            description="The number of entries that occurred within the source period’s date range.",
        ),
    ]
    entries_out_of_period: Annotated[
        Optional[int],
        Field(
            None,
            alias="entriesOutOfPeriod",
            description="The number of entries that occurred outside of the source period’s date range.",
        ),
    ]
    in_period_count_histogram: Annotated[
        Optional[Dict[str, int]],
        Field(
            None,
            alias="inPeriodCountHistogram",
            description="A map showing the total number of entries that occurred within each indicated date period.",
        ),
    ]
    out_of_period_count_histogram: Annotated[
        Optional[Dict[str, int]],
        Field(
            None,
            alias="outOfPeriodCountHistogram",
            description="A map showing the total number of entries that occurred outside of each indicated date period.",
        ),
    ]
    period_type: Annotated[
        Optional[PeriodType],
        Field(
            None,
            alias="periodType",
            description="Indicates the time period by which the histogram has been broken down.",
        ),
    ]


class ApiEngagementRollForwardRequest(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    analysis_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="analysisId",
            description="Identifies the analysis to roll forward.",
        ),
    ]
    interim: Annotated[
        Optional[bool],
        Field(
            None,
            description="When `true`, the new analysis period will use an interim time frame.",
        ),
    ]
    target_engagement_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="targetEngagementId",
            description="Identifies the engagement that the analysis will be rolled forward into.",
        ),
    ]


class ApiEngagementCreateOnly(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    accounting_package: Annotated[
        Optional[str],
        Field(
            None,
            alias="accountingPackage",
            description="The ERP or financial management system that your client is using.",
        ),
    ]
    accounting_period: Annotated[
        Optional[ApiAccountingPeriodCreateOnly], Field(None, alias="accountingPeriod")
    ]
    audit_period_end_date: Annotated[
        Optional[date],
        Field(
            None,
            alias="auditPeriodEndDate",
            description="The last day of the occurring audit.",
        ),
    ]
    auditor_ids: Annotated[
        Optional[List[str]],
        Field(
            None,
            alias="auditorIds",
            description="Identifies the users who will act as auditors in the engagement.",
        ),
    ]
    billing_code: Annotated[
        Optional[str],
        Field(
            None,
            alias="billingCode",
            description="A unique code that associates engagements and analyses with clients to ensure those clients are billed appropriately for MindBridge usage.",
        ),
    ]
    engagement_lead_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="engagementLeadId",
            description="Identifies the user who will lead the engagement.",
        ),
    ]
    industry: Annotated[
        Optional[str],
        Field(
            None, description="The type of industry that your client operates within."
        ),
    ]
    library_id: Annotated[
        Optional[str],
        Field(None, alias="libraryId", description="Identifies the library."),
    ]
    name: Annotated[
        Optional[str],
        Field(
            None, description="The name of the engagement.", max_length=80, min_length=0
        ),
    ]
    organization_id: Annotated[
        Optional[str],
        Field(None, alias="organizationId", description="Identifies the organization."),
    ]
    settings_based_on_engagement_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="settingsBasedOnEngagementId",
            description="Identifies the engagement that the settings are based on.",
        ),
    ]


class ApiEngagementUpdate(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    accounting_package: Annotated[
        Optional[str],
        Field(
            None,
            alias="accountingPackage",
            description="The ERP or financial management system that your client is using.",
        ),
    ]
    accounting_period: Annotated[
        Optional[ApiAccountingPeriodUpdate], Field(None, alias="accountingPeriod")
    ]
    audit_period_end_date: Annotated[
        Optional[date],
        Field(
            None,
            alias="auditPeriodEndDate",
            description="The last day of the occurring audit.",
        ),
    ]
    auditor_ids: Annotated[
        Optional[List[str]],
        Field(
            None,
            alias="auditorIds",
            description="Identifies the users who will act as auditors in the engagement.",
        ),
    ]
    billing_code: Annotated[
        Optional[str],
        Field(
            None,
            alias="billingCode",
            description="A unique code that associates engagements and analyses with clients to ensure those clients are billed appropriately for MindBridge usage.",
        ),
    ]
    engagement_lead_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="engagementLeadId",
            description="Identifies the user who will lead the engagement.",
        ),
    ]
    industry: Annotated[
        Optional[str],
        Field(
            None, description="The type of industry that your client operates within."
        ),
    ]
    name: Annotated[
        Optional[str],
        Field(
            None, description="The name of the engagement.", max_length=80, min_length=0
        ),
    ]
    version: Annotated[
        Optional[int],
        Field(
            None,
            description="Indicates the data integrity version to ensure data consistency.",
        ),
    ]


class ApiFileInfoRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    name: Annotated[Optional[str], Field(None, description="The name of the file.")]
    type: Annotated[
        Optional[str], Field(None, description="The file info entity type.")
    ]


class ApiFileManagerDirectoryCreateOnly(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    engagement_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="engagementId",
            description="Identifies the associated engagement.",
        ),
    ]
    name: Annotated[
        Optional[str], Field(None, description="The current name of the directory.")
    ]
    parent_file_manager_entity_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="parentFileManagerEntityId",
            description="Identifies the parent directory. If NULL, the directory is positioned at the root level.",
        ),
    ]


class Type5(str, Enum):
    """
    Indicates whether the object is a DIRECTORY or a FILE within the directory.
    """

    DIRECTORY = "DIRECTORY"
    FILE = "FILE"


class ApiFileManagerEntityUpdate(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    parent_file_manager_entity_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="parentFileManagerEntityId",
            description="Identifies the parent directory. If NULL, the directory is positioned at the root level.",
        ),
    ]
    type: Annotated[
        Optional[Type5],
        Field(
            None,
            description="Indicates whether the object is a DIRECTORY or a FILE within the directory.",
        ),
    ]
    version: Annotated[
        Optional[int],
        Field(
            None,
            description="Indicates the data integrity version to ensure data consistency.",
        ),
    ]


class ApiFileManagerFileCreateOnly(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    engagement_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="engagementId",
            description="Identifies the associated engagement.",
        ),
    ]
    name: Annotated[
        Optional[str],
        Field(
            None, description="The current name of the file, excluding the extension."
        ),
    ]
    parent_file_manager_entity_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="parentFileManagerEntityId",
            description="Identifies the parent directory. If NULL, the directory is positioned at the root level.",
        ),
    ]


class StatusEnum(str, Enum):
    MODIFIED = "MODIFIED"
    ROLLED_FORWARD = "ROLLED_FORWARD"


class ApiFileManagerFileUpdate(ApiFileManagerEntityUpdate):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    name: Annotated[
        Optional[str],
        Field(
            None, description="The current name of the file, excluding the extension."
        ),
    ]
    version: Annotated[
        int,
        Field(
            description="Indicates the data integrity version to ensure data consistency."
        ),
    ]


class ApiHistogramMetricsRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    count: Optional[int] = None
    data_previews: Annotated[
        Optional[List[ApiDataPreviewRead]], Field(None, alias="dataPreviews")
    ]
    histogram: Optional[Dict[str, int]] = None
    state: Optional[State] = None


class Type7(str, Enum):
    """
    The type of account grouping file being imported.
    """

    MINDBRIDGE_TEMPLATE = "MINDBRIDGE_TEMPLATE"
    CCH_GROUP_TRIAL_BALANCE = "CCH_GROUP_TRIAL_BALANCE"


class ApiImportAccountGroupingParamsCreateOnly(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    chunked_file_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="chunkedFileId",
            description="The unique identifier of the chunked file that contains the account grouping data.",
        ),
    ]
    name: Annotated[
        Optional[str], Field(None, description="The name of the new account grouping.")
    ]
    type: Annotated[
        Optional[Type7],
        Field(None, description="The type of account grouping file being imported."),
    ]


class ApiImportAccountGroupingParamsUpdate(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    chunked_file_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="chunkedFileId",
            description="The unique identifier of the chunked file that contains the account grouping data.",
        ),
    ]


class RiskScoreDisplay(str, Enum):
    """
    Determines whether risk scores will be presented as percentages (%), or using High, Medium, and Low label indicators.
    """

    HIGH_MEDIUM_LOW = "HIGH_MEDIUM_LOW"
    PERCENTAGE = "PERCENTAGE"


class ApiLibraryCreateOnly(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    account_grouping_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="accountGroupingId",
            description="Identifies the account grouping used.",
        ),
    ]
    analysis_type_ids: Annotated[
        Optional[List[str]],
        Field(
            None,
            alias="analysisTypeIds",
            description="Identifies the analysis types used in the library.",
        ),
    ]
    based_on_library_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="basedOnLibraryId",
            description="Identifies the library that the new library is based on. This may be a user-created library or a MindBridge system library.",
        ),
    ]
    control_point_selection_permission: Annotated[
        Optional[bool],
        Field(
            None,
            alias="controlPointSelectionPermission",
            description="When set to `true`, control points can be added or removed within each risk score.",
        ),
    ]
    control_point_settings_permission: Annotated[
        Optional[bool],
        Field(
            None,
            alias="controlPointSettingsPermission",
            description="When set to `true`, individual control point settings can be adjusted within each risk score.",
        ),
    ]
    control_point_weight_permission: Annotated[
        Optional[bool],
        Field(
            None,
            alias="controlPointWeightPermission",
            description="When set to `true`, the weight of each control point can be adjusted within each risk score.",
        ),
    ]
    convert_settings: Annotated[
        Optional[bool],
        Field(
            None,
            alias="convertSettings",
            description="Indicates whether or not settings from the selected base library should be converted for use with the selected account grouping.",
        ),
    ]
    default_delimiter: Annotated[
        Optional[str],
        Field(
            None,
            alias="defaultDelimiter",
            description="Identifies the default delimiter used in imported CSV files.",
        ),
    ]
    industry_tags: Annotated[
        Optional[List[str]],
        Field(
            None,
            alias="industryTags",
            description="The tags used to indicate the industry that your client operates in.",
        ),
    ]
    name: Annotated[
        Optional[str],
        Field(
            None,
            description="The current name of the library.",
            max_length=80,
            min_length=0,
        ),
    ]
    risk_score_and_groups_selection_permission: Annotated[
        Optional[bool],
        Field(
            None,
            alias="riskScoreAndGroupsSelectionPermission",
            description="When set to `true`, risk scores and groups can be disabled, and accounts associated with risk scores can be edited.",
        ),
    ]
    risk_score_display: Annotated[
        Optional[RiskScoreDisplay],
        Field(
            None,
            alias="riskScoreDisplay",
            description="Determines whether risk scores will be presented as percentages (%), or using High, Medium, and Low label indicators.",
        ),
    ]
    warnings_dismissed: Annotated[
        Optional[bool],
        Field(
            None,
            alias="warningsDismissed",
            description="When set to `true`, any conversion warnings for this library will not be displayed in the **Libraries** tab in the UI.",
        ),
    ]


class ApiLibraryUpdate(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    analysis_type_ids: Annotated[
        Optional[List[str]],
        Field(
            None,
            alias="analysisTypeIds",
            description="Identifies the analysis types used in the library.",
        ),
    ]
    archived: Annotated[
        Optional[bool],
        Field(
            None,
            description="Indicates whether or not the library is archived. Archived libraries cannot be selected when creating an engagement.",
        ),
    ]
    control_point_selection_permission: Annotated[
        Optional[bool],
        Field(
            None,
            alias="controlPointSelectionPermission",
            description="When set to `true`, control points can be added or removed within each risk score.",
        ),
    ]
    control_point_settings_permission: Annotated[
        Optional[bool],
        Field(
            None,
            alias="controlPointSettingsPermission",
            description="When set to `true`, individual control point settings can be adjusted within each risk score.",
        ),
    ]
    control_point_weight_permission: Annotated[
        Optional[bool],
        Field(
            None,
            alias="controlPointWeightPermission",
            description="When set to `true`, the weight of each control point can be adjusted within each risk score.",
        ),
    ]
    default_delimiter: Annotated[
        Optional[str],
        Field(
            None,
            alias="defaultDelimiter",
            description="Identifies the default delimiter used in imported CSV files.",
        ),
    ]
    name: Annotated[
        Optional[str],
        Field(
            None,
            description="The current name of the library.",
            max_length=80,
            min_length=0,
        ),
    ]
    risk_score_and_groups_selection_permission: Annotated[
        Optional[bool],
        Field(
            None,
            alias="riskScoreAndGroupsSelectionPermission",
            description="When set to `true`, risk scores and groups can be disabled, and accounts associated with risk scores can be edited.",
        ),
    ]
    risk_score_display: Annotated[
        Optional[RiskScoreDisplay],
        Field(
            None,
            alias="riskScoreDisplay",
            description="Determines whether risk scores will be presented as percentages (%), or using High, Medium, and Low label indicators.",
        ),
    ]
    version: Annotated[
        Optional[int],
        Field(
            None,
            description="Indicates the data integrity version to ensure data consistency.",
        ),
    ]
    warnings_dismissed: Annotated[
        Optional[bool],
        Field(
            None,
            alias="warningsDismissed",
            description="When set to `true`, any conversion warnings for this library will not be displayed in the **Libraries** tab in the UI.",
        ),
    ]


class ApiMessageRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    code: Annotated[
        Optional[str], Field(None, description="Identifies the message type.")
    ]
    default_message: Annotated[
        Optional[str],
        Field(
            None,
            alias="defaultMessage",
            description="The message as it appears in MindBridge.",
        ),
    ]


class ApiOrganizationCreateOnly(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    external_client_code: Annotated[
        Optional[str],
        Field(
            None,
            alias="externalClientCode",
            description="The unique client ID applied to this organization.",
            max_length=80,
            min_length=0,
        ),
    ]
    manager_user_ids: Annotated[
        Optional[List[str]],
        Field(
            None,
            alias="managerUserIds",
            description="Identifies users assigned to the organization manager role.",
        ),
    ]
    name: Annotated[
        Optional[str],
        Field(
            None,
            description="The name of the organization.",
            max_length=80,
            min_length=0,
        ),
    ]


class ApiOrganizationUpdate(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    external_client_code: Annotated[
        Optional[str],
        Field(
            None,
            alias="externalClientCode",
            description="The unique client ID applied to this organization.",
            max_length=80,
            min_length=0,
        ),
    ]
    manager_user_ids: Annotated[
        Optional[List[str]],
        Field(
            None,
            alias="managerUserIds",
            description="Identifies users assigned to the organization manager role.",
        ),
    ]
    name: Annotated[
        Optional[str],
        Field(
            None,
            description="The name of the organization.",
            max_length=80,
            min_length=0,
        ),
    ]
    version: Annotated[
        Optional[int],
        Field(
            None,
            description="Indicates the data integrity version to ensure data consistency.",
        ),
    ]


class ApiOverallDataTypeMetricsRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    blank_records: Annotated[Optional[int], Field(None, alias="blankRecords")]
    cell_type_counts: Annotated[
        Optional[Dict[str, int]], Field(None, alias="cellTypeCounts")
    ]
    column_count: Annotated[Optional[int], Field(None, alias="columnCount")]
    column_type_counts: Annotated[
        Optional[Dict[str, int]], Field(None, alias="columnTypeCounts")
    ]
    data_previews: Annotated[
        Optional[List[ApiDataPreviewRead]], Field(None, alias="dataPreviews")
    ]
    state: Optional[State] = None
    total_records: Annotated[Optional[int], Field(None, alias="totalRecords")]
    total_rows: Annotated[Optional[int], Field(None, alias="totalRows")]


class ApiProposedAmbiguousColumnResolutionCreateOnly(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    position: Annotated[
        Optional[int],
        Field(
            None,
            description="The position of the column with the proposed resolution.",
            ge=0,
        ),
    ]
    selected_format: Annotated[
        Optional[str],
        Field(
            None,
            alias="selectedFormat",
            description="The selected format of the proposed resolution.",
        ),
    ]


class ApiProposedAmbiguousColumnResolutionRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    position: Annotated[
        Optional[int],
        Field(
            None,
            description="The position of the column with the proposed resolution.",
            ge=0,
        ),
    ]
    selected_format: Annotated[
        Optional[str],
        Field(
            None,
            alias="selectedFormat",
            description="The selected format of the proposed resolution.",
        ),
    ]


class ApiProposedAmbiguousColumnResolutionUpdate(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    position: Annotated[
        Optional[int],
        Field(
            None,
            description="The position of the column with the proposed resolution.",
            ge=0,
        ),
    ]
    selected_format: Annotated[
        Optional[str],
        Field(
            None,
            alias="selectedFormat",
            description="The selected format of the proposed resolution.",
        ),
    ]


class ApiProposedColumnMappingCreateOnly(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    additional_column_name: Annotated[
        Optional[str],
        Field(
            None,
            alias="additionalColumnName",
            description="Proposed additional columns of data to be added to the analysis.",
        ),
    ]
    column_position: Annotated[
        Optional[int],
        Field(
            None,
            alias="columnPosition",
            description="The position of the proposed column mapping in the original input file.",
        ),
    ]
    mindbridge_field: Annotated[
        Optional[str],
        Field(
            None,
            alias="mindbridgeField",
            description="The MindBridge field that the data column should be mapped to.",
        ),
    ]
    virtual_column_index: Annotated[
        Optional[int],
        Field(
            None,
            alias="virtualColumnIndex",
            description="The position of the proposed virtual columns within the `proposedVirtualColumns` list.",
        ),
    ]


class ApiProposedColumnMappingRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    additional_column_name: Annotated[
        Optional[str],
        Field(
            None,
            alias="additionalColumnName",
            description="Proposed additional columns of data to be added to the analysis.",
        ),
    ]
    column_position: Annotated[
        Optional[int],
        Field(
            None,
            alias="columnPosition",
            description="The position of the proposed column mapping in the original input file.",
        ),
    ]
    mindbridge_field: Annotated[
        Optional[str],
        Field(
            None,
            alias="mindbridgeField",
            description="The MindBridge field that the data column should be mapped to.",
        ),
    ]
    virtual_column_index: Annotated[
        Optional[int],
        Field(
            None,
            alias="virtualColumnIndex",
            description="The position of the proposed virtual columns within the `proposedVirtualColumns` list.",
        ),
    ]


class ApiProposedColumnMappingUpdate(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    additional_column_name: Annotated[
        Optional[str],
        Field(
            None,
            alias="additionalColumnName",
            description="Proposed additional columns of data to be added to the analysis.",
        ),
    ]
    column_position: Annotated[
        Optional[int],
        Field(
            None,
            alias="columnPosition",
            description="The position of the proposed column mapping in the original input file.",
        ),
    ]
    mindbridge_field: Annotated[
        Optional[str],
        Field(
            None,
            alias="mindbridgeField",
            description="The MindBridge field that the data column should be mapped to.",
        ),
    ]
    virtual_column_index: Annotated[
        Optional[int],
        Field(
            None,
            alias="virtualColumnIndex",
            description="The position of the proposed virtual columns within the `proposedVirtualColumns` list.",
        ),
    ]


class Type8(str, Enum):
    """
    The type of proposed virtual column.
    """

    DUPLICATE = "DUPLICATE"
    SPLIT_BY_POSITION = "SPLIT_BY_POSITION"
    SPLIT_BY_DELIMITER = "SPLIT_BY_DELIMITER"
    JOIN = "JOIN"


class ApiProposedVirtualColumnCreateOnly(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    name: Annotated[
        Optional[str],
        Field(None, description="The name of the proposed virtual column."),
    ]
    type: Annotated[
        Optional[Type8], Field(None, description="The type of proposed virtual column.")
    ]


class ApiProposedVirtualColumnRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    name: Annotated[
        Optional[str],
        Field(None, description="The name of the proposed virtual column."),
    ]
    type: Annotated[
        Optional[Type8], Field(None, description="The type of proposed virtual column.")
    ]


class ApiProposedVirtualColumnUpdate(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    name: Annotated[
        Optional[str],
        Field(None, description="The name of the proposed virtual column."),
    ]
    type: Annotated[
        Optional[Type8], Field(None, description="The type of proposed virtual column.")
    ]


class ApiSheetMetricsRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    count: Optional[int] = None
    data_previews: Annotated[
        Optional[List[ApiDataPreviewRead]], Field(None, alias="dataPreviews")
    ]
    sheet_names: Annotated[Optional[List[str]], Field(None, alias="sheetNames")]
    state: Optional[State] = None
    valid_sheets: Annotated[Optional[List[str]], Field(None, alias="validSheets")]


class SourceScope(str, Enum):
    """
    Indicates whether the source configuration applies to the current period, all of the prior periods, or the entire analysis.

    **Note**: Sources with an `ANALYSIS` scope should not provide an `analysisPeriodId`.
    """

    CURRENT_PERIOD = "CURRENT_PERIOD"
    PRIOR_PERIOD = "PRIOR_PERIOD"
    ANALYSIS = "ANALYSIS"


class ApiSourceConfigurationRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    allow_multiple: Annotated[
        Optional[bool],
        Field(
            None,
            alias="allowMultiple",
            description="When `true`, multiple versions of this analysis source type may be imported using this source scope.",
        ),
    ]
    allow_multiple_for_periodic: Annotated[
        Optional[bool],
        Field(
            None,
            alias="allowMultipleForPeriodic",
            description="When `true` and the periodic time frame is used, multiple versions of this analysis source type may be imported using this source scope.",
        ),
    ]
    alternative_required_source_types: Annotated[
        Optional[List[str]],
        Field(
            None,
            alias="alternativeRequiredSourceTypes",
            description="A list of alternative analysis source types. If one of the alternatives is present for this source scope, then the `required` constraint is considered satisfied.",
        ),
    ]
    disable_for_interim: Annotated[
        Optional[bool],
        Field(
            None,
            alias="disableForInterim",
            description="When `true` and the interim time frame is used (i.e., it has not been converted for use with a full time frame), new analysis sources of this source type and source scope cannot be added.",
        ),
    ]
    interim_only: Annotated[
        Optional[bool],
        Field(
            None,
            alias="interimOnly",
            description="When `true`, this source configuration only applies when the interim time frame is used (i.e., it has not been converted for use with a full time frame).",
        ),
    ]
    post_analysis: Annotated[
        Optional[bool],
        Field(
            None,
            alias="postAnalysis",
            description="When `true`, this source configuration will be enabled after an analysis is run (not before).",
        ),
    ]
    required: Annotated[
        Optional[bool],
        Field(
            None,
            description="When `true`, the analysis cannot be run until at least one analysis source with this source type in this source scope is present.",
        ),
    ]
    source_scope: Annotated[
        Optional[SourceScope],
        Field(
            None,
            alias="sourceScope",
            description="Indicates whether the source configuration applies to the current period, all of the prior periods, or the entire analysis.\n\n**Note**: Sources with an `ANALYSIS` scope should not provide an `analysisPeriodId`.",
        ),
    ]
    source_type_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="sourceTypeId",
            description="The source type ID selected as part of this configuration.",
        ),
    ]
    tracks_additional_data_entries: Annotated[
        Optional[bool],
        Field(
            None,
            alias="tracksAdditionalDataEntries",
            description="When `true`, the `additionalDataColumnField` field is required upon importing an analysis source type.",
        ),
    ]


class ApiTaskCommentCreateOnly(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    comment_text: Annotated[
        Optional[str],
        Field(None, alias="commentText", description="The text of the comment."),
    ]


class ApiTaskCommentRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    author_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="authorId",
            description="The unique identifier of the user who created this comment.",
        ),
    ]
    captured: Annotated[
        Optional[AwareDatetime],
        Field(None, description="The timestamp when this comment was made."),
    ]
    comment_text: Annotated[
        Optional[str],
        Field(None, alias="commentText", description="The text of the comment."),
    ]


class Status4(str, Enum):
    """
    The current state of the task.
    """

    OPEN = "OPEN"
    NORMAL = "NORMAL"
    RESOLVED = "RESOLVED"


class Type11(str, Enum):
    """
    The type of entry this task is associated with.
    """

    ENTRY = "ENTRY"
    TRANSACTION = "TRANSACTION"
    AP_ENTRY = "AP_ENTRY"
    AR_ENTRY = "AR_ENTRY"
    AP_OUTSTANDING_ENTRY = "AP_OUTSTANDING_ENTRY"
    AR_OUTSTANDING_ENTRY = "AR_OUTSTANDING_ENTRY"


class ApiTaskCreateOnly(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    analysis_id: Annotated[
        Optional[str],
        Field(
            None, alias="analysisId", description="Identifies the associated analysis."
        ),
    ]
    assertions: Annotated[
        Optional[List[str]],
        Field(None, description="Which assertions this task is associated with."),
    ]
    assigned_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="assignedId",
            description="Identifies the user assigned to this task.",
        ),
    ]
    audit_areas: Annotated[
        Optional[List[str]],
        Field(
            None,
            alias="auditAreas",
            description="Which audit areas this task is associated with.",
        ),
    ]
    description: Annotated[
        Optional[str], Field(None, description="A description of the task.")
    ]
    engagement_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="engagementId",
            description="Identifies the associated engagement.",
        ),
    ]
    row_id: Annotated[
        Optional[int],
        Field(None, alias="rowId", description="Identifies the associated entry."),
    ]
    sample: Annotated[
        Optional[str], Field(None, description="Which sample this task is a part of.")
    ]
    status: Annotated[
        Optional[Status4], Field(None, description="The current state of the task.")
    ]
    transaction_id: Annotated[
        Optional[int],
        Field(
            None,
            alias="transactionId",
            description="Identifies the associated transaction.",
        ),
    ]
    type: Annotated[
        Optional[Type11],
        Field(None, description="The type of entry this task is associated with."),
    ]


class SampleType(str, Enum):
    """
    The sampling method used to create this task.
    """

    RISK_BASED = "RISK_BASED"
    RANDOM = "RANDOM"
    MANUAL = "MANUAL"


class ApiTaskUpdate(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    assertions: Annotated[
        Optional[List[str]],
        Field(None, description="Which assertions this task is associated with."),
    ]
    assigned_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="assignedId",
            description="Identifies the user assigned to this task.",
        ),
    ]
    audit_areas: Annotated[
        Optional[List[str]],
        Field(
            None,
            alias="auditAreas",
            description="Which audit areas this task is associated with.",
        ),
    ]
    description: Annotated[
        Optional[str], Field(None, description="A description of the task.")
    ]
    sample: Annotated[
        Optional[str], Field(None, description="Which sample this task is a part of.")
    ]
    status: Annotated[
        Optional[Status4], Field(None, description="The current state of the task.")
    ]
    version: Annotated[
        Optional[int],
        Field(
            None,
            description="Indicates the data integrity version to ensure data consistency.",
        ),
    ]


class Rating(str, Enum):
    """
    The quality of the indicator as rated by MindBridge.
    """

    FAIL = "FAIL"
    POOR = "POOR"
    NEUTRAL = "NEUTRAL"
    GOOD = "GOOD"


class ApiTransactionIdPreviewRowRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    balance: Annotated[
        Optional[int], Field(None, description="The balance of the transaction.")
    ]
    detail_rows: Annotated[
        Optional[List[Dict[str, Dict[str, Any]]]],
        Field(
            None,
            alias="detailRows",
            description="The set of entries that appear within the transaction.",
        ),
    ]
    entry_count: Annotated[
        Optional[int],
        Field(
            None,
            alias="entryCount",
            description="The number of entries that appear within the transaction.",
        ),
    ]
    transaction_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="transactionId",
            description="Identifies the transaction ID for this transaction.",
        ),
    ]


class OverallRating(str, Enum):
    """
    The quality of the transaction ID as rated by MindBridge.
    """

    FAIL = "FAIL"
    POOR = "POOR"
    NEUTRAL = "NEUTRAL"
    GOOD = "GOOD"


class Type13(str, Enum):
    """
    The type used when selecting a transaction ID.
    """

    COMBINATION = "COMBINATION"
    RUNNING_TOTAL = "RUNNING_TOTAL"


class ApiTransactionIdSelectionCreateOnly(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    apply_smart_splitter: Annotated[
        Optional[bool],
        Field(
            None,
            alias="applySmartSplitter",
            description="Indicates whether or not the Smart Splitter was run when selecting a transaction ID.",
        ),
    ]
    column_selection: Annotated[
        Optional[List[int]],
        Field(
            None,
            alias="columnSelection",
            description="The columns included when selecting a transaction ID.",
        ),
    ]
    type: Annotated[
        Optional[Type13],
        Field(None, description="The type used when selecting a transaction ID."),
    ]
    virtual_column_selection: Annotated[
        Optional[List[int]],
        Field(
            None,
            alias="virtualColumnSelection",
            description="The virtual columns included when selecting a transaction ID.",
        ),
    ]


class ApiTransactionIdSelectionRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    apply_smart_splitter: Annotated[
        Optional[bool],
        Field(
            None,
            alias="applySmartSplitter",
            description="Indicates whether or not the Smart Splitter was run when selecting a transaction ID.",
        ),
    ]
    column_selection: Annotated[
        Optional[List[int]],
        Field(
            None,
            alias="columnSelection",
            description="The columns included when selecting a transaction ID.",
        ),
    ]
    type: Annotated[
        Optional[Type13],
        Field(None, description="The type used when selecting a transaction ID."),
    ]
    virtual_column_selection: Annotated[
        Optional[List[int]],
        Field(
            None,
            alias="virtualColumnSelection",
            description="The virtual columns included when selecting a transaction ID.",
        ),
    ]


class ApiTransactionIdSelectionUpdate(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    apply_smart_splitter: Annotated[
        Optional[bool],
        Field(
            None,
            alias="applySmartSplitter",
            description="Indicates whether or not the Smart Splitter was run when selecting a transaction ID.",
        ),
    ]
    column_selection: Annotated[
        Optional[List[int]],
        Field(
            None,
            alias="columnSelection",
            description="The columns included when selecting a transaction ID.",
        ),
    ]
    type: Annotated[
        Optional[Type13],
        Field(None, description="The type used when selecting a transaction ID."),
    ]
    virtual_column_selection: Annotated[
        Optional[List[int]],
        Field(
            None,
            alias="virtualColumnSelection",
            description="The virtual columns included when selecting a transaction ID.",
        ),
    ]


class ApiUserInfo(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    user_id: Annotated[
        Optional[str], Field(None, alias="userId", description="Identifies the user.")
    ]
    user_name: Annotated[
        Optional[str],
        Field(None, alias="userName", description="The name of the user."),
    ]


class ApiUserInfoRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    user_id: Annotated[
        Optional[str], Field(None, alias="userId", description="Identifies the user.")
    ]
    user_name: Annotated[
        Optional[str],
        Field(None, alias="userName", description="The name of the user."),
    ]


class Role(str, Enum):
    """
    The MindBridge role assigned to the user. [Learn about user roles](https://support.mindbridge.ai/hc/en-us/articles/360056394954-User-roles-available-in-MindBridge)
    """

    ROLE_ADMIN = "ROLE_ADMIN"
    ROLE_ORGANIZATION_ADMIN = "ROLE_ORGANIZATION_ADMIN"
    ROLE_USER = "ROLE_USER"
    ROLE_CLIENT = "ROLE_CLIENT"
    ROLE_MINDBRIDGE_SUPPORT = "ROLE_MINDBRIDGE_SUPPORT"
    ROLE_USER_ADMIN = "ROLE_USER_ADMIN"


class ApiUserCreateOnly(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    email: Annotated[
        Optional[str], Field(None, description="The user’s email address.")
    ]
    role: Annotated[
        Optional[Role],
        Field(
            None,
            description="The MindBridge role assigned to the user. [Learn about user roles](https://support.mindbridge.ai/hc/en-us/articles/360056394954-User-roles-available-in-MindBridge)",
        ),
    ]


class ApiUserRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    created_user_info: Annotated[
        Optional[ApiUserInfoRead], Field(None, alias="createdUserInfo")
    ]
    creation_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="creationDate",
            description="The date that the object was originally created.",
        ),
    ]
    email: Annotated[
        Optional[str], Field(None, description="The user’s email address.")
    ]
    enabled: Annotated[
        Optional[bool],
        Field(
            None,
            description="Indicates whether or not the user is enabled within this tenant.",
        ),
    ]
    first_name: Annotated[
        Optional[str],
        Field(None, alias="firstName", description="The user’s first name."),
    ]
    id: Annotated[
        Optional[str], Field(None, description="The unique object identifier.")
    ]
    last_modified_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="lastModifiedDate",
            description="The date that the object was last updated or modified.",
        ),
    ]
    last_modified_user_info: Annotated[
        Optional[ApiUserInfoRead], Field(None, alias="lastModifiedUserInfo")
    ]
    last_name: Annotated[
        Optional[str],
        Field(None, alias="lastName", description="The user’s last name."),
    ]
    role: Annotated[
        Optional[Role],
        Field(
            None,
            description="The MindBridge role assigned to the user. [Learn about user roles](https://support.mindbridge.ai/hc/en-us/articles/360056394954-User-roles-available-in-MindBridge)",
        ),
    ]
    service_account: Annotated[
        Optional[bool],
        Field(
            None,
            alias="serviceAccount",
            description="Indicates whether or not this account is used as part of an API token.",
        ),
    ]
    validated: Annotated[
        Optional[bool],
        Field(
            None,
            description="Indicates whether or not the user has opened the account activation link after being created.",
        ),
    ]
    version: Annotated[
        Optional[int],
        Field(
            None,
            description="Indicates the data integrity version to ensure data consistency.",
        ),
    ]


class ApiUserUpdate(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    enabled: Annotated[
        Optional[bool],
        Field(
            None,
            description="Indicates whether or not the user is enabled within this tenant.",
        ),
    ]
    role: Annotated[
        Optional[Role],
        Field(
            None,
            description="The MindBridge role assigned to the user. [Learn about user roles](https://support.mindbridge.ai/hc/en-us/articles/360056394954-User-roles-available-in-MindBridge)",
        ),
    ]
    version: Annotated[
        Optional[int],
        Field(
            None,
            description="Indicates the data integrity version to ensure data consistency.",
        ),
    ]


class Type17(str, Enum):
    """
    The type of virtual column.
    """

    DUPLICATE = "DUPLICATE"
    SPLIT_BY_POSITION = "SPLIT_BY_POSITION"
    SPLIT_BY_DELIMITER = "SPLIT_BY_DELIMITER"
    JOIN = "JOIN"


class ApiVirtualColumnRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    created_user_info: Annotated[
        Optional[ApiUserInfoRead], Field(None, alias="createdUserInfo")
    ]
    creation_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="creationDate",
            description="The date that the object was originally created.",
        ),
    ]
    id: Annotated[
        Optional[str], Field(None, description="The unique object identifier.")
    ]
    index: Annotated[
        Optional[int], Field(None, description="The position of the virtual column.")
    ]
    last_modified_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="lastModifiedDate",
            description="The date that the object was last updated or modified.",
        ),
    ]
    last_modified_user_info: Annotated[
        Optional[ApiUserInfoRead], Field(None, alias="lastModifiedUserInfo")
    ]
    name: Annotated[
        Optional[str], Field(None, description="The name of the virtual column.")
    ]
    type: Annotated[
        Optional[Type17], Field(None, description="The type of virtual column.")
    ]
    version: Annotated[
        Optional[int],
        Field(
            None,
            description="Indicates the data integrity version to ensure data consistency.",
        ),
    ]


class ApiVirtualColumnUpdate(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    name: Annotated[
        Optional[str], Field(None, description="The name of the virtual column.")
    ]
    type: Annotated[
        Optional[Type17], Field(None, description="The type of virtual column.")
    ]
    version: Annotated[
        Optional[int],
        Field(
            None,
            description="Indicates the data integrity version to ensure data consistency.",
        ),
    ]


class CreateApiTokenResponseRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    allowed_addresses: Annotated[
        Optional[List[str]],
        Field(
            None,
            alias="allowedAddresses",
            description="Indicates the set of addresses that are allowed to use this token. If empty, any address may use it.",
        ),
    ]
    created_user_info: Annotated[
        Optional[ApiUserInfoRead], Field(None, alias="createdUserInfo")
    ]
    creation_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="creationDate",
            description="The date that the object was originally created.",
        ),
    ]
    expiry: Annotated[
        Optional[AwareDatetime],
        Field(None, description="The day on which the API token expires."),
    ]
    id: Annotated[
        Optional[str], Field(None, description="The unique object identifier.")
    ]
    last_modified_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="lastModifiedDate",
            description="The date that the object was last updated or modified.",
        ),
    ]
    last_modified_user_info: Annotated[
        Optional[ApiUserInfoRead], Field(None, alias="lastModifiedUserInfo")
    ]
    name: Annotated[
        Optional[str],
        Field(
            None,
            description="The token record’s name. This will also be used as the API Token User’s name.",
        ),
    ]
    partial_token: Annotated[
        Optional[str],
        Field(
            None,
            alias="partialToken",
            description="A partial representation of the API token.",
        ),
    ]
    permissions: Annotated[
        Optional[List[Permission]],
        Field(
            None,
            description="The set of permissions that inform which endpoints this token is authorized to access.",
        ),
    ]
    token: Annotated[
        Optional[str],
        Field(
            None,
            description="The API token.\n\n**Note:** The security of the API token is paramount. If compromised, contact your **App Admin** immediately.",
        ),
    ]
    user_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="userId",
            description="Identifies the API Token User associated with this token.",
        ),
    ]
    version: Annotated[
        Optional[int],
        Field(
            None,
            description="Indicates the data integrity version to ensure data consistency.",
        ),
    ]


class MindBridgeQueryTerm1(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    field_eq: Annotated[
        Optional[Union[int, float, bool, str]], Field(None, alias="$eq")
    ]


class MindBridgeQueryTerm2(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    field_ne: Annotated[
        Optional[Union[int, float, bool, str]], Field(None, alias="$ne")
    ]


class MindBridgeQueryTerm3(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    field_gt: Annotated[Optional[Union[int, float, str]], Field(None, alias="$gt")]


class MindBridgeQueryTerm4(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    field_gte: Annotated[Optional[Union[int, float, str]], Field(None, alias="$gte")]


class MindBridgeQueryTerm5(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    field_lt: Annotated[Optional[Union[int, float, str]], Field(None, alias="$lt")]


class MindBridgeQueryTerm6(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    field_lte: Annotated[Optional[Union[int, float, str]], Field(None, alias="$lte")]


class MindBridgeQueryTerm7(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    field_contains: Annotated[Optional[List[str]], Field(None, alias="$contains")]


class MindBridgeQueryTerm9(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    field_in: Annotated[
        Optional[List[Union[int, float, bool, str]]], Field(None, alias="$in")
    ]


class MindBridgeQueryTerm10(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    field_nin: Annotated[
        Optional[List[Union[int, float, bool, str]]], Field(None, alias="$nin")
    ]


class MindBridgeQueryTerm11(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    field_flags: Annotated[Optional[Dict[str, bool]], Field(None, alias="$flags")]


class MindBridgeQueryTerm12(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    field_isubstr: Annotated[Optional[str], Field(None, alias="$isubstr")]


class MindBridgeQueryTerm13(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    field_iprefix: Annotated[Optional[str], Field(None, alias="$iprefix")]


class MindBridgeQueryTerm14(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    field_niprefix: Annotated[Optional[str], Field(None, alias="$niprefix")]


class MindBridgeQueryTerm17(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    field_keyword_prefix: Annotated[Optional[str], Field(None, alias="$keyword_prefix")]


class MindBridgeQueryTerm18(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    field_keyword_prefix_not: Annotated[
        Optional[str], Field(None, alias="$keyword_prefix_not")
    ]


class ProblemType(str, Enum):
    """
    The type of problem.
    """

    UNKNOWN = "UNKNOWN"
    ILLEGAL_ARGUMENT = "ILLEGAL_ARGUMENT"
    CANNOT_DELETE = "CANNOT_DELETE"
    GREATER_VALUE_REQUIRED = "GREATER_VALUE_REQUIRED"
    LESS_VALUE_REQUIRED = "LESS_VALUE_REQUIRED"
    NON_UNIQUE_VALUE = "NON_UNIQUE_VALUE"
    USER_EMAIL_ALREADY_EXISTS = "USER_EMAIL_ALREADY_EXISTS"
    INCORRECT_DATA_TYPE = "INCORRECT_DATA_TYPE"
    RATIO_CONVERSION_FAILED = "RATIO_CONVERSION_FAILED"
    RISK_SCORE_FILTER_CONVERSION_FAILED = "RISK_SCORE_FILTER_CONVERSION_FAILED"
    FILTER_CONVERSION_FAILED = "FILTER_CONVERSION_FAILED"
    POPULATION_CONVERSION_FAILED = "POPULATION_CONVERSION_FAILED"
    INSUFFICIENT_PERMISSION = "INSUFFICIENT_PERMISSION"
    ACCOUNT_GROUPING_NODES_CONTAIN_ERRORS = "ACCOUNT_GROUPING_NODES_CONTAIN_ERRORS"
    ACCOUNT_GROUPING_IN_USE_BY_LIBRARY = "ACCOUNT_GROUPING_IN_USE_BY_LIBRARY"
    INVALID_ACCOUNT_GROUPING_FILE = "INVALID_ACCOUNT_GROUPING_FILE"


class Severity(str, Enum):
    """
    Indicates how severe the error is.
    """

    WARNING = "WARNING"
    ERROR = "ERROR"


class Problem(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    entity_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="entityId",
            description="Identifies the entity impacted by the problem.",
        ),
    ]
    entity_type: Annotated[
        Optional[str],
        Field(
            None,
            alias="entityType",
            description="The type of entity impacted by the problem.",
        ),
    ]
    identifier: Annotated[
        Optional[str],
        Field(None, description="Identifies the field causing the problem."),
    ]
    problem_count: Annotated[
        Optional[int],
        Field(None, alias="problemCount", description="The total number of problems."),
    ]
    problem_type: Annotated[
        Optional[ProblemType],
        Field(None, alias="problemType", description="The type of problem."),
    ]
    reason: Annotated[
        Optional[str],
        Field(None, description="The reason(s) why the problem occurred."),
    ]
    severity: Annotated[
        Optional[Severity],
        Field(None, description="Indicates how severe the error is."),
    ]
    suggested_values: Annotated[
        Optional[List[str]],
        Field(
            None,
            alias="suggestedValues",
            description="A suggested set of values to assist in resolving the problem.",
        ),
    ]
    values: Annotated[
        Optional[List[str]],
        Field(None, description="Identifies the entity impacted by the error."),
    ]


class ProblemRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    entity_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="entityId",
            description="Identifies the entity impacted by the problem.",
        ),
    ]
    entity_type: Annotated[
        Optional[str],
        Field(
            None,
            alias="entityType",
            description="The type of entity impacted by the problem.",
        ),
    ]
    identifier: Annotated[
        Optional[str],
        Field(None, description="Identifies the field causing the problem."),
    ]
    problem_count: Annotated[
        Optional[int],
        Field(None, alias="problemCount", description="The total number of problems."),
    ]
    problem_type: Annotated[
        Optional[ProblemType],
        Field(None, alias="problemType", description="The type of problem."),
    ]
    reason: Annotated[
        Optional[str],
        Field(None, description="The reason(s) why the problem occurred."),
    ]
    severity: Annotated[
        Optional[Severity],
        Field(None, description="Indicates how severe the error is."),
    ]
    suggested_values: Annotated[
        Optional[List[str]],
        Field(
            None,
            alias="suggestedValues",
            description="A suggested set of values to assist in resolving the problem.",
        ),
    ]
    values: Annotated[
        Optional[List[str]],
        Field(None, description="Identifies the entity impacted by the error."),
    ]


class RangeBigDecimalRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    max: Optional[float] = None
    min: Optional[float] = None


class RangeIntegerRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    max: Optional[int] = None
    min: Optional[int] = None


class RangeZonedDateTimeRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    max: Optional[AwareDatetime] = None
    min: Optional[AwareDatetime] = None


class Category(str, Enum):
    ACCOUNT_GROUPING = "ACCOUNT_GROUPING"
    ACCOUNT_MAPPING = "ACCOUNT_MAPPING"
    ADMIN_REPORT = "ADMIN_REPORT"
    ANALYSIS_TYPE = "ANALYSIS_TYPE"
    API_TOKEN = "API_TOKEN"
    AUDIT_ANNOTATION = "AUDIT_ANNOTATION"
    CLOUD_ELEMENTS = "CLOUD_ELEMENTS"
    COLLECTION_ASSIGNMENT = "COLLECTION_ASSIGNMENT"
    ENGAGEMENT = "ENGAGEMENT"
    FILE_LOCKER = "FILE_LOCKER"
    FILE_MANAGER = "FILE_MANAGER"
    FILTER = "FILTER"
    GDPDU = "GDPDU"
    INGESTION = "INGESTION"
    INTEGRATIONS = "INTEGRATIONS"
    LIBRARY = "LIBRARY"
    MIGRATION = "MIGRATION"
    ORGANIZATION = "ORGANIZATION"
    POPULATION = "POPULATION"
    QUERY = "QUERY"
    RATIO = "RATIO"
    REPORT_BUILDER = "REPORT_BUILDER"
    REPORT = "REPORT"
    RESULTS_EXPORT = "RESULTS_EXPORT"
    RISK_RANGES = "RISK_RANGES"
    RISK_SEGMENTATION_DASHBOARD = "RISK_SEGMENTATION_DASHBOARD"
    SCIM_API = "SCIM_API"
    SUPPORT_ACCESS = "SUPPORT_ACCESS"
    TASK = "TASK"
    USER = "USER"
    WORKFLOW = "WORKFLOW"


class RunActivityReportRequestRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    categories: Annotated[
        Optional[List[Category]],
        Field(
            None,
            description="The categories to include in the report. If empty, all categories will be included.",
        ),
    ]
    end: Annotated[
        Optional[AwareDatetime],
        Field(None, description="The last date in the reporting timeframe."),
    ]
    only_completed_analyses: Annotated[
        Optional[bool],
        Field(
            None,
            alias="onlyCompletedAnalyses",
            description="Restrict entries to analysis complete events.",
        ),
    ]
    start: Annotated[
        Optional[AwareDatetime],
        Field(None, description="The first date in the reporting timeframe."),
    ]
    user_ids: Annotated[
        Optional[List[str]],
        Field(
            None,
            alias="userIds",
            description="The users to include in the report. If empty, all users will be included.",
        ),
    ]


class RunAdminReportRequestRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    end: Annotated[
        Optional[AwareDatetime],
        Field(None, description="The last date in the reporting timeframe."),
    ]
    start: Annotated[
        Optional[AwareDatetime],
        Field(None, description="The first date in the reporting timeframe."),
    ]


class SortObject(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    ascending: Optional[bool] = None
    direction: Optional[str] = None
    ignore_case: Annotated[Optional[bool], Field(None, alias="ignoreCase")]
    null_handling: Annotated[Optional[str], Field(None, alias="nullHandling")]
    property: Optional[str] = None


class ActionableErrorResponse(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    entity_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="entityId",
            description="Identifies the entity impacted by the error.",
        ),
    ]
    entity_type: Annotated[
        Optional[str],
        Field(
            None,
            alias="entityType",
            description="The type of entity impacted by the error.",
        ),
    ]
    instance: Annotated[
        Optional[str], Field(None, description="A unique identifier for this request.")
    ]
    origin: Annotated[
        Optional[str],
        Field(None, description="The endpoint where this request originated from."),
    ]
    problem_count: Annotated[
        Optional[int],
        Field(None, alias="problemCount", description="The total number of problems."),
    ]
    problems: Annotated[
        Optional[List[Problem]],
        Field(None, description="The reason(s) why the error occurred."),
    ]
    status: Annotated[
        Optional[int],
        Field(None, description="The HTTP status code determined by the error type."),
    ]
    title: Annotated[
        Optional[str], Field(None, description="A description of the error.")
    ]
    type: Annotated[
        Optional[str],
        Field(
            None,
            description="Indicates the type of error that occurred. Type values are formatted as URLs.",
        ),
    ]


class ApiAccountGrouping(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    archived: Annotated[
        Optional[bool],
        Field(None, description="When `true`, the account grouping is archived."),
    ]
    code_display_name: Annotated[
        Optional[Dict[str, str]],
        Field(
            None,
            alias="codeDisplayName",
            description="The name of the account code hierarchy system used within the dataset.",
        ),
    ]
    created_user_info: Annotated[
        Optional[ApiUserInfo], Field(None, alias="createdUserInfo")
    ]
    creation_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="creationDate",
            description="The date that the object was originally created.",
        ),
    ]
    delimiter: Annotated[
        Optional[str],
        Field(
            None,
            description="The delimiter character used to separate each category level in an account grouping code.",
        ),
    ]
    id: Annotated[
        Optional[str], Field(None, description="The unique object identifier.")
    ]
    industry_tags: Annotated[
        Optional[List[str]],
        Field(
            None,
            alias="industryTags",
            description="A set of all the unique industry tags included in the account grouping.",
        ),
    ]
    last_modified_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="lastModifiedDate",
            description="The date that the object was last updated or modified.",
        ),
    ]
    last_modified_user_info: Annotated[
        Optional[ApiUserInfo], Field(None, alias="lastModifiedUserInfo")
    ]
    mac: Annotated[
        Optional[bool],
        Field(
            None,
            description="When `true`, the account grouping is based on the MAC code system.",
        ),
    ]
    name: Annotated[
        Optional[Dict[str, str]],
        Field(None, description="The name of the account grouping."),
    ]
    publish_status: Annotated[
        Optional[PublishStatus],
        Field(
            None,
            alias="publishStatus",
            description="The current status of the account grouping.",
        ),
    ]
    published_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="publishedDate",
            description="The date that the account grouping was published.",
        ),
    ]
    system: Annotated[
        Optional[bool],
        Field(
            None,
            description="When `true`, the account grouping is a system account grouping and cannot be modified.",
        ),
    ]
    version: Annotated[
        Optional[int],
        Field(
            None, description="The data integrity version, to ensure data consistency."
        ),
    ]


class ApiAccountGroupingRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    archived: Annotated[
        Optional[bool],
        Field(None, description="When `true`, the account grouping is archived."),
    ]
    code_display_name: Annotated[
        Optional[Dict[str, str]],
        Field(
            None,
            alias="codeDisplayName",
            description="The name of the account code hierarchy system used within the dataset.",
        ),
    ]
    created_user_info: Annotated[
        Optional[ApiUserInfoRead], Field(None, alias="createdUserInfo")
    ]
    creation_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="creationDate",
            description="The date that the object was originally created.",
        ),
    ]
    delimiter: Annotated[
        Optional[str],
        Field(
            None,
            description="The delimiter character used to separate each category level in an account grouping code.",
        ),
    ]
    id: Annotated[
        Optional[str], Field(None, description="The unique object identifier.")
    ]
    industry_tags: Annotated[
        Optional[List[str]],
        Field(
            None,
            alias="industryTags",
            description="A set of all the unique industry tags included in the account grouping.",
        ),
    ]
    last_modified_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="lastModifiedDate",
            description="The date that the object was last updated or modified.",
        ),
    ]
    last_modified_user_info: Annotated[
        Optional[ApiUserInfoRead], Field(None, alias="lastModifiedUserInfo")
    ]
    mac: Annotated[
        Optional[bool],
        Field(
            None,
            description="When `true`, the account grouping is based on the MAC code system.",
        ),
    ]
    name: Annotated[
        Optional[Dict[str, str]],
        Field(None, description="The name of the account grouping."),
    ]
    publish_status: Annotated[
        Optional[PublishStatus],
        Field(
            None,
            alias="publishStatus",
            description="The current status of the account grouping.",
        ),
    ]
    published_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="publishedDate",
            description="The date that the account grouping was published.",
        ),
    ]
    system: Annotated[
        Optional[bool],
        Field(
            None,
            description="When `true`, the account grouping is a system account grouping and cannot be modified.",
        ),
    ]
    version: Annotated[
        Optional[int],
        Field(
            None, description="The data integrity version, to ensure data consistency."
        ),
    ]


class ApiAnalysisSourceTypeRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    archived: Annotated[
        Optional[bool],
        Field(
            None,
            description="Indicates whether or not the analysis source type is archived.",
        ),
    ]
    column_definitions: Annotated[
        Optional[List[ApiColumnDefinitionRead]],
        Field(
            None,
            alias="columnDefinitions",
            description="A list of MindBridge column definitions that this analysis source type supports.",
        ),
    ]
    created_user_info: Annotated[
        Optional[ApiUserInfoRead], Field(None, alias="createdUserInfo")
    ]
    creation_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="creationDate",
            description="The date that the object was originally created.",
        ),
    ]
    features: Annotated[
        Optional[List[Feature]],
        Field(
            None,
            description="A list of the features used when importing data for this analysis source type.",
        ),
    ]
    id: Annotated[
        Optional[str], Field(None, description="The unique object identifier.")
    ]
    interim_name: Annotated[
        Optional[str],
        Field(
            None,
            alias="interimName",
            description="The name of the analysis source type when the analysis uses an interim time frame.",
        ),
    ]
    last_modified_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="lastModifiedDate",
            description="The date that the object was last updated or modified.",
        ),
    ]
    last_modified_user_info: Annotated[
        Optional[ApiUserInfoRead], Field(None, alias="lastModifiedUserInfo")
    ]
    name: Annotated[
        Optional[str], Field(None, description="The name of the analysis source type.")
    ]
    version: Annotated[
        Optional[int],
        Field(None, description="Data integrity version to ensure data consistency."),
    ]


class ApiAnalysisTypeRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    account_mapping_required: Annotated[
        Optional[bool],
        Field(
            None,
            alias="accountMappingRequired",
            description="Indicates whether or not account mapping must be performed.",
        ),
    ]
    archived: Annotated[
        Optional[bool],
        Field(
            None,
            description="Indicates whether or not the analysis type has been archived.",
        ),
    ]
    created_user_info: Annotated[
        Optional[ApiUserInfoRead], Field(None, alias="createdUserInfo")
    ]
    creation_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="creationDate",
            description="The date that the object was originally created.",
        ),
    ]
    description: Annotated[
        Optional[str], Field(None, description="The description of the analysis type.")
    ]
    fund_supported: Annotated[
        Optional[bool],
        Field(
            None,
            alias="fundSupported",
            description="Indicates whether or not the analysis supports restricted and unrestricted funds.",
        ),
    ]
    id: Annotated[
        Optional[str], Field(None, description="The unique object identifier.")
    ]
    interim_name: Annotated[
        Optional[str],
        Field(
            None,
            alias="interimName",
            description="The name of the analysis type when the analysis uses an interim time frame.",
        ),
    ]
    interim_supported: Annotated[
        Optional[bool],
        Field(
            None,
            alias="interimSupported",
            description="Indicates whether or not the analysis supports the interim time frame.",
        ),
    ]
    last_modified_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="lastModifiedDate",
            description="The date that the object was last updated or modified.",
        ),
    ]
    last_modified_user_info: Annotated[
        Optional[ApiUserInfoRead], Field(None, alias="lastModifiedUserInfo")
    ]
    name: Annotated[
        Optional[str], Field(None, description="The name of the analysis type.")
    ]
    periodic_supported: Annotated[
        Optional[bool],
        Field(
            None,
            alias="periodicSupported",
            description="Indicates whether or not the analysis supports the periodic time frame.",
        ),
    ]
    source_configurations: Annotated[
        Optional[List[ApiSourceConfigurationRead]],
        Field(
            None,
            alias="sourceConfigurations",
            description="A list of analysis source configurations that can be imported into the analysis, as determined by the analysis type.",
        ),
    ]
    version: Annotated[
        Optional[int],
        Field(None, description="Data integrity version to ensure data consistency."),
    ]


class ApiAnalysisRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    analysis_period_gaps: Annotated[
        Optional[List[ApiAnalysisPeriodGapRead]],
        Field(
            None,
            alias="analysisPeriodGaps",
            description="Details about the gap in time between two analysis periods.",
        ),
    ]
    analysis_periods: Annotated[
        Optional[List[ApiAnalysisPeriodRead]],
        Field(
            None,
            alias="analysisPeriods",
            description="Details about the specific analysis periods under audit.",
        ),
    ]
    analysis_type_id: Annotated[
        Optional[str],
        Field(
            None, alias="analysisTypeId", description="Identifies the type of analysis."
        ),
    ]
    archived: Annotated[
        Optional[bool],
        Field(
            None, description="Indicates whether or not the analysis has been archived."
        ),
    ]
    converted: Annotated[
        Optional[bool],
        Field(
            None,
            description="Indicates whether or not an interim analysis time frame has been converted to a full analysis time frame.",
        ),
    ]
    created_user_info: Annotated[
        Optional[ApiUserInfoRead], Field(None, alias="createdUserInfo")
    ]
    creation_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="creationDate",
            description="The date that the object was originally created.",
        ),
    ]
    currency_code: Annotated[
        Optional[str],
        Field(
            None,
            alias="currencyCode",
            description="The currency to be displayed across the analysis results.",
        ),
    ]
    engagement_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="engagementId",
            description="Identifies the associated engagement.",
        ),
    ]
    id: Annotated[
        Optional[str], Field(None, description="The unique object identifier.")
    ]
    important_columns: Annotated[
        Optional[List[ApiAnalysisImportantColumnRead]],
        Field(
            None,
            alias="importantColumns",
            description="Additional data columns that can be used when importing additional data.",
        ),
    ]
    interim: Annotated[
        Optional[bool],
        Field(
            None,
            description="Indicates whether or not the analysis is using an interim time frame.",
        ),
    ]
    last_modified_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="lastModifiedDate",
            description="The date that the object was last updated or modified.",
        ),
    ]
    last_modified_user_info: Annotated[
        Optional[ApiUserInfoRead], Field(None, alias="lastModifiedUserInfo")
    ]
    name: Annotated[
        Optional[str],
        Field(
            None, description="The name of the analysis.", max_length=80, min_length=0
        ),
    ]
    periodic: Annotated[
        Optional[bool],
        Field(
            None,
            description="Indicates whether or not the analysis is using a periodic time frame.",
        ),
    ]
    version: Annotated[
        Optional[int],
        Field(
            None,
            description="Indicates the data integrity version to ensure data consistency.",
        ),
    ]


class ApiApiTokenRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    allowed_addresses: Annotated[
        Optional[List[str]],
        Field(
            None,
            alias="allowedAddresses",
            description="Indicates the set of addresses that are allowed to use this token. If empty, any address may use it.",
        ),
    ]
    created_user_info: Annotated[
        Optional[ApiUserInfoRead], Field(None, alias="createdUserInfo")
    ]
    creation_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="creationDate",
            description="The date that the object was originally created.",
        ),
    ]
    expiry: Annotated[
        Optional[AwareDatetime],
        Field(None, description="The day on which the API token expires."),
    ]
    id: Annotated[
        Optional[str], Field(None, description="The unique object identifier.")
    ]
    last_modified_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="lastModifiedDate",
            description="The date that the object was last updated or modified.",
        ),
    ]
    last_modified_user_info: Annotated[
        Optional[ApiUserInfoRead], Field(None, alias="lastModifiedUserInfo")
    ]
    name: Annotated[
        Optional[str],
        Field(
            None,
            description="The token record’s name. This will also be used as the API Token User’s name.",
        ),
    ]
    partial_token: Annotated[
        Optional[str],
        Field(
            None,
            alias="partialToken",
            description="A partial representation of the API token.",
        ),
    ]
    permissions: Annotated[
        Optional[List[Permission]],
        Field(
            None,
            description="The set of permissions that inform which endpoints this token is authorized to access.",
        ),
    ]
    user_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="userId",
            description="Identifies the API Token User associated with this token.",
        ),
    ]
    version: Annotated[
        Optional[int],
        Field(
            None,
            description="Indicates the data integrity version to ensure data consistency.",
        ),
    ]


class ApiAsyncResult(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    created_user_info: Annotated[
        Optional[ApiUserInfo], Field(None, alias="createdUserInfo")
    ]
    creation_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="creationDate",
            description="The date that the object was originally created.",
        ),
    ]
    entity_id: Annotated[
        Optional[str],
        Field(
            None, alias="entityId", description="Identifies the entity used in the job."
        ),
    ]
    entity_type: Annotated[
        Optional[EntityType],
        Field(
            None,
            alias="entityType",
            description="Identifies the entity type used in the job.",
        ),
    ]
    error: Annotated[
        Optional[str], Field(None, description="The reason why the async job failed.")
    ]
    id: Annotated[
        Optional[str], Field(None, description="The unique object identifier.")
    ]
    last_modified_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="lastModifiedDate",
            description="The date that the object was last updated or modified.",
        ),
    ]
    last_modified_user_info: Annotated[
        Optional[ApiUserInfo], Field(None, alias="lastModifiedUserInfo")
    ]
    status: Annotated[
        Optional[Status2],
        Field(None, description="Indicates the current state of the job."),
    ]
    type: Annotated[
        Optional[Type1], Field(None, description="Indicates the type of job being run.")
    ]
    version: Annotated[
        Optional[int],
        Field(
            None,
            description="Indicates the data integrity version to ensure data consistency.",
        ),
    ]


class ApiAsyncResultRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    created_user_info: Annotated[
        Optional[ApiUserInfoRead], Field(None, alias="createdUserInfo")
    ]
    creation_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="creationDate",
            description="The date that the object was originally created.",
        ),
    ]
    entity_id: Annotated[
        Optional[str],
        Field(
            None, alias="entityId", description="Identifies the entity used in the job."
        ),
    ]
    entity_type: Annotated[
        Optional[EntityType],
        Field(
            None,
            alias="entityType",
            description="Identifies the entity type used in the job.",
        ),
    ]
    error: Annotated[
        Optional[str], Field(None, description="The reason why the async job failed.")
    ]
    id: Annotated[
        Optional[str], Field(None, description="The unique object identifier.")
    ]
    last_modified_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="lastModifiedDate",
            description="The date that the object was last updated or modified.",
        ),
    ]
    last_modified_user_info: Annotated[
        Optional[ApiUserInfoRead], Field(None, alias="lastModifiedUserInfo")
    ]
    status: Annotated[
        Optional[Status2],
        Field(None, description="Indicates the current state of the job."),
    ]
    type: Annotated[
        Optional[Type1], Field(None, description="Indicates the type of job being run.")
    ]
    version: Annotated[
        Optional[int],
        Field(
            None,
            description="Indicates the data integrity version to ensure data consistency.",
        ),
    ]


class ApiBasicMetricsRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    data_previews: Annotated[
        Optional[List[ApiDataPreviewRead]], Field(None, alias="dataPreviews")
    ]
    state: Optional[State] = None


class ApiChunkedFileRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    chunked_file_parts: Annotated[
        Optional[List[ApiChunkedFilePartRead]],
        Field(
            None,
            alias="chunkedFileParts",
            description="The offset and size of the chunked file parts.",
        ),
    ]
    created_user_info: Annotated[
        Optional[ApiUserInfoRead], Field(None, alias="createdUserInfo")
    ]
    creation_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="creationDate",
            description="The date that the object was originally created.",
        ),
    ]
    id: Annotated[
        Optional[str], Field(None, description="The unique object identifier.")
    ]
    last_modified_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="lastModifiedDate",
            description="The date that the object was last updated or modified.",
        ),
    ]
    last_modified_user_info: Annotated[
        Optional[ApiUserInfoRead], Field(None, alias="lastModifiedUserInfo")
    ]
    name: Annotated[
        Optional[str], Field(None, description="The name of the chunked file.")
    ]
    size: Annotated[
        Optional[int], Field(None, description="The size of the chunked file.", ge=0)
    ]
    version: Annotated[
        Optional[int],
        Field(
            None,
            description="Indicates the data integrity version to ensure data consistency.",
        ),
    ]


class ApiCountMetricsRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    count: Optional[int] = None
    data_previews: Annotated[
        Optional[List[ApiDataPreviewRead]], Field(None, alias="dataPreviews")
    ]
    state: Optional[State] = None


class ApiDateTypeDetailsRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    ambiguous_date_time_formats: Annotated[
        Optional[List[ApiColumnDateTimeFormatRead]],
        Field(None, alias="ambiguousDateTimeFormats"),
    ]
    range: Optional[RangeZonedDateTimeRead] = None
    unambiguous_date_time_formats: Annotated[
        Optional[List[ApiColumnDateTimeFormatRead]],
        Field(None, alias="unambiguousDateTimeFormats"),
    ]


class ApiDuplicateVirtualColumnRead(ApiVirtualColumnRead):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    column_index: Annotated[
        Optional[int],
        Field(
            None,
            alias="columnIndex",
            description="The position of the duplicated column.",
        ),
    ]
    name: Annotated[str, Field(description="The name of the virtual column.")]
    type: Annotated[Type17, Field(description="The type of virtual column.")]
    version: Annotated[
        int,
        Field(
            description="Indicates the data integrity version to ensure data consistency."
        ),
    ]


class ApiDuplicateVirtualColumnUpdate(ApiVirtualColumnUpdate):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    column_index: Annotated[
        Optional[int],
        Field(
            None,
            alias="columnIndex",
            description="The position of the duplicated column.",
        ),
    ]
    name: Annotated[str, Field(description="The name of the virtual column.")]
    type: Annotated[Type17, Field(description="The type of virtual column.")]
    version: Annotated[
        int,
        Field(
            description="Indicates the data integrity version to ensure data consistency."
        ),
    ]


class ApiEngagementAccountGroupingRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    account_grouping_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="accountGroupingId",
            description="The unique identifier of the account grouping on which this is based.",
        ),
    ]
    code_display_name: Annotated[
        Optional[Dict[str, str]],
        Field(
            None,
            alias="codeDisplayName",
            description="The name of the account code hierarchy system used within the dataset.",
        ),
    ]
    created_user_info: Annotated[
        Optional[ApiUserInfoRead], Field(None, alias="createdUserInfo")
    ]
    creation_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="creationDate",
            description="The date that the object was originally created.",
        ),
    ]
    delimiter: Annotated[
        Optional[str],
        Field(
            None,
            description="The delimiter character used to separate each category level in an account grouping code.",
        ),
    ]
    engagement_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="engagementId",
            description="The unique identifier of the engagement that this engagement account grouping belongs to.",
        ),
    ]
    id: Annotated[
        Optional[str], Field(None, description="The unique object identifier.")
    ]
    last_modified_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="lastModifiedDate",
            description="The date that the object was last updated or modified.",
        ),
    ]
    last_modified_user_info: Annotated[
        Optional[ApiUserInfoRead], Field(None, alias="lastModifiedUserInfo")
    ]
    name: Annotated[
        Optional[Dict[str, str]],
        Field(None, description="The name of the account grouping."),
    ]
    version: Annotated[
        Optional[int],
        Field(
            None, description="The data integrity version, to ensure data consistency."
        ),
    ]


class ApiEngagementRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    accounting_package: Annotated[
        Optional[str],
        Field(
            None,
            alias="accountingPackage",
            description="The ERP or financial management system that your client is using.",
        ),
    ]
    accounting_period: Annotated[
        Optional[ApiAccountingPeriodRead], Field(None, alias="accountingPeriod")
    ]
    audit_period_end_date: Annotated[
        Optional[date],
        Field(
            None,
            alias="auditPeriodEndDate",
            description="The last day of the occurring audit.",
        ),
    ]
    auditor_ids: Annotated[
        Optional[List[str]],
        Field(
            None,
            alias="auditorIds",
            description="Identifies the users who will act as auditors in the engagement.",
        ),
    ]
    billing_code: Annotated[
        Optional[str],
        Field(
            None,
            alias="billingCode",
            description="A unique code that associates engagements and analyses with clients to ensure those clients are billed appropriately for MindBridge usage.",
        ),
    ]
    created_user_info: Annotated[
        Optional[ApiUserInfoRead], Field(None, alias="createdUserInfo")
    ]
    creation_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="creationDate",
            description="The date that the object was originally created.",
        ),
    ]
    engagement_lead_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="engagementLeadId",
            description="Identifies the user who will lead the engagement.",
        ),
    ]
    id: Annotated[
        Optional[str], Field(None, description="The unique object identifier.")
    ]
    industry: Annotated[
        Optional[str],
        Field(
            None, description="The type of industry that your client operates within."
        ),
    ]
    last_modified_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="lastModifiedDate",
            description="The date that the object was last updated or modified.",
        ),
    ]
    last_modified_user_info: Annotated[
        Optional[ApiUserInfoRead], Field(None, alias="lastModifiedUserInfo")
    ]
    library_id: Annotated[
        Optional[str],
        Field(None, alias="libraryId", description="Identifies the library."),
    ]
    name: Annotated[
        Optional[str],
        Field(
            None, description="The name of the engagement.", max_length=80, min_length=0
        ),
    ]
    organization_id: Annotated[
        Optional[str],
        Field(None, alias="organizationId", description="Identifies the organization."),
    ]
    version: Annotated[
        Optional[int],
        Field(
            None,
            description="Indicates the data integrity version to ensure data consistency.",
        ),
    ]


class ApiFileExportRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    created_user_info: Annotated[
        Optional[ApiUserInfoRead], Field(None, alias="createdUserInfo")
    ]
    creation_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="creationDate",
            description="The date that the object was originally created.",
        ),
    ]
    file_name: Annotated[
        Optional[str],
        Field(None, alias="fileName", description="The name of the file."),
    ]
    id: Annotated[
        Optional[str], Field(None, description="The unique file export identifier.")
    ]
    last_modified_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="lastModifiedDate",
            description="The date that the object was last updated or modified.",
        ),
    ]
    last_modified_user_info: Annotated[
        Optional[ApiUserInfoRead], Field(None, alias="lastModifiedUserInfo")
    ]
    size: Annotated[Optional[int], Field(None, description="The size of the file.")]
    version: Annotated[
        Optional[int],
        Field(
            None,
            description="Indicates the data integrity version to ensure data consistency.",
        ),
    ]


class ApiFileManagerDirectoryUpdate(ApiFileManagerEntityUpdate):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    name: Annotated[
        Optional[str], Field(None, description="The current name of the directory.")
    ]
    version: Annotated[
        int,
        Field(
            description="Indicates the data integrity version to ensure data consistency."
        ),
    ]


class ApiFileManagerEntityRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    created_user_info: Annotated[
        Optional[ApiUserInfoRead], Field(None, alias="createdUserInfo")
    ]
    creation_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="creationDate",
            description="The date that the object was originally created.",
        ),
    ]
    engagement_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="engagementId",
            description="Identifies the associated engagement.",
        ),
    ]
    id: Annotated[
        Optional[str], Field(None, description="The unique object identifier.")
    ]
    last_modified_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="lastModifiedDate",
            description="The date that the object was last updated or modified.",
        ),
    ]
    last_modified_user_info: Annotated[
        Optional[ApiUserInfoRead], Field(None, alias="lastModifiedUserInfo")
    ]
    parent_file_manager_entity_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="parentFileManagerEntityId",
            description="Identifies the parent directory. If NULL, the directory is positioned at the root level.",
        ),
    ]
    type: Annotated[
        Optional[Type5],
        Field(
            None,
            description="Indicates whether the object is a DIRECTORY or a FILE within the directory.",
        ),
    ]
    version: Annotated[
        Optional[int],
        Field(
            None,
            description="Indicates the data integrity version to ensure data consistency.",
        ),
    ]


class ApiFileManagerFileRead(ApiFileManagerEntityRead):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    extension: Annotated[
        Optional[str],
        Field(None, description="The suffix used at the end of the file."),
    ]
    name: Annotated[
        Optional[str],
        Field(
            None, description="The current name of the file, excluding the extension."
        ),
    ]
    original_name: Annotated[
        Optional[str],
        Field(
            None,
            alias="originalName",
            description="The name of the file as it appeared when first imported, including the extension.",
        ),
    ]
    status: Annotated[
        Optional[List[StatusEnum]],
        Field(None, description="The status of the file as it appears in MindBridge."),
    ]
    engagement_id: Annotated[
        str,
        Field(
            alias="engagementId", description="Identifies the associated engagement."
        ),
    ]
    version: Annotated[
        int,
        Field(
            description="Indicates the data integrity version to ensure data consistency."
        ),
    ]


class ApiJoinVirtualColumnRead(ApiVirtualColumnRead):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    column_indices: Annotated[
        Optional[List[int]],
        Field(
            None,
            alias="columnIndices",
            description="The positions of the column to be joined.",
        ),
    ]
    delimiter: Annotated[
        Optional[str],
        Field(
            None,
            description="The character(s) that should be inserted to separate values.",
        ),
    ]
    name: Annotated[str, Field(description="The name of the virtual column.")]
    type: Annotated[Type17, Field(description="The type of virtual column.")]
    version: Annotated[
        int,
        Field(
            description="Indicates the data integrity version to ensure data consistency."
        ),
    ]


class ApiJoinVirtualColumnUpdate(ApiVirtualColumnUpdate):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    column_indices: Annotated[
        Optional[List[int]],
        Field(
            None,
            alias="columnIndices",
            description="The positions of the column to be joined.",
        ),
    ]
    delimiter: Annotated[
        Optional[str],
        Field(
            None,
            description="The character(s) that should be inserted to separate values.",
        ),
    ]
    name: Annotated[str, Field(description="The name of the virtual column.")]
    type: Annotated[Type17, Field(description="The type of virtual column.")]
    version: Annotated[
        int,
        Field(
            description="Indicates the data integrity version to ensure data consistency."
        ),
    ]


class ApiLibraryRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    account_grouping_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="accountGroupingId",
            description="Identifies the account grouping used.",
        ),
    ]
    analysis_type_ids: Annotated[
        Optional[List[str]],
        Field(
            None,
            alias="analysisTypeIds",
            description="Identifies the analysis types used in the library.",
        ),
    ]
    archived: Annotated[
        Optional[bool],
        Field(
            None,
            description="Indicates whether or not the library is archived. Archived libraries cannot be selected when creating an engagement.",
        ),
    ]
    based_on_library_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="basedOnLibraryId",
            description="Identifies the library that the new library is based on. This may be a user-created library or a MindBridge system library.",
        ),
    ]
    control_point_selection_permission: Annotated[
        Optional[bool],
        Field(
            None,
            alias="controlPointSelectionPermission",
            description="When set to `true`, control points can be added or removed within each risk score.",
        ),
    ]
    control_point_settings_permission: Annotated[
        Optional[bool],
        Field(
            None,
            alias="controlPointSettingsPermission",
            description="When set to `true`, individual control point settings can be adjusted within each risk score.",
        ),
    ]
    control_point_weight_permission: Annotated[
        Optional[bool],
        Field(
            None,
            alias="controlPointWeightPermission",
            description="When set to `true`, the weight of each control point can be adjusted within each risk score.",
        ),
    ]
    conversion_warnings: Annotated[
        Optional[List[ProblemRead]],
        Field(
            None,
            alias="conversionWarnings",
            description="A list of accounts that failed to convert the selected base library’s setting to the selected account grouping.",
        ),
    ]
    created_user_info: Annotated[
        Optional[ApiUserInfoRead], Field(None, alias="createdUserInfo")
    ]
    creation_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="creationDate",
            description="The date that the object was originally created.",
        ),
    ]
    default_delimiter: Annotated[
        Optional[str],
        Field(
            None,
            alias="defaultDelimiter",
            description="Identifies the default delimiter used in imported CSV files.",
        ),
    ]
    id: Annotated[
        Optional[str], Field(None, description="The unique object identifier.")
    ]
    industry_tags: Annotated[
        Optional[List[str]],
        Field(
            None,
            alias="industryTags",
            description="The tags used to indicate the industry that your client operates in.",
        ),
    ]
    last_modified_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="lastModifiedDate",
            description="The date that the object was last updated or modified.",
        ),
    ]
    last_modified_user_info: Annotated[
        Optional[ApiUserInfoRead], Field(None, alias="lastModifiedUserInfo")
    ]
    name: Annotated[
        Optional[str],
        Field(
            None,
            description="The current name of the library.",
            max_length=80,
            min_length=0,
        ),
    ]
    original_system_library_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="originalSystemLibraryId",
            description="Identifies the original MindBridge-supplied library.",
        ),
    ]
    risk_score_and_groups_selection_permission: Annotated[
        Optional[bool],
        Field(
            None,
            alias="riskScoreAndGroupsSelectionPermission",
            description="When set to `true`, risk scores and groups can be disabled, and accounts associated with risk scores can be edited.",
        ),
    ]
    risk_score_display: Annotated[
        Optional[RiskScoreDisplay],
        Field(
            None,
            alias="riskScoreDisplay",
            description="Determines whether risk scores will be presented as percentages (%), or using High, Medium, and Low label indicators.",
        ),
    ]
    system: Annotated[
        Optional[bool],
        Field(
            None,
            description="Indicates whether or not the library is a MindBridge system library.",
        ),
    ]
    version: Annotated[
        Optional[int],
        Field(
            None,
            description="Indicates the data integrity version to ensure data consistency.",
        ),
    ]
    warnings_dismissed: Annotated[
        Optional[bool],
        Field(
            None,
            alias="warningsDismissed",
            description="When set to `true`, any conversion warnings for this library will not be displayed in the **Libraries** tab in the UI.",
        ),
    ]


class ApiNumericTypeDetailsRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    capped_max: Annotated[Optional[bool], Field(None, alias="cappedMax")]
    capped_sum: Annotated[Optional[bool], Field(None, alias="cappedSum")]
    currency_format: Annotated[
        Optional[ApiCurrencyFormatRead], Field(None, alias="currencyFormat")
    ]
    example_pair_from_currency_formatter: Annotated[
        Optional[List[str]], Field(None, alias="examplePairFromCurrencyFormatter")
    ]
    range: Optional[RangeBigDecimalRead] = None
    sum: Optional[float] = None


class ApiOrganizationRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    created_user_info: Annotated[
        Optional[ApiUserInfoRead], Field(None, alias="createdUserInfo")
    ]
    creation_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="creationDate",
            description="The date that the object was originally created.",
        ),
    ]
    external_client_code: Annotated[
        Optional[str],
        Field(
            None,
            alias="externalClientCode",
            description="The unique client ID applied to this organization.",
            max_length=80,
            min_length=0,
        ),
    ]
    id: Annotated[
        Optional[str], Field(None, description="The unique object identifier.")
    ]
    last_modified_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="lastModifiedDate",
            description="The date that the object was last updated or modified.",
        ),
    ]
    last_modified_user_info: Annotated[
        Optional[ApiUserInfoRead], Field(None, alias="lastModifiedUserInfo")
    ]
    manager_user_ids: Annotated[
        Optional[List[str]],
        Field(
            None,
            alias="managerUserIds",
            description="Identifies users assigned to the organization manager role.",
        ),
    ]
    name: Annotated[
        Optional[str],
        Field(
            None,
            description="The name of the organization.",
            max_length=80,
            min_length=0,
        ),
    ]
    version: Annotated[
        Optional[int],
        Field(
            None,
            description="Indicates the data integrity version to ensure data consistency.",
        ),
    ]


class ApiPopulationTagRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    analysis_id: Annotated[
        Optional[str],
        Field(
            None, alias="analysisId", description="Identifies the parent analysis ID."
        ),
    ]
    base_population_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="basePopulationId",
            description="Identifies the population the current population was based off of.",
        ),
    ]
    category: Annotated[
        Optional[str],
        Field(
            None,
            description="The category of the population.",
            max_length=80,
            min_length=0,
        ),
    ]
    cloned_from: Annotated[
        Optional[str],
        Field(
            None,
            alias="clonedFrom",
            description="Identifies the population the current population was cloned form.",
        ),
    ]
    created_user_info: Annotated[
        Optional[ApiUserInfoRead], Field(None, alias="createdUserInfo")
    ]
    creation_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="creationDate",
            description="The date that the object was originally created.",
        ),
    ]
    derived_from_engagement: Annotated[
        Optional[bool],
        Field(
            None,
            alias="derivedFromEngagement",
            description="Identifies the engagement that the analysis population is derived from.",
        ),
    ]
    derived_from_library: Annotated[
        Optional[bool],
        Field(
            None,
            alias="derivedFromLibrary",
            description="Identifies the library that the engagement population is derived from.",
        ),
    ]
    description: Annotated[
        Optional[str],
        Field(
            None,
            description="The description of the population.",
            max_length=250,
            min_length=0,
        ),
    ]
    disabled: Annotated[
        Optional[bool],
        Field(None, description="Indicates whether or not the population is disabled."),
    ]
    disabled_for_analysis_ids: Annotated[
        Optional[List[str]],
        Field(
            None,
            alias="disabledForAnalysisIds",
            description="Identifies the analyses that the engagement population is disabled within.",
        ),
    ]
    engagement_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="engagementId",
            description="Identifies the parent engagement ID.",
        ),
    ]
    id: Annotated[
        Optional[str], Field(None, description="The unique object identifier.")
    ]
    last_modified_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="lastModifiedDate",
            description="The date that the object was last updated or modified.",
        ),
    ]
    last_modified_user_info: Annotated[
        Optional[ApiUserInfoRead], Field(None, alias="lastModifiedUserInfo")
    ]
    library_id: Annotated[
        Optional[str],
        Field(None, alias="libraryId", description="Identifies the parent library ID."),
    ]
    name: Annotated[
        Optional[str],
        Field(
            None,
            description="The current name of the population.",
            max_length=80,
            min_length=0,
        ),
    ]
    promoted_from_analysis_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="promotedFromAnalysisId",
            description="Identifies the analysis that the engagement population was added to.",
        ),
    ]
    reason_for_change: Annotated[
        Optional[str],
        Field(
            None,
            alias="reasonForChange",
            description="The reason for the latest change to the population.",
            max_length=250,
            min_length=0,
        ),
    ]
    version: Annotated[
        Optional[int],
        Field(
            None,
            description="Indicates the data integrity version to ensure data consistency.",
        ),
    ]


class ApiProposedDuplicateVirtualColumnCreateOnly(ApiProposedVirtualColumnCreateOnly):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    column_index: Annotated[
        Optional[int],
        Field(
            None,
            alias="columnIndex",
            description="The position of the column to be duplicated.",
        ),
    ]


class ApiProposedDuplicateVirtualColumnRead(ApiProposedVirtualColumnRead):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    column_index: Annotated[
        Optional[int],
        Field(
            None,
            alias="columnIndex",
            description="The position of the column to be duplicated.",
        ),
    ]


class ApiProposedDuplicateVirtualColumnUpdate(ApiProposedVirtualColumnUpdate):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    column_index: Annotated[
        Optional[int],
        Field(
            None,
            alias="columnIndex",
            description="The position of the column to be duplicated.",
        ),
    ]


class ApiProposedJoinVirtualColumnCreateOnly(ApiProposedVirtualColumnCreateOnly):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    column_indices: Annotated[
        Optional[List[int]],
        Field(
            None,
            alias="columnIndices",
            description="The positions of the columns to be joined.",
        ),
    ]
    delimiter: Annotated[
        Optional[str],
        Field(
            None,
            description="The character(s) that should be inserted to separate values.",
        ),
    ]


class ApiProposedJoinVirtualColumnRead(ApiProposedVirtualColumnRead):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    column_indices: Annotated[
        Optional[List[int]],
        Field(
            None,
            alias="columnIndices",
            description="The positions of the columns to be joined.",
        ),
    ]
    delimiter: Annotated[
        Optional[str],
        Field(
            None,
            description="The character(s) that should be inserted to separate values.",
        ),
    ]


class ApiProposedJoinVirtualColumnUpdate(ApiProposedVirtualColumnUpdate):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    column_indices: Annotated[
        Optional[List[int]],
        Field(
            None,
            alias="columnIndices",
            description="The positions of the columns to be joined.",
        ),
    ]
    delimiter: Annotated[
        Optional[str],
        Field(
            None,
            description="The character(s) that should be inserted to separate values.",
        ),
    ]


class ApiProposedSplitByDelimiterVirtualColumnCreateOnly(
    ApiProposedVirtualColumnCreateOnly
):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    column_index: Annotated[
        Optional[int],
        Field(
            None,
            alias="columnIndex",
            description="The position of the column to be split.",
        ),
    ]
    delimiter: Annotated[
        Optional[str],
        Field(
            None,
            description="The character(s) that should be used to separate the string into parts.",
        ),
    ]
    split_index: Annotated[
        Optional[int],
        Field(
            None,
            alias="splitIndex",
            description="The position of the part to be used as a virtual column.",
        ),
    ]


class ApiProposedSplitByDelimiterVirtualColumnRead(ApiProposedVirtualColumnRead):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    column_index: Annotated[
        Optional[int],
        Field(
            None,
            alias="columnIndex",
            description="The position of the column to be split.",
        ),
    ]
    delimiter: Annotated[
        Optional[str],
        Field(
            None,
            description="The character(s) that should be used to separate the string into parts.",
        ),
    ]
    split_index: Annotated[
        Optional[int],
        Field(
            None,
            alias="splitIndex",
            description="The position of the part to be used as a virtual column.",
        ),
    ]


class ApiProposedSplitByDelimiterVirtualColumnUpdate(ApiProposedVirtualColumnUpdate):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    column_index: Annotated[
        Optional[int],
        Field(
            None,
            alias="columnIndex",
            description="The position of the column to be split.",
        ),
    ]
    delimiter: Annotated[
        Optional[str],
        Field(
            None,
            description="The character(s) that should be used to separate the string into parts.",
        ),
    ]
    split_index: Annotated[
        Optional[int],
        Field(
            None,
            alias="splitIndex",
            description="The position of the part to be used as a virtual column.",
        ),
    ]


class ApiProposedSplitByPositionVirtualColumnCreateOnly(
    ApiProposedVirtualColumnCreateOnly
):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    column_index: Annotated[
        Optional[int],
        Field(
            None,
            alias="columnIndex",
            description="The position of the column to be split.",
        ),
    ]
    end_position: Annotated[
        Optional[int],
        Field(
            None,
            alias="endPosition",
            description="The ending position of the substring to be used as the new column. **Exclusive**.",
        ),
    ]
    start_position: Annotated[
        Optional[int],
        Field(
            None,
            alias="startPosition",
            description="The starting position of the substring to be used as the new column. **Inclusive**.",
        ),
    ]


class ApiProposedSplitByPositionVirtualColumnRead(ApiProposedVirtualColumnRead):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    column_index: Annotated[
        Optional[int],
        Field(
            None,
            alias="columnIndex",
            description="The position of the column to be split.",
        ),
    ]
    end_position: Annotated[
        Optional[int],
        Field(
            None,
            alias="endPosition",
            description="The ending position of the substring to be used as the new column. **Exclusive**.",
        ),
    ]
    start_position: Annotated[
        Optional[int],
        Field(
            None,
            alias="startPosition",
            description="The starting position of the substring to be used as the new column. **Inclusive**.",
        ),
    ]


class ApiProposedSplitByPositionVirtualColumnUpdate(ApiProposedVirtualColumnUpdate):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    column_index: Annotated[
        Optional[int],
        Field(
            None,
            alias="columnIndex",
            description="The position of the column to be split.",
        ),
    ]
    end_position: Annotated[
        Optional[int],
        Field(
            None,
            alias="endPosition",
            description="The ending position of the substring to be used as the new column. **Exclusive**.",
        ),
    ]
    start_position: Annotated[
        Optional[int],
        Field(
            None,
            alias="startPosition",
            description="The starting position of the substring to be used as the new column. **Inclusive**.",
        ),
    ]


class ApiSplitByDelimiterVirtualColumnRead(ApiVirtualColumnRead):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    column_index: Annotated[
        Optional[int],
        Field(
            None, alias="columnIndex", description="The position of the split column."
        ),
    ]
    delimiter: Annotated[
        Optional[str],
        Field(
            None, description="The character(s) used to separate the string into parts."
        ),
    ]
    split_index: Annotated[
        Optional[int],
        Field(
            None,
            alias="splitIndex",
            description="The position of the part used as a virtual column.",
        ),
    ]
    name: Annotated[str, Field(description="The name of the virtual column.")]
    type: Annotated[Type17, Field(description="The type of virtual column.")]
    version: Annotated[
        int,
        Field(
            description="Indicates the data integrity version to ensure data consistency."
        ),
    ]


class ApiSplitByDelimiterVirtualColumnUpdate(ApiVirtualColumnUpdate):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    column_index: Annotated[
        Optional[int],
        Field(
            None, alias="columnIndex", description="The position of the split column."
        ),
    ]
    delimiter: Annotated[
        Optional[str],
        Field(
            None, description="The character(s) used to separate the string into parts."
        ),
    ]
    split_index: Annotated[
        Optional[int],
        Field(
            None,
            alias="splitIndex",
            description="The position of the part used as a virtual column.",
        ),
    ]
    name: Annotated[str, Field(description="The name of the virtual column.")]
    type: Annotated[Type17, Field(description="The type of virtual column.")]
    version: Annotated[
        int,
        Field(
            description="Indicates the data integrity version to ensure data consistency."
        ),
    ]


class ApiSplitByPositionVirtualColumnRead(ApiVirtualColumnRead):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    column_index: Annotated[
        Optional[int],
        Field(
            None, alias="columnIndex", description="The position of the split column."
        ),
    ]
    end_position: Annotated[
        Optional[int],
        Field(
            None,
            alias="endPosition",
            description="The ending position of the substring in the new column. **Exclusive**.",
        ),
    ]
    start_position: Annotated[
        Optional[int],
        Field(
            None,
            alias="startPosition",
            description="The starting position of the substring in the new column. **Inclusive**.",
        ),
    ]
    name: Annotated[str, Field(description="The name of the virtual column.")]
    type: Annotated[Type17, Field(description="The type of virtual column.")]
    version: Annotated[
        int,
        Field(
            description="Indicates the data integrity version to ensure data consistency."
        ),
    ]


class ApiSplitByPositionVirtualColumnUpdate(ApiVirtualColumnUpdate):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    column_index: Annotated[
        Optional[int],
        Field(
            None, alias="columnIndex", description="The position of the split column."
        ),
    ]
    end_position: Annotated[
        Optional[int],
        Field(
            None,
            alias="endPosition",
            description="The ending position of the substring in the new column. **Exclusive**.",
        ),
    ]
    start_position: Annotated[
        Optional[int],
        Field(
            None,
            alias="startPosition",
            description="The starting position of the substring in the new column. **Inclusive**.",
        ),
    ]
    name: Annotated[str, Field(description="The name of the virtual column.")]
    type: Annotated[Type17, Field(description="The type of virtual column.")]
    version: Annotated[
        int,
        Field(
            description="Indicates the data integrity version to ensure data consistency."
        ),
    ]


class ApiTableMetadataRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    cell_length_metrics: Annotated[
        Optional[ApiCountMetricsRead], Field(None, alias="cellLengthMetrics")
    ]
    density_metrics: Annotated[
        Optional[ApiDensityMetricsRead], Field(None, alias="densityMetrics")
    ]
    inconsistent_date_metrics: Annotated[
        Optional[ApiCountMetricsRead], Field(None, alias="inconsistentDateMetrics")
    ]
    null_value_metrics: Annotated[
        Optional[ApiCountMetricsRead], Field(None, alias="nullValueMetrics")
    ]
    numeric_column_metrics: Annotated[
        Optional[ApiBasicMetricsRead], Field(None, alias="numericColumnMetrics")
    ]
    overall_data_type_metrics: Annotated[
        Optional[ApiOverallDataTypeMetricsRead],
        Field(None, alias="overallDataTypeMetrics"),
    ]
    scientific_notation_metrics: Annotated[
        Optional[ApiCountMetricsRead], Field(None, alias="scientificNotationMetrics")
    ]
    sheet_metrics: Annotated[
        Optional[ApiSheetMetricsRead], Field(None, alias="sheetMetrics")
    ]
    special_character_metrics: Annotated[
        Optional[ApiCountMetricsRead], Field(None, alias="specialCharacterMetrics")
    ]
    uneven_columns_metrics: Annotated[
        Optional[ApiHistogramMetricsRead], Field(None, alias="unevenColumnsMetrics")
    ]


class ApiTaskRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    analysis_id: Annotated[
        Optional[str],
        Field(
            None, alias="analysisId", description="Identifies the associated analysis."
        ),
    ]
    analysis_type_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="analysisTypeId",
            description="Identifies the associated analysis type.",
        ),
    ]
    assertions: Annotated[
        Optional[List[str]],
        Field(None, description="Which assertions this task is associated with."),
    ]
    assigned_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="assignedId",
            description="Identifies the user assigned to this task.",
        ),
    ]
    audit_areas: Annotated[
        Optional[List[str]],
        Field(
            None,
            alias="auditAreas",
            description="Which audit areas this task is associated with.",
        ),
    ]
    comments: Annotated[
        Optional[List[ApiTaskCommentRead]],
        Field(
            None,
            description="A list of all the comments that have been made on this task.",
        ),
    ]
    created_user_info: Annotated[
        Optional[ApiUserInfoRead], Field(None, alias="createdUserInfo")
    ]
    creation_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="creationDate",
            description="The date that the object was originally created.",
        ),
    ]
    credit_value: Annotated[
        Optional[int],
        Field(
            None,
            alias="creditValue",
            description="The credit value of the associated transaction or entry, formatted as MONEY_100.",
        ),
    ]
    customer_name: Annotated[
        Optional[str],
        Field(
            None,
            alias="customerName",
            description="For AR analyses this is the customer name for the associated entry.",
        ),
    ]
    debit_value: Annotated[
        Optional[int],
        Field(
            None,
            alias="debitValue",
            description="The debit value of the associated transaction or entry, formatted as MONEY_100.",
        ),
    ]
    description: Annotated[
        Optional[str], Field(None, description="A description of the task.")
    ]
    engagement_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="engagementId",
            description="Identifies the associated engagement.",
        ),
    ]
    entry_type: Annotated[
        Optional[str],
        Field(
            None,
            alias="entryType",
            description="For AP and AR analyses this is the entry type for the associated entry.",
        ),
    ]
    filter_statement: Annotated[
        Optional[str],
        Field(
            None,
            alias="filterStatement",
            description="The filter statement that was applied when creating this task via a bulk task creation.",
        ),
    ]
    id: Annotated[
        Optional[str], Field(None, description="The unique object identifier.")
    ]
    invoice_ref: Annotated[
        Optional[str],
        Field(
            None,
            alias="invoiceRef",
            description="For AP and AR analyses this is the Invoice ref value for the associated entry.",
        ),
    ]
    last_modified_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="lastModifiedDate",
            description="The date that the object was last updated or modified.",
        ),
    ]
    last_modified_user_info: Annotated[
        Optional[ApiUserInfoRead], Field(None, alias="lastModifiedUserInfo")
    ]
    name: Annotated[
        Optional[str],
        Field(
            None,
            description="The task's name. Generated based on on the related entry or transaction.",
        ),
    ]
    risk_scores: Annotated[
        Optional[Dict[str, int]],
        Field(
            None,
            alias="riskScores",
            description="A map of ensemble names or IDs mapped to their risk score value. The value is a PERCENTAGE_FIXED_POINT type.",
        ),
    ]
    row_id: Annotated[
        Optional[int],
        Field(None, alias="rowId", description="Identifies the associated entry."),
    ]
    sample: Annotated[
        Optional[str], Field(None, description="Which sample this task is a part of.")
    ]
    sample_type: Annotated[
        Optional[SampleType],
        Field(
            None,
            alias="sampleType",
            description="The sampling method used to create this task.",
        ),
    ]
    status: Annotated[
        Optional[Status4], Field(None, description="The current state of the task.")
    ]
    transaction: Annotated[
        Optional[str],
        Field(None, description="The name of the associated transaction."),
    ]
    transaction_id: Annotated[
        Optional[int],
        Field(
            None,
            alias="transactionId",
            description="Identifies the associated transaction.",
        ),
    ]
    type: Annotated[
        Optional[Type11],
        Field(None, description="The type of entry this task is associated with."),
    ]
    vendor_name: Annotated[
        Optional[str],
        Field(
            None,
            alias="vendorName",
            description="For AP analyses this is the vendor name for the associated entry.",
        ),
    ]
    version: Annotated[
        Optional[int],
        Field(
            None,
            description="Indicates the data integrity version to ensure data consistency.",
        ),
    ]


class ApiTextTypeDetailsRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    range: Optional[RangeIntegerRead] = None


class ApiTransactionIdPreviewIndicatorRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    data: Annotated[
        Optional[List[ApiTransactionIdPreviewRowRead]],
        Field(
            None, description="The set of transactions related to a specific indicator."
        ),
    ]
    rating: Annotated[
        Optional[Rating],
        Field(None, description="The quality of the indicator as rated by MindBridge."),
    ]
    value: Annotated[
        Optional[Dict[str, Any]],
        Field(None, description="A value for this specific indicator."),
    ]


class ApiTransactionIdPreviewRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    analysis_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="analysisId",
            description="The unique identifier of the associated analysis.",
        ),
    ]
    analysis_source_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="analysisSourceId",
            description="The unique identifier of the associated analysis source.",
        ),
    ]
    column_selection: Annotated[
        Optional[List[int]],
        Field(
            None,
            alias="columnSelection",
            description="The list of columns used to generate the transaction ID.",
        ),
    ]
    created_user_info: Annotated[
        Optional[ApiUserInfoRead], Field(None, alias="createdUserInfo")
    ]
    creation_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="creationDate",
            description="The date that the object was originally created.",
        ),
    ]
    engagement_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="engagementId",
            description="The unique identifier of the associated engagement.",
        ),
    ]
    entry_previews: Annotated[
        Optional[List[ApiTransactionIdPreviewRowRead]],
        Field(
            None,
            alias="entryPreviews",
            description="Details about the transactions generated by this transaction ID selection.",
        ),
    ]
    id: Annotated[
        Optional[str], Field(None, description="The unique object identifier.")
    ]
    indicators: Annotated[
        Optional[Dict[str, ApiTransactionIdPreviewIndicatorRead]],
        Field(
            None,
            description="The data integrity checks used when selecting a transaction ID.",
        ),
    ]
    last_modified_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="lastModifiedDate",
            description="The date that the object was last updated or modified.",
        ),
    ]
    last_modified_user_info: Annotated[
        Optional[ApiUserInfoRead], Field(None, alias="lastModifiedUserInfo")
    ]
    overall_rating: Annotated[
        Optional[OverallRating],
        Field(
            None,
            alias="overallRating",
            description="The quality of the transaction ID as rated by MindBridge.",
        ),
    ]
    smart_splitter: Annotated[
        Optional[bool],
        Field(
            None,
            alias="smartSplitter",
            description="Indicates whether or not the Smart Splitter was run when selecting a transaction ID.",
        ),
    ]
    type: Annotated[
        Optional[Type13],
        Field(None, description="The type used when selecting a transaction ID."),
    ]
    version: Annotated[
        Optional[int],
        Field(
            None,
            description="Indicates the data integrity version to ensure data consistency.",
        ),
    ]


class PageableObjectRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    offset: Optional[int] = None
    page_number: Annotated[Optional[int], Field(None, alias="pageNumber")]
    page_size: Annotated[Optional[int], Field(None, alias="pageSize")]
    paged: Optional[bool] = None
    sort: Optional[List[SortObject]] = None
    unpaged: Optional[bool] = None


class ApiAnalysisSourceCreateOnly(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    additional_data_column_field: Annotated[
        Optional[str],
        Field(
            None,
            alias="additionalDataColumnField",
            description="When creating an additional data source type, this indicates which additional data column is being targeted.",
        ),
    ]
    analysis_id: Annotated[
        Optional[str],
        Field(
            None, alias="analysisId", description="Identifies the associated analysis."
        ),
    ]
    analysis_period_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="analysisPeriodId",
            description="Identifies the analysis period within MindBridge.",
        ),
    ]
    analysis_source_type_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="analysisSourceTypeId",
            description="Identifies the analysis source type.",
        ),
    ]
    apply_degrouper: Annotated[
        Optional[bool],
        Field(
            None,
            alias="applyDegrouper",
            description="Indicates whether or not the degrouper should be applied.",
        ),
    ]
    engagement_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="engagementId",
            description="Identifies the associated engagement.",
        ),
    ]
    file_manager_file_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="fileManagerFileId",
            description="Identifies the specific file manager file within MindBridge.",
        ),
    ]
    proposed_ambiguous_column_resolutions: Annotated[
        Optional[List[ApiProposedAmbiguousColumnResolutionCreateOnly]],
        Field(
            None,
            alias="proposedAmbiguousColumnResolutions",
            description="Details about the virtual columns added during file ingestion.",
        ),
    ]
    proposed_column_mappings: Annotated[
        Optional[List[ApiProposedColumnMappingCreateOnly]],
        Field(
            None,
            alias="proposedColumnMappings",
            description="Details about the proposed column mapping.",
        ),
    ]
    proposed_transaction_id_selection: Annotated[
        Optional[ApiTransactionIdSelectionCreateOnly],
        Field(None, alias="proposedTransactionIdSelection"),
    ]
    proposed_virtual_columns: Annotated[
        Optional[
            List[
                Union[
                    ApiProposedDuplicateVirtualColumnCreateOnly,
                    ApiProposedJoinVirtualColumnCreateOnly,
                    ApiProposedSplitByDelimiterVirtualColumnCreateOnly,
                    ApiProposedSplitByPositionVirtualColumnCreateOnly,
                ]
            ]
        ],
        Field(
            None,
            alias="proposedVirtualColumns",
            description="Details about the proposed virtual columns added during the file import process.",
        ),
    ]
    target_workflow_state: Annotated[
        Optional[TargetWorkflowState],
        Field(
            None,
            alias="targetWorkflowState",
            description="The state that the current workflow will advance to.",
        ),
    ]
    warnings_ignored: Annotated[
        Optional[bool],
        Field(
            None,
            alias="warningsIgnored",
            description="Indicates whether or not warnings should be ignored.",
        ),
    ]


class ApiAnalysisSourceUpdate(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    ambiguous_column_resolutions: Annotated[
        Optional[List[ApiAmbiguousColumnUpdate]],
        Field(
            None,
            alias="ambiguousColumnResolutions",
            description="Details about resolutions to ambiguity in a column.",
        ),
    ]
    apply_degrouper: Annotated[
        Optional[bool],
        Field(
            None,
            alias="applyDegrouper",
            description="Indicates whether or not the degrouper should be applied.",
        ),
    ]
    column_mappings: Annotated[
        Optional[List[ApiColumnMappingUpdate]],
        Field(
            None, alias="columnMappings", description="Details about column mapping."
        ),
    ]
    proposed_ambiguous_column_resolutions: Annotated[
        Optional[List[ApiProposedAmbiguousColumnResolutionUpdate]],
        Field(
            None,
            alias="proposedAmbiguousColumnResolutions",
            description="Details about the virtual columns added during file ingestion.",
        ),
    ]
    proposed_column_mappings: Annotated[
        Optional[List[ApiProposedColumnMappingUpdate]],
        Field(
            None,
            alias="proposedColumnMappings",
            description="Details about the proposed column mapping.",
        ),
    ]
    proposed_transaction_id_selection: Annotated[
        Optional[ApiTransactionIdSelectionUpdate],
        Field(None, alias="proposedTransactionIdSelection"),
    ]
    proposed_virtual_columns: Annotated[
        Optional[
            List[
                Union[
                    ApiProposedDuplicateVirtualColumnUpdate,
                    ApiProposedJoinVirtualColumnUpdate,
                    ApiProposedSplitByDelimiterVirtualColumnUpdate,
                    ApiProposedSplitByPositionVirtualColumnUpdate,
                ]
            ]
        ],
        Field(
            None,
            alias="proposedVirtualColumns",
            description="Details about the proposed virtual columns added during the file import process.",
        ),
    ]
    target_workflow_state: Annotated[
        Optional[TargetWorkflowState],
        Field(
            None,
            alias="targetWorkflowState",
            description="The state that the current workflow will advance to.",
        ),
    ]
    transaction_id_selection: Annotated[
        Optional[ApiTransactionIdSelectionUpdate],
        Field(None, alias="transactionIdSelection"),
    ]
    version: Annotated[
        Optional[int],
        Field(
            None,
            description="Indicates the data integrity version to ensure data consistency.",
        ),
    ]
    virtual_columns: Annotated[
        Optional[
            List[
                Union[
                    ApiDuplicateVirtualColumnUpdate,
                    ApiJoinVirtualColumnUpdate,
                    ApiSplitByDelimiterVirtualColumnUpdate,
                    ApiSplitByPositionVirtualColumnUpdate,
                ]
            ]
        ],
        Field(
            None,
            alias="virtualColumns",
            description="Details about the virtual columns added during file ingestion. ",
        ),
    ]
    warnings_ignored: Annotated[
        Optional[bool],
        Field(
            None,
            alias="warningsIgnored",
            description="Indicates whether or not warnings should be ignored.",
        ),
    ]


class ApiDataTypeMetricsRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    data_previews: Annotated[
        Optional[List[ApiDataPreviewRead]], Field(None, alias="dataPreviews")
    ]
    date_type_details: Annotated[
        Optional[ApiDateTypeDetailsRead], Field(None, alias="dateTypeDetails")
    ]
    detected_types: Annotated[
        Optional[List[DetectedType]], Field(None, alias="detectedTypes")
    ]
    dominant_type: Annotated[Optional[DominantType], Field(None, alias="dominantType")]
    non_null_value_count: Annotated[
        Optional[int], Field(None, alias="nonNullValueCount")
    ]
    numeric_type_details: Annotated[
        Optional[ApiNumericTypeDetailsRead], Field(None, alias="numericTypeDetails")
    ]
    state: Optional[State] = None
    text_type_details: Annotated[
        Optional[ApiTextTypeDetailsRead], Field(None, alias="textTypeDetails")
    ]
    type_counts: Annotated[Optional[Dict[str, int]], Field(None, alias="typeCounts")]


class ApiFileManagerDirectoryRead(ApiFileManagerEntityRead):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    name: Annotated[
        Optional[str], Field(None, description="The current name of the directory.")
    ]
    engagement_id: Annotated[
        str,
        Field(
            alias="engagementId", description="Identifies the associated engagement."
        ),
    ]
    version: Annotated[
        int,
        Field(
            description="Indicates the data integrity version to ensure data consistency."
        ),
    ]


class PageApiAccountGroupRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    content: Optional[List[ApiAccountGroupRead]] = None
    empty: Optional[bool] = None
    first: Optional[bool] = None
    last: Optional[bool] = None
    number: Optional[int] = None
    number_of_elements: Annotated[Optional[int], Field(None, alias="numberOfElements")]
    pageable: Optional[PageableObjectRead] = None
    size: Optional[int] = None
    sort: Optional[List[SortObject]] = None
    total_elements: Annotated[Optional[int], Field(None, alias="totalElements")]
    total_pages: Annotated[Optional[int], Field(None, alias="totalPages")]


class PageApiAccountGroupingRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    content: Optional[List[ApiAccountGroupingRead]] = None
    empty: Optional[bool] = None
    first: Optional[bool] = None
    last: Optional[bool] = None
    number: Optional[int] = None
    number_of_elements: Annotated[Optional[int], Field(None, alias="numberOfElements")]
    pageable: Optional[PageableObjectRead] = None
    size: Optional[int] = None
    sort: Optional[List[SortObject]] = None
    total_elements: Annotated[Optional[int], Field(None, alias="totalElements")]
    total_pages: Annotated[Optional[int], Field(None, alias="totalPages")]


class PageApiAnalysisSourceTypeRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    content: Optional[List[ApiAnalysisSourceTypeRead]] = None
    empty: Optional[bool] = None
    first: Optional[bool] = None
    last: Optional[bool] = None
    number: Optional[int] = None
    number_of_elements: Annotated[Optional[int], Field(None, alias="numberOfElements")]
    pageable: Optional[PageableObjectRead] = None
    size: Optional[int] = None
    sort: Optional[List[SortObject]] = None
    total_elements: Annotated[Optional[int], Field(None, alias="totalElements")]
    total_pages: Annotated[Optional[int], Field(None, alias="totalPages")]


class PageApiAnalysisTypeRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    content: Optional[List[ApiAnalysisTypeRead]] = None
    empty: Optional[bool] = None
    first: Optional[bool] = None
    last: Optional[bool] = None
    number: Optional[int] = None
    number_of_elements: Annotated[Optional[int], Field(None, alias="numberOfElements")]
    pageable: Optional[PageableObjectRead] = None
    size: Optional[int] = None
    sort: Optional[List[SortObject]] = None
    total_elements: Annotated[Optional[int], Field(None, alias="totalElements")]
    total_pages: Annotated[Optional[int], Field(None, alias="totalPages")]


class PageApiAnalysisRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    content: Optional[List[ApiAnalysisRead]] = None
    empty: Optional[bool] = None
    first: Optional[bool] = None
    last: Optional[bool] = None
    number: Optional[int] = None
    number_of_elements: Annotated[Optional[int], Field(None, alias="numberOfElements")]
    pageable: Optional[PageableObjectRead] = None
    size: Optional[int] = None
    sort: Optional[List[SortObject]] = None
    total_elements: Annotated[Optional[int], Field(None, alias="totalElements")]
    total_pages: Annotated[Optional[int], Field(None, alias="totalPages")]


class PageApiApiTokenRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    content: Optional[List[ApiApiTokenRead]] = None
    empty: Optional[bool] = None
    first: Optional[bool] = None
    last: Optional[bool] = None
    number: Optional[int] = None
    number_of_elements: Annotated[Optional[int], Field(None, alias="numberOfElements")]
    pageable: Optional[PageableObjectRead] = None
    size: Optional[int] = None
    sort: Optional[List[SortObject]] = None
    total_elements: Annotated[Optional[int], Field(None, alias="totalElements")]
    total_pages: Annotated[Optional[int], Field(None, alias="totalPages")]


class PageApiAsyncResultRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    content: Optional[List[ApiAsyncResultRead]] = None
    empty: Optional[bool] = None
    first: Optional[bool] = None
    last: Optional[bool] = None
    number: Optional[int] = None
    number_of_elements: Annotated[Optional[int], Field(None, alias="numberOfElements")]
    pageable: Optional[PageableObjectRead] = None
    size: Optional[int] = None
    sort: Optional[List[SortObject]] = None
    total_elements: Annotated[Optional[int], Field(None, alias="totalElements")]
    total_pages: Annotated[Optional[int], Field(None, alias="totalPages")]


class PageApiChunkedFileRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    content: Optional[List[ApiChunkedFileRead]] = None
    empty: Optional[bool] = None
    first: Optional[bool] = None
    last: Optional[bool] = None
    number: Optional[int] = None
    number_of_elements: Annotated[Optional[int], Field(None, alias="numberOfElements")]
    pageable: Optional[PageableObjectRead] = None
    size: Optional[int] = None
    sort: Optional[List[SortObject]] = None
    total_elements: Annotated[Optional[int], Field(None, alias="totalElements")]
    total_pages: Annotated[Optional[int], Field(None, alias="totalPages")]


class PageApiDataTableRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    content: Optional[List[ApiDataTableRead]] = None
    empty: Optional[bool] = None
    first: Optional[bool] = None
    last: Optional[bool] = None
    number: Optional[int] = None
    number_of_elements: Annotated[Optional[int], Field(None, alias="numberOfElements")]
    pageable: Optional[PageableObjectRead] = None
    size: Optional[int] = None
    sort: Optional[List[SortObject]] = None
    total_elements: Annotated[Optional[int], Field(None, alias="totalElements")]
    total_pages: Annotated[Optional[int], Field(None, alias="totalPages")]


class PageApiEngagementAccountGroupingRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    content: Optional[List[ApiEngagementAccountGroupingRead]] = None
    empty: Optional[bool] = None
    first: Optional[bool] = None
    last: Optional[bool] = None
    number: Optional[int] = None
    number_of_elements: Annotated[Optional[int], Field(None, alias="numberOfElements")]
    pageable: Optional[PageableObjectRead] = None
    size: Optional[int] = None
    sort: Optional[List[SortObject]] = None
    total_elements: Annotated[Optional[int], Field(None, alias="totalElements")]
    total_pages: Annotated[Optional[int], Field(None, alias="totalPages")]


class PageApiEngagementRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    content: Optional[List[ApiEngagementRead]] = None
    empty: Optional[bool] = None
    first: Optional[bool] = None
    last: Optional[bool] = None
    number: Optional[int] = None
    number_of_elements: Annotated[Optional[int], Field(None, alias="numberOfElements")]
    pageable: Optional[PageableObjectRead] = None
    size: Optional[int] = None
    sort: Optional[List[SortObject]] = None
    total_elements: Annotated[Optional[int], Field(None, alias="totalElements")]
    total_pages: Annotated[Optional[int], Field(None, alias="totalPages")]


class PageApiFileExportRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    content: Optional[List[ApiFileExportRead]] = None
    empty: Optional[bool] = None
    first: Optional[bool] = None
    last: Optional[bool] = None
    number: Optional[int] = None
    number_of_elements: Annotated[Optional[int], Field(None, alias="numberOfElements")]
    pageable: Optional[PageableObjectRead] = None
    size: Optional[int] = None
    sort: Optional[List[SortObject]] = None
    total_elements: Annotated[Optional[int], Field(None, alias="totalElements")]
    total_pages: Annotated[Optional[int], Field(None, alias="totalPages")]


class PageApiFileManagerEntityRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    content: Optional[
        List[Union[ApiFileManagerDirectoryRead, ApiFileManagerFileRead]]
    ] = None
    empty: Optional[bool] = None
    first: Optional[bool] = None
    last: Optional[bool] = None
    number: Optional[int] = None
    number_of_elements: Annotated[Optional[int], Field(None, alias="numberOfElements")]
    pageable: Optional[PageableObjectRead] = None
    size: Optional[int] = None
    sort: Optional[List[SortObject]] = None
    total_elements: Annotated[Optional[int], Field(None, alias="totalElements")]
    total_pages: Annotated[Optional[int], Field(None, alias="totalPages")]


class PageApiLibraryRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    content: Optional[List[ApiLibraryRead]] = None
    empty: Optional[bool] = None
    first: Optional[bool] = None
    last: Optional[bool] = None
    number: Optional[int] = None
    number_of_elements: Annotated[Optional[int], Field(None, alias="numberOfElements")]
    pageable: Optional[PageableObjectRead] = None
    size: Optional[int] = None
    sort: Optional[List[SortObject]] = None
    total_elements: Annotated[Optional[int], Field(None, alias="totalElements")]
    total_pages: Annotated[Optional[int], Field(None, alias="totalPages")]


class PageApiOrganizationRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    content: Optional[List[ApiOrganizationRead]] = None
    empty: Optional[bool] = None
    first: Optional[bool] = None
    last: Optional[bool] = None
    number: Optional[int] = None
    number_of_elements: Annotated[Optional[int], Field(None, alias="numberOfElements")]
    pageable: Optional[PageableObjectRead] = None
    size: Optional[int] = None
    sort: Optional[List[SortObject]] = None
    total_elements: Annotated[Optional[int], Field(None, alias="totalElements")]
    total_pages: Annotated[Optional[int], Field(None, alias="totalPages")]


class PageApiPopulationTagRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    content: Optional[List[ApiPopulationTagRead]] = None
    empty: Optional[bool] = None
    first: Optional[bool] = None
    last: Optional[bool] = None
    number: Optional[int] = None
    number_of_elements: Annotated[Optional[int], Field(None, alias="numberOfElements")]
    pageable: Optional[PageableObjectRead] = None
    size: Optional[int] = None
    sort: Optional[List[SortObject]] = None
    total_elements: Annotated[Optional[int], Field(None, alias="totalElements")]
    total_pages: Annotated[Optional[int], Field(None, alias="totalPages")]


class PageApiTaskRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    content: Optional[List[ApiTaskRead]] = None
    empty: Optional[bool] = None
    first: Optional[bool] = None
    last: Optional[bool] = None
    number: Optional[int] = None
    number_of_elements: Annotated[Optional[int], Field(None, alias="numberOfElements")]
    pageable: Optional[PageableObjectRead] = None
    size: Optional[int] = None
    sort: Optional[List[SortObject]] = None
    total_elements: Annotated[Optional[int], Field(None, alias="totalElements")]
    total_pages: Annotated[Optional[int], Field(None, alias="totalPages")]


class PageApiTransactionIdPreviewRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    content: Optional[List[ApiTransactionIdPreviewRead]] = None
    empty: Optional[bool] = None
    first: Optional[bool] = None
    last: Optional[bool] = None
    number: Optional[int] = None
    number_of_elements: Annotated[Optional[int], Field(None, alias="numberOfElements")]
    pageable: Optional[PageableObjectRead] = None
    size: Optional[int] = None
    sort: Optional[List[SortObject]] = None
    total_elements: Annotated[Optional[int], Field(None, alias="totalElements")]
    total_pages: Annotated[Optional[int], Field(None, alias="totalPages")]


class PageApiUserRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    content: Optional[List[ApiUserRead]] = None
    empty: Optional[bool] = None
    first: Optional[bool] = None
    last: Optional[bool] = None
    number: Optional[int] = None
    number_of_elements: Annotated[Optional[int], Field(None, alias="numberOfElements")]
    pageable: Optional[PageableObjectRead] = None
    size: Optional[int] = None
    sort: Optional[List[SortObject]] = None
    total_elements: Annotated[Optional[int], Field(None, alias="totalElements")]
    total_pages: Annotated[Optional[int], Field(None, alias="totalPages")]


class ApiColumnMetadataRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    cell_length_metrics: Annotated[
        Optional[ApiCountMetricsRead], Field(None, alias="cellLengthMetrics")
    ]
    data_type_metrics: Annotated[
        Optional[ApiDataTypeMetricsRead], Field(None, alias="dataTypeMetrics")
    ]
    density_metrics: Annotated[
        Optional[ApiDensityMetricsRead], Field(None, alias="densityMetrics")
    ]
    distinct_value_metrics: Annotated[
        Optional[ApiDistinctValueMetricsRead], Field(None, alias="distinctValueMetrics")
    ]
    null_value_metrics: Annotated[
        Optional[ApiCountMetricsRead], Field(None, alias="nullValueMetrics")
    ]
    scientific_notation_metrics: Annotated[
        Optional[ApiCountMetricsRead], Field(None, alias="scientificNotationMetrics")
    ]
    special_character_metrics: Annotated[
        Optional[ApiCountMetricsRead], Field(None, alias="specialCharacterMetrics")
    ]


class ApiColumnDataRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    column_metadata: Annotated[
        Optional[ApiColumnMetadataRead], Field(None, alias="columnMetadata")
    ]
    column_name: Annotated[Optional[str], Field(None, alias="columnName")]
    position: Optional[int] = None
    row_sample: Annotated[Optional[List[str]], Field(None, alias="rowSample")]
    synthetic: Optional[bool] = None


class ApiTabularFileInfoRead(ApiFileInfoRead):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    column_data: Annotated[
        Optional[List[ApiColumnDataRead]],
        Field(
            None,
            alias="columnData",
            description="The metadata associated with each individual column within the table.",
        ),
    ]
    header_row_index: Annotated[
        Optional[int],
        Field(
            None,
            alias="headerRowIndex",
            description="The line where the table header is located.",
        ),
    ]
    table_metadata: Annotated[
        Optional[ApiTableMetadataRead], Field(None, alias="tableMetadata")
    ]


class ApiAnalysisSourceRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    additional_data_column_field: Annotated[
        Optional[str],
        Field(
            None,
            alias="additionalDataColumnField",
            description="When creating an additional data source type, this indicates which additional data column is being targeted.",
        ),
    ]
    ambiguous_column_resolutions: Annotated[
        Optional[List[ApiAmbiguousColumnRead]],
        Field(
            None,
            alias="ambiguousColumnResolutions",
            description="Details about resolutions to ambiguity in a column.",
        ),
    ]
    analysis_id: Annotated[
        Optional[str],
        Field(
            None, alias="analysisId", description="Identifies the associated analysis."
        ),
    ]
    analysis_period_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="analysisPeriodId",
            description="Identifies the analysis period within MindBridge.",
        ),
    ]
    analysis_source_type_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="analysisSourceTypeId",
            description="Identifies the analysis source type.",
        ),
    ]
    apply_degrouper: Annotated[
        Optional[bool],
        Field(
            None,
            alias="applyDegrouper",
            description="Indicates whether or not the degrouper should be applied.",
        ),
    ]
    column_mappings: Annotated[
        Optional[List[ApiColumnMappingRead]],
        Field(
            None, alias="columnMappings", description="Details about column mapping."
        ),
    ]
    created_user_info: Annotated[
        Optional[ApiUserInfoRead], Field(None, alias="createdUserInfo")
    ]
    creation_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="creationDate",
            description="The date that the object was originally created.",
        ),
    ]
    degrouper_applied: Annotated[
        Optional[bool],
        Field(
            None,
            alias="degrouperApplied",
            description="Indicates whether or not the degrouper was applied.",
        ),
    ]
    detected_format: Annotated[
        Optional[DetectedFormat],
        Field(
            None,
            alias="detectedFormat",
            description="The data format that MindBridge detected.",
        ),
    ]
    engagement_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="engagementId",
            description="Identifies the associated engagement.",
        ),
    ]
    errors: Annotated[
        Optional[List[ApiMessageRead]],
        Field(
            None,
            description="Details about the errors associated with the specific source.",
        ),
    ]
    file_info: Annotated[
        Optional[Union[ApiFileInfoRead, ApiTabularFileInfoRead]],
        Field(
            None,
            alias="fileInfo",
            description="Details about the file being imported into MindBridge.",
        ),
    ]
    file_manager_file_id: Annotated[
        Optional[str],
        Field(
            None,
            alias="fileManagerFileId",
            description="Identifies the specific file manager file within MindBridge.",
        ),
    ]
    id: Annotated[
        Optional[str], Field(None, description="The unique object identifier.")
    ]
    last_modified_date: Annotated[
        Optional[AwareDatetime],
        Field(
            None,
            alias="lastModifiedDate",
            description="The date that the object was last updated or modified.",
        ),
    ]
    last_modified_user_info: Annotated[
        Optional[ApiUserInfoRead], Field(None, alias="lastModifiedUserInfo")
    ]
    proposed_ambiguous_column_resolutions: Annotated[
        Optional[List[ApiProposedAmbiguousColumnResolutionRead]],
        Field(
            None,
            alias="proposedAmbiguousColumnResolutions",
            description="Details about the virtual columns added during file ingestion.",
        ),
    ]
    proposed_column_mappings: Annotated[
        Optional[List[ApiProposedColumnMappingRead]],
        Field(
            None,
            alias="proposedColumnMappings",
            description="Details about the proposed column mapping.",
        ),
    ]
    proposed_transaction_id_selection: Annotated[
        Optional[ApiTransactionIdSelectionRead],
        Field(None, alias="proposedTransactionIdSelection"),
    ]
    proposed_virtual_columns: Annotated[
        Optional[
            List[
                Union[
                    ApiProposedDuplicateVirtualColumnRead,
                    ApiProposedJoinVirtualColumnRead,
                    ApiProposedSplitByDelimiterVirtualColumnRead,
                    ApiProposedSplitByPositionVirtualColumnRead,
                ]
            ]
        ],
        Field(
            None,
            alias="proposedVirtualColumns",
            description="Details about the proposed virtual columns added during the file import process.",
        ),
    ]
    target_workflow_state: Annotated[
        Optional[TargetWorkflowState],
        Field(
            None,
            alias="targetWorkflowState",
            description="The state that the current workflow will advance to.",
        ),
    ]
    transaction_id_selection: Annotated[
        Optional[ApiTransactionIdSelectionRead],
        Field(None, alias="transactionIdSelection"),
    ]
    version: Annotated[
        Optional[int],
        Field(
            None,
            description="Indicates the data integrity version to ensure data consistency.",
        ),
    ]
    virtual_columns: Annotated[
        Optional[
            List[
                Union[
                    ApiDuplicateVirtualColumnRead,
                    ApiJoinVirtualColumnRead,
                    ApiSplitByDelimiterVirtualColumnRead,
                    ApiSplitByPositionVirtualColumnRead,
                ]
            ]
        ],
        Field(
            None,
            alias="virtualColumns",
            description="Details about the virtual columns added during file ingestion. ",
        ),
    ]
    warnings: Annotated[
        Optional[List[ApiMessageRead]],
        Field(
            None, description="Details about the warnings associated with the source."
        ),
    ]
    warnings_ignored: Annotated[
        Optional[bool],
        Field(
            None,
            alias="warningsIgnored",
            description="Indicates whether or not warnings should be ignored.",
        ),
    ]
    workflow_state: Annotated[
        Optional[WorkflowState],
        Field(
            None,
            alias="workflowState",
            description="The current state of the workflow.",
        ),
    ]


class PageApiAnalysisSourceRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    content: Optional[List[ApiAnalysisSourceRead]] = None
    empty: Optional[bool] = None
    first: Optional[bool] = None
    last: Optional[bool] = None
    number: Optional[int] = None
    number_of_elements: Annotated[Optional[int], Field(None, alias="numberOfElements")]
    pageable: Optional[PageableObjectRead] = None
    size: Optional[int] = None
    sort: Optional[List[SortObject]] = None
    total_elements: Annotated[Optional[int], Field(None, alias="totalElements")]
    total_pages: Annotated[Optional[int], Field(None, alias="totalPages")]


class ApiDataTableExportRequest(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    csv_configuration: Annotated[
        Optional[ApiCsvConfiguration], Field(None, alias="csvConfiguration")
    ]
    fields: Annotated[
        Optional[List[str]],
        Field(None, description="The data table fields to be included in the results."),
    ]
    inner_list_csv_configuration: Annotated[
        Optional[ApiCsvConfiguration], Field(None, alias="innerListCsvConfiguration")
    ]
    limit: Annotated[
        Optional[int],
        Field(None, description="The number of results to be returned.", ge=1),
    ]
    query: Optional[MindBridgeQueryTerm] = None
    sort: Optional[ApiDataTableQuerySortOrder] = None


class ApiDataTableQueryRead(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    fields: Annotated[
        Optional[List[str]],
        Field(None, description="The data table fields to be included in the results."),
    ]
    page: Annotated[
        Optional[int],
        Field(
            None,
            description="The specific page of results. This operates on a zero-based page index (0..N).",
            ge=0,
        ),
    ]
    page_size: Annotated[
        Optional[int],
        Field(
            None,
            alias="pageSize",
            description="The number of results to be returned on each page.",
            ge=1,
            le=100,
        ),
    ]
    query: Optional[MindBridgeQueryTerm] = None
    sort: Optional[ApiDataTableQuerySortOrderRead] = None


class MindBridgeQueryTerm15(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    field_and: Annotated[Optional[List[MindBridgeQueryTerm]], Field(None, alias="$and")]


class MindBridgeQueryTerm16(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    field_or: Annotated[Optional[List[MindBridgeQueryTerm]], Field(None, alias="$or")]


class MindBridgeQueryTerm(
    RootModel[
        Optional[
            Union[
                Dict[str, Union[int, float, bool, str]],
                Dict[str, MindBridgeQueryTerm1],
                Dict[str, MindBridgeQueryTerm2],
                Dict[str, MindBridgeQueryTerm3],
                Dict[str, MindBridgeQueryTerm4],
                Dict[str, MindBridgeQueryTerm5],
                Dict[str, MindBridgeQueryTerm6],
                Dict[str, MindBridgeQueryTerm7],
                Dict[str, MindBridgeQueryTerm9],
                Dict[str, MindBridgeQueryTerm10],
                Dict[str, MindBridgeQueryTerm11],
                Dict[str, MindBridgeQueryTerm12],
                Dict[str, MindBridgeQueryTerm13],
                Dict[str, MindBridgeQueryTerm14],
                MindBridgeQueryTerm15,
                MindBridgeQueryTerm16,
                MindBridgeQueryTerm17,
                MindBridgeQueryTerm18,
                Dict[str, Any],
            ]
        ]
    ]
):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Optional[
        Union[
            Dict[str, Union[int, float, bool, str]],
            Dict[str, MindBridgeQueryTerm1],
            Dict[str, MindBridgeQueryTerm2],
            Dict[str, MindBridgeQueryTerm3],
            Dict[str, MindBridgeQueryTerm4],
            Dict[str, MindBridgeQueryTerm5],
            Dict[str, MindBridgeQueryTerm6],
            Dict[str, MindBridgeQueryTerm7],
            Dict[str, MindBridgeQueryTerm9],
            Dict[str, MindBridgeQueryTerm10],
            Dict[str, MindBridgeQueryTerm11],
            Dict[str, MindBridgeQueryTerm12],
            Dict[str, MindBridgeQueryTerm13],
            Dict[str, MindBridgeQueryTerm14],
            MindBridgeQueryTerm15,
            MindBridgeQueryTerm16,
            MindBridgeQueryTerm17,
            MindBridgeQueryTerm18,
            Dict[str, Any],
        ]
    ] = None


class ShieldQueryTermRead(RootModel[Optional[MindBridgeQueryTerm]]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Optional[MindBridgeQueryTerm] = None


ApiDataTableExportRequest.model_rebuild()
ApiDataTableQueryRead.model_rebuild()
MindBridgeQueryTerm15.model_rebuild()
MindBridgeQueryTerm16.model_rebuild()
