"""
Type annotations for codecommit service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_codecommit.client import CodeCommitClient

    session = get_session()
    async with session.create_client("codecommit") as client:
        client: CodeCommitClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    ApprovalStateType,
    ConflictDetailLevelTypeEnumType,
    ConflictResolutionStrategyTypeEnumType,
    FileModeTypeEnumType,
    MergeOptionTypeEnumType,
    OrderEnumType,
    OverrideStatusType,
    PullRequestEventTypeType,
    PullRequestStatusEnumType,
    SortByEnumType,
)
from .paginator import (
    DescribePullRequestEventsPaginator,
    GetCommentsForComparedCommitPaginator,
    GetCommentsForPullRequestPaginator,
    GetDifferencesPaginator,
    ListBranchesPaginator,
    ListPullRequestsPaginator,
    ListRepositoriesPaginator,
)
from .type_defs import (
    BatchAssociateApprovalRuleTemplateWithRepositoriesOutputTypeDef,
    BatchDescribeMergeConflictsOutputTypeDef,
    BatchDisassociateApprovalRuleTemplateFromRepositoriesOutputTypeDef,
    BatchGetCommitsOutputTypeDef,
    BatchGetRepositoriesOutputTypeDef,
    BlobTypeDef,
    ConflictResolutionTypeDef,
    CreateApprovalRuleTemplateOutputTypeDef,
    CreateCommitOutputTypeDef,
    CreatePullRequestApprovalRuleOutputTypeDef,
    CreatePullRequestOutputTypeDef,
    CreateRepositoryOutputTypeDef,
    CreateUnreferencedMergeCommitOutputTypeDef,
    DeleteApprovalRuleTemplateOutputTypeDef,
    DeleteBranchOutputTypeDef,
    DeleteCommentContentOutputTypeDef,
    DeleteFileEntryTypeDef,
    DeleteFileOutputTypeDef,
    DeletePullRequestApprovalRuleOutputTypeDef,
    DeleteRepositoryOutputTypeDef,
    DescribeMergeConflictsOutputTypeDef,
    DescribePullRequestEventsOutputTypeDef,
    EmptyResponseMetadataTypeDef,
    EvaluatePullRequestApprovalRulesOutputTypeDef,
    GetApprovalRuleTemplateOutputTypeDef,
    GetBlobOutputTypeDef,
    GetBranchOutputTypeDef,
    GetCommentOutputTypeDef,
    GetCommentReactionsOutputTypeDef,
    GetCommentsForComparedCommitOutputTypeDef,
    GetCommentsForPullRequestOutputTypeDef,
    GetCommitOutputTypeDef,
    GetDifferencesOutputTypeDef,
    GetFileOutputTypeDef,
    GetFolderOutputTypeDef,
    GetMergeCommitOutputTypeDef,
    GetMergeConflictsOutputTypeDef,
    GetMergeOptionsOutputTypeDef,
    GetPullRequestApprovalStatesOutputTypeDef,
    GetPullRequestOutputTypeDef,
    GetPullRequestOverrideStateOutputTypeDef,
    GetRepositoryOutputTypeDef,
    GetRepositoryTriggersOutputTypeDef,
    ListApprovalRuleTemplatesOutputTypeDef,
    ListAssociatedApprovalRuleTemplatesForRepositoryOutputTypeDef,
    ListBranchesOutputTypeDef,
    ListFileCommitHistoryResponseTypeDef,
    ListPullRequestsOutputTypeDef,
    ListRepositoriesForApprovalRuleTemplateOutputTypeDef,
    ListRepositoriesOutputTypeDef,
    ListTagsForResourceOutputTypeDef,
    LocationTypeDef,
    MergeBranchesByFastForwardOutputTypeDef,
    MergeBranchesBySquashOutputTypeDef,
    MergeBranchesByThreeWayOutputTypeDef,
    MergePullRequestByFastForwardOutputTypeDef,
    MergePullRequestBySquashOutputTypeDef,
    MergePullRequestByThreeWayOutputTypeDef,
    PostCommentForComparedCommitOutputTypeDef,
    PostCommentForPullRequestOutputTypeDef,
    PostCommentReplyOutputTypeDef,
    PutFileEntryTypeDef,
    PutFileOutputTypeDef,
    PutRepositoryTriggersOutputTypeDef,
    RepositoryTriggerUnionTypeDef,
    SetFileModeEntryTypeDef,
    TargetTypeDef,
    TestRepositoryTriggersOutputTypeDef,
    UpdateApprovalRuleTemplateContentOutputTypeDef,
    UpdateApprovalRuleTemplateDescriptionOutputTypeDef,
    UpdateApprovalRuleTemplateNameOutputTypeDef,
    UpdateCommentOutputTypeDef,
    UpdatePullRequestApprovalRuleContentOutputTypeDef,
    UpdatePullRequestDescriptionOutputTypeDef,
    UpdatePullRequestStatusOutputTypeDef,
    UpdatePullRequestTitleOutputTypeDef,
    UpdateRepositoryEncryptionKeyOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("CodeCommitClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ActorDoesNotExistException: Type[BotocoreClientError]
    ApprovalRuleContentRequiredException: Type[BotocoreClientError]
    ApprovalRuleDoesNotExistException: Type[BotocoreClientError]
    ApprovalRuleNameAlreadyExistsException: Type[BotocoreClientError]
    ApprovalRuleNameRequiredException: Type[BotocoreClientError]
    ApprovalRuleTemplateContentRequiredException: Type[BotocoreClientError]
    ApprovalRuleTemplateDoesNotExistException: Type[BotocoreClientError]
    ApprovalRuleTemplateInUseException: Type[BotocoreClientError]
    ApprovalRuleTemplateNameAlreadyExistsException: Type[BotocoreClientError]
    ApprovalRuleTemplateNameRequiredException: Type[BotocoreClientError]
    ApprovalStateRequiredException: Type[BotocoreClientError]
    AuthorDoesNotExistException: Type[BotocoreClientError]
    BeforeCommitIdAndAfterCommitIdAreSameException: Type[BotocoreClientError]
    BlobIdDoesNotExistException: Type[BotocoreClientError]
    BlobIdRequiredException: Type[BotocoreClientError]
    BranchDoesNotExistException: Type[BotocoreClientError]
    BranchNameExistsException: Type[BotocoreClientError]
    BranchNameIsTagNameException: Type[BotocoreClientError]
    BranchNameRequiredException: Type[BotocoreClientError]
    CannotDeleteApprovalRuleFromTemplateException: Type[BotocoreClientError]
    CannotModifyApprovalRuleFromTemplateException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ClientRequestTokenRequiredException: Type[BotocoreClientError]
    CommentContentRequiredException: Type[BotocoreClientError]
    CommentContentSizeLimitExceededException: Type[BotocoreClientError]
    CommentDeletedException: Type[BotocoreClientError]
    CommentDoesNotExistException: Type[BotocoreClientError]
    CommentIdRequiredException: Type[BotocoreClientError]
    CommentNotCreatedByCallerException: Type[BotocoreClientError]
    CommitDoesNotExistException: Type[BotocoreClientError]
    CommitIdDoesNotExistException: Type[BotocoreClientError]
    CommitIdRequiredException: Type[BotocoreClientError]
    CommitIdsLimitExceededException: Type[BotocoreClientError]
    CommitIdsListRequiredException: Type[BotocoreClientError]
    CommitMessageLengthExceededException: Type[BotocoreClientError]
    CommitRequiredException: Type[BotocoreClientError]
    ConcurrentReferenceUpdateException: Type[BotocoreClientError]
    DefaultBranchCannotBeDeletedException: Type[BotocoreClientError]
    DirectoryNameConflictsWithFileNameException: Type[BotocoreClientError]
    EncryptionIntegrityChecksFailedException: Type[BotocoreClientError]
    EncryptionKeyAccessDeniedException: Type[BotocoreClientError]
    EncryptionKeyDisabledException: Type[BotocoreClientError]
    EncryptionKeyInvalidIdException: Type[BotocoreClientError]
    EncryptionKeyInvalidUsageException: Type[BotocoreClientError]
    EncryptionKeyNotFoundException: Type[BotocoreClientError]
    EncryptionKeyRequiredException: Type[BotocoreClientError]
    EncryptionKeyUnavailableException: Type[BotocoreClientError]
    FileContentAndSourceFileSpecifiedException: Type[BotocoreClientError]
    FileContentRequiredException: Type[BotocoreClientError]
    FileContentSizeLimitExceededException: Type[BotocoreClientError]
    FileDoesNotExistException: Type[BotocoreClientError]
    FileEntryRequiredException: Type[BotocoreClientError]
    FileModeRequiredException: Type[BotocoreClientError]
    FileNameConflictsWithDirectoryNameException: Type[BotocoreClientError]
    FilePathConflictsWithSubmodulePathException: Type[BotocoreClientError]
    FileTooLargeException: Type[BotocoreClientError]
    FolderContentSizeLimitExceededException: Type[BotocoreClientError]
    FolderDoesNotExistException: Type[BotocoreClientError]
    IdempotencyParameterMismatchException: Type[BotocoreClientError]
    InvalidActorArnException: Type[BotocoreClientError]
    InvalidApprovalRuleContentException: Type[BotocoreClientError]
    InvalidApprovalRuleNameException: Type[BotocoreClientError]
    InvalidApprovalRuleTemplateContentException: Type[BotocoreClientError]
    InvalidApprovalRuleTemplateDescriptionException: Type[BotocoreClientError]
    InvalidApprovalRuleTemplateNameException: Type[BotocoreClientError]
    InvalidApprovalStateException: Type[BotocoreClientError]
    InvalidAuthorArnException: Type[BotocoreClientError]
    InvalidBlobIdException: Type[BotocoreClientError]
    InvalidBranchNameException: Type[BotocoreClientError]
    InvalidClientRequestTokenException: Type[BotocoreClientError]
    InvalidCommentIdException: Type[BotocoreClientError]
    InvalidCommitException: Type[BotocoreClientError]
    InvalidCommitIdException: Type[BotocoreClientError]
    InvalidConflictDetailLevelException: Type[BotocoreClientError]
    InvalidConflictResolutionException: Type[BotocoreClientError]
    InvalidConflictResolutionStrategyException: Type[BotocoreClientError]
    InvalidContinuationTokenException: Type[BotocoreClientError]
    InvalidDeletionParameterException: Type[BotocoreClientError]
    InvalidDescriptionException: Type[BotocoreClientError]
    InvalidDestinationCommitSpecifierException: Type[BotocoreClientError]
    InvalidEmailException: Type[BotocoreClientError]
    InvalidFileLocationException: Type[BotocoreClientError]
    InvalidFileModeException: Type[BotocoreClientError]
    InvalidFilePositionException: Type[BotocoreClientError]
    InvalidMaxConflictFilesException: Type[BotocoreClientError]
    InvalidMaxMergeHunksException: Type[BotocoreClientError]
    InvalidMaxResultsException: Type[BotocoreClientError]
    InvalidMergeOptionException: Type[BotocoreClientError]
    InvalidOrderException: Type[BotocoreClientError]
    InvalidOverrideStatusException: Type[BotocoreClientError]
    InvalidParentCommitIdException: Type[BotocoreClientError]
    InvalidPathException: Type[BotocoreClientError]
    InvalidPullRequestEventTypeException: Type[BotocoreClientError]
    InvalidPullRequestIdException: Type[BotocoreClientError]
    InvalidPullRequestStatusException: Type[BotocoreClientError]
    InvalidPullRequestStatusUpdateException: Type[BotocoreClientError]
    InvalidReactionUserArnException: Type[BotocoreClientError]
    InvalidReactionValueException: Type[BotocoreClientError]
    InvalidReferenceNameException: Type[BotocoreClientError]
    InvalidRelativeFileVersionEnumException: Type[BotocoreClientError]
    InvalidReplacementContentException: Type[BotocoreClientError]
    InvalidReplacementTypeException: Type[BotocoreClientError]
    InvalidRepositoryDescriptionException: Type[BotocoreClientError]
    InvalidRepositoryNameException: Type[BotocoreClientError]
    InvalidRepositoryTriggerBranchNameException: Type[BotocoreClientError]
    InvalidRepositoryTriggerCustomDataException: Type[BotocoreClientError]
    InvalidRepositoryTriggerDestinationArnException: Type[BotocoreClientError]
    InvalidRepositoryTriggerEventsException: Type[BotocoreClientError]
    InvalidRepositoryTriggerNameException: Type[BotocoreClientError]
    InvalidRepositoryTriggerRegionException: Type[BotocoreClientError]
    InvalidResourceArnException: Type[BotocoreClientError]
    InvalidRevisionIdException: Type[BotocoreClientError]
    InvalidRuleContentSha256Exception: Type[BotocoreClientError]
    InvalidSortByException: Type[BotocoreClientError]
    InvalidSourceCommitSpecifierException: Type[BotocoreClientError]
    InvalidSystemTagUsageException: Type[BotocoreClientError]
    InvalidTagKeysListException: Type[BotocoreClientError]
    InvalidTagsMapException: Type[BotocoreClientError]
    InvalidTargetBranchException: Type[BotocoreClientError]
    InvalidTargetException: Type[BotocoreClientError]
    InvalidTargetsException: Type[BotocoreClientError]
    InvalidTitleException: Type[BotocoreClientError]
    ManualMergeRequiredException: Type[BotocoreClientError]
    MaximumBranchesExceededException: Type[BotocoreClientError]
    MaximumConflictResolutionEntriesExceededException: Type[BotocoreClientError]
    MaximumFileContentToLoadExceededException: Type[BotocoreClientError]
    MaximumFileEntriesExceededException: Type[BotocoreClientError]
    MaximumItemsToCompareExceededException: Type[BotocoreClientError]
    MaximumNumberOfApprovalsExceededException: Type[BotocoreClientError]
    MaximumOpenPullRequestsExceededException: Type[BotocoreClientError]
    MaximumRepositoryNamesExceededException: Type[BotocoreClientError]
    MaximumRepositoryTriggersExceededException: Type[BotocoreClientError]
    MaximumRuleTemplatesAssociatedWithRepositoryException: Type[BotocoreClientError]
    MergeOptionRequiredException: Type[BotocoreClientError]
    MultipleConflictResolutionEntriesException: Type[BotocoreClientError]
    MultipleRepositoriesInPullRequestException: Type[BotocoreClientError]
    NameLengthExceededException: Type[BotocoreClientError]
    NoChangeException: Type[BotocoreClientError]
    NumberOfRuleTemplatesExceededException: Type[BotocoreClientError]
    NumberOfRulesExceededException: Type[BotocoreClientError]
    OperationNotAllowedException: Type[BotocoreClientError]
    OverrideAlreadySetException: Type[BotocoreClientError]
    OverrideStatusRequiredException: Type[BotocoreClientError]
    ParentCommitDoesNotExistException: Type[BotocoreClientError]
    ParentCommitIdOutdatedException: Type[BotocoreClientError]
    ParentCommitIdRequiredException: Type[BotocoreClientError]
    PathDoesNotExistException: Type[BotocoreClientError]
    PathRequiredException: Type[BotocoreClientError]
    PullRequestAlreadyClosedException: Type[BotocoreClientError]
    PullRequestApprovalRulesNotSatisfiedException: Type[BotocoreClientError]
    PullRequestCannotBeApprovedByAuthorException: Type[BotocoreClientError]
    PullRequestDoesNotExistException: Type[BotocoreClientError]
    PullRequestIdRequiredException: Type[BotocoreClientError]
    PullRequestStatusRequiredException: Type[BotocoreClientError]
    PutFileEntryConflictException: Type[BotocoreClientError]
    ReactionLimitExceededException: Type[BotocoreClientError]
    ReactionValueRequiredException: Type[BotocoreClientError]
    ReferenceDoesNotExistException: Type[BotocoreClientError]
    ReferenceNameRequiredException: Type[BotocoreClientError]
    ReferenceTypeNotSupportedException: Type[BotocoreClientError]
    ReplacementContentRequiredException: Type[BotocoreClientError]
    ReplacementTypeRequiredException: Type[BotocoreClientError]
    RepositoryDoesNotExistException: Type[BotocoreClientError]
    RepositoryLimitExceededException: Type[BotocoreClientError]
    RepositoryNameExistsException: Type[BotocoreClientError]
    RepositoryNameRequiredException: Type[BotocoreClientError]
    RepositoryNamesRequiredException: Type[BotocoreClientError]
    RepositoryNotAssociatedWithPullRequestException: Type[BotocoreClientError]
    RepositoryTriggerBranchNameListRequiredException: Type[BotocoreClientError]
    RepositoryTriggerDestinationArnRequiredException: Type[BotocoreClientError]
    RepositoryTriggerEventsListRequiredException: Type[BotocoreClientError]
    RepositoryTriggerNameRequiredException: Type[BotocoreClientError]
    RepositoryTriggersListRequiredException: Type[BotocoreClientError]
    ResourceArnRequiredException: Type[BotocoreClientError]
    RestrictedSourceFileException: Type[BotocoreClientError]
    RevisionIdRequiredException: Type[BotocoreClientError]
    RevisionNotCurrentException: Type[BotocoreClientError]
    SameFileContentException: Type[BotocoreClientError]
    SamePathRequestException: Type[BotocoreClientError]
    SourceAndDestinationAreSameException: Type[BotocoreClientError]
    SourceFileOrContentRequiredException: Type[BotocoreClientError]
    TagKeysListRequiredException: Type[BotocoreClientError]
    TagPolicyException: Type[BotocoreClientError]
    TagsMapRequiredException: Type[BotocoreClientError]
    TargetRequiredException: Type[BotocoreClientError]
    TargetsRequiredException: Type[BotocoreClientError]
    TipOfSourceReferenceIsDifferentException: Type[BotocoreClientError]
    TipsDivergenceExceededException: Type[BotocoreClientError]
    TitleRequiredException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]


class CodeCommitClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CodeCommitClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#exceptions)
        """

    async def associate_approval_rule_template_with_repository(
        self, *, approvalRuleTemplateName: str, repositoryName: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates an association between an approval rule template and a specified
        repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.associate_approval_rule_template_with_repository)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#associate_approval_rule_template_with_repository)
        """

    async def batch_associate_approval_rule_template_with_repositories(
        self, *, approvalRuleTemplateName: str, repositoryNames: Sequence[str]
    ) -> BatchAssociateApprovalRuleTemplateWithRepositoriesOutputTypeDef:
        """
        Creates an association between an approval rule template and one or more
        specified
        repositories.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.batch_associate_approval_rule_template_with_repositories)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#batch_associate_approval_rule_template_with_repositories)
        """

    async def batch_describe_merge_conflicts(
        self,
        *,
        repositoryName: str,
        destinationCommitSpecifier: str,
        sourceCommitSpecifier: str,
        mergeOption: MergeOptionTypeEnumType,
        maxMergeHunks: int = ...,
        maxConflictFiles: int = ...,
        filePaths: Sequence[str] = ...,
        conflictDetailLevel: ConflictDetailLevelTypeEnumType = ...,
        conflictResolutionStrategy: ConflictResolutionStrategyTypeEnumType = ...,
        nextToken: str = ...,
    ) -> BatchDescribeMergeConflictsOutputTypeDef:
        """
        Returns information about one or more merge conflicts in the attempted merge of
        two commit specifiers using the squash or three-way merge
        strategy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.batch_describe_merge_conflicts)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#batch_describe_merge_conflicts)
        """

    async def batch_disassociate_approval_rule_template_from_repositories(
        self, *, approvalRuleTemplateName: str, repositoryNames: Sequence[str]
    ) -> BatchDisassociateApprovalRuleTemplateFromRepositoriesOutputTypeDef:
        """
        Removes the association between an approval rule template and one or more
        specified
        repositories.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.batch_disassociate_approval_rule_template_from_repositories)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#batch_disassociate_approval_rule_template_from_repositories)
        """

    async def batch_get_commits(
        self, *, commitIds: Sequence[str], repositoryName: str
    ) -> BatchGetCommitsOutputTypeDef:
        """
        Returns information about the contents of one or more commits in a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.batch_get_commits)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#batch_get_commits)
        """

    async def batch_get_repositories(
        self, *, repositoryNames: Sequence[str]
    ) -> BatchGetRepositoriesOutputTypeDef:
        """
        Returns information about one or more repositories.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.batch_get_repositories)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#batch_get_repositories)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#close)
        """

    async def create_approval_rule_template(
        self,
        *,
        approvalRuleTemplateName: str,
        approvalRuleTemplateContent: str,
        approvalRuleTemplateDescription: str = ...,
    ) -> CreateApprovalRuleTemplateOutputTypeDef:
        """
        Creates a template for approval rules that can then be associated with one or
        more repositories in your Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.create_approval_rule_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#create_approval_rule_template)
        """

    async def create_branch(
        self, *, repositoryName: str, branchName: str, commitId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates a branch in a repository and points the branch to a commit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.create_branch)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#create_branch)
        """

    async def create_commit(
        self,
        *,
        repositoryName: str,
        branchName: str,
        parentCommitId: str = ...,
        authorName: str = ...,
        email: str = ...,
        commitMessage: str = ...,
        keepEmptyFolders: bool = ...,
        putFiles: Sequence[PutFileEntryTypeDef] = ...,
        deleteFiles: Sequence[DeleteFileEntryTypeDef] = ...,
        setFileModes: Sequence[SetFileModeEntryTypeDef] = ...,
    ) -> CreateCommitOutputTypeDef:
        """
        Creates a commit for a repository on the tip of a specified branch.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.create_commit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#create_commit)
        """

    async def create_pull_request(
        self,
        *,
        title: str,
        targets: Sequence[TargetTypeDef],
        description: str = ...,
        clientRequestToken: str = ...,
    ) -> CreatePullRequestOutputTypeDef:
        """
        Creates a pull request in the specified repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.create_pull_request)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#create_pull_request)
        """

    async def create_pull_request_approval_rule(
        self, *, pullRequestId: str, approvalRuleName: str, approvalRuleContent: str
    ) -> CreatePullRequestApprovalRuleOutputTypeDef:
        """
        Creates an approval rule for a pull request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.create_pull_request_approval_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#create_pull_request_approval_rule)
        """

    async def create_repository(
        self,
        *,
        repositoryName: str,
        repositoryDescription: str = ...,
        tags: Mapping[str, str] = ...,
        kmsKeyId: str = ...,
    ) -> CreateRepositoryOutputTypeDef:
        """
        Creates a new, empty repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.create_repository)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#create_repository)
        """

    async def create_unreferenced_merge_commit(
        self,
        *,
        repositoryName: str,
        sourceCommitSpecifier: str,
        destinationCommitSpecifier: str,
        mergeOption: MergeOptionTypeEnumType,
        conflictDetailLevel: ConflictDetailLevelTypeEnumType = ...,
        conflictResolutionStrategy: ConflictResolutionStrategyTypeEnumType = ...,
        authorName: str = ...,
        email: str = ...,
        commitMessage: str = ...,
        keepEmptyFolders: bool = ...,
        conflictResolution: ConflictResolutionTypeDef = ...,
    ) -> CreateUnreferencedMergeCommitOutputTypeDef:
        """
        Creates an unreferenced commit that represents the result of merging two
        branches using a specified merge
        strategy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.create_unreferenced_merge_commit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#create_unreferenced_merge_commit)
        """

    async def delete_approval_rule_template(
        self, *, approvalRuleTemplateName: str
    ) -> DeleteApprovalRuleTemplateOutputTypeDef:
        """
        Deletes a specified approval rule template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.delete_approval_rule_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#delete_approval_rule_template)
        """

    async def delete_branch(
        self, *, repositoryName: str, branchName: str
    ) -> DeleteBranchOutputTypeDef:
        """
        Deletes a branch from a repository, unless that branch is the default branch
        for the
        repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.delete_branch)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#delete_branch)
        """

    async def delete_comment_content(self, *, commentId: str) -> DeleteCommentContentOutputTypeDef:
        """
        Deletes the content of a comment made on a change, file, or commit in a
        repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.delete_comment_content)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#delete_comment_content)
        """

    async def delete_file(
        self,
        *,
        repositoryName: str,
        branchName: str,
        filePath: str,
        parentCommitId: str,
        keepEmptyFolders: bool = ...,
        commitMessage: str = ...,
        name: str = ...,
        email: str = ...,
    ) -> DeleteFileOutputTypeDef:
        """
        Deletes a specified file from a specified branch.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.delete_file)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#delete_file)
        """

    async def delete_pull_request_approval_rule(
        self, *, pullRequestId: str, approvalRuleName: str
    ) -> DeletePullRequestApprovalRuleOutputTypeDef:
        """
        Deletes an approval rule from a specified pull request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.delete_pull_request_approval_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#delete_pull_request_approval_rule)
        """

    async def delete_repository(self, *, repositoryName: str) -> DeleteRepositoryOutputTypeDef:
        """
        Deletes a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.delete_repository)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#delete_repository)
        """

    async def describe_merge_conflicts(
        self,
        *,
        repositoryName: str,
        destinationCommitSpecifier: str,
        sourceCommitSpecifier: str,
        mergeOption: MergeOptionTypeEnumType,
        filePath: str,
        maxMergeHunks: int = ...,
        conflictDetailLevel: ConflictDetailLevelTypeEnumType = ...,
        conflictResolutionStrategy: ConflictResolutionStrategyTypeEnumType = ...,
        nextToken: str = ...,
    ) -> DescribeMergeConflictsOutputTypeDef:
        """
        Returns information about one or more merge conflicts in the attempted merge of
        two commit specifiers using the squash or three-way merge
        strategy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.describe_merge_conflicts)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#describe_merge_conflicts)
        """

    async def describe_pull_request_events(
        self,
        *,
        pullRequestId: str,
        pullRequestEventType: PullRequestEventTypeType = ...,
        actorArn: str = ...,
        nextToken: str = ...,
        maxResults: int = ...,
    ) -> DescribePullRequestEventsOutputTypeDef:
        """
        Returns information about one or more pull request events.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.describe_pull_request_events)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#describe_pull_request_events)
        """

    async def disassociate_approval_rule_template_from_repository(
        self, *, approvalRuleTemplateName: str, repositoryName: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the association between a template and a repository so that approval
        rules based on the template are not automatically created when pull requests
        are created in the specified
        repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.disassociate_approval_rule_template_from_repository)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#disassociate_approval_rule_template_from_repository)
        """

    async def evaluate_pull_request_approval_rules(
        self, *, pullRequestId: str, revisionId: str
    ) -> EvaluatePullRequestApprovalRulesOutputTypeDef:
        """
        Evaluates whether a pull request has met all the conditions specified in its
        associated approval
        rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.evaluate_pull_request_approval_rules)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#evaluate_pull_request_approval_rules)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#generate_presigned_url)
        """

    async def get_approval_rule_template(
        self, *, approvalRuleTemplateName: str
    ) -> GetApprovalRuleTemplateOutputTypeDef:
        """
        Returns information about a specified approval rule template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.get_approval_rule_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#get_approval_rule_template)
        """

    async def get_blob(self, *, repositoryName: str, blobId: str) -> GetBlobOutputTypeDef:
        """
        Returns the base-64 encoded content of an individual blob in a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.get_blob)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#get_blob)
        """

    async def get_branch(
        self, *, repositoryName: str = ..., branchName: str = ...
    ) -> GetBranchOutputTypeDef:
        """
        Returns information about a repository branch, including its name and the last
        commit
        ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.get_branch)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#get_branch)
        """

    async def get_comment(self, *, commentId: str) -> GetCommentOutputTypeDef:
        """
        Returns the content of a comment made on a change, file, or commit in a
        repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.get_comment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#get_comment)
        """

    async def get_comment_reactions(
        self,
        *,
        commentId: str,
        reactionUserArn: str = ...,
        nextToken: str = ...,
        maxResults: int = ...,
    ) -> GetCommentReactionsOutputTypeDef:
        """
        Returns information about reactions to a specified comment ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.get_comment_reactions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#get_comment_reactions)
        """

    async def get_comments_for_compared_commit(
        self,
        *,
        repositoryName: str,
        afterCommitId: str,
        beforeCommitId: str = ...,
        nextToken: str = ...,
        maxResults: int = ...,
    ) -> GetCommentsForComparedCommitOutputTypeDef:
        """
        Returns information about comments made on the comparison between two commits.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.get_comments_for_compared_commit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#get_comments_for_compared_commit)
        """

    async def get_comments_for_pull_request(
        self,
        *,
        pullRequestId: str,
        repositoryName: str = ...,
        beforeCommitId: str = ...,
        afterCommitId: str = ...,
        nextToken: str = ...,
        maxResults: int = ...,
    ) -> GetCommentsForPullRequestOutputTypeDef:
        """
        Returns comments made on a pull request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.get_comments_for_pull_request)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#get_comments_for_pull_request)
        """

    async def get_commit(self, *, repositoryName: str, commitId: str) -> GetCommitOutputTypeDef:
        """
        Returns information about a commit, including commit message and committer
        information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.get_commit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#get_commit)
        """

    async def get_differences(
        self,
        *,
        repositoryName: str,
        afterCommitSpecifier: str,
        beforeCommitSpecifier: str = ...,
        beforePath: str = ...,
        afterPath: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> GetDifferencesOutputTypeDef:
        """
        Returns information about the differences in a valid commit specifier (such as
        a branch, tag, HEAD, commit ID, or other fully qualified
        reference).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.get_differences)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#get_differences)
        """

    async def get_file(
        self, *, repositoryName: str, filePath: str, commitSpecifier: str = ...
    ) -> GetFileOutputTypeDef:
        """
        Returns the base-64 encoded contents of a specified file and its metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.get_file)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#get_file)
        """

    async def get_folder(
        self, *, repositoryName: str, folderPath: str, commitSpecifier: str = ...
    ) -> GetFolderOutputTypeDef:
        """
        Returns the contents of a specified folder in a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.get_folder)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#get_folder)
        """

    async def get_merge_commit(
        self,
        *,
        repositoryName: str,
        sourceCommitSpecifier: str,
        destinationCommitSpecifier: str,
        conflictDetailLevel: ConflictDetailLevelTypeEnumType = ...,
        conflictResolutionStrategy: ConflictResolutionStrategyTypeEnumType = ...,
    ) -> GetMergeCommitOutputTypeDef:
        """
        Returns information about a specified merge commit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.get_merge_commit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#get_merge_commit)
        """

    async def get_merge_conflicts(
        self,
        *,
        repositoryName: str,
        destinationCommitSpecifier: str,
        sourceCommitSpecifier: str,
        mergeOption: MergeOptionTypeEnumType,
        conflictDetailLevel: ConflictDetailLevelTypeEnumType = ...,
        maxConflictFiles: int = ...,
        conflictResolutionStrategy: ConflictResolutionStrategyTypeEnumType = ...,
        nextToken: str = ...,
    ) -> GetMergeConflictsOutputTypeDef:
        """
        Returns information about merge conflicts between the before and after commit
        IDs for a pull request in a
        repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.get_merge_conflicts)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#get_merge_conflicts)
        """

    async def get_merge_options(
        self,
        *,
        repositoryName: str,
        sourceCommitSpecifier: str,
        destinationCommitSpecifier: str,
        conflictDetailLevel: ConflictDetailLevelTypeEnumType = ...,
        conflictResolutionStrategy: ConflictResolutionStrategyTypeEnumType = ...,
    ) -> GetMergeOptionsOutputTypeDef:
        """
        Returns information about the merge options available for merging two specified
        branches.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.get_merge_options)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#get_merge_options)
        """

    async def get_pull_request(self, *, pullRequestId: str) -> GetPullRequestOutputTypeDef:
        """
        Gets information about a pull request in a specified repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.get_pull_request)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#get_pull_request)
        """

    async def get_pull_request_approval_states(
        self, *, pullRequestId: str, revisionId: str
    ) -> GetPullRequestApprovalStatesOutputTypeDef:
        """
        Gets information about the approval states for a specified pull request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.get_pull_request_approval_states)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#get_pull_request_approval_states)
        """

    async def get_pull_request_override_state(
        self, *, pullRequestId: str, revisionId: str
    ) -> GetPullRequestOverrideStateOutputTypeDef:
        """
        Returns information about whether approval rules have been set aside
        (overridden) for a pull request, and if so, the Amazon Resource Name (ARN) of
        the user or identity that overrode the rules and their requirements for the
        pull
        request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.get_pull_request_override_state)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#get_pull_request_override_state)
        """

    async def get_repository(self, *, repositoryName: str) -> GetRepositoryOutputTypeDef:
        """
        Returns information about a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.get_repository)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#get_repository)
        """

    async def get_repository_triggers(
        self, *, repositoryName: str
    ) -> GetRepositoryTriggersOutputTypeDef:
        """
        Gets information about triggers configured for a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.get_repository_triggers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#get_repository_triggers)
        """

    async def list_approval_rule_templates(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListApprovalRuleTemplatesOutputTypeDef:
        """
        Lists all approval rule templates in the specified Amazon Web Services Region
        in your Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.list_approval_rule_templates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#list_approval_rule_templates)
        """

    async def list_associated_approval_rule_templates_for_repository(
        self, *, repositoryName: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListAssociatedApprovalRuleTemplatesForRepositoryOutputTypeDef:
        """
        Lists all approval rule templates that are associated with a specified
        repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.list_associated_approval_rule_templates_for_repository)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#list_associated_approval_rule_templates_for_repository)
        """

    async def list_branches(
        self, *, repositoryName: str, nextToken: str = ...
    ) -> ListBranchesOutputTypeDef:
        """
        Gets information about one or more branches in a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.list_branches)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#list_branches)
        """

    async def list_file_commit_history(
        self,
        *,
        repositoryName: str,
        filePath: str,
        commitSpecifier: str = ...,
        maxResults: int = ...,
        nextToken: str = ...,
    ) -> ListFileCommitHistoryResponseTypeDef:
        """
        Retrieves a list of commits and changes to a specified file.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.list_file_commit_history)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#list_file_commit_history)
        """

    async def list_pull_requests(
        self,
        *,
        repositoryName: str,
        authorArn: str = ...,
        pullRequestStatus: PullRequestStatusEnumType = ...,
        nextToken: str = ...,
        maxResults: int = ...,
    ) -> ListPullRequestsOutputTypeDef:
        """
        Returns a list of pull requests for a specified repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.list_pull_requests)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#list_pull_requests)
        """

    async def list_repositories(
        self, *, nextToken: str = ..., sortBy: SortByEnumType = ..., order: OrderEnumType = ...
    ) -> ListRepositoriesOutputTypeDef:
        """
        Gets information about one or more repositories.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.list_repositories)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#list_repositories)
        """

    async def list_repositories_for_approval_rule_template(
        self, *, approvalRuleTemplateName: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListRepositoriesForApprovalRuleTemplateOutputTypeDef:
        """
        Lists all repositories associated with the specified approval rule template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.list_repositories_for_approval_rule_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#list_repositories_for_approval_rule_template)
        """

    async def list_tags_for_resource(
        self, *, resourceArn: str, nextToken: str = ...
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Gets information about Amazon Web Servicestags for a specified Amazon Resource
        Name (ARN) in
        CodeCommit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#list_tags_for_resource)
        """

    async def merge_branches_by_fast_forward(
        self,
        *,
        repositoryName: str,
        sourceCommitSpecifier: str,
        destinationCommitSpecifier: str,
        targetBranch: str = ...,
    ) -> MergeBranchesByFastForwardOutputTypeDef:
        """
        Merges two branches using the fast-forward merge strategy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.merge_branches_by_fast_forward)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#merge_branches_by_fast_forward)
        """

    async def merge_branches_by_squash(
        self,
        *,
        repositoryName: str,
        sourceCommitSpecifier: str,
        destinationCommitSpecifier: str,
        targetBranch: str = ...,
        conflictDetailLevel: ConflictDetailLevelTypeEnumType = ...,
        conflictResolutionStrategy: ConflictResolutionStrategyTypeEnumType = ...,
        authorName: str = ...,
        email: str = ...,
        commitMessage: str = ...,
        keepEmptyFolders: bool = ...,
        conflictResolution: ConflictResolutionTypeDef = ...,
    ) -> MergeBranchesBySquashOutputTypeDef:
        """
        Merges two branches using the squash merge strategy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.merge_branches_by_squash)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#merge_branches_by_squash)
        """

    async def merge_branches_by_three_way(
        self,
        *,
        repositoryName: str,
        sourceCommitSpecifier: str,
        destinationCommitSpecifier: str,
        targetBranch: str = ...,
        conflictDetailLevel: ConflictDetailLevelTypeEnumType = ...,
        conflictResolutionStrategy: ConflictResolutionStrategyTypeEnumType = ...,
        authorName: str = ...,
        email: str = ...,
        commitMessage: str = ...,
        keepEmptyFolders: bool = ...,
        conflictResolution: ConflictResolutionTypeDef = ...,
    ) -> MergeBranchesByThreeWayOutputTypeDef:
        """
        Merges two specified branches using the three-way merge strategy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.merge_branches_by_three_way)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#merge_branches_by_three_way)
        """

    async def merge_pull_request_by_fast_forward(
        self, *, pullRequestId: str, repositoryName: str, sourceCommitId: str = ...
    ) -> MergePullRequestByFastForwardOutputTypeDef:
        """
        Attempts to merge the source commit of a pull request into the specified
        destination branch for that pull request at the specified commit using the
        fast-forward merge
        strategy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.merge_pull_request_by_fast_forward)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#merge_pull_request_by_fast_forward)
        """

    async def merge_pull_request_by_squash(
        self,
        *,
        pullRequestId: str,
        repositoryName: str,
        sourceCommitId: str = ...,
        conflictDetailLevel: ConflictDetailLevelTypeEnumType = ...,
        conflictResolutionStrategy: ConflictResolutionStrategyTypeEnumType = ...,
        commitMessage: str = ...,
        authorName: str = ...,
        email: str = ...,
        keepEmptyFolders: bool = ...,
        conflictResolution: ConflictResolutionTypeDef = ...,
    ) -> MergePullRequestBySquashOutputTypeDef:
        """
        Attempts to merge the source commit of a pull request into the specified
        destination branch for that pull request at the specified commit using the
        squash merge
        strategy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.merge_pull_request_by_squash)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#merge_pull_request_by_squash)
        """

    async def merge_pull_request_by_three_way(
        self,
        *,
        pullRequestId: str,
        repositoryName: str,
        sourceCommitId: str = ...,
        conflictDetailLevel: ConflictDetailLevelTypeEnumType = ...,
        conflictResolutionStrategy: ConflictResolutionStrategyTypeEnumType = ...,
        commitMessage: str = ...,
        authorName: str = ...,
        email: str = ...,
        keepEmptyFolders: bool = ...,
        conflictResolution: ConflictResolutionTypeDef = ...,
    ) -> MergePullRequestByThreeWayOutputTypeDef:
        """
        Attempts to merge the source commit of a pull request into the specified
        destination branch for that pull request at the specified commit using the
        three-way merge
        strategy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.merge_pull_request_by_three_way)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#merge_pull_request_by_three_way)
        """

    async def override_pull_request_approval_rules(
        self, *, pullRequestId: str, revisionId: str, overrideStatus: OverrideStatusType
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets aside (overrides) all approval rule requirements for a specified pull
        request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.override_pull_request_approval_rules)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#override_pull_request_approval_rules)
        """

    async def post_comment_for_compared_commit(
        self,
        *,
        repositoryName: str,
        afterCommitId: str,
        content: str,
        beforeCommitId: str = ...,
        location: LocationTypeDef = ...,
        clientRequestToken: str = ...,
    ) -> PostCommentForComparedCommitOutputTypeDef:
        """
        Posts a comment on the comparison between two commits.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.post_comment_for_compared_commit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#post_comment_for_compared_commit)
        """

    async def post_comment_for_pull_request(
        self,
        *,
        pullRequestId: str,
        repositoryName: str,
        beforeCommitId: str,
        afterCommitId: str,
        content: str,
        location: LocationTypeDef = ...,
        clientRequestToken: str = ...,
    ) -> PostCommentForPullRequestOutputTypeDef:
        """
        Posts a comment on a pull request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.post_comment_for_pull_request)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#post_comment_for_pull_request)
        """

    async def post_comment_reply(
        self, *, inReplyTo: str, content: str, clientRequestToken: str = ...
    ) -> PostCommentReplyOutputTypeDef:
        """
        Posts a comment in reply to an existing comment on a comparison between commits
        or a pull
        request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.post_comment_reply)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#post_comment_reply)
        """

    async def put_comment_reaction(
        self, *, commentId: str, reactionValue: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds or updates a reaction to a specified comment for the user whose identity
        is used to make the
        request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.put_comment_reaction)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#put_comment_reaction)
        """

    async def put_file(
        self,
        *,
        repositoryName: str,
        branchName: str,
        fileContent: BlobTypeDef,
        filePath: str,
        fileMode: FileModeTypeEnumType = ...,
        parentCommitId: str = ...,
        commitMessage: str = ...,
        name: str = ...,
        email: str = ...,
    ) -> PutFileOutputTypeDef:
        """
        Adds or updates a file in a branch in an CodeCommit repository, and generates a
        commit for the addition in the specified
        branch.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.put_file)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#put_file)
        """

    async def put_repository_triggers(
        self, *, repositoryName: str, triggers: Sequence[RepositoryTriggerUnionTypeDef]
    ) -> PutRepositoryTriggersOutputTypeDef:
        """
        Replaces all triggers for a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.put_repository_triggers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#put_repository_triggers)
        """

    async def tag_resource(
        self, *, resourceArn: str, tags: Mapping[str, str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds or updates tags for a resource in CodeCommit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#tag_resource)
        """

    async def test_repository_triggers(
        self, *, repositoryName: str, triggers: Sequence[RepositoryTriggerUnionTypeDef]
    ) -> TestRepositoryTriggersOutputTypeDef:
        """
        Tests the functionality of repository triggers by sending information to the
        trigger
        target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.test_repository_triggers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#test_repository_triggers)
        """

    async def untag_resource(
        self, *, resourceArn: str, tagKeys: Sequence[str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes tags for a resource in CodeCommit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#untag_resource)
        """

    async def update_approval_rule_template_content(
        self,
        *,
        approvalRuleTemplateName: str,
        newRuleContent: str,
        existingRuleContentSha256: str = ...,
    ) -> UpdateApprovalRuleTemplateContentOutputTypeDef:
        """
        Updates the content of an approval rule template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.update_approval_rule_template_content)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#update_approval_rule_template_content)
        """

    async def update_approval_rule_template_description(
        self, *, approvalRuleTemplateName: str, approvalRuleTemplateDescription: str
    ) -> UpdateApprovalRuleTemplateDescriptionOutputTypeDef:
        """
        Updates the description for a specified approval rule template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.update_approval_rule_template_description)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#update_approval_rule_template_description)
        """

    async def update_approval_rule_template_name(
        self, *, oldApprovalRuleTemplateName: str, newApprovalRuleTemplateName: str
    ) -> UpdateApprovalRuleTemplateNameOutputTypeDef:
        """
        Updates the name of a specified approval rule template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.update_approval_rule_template_name)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#update_approval_rule_template_name)
        """

    async def update_comment(self, *, commentId: str, content: str) -> UpdateCommentOutputTypeDef:
        """
        Replaces the contents of a comment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.update_comment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#update_comment)
        """

    async def update_default_branch(
        self, *, repositoryName: str, defaultBranchName: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets or changes the default branch name for the specified repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.update_default_branch)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#update_default_branch)
        """

    async def update_pull_request_approval_rule_content(
        self,
        *,
        pullRequestId: str,
        approvalRuleName: str,
        newRuleContent: str,
        existingRuleContentSha256: str = ...,
    ) -> UpdatePullRequestApprovalRuleContentOutputTypeDef:
        """
        Updates the structure of an approval rule created specifically for a pull
        request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.update_pull_request_approval_rule_content)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#update_pull_request_approval_rule_content)
        """

    async def update_pull_request_approval_state(
        self, *, pullRequestId: str, revisionId: str, approvalState: ApprovalStateType
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the state of a user's approval on a pull request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.update_pull_request_approval_state)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#update_pull_request_approval_state)
        """

    async def update_pull_request_description(
        self, *, pullRequestId: str, description: str
    ) -> UpdatePullRequestDescriptionOutputTypeDef:
        """
        Replaces the contents of the description of a pull request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.update_pull_request_description)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#update_pull_request_description)
        """

    async def update_pull_request_status(
        self, *, pullRequestId: str, pullRequestStatus: PullRequestStatusEnumType
    ) -> UpdatePullRequestStatusOutputTypeDef:
        """
        Updates the status of a pull request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.update_pull_request_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#update_pull_request_status)
        """

    async def update_pull_request_title(
        self, *, pullRequestId: str, title: str
    ) -> UpdatePullRequestTitleOutputTypeDef:
        """
        Replaces the title of a pull request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.update_pull_request_title)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#update_pull_request_title)
        """

    async def update_repository_description(
        self, *, repositoryName: str, repositoryDescription: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets or changes the comment or description for a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.update_repository_description)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#update_repository_description)
        """

    async def update_repository_encryption_key(
        self, *, repositoryName: str, kmsKeyId: str
    ) -> UpdateRepositoryEncryptionKeyOutputTypeDef:
        """
        Updates the Key Management Service encryption key used to encrypt and decrypt a
        CodeCommit
        repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.update_repository_encryption_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#update_repository_encryption_key)
        """

    async def update_repository_name(
        self, *, oldName: str, newName: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Renames a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.update_repository_name)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#update_repository_name)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_pull_request_events"]
    ) -> DescribePullRequestEventsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_comments_for_compared_commit"]
    ) -> GetCommentsForComparedCommitPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_comments_for_pull_request"]
    ) -> GetCommentsForPullRequestPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_differences"]) -> GetDifferencesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_branches"]) -> ListBranchesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_pull_requests"]
    ) -> ListPullRequestsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_repositories"]
    ) -> ListRepositoriesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/#get_paginator)
        """

    async def __aenter__(self) -> "CodeCommitClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit.html#CodeCommit.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/client/)
        """
