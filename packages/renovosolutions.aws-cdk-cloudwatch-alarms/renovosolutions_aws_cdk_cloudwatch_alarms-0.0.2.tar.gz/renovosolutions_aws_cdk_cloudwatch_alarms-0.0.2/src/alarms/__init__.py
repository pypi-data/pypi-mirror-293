r'''
# cdk-library-cloudwatch-alarms

WIP - Library to provide constructs, aspects, and construct extensions to more easily set up alarms for AWS resources in CDK code based on AWS recommended alarms list. This project is still in early development so YMMV.

## Usage

This library is flexible in its approach and there are multiple paths to configuring alarms depending on how you'd like to work with the recommended alarms.

## Feature Availability

Intended feature list as of Aug 2024

* [x] Aspects to apply recommended alarms to a wide scope such as a whole CDK app

  * [x] Ability to exclude specific alarms
  * [x] Ability to define a default set of alarm actions
  * [x] Ability to modify the configuration of each alarm type
  * [ ] Ability to exclude specific resources
* [x] Constructs to ease alarm configuration for individual resources at a granular scope

  * [x] Constructs for each available alarm according to the coverage table
  * [x] Constructs for applying all recommended alarms to a specific resource
  * [x] Ability to exclude specific alarms from the all recommended alarms construct
* [x] Extended versions of resource constructs with alarm helper methods

## Resource Coverage

If its not shown it hasn't been worked on.

| Service   | Status | Notes |
| --- | --- | --- |
| S3  | <ul><li>[x] 4xxErrors</li><li>[x] 5xxErrors</li><li>[ ] OperationsFailedReplication</li></ul> | Replication errors are difficult to set up in CDK at the moment due to rule properties being IResolvables and replication rules not being available on the L2 Bucket construct |
| SQS | <ul><li>[x] ApproximateAgeOfOldestMessage</li><li>[x] ApproximateNumberOfMessagesNotVisible</li><li>[x] ApproximateNumberOfMessagesVisible</li><li>[x] NumberOfMessagesSent | All alarms with the exception of number of messages sent require a user defined threshold because its very usecase specific |
| SNS | <ul><li>[x] NumberOfMessagesPublished</li><li>[x] NumberOfNotificationsDelivered</li><li>[x] NumberOfNotificationsFailed</li><li>[x] NumberOfNotificationsFilteredOut-InvalidAttributes</li><li>[x] NumberOfNotificationsFilteredOut-InvalidMessageBody</li><li>[x] NumberOfNotificationsRedrivenToDlq</li><li>[x] NumberOfNotificationsFailedToRedriveToDlq</li><li>[ ] SMSMonthToDateSpentUSD</li><li>[ ] SMSSuccessRate</li></ul> | Some alarms require a threshold to be defined. SMS alarms are not implememented.
| Lambda | <ul><li>[ ] ClaimedAccountConcurrency</li><li>[x] Errors</li><li>[x] Throttles</li><li>[x] Duration</li><li>[x] ConcurrentExecutions</li></ul> | ClaimedAccountConcurrency is account wide and one time so not covered by this library at this time |

### Aspects

Below is an example of configuring the Lambda aspect. You must configure non-defaults for alarms which is most cases is only a `threshold`. Since the aspect is applied at the `app` level it applies to both the `TestStack` and `TestStack2` lambda functions and will create all available recommended alarms for those functions. See references for additional details on Aspects which can be applied to the app, stack, or individual constructs depending on your use case.

```python
import { App, Stack, Aspects, aws_lambda as lambda } from 'aws-cdk-lib';
import * as recommendedalarms from '@renovosolutions/cdk-library-cloudwatch-alarms';

const app = new App();
const stack = new Stack(app, 'TestStack', {
  env: {
    account: '123456789012',
    region: 'us-east-1',
  },
});

const stack2 = new Stack(app, 'TestStack2', {
  env: {
    account: '123456789012',
    region: 'us-east-1',
  },
});

const appAspects = Aspects.of(app);

appAspects.add(
  new recommendedalarms.LambdaRecommendedAlarmsAspect({
    configDurationAlarm: {
      threshold: 15,
    },
    configErrorsAlarm: {
      threshold: 1,
    },
    configThrottlesAlarm: {
      threshold: 0,
    },
  }),
);

new lambda.Function(stack, 'Lambda', {
  runtime: lambda.Runtime.NODEJS_20_X,
  handler: 'index.handler',
  code: lambda.Code.fromInline('exports.handler = async (event) => { console.log(event); }'),
});

new lambda.Function(stack2, 'Lambda2', {
  runtime: lambda.Runtime.NODEJS_20_X,
  handler: 'index.handler',
  code: lambda.Code.fromInline('exports.handler = async (event) => { console.log(event); }'),
});
```

### Recommended Alarm Constructs

You can also apply alarms to a specific resource using the recommended alarm construct for a given resource type. For example if you have an S3 Bucket you might do something like below. None of the S3 alarms require configuration so no config props are needed in this case:

```python
import { App, Stack, Aspects, aws_s3 as s3 } from 'aws-cdk-lib';
import * as recommendedalarms from '@renovosolutions/cdk-library-cloudwatch-alarms';

const app = new App();
const stack = new Stack(app, 'TestStack', {
  env: {
    account: '123456789012',
    region: 'us-east-1',
  },
});

const bucket = new s3.Bucket(stack, 'Bucket', {});

new recommendedalarms.S3RecommendedAlarms(stack, 'RecommendedAlarms', {
  bucket,
});
```

### Individual Constructs

You can also apply specific alarms from their individual constructs:

```python
import { App, Stack, Aspects, aws_s3 as s3 } from 'aws-cdk-lib';
import * as recommendedalarms from '@renovosolutions/cdk-library-cloudwatch-alarms';

const app = new App();
const stack = new Stack(app, 'TestStack', {
  env: {
    account: '123456789012',
    region: 'us-east-1',
  },
});

const bucket = new s3.Bucket(stack, 'Bucket', {});

new recommendedalarms.S3Bucket5xxErrorsAlarm(stack, 'RecommendedAlarms', {
  bucket,
  threshold: 0.10,
});
```

### Construct Extensions

You can use extended versions of the constructs you are familiar with to expose helper methods for alarms if you'd like to keep alarms more tightly coupled to specific resources.

```python
import { App, Stack, Aspects, aws_s3 as s3 } from 'aws-cdk-lib';
import * as recommendedalarms from '@renovosolutions/cdk-library-cloudwatch-alarms';

const app = new App();
const stack = new Stack(app, 'TestStack', {
  env: {
    account: '123456789012',
    region: 'us-east-1',
  },
});

  const bucket = new recommendedalarms.Bucket(stack, 'Bucket', {});

  bucket.applyRecommendedAlarms();
```

### Alarm Actions

You can apply alarm actions using the default actions on an aspect or all recommended alarms construct or you can apply individual alarm actions for helper methods of individual constructs. See below where default actions are set but an override is set for a specific alarm for the alarm action to use a different SNS topic.

```python
import { App, Stack, Aspects, aws_lambda as lambda } from 'aws-cdk-lib';
import * as recommendedalarms from '@renovosolutions/cdk-library-cloudwatch-alarms';

const app = new App();
const stack = new Stack(app, 'TestStack', {
  env: {
    account: '123456789012',
    region: 'us-east-1',
  },
});

const stack2 = new Stack(app, 'TestStack2', {
  env: {
    account: '123456789012',
    region: 'us-east-1',
  },
});

const alarmTopic = new sns.Topic(stack, 'Topic');
const topicAction =  new cloudwatch_actions.SnsAction(alarmTopic)

const alarmTopic2 = new sns.Topic(stack, 'Topic');
const topicAction2 =  new cloudwatch_actions.SnsAction(alarmTopic2)

const appAspects = Aspects.of(app);

appAspects.add(
  new recommendedalarms.LambdaRecommendedAlarmsAspect({
    defaultAlarmAction: topicAction,
    defaultOkAction: topicAction,
    defaultInsufficientDataAction: topicAction,
    configDurationAlarm: {
      threshold: 15,
      alarmAction: topicAction2,
    },
    configErrorsAlarm: {
      threshold: 1,
    },
    configThrottlesAlarm: {
      threshold: 0,
    },

  }),
);

new lambda.Function(stack, 'Lambda', {
  runtime: lambda.Runtime.NODEJS_20_X,
  handler: 'index.handler',
  code: lambda.Code.fromInline('exports.handler = async (event) => { console.log(event); }'),
});

new lambda.Function(stack2, 'Lambda2', {
  runtime: lambda.Runtime.NODEJS_20_X,
  handler: 'index.handler',
  code: lambda.Code.fromInline('exports.handler = async (event) => { console.log(event); }'),
});
```

### Exclusions

You can exclude specific alarms or specific resources. Alarms use the available metrics enums and resources use the string used for a resources id. For example below Lambda1 will not have alarms created and there will be no alarm for the Duration metric for either lambda function.

```python
import { App, Stack, Aspects, aws_lambda as lambda } from 'aws-cdk-lib';
import * as recommendedalarms from '@renovosolutions/cdk-library-cloudwatch-alarms';

const app = new App();
const stack = new Stack(app, 'TestStack', {
  env: {
    account: '123456789012', // not a real account
    region: 'us-east-1',
  },
});

const appAspects = Aspects.of(app);

appAspects.add(
  new recommendedalarms.LambdaRecommendedAlarmsAspect({
    excludeResources: ['Lambda1'],
    excludeAlarms: [recommendedalarms.LambdaRecommendedAlarmsMetrics.DURATION],
    configDurationAlarm: {
      threshold: 15,
    },
    configErrorsAlarm: {
      threshold: 1,
    },
    configThrottlesAlarm: {
      threshold: 0,
    },
  }),
);

new lambda.Function(stack, 'Lambda1', {
  runtime: lambda.Runtime.NODEJS_20_X,
  handler: 'index.handler',
  code: lambda.Code.fromInline('exports.handler = async (event) => { console.log(event); }'),
});

new lambda.Function(stack, 'Lambda2', {
  runtime: lambda.Runtime.NODEJS_20_X,
  handler: 'index.handler',
  code: lambda.Code.fromInline('exports.handler = async (event) => { console.log(event); }'),
});
```

## References

* [AWS Recommended Alarms](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Best_Practice_Recommended_Alarms_AWS_Services.html)
* [Aspects and the AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/aspects.html)
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_cloudwatch as _aws_cdk_aws_cloudwatch_ceddda9d
import aws_cdk.aws_codeguruprofiler as _aws_cdk_aws_codeguruprofiler_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_kms as _aws_cdk_aws_kms_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import aws_cdk.aws_logs as _aws_cdk_aws_logs_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import aws_cdk.aws_sns as _aws_cdk_aws_sns_ceddda9d
import aws_cdk.aws_sqs as _aws_cdk_aws_sqs_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.AlarmBaseProps",
    jsii_struct_bases=[],
    name_mapping={
        "alarm_action": "alarmAction",
        "insufficient_data_action": "insufficientDataAction",
        "ok_action": "okAction",
        "treat_missing_data": "treatMissingData",
    },
)
class AlarmBaseProps:
    def __init__(
        self,
        *,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> None:
        '''The base properties for an alarm where default values are consistent across all alarms.

        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc8826645a1e265ceca74e67c468d47f270a951fd40c4c3bcf8922d80e34f685)
            check_type(argname="argument alarm_action", value=alarm_action, expected_type=type_hints["alarm_action"])
            check_type(argname="argument insufficient_data_action", value=insufficient_data_action, expected_type=type_hints["insufficient_data_action"])
            check_type(argname="argument ok_action", value=ok_action, expected_type=type_hints["ok_action"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alarm_action is not None:
            self._values["alarm_action"] = alarm_action
        if insufficient_data_action is not None:
            self._values["insufficient_data_action"] = insufficient_data_action
        if ok_action is not None:
            self._values["ok_action"] = ok_action
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data

    @builtins.property
    def alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlarmBaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Bucket(
    _aws_cdk_aws_s3_ceddda9d.Bucket,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.Bucket",
):
    '''An extension for the S3 Bucket construct that provides methods to create recommended alarms.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        access_control: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketAccessControl] = None,
        auto_delete_objects: typing.Optional[builtins.bool] = None,
        block_public_access: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BlockPublicAccess] = None,
        bucket_key_enabled: typing.Optional[builtins.bool] = None,
        bucket_name: typing.Optional[builtins.str] = None,
        cors: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.CorsRule, typing.Dict[builtins.str, typing.Any]]]] = None,
        encryption: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketEncryption] = None,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        enforce_ssl: typing.Optional[builtins.bool] = None,
        event_bridge_enabled: typing.Optional[builtins.bool] = None,
        intelligent_tiering_configurations: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.IntelligentTieringConfiguration, typing.Dict[builtins.str, typing.Any]]]] = None,
        inventories: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.Inventory, typing.Dict[builtins.str, typing.Any]]]] = None,
        lifecycle_rules: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.LifecycleRule, typing.Dict[builtins.str, typing.Any]]]] = None,
        metrics: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.BucketMetrics, typing.Dict[builtins.str, typing.Any]]]] = None,
        minimum_tls_version: typing.Optional[jsii.Number] = None,
        notifications_handler_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        notifications_skip_destination_validation: typing.Optional[builtins.bool] = None,
        object_lock_default_retention: typing.Optional[_aws_cdk_aws_s3_ceddda9d.ObjectLockRetention] = None,
        object_lock_enabled: typing.Optional[builtins.bool] = None,
        object_ownership: typing.Optional[_aws_cdk_aws_s3_ceddda9d.ObjectOwnership] = None,
        public_read_access: typing.Optional[builtins.bool] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        server_access_logs_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
        server_access_logs_prefix: typing.Optional[builtins.str] = None,
        target_object_key_format: typing.Optional[_aws_cdk_aws_s3_ceddda9d.TargetObjectKeyFormat] = None,
        transfer_acceleration: typing.Optional[builtins.bool] = None,
        versioned: typing.Optional[builtins.bool] = None,
        website_error_document: typing.Optional[builtins.str] = None,
        website_index_document: typing.Optional[builtins.str] = None,
        website_redirect: typing.Optional[typing.Union[_aws_cdk_aws_s3_ceddda9d.RedirectTarget, typing.Dict[builtins.str, typing.Any]]] = None,
        website_routing_rules: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.RoutingRule, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param access_control: Specifies a canned ACL that grants predefined permissions to the bucket. Default: BucketAccessControl.PRIVATE
        :param auto_delete_objects: Whether all objects should be automatically deleted when the bucket is removed from the stack or when the stack is deleted. Requires the ``removalPolicy`` to be set to ``RemovalPolicy.DESTROY``. **Warning** if you have deployed a bucket with ``autoDeleteObjects: true``, switching this to ``false`` in a CDK version *before* ``1.126.0`` will lead to all objects in the bucket being deleted. Be sure to update your bucket resources by deploying with CDK version ``1.126.0`` or later **before** switching this value to ``false``. Setting ``autoDeleteObjects`` to true on a bucket will add ``s3:PutBucketPolicy`` to the bucket policy. This is because during bucket deletion, the custom resource provider needs to update the bucket policy by adding a deny policy for ``s3:PutObject`` to prevent race conditions with external bucket writers. Default: false
        :param block_public_access: The block public access configuration of this bucket. Default: - CloudFormation defaults will apply. New buckets and objects don't allow public access, but users can modify bucket policies or object permissions to allow public access
        :param bucket_key_enabled: Whether Amazon S3 should use its own intermediary key to generate data keys. Only relevant when using KMS for encryption. - If not enabled, every object GET and PUT will cause an API call to KMS (with the attendant cost implications of that). - If enabled, S3 will use its own time-limited key instead. Only relevant, when Encryption is not set to ``BucketEncryption.UNENCRYPTED``. Default: - false
        :param bucket_name: Physical name of this bucket. Default: - Assigned by CloudFormation (recommended).
        :param cors: The CORS configuration of this bucket. Default: - No CORS configuration.
        :param encryption: The kind of server-side encryption to apply to this bucket. If you choose KMS, you can specify a KMS key via ``encryptionKey``. If encryption key is not specified, a key will automatically be created. Default: - ``KMS`` if ``encryptionKey`` is specified, or ``UNENCRYPTED`` otherwise. But if ``UNENCRYPTED`` is specified, the bucket will be encrypted as ``S3_MANAGED`` automatically.
        :param encryption_key: External KMS key to use for bucket encryption. The ``encryption`` property must be either not specified or set to ``KMS`` or ``DSSE``. An error will be emitted if ``encryption`` is set to ``UNENCRYPTED`` or ``S3_MANAGED``. Default: - If ``encryption`` is set to ``KMS`` and this property is undefined, a new KMS key will be created and associated with this bucket.
        :param enforce_ssl: Enforces SSL for requests. S3.5 of the AWS Foundational Security Best Practices Regarding S3. Default: false
        :param event_bridge_enabled: Whether this bucket should send notifications to Amazon EventBridge or not. Default: false
        :param intelligent_tiering_configurations: Inteligent Tiering Configurations. Default: No Intelligent Tiiering Configurations.
        :param inventories: The inventory configuration of the bucket. Default: - No inventory configuration
        :param lifecycle_rules: Rules that define how Amazon S3 manages objects during their lifetime. Default: - No lifecycle rules.
        :param metrics: The metrics configuration of this bucket. Default: - No metrics configuration.
        :param minimum_tls_version: Enforces minimum TLS version for requests. Requires ``enforceSSL`` to be enabled. Default: No minimum TLS version is enforced.
        :param notifications_handler_role: The role to be used by the notifications handler. Default: - a new role will be created.
        :param notifications_skip_destination_validation: Skips notification validation of Amazon SQS, Amazon SNS, and Lambda destinations. Default: false
        :param object_lock_default_retention: The default retention mode and rules for S3 Object Lock. Default retention can be configured after a bucket is created if the bucket already has object lock enabled. Enabling object lock for existing buckets is not supported. Default: no default retention period
        :param object_lock_enabled: Enable object lock on the bucket. Enabling object lock for existing buckets is not supported. Object lock must be enabled when the bucket is created. Default: false, unless objectLockDefaultRetention is set (then, true)
        :param object_ownership: The objectOwnership of the bucket. Default: - No ObjectOwnership configuration. By default, Amazon S3 sets Object Ownership to ``Bucket owner enforced``. This means ACLs are disabled and the bucket owner will own every object.
        :param public_read_access: Grants public read access to all objects in the bucket. Similar to calling ``bucket.grantPublicAccess()`` Default: false
        :param removal_policy: Policy to apply when the bucket is removed from this stack. Default: - The bucket will be orphaned.
        :param server_access_logs_bucket: Destination bucket for the server access logs. Default: - If "serverAccessLogsPrefix" undefined - access logs disabled, otherwise - log to current bucket.
        :param server_access_logs_prefix: Optional log file prefix to use for the bucket's access logs. If defined without "serverAccessLogsBucket", enables access logs to current bucket with this prefix. Default: - No log file prefix
        :param target_object_key_format: Optional key format for log objects. Default: - the default key format is: [DestinationPrefix][YYYY]-[MM]-[DD]-[hh]-[mm]-[ss]-[UniqueString]
        :param transfer_acceleration: Whether this bucket should have transfer acceleration turned on or not. Default: false
        :param versioned: Whether this bucket should have versioning turned on or not. Default: false (unless object lock is enabled, then true)
        :param website_error_document: The name of the error document (e.g. "404.html") for the website. ``websiteIndexDocument`` must also be set if this is set. Default: - No error document.
        :param website_index_document: The name of the index document (e.g. "index.html") for the website. Enables static website hosting for this bucket. Default: - No index document.
        :param website_redirect: Specifies the redirect behavior of all requests to a website endpoint of a bucket. If you specify this property, you can't specify "websiteIndexDocument", "websiteErrorDocument" nor , "websiteRoutingRules". Default: - No redirection.
        :param website_routing_rules: Rules that define when a redirect is applied and the redirect behavior. Default: - No redirection rules.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__997fd23e9dec2f8580d4a0f3905a7216624c6b51043d6491f7523aa123af316d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = _aws_cdk_aws_s3_ceddda9d.BucketProps(
            access_control=access_control,
            auto_delete_objects=auto_delete_objects,
            block_public_access=block_public_access,
            bucket_key_enabled=bucket_key_enabled,
            bucket_name=bucket_name,
            cors=cors,
            encryption=encryption,
            encryption_key=encryption_key,
            enforce_ssl=enforce_ssl,
            event_bridge_enabled=event_bridge_enabled,
            intelligent_tiering_configurations=intelligent_tiering_configurations,
            inventories=inventories,
            lifecycle_rules=lifecycle_rules,
            metrics=metrics,
            minimum_tls_version=minimum_tls_version,
            notifications_handler_role=notifications_handler_role,
            notifications_skip_destination_validation=notifications_skip_destination_validation,
            object_lock_default_retention=object_lock_default_retention,
            object_lock_enabled=object_lock_enabled,
            object_ownership=object_ownership,
            public_read_access=public_read_access,
            removal_policy=removal_policy,
            server_access_logs_bucket=server_access_logs_bucket,
            server_access_logs_prefix=server_access_logs_prefix,
            target_object_key_format=target_object_key_format,
            transfer_acceleration=transfer_acceleration,
            versioned=versioned,
            website_error_document=website_error_document,
            website_index_document=website_index_document,
            website_redirect=website_redirect,
            website_routing_rules=website_routing_rules,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="alarm4xxErrors")
    def alarm4xx_errors(
        self,
        *,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        threshold: typing.Optional[jsii.Number] = None,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> "S3Bucket4xxErrorsAlarm":
        '''Creates an alarm that monitors the 4xx errors for the S3 bucket.

        :param alarm_description: The alarm description. Default: - This alarm helps us report the total number of 4xx error status codes that are made in response to client requests. 403 error codes might indicate an incorrect IAM policy, and 404 error codes might indicate mis-behaving client application, for example. Enabling S3 server access logging on a temporary basis will help you to pinpoint the issue's origin using the fields HTTP status and Error Code. To understand more about the error code, see Error Responses (https://docs.aws.amazon.com/AmazonS3/latest/API/ErrorResponses.html).
        :param alarm_name: The alarm name. Default: - bucket.bucketName + ' - 4xxErrors'
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 15
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 15
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param threshold: The value against which the specified statistic is compared. Default: 0.05
        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        props = S3Bucket4xxErrorsAlarmConfig(
            alarm_description=alarm_description,
            alarm_name=alarm_name,
            datapoints_to_alarm=datapoints_to_alarm,
            evaluation_periods=evaluation_periods,
            period=period,
            threshold=threshold,
            alarm_action=alarm_action,
            insufficient_data_action=insufficient_data_action,
            ok_action=ok_action,
            treat_missing_data=treat_missing_data,
        )

        return typing.cast("S3Bucket4xxErrorsAlarm", jsii.invoke(self, "alarm4xxErrors", [props]))

    @jsii.member(jsii_name="alarm5xxErrors")
    def alarm5xx_errors(
        self,
        *,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        threshold: typing.Optional[jsii.Number] = None,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> "S3Bucket5xxErrorsAlarm":
        '''Creates an alarm that monitors the 5xx errors for the S3 bucket.

        :param alarm_description: The alarm description. Default: - This alarm helps you detect a high number of server-side errors. These errors indicate that a client made a request that the server couldn’t complete. This can help you correlate the issue your application is facing because of S3. For more information to help you efficiently handle or reduce errors, see Optimizing performance design patterns (https://docs.aws.amazon.com/AmazonS3/latest/userguide/optimizing-performance-design-patterns.html#optimizing-performance-timeouts-retries). Errors might also be caused by an the issue with S3, check AWS service health dashboard for the status of Amazon S3 in your Region.
        :param alarm_name: The alarm name. Default: - bucket.bucketName + ' - 5xxErrors'
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 15
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 15
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param threshold: The value against which the specified statistic is compared. Default: 0.05
        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        props = S3Bucket5xxErrorsAlarmConfig(
            alarm_description=alarm_description,
            alarm_name=alarm_name,
            datapoints_to_alarm=datapoints_to_alarm,
            evaluation_periods=evaluation_periods,
            period=period,
            threshold=threshold,
            alarm_action=alarm_action,
            insufficient_data_action=insufficient_data_action,
            ok_action=ok_action,
            treat_missing_data=treat_missing_data,
        )

        return typing.cast("S3Bucket5xxErrorsAlarm", jsii.invoke(self, "alarm5xxErrors", [props]))

    @jsii.member(jsii_name="applyRecommendedAlarms")
    def apply_recommended_alarms(
        self,
        *,
        config4xx_errors_alarm: typing.Optional[typing.Union["S3Bucket4xxErrorsAlarmConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        config5xx_errors_alarm: typing.Optional[typing.Union["S3Bucket5xxErrorsAlarmConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        default_alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        default_insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        default_ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        exclude_alarms: typing.Optional[typing.Sequence["S3RecommendedAlarmsMetrics"]] = None,
        exclude_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> "S3RecommendedAlarms":
        '''Creates the recommended alarms for the S3 bucket.

        :param config4xx_errors_alarm: The configuration for the 4xx errors alarm.
        :param config5xx_errors_alarm: The configuration for the 5xx errors alarm.
        :param default_alarm_action: The default action to take when an alarm is triggered. Default: - None
        :param default_insufficient_data_action: The default action to take when an alarm has insufficient data. Default: - None
        :param default_ok_action: The default action to take when an alarm enters the ok state. Default: - None
        :param exclude_alarms: Alarm metrics to exclude from the recommended alarms. Default: - None
        :param exclude_resources: The resources to exclude from the recommended alarms. Use a resources id to exclude a specific resource.
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Best_Practice_Recommended_Alarms_AWS_Services.html#S3
        '''
        props = S3RecommendedAlarmsConfig(
            config4xx_errors_alarm=config4xx_errors_alarm,
            config5xx_errors_alarm=config5xx_errors_alarm,
            default_alarm_action=default_alarm_action,
            default_insufficient_data_action=default_insufficient_data_action,
            default_ok_action=default_ok_action,
            exclude_alarms=exclude_alarms,
            exclude_resources=exclude_resources,
            treat_missing_data=treat_missing_data,
        )

        return typing.cast("S3RecommendedAlarms", jsii.invoke(self, "applyRecommendedAlarms", [props]))


class Function(
    _aws_cdk_aws_lambda_ceddda9d.Function,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.Function",
):
    '''An extension of the Lambda function construct that provides methods to create recommended alarms.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        code: _aws_cdk_aws_lambda_ceddda9d.Code,
        handler: builtins.str,
        runtime: _aws_cdk_aws_lambda_ceddda9d.Runtime,
        adot_instrumentation: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.AdotInstrumentationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        allow_all_outbound: typing.Optional[builtins.bool] = None,
        allow_public_subnet: typing.Optional[builtins.bool] = None,
        application_log_level: typing.Optional[builtins.str] = None,
        application_log_level_v2: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.ApplicationLogLevel] = None,
        architecture: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture] = None,
        code_signing_config: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.ICodeSigningConfig] = None,
        current_version_options: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.VersionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        dead_letter_queue_enabled: typing.Optional[builtins.bool] = None,
        dead_letter_topic: typing.Optional[_aws_cdk_aws_sns_ceddda9d.ITopic] = None,
        description: typing.Optional[builtins.str] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        environment_encryption: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        ephemeral_storage_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
        events: typing.Optional[typing.Sequence[_aws_cdk_aws_lambda_ceddda9d.IEventSource]] = None,
        filesystem: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.FileSystem] = None,
        function_name: typing.Optional[builtins.str] = None,
        initial_policy: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]] = None,
        insights_version: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.LambdaInsightsVersion] = None,
        ipv6_allowed_for_dual_stack: typing.Optional[builtins.bool] = None,
        layers: typing.Optional[typing.Sequence[_aws_cdk_aws_lambda_ceddda9d.ILayerVersion]] = None,
        log_format: typing.Optional[builtins.str] = None,
        logging_format: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.LoggingFormat] = None,
        log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup] = None,
        log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
        log_retention_retry_options: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.LogRetentionRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        log_retention_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        memory_size: typing.Optional[jsii.Number] = None,
        params_and_secrets: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.ParamsAndSecretsLayerVersion] = None,
        profiling: typing.Optional[builtins.bool] = None,
        profiling_group: typing.Optional[_aws_cdk_aws_codeguruprofiler_ceddda9d.IProfilingGroup] = None,
        recursive_loop: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.RecursiveLoop] = None,
        reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        runtime_management_mode: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.RuntimeManagementMode] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        snap_start: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.SnapStartConf] = None,
        system_log_level: typing.Optional[builtins.str] = None,
        system_log_level_v2: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.SystemLogLevel] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        tracing: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Tracing] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        on_failure: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination] = None,
        on_success: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param code: The source code of your Lambda function. You can point to a file in an Amazon Simple Storage Service (Amazon S3) bucket or specify your source code as inline text.
        :param handler: The name of the method within your code that Lambda calls to execute your function. The format includes the file name. It can also include namespaces and other qualifiers, depending on the runtime. For more information, see https://docs.aws.amazon.com/lambda/latest/dg/foundation-progmodel.html. Use ``Handler.FROM_IMAGE`` when defining a function from a Docker image. NOTE: If you specify your source code as inline text by specifying the ZipFile property within the Code property, specify index.function_name as the handler.
        :param runtime: The runtime environment for the Lambda function that you are uploading. For valid values, see the Runtime property in the AWS Lambda Developer Guide. Use ``Runtime.FROM_IMAGE`` when defining a function from a Docker image.
        :param adot_instrumentation: Specify the configuration of AWS Distro for OpenTelemetry (ADOT) instrumentation. Default: - No ADOT instrumentation
        :param allow_all_outbound: Whether to allow the Lambda to send all network traffic. If set to false, you must individually add traffic rules to allow the Lambda to connect to network targets. Do not specify this property if the ``securityGroups`` or ``securityGroup`` property is set. Instead, configure ``allowAllOutbound`` directly on the security group. Default: true
        :param allow_public_subnet: Lambda Functions in a public subnet can NOT access the internet. Use this property to acknowledge this limitation and still place the function in a public subnet. Default: false
        :param application_log_level: (deprecated) Sets the application log level for the function. Default: "INFO"
        :param application_log_level_v2: Sets the application log level for the function. Default: ApplicationLogLevel.INFO
        :param architecture: The system architectures compatible with this lambda function. Default: Architecture.X86_64
        :param code_signing_config: Code signing config associated with this function. Default: - Not Sign the Code
        :param current_version_options: Options for the ``lambda.Version`` resource automatically created by the ``fn.currentVersion`` method. Default: - default options as described in ``VersionOptions``
        :param dead_letter_queue: The SQS queue to use if DLQ is enabled. If SNS topic is desired, specify ``deadLetterTopic`` property instead. Default: - SQS queue with 14 day retention period if ``deadLetterQueueEnabled`` is ``true``
        :param dead_letter_queue_enabled: Enabled DLQ. If ``deadLetterQueue`` is undefined, an SQS queue with default options will be defined for your Function. Default: - false unless ``deadLetterQueue`` is set, which implies DLQ is enabled.
        :param dead_letter_topic: The SNS topic to use as a DLQ. Note that if ``deadLetterQueueEnabled`` is set to ``true``, an SQS queue will be created rather than an SNS topic. Using an SNS topic as a DLQ requires this property to be set explicitly. Default: - no SNS topic
        :param description: A description of the function. Default: - No description.
        :param environment: Key-value pairs that Lambda caches and makes available for your Lambda functions. Use environment variables to apply configuration changes, such as test and production environment configurations, without changing your Lambda function source code. Default: - No environment variables.
        :param environment_encryption: The AWS KMS key that's used to encrypt your function's environment variables. Default: - AWS Lambda creates and uses an AWS managed customer master key (CMK).
        :param ephemeral_storage_size: The size of the function’s /tmp directory in MiB. Default: 512 MiB
        :param events: Event sources for this function. You can also add event sources using ``addEventSource``. Default: - No event sources.
        :param filesystem: The filesystem configuration for the lambda function. Default: - will not mount any filesystem
        :param function_name: A name for the function. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the function's name. For more information, see Name Type.
        :param initial_policy: Initial policy statements to add to the created Lambda Role. You can call ``addToRolePolicy`` to the created lambda to add statements post creation. Default: - No policy statements are added to the created Lambda role.
        :param insights_version: Specify the version of CloudWatch Lambda insights to use for monitoring. Default: - No Lambda Insights
        :param ipv6_allowed_for_dual_stack: Allows outbound IPv6 traffic on VPC functions that are connected to dual-stack subnets. Only used if 'vpc' is supplied. Default: false
        :param layers: A list of layers to add to the function's execution environment. You can configure your Lambda function to pull in additional code during initialization in the form of layers. Layers are packages of libraries or other dependencies that can be used by multiple functions. Default: - No layers.
        :param log_format: (deprecated) Sets the logFormat for the function. Default: "Text"
        :param logging_format: Sets the loggingFormat for the function. Default: LoggingFormat.TEXT
        :param log_group: The log group the function sends logs to. By default, Lambda functions send logs to an automatically created default log group named /aws/lambda/<function name>. However you cannot change the properties of this auto-created log group using the AWS CDK, e.g. you cannot set a different log retention. Use the ``logGroup`` property to create a fully customizable LogGroup ahead of time, and instruct the Lambda function to send logs to it. Providing a user-controlled log group was rolled out to commercial regions on 2023-11-16. If you are deploying to another type of region, please check regional availability first. Default: ``/aws/lambda/${this.functionName}`` - default log group created by Lambda
        :param log_retention: The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. This is a legacy API and we strongly recommend you move away from it if you can. Instead create a fully customizable log group with ``logs.LogGroup`` and use the ``logGroup`` property to instruct the Lambda function to send logs to it. Migrating from ``logRetention`` to ``logGroup`` will cause the name of the log group to change. Users and code and referencing the name verbatim will have to adjust. In AWS CDK code, you can access the log group name directly from the LogGroup construct:: import * as logs from 'aws-cdk-lib/aws-logs'; declare const myLogGroup: logs.LogGroup; myLogGroup.logGroupName; Default: logs.RetentionDays.INFINITE
        :param log_retention_retry_options: When log retention is specified, a custom resource attempts to create the CloudWatch log group. These options control the retry policy when interacting with CloudWatch APIs. This is a legacy API and we strongly recommend you migrate to ``logGroup`` if you can. ``logGroup`` allows you to create a fully customizable log group and instruct the Lambda function to send logs to it. Default: - Default AWS SDK retry options.
        :param log_retention_role: The IAM role for the Lambda function associated with the custom resource that sets the retention policy. This is a legacy API and we strongly recommend you migrate to ``logGroup`` if you can. ``logGroup`` allows you to create a fully customizable log group and instruct the Lambda function to send logs to it. Default: - A new role is created.
        :param memory_size: The amount of memory, in MB, that is allocated to your Lambda function. Lambda uses this value to proportionally allocate the amount of CPU power. For more information, see Resource Model in the AWS Lambda Developer Guide. Default: 128
        :param params_and_secrets: Specify the configuration of Parameters and Secrets Extension. Default: - No Parameters and Secrets Extension
        :param profiling: Enable profiling. Default: - No profiling.
        :param profiling_group: Profiling Group. Default: - A new profiling group will be created if ``profiling`` is set.
        :param recursive_loop: Sets the Recursive Loop Protection for Lambda Function. It lets Lambda detect and terminate unintended recusrive loops. Default: RecursiveLoop.Terminate
        :param reserved_concurrent_executions: The maximum of concurrent executions you want to reserve for the function. Default: - No specific limit - account limit.
        :param role: Lambda execution role. This is the role that will be assumed by the function upon execution. It controls the permissions that the function will have. The Role must be assumable by the 'lambda.amazonaws.com' service principal. The default Role automatically has permissions granted for Lambda execution. If you provide a Role, you must add the relevant AWS managed policies yourself. The relevant managed policies are "service-role/AWSLambdaBasicExecutionRole" and "service-role/AWSLambdaVPCAccessExecutionRole". Default: - A unique role will be generated for this lambda function. Both supplied and generated roles can always be changed by calling ``addToRolePolicy``.
        :param runtime_management_mode: Sets the runtime management configuration for a function's version. Default: Auto
        :param security_groups: The list of security groups to associate with the Lambda's network interfaces. Only used if 'vpc' is supplied. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroup prop, a dedicated security group will be created for this function.
        :param snap_start: Enable SnapStart for Lambda Function. SnapStart is currently supported only for Java 11, 17 runtime Default: - No snapstart
        :param system_log_level: (deprecated) Sets the system log level for the function. Default: "INFO"
        :param system_log_level_v2: Sets the system log level for the function. Default: SystemLogLevel.INFO
        :param timeout: The function execution time (in seconds) after which Lambda terminates the function. Because the execution time affects cost, set this value based on the function's expected execution time. Default: Duration.seconds(3)
        :param tracing: Enable AWS X-Ray Tracing for Lambda Function. Default: Tracing.Disabled
        :param vpc: VPC network to place Lambda network interfaces. Specify this if the Lambda function needs to access resources in a VPC. This is required when ``vpcSubnets`` is specified. Default: - Function is not placed within a VPC.
        :param vpc_subnets: Where to place the network interfaces within the VPC. This requires ``vpc`` to be specified in order for interfaces to actually be placed in the subnets. If ``vpc`` is not specify, this will raise an error. Note: Internet access for Lambda Functions requires a NAT Gateway, so picking public subnets is not allowed (unless ``allowPublicSubnet`` is set to ``true``). Default: - the Vpc default strategy if not specified
        :param max_event_age: The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: The destination for failed invocations. Default: - no destination
        :param on_success: The destination for successful invocations. Default: - no destination
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__300e1b7b513ed361a8dde12f23c6adb84738ebf013386259a5dbea5024022ffa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = _aws_cdk_aws_lambda_ceddda9d.FunctionProps(
            code=code,
            handler=handler,
            runtime=runtime,
            adot_instrumentation=adot_instrumentation,
            allow_all_outbound=allow_all_outbound,
            allow_public_subnet=allow_public_subnet,
            application_log_level=application_log_level,
            application_log_level_v2=application_log_level_v2,
            architecture=architecture,
            code_signing_config=code_signing_config,
            current_version_options=current_version_options,
            dead_letter_queue=dead_letter_queue,
            dead_letter_queue_enabled=dead_letter_queue_enabled,
            dead_letter_topic=dead_letter_topic,
            description=description,
            environment=environment,
            environment_encryption=environment_encryption,
            ephemeral_storage_size=ephemeral_storage_size,
            events=events,
            filesystem=filesystem,
            function_name=function_name,
            initial_policy=initial_policy,
            insights_version=insights_version,
            ipv6_allowed_for_dual_stack=ipv6_allowed_for_dual_stack,
            layers=layers,
            log_format=log_format,
            logging_format=logging_format,
            log_group=log_group,
            log_retention=log_retention,
            log_retention_retry_options=log_retention_retry_options,
            log_retention_role=log_retention_role,
            memory_size=memory_size,
            params_and_secrets=params_and_secrets,
            profiling=profiling,
            profiling_group=profiling_group,
            recursive_loop=recursive_loop,
            reserved_concurrent_executions=reserved_concurrent_executions,
            role=role,
            runtime_management_mode=runtime_management_mode,
            security_groups=security_groups,
            snap_start=snap_start,
            system_log_level=system_log_level,
            system_log_level_v2=system_log_level_v2,
            timeout=timeout,
            tracing=tracing,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
            max_event_age=max_event_age,
            on_failure=on_failure,
            on_success=on_success,
            retry_attempts=retry_attempts,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="alarmConcurrentExecutions")
    def alarm_concurrent_executions(
        self,
        *,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        threshold: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> "LambdaConcurrentExecutionsAlarm":
        '''Creates an alarm that monitors the number of concurrent executions.

        :param alarm_description: The description of the alarm. Default: - This alarm helps to monitor if the concurrency of the function is approaching the Region-level concurrency limit of your account. A function starts to be throttled if it reaches the concurrency limit.
        :param alarm_name: The alarm name. Default: - lambdaFunction.functionName + ' - ConcurrentExecutions'
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 10
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 10
        :param threshold: The value against which the specified statictis is compared. Set the threshold to about 90% of the concurrency quota set for the account in the Region. By default, your account has a concurrency quota of 1,000 across all functions in a Region. However, you can check the quota of your account, as it can be increased by contacting AWS support. Default: 900
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        props = LambdaConcurrentExecutionsAlarmConfig(
            alarm_description=alarm_description,
            alarm_name=alarm_name,
            datapoints_to_alarm=datapoints_to_alarm,
            evaluation_periods=evaluation_periods,
            threshold=threshold,
            period=period,
            alarm_action=alarm_action,
            insufficient_data_action=insufficient_data_action,
            ok_action=ok_action,
            treat_missing_data=treat_missing_data,
        )

        return typing.cast("LambdaConcurrentExecutionsAlarm", jsii.invoke(self, "alarmConcurrentExecutions", [props]))

    @jsii.member(jsii_name="alarmDuration")
    def alarm_duration(
        self,
        *,
        threshold: jsii.Number,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> "LambdaDurationAlarm":
        '''Creates an alarm that monitors the duration of the function invocations.

        :param threshold: The value against which the specified statictis is compared. The threshold for the duration depends on your application and workloads and your performance requirements. For high-performance requirements, set the threshold to a shorter time to see if the function is meeting expectations. You can also analyze historical data for duration metrics to see the if the time taken matches the performance expectation of the function, and then set the threshold to a longer time than the historical average. Make sure to set the threshold lower than the configured function timeout.
        :param alarm_description: The description of the alarm. Default: - This alarm detects long duration times for processing an event by a Lambda function. Long durations might be because of changes in function code making the function take longer to execute, or the function's dependencies taking longer.
        :param alarm_name: The alarm name. Default: - lambdaFunction.functionName + ' - Duration'
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 15
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 15
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        props = LambdaDurationAlarmConfig(
            threshold=threshold,
            alarm_description=alarm_description,
            alarm_name=alarm_name,
            datapoints_to_alarm=datapoints_to_alarm,
            evaluation_periods=evaluation_periods,
            period=period,
            alarm_action=alarm_action,
            insufficient_data_action=insufficient_data_action,
            ok_action=ok_action,
            treat_missing_data=treat_missing_data,
        )

        return typing.cast("LambdaDurationAlarm", jsii.invoke(self, "alarmDuration", [props]))

    @jsii.member(jsii_name="alarmErrors")
    def alarm_errors(
        self,
        *,
        threshold: jsii.Number,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> "LambdaErrorsAlarm":
        '''Creates an alarm that monitors the number of errors.

        :param threshold: The value against which the specified statictis is compared. Set the threshold to a number greater than zero. The exact value can depend on the tolerance for errors in your application. Understand the criticality of the invocations that the function is handling. For some applications, any error might be unacceptable, while other applications might allow for a certain margin of error.
        :param alarm_description: The description of the alarm. Default: - This alarm detects high error counts. Errors includes the exceptions thrown by the code as well as exceptions thrown by the Lambda runtime. You can check the logs related to the function to diagnose the issue.
        :param alarm_name: The alarm name. Default: - lambdaFunction.functionName + ' - Errors'
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 3
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 3
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        props = LambdaErrorsAlarmConfig(
            threshold=threshold,
            alarm_description=alarm_description,
            alarm_name=alarm_name,
            datapoints_to_alarm=datapoints_to_alarm,
            evaluation_periods=evaluation_periods,
            period=period,
            alarm_action=alarm_action,
            insufficient_data_action=insufficient_data_action,
            ok_action=ok_action,
            treat_missing_data=treat_missing_data,
        )

        return typing.cast("LambdaErrorsAlarm", jsii.invoke(self, "alarmErrors", [props]))

    @jsii.member(jsii_name="alarmThrottles")
    def alarm_throttles(
        self,
        *,
        threshold: jsii.Number,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> "LambdaThrottlesAlarm":
        '''Creates an alarm that monitors the number of throttles.

        :param threshold: The value against which the specified statictis is compared. Set the threshold to a number greater than zero. The exact value of the threshold can depend on the tolerance of the application. Set the threshold according to its usage and scaling requirements of the function.
        :param alarm_description: The description of the alarm. Default: - This alarm detects a high number of throttled invocation requests. Throttling occurs when there is no concurrency is available for scale up. There are several approaches to resolve this issue. 1. Request a concurrency increase from AWS Support in this Region. 2) Identify performance issues in the function to improve the speed of processing and therefore improve throughput. 3) Increase the batch size of the function, so that more messages are processed by each function invocation.
        :param alarm_name: The alarm name. Default: - lambdaFunction.functionName + ' - Throttles'
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 5
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 5
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        props = LambdaThrottlesAlarmConfig(
            threshold=threshold,
            alarm_description=alarm_description,
            alarm_name=alarm_name,
            datapoints_to_alarm=datapoints_to_alarm,
            evaluation_periods=evaluation_periods,
            period=period,
            alarm_action=alarm_action,
            insufficient_data_action=insufficient_data_action,
            ok_action=ok_action,
            treat_missing_data=treat_missing_data,
        )

        return typing.cast("LambdaThrottlesAlarm", jsii.invoke(self, "alarmThrottles", [props]))

    @jsii.member(jsii_name="applyRecommendedAlarms")
    def apply_recommended_alarms(
        self,
        *,
        config_duration_alarm: typing.Union["LambdaDurationAlarmConfig", typing.Dict[builtins.str, typing.Any]],
        config_errors_alarm: typing.Union["LambdaErrorsAlarmConfig", typing.Dict[builtins.str, typing.Any]],
        config_throttles_alarm: typing.Union["LambdaThrottlesAlarmConfig", typing.Dict[builtins.str, typing.Any]],
        config_concurrent_executions_alarm: typing.Optional[typing.Union["LambdaConcurrentExecutionsAlarmConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        default_alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        default_insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        default_ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        exclude_alarms: typing.Optional[typing.Sequence["LambdaRecommendedAlarmsMetrics"]] = None,
        exclude_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> "LambdaRecommendedAlarms":
        '''Creates recommended alarms for the Lambda function.

        :param config_duration_alarm: The configuration for the Duration alarm.
        :param config_errors_alarm: The configuration for the Errors alarm.
        :param config_throttles_alarm: The configuration for the Throttles alarm.
        :param config_concurrent_executions_alarm: The configuration for the ConcurrentExecutions alarm.
        :param default_alarm_action: The default action to take when an alarm is triggered. Default: - None
        :param default_insufficient_data_action: The default action to take when an alarm has insufficient data. Default: - None
        :param default_ok_action: The default action to take when an alarm enters the ok state. Default: - None
        :param exclude_alarms: Alarm metrics to exclude from the recommended alarms. Default: - None
        :param exclude_resources: The resources to exclude from the recommended alarms. Use a resources id to exclude a specific resource.
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Best_Practice_Recommended_Alarms_AWS_Services.html#Lambda
        '''
        props = LambdaRecommendedAlarmsConfig(
            config_duration_alarm=config_duration_alarm,
            config_errors_alarm=config_errors_alarm,
            config_throttles_alarm=config_throttles_alarm,
            config_concurrent_executions_alarm=config_concurrent_executions_alarm,
            default_alarm_action=default_alarm_action,
            default_insufficient_data_action=default_insufficient_data_action,
            default_ok_action=default_ok_action,
            exclude_alarms=exclude_alarms,
            exclude_resources=exclude_resources,
            treat_missing_data=treat_missing_data,
        )

        return typing.cast("LambdaRecommendedAlarms", jsii.invoke(self, "applyRecommendedAlarms", [props]))


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.LambdaAlarmBaseConfig",
    jsii_struct_bases=[AlarmBaseProps],
    name_mapping={
        "alarm_action": "alarmAction",
        "insufficient_data_action": "insufficientDataAction",
        "ok_action": "okAction",
        "treat_missing_data": "treatMissingData",
        "period": "period",
    },
)
class LambdaAlarmBaseConfig(AlarmBaseProps):
    def __init__(
        self,
        *,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''
        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__716b419718f93d506f3a8f28e319b9f808eddee3d4641ebd195dccca8d474eec)
            check_type(argname="argument alarm_action", value=alarm_action, expected_type=type_hints["alarm_action"])
            check_type(argname="argument insufficient_data_action", value=insufficient_data_action, expected_type=type_hints["insufficient_data_action"])
            check_type(argname="argument ok_action", value=ok_action, expected_type=type_hints["ok_action"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alarm_action is not None:
            self._values["alarm_action"] = alarm_action
        if insufficient_data_action is not None:
            self._values["insufficient_data_action"] = insufficient_data_action
        if ok_action is not None:
            self._values["ok_action"] = ok_action
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data
        if period is not None:
            self._values["period"] = period

    @builtins.property
    def alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    @builtins.property
    def period(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The period over which the specified statistic is applied.

        :default: Duration.minutes(1)
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaAlarmBaseConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaConcurrentExecutionsAlarm(
    _aws_cdk_aws_cloudwatch_ceddda9d.Alarm,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.LambdaConcurrentExecutionsAlarm",
):
    '''This alarm can proactively detect if the concurrency of the function is approaching the Region-level concurrency quota of your account, so that you can act on it.

    A function is
    throttled if it reaches the Region-level concurrency quota
    of the account.

    The alarm is triggered when the number of concurrent executions
    exceeds the specified threshold.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        lambda_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        threshold: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param lambda_function: The Lambda function to monitor.
        :param alarm_description: The description of the alarm. Default: - This alarm helps to monitor if the concurrency of the function is approaching the Region-level concurrency limit of your account. A function starts to be throttled if it reaches the concurrency limit.
        :param alarm_name: The alarm name. Default: - lambdaFunction.functionName + ' - ConcurrentExecutions'
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 10
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 10
        :param threshold: The value against which the specified statictis is compared. Set the threshold to about 90% of the concurrency quota set for the account in the Region. By default, your account has a concurrency quota of 1,000 across all functions in a Region. However, you can check the quota of your account, as it can be increased by contacting AWS support. Default: 900
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bfb27966b8b66696e58f0cdca63f38b3e4abd2f029e1dcdd883870f471a74c7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = LambdaConcurrentExecutionsAlarmProps(
            lambda_function=lambda_function,
            alarm_description=alarm_description,
            alarm_name=alarm_name,
            datapoints_to_alarm=datapoints_to_alarm,
            evaluation_periods=evaluation_periods,
            threshold=threshold,
            period=period,
            alarm_action=alarm_action,
            insufficient_data_action=insufficient_data_action,
            ok_action=ok_action,
            treat_missing_data=treat_missing_data,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.LambdaConcurrentExecutionsAlarmConfig",
    jsii_struct_bases=[LambdaAlarmBaseConfig],
    name_mapping={
        "alarm_action": "alarmAction",
        "insufficient_data_action": "insufficientDataAction",
        "ok_action": "okAction",
        "treat_missing_data": "treatMissingData",
        "period": "period",
        "alarm_description": "alarmDescription",
        "alarm_name": "alarmName",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluation_periods": "evaluationPeriods",
        "threshold": "threshold",
    },
)
class LambdaConcurrentExecutionsAlarmConfig(LambdaAlarmBaseConfig):
    def __init__(
        self,
        *,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Configuration for the ConcurrentExecutions alarm.

        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param alarm_description: The description of the alarm. Default: - This alarm helps to monitor if the concurrency of the function is approaching the Region-level concurrency limit of your account. A function starts to be throttled if it reaches the concurrency limit.
        :param alarm_name: The alarm name. Default: - lambdaFunction.functionName + ' - ConcurrentExecutions'
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 10
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 10
        :param threshold: The value against which the specified statictis is compared. Set the threshold to about 90% of the concurrency quota set for the account in the Region. By default, your account has a concurrency quota of 1,000 across all functions in a Region. However, you can check the quota of your account, as it can be increased by contacting AWS support. Default: 900
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f6d24fc2ab7dcff701615e4987ae78b3dd173cefd3eb98f56fd3cd288d75b47)
            check_type(argname="argument alarm_action", value=alarm_action, expected_type=type_hints["alarm_action"])
            check_type(argname="argument insufficient_data_action", value=insufficient_data_action, expected_type=type_hints["insufficient_data_action"])
            check_type(argname="argument ok_action", value=ok_action, expected_type=type_hints["ok_action"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument alarm_description", value=alarm_description, expected_type=type_hints["alarm_description"])
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alarm_action is not None:
            self._values["alarm_action"] = alarm_action
        if insufficient_data_action is not None:
            self._values["insufficient_data_action"] = insufficient_data_action
        if ok_action is not None:
            self._values["ok_action"] = ok_action
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data
        if period is not None:
            self._values["period"] = period
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if alarm_name is not None:
            self._values["alarm_name"] = alarm_name
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluation_periods is not None:
            self._values["evaluation_periods"] = evaluation_periods
        if threshold is not None:
            self._values["threshold"] = threshold

    @builtins.property
    def alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    @builtins.property
    def period(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The period over which the specified statistic is applied.

        :default: Duration.minutes(1)
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        '''The description of the alarm.

        :default:

        - This alarm helps to monitor if the concurrency of the function is approaching the Region-level
        concurrency limit of your account. A function starts to be throttled if it reaches the concurrency limit.
        '''
        result = self._values.get("alarm_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_name(self) -> typing.Optional[builtins.str]:
        '''The alarm name.

        :default: - lambdaFunction.functionName + ' - ConcurrentExecutions'
        '''
        result = self._values.get("alarm_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of data points that must be breaching to trigger the alarm.

        :default: 10
        '''
        result = self._values.get("datapoints_to_alarm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''The number of periods over which data is compared to the specified threshold.

        :default: 10
        '''
        result = self._values.get("evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def threshold(self) -> typing.Optional[jsii.Number]:
        '''The value against which the specified statictis is compared.

        Set the threshold to about 90% of the concurrency quota set
        for the account in the Region. By default, your account has
        a concurrency quota of 1,000 across all functions in a Region.
        However, you can check the quota of your account, as it can
        be increased by contacting AWS support.

        :default: 900
        '''
        result = self._values.get("threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaConcurrentExecutionsAlarmConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.LambdaConcurrentExecutionsAlarmProps",
    jsii_struct_bases=[LambdaConcurrentExecutionsAlarmConfig],
    name_mapping={
        "alarm_action": "alarmAction",
        "insufficient_data_action": "insufficientDataAction",
        "ok_action": "okAction",
        "treat_missing_data": "treatMissingData",
        "period": "period",
        "alarm_description": "alarmDescription",
        "alarm_name": "alarmName",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluation_periods": "evaluationPeriods",
        "threshold": "threshold",
        "lambda_function": "lambdaFunction",
    },
)
class LambdaConcurrentExecutionsAlarmProps(LambdaConcurrentExecutionsAlarmConfig):
    def __init__(
        self,
        *,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        threshold: typing.Optional[jsii.Number] = None,
        lambda_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
    ) -> None:
        '''The properties for the LambdaConcurrentExecutionsAlarm construct.

        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param alarm_description: The description of the alarm. Default: - This alarm helps to monitor if the concurrency of the function is approaching the Region-level concurrency limit of your account. A function starts to be throttled if it reaches the concurrency limit.
        :param alarm_name: The alarm name. Default: - lambdaFunction.functionName + ' - ConcurrentExecutions'
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 10
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 10
        :param threshold: The value against which the specified statictis is compared. Set the threshold to about 90% of the concurrency quota set for the account in the Region. By default, your account has a concurrency quota of 1,000 across all functions in a Region. However, you can check the quota of your account, as it can be increased by contacting AWS support. Default: 900
        :param lambda_function: The Lambda function to monitor.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d8926f47d763f0933cbd527860988a8a2749c891924dcd36c2f3f1e29039d6f)
            check_type(argname="argument alarm_action", value=alarm_action, expected_type=type_hints["alarm_action"])
            check_type(argname="argument insufficient_data_action", value=insufficient_data_action, expected_type=type_hints["insufficient_data_action"])
            check_type(argname="argument ok_action", value=ok_action, expected_type=type_hints["ok_action"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument alarm_description", value=alarm_description, expected_type=type_hints["alarm_description"])
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument lambda_function", value=lambda_function, expected_type=type_hints["lambda_function"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "lambda_function": lambda_function,
        }
        if alarm_action is not None:
            self._values["alarm_action"] = alarm_action
        if insufficient_data_action is not None:
            self._values["insufficient_data_action"] = insufficient_data_action
        if ok_action is not None:
            self._values["ok_action"] = ok_action
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data
        if period is not None:
            self._values["period"] = period
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if alarm_name is not None:
            self._values["alarm_name"] = alarm_name
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluation_periods is not None:
            self._values["evaluation_periods"] = evaluation_periods
        if threshold is not None:
            self._values["threshold"] = threshold

    @builtins.property
    def alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    @builtins.property
    def period(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The period over which the specified statistic is applied.

        :default: Duration.minutes(1)
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        '''The description of the alarm.

        :default:

        - This alarm helps to monitor if the concurrency of the function is approaching the Region-level
        concurrency limit of your account. A function starts to be throttled if it reaches the concurrency limit.
        '''
        result = self._values.get("alarm_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_name(self) -> typing.Optional[builtins.str]:
        '''The alarm name.

        :default: - lambdaFunction.functionName + ' - ConcurrentExecutions'
        '''
        result = self._values.get("alarm_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of data points that must be breaching to trigger the alarm.

        :default: 10
        '''
        result = self._values.get("datapoints_to_alarm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''The number of periods over which data is compared to the specified threshold.

        :default: 10
        '''
        result = self._values.get("evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def threshold(self) -> typing.Optional[jsii.Number]:
        '''The value against which the specified statictis is compared.

        Set the threshold to about 90% of the concurrency quota set
        for the account in the Region. By default, your account has
        a concurrency quota of 1,000 across all functions in a Region.
        However, you can check the quota of your account, as it can
        be increased by contacting AWS support.

        :default: 900
        '''
        result = self._values.get("threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def lambda_function(self) -> _aws_cdk_aws_lambda_ceddda9d.IFunction:
        '''The Lambda function to monitor.'''
        result = self._values.get("lambda_function")
        assert result is not None, "Required property 'lambda_function' is missing"
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.IFunction, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaConcurrentExecutionsAlarmProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaDurationAlarm(
    _aws_cdk_aws_cloudwatch_ceddda9d.Alarm,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.LambdaDurationAlarm",
):
    '''This alarm can detect a long running duration of a Lambda function.

    High runtime duration indicates that
    a function is taking a longer time for invocation, and
    can also impact the concurrency capacity of invocation
    if Lambda is handling a higher number of events. It is
    critical to know if the Lambda function is constantly
    taking longer execution time than expected.

    The alarm is triggered when the duration of the function
    invocations exceeds the specified threshold.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        lambda_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
        threshold: jsii.Number,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param lambda_function: The Lambda function to monitor.
        :param threshold: The value against which the specified statictis is compared. The threshold for the duration depends on your application and workloads and your performance requirements. For high-performance requirements, set the threshold to a shorter time to see if the function is meeting expectations. You can also analyze historical data for duration metrics to see the if the time taken matches the performance expectation of the function, and then set the threshold to a longer time than the historical average. Make sure to set the threshold lower than the configured function timeout.
        :param alarm_description: The description of the alarm. Default: - This alarm detects long duration times for processing an event by a Lambda function. Long durations might be because of changes in function code making the function take longer to execute, or the function's dependencies taking longer.
        :param alarm_name: The alarm name. Default: - lambdaFunction.functionName + ' - Duration'
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 15
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 15
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e14f288432f1c93dade6ca87e081a4cf16901cbcbef6b7c783c411f561140323)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = LambdaDurationAlarmProps(
            lambda_function=lambda_function,
            threshold=threshold,
            alarm_description=alarm_description,
            alarm_name=alarm_name,
            datapoints_to_alarm=datapoints_to_alarm,
            evaluation_periods=evaluation_periods,
            period=period,
            alarm_action=alarm_action,
            insufficient_data_action=insufficient_data_action,
            ok_action=ok_action,
            treat_missing_data=treat_missing_data,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.LambdaDurationAlarmConfig",
    jsii_struct_bases=[LambdaAlarmBaseConfig],
    name_mapping={
        "alarm_action": "alarmAction",
        "insufficient_data_action": "insufficientDataAction",
        "ok_action": "okAction",
        "treat_missing_data": "treatMissingData",
        "period": "period",
        "threshold": "threshold",
        "alarm_description": "alarmDescription",
        "alarm_name": "alarmName",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluation_periods": "evaluationPeriods",
    },
)
class LambdaDurationAlarmConfig(LambdaAlarmBaseConfig):
    def __init__(
        self,
        *,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        threshold: jsii.Number,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Configuration for the Duration alarm.

        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param threshold: The value against which the specified statictis is compared. The threshold for the duration depends on your application and workloads and your performance requirements. For high-performance requirements, set the threshold to a shorter time to see if the function is meeting expectations. You can also analyze historical data for duration metrics to see the if the time taken matches the performance expectation of the function, and then set the threshold to a longer time than the historical average. Make sure to set the threshold lower than the configured function timeout.
        :param alarm_description: The description of the alarm. Default: - This alarm detects long duration times for processing an event by a Lambda function. Long durations might be because of changes in function code making the function take longer to execute, or the function's dependencies taking longer.
        :param alarm_name: The alarm name. Default: - lambdaFunction.functionName + ' - Duration'
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 15
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 15
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16f9aa6367d9f62672010c74b9c77970e9a4ad803a8333d788aa6ea4f74dfb61)
            check_type(argname="argument alarm_action", value=alarm_action, expected_type=type_hints["alarm_action"])
            check_type(argname="argument insufficient_data_action", value=insufficient_data_action, expected_type=type_hints["insufficient_data_action"])
            check_type(argname="argument ok_action", value=ok_action, expected_type=type_hints["ok_action"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument alarm_description", value=alarm_description, expected_type=type_hints["alarm_description"])
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "threshold": threshold,
        }
        if alarm_action is not None:
            self._values["alarm_action"] = alarm_action
        if insufficient_data_action is not None:
            self._values["insufficient_data_action"] = insufficient_data_action
        if ok_action is not None:
            self._values["ok_action"] = ok_action
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data
        if period is not None:
            self._values["period"] = period
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if alarm_name is not None:
            self._values["alarm_name"] = alarm_name
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluation_periods is not None:
            self._values["evaluation_periods"] = evaluation_periods

    @builtins.property
    def alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    @builtins.property
    def period(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The period over which the specified statistic is applied.

        :default: Duration.minutes(1)
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def threshold(self) -> jsii.Number:
        '''The value against which the specified statictis is compared.

        The threshold for the duration depends on your application
        and workloads and your performance requirements. For
        high-performance requirements, set the threshold to a
        shorter time to see if the function is meeting expectations.
        You can also analyze historical data for duration metrics
        to see the if the time taken matches the performance
        expectation of the function, and then set the threshold to
        a longer time than the historical average. Make sure to
        set the threshold lower than the configured function
        timeout.
        '''
        result = self._values.get("threshold")
        assert result is not None, "Required property 'threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        '''The description of the alarm.

        :default: - This alarm detects long duration times for processing an event by a Lambda function. Long durations might be because of changes in function code making the function take longer to execute, or the function's dependencies taking longer.
        '''
        result = self._values.get("alarm_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_name(self) -> typing.Optional[builtins.str]:
        '''The alarm name.

        :default: - lambdaFunction.functionName + ' - Duration'
        '''
        result = self._values.get("alarm_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of data points that must be breaching to trigger the alarm.

        :default: 15
        '''
        result = self._values.get("datapoints_to_alarm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''The number of periods over which data is compared to the specified threshold.

        :default: 15
        '''
        result = self._values.get("evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaDurationAlarmConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.LambdaDurationAlarmProps",
    jsii_struct_bases=[LambdaDurationAlarmConfig],
    name_mapping={
        "alarm_action": "alarmAction",
        "insufficient_data_action": "insufficientDataAction",
        "ok_action": "okAction",
        "treat_missing_data": "treatMissingData",
        "period": "period",
        "threshold": "threshold",
        "alarm_description": "alarmDescription",
        "alarm_name": "alarmName",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluation_periods": "evaluationPeriods",
        "lambda_function": "lambdaFunction",
    },
)
class LambdaDurationAlarmProps(LambdaDurationAlarmConfig):
    def __init__(
        self,
        *,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        threshold: jsii.Number,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        lambda_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
    ) -> None:
        '''The properties for the LambdaDurationAlarm construct.

        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param threshold: The value against which the specified statictis is compared. The threshold for the duration depends on your application and workloads and your performance requirements. For high-performance requirements, set the threshold to a shorter time to see if the function is meeting expectations. You can also analyze historical data for duration metrics to see the if the time taken matches the performance expectation of the function, and then set the threshold to a longer time than the historical average. Make sure to set the threshold lower than the configured function timeout.
        :param alarm_description: The description of the alarm. Default: - This alarm detects long duration times for processing an event by a Lambda function. Long durations might be because of changes in function code making the function take longer to execute, or the function's dependencies taking longer.
        :param alarm_name: The alarm name. Default: - lambdaFunction.functionName + ' - Duration'
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 15
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 15
        :param lambda_function: The Lambda function to monitor.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c35e2842ae53ffd154b79e7db69c642434d4bb574cd771ed7bdc184108099771)
            check_type(argname="argument alarm_action", value=alarm_action, expected_type=type_hints["alarm_action"])
            check_type(argname="argument insufficient_data_action", value=insufficient_data_action, expected_type=type_hints["insufficient_data_action"])
            check_type(argname="argument ok_action", value=ok_action, expected_type=type_hints["ok_action"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument alarm_description", value=alarm_description, expected_type=type_hints["alarm_description"])
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument lambda_function", value=lambda_function, expected_type=type_hints["lambda_function"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "threshold": threshold,
            "lambda_function": lambda_function,
        }
        if alarm_action is not None:
            self._values["alarm_action"] = alarm_action
        if insufficient_data_action is not None:
            self._values["insufficient_data_action"] = insufficient_data_action
        if ok_action is not None:
            self._values["ok_action"] = ok_action
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data
        if period is not None:
            self._values["period"] = period
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if alarm_name is not None:
            self._values["alarm_name"] = alarm_name
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluation_periods is not None:
            self._values["evaluation_periods"] = evaluation_periods

    @builtins.property
    def alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    @builtins.property
    def period(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The period over which the specified statistic is applied.

        :default: Duration.minutes(1)
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def threshold(self) -> jsii.Number:
        '''The value against which the specified statictis is compared.

        The threshold for the duration depends on your application
        and workloads and your performance requirements. For
        high-performance requirements, set the threshold to a
        shorter time to see if the function is meeting expectations.
        You can also analyze historical data for duration metrics
        to see the if the time taken matches the performance
        expectation of the function, and then set the threshold to
        a longer time than the historical average. Make sure to
        set the threshold lower than the configured function
        timeout.
        '''
        result = self._values.get("threshold")
        assert result is not None, "Required property 'threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        '''The description of the alarm.

        :default: - This alarm detects long duration times for processing an event by a Lambda function. Long durations might be because of changes in function code making the function take longer to execute, or the function's dependencies taking longer.
        '''
        result = self._values.get("alarm_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_name(self) -> typing.Optional[builtins.str]:
        '''The alarm name.

        :default: - lambdaFunction.functionName + ' - Duration'
        '''
        result = self._values.get("alarm_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of data points that must be breaching to trigger the alarm.

        :default: 15
        '''
        result = self._values.get("datapoints_to_alarm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''The number of periods over which data is compared to the specified threshold.

        :default: 15
        '''
        result = self._values.get("evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def lambda_function(self) -> _aws_cdk_aws_lambda_ceddda9d.IFunction:
        '''The Lambda function to monitor.'''
        result = self._values.get("lambda_function")
        assert result is not None, "Required property 'lambda_function' is missing"
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.IFunction, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaDurationAlarmProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaErrorsAlarm(
    _aws_cdk_aws_cloudwatch_ceddda9d.Alarm,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.LambdaErrorsAlarm",
):
    '''The alarm helps detect high error counts in function invocations.

    The alarm is triggered when the number of errors exceeds the specified
    threshold.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        lambda_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
        threshold: jsii.Number,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param lambda_function: The Lambda function to monitor.
        :param threshold: The value against which the specified statictis is compared. Set the threshold to a number greater than zero. The exact value can depend on the tolerance for errors in your application. Understand the criticality of the invocations that the function is handling. For some applications, any error might be unacceptable, while other applications might allow for a certain margin of error.
        :param alarm_description: The description of the alarm. Default: - This alarm detects high error counts. Errors includes the exceptions thrown by the code as well as exceptions thrown by the Lambda runtime. You can check the logs related to the function to diagnose the issue.
        :param alarm_name: The alarm name. Default: - lambdaFunction.functionName + ' - Errors'
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 3
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 3
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f5d57bf581f2eea2bb19216346016a8105d14c7a16a9ac673410b280a87fc3a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = LambdaErrorsAlarmProps(
            lambda_function=lambda_function,
            threshold=threshold,
            alarm_description=alarm_description,
            alarm_name=alarm_name,
            datapoints_to_alarm=datapoints_to_alarm,
            evaluation_periods=evaluation_periods,
            period=period,
            alarm_action=alarm_action,
            insufficient_data_action=insufficient_data_action,
            ok_action=ok_action,
            treat_missing_data=treat_missing_data,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.LambdaErrorsAlarmConfig",
    jsii_struct_bases=[LambdaAlarmBaseConfig],
    name_mapping={
        "alarm_action": "alarmAction",
        "insufficient_data_action": "insufficientDataAction",
        "ok_action": "okAction",
        "treat_missing_data": "treatMissingData",
        "period": "period",
        "threshold": "threshold",
        "alarm_description": "alarmDescription",
        "alarm_name": "alarmName",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluation_periods": "evaluationPeriods",
    },
)
class LambdaErrorsAlarmConfig(LambdaAlarmBaseConfig):
    def __init__(
        self,
        *,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        threshold: jsii.Number,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Configuration for the Errors alarm.

        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param threshold: The value against which the specified statictis is compared. Set the threshold to a number greater than zero. The exact value can depend on the tolerance for errors in your application. Understand the criticality of the invocations that the function is handling. For some applications, any error might be unacceptable, while other applications might allow for a certain margin of error.
        :param alarm_description: The description of the alarm. Default: - This alarm detects high error counts. Errors includes the exceptions thrown by the code as well as exceptions thrown by the Lambda runtime. You can check the logs related to the function to diagnose the issue.
        :param alarm_name: The alarm name. Default: - lambdaFunction.functionName + ' - Errors'
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 3
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 3
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a80f94cd00993ff5508c02a09a080a5e3dfe40d123f162a15591a81b8faf940)
            check_type(argname="argument alarm_action", value=alarm_action, expected_type=type_hints["alarm_action"])
            check_type(argname="argument insufficient_data_action", value=insufficient_data_action, expected_type=type_hints["insufficient_data_action"])
            check_type(argname="argument ok_action", value=ok_action, expected_type=type_hints["ok_action"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument alarm_description", value=alarm_description, expected_type=type_hints["alarm_description"])
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "threshold": threshold,
        }
        if alarm_action is not None:
            self._values["alarm_action"] = alarm_action
        if insufficient_data_action is not None:
            self._values["insufficient_data_action"] = insufficient_data_action
        if ok_action is not None:
            self._values["ok_action"] = ok_action
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data
        if period is not None:
            self._values["period"] = period
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if alarm_name is not None:
            self._values["alarm_name"] = alarm_name
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluation_periods is not None:
            self._values["evaluation_periods"] = evaluation_periods

    @builtins.property
    def alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    @builtins.property
    def period(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The period over which the specified statistic is applied.

        :default: Duration.minutes(1)
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def threshold(self) -> jsii.Number:
        '''The value against which the specified statictis is compared.

        Set the threshold to a number greater than zero. The exact
        value can depend on the tolerance for errors in your
        application. Understand the criticality of the invocations
        that the function is handling. For some applications, any
        error might be unacceptable, while other applications might
        allow for a certain margin of error.
        '''
        result = self._values.get("threshold")
        assert result is not None, "Required property 'threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        '''The description of the alarm.

        :default:

        - This alarm detects high error counts. Errors includes the exceptions thrown by the code
        as well as exceptions thrown by the Lambda runtime. You can check the logs related to the function
        to diagnose the issue.
        '''
        result = self._values.get("alarm_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_name(self) -> typing.Optional[builtins.str]:
        '''The alarm name.

        :default: - lambdaFunction.functionName + ' - Errors'
        '''
        result = self._values.get("alarm_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of data points that must be breaching to trigger the alarm.

        :default: 3
        '''
        result = self._values.get("datapoints_to_alarm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''The number of periods over which data is compared to the specified threshold.

        :default: 3
        '''
        result = self._values.get("evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaErrorsAlarmConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.LambdaErrorsAlarmProps",
    jsii_struct_bases=[LambdaErrorsAlarmConfig],
    name_mapping={
        "alarm_action": "alarmAction",
        "insufficient_data_action": "insufficientDataAction",
        "ok_action": "okAction",
        "treat_missing_data": "treatMissingData",
        "period": "period",
        "threshold": "threshold",
        "alarm_description": "alarmDescription",
        "alarm_name": "alarmName",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluation_periods": "evaluationPeriods",
        "lambda_function": "lambdaFunction",
    },
)
class LambdaErrorsAlarmProps(LambdaErrorsAlarmConfig):
    def __init__(
        self,
        *,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        threshold: jsii.Number,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        lambda_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
    ) -> None:
        '''The properties for the LambdaErrorsAlarm construct.

        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param threshold: The value against which the specified statictis is compared. Set the threshold to a number greater than zero. The exact value can depend on the tolerance for errors in your application. Understand the criticality of the invocations that the function is handling. For some applications, any error might be unacceptable, while other applications might allow for a certain margin of error.
        :param alarm_description: The description of the alarm. Default: - This alarm detects high error counts. Errors includes the exceptions thrown by the code as well as exceptions thrown by the Lambda runtime. You can check the logs related to the function to diagnose the issue.
        :param alarm_name: The alarm name. Default: - lambdaFunction.functionName + ' - Errors'
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 3
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 3
        :param lambda_function: The Lambda function to monitor.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__065075f4736ec308df17eee0d6a5100064d7a899d094aeb4533fdde663ffc607)
            check_type(argname="argument alarm_action", value=alarm_action, expected_type=type_hints["alarm_action"])
            check_type(argname="argument insufficient_data_action", value=insufficient_data_action, expected_type=type_hints["insufficient_data_action"])
            check_type(argname="argument ok_action", value=ok_action, expected_type=type_hints["ok_action"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument alarm_description", value=alarm_description, expected_type=type_hints["alarm_description"])
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument lambda_function", value=lambda_function, expected_type=type_hints["lambda_function"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "threshold": threshold,
            "lambda_function": lambda_function,
        }
        if alarm_action is not None:
            self._values["alarm_action"] = alarm_action
        if insufficient_data_action is not None:
            self._values["insufficient_data_action"] = insufficient_data_action
        if ok_action is not None:
            self._values["ok_action"] = ok_action
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data
        if period is not None:
            self._values["period"] = period
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if alarm_name is not None:
            self._values["alarm_name"] = alarm_name
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluation_periods is not None:
            self._values["evaluation_periods"] = evaluation_periods

    @builtins.property
    def alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    @builtins.property
    def period(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The period over which the specified statistic is applied.

        :default: Duration.minutes(1)
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def threshold(self) -> jsii.Number:
        '''The value against which the specified statictis is compared.

        Set the threshold to a number greater than zero. The exact
        value can depend on the tolerance for errors in your
        application. Understand the criticality of the invocations
        that the function is handling. For some applications, any
        error might be unacceptable, while other applications might
        allow for a certain margin of error.
        '''
        result = self._values.get("threshold")
        assert result is not None, "Required property 'threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        '''The description of the alarm.

        :default:

        - This alarm detects high error counts. Errors includes the exceptions thrown by the code
        as well as exceptions thrown by the Lambda runtime. You can check the logs related to the function
        to diagnose the issue.
        '''
        result = self._values.get("alarm_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_name(self) -> typing.Optional[builtins.str]:
        '''The alarm name.

        :default: - lambdaFunction.functionName + ' - Errors'
        '''
        result = self._values.get("alarm_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of data points that must be breaching to trigger the alarm.

        :default: 3
        '''
        result = self._values.get("datapoints_to_alarm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''The number of periods over which data is compared to the specified threshold.

        :default: 3
        '''
        result = self._values.get("evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def lambda_function(self) -> _aws_cdk_aws_lambda_ceddda9d.IFunction:
        '''The Lambda function to monitor.'''
        result = self._values.get("lambda_function")
        assert result is not None, "Required property 'lambda_function' is missing"
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.IFunction, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaErrorsAlarmProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaRecommendedAlarms(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.LambdaRecommendedAlarms",
):
    '''A construct that creates recommended alarms for a Lambda function.

    :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Best_Practice_Recommended_Alarms_AWS_Services.html#Lambda
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        lambda_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
        config_duration_alarm: typing.Union[LambdaDurationAlarmConfig, typing.Dict[builtins.str, typing.Any]],
        config_errors_alarm: typing.Union[LambdaErrorsAlarmConfig, typing.Dict[builtins.str, typing.Any]],
        config_throttles_alarm: typing.Union["LambdaThrottlesAlarmConfig", typing.Dict[builtins.str, typing.Any]],
        config_concurrent_executions_alarm: typing.Optional[typing.Union[LambdaConcurrentExecutionsAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        default_alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        default_insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        default_ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        exclude_alarms: typing.Optional[typing.Sequence["LambdaRecommendedAlarmsMetrics"]] = None,
        exclude_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param lambda_function: The lambda function to apply the recommended alarms.
        :param config_duration_alarm: The configuration for the Duration alarm.
        :param config_errors_alarm: The configuration for the Errors alarm.
        :param config_throttles_alarm: The configuration for the Throttles alarm.
        :param config_concurrent_executions_alarm: The configuration for the ConcurrentExecutions alarm.
        :param default_alarm_action: The default action to take when an alarm is triggered. Default: - None
        :param default_insufficient_data_action: The default action to take when an alarm has insufficient data. Default: - None
        :param default_ok_action: The default action to take when an alarm enters the ok state. Default: - None
        :param exclude_alarms: Alarm metrics to exclude from the recommended alarms. Default: - None
        :param exclude_resources: The resources to exclude from the recommended alarms. Use a resources id to exclude a specific resource.
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27101909e8d5207062982ebba2ceaa835aa71fc168b8d767b66d1a5c1a11d99b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = LambdaRecommendedAlarmsProps(
            lambda_function=lambda_function,
            config_duration_alarm=config_duration_alarm,
            config_errors_alarm=config_errors_alarm,
            config_throttles_alarm=config_throttles_alarm,
            config_concurrent_executions_alarm=config_concurrent_executions_alarm,
            default_alarm_action=default_alarm_action,
            default_insufficient_data_action=default_insufficient_data_action,
            default_ok_action=default_ok_action,
            exclude_alarms=exclude_alarms,
            exclude_resources=exclude_resources,
            treat_missing_data=treat_missing_data,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="alarmConcurrentExecutions")
    def alarm_concurrent_executions(
        self,
    ) -> typing.Optional[LambdaConcurrentExecutionsAlarm]:
        '''The concurrent executions alarm for the Lambda function.'''
        return typing.cast(typing.Optional[LambdaConcurrentExecutionsAlarm], jsii.get(self, "alarmConcurrentExecutions"))

    @builtins.property
    @jsii.member(jsii_name="alarmDuration")
    def alarm_duration(self) -> typing.Optional[LambdaDurationAlarm]:
        '''The duration alarm for the Lambda function.'''
        return typing.cast(typing.Optional[LambdaDurationAlarm], jsii.get(self, "alarmDuration"))

    @builtins.property
    @jsii.member(jsii_name="alarmErrors")
    def alarm_errors(self) -> typing.Optional[LambdaErrorsAlarm]:
        '''The error alarm for the Lambda function.'''
        return typing.cast(typing.Optional[LambdaErrorsAlarm], jsii.get(self, "alarmErrors"))

    @builtins.property
    @jsii.member(jsii_name="alarmThrottles")
    def alarm_throttles(self) -> typing.Optional["LambdaThrottlesAlarm"]:
        '''The throttles alarm for the Lambda function.'''
        return typing.cast(typing.Optional["LambdaThrottlesAlarm"], jsii.get(self, "alarmThrottles"))


@jsii.implements(_aws_cdk_ceddda9d.IAspect)
class LambdaRecommendedAlarmsAspect(
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.LambdaRecommendedAlarmsAspect",
):
    '''An aspect that applies recommended alarms for Lambda functions.

    :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Best_Practice_Recommended_Alarms_AWS_Services.html#Lambda
    '''

    def __init__(
        self,
        *,
        config_duration_alarm: typing.Union[LambdaDurationAlarmConfig, typing.Dict[builtins.str, typing.Any]],
        config_errors_alarm: typing.Union[LambdaErrorsAlarmConfig, typing.Dict[builtins.str, typing.Any]],
        config_throttles_alarm: typing.Union["LambdaThrottlesAlarmConfig", typing.Dict[builtins.str, typing.Any]],
        config_concurrent_executions_alarm: typing.Optional[typing.Union[LambdaConcurrentExecutionsAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        default_alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        default_insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        default_ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        exclude_alarms: typing.Optional[typing.Sequence["LambdaRecommendedAlarmsMetrics"]] = None,
        exclude_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> None:
        '''
        :param config_duration_alarm: The configuration for the Duration alarm.
        :param config_errors_alarm: The configuration for the Errors alarm.
        :param config_throttles_alarm: The configuration for the Throttles alarm.
        :param config_concurrent_executions_alarm: The configuration for the ConcurrentExecutions alarm.
        :param default_alarm_action: The default action to take when an alarm is triggered. Default: - None
        :param default_insufficient_data_action: The default action to take when an alarm has insufficient data. Default: - None
        :param default_ok_action: The default action to take when an alarm enters the ok state. Default: - None
        :param exclude_alarms: Alarm metrics to exclude from the recommended alarms. Default: - None
        :param exclude_resources: The resources to exclude from the recommended alarms. Use a resources id to exclude a specific resource.
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        props = LambdaRecommendedAlarmsConfig(
            config_duration_alarm=config_duration_alarm,
            config_errors_alarm=config_errors_alarm,
            config_throttles_alarm=config_throttles_alarm,
            config_concurrent_executions_alarm=config_concurrent_executions_alarm,
            default_alarm_action=default_alarm_action,
            default_insufficient_data_action=default_insufficient_data_action,
            default_ok_action=default_ok_action,
            exclude_alarms=exclude_alarms,
            exclude_resources=exclude_resources,
            treat_missing_data=treat_missing_data,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="visit")
    def visit(self, node: _constructs_77d1e7e8.IConstruct) -> None:
        '''All aspects can visit an IConstruct.

        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ac98314bcd4923aabdf6919cacbc99fe09b02e5eba9973007f013c04c677d9e)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "visit", [node]))


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.LambdaRecommendedAlarmsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "config_duration_alarm": "configDurationAlarm",
        "config_errors_alarm": "configErrorsAlarm",
        "config_throttles_alarm": "configThrottlesAlarm",
        "config_concurrent_executions_alarm": "configConcurrentExecutionsAlarm",
        "default_alarm_action": "defaultAlarmAction",
        "default_insufficient_data_action": "defaultInsufficientDataAction",
        "default_ok_action": "defaultOkAction",
        "exclude_alarms": "excludeAlarms",
        "exclude_resources": "excludeResources",
        "treat_missing_data": "treatMissingData",
    },
)
class LambdaRecommendedAlarmsConfig:
    def __init__(
        self,
        *,
        config_duration_alarm: typing.Union[LambdaDurationAlarmConfig, typing.Dict[builtins.str, typing.Any]],
        config_errors_alarm: typing.Union[LambdaErrorsAlarmConfig, typing.Dict[builtins.str, typing.Any]],
        config_throttles_alarm: typing.Union["LambdaThrottlesAlarmConfig", typing.Dict[builtins.str, typing.Any]],
        config_concurrent_executions_alarm: typing.Optional[typing.Union[LambdaConcurrentExecutionsAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        default_alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        default_insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        default_ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        exclude_alarms: typing.Optional[typing.Sequence["LambdaRecommendedAlarmsMetrics"]] = None,
        exclude_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> None:
        '''Configuration for Lambda recommended alarms.

        Default actions are overridden by the actions specified in the
        individual alarm configurations.

        :param config_duration_alarm: The configuration for the Duration alarm.
        :param config_errors_alarm: The configuration for the Errors alarm.
        :param config_throttles_alarm: The configuration for the Throttles alarm.
        :param config_concurrent_executions_alarm: The configuration for the ConcurrentExecutions alarm.
        :param default_alarm_action: The default action to take when an alarm is triggered. Default: - None
        :param default_insufficient_data_action: The default action to take when an alarm has insufficient data. Default: - None
        :param default_ok_action: The default action to take when an alarm enters the ok state. Default: - None
        :param exclude_alarms: Alarm metrics to exclude from the recommended alarms. Default: - None
        :param exclude_resources: The resources to exclude from the recommended alarms. Use a resources id to exclude a specific resource.
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        if isinstance(config_duration_alarm, dict):
            config_duration_alarm = LambdaDurationAlarmConfig(**config_duration_alarm)
        if isinstance(config_errors_alarm, dict):
            config_errors_alarm = LambdaErrorsAlarmConfig(**config_errors_alarm)
        if isinstance(config_throttles_alarm, dict):
            config_throttles_alarm = LambdaThrottlesAlarmConfig(**config_throttles_alarm)
        if isinstance(config_concurrent_executions_alarm, dict):
            config_concurrent_executions_alarm = LambdaConcurrentExecutionsAlarmConfig(**config_concurrent_executions_alarm)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cd52c68a63a1358db1966d2a14b5e03f18458ff71753842a0c469174dd15066)
            check_type(argname="argument config_duration_alarm", value=config_duration_alarm, expected_type=type_hints["config_duration_alarm"])
            check_type(argname="argument config_errors_alarm", value=config_errors_alarm, expected_type=type_hints["config_errors_alarm"])
            check_type(argname="argument config_throttles_alarm", value=config_throttles_alarm, expected_type=type_hints["config_throttles_alarm"])
            check_type(argname="argument config_concurrent_executions_alarm", value=config_concurrent_executions_alarm, expected_type=type_hints["config_concurrent_executions_alarm"])
            check_type(argname="argument default_alarm_action", value=default_alarm_action, expected_type=type_hints["default_alarm_action"])
            check_type(argname="argument default_insufficient_data_action", value=default_insufficient_data_action, expected_type=type_hints["default_insufficient_data_action"])
            check_type(argname="argument default_ok_action", value=default_ok_action, expected_type=type_hints["default_ok_action"])
            check_type(argname="argument exclude_alarms", value=exclude_alarms, expected_type=type_hints["exclude_alarms"])
            check_type(argname="argument exclude_resources", value=exclude_resources, expected_type=type_hints["exclude_resources"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "config_duration_alarm": config_duration_alarm,
            "config_errors_alarm": config_errors_alarm,
            "config_throttles_alarm": config_throttles_alarm,
        }
        if config_concurrent_executions_alarm is not None:
            self._values["config_concurrent_executions_alarm"] = config_concurrent_executions_alarm
        if default_alarm_action is not None:
            self._values["default_alarm_action"] = default_alarm_action
        if default_insufficient_data_action is not None:
            self._values["default_insufficient_data_action"] = default_insufficient_data_action
        if default_ok_action is not None:
            self._values["default_ok_action"] = default_ok_action
        if exclude_alarms is not None:
            self._values["exclude_alarms"] = exclude_alarms
        if exclude_resources is not None:
            self._values["exclude_resources"] = exclude_resources
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data

    @builtins.property
    def config_duration_alarm(self) -> LambdaDurationAlarmConfig:
        '''The configuration for the Duration alarm.'''
        result = self._values.get("config_duration_alarm")
        assert result is not None, "Required property 'config_duration_alarm' is missing"
        return typing.cast(LambdaDurationAlarmConfig, result)

    @builtins.property
    def config_errors_alarm(self) -> LambdaErrorsAlarmConfig:
        '''The configuration for the Errors alarm.'''
        result = self._values.get("config_errors_alarm")
        assert result is not None, "Required property 'config_errors_alarm' is missing"
        return typing.cast(LambdaErrorsAlarmConfig, result)

    @builtins.property
    def config_throttles_alarm(self) -> "LambdaThrottlesAlarmConfig":
        '''The configuration for the Throttles alarm.'''
        result = self._values.get("config_throttles_alarm")
        assert result is not None, "Required property 'config_throttles_alarm' is missing"
        return typing.cast("LambdaThrottlesAlarmConfig", result)

    @builtins.property
    def config_concurrent_executions_alarm(
        self,
    ) -> typing.Optional[LambdaConcurrentExecutionsAlarmConfig]:
        '''The configuration for the ConcurrentExecutions alarm.'''
        result = self._values.get("config_concurrent_executions_alarm")
        return typing.cast(typing.Optional[LambdaConcurrentExecutionsAlarmConfig], result)

    @builtins.property
    def default_alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The default action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("default_alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def default_insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The default action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("default_insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def default_ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The default action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("default_ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def exclude_alarms(
        self,
    ) -> typing.Optional[typing.List["LambdaRecommendedAlarmsMetrics"]]:
        '''Alarm metrics to exclude from the recommended alarms.

        :default: - None
        '''
        result = self._values.get("exclude_alarms")
        return typing.cast(typing.Optional[typing.List["LambdaRecommendedAlarmsMetrics"]], result)

    @builtins.property
    def exclude_resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The resources to exclude from the recommended alarms.

        Use a resources id to exclude a specific resource.
        '''
        result = self._values.get("exclude_resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaRecommendedAlarmsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.LambdaRecommendedAlarmsMetrics"
)
class LambdaRecommendedAlarmsMetrics(enum.Enum):
    '''The recommended metrics for Lambda alarms.'''

    ERRORS = "ERRORS"
    '''Errors include the exceptions thrown by the code as well as exceptions thrown by the Lambda runtime.'''
    THROTTLES = "THROTTLES"
    '''Throttles occur when there is no concurrency available for scale up.'''
    DURATION = "DURATION"
    '''Duration is the time taken for the function to process an event.'''
    CONCURRENT_EXECUTIONS = "CONCURRENT_EXECUTIONS"
    '''ConcurrentExecutions is the number of concurrent executions of the function.'''


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.LambdaRecommendedAlarmsProps",
    jsii_struct_bases=[LambdaRecommendedAlarmsConfig],
    name_mapping={
        "config_duration_alarm": "configDurationAlarm",
        "config_errors_alarm": "configErrorsAlarm",
        "config_throttles_alarm": "configThrottlesAlarm",
        "config_concurrent_executions_alarm": "configConcurrentExecutionsAlarm",
        "default_alarm_action": "defaultAlarmAction",
        "default_insufficient_data_action": "defaultInsufficientDataAction",
        "default_ok_action": "defaultOkAction",
        "exclude_alarms": "excludeAlarms",
        "exclude_resources": "excludeResources",
        "treat_missing_data": "treatMissingData",
        "lambda_function": "lambdaFunction",
    },
)
class LambdaRecommendedAlarmsProps(LambdaRecommendedAlarmsConfig):
    def __init__(
        self,
        *,
        config_duration_alarm: typing.Union[LambdaDurationAlarmConfig, typing.Dict[builtins.str, typing.Any]],
        config_errors_alarm: typing.Union[LambdaErrorsAlarmConfig, typing.Dict[builtins.str, typing.Any]],
        config_throttles_alarm: typing.Union["LambdaThrottlesAlarmConfig", typing.Dict[builtins.str, typing.Any]],
        config_concurrent_executions_alarm: typing.Optional[typing.Union[LambdaConcurrentExecutionsAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        default_alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        default_insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        default_ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        exclude_alarms: typing.Optional[typing.Sequence[LambdaRecommendedAlarmsMetrics]] = None,
        exclude_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
        lambda_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
    ) -> None:
        '''
        :param config_duration_alarm: The configuration for the Duration alarm.
        :param config_errors_alarm: The configuration for the Errors alarm.
        :param config_throttles_alarm: The configuration for the Throttles alarm.
        :param config_concurrent_executions_alarm: The configuration for the ConcurrentExecutions alarm.
        :param default_alarm_action: The default action to take when an alarm is triggered. Default: - None
        :param default_insufficient_data_action: The default action to take when an alarm has insufficient data. Default: - None
        :param default_ok_action: The default action to take when an alarm enters the ok state. Default: - None
        :param exclude_alarms: Alarm metrics to exclude from the recommended alarms. Default: - None
        :param exclude_resources: The resources to exclude from the recommended alarms. Use a resources id to exclude a specific resource.
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        :param lambda_function: The lambda function to apply the recommended alarms.
        '''
        if isinstance(config_duration_alarm, dict):
            config_duration_alarm = LambdaDurationAlarmConfig(**config_duration_alarm)
        if isinstance(config_errors_alarm, dict):
            config_errors_alarm = LambdaErrorsAlarmConfig(**config_errors_alarm)
        if isinstance(config_throttles_alarm, dict):
            config_throttles_alarm = LambdaThrottlesAlarmConfig(**config_throttles_alarm)
        if isinstance(config_concurrent_executions_alarm, dict):
            config_concurrent_executions_alarm = LambdaConcurrentExecutionsAlarmConfig(**config_concurrent_executions_alarm)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2028de2c7bc54f62581b4499458b79fb36fb2c32306e074814ca31178c7a120)
            check_type(argname="argument config_duration_alarm", value=config_duration_alarm, expected_type=type_hints["config_duration_alarm"])
            check_type(argname="argument config_errors_alarm", value=config_errors_alarm, expected_type=type_hints["config_errors_alarm"])
            check_type(argname="argument config_throttles_alarm", value=config_throttles_alarm, expected_type=type_hints["config_throttles_alarm"])
            check_type(argname="argument config_concurrent_executions_alarm", value=config_concurrent_executions_alarm, expected_type=type_hints["config_concurrent_executions_alarm"])
            check_type(argname="argument default_alarm_action", value=default_alarm_action, expected_type=type_hints["default_alarm_action"])
            check_type(argname="argument default_insufficient_data_action", value=default_insufficient_data_action, expected_type=type_hints["default_insufficient_data_action"])
            check_type(argname="argument default_ok_action", value=default_ok_action, expected_type=type_hints["default_ok_action"])
            check_type(argname="argument exclude_alarms", value=exclude_alarms, expected_type=type_hints["exclude_alarms"])
            check_type(argname="argument exclude_resources", value=exclude_resources, expected_type=type_hints["exclude_resources"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
            check_type(argname="argument lambda_function", value=lambda_function, expected_type=type_hints["lambda_function"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "config_duration_alarm": config_duration_alarm,
            "config_errors_alarm": config_errors_alarm,
            "config_throttles_alarm": config_throttles_alarm,
            "lambda_function": lambda_function,
        }
        if config_concurrent_executions_alarm is not None:
            self._values["config_concurrent_executions_alarm"] = config_concurrent_executions_alarm
        if default_alarm_action is not None:
            self._values["default_alarm_action"] = default_alarm_action
        if default_insufficient_data_action is not None:
            self._values["default_insufficient_data_action"] = default_insufficient_data_action
        if default_ok_action is not None:
            self._values["default_ok_action"] = default_ok_action
        if exclude_alarms is not None:
            self._values["exclude_alarms"] = exclude_alarms
        if exclude_resources is not None:
            self._values["exclude_resources"] = exclude_resources
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data

    @builtins.property
    def config_duration_alarm(self) -> LambdaDurationAlarmConfig:
        '''The configuration for the Duration alarm.'''
        result = self._values.get("config_duration_alarm")
        assert result is not None, "Required property 'config_duration_alarm' is missing"
        return typing.cast(LambdaDurationAlarmConfig, result)

    @builtins.property
    def config_errors_alarm(self) -> LambdaErrorsAlarmConfig:
        '''The configuration for the Errors alarm.'''
        result = self._values.get("config_errors_alarm")
        assert result is not None, "Required property 'config_errors_alarm' is missing"
        return typing.cast(LambdaErrorsAlarmConfig, result)

    @builtins.property
    def config_throttles_alarm(self) -> "LambdaThrottlesAlarmConfig":
        '''The configuration for the Throttles alarm.'''
        result = self._values.get("config_throttles_alarm")
        assert result is not None, "Required property 'config_throttles_alarm' is missing"
        return typing.cast("LambdaThrottlesAlarmConfig", result)

    @builtins.property
    def config_concurrent_executions_alarm(
        self,
    ) -> typing.Optional[LambdaConcurrentExecutionsAlarmConfig]:
        '''The configuration for the ConcurrentExecutions alarm.'''
        result = self._values.get("config_concurrent_executions_alarm")
        return typing.cast(typing.Optional[LambdaConcurrentExecutionsAlarmConfig], result)

    @builtins.property
    def default_alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The default action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("default_alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def default_insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The default action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("default_insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def default_ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The default action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("default_ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def exclude_alarms(
        self,
    ) -> typing.Optional[typing.List[LambdaRecommendedAlarmsMetrics]]:
        '''Alarm metrics to exclude from the recommended alarms.

        :default: - None
        '''
        result = self._values.get("exclude_alarms")
        return typing.cast(typing.Optional[typing.List[LambdaRecommendedAlarmsMetrics]], result)

    @builtins.property
    def exclude_resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The resources to exclude from the recommended alarms.

        Use a resources id to exclude a specific resource.
        '''
        result = self._values.get("exclude_resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    @builtins.property
    def lambda_function(self) -> _aws_cdk_aws_lambda_ceddda9d.IFunction:
        '''The lambda function to apply the recommended alarms.'''
        result = self._values.get("lambda_function")
        assert result is not None, "Required property 'lambda_function' is missing"
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.IFunction, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaRecommendedAlarmsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaThrottlesAlarm(
    _aws_cdk_aws_cloudwatch_ceddda9d.Alarm,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.LambdaThrottlesAlarm",
):
    '''The alarm helps detect a high number of throttled invocation requests for a Lambda function.

    It is important to know if requests are constantly
    getting rejected due to throttling and if you need to improve Lambda
    function performance or increase concurrency capacity to avoid constant
    throttling.

    The alarm is triggered when the number of throttles exceeds or equals
    the specified threshold.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        lambda_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
        threshold: jsii.Number,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param lambda_function: The Lambda function to monitor.
        :param threshold: The value against which the specified statictis is compared. Set the threshold to a number greater than zero. The exact value of the threshold can depend on the tolerance of the application. Set the threshold according to its usage and scaling requirements of the function.
        :param alarm_description: The description of the alarm. Default: - This alarm detects a high number of throttled invocation requests. Throttling occurs when there is no concurrency is available for scale up. There are several approaches to resolve this issue. 1. Request a concurrency increase from AWS Support in this Region. 2) Identify performance issues in the function to improve the speed of processing and therefore improve throughput. 3) Increase the batch size of the function, so that more messages are processed by each function invocation.
        :param alarm_name: The alarm name. Default: - lambdaFunction.functionName + ' - Throttles'
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 5
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 5
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__488351c06ad0ced06f68b654c629b883306654b7e2b923062e130cd249a4ad16)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = LambdaThrottlesAlarmProps(
            lambda_function=lambda_function,
            threshold=threshold,
            alarm_description=alarm_description,
            alarm_name=alarm_name,
            datapoints_to_alarm=datapoints_to_alarm,
            evaluation_periods=evaluation_periods,
            period=period,
            alarm_action=alarm_action,
            insufficient_data_action=insufficient_data_action,
            ok_action=ok_action,
            treat_missing_data=treat_missing_data,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.LambdaThrottlesAlarmConfig",
    jsii_struct_bases=[LambdaAlarmBaseConfig],
    name_mapping={
        "alarm_action": "alarmAction",
        "insufficient_data_action": "insufficientDataAction",
        "ok_action": "okAction",
        "treat_missing_data": "treatMissingData",
        "period": "period",
        "threshold": "threshold",
        "alarm_description": "alarmDescription",
        "alarm_name": "alarmName",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluation_periods": "evaluationPeriods",
    },
)
class LambdaThrottlesAlarmConfig(LambdaAlarmBaseConfig):
    def __init__(
        self,
        *,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        threshold: jsii.Number,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Configuration for the Throttles alarm.

        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param threshold: The value against which the specified statictis is compared. Set the threshold to a number greater than zero. The exact value of the threshold can depend on the tolerance of the application. Set the threshold according to its usage and scaling requirements of the function.
        :param alarm_description: The description of the alarm. Default: - This alarm detects a high number of throttled invocation requests. Throttling occurs when there is no concurrency is available for scale up. There are several approaches to resolve this issue. 1. Request a concurrency increase from AWS Support in this Region. 2) Identify performance issues in the function to improve the speed of processing and therefore improve throughput. 3) Increase the batch size of the function, so that more messages are processed by each function invocation.
        :param alarm_name: The alarm name. Default: - lambdaFunction.functionName + ' - Throttles'
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 5
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 5
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73e2fd37e074d8437164ecec0a7146e6185d991ab6cce0ab1f03a6d551db8a84)
            check_type(argname="argument alarm_action", value=alarm_action, expected_type=type_hints["alarm_action"])
            check_type(argname="argument insufficient_data_action", value=insufficient_data_action, expected_type=type_hints["insufficient_data_action"])
            check_type(argname="argument ok_action", value=ok_action, expected_type=type_hints["ok_action"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument alarm_description", value=alarm_description, expected_type=type_hints["alarm_description"])
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "threshold": threshold,
        }
        if alarm_action is not None:
            self._values["alarm_action"] = alarm_action
        if insufficient_data_action is not None:
            self._values["insufficient_data_action"] = insufficient_data_action
        if ok_action is not None:
            self._values["ok_action"] = ok_action
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data
        if period is not None:
            self._values["period"] = period
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if alarm_name is not None:
            self._values["alarm_name"] = alarm_name
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluation_periods is not None:
            self._values["evaluation_periods"] = evaluation_periods

    @builtins.property
    def alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    @builtins.property
    def period(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The period over which the specified statistic is applied.

        :default: Duration.minutes(1)
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def threshold(self) -> jsii.Number:
        '''The value against which the specified statictis is compared.

        Set the threshold to a number greater than zero. The exact value
        of the threshold can depend on the tolerance of the application.
        Set the threshold according to its usage and scaling requirements
        of the function.
        '''
        result = self._values.get("threshold")
        assert result is not None, "Required property 'threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        '''The description of the alarm.

        :default:

        - This alarm detects a high number of throttled invocation requests. Throttling occurs when
        there is no concurrency is available for scale up. There are several approaches to resolve this issue.

        1. Request a concurrency increase from AWS Support in this Region. 2) Identify performance issues in
        the function to improve the speed of processing and therefore improve throughput. 3) Increase the batch
        size of the function, so that more messages are processed by each function invocation.
        '''
        result = self._values.get("alarm_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_name(self) -> typing.Optional[builtins.str]:
        '''The alarm name.

        :default: - lambdaFunction.functionName + ' - Throttles'
        '''
        result = self._values.get("alarm_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of data points that must be breaching to trigger the alarm.

        :default: 5
        '''
        result = self._values.get("datapoints_to_alarm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''The number of periods over which data is compared to the specified threshold.

        :default: 5
        '''
        result = self._values.get("evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaThrottlesAlarmConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.LambdaThrottlesAlarmProps",
    jsii_struct_bases=[LambdaThrottlesAlarmConfig],
    name_mapping={
        "alarm_action": "alarmAction",
        "insufficient_data_action": "insufficientDataAction",
        "ok_action": "okAction",
        "treat_missing_data": "treatMissingData",
        "period": "period",
        "threshold": "threshold",
        "alarm_description": "alarmDescription",
        "alarm_name": "alarmName",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluation_periods": "evaluationPeriods",
        "lambda_function": "lambdaFunction",
    },
)
class LambdaThrottlesAlarmProps(LambdaThrottlesAlarmConfig):
    def __init__(
        self,
        *,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        threshold: jsii.Number,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        lambda_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
    ) -> None:
        '''The properties for the LambdaThrottlesAlarm construct.

        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param threshold: The value against which the specified statictis is compared. Set the threshold to a number greater than zero. The exact value of the threshold can depend on the tolerance of the application. Set the threshold according to its usage and scaling requirements of the function.
        :param alarm_description: The description of the alarm. Default: - This alarm detects a high number of throttled invocation requests. Throttling occurs when there is no concurrency is available for scale up. There are several approaches to resolve this issue. 1. Request a concurrency increase from AWS Support in this Region. 2) Identify performance issues in the function to improve the speed of processing and therefore improve throughput. 3) Increase the batch size of the function, so that more messages are processed by each function invocation.
        :param alarm_name: The alarm name. Default: - lambdaFunction.functionName + ' - Throttles'
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 5
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 5
        :param lambda_function: The Lambda function to monitor.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e1cacf0523a9e7229f0a95e8fd3bb47e8e7bceca45491724237db0109dd5b93)
            check_type(argname="argument alarm_action", value=alarm_action, expected_type=type_hints["alarm_action"])
            check_type(argname="argument insufficient_data_action", value=insufficient_data_action, expected_type=type_hints["insufficient_data_action"])
            check_type(argname="argument ok_action", value=ok_action, expected_type=type_hints["ok_action"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument alarm_description", value=alarm_description, expected_type=type_hints["alarm_description"])
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument lambda_function", value=lambda_function, expected_type=type_hints["lambda_function"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "threshold": threshold,
            "lambda_function": lambda_function,
        }
        if alarm_action is not None:
            self._values["alarm_action"] = alarm_action
        if insufficient_data_action is not None:
            self._values["insufficient_data_action"] = insufficient_data_action
        if ok_action is not None:
            self._values["ok_action"] = ok_action
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data
        if period is not None:
            self._values["period"] = period
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if alarm_name is not None:
            self._values["alarm_name"] = alarm_name
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluation_periods is not None:
            self._values["evaluation_periods"] = evaluation_periods

    @builtins.property
    def alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    @builtins.property
    def period(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The period over which the specified statistic is applied.

        :default: Duration.minutes(1)
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def threshold(self) -> jsii.Number:
        '''The value against which the specified statictis is compared.

        Set the threshold to a number greater than zero. The exact value
        of the threshold can depend on the tolerance of the application.
        Set the threshold according to its usage and scaling requirements
        of the function.
        '''
        result = self._values.get("threshold")
        assert result is not None, "Required property 'threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        '''The description of the alarm.

        :default:

        - This alarm detects a high number of throttled invocation requests. Throttling occurs when
        there is no concurrency is available for scale up. There are several approaches to resolve this issue.

        1. Request a concurrency increase from AWS Support in this Region. 2) Identify performance issues in
        the function to improve the speed of processing and therefore improve throughput. 3) Increase the batch
        size of the function, so that more messages are processed by each function invocation.
        '''
        result = self._values.get("alarm_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_name(self) -> typing.Optional[builtins.str]:
        '''The alarm name.

        :default: - lambdaFunction.functionName + ' - Throttles'
        '''
        result = self._values.get("alarm_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of data points that must be breaching to trigger the alarm.

        :default: 5
        '''
        result = self._values.get("datapoints_to_alarm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''The number of periods over which data is compared to the specified threshold.

        :default: 5
        '''
        result = self._values.get("evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def lambda_function(self) -> _aws_cdk_aws_lambda_ceddda9d.IFunction:
        '''The Lambda function to monitor.'''
        result = self._values.get("lambda_function")
        assert result is not None, "Required property 'lambda_function' is missing"
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.IFunction, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaThrottlesAlarmProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Queue(
    _aws_cdk_aws_sqs_ceddda9d.Queue,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.Queue",
):
    '''An extension of the SQS Queue construct that adds methods to create recommended alarms.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        content_based_deduplication: typing.Optional[builtins.bool] = None,
        data_key_reuse: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        dead_letter_queue: typing.Optional[typing.Union[_aws_cdk_aws_sqs_ceddda9d.DeadLetterQueue, typing.Dict[builtins.str, typing.Any]]] = None,
        deduplication_scope: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.DeduplicationScope] = None,
        delivery_delay: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        encryption: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.QueueEncryption] = None,
        encryption_master_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        enforce_ssl: typing.Optional[builtins.bool] = None,
        fifo: typing.Optional[builtins.bool] = None,
        fifo_throughput_limit: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.FifoThroughputLimit] = None,
        max_message_size_bytes: typing.Optional[jsii.Number] = None,
        queue_name: typing.Optional[builtins.str] = None,
        receive_message_wait_time: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        redrive_allow_policy: typing.Optional[typing.Union[_aws_cdk_aws_sqs_ceddda9d.RedriveAllowPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        retention_period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        visibility_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param content_based_deduplication: Specifies whether to enable content-based deduplication. During the deduplication interval (5 minutes), Amazon SQS treats messages that are sent with identical content (excluding attributes) as duplicates and delivers only one copy of the message. If you don't enable content-based deduplication and you want to deduplicate messages, provide an explicit deduplication ID in your SendMessage() call. (Only applies to FIFO queues.) Default: false
        :param data_key_reuse: The length of time that Amazon SQS reuses a data key before calling KMS again. The value must be an integer between 60 (1 minute) and 86,400 (24 hours). The default is 300 (5 minutes). Default: Duration.minutes(5)
        :param dead_letter_queue: Send messages to this queue if they were unsuccessfully dequeued a number of times. Default: no dead-letter queue
        :param deduplication_scope: For high throughput for FIFO queues, specifies whether message deduplication occurs at the message group or queue level. (Only applies to FIFO queues.) Default: DeduplicationScope.QUEUE
        :param delivery_delay: The time in seconds that the delivery of all messages in the queue is delayed. You can specify an integer value of 0 to 900 (15 minutes). The default value is 0. Default: 0
        :param encryption: Whether the contents of the queue are encrypted, and by what type of key. Be aware that encryption is not available in all regions, please see the docs for current availability details. Default: SQS_MANAGED (SSE-SQS) for newly created queues
        :param encryption_master_key: External KMS key to use for queue encryption. Individual messages will be encrypted using data keys. The data keys in turn will be encrypted using this key, and reused for a maximum of ``dataKeyReuseSecs`` seconds. If the 'encryptionMasterKey' property is set, 'encryption' type will be implicitly set to "KMS". Default: If encryption is set to KMS and not specified, a key will be created.
        :param enforce_ssl: Enforce encryption of data in transit. Default: false
        :param fifo: Whether this a first-in-first-out (FIFO) queue. Default: false, unless queueName ends in '.fifo' or 'contentBasedDeduplication' is true.
        :param fifo_throughput_limit: For high throughput for FIFO queues, specifies whether the FIFO queue throughput quota applies to the entire queue or per message group. (Only applies to FIFO queues.) Default: FifoThroughputLimit.PER_QUEUE
        :param max_message_size_bytes: The limit of how many bytes that a message can contain before Amazon SQS rejects it. You can specify an integer value from 1024 bytes (1 KiB) to 262144 bytes (256 KiB). The default value is 262144 (256 KiB). Default: 256KiB
        :param queue_name: A name for the queue. If specified and this is a FIFO queue, must end in the string '.fifo'. Default: CloudFormation-generated name
        :param receive_message_wait_time: Default wait time for ReceiveMessage calls. Does not wait if set to 0, otherwise waits this amount of seconds by default for messages to arrive. For more information, see Amazon SQS Long Poll. Default: 0
        :param redrive_allow_policy: The string that includes the parameters for the permissions for the dead-letter queue redrive permission and which source queues can specify dead-letter queues. Default: - All source queues can designate this queue as their dead-letter queue.
        :param removal_policy: Policy to apply when the queue is removed from the stack. Even though queues are technically stateful, their contents are transient and it is common to add and remove Queues while rearchitecting your application. The default is therefore ``DESTROY``. Change it to ``RETAIN`` if the messages are so valuable that accidentally losing them would be unacceptable. Default: RemovalPolicy.DESTROY
        :param retention_period: The number of seconds that Amazon SQS retains a message. You can specify an integer value from 60 seconds (1 minute) to 1209600 seconds (14 days). The default value is 345600 seconds (4 days). Default: Duration.days(4)
        :param visibility_timeout: Timeout of processing a single message. After dequeuing, the processor has this much time to handle the message and delete it from the queue before it becomes visible again for dequeueing by another processor. Values must be from 0 to 43200 seconds (12 hours). If you don't specify a value, AWS CloudFormation uses the default value of 30 seconds. Default: Duration.seconds(30)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e63632b9287782cde140e2fa25c2d500852c1e3fdad4c8d2118b305c4ebd894d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = _aws_cdk_aws_sqs_ceddda9d.QueueProps(
            content_based_deduplication=content_based_deduplication,
            data_key_reuse=data_key_reuse,
            dead_letter_queue=dead_letter_queue,
            deduplication_scope=deduplication_scope,
            delivery_delay=delivery_delay,
            encryption=encryption,
            encryption_master_key=encryption_master_key,
            enforce_ssl=enforce_ssl,
            fifo=fifo,
            fifo_throughput_limit=fifo_throughput_limit,
            max_message_size_bytes=max_message_size_bytes,
            queue_name=queue_name,
            receive_message_wait_time=receive_message_wait_time,
            redrive_allow_policy=redrive_allow_policy,
            removal_policy=removal_policy,
            retention_period=retention_period,
            visibility_timeout=visibility_timeout,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="alarmApproximateAgeOfOldestMessage")
    def alarm_approximate_age_of_oldest_message(
        self,
        *,
        threshold: jsii.Number,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> "SqsApproximateAgeOfOldestMessageAlarm":
        '''Creates an alarm that watches the age of the oldest message in the queue.

        :param threshold: The value against which the specified statistic is compared. The recommended threshold value for this alarm is highly dependent on the expected message processing time. You can use historical data to calculate the average message processing time, and then set the threshold to 50% higher than the maximum expected SQS message processing time by queue consumers.
        :param alarm_description: The description of the alarm. Default: - This alarm watches the age of the oldest message in the queue. You can use this alarm to monitor if your consumers are processing SQS messages at the desired speed. Consider increasing the consumer count or consumer throughput to reduce message age. This metric can be used in combination with ApproximateNumberOfMessagesVisible to determine how big the queue backlog is and how quickly messages are being processed. To prevent messages from being deleted before processed, consider configuring the dead-letter queue to sideline potential poison pill messages.
        :param alarm_name: The alarm name. Default: - queue.queueName + ' - ApproximateAgeOfOldestMessage'
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 15
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 15
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        props = SqsApproximateAgeOfOldestMessageAlarmConfig(
            threshold=threshold,
            alarm_description=alarm_description,
            alarm_name=alarm_name,
            datapoints_to_alarm=datapoints_to_alarm,
            evaluation_periods=evaluation_periods,
            period=period,
            alarm_action=alarm_action,
            insufficient_data_action=insufficient_data_action,
            ok_action=ok_action,
            treat_missing_data=treat_missing_data,
        )

        return typing.cast("SqsApproximateAgeOfOldestMessageAlarm", jsii.invoke(self, "alarmApproximateAgeOfOldestMessage", [props]))

    @jsii.member(jsii_name="alarmApproximateNumberOfMessagesNotVisible")
    def alarm_approximate_number_of_messages_not_visible(
        self,
        *,
        threshold: jsii.Number,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> "SqsApproximateNumberOfMessagesNotVisibleAlarm":
        '''Creates an alarm that watches the number of messages that are in flight.

        :param threshold: The value against which the specified statistic is compared. The recommended threshold value for this alarm is highly dependent on the expected number of messages in flight. You can use historical data to calculate the maximum expected number of messages in flight and set the threshold to 50% over this value. If consumers of the queue are processing but not deleting messages from the queue, this number will suddenly increase.
        :param alarm_description: The description of the alarm. Default: - This alarm helps to detect a high number of in-flight messages with respect to QueueName. For troubleshooting, check message backlog decreasing (https://repost.aws/knowledge-center/sqs-message-backlog).
        :param alarm_name: The alarm name. Default: - queue.queueName + ' - ApproximateNumberOfMessagesNotVisible'
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 15
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 15
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        props = SqsApproximateNumberOfMessagesNotVisibleAlarmConfig(
            threshold=threshold,
            alarm_description=alarm_description,
            alarm_name=alarm_name,
            datapoints_to_alarm=datapoints_to_alarm,
            evaluation_periods=evaluation_periods,
            period=period,
            alarm_action=alarm_action,
            insufficient_data_action=insufficient_data_action,
            ok_action=ok_action,
            treat_missing_data=treat_missing_data,
        )

        return typing.cast("SqsApproximateNumberOfMessagesNotVisibleAlarm", jsii.invoke(self, "alarmApproximateNumberOfMessagesNotVisible", [props]))

    @jsii.member(jsii_name="alarmApproximateNumberOfMessagesVisible")
    def alarm_approximate_number_of_messages_visible(
        self,
        *,
        threshold: jsii.Number,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> "SqsApproximateNumberOfMessagesVisibleAlarm":
        '''Creates an alarm that watches the number of messages that are visible in the queue.

        :param threshold: The value against which the specified statistic is compared. An unexpectedly high number of messages visible indicates that messages are not being processed by a consumer at the expected rate. You should consider historical data when you set this threshold.
        :param alarm_description: The description of the alarm. Default: - This alarm helps to detect a high number of in-flight messages with respect to QueueName. For troubleshooting, check message backlog decreasing (https://repost.aws/knowledge-center/sqs-message-backlog).
        :param alarm_name: The alarm name. Default: - queue.queueName + ' - ApproximateNumberOfMessagesVisible'
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 15
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 15
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        props = SqsApproximateNumberOfMessagesVisibleAlarmConfig(
            threshold=threshold,
            alarm_description=alarm_description,
            alarm_name=alarm_name,
            datapoints_to_alarm=datapoints_to_alarm,
            evaluation_periods=evaluation_periods,
            period=period,
            alarm_action=alarm_action,
            insufficient_data_action=insufficient_data_action,
            ok_action=ok_action,
            treat_missing_data=treat_missing_data,
        )

        return typing.cast("SqsApproximateNumberOfMessagesVisibleAlarm", jsii.invoke(self, "alarmApproximateNumberOfMessagesVisible", [props]))

    @jsii.member(jsii_name="alarmNumberOfMessagesSent")
    def alarm_number_of_messages_sent(
        self,
        *,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        threshold: typing.Optional[jsii.Number] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> "SqsNumberOfMessagesSentAlarm":
        '''Creates an alarm that watches the number of messages that are sent.

        :param alarm_description: The description of the alarm. Default: - This alarm helps to detect a high number of in-flight messages with respect to QueueName. For troubleshooting, check message backlog decreasing (https://repost.aws/knowledge-center/sqs-message-backlog).
        :param alarm_name: The alarm name. Default: - queue.queueName + ' - NumberOfMessagesSent'
        :param threshold: The value against which the specified statistic is compared. If the number of messages sent is 0, the producer is not sending any messages. If this queue has a low TPS, increase the number of EvaluationPeriods accordingly. Default: 0
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 15
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 15
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        props = SqsNumberOfMessagesSentAlarmConfig(
            alarm_description=alarm_description,
            alarm_name=alarm_name,
            threshold=threshold,
            datapoints_to_alarm=datapoints_to_alarm,
            evaluation_periods=evaluation_periods,
            period=period,
            alarm_action=alarm_action,
            insufficient_data_action=insufficient_data_action,
            ok_action=ok_action,
            treat_missing_data=treat_missing_data,
        )

        return typing.cast("SqsNumberOfMessagesSentAlarm", jsii.invoke(self, "alarmNumberOfMessagesSent", [props]))

    @jsii.member(jsii_name="applyRecommendedAlarms")
    def apply_recommended_alarms(
        self,
        *,
        config_approximate_age_of_oldest_message_alarm: typing.Union["SqsApproximateAgeOfOldestMessageAlarmConfig", typing.Dict[builtins.str, typing.Any]],
        config_approximate_number_of_messages_not_visible_alarm: typing.Union["SqsApproximateNumberOfMessagesNotVisibleAlarmConfig", typing.Dict[builtins.str, typing.Any]],
        config_approximate_number_of_messages_visible_alarm: typing.Union["SqsApproximateNumberOfMessagesVisibleAlarmConfig", typing.Dict[builtins.str, typing.Any]],
        config_number_of_messages_sent_alarm: typing.Optional[typing.Union["SqsNumberOfMessagesSentAlarmConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        default_alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        default_insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        default_ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        exclude_alarms: typing.Optional[typing.Sequence["SqsRecommendedAlarmsMetrics"]] = None,
        exclude_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> None:
        '''Creates the recommended alarms for an SQS queue.

        :param config_approximate_age_of_oldest_message_alarm: The configuration for the approximate age of oldest message alarm.
        :param config_approximate_number_of_messages_not_visible_alarm: The configuration for the approximate number of messages not visible alarm.
        :param config_approximate_number_of_messages_visible_alarm: The configuration for the approximate number of messages visible alarm.
        :param config_number_of_messages_sent_alarm: The configuration for the number of messages sent alarm.
        :param default_alarm_action: The default action to take when an alarm is triggered. Default: - None
        :param default_insufficient_data_action: The default action to take when an alarm has insufficient data. Default: - None
        :param default_ok_action: The default action to take when an alarm enters the ok state. Default: - None
        :param exclude_alarms: Alarm metrics to exclude from the recommended alarms. Default: - None
        :param exclude_resources: The resources to exclude from the recommended alarms. Use a resources id to exclude a specific resource.
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        props = SqsRecommendedAlarmsConfig(
            config_approximate_age_of_oldest_message_alarm=config_approximate_age_of_oldest_message_alarm,
            config_approximate_number_of_messages_not_visible_alarm=config_approximate_number_of_messages_not_visible_alarm,
            config_approximate_number_of_messages_visible_alarm=config_approximate_number_of_messages_visible_alarm,
            config_number_of_messages_sent_alarm=config_number_of_messages_sent_alarm,
            default_alarm_action=default_alarm_action,
            default_insufficient_data_action=default_insufficient_data_action,
            default_ok_action=default_ok_action,
            exclude_alarms=exclude_alarms,
            exclude_resources=exclude_resources,
            treat_missing_data=treat_missing_data,
        )

        return typing.cast(None, jsii.invoke(self, "applyRecommendedAlarms", [props]))


class S3Bucket4xxErrorsAlarm(
    _aws_cdk_aws_cloudwatch_ceddda9d.Alarm,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.S3Bucket4xxErrorsAlarm",
):
    '''An alarm that monitors the 4xx errors for an S3 bucket.

    This alarm is used to create a baseline for typical 4xx error
    rates so that you can look into any abnormalities that might
    indicate a setup issue.

    The alarm is triggered when the 4xx error rate exceeds the % threshold.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        threshold: typing.Optional[jsii.Number] = None,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param bucket: The S3 bucket to monitor.
        :param alarm_description: The alarm description. Default: - This alarm helps us report the total number of 4xx error status codes that are made in response to client requests. 403 error codes might indicate an incorrect IAM policy, and 404 error codes might indicate mis-behaving client application, for example. Enabling S3 server access logging on a temporary basis will help you to pinpoint the issue's origin using the fields HTTP status and Error Code. To understand more about the error code, see Error Responses (https://docs.aws.amazon.com/AmazonS3/latest/API/ErrorResponses.html).
        :param alarm_name: The alarm name. Default: - bucket.bucketName + ' - 4xxErrors'
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 15
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 15
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param threshold: The value against which the specified statistic is compared. Default: 0.05
        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9d4f29388ca9807519ae0412e8634338d955302b834578576dc547f464049e6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = S3Bucket4xxErrorsAlarmProps(
            bucket=bucket,
            alarm_description=alarm_description,
            alarm_name=alarm_name,
            datapoints_to_alarm=datapoints_to_alarm,
            evaluation_periods=evaluation_periods,
            period=period,
            threshold=threshold,
            alarm_action=alarm_action,
            insufficient_data_action=insufficient_data_action,
            ok_action=ok_action,
            treat_missing_data=treat_missing_data,
        )

        jsii.create(self.__class__, self, [scope, id, props])


class S3Bucket5xxErrorsAlarm(
    _aws_cdk_aws_cloudwatch_ceddda9d.Alarm,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.S3Bucket5xxErrorsAlarm",
):
    '''An alarm that monitors the 5xx errors for an S3 bucket.

    This alarm can help to detect if the application is
    experiencing issues due to 5xx errors.

    The alarm is triggered when the 5xx error rate exceeds the % threshold.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        threshold: typing.Optional[jsii.Number] = None,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param bucket: The S3 bucket to monitor.
        :param alarm_description: The alarm description. Default: - This alarm helps you detect a high number of server-side errors. These errors indicate that a client made a request that the server couldn’t complete. This can help you correlate the issue your application is facing because of S3. For more information to help you efficiently handle or reduce errors, see Optimizing performance design patterns (https://docs.aws.amazon.com/AmazonS3/latest/userguide/optimizing-performance-design-patterns.html#optimizing-performance-timeouts-retries). Errors might also be caused by an the issue with S3, check AWS service health dashboard for the status of Amazon S3 in your Region.
        :param alarm_name: The alarm name. Default: - bucket.bucketName + ' - 5xxErrors'
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 15
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 15
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param threshold: The value against which the specified statistic is compared. Default: 0.05
        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e32caa975316b8e881679f0e3ca0297c5c175dcc49fcb62b683c66bf9f5782bb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = S3Bucket5xxErrorsAlarmProps(
            bucket=bucket,
            alarm_description=alarm_description,
            alarm_name=alarm_name,
            datapoints_to_alarm=datapoints_to_alarm,
            evaluation_periods=evaluation_periods,
            period=period,
            threshold=threshold,
            alarm_action=alarm_action,
            insufficient_data_action=insufficient_data_action,
            ok_action=ok_action,
            treat_missing_data=treat_missing_data,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.S3BucketHttpErrorsAlarmConfig",
    jsii_struct_bases=[AlarmBaseProps],
    name_mapping={
        "alarm_action": "alarmAction",
        "insufficient_data_action": "insufficientDataAction",
        "ok_action": "okAction",
        "treat_missing_data": "treatMissingData",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluation_periods": "evaluationPeriods",
        "period": "period",
        "threshold": "threshold",
    },
)
class S3BucketHttpErrorsAlarmConfig(AlarmBaseProps):
    def __init__(
        self,
        *,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''The optional configuration for the 4xx and 5xx error alarms for an S3 bucket.

        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 15
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 15
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param threshold: The value against which the specified statistic is compared. Default: 0.05
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2fd29de3b481f2cfa00b9af24444e83bc204407864373f5dd40399adff9991d)
            check_type(argname="argument alarm_action", value=alarm_action, expected_type=type_hints["alarm_action"])
            check_type(argname="argument insufficient_data_action", value=insufficient_data_action, expected_type=type_hints["insufficient_data_action"])
            check_type(argname="argument ok_action", value=ok_action, expected_type=type_hints["ok_action"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alarm_action is not None:
            self._values["alarm_action"] = alarm_action
        if insufficient_data_action is not None:
            self._values["insufficient_data_action"] = insufficient_data_action
        if ok_action is not None:
            self._values["ok_action"] = ok_action
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluation_periods is not None:
            self._values["evaluation_periods"] = evaluation_periods
        if period is not None:
            self._values["period"] = period
        if threshold is not None:
            self._values["threshold"] = threshold

    @builtins.property
    def alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of data points that must be breaching to trigger the alarm.

        :default: 15
        '''
        result = self._values.get("datapoints_to_alarm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''The number of periods over which data is compared to the specified threshold.

        :default: 15
        '''
        result = self._values.get("evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The period over which the specified statistic is applied.

        :default: Duration.minutes(1)
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def threshold(self) -> typing.Optional[jsii.Number]:
        '''The value against which the specified statistic is compared.

        :default: 0.05
        '''
        result = self._values.get("threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3BucketHttpErrorsAlarmConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3RecommendedAlarms(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.S3RecommendedAlarms",
):
    '''A construct that creates the recommended alarms for an S3 bucket.

    :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Best_Practice_Recommended_Alarms_AWS_Services.html#S3
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        config4xx_errors_alarm: typing.Optional[typing.Union["S3Bucket4xxErrorsAlarmConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        config5xx_errors_alarm: typing.Optional[typing.Union["S3Bucket5xxErrorsAlarmConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        default_alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        default_insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        default_ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        exclude_alarms: typing.Optional[typing.Sequence["S3RecommendedAlarmsMetrics"]] = None,
        exclude_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param bucket: The S3 bucket to apply the recommended alarms to.
        :param config4xx_errors_alarm: The configuration for the 4xx errors alarm.
        :param config5xx_errors_alarm: The configuration for the 5xx errors alarm.
        :param default_alarm_action: The default action to take when an alarm is triggered. Default: - None
        :param default_insufficient_data_action: The default action to take when an alarm has insufficient data. Default: - None
        :param default_ok_action: The default action to take when an alarm enters the ok state. Default: - None
        :param exclude_alarms: Alarm metrics to exclude from the recommended alarms. Default: - None
        :param exclude_resources: The resources to exclude from the recommended alarms. Use a resources id to exclude a specific resource.
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47bd74a1f4cc68aa49abcb9ddefc859f62a8d650ec660e1f1dc076405de12203)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = S3RecommendedAlarmsProps(
            bucket=bucket,
            config4xx_errors_alarm=config4xx_errors_alarm,
            config5xx_errors_alarm=config5xx_errors_alarm,
            default_alarm_action=default_alarm_action,
            default_insufficient_data_action=default_insufficient_data_action,
            default_ok_action=default_ok_action,
            exclude_alarms=exclude_alarms,
            exclude_resources=exclude_resources,
            treat_missing_data=treat_missing_data,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="alarm4xxErrors")
    def alarm4xx_errors(self) -> typing.Optional[S3Bucket4xxErrorsAlarm]:
        '''The 4xx errors alarm.'''
        return typing.cast(typing.Optional[S3Bucket4xxErrorsAlarm], jsii.get(self, "alarm4xxErrors"))

    @builtins.property
    @jsii.member(jsii_name="alarm5xxErrors")
    def alarm5xx_errors(self) -> typing.Optional[S3Bucket5xxErrorsAlarm]:
        '''The 5xx errors alarm.'''
        return typing.cast(typing.Optional[S3Bucket5xxErrorsAlarm], jsii.get(self, "alarm5xxErrors"))


@jsii.implements(_aws_cdk_ceddda9d.IAspect)
class S3RecommendedAlarmsAspect(
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.S3RecommendedAlarmsAspect",
):
    '''Configures the recommended alarms for an S3 bucket.

    :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Best_Practice_Recommended_Alarms_AWS_Services.html#S3
    '''

    def __init__(
        self,
        *,
        config4xx_errors_alarm: typing.Optional[typing.Union["S3Bucket4xxErrorsAlarmConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        config5xx_errors_alarm: typing.Optional[typing.Union["S3Bucket5xxErrorsAlarmConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        default_alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        default_insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        default_ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        exclude_alarms: typing.Optional[typing.Sequence["S3RecommendedAlarmsMetrics"]] = None,
        exclude_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> None:
        '''
        :param config4xx_errors_alarm: The configuration for the 4xx errors alarm.
        :param config5xx_errors_alarm: The configuration for the 5xx errors alarm.
        :param default_alarm_action: The default action to take when an alarm is triggered. Default: - None
        :param default_insufficient_data_action: The default action to take when an alarm has insufficient data. Default: - None
        :param default_ok_action: The default action to take when an alarm enters the ok state. Default: - None
        :param exclude_alarms: Alarm metrics to exclude from the recommended alarms. Default: - None
        :param exclude_resources: The resources to exclude from the recommended alarms. Use a resources id to exclude a specific resource.
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        props = S3RecommendedAlarmsConfig(
            config4xx_errors_alarm=config4xx_errors_alarm,
            config5xx_errors_alarm=config5xx_errors_alarm,
            default_alarm_action=default_alarm_action,
            default_insufficient_data_action=default_insufficient_data_action,
            default_ok_action=default_ok_action,
            exclude_alarms=exclude_alarms,
            exclude_resources=exclude_resources,
            treat_missing_data=treat_missing_data,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="visit")
    def visit(self, node: _constructs_77d1e7e8.IConstruct) -> None:
        '''All aspects can visit an IConstruct.

        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81cb56b973536fefe93bd8cdf5503a61b0f7a86c873b9ea667e56303d99c024b)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "visit", [node]))


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.S3RecommendedAlarmsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "config4xx_errors_alarm": "config4xxErrorsAlarm",
        "config5xx_errors_alarm": "config5xxErrorsAlarm",
        "default_alarm_action": "defaultAlarmAction",
        "default_insufficient_data_action": "defaultInsufficientDataAction",
        "default_ok_action": "defaultOkAction",
        "exclude_alarms": "excludeAlarms",
        "exclude_resources": "excludeResources",
        "treat_missing_data": "treatMissingData",
    },
)
class S3RecommendedAlarmsConfig:
    def __init__(
        self,
        *,
        config4xx_errors_alarm: typing.Optional[typing.Union["S3Bucket4xxErrorsAlarmConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        config5xx_errors_alarm: typing.Optional[typing.Union["S3Bucket5xxErrorsAlarmConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        default_alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        default_insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        default_ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        exclude_alarms: typing.Optional[typing.Sequence["S3RecommendedAlarmsMetrics"]] = None,
        exclude_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> None:
        '''Configurations for the recommended alarms for an S3 bucket.

        Default actions are overridden by the actions specified in the
        individual alarm configurations.

        :param config4xx_errors_alarm: The configuration for the 4xx errors alarm.
        :param config5xx_errors_alarm: The configuration for the 5xx errors alarm.
        :param default_alarm_action: The default action to take when an alarm is triggered. Default: - None
        :param default_insufficient_data_action: The default action to take when an alarm has insufficient data. Default: - None
        :param default_ok_action: The default action to take when an alarm enters the ok state. Default: - None
        :param exclude_alarms: Alarm metrics to exclude from the recommended alarms. Default: - None
        :param exclude_resources: The resources to exclude from the recommended alarms. Use a resources id to exclude a specific resource.
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        if isinstance(config4xx_errors_alarm, dict):
            config4xx_errors_alarm = S3Bucket4xxErrorsAlarmConfig(**config4xx_errors_alarm)
        if isinstance(config5xx_errors_alarm, dict):
            config5xx_errors_alarm = S3Bucket5xxErrorsAlarmConfig(**config5xx_errors_alarm)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a54261617c599ef9e038be027b2446bed17b11cfdf8002aee30d2b71f6ea7868)
            check_type(argname="argument config4xx_errors_alarm", value=config4xx_errors_alarm, expected_type=type_hints["config4xx_errors_alarm"])
            check_type(argname="argument config5xx_errors_alarm", value=config5xx_errors_alarm, expected_type=type_hints["config5xx_errors_alarm"])
            check_type(argname="argument default_alarm_action", value=default_alarm_action, expected_type=type_hints["default_alarm_action"])
            check_type(argname="argument default_insufficient_data_action", value=default_insufficient_data_action, expected_type=type_hints["default_insufficient_data_action"])
            check_type(argname="argument default_ok_action", value=default_ok_action, expected_type=type_hints["default_ok_action"])
            check_type(argname="argument exclude_alarms", value=exclude_alarms, expected_type=type_hints["exclude_alarms"])
            check_type(argname="argument exclude_resources", value=exclude_resources, expected_type=type_hints["exclude_resources"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if config4xx_errors_alarm is not None:
            self._values["config4xx_errors_alarm"] = config4xx_errors_alarm
        if config5xx_errors_alarm is not None:
            self._values["config5xx_errors_alarm"] = config5xx_errors_alarm
        if default_alarm_action is not None:
            self._values["default_alarm_action"] = default_alarm_action
        if default_insufficient_data_action is not None:
            self._values["default_insufficient_data_action"] = default_insufficient_data_action
        if default_ok_action is not None:
            self._values["default_ok_action"] = default_ok_action
        if exclude_alarms is not None:
            self._values["exclude_alarms"] = exclude_alarms
        if exclude_resources is not None:
            self._values["exclude_resources"] = exclude_resources
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data

    @builtins.property
    def config4xx_errors_alarm(self) -> typing.Optional["S3Bucket4xxErrorsAlarmConfig"]:
        '''The configuration for the 4xx errors alarm.'''
        result = self._values.get("config4xx_errors_alarm")
        return typing.cast(typing.Optional["S3Bucket4xxErrorsAlarmConfig"], result)

    @builtins.property
    def config5xx_errors_alarm(self) -> typing.Optional["S3Bucket5xxErrorsAlarmConfig"]:
        '''The configuration for the 5xx errors alarm.'''
        result = self._values.get("config5xx_errors_alarm")
        return typing.cast(typing.Optional["S3Bucket5xxErrorsAlarmConfig"], result)

    @builtins.property
    def default_alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The default action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("default_alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def default_insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The default action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("default_insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def default_ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The default action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("default_ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def exclude_alarms(
        self,
    ) -> typing.Optional[typing.List["S3RecommendedAlarmsMetrics"]]:
        '''Alarm metrics to exclude from the recommended alarms.

        :default: - None
        '''
        result = self._values.get("exclude_alarms")
        return typing.cast(typing.Optional[typing.List["S3RecommendedAlarmsMetrics"]], result)

    @builtins.property
    def exclude_resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The resources to exclude from the recommended alarms.

        Use a resources id to exclude a specific resource.
        '''
        result = self._values.get("exclude_resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3RecommendedAlarmsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.S3RecommendedAlarmsMetrics"
)
class S3RecommendedAlarmsMetrics(enum.Enum):
    '''The recommended metrics for S3 bucket alarms.'''

    ERRORS_4XX = "ERRORS_4XX"
    '''4xxErrors are errors (4xx error codes) that are made in response to client requests.'''
    ERRORS_5XX = "ERRORS_5XX"
    '''5xxErrors are server errors (5xx error codes) that are made in response to client requests.'''


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.S3RecommendedAlarmsProps",
    jsii_struct_bases=[S3RecommendedAlarmsConfig],
    name_mapping={
        "config4xx_errors_alarm": "config4xxErrorsAlarm",
        "config5xx_errors_alarm": "config5xxErrorsAlarm",
        "default_alarm_action": "defaultAlarmAction",
        "default_insufficient_data_action": "defaultInsufficientDataAction",
        "default_ok_action": "defaultOkAction",
        "exclude_alarms": "excludeAlarms",
        "exclude_resources": "excludeResources",
        "treat_missing_data": "treatMissingData",
        "bucket": "bucket",
    },
)
class S3RecommendedAlarmsProps(S3RecommendedAlarmsConfig):
    def __init__(
        self,
        *,
        config4xx_errors_alarm: typing.Optional[typing.Union["S3Bucket4xxErrorsAlarmConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        config5xx_errors_alarm: typing.Optional[typing.Union["S3Bucket5xxErrorsAlarmConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        default_alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        default_insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        default_ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        exclude_alarms: typing.Optional[typing.Sequence[S3RecommendedAlarmsMetrics]] = None,
        exclude_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    ) -> None:
        '''
        :param config4xx_errors_alarm: The configuration for the 4xx errors alarm.
        :param config5xx_errors_alarm: The configuration for the 5xx errors alarm.
        :param default_alarm_action: The default action to take when an alarm is triggered. Default: - None
        :param default_insufficient_data_action: The default action to take when an alarm has insufficient data. Default: - None
        :param default_ok_action: The default action to take when an alarm enters the ok state. Default: - None
        :param exclude_alarms: Alarm metrics to exclude from the recommended alarms. Default: - None
        :param exclude_resources: The resources to exclude from the recommended alarms. Use a resources id to exclude a specific resource.
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        :param bucket: The S3 bucket to apply the recommended alarms to.
        '''
        if isinstance(config4xx_errors_alarm, dict):
            config4xx_errors_alarm = S3Bucket4xxErrorsAlarmConfig(**config4xx_errors_alarm)
        if isinstance(config5xx_errors_alarm, dict):
            config5xx_errors_alarm = S3Bucket5xxErrorsAlarmConfig(**config5xx_errors_alarm)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bffe2626f56a0b42370556b496eae7b36c626ba33a4d8d3b6ee7cf6c6e78caeb)
            check_type(argname="argument config4xx_errors_alarm", value=config4xx_errors_alarm, expected_type=type_hints["config4xx_errors_alarm"])
            check_type(argname="argument config5xx_errors_alarm", value=config5xx_errors_alarm, expected_type=type_hints["config5xx_errors_alarm"])
            check_type(argname="argument default_alarm_action", value=default_alarm_action, expected_type=type_hints["default_alarm_action"])
            check_type(argname="argument default_insufficient_data_action", value=default_insufficient_data_action, expected_type=type_hints["default_insufficient_data_action"])
            check_type(argname="argument default_ok_action", value=default_ok_action, expected_type=type_hints["default_ok_action"])
            check_type(argname="argument exclude_alarms", value=exclude_alarms, expected_type=type_hints["exclude_alarms"])
            check_type(argname="argument exclude_resources", value=exclude_resources, expected_type=type_hints["exclude_resources"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
        }
        if config4xx_errors_alarm is not None:
            self._values["config4xx_errors_alarm"] = config4xx_errors_alarm
        if config5xx_errors_alarm is not None:
            self._values["config5xx_errors_alarm"] = config5xx_errors_alarm
        if default_alarm_action is not None:
            self._values["default_alarm_action"] = default_alarm_action
        if default_insufficient_data_action is not None:
            self._values["default_insufficient_data_action"] = default_insufficient_data_action
        if default_ok_action is not None:
            self._values["default_ok_action"] = default_ok_action
        if exclude_alarms is not None:
            self._values["exclude_alarms"] = exclude_alarms
        if exclude_resources is not None:
            self._values["exclude_resources"] = exclude_resources
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data

    @builtins.property
    def config4xx_errors_alarm(self) -> typing.Optional["S3Bucket4xxErrorsAlarmConfig"]:
        '''The configuration for the 4xx errors alarm.'''
        result = self._values.get("config4xx_errors_alarm")
        return typing.cast(typing.Optional["S3Bucket4xxErrorsAlarmConfig"], result)

    @builtins.property
    def config5xx_errors_alarm(self) -> typing.Optional["S3Bucket5xxErrorsAlarmConfig"]:
        '''The configuration for the 5xx errors alarm.'''
        result = self._values.get("config5xx_errors_alarm")
        return typing.cast(typing.Optional["S3Bucket5xxErrorsAlarmConfig"], result)

    @builtins.property
    def default_alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The default action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("default_alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def default_insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The default action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("default_insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def default_ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The default action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("default_ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def exclude_alarms(
        self,
    ) -> typing.Optional[typing.List[S3RecommendedAlarmsMetrics]]:
        '''Alarm metrics to exclude from the recommended alarms.

        :default: - None
        '''
        result = self._values.get("exclude_alarms")
        return typing.cast(typing.Optional[typing.List[S3RecommendedAlarmsMetrics]], result)

    @builtins.property
    def exclude_resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The resources to exclude from the recommended alarms.

        Use a resources id to exclude a specific resource.
        '''
        result = self._values.get("exclude_resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    @builtins.property
    def bucket(self) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        '''The S3 bucket to apply the recommended alarms to.'''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3RecommendedAlarmsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.SnsAlarmBaseConfig",
    jsii_struct_bases=[AlarmBaseProps],
    name_mapping={
        "alarm_action": "alarmAction",
        "insufficient_data_action": "insufficientDataAction",
        "ok_action": "okAction",
        "treat_missing_data": "treatMissingData",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluation_periods": "evaluationPeriods",
        "period": "period",
    },
)
class SnsAlarmBaseConfig(AlarmBaseProps):
    def __init__(
        self,
        *,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''
        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 5
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 5
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6357da9f37e3e6b457ad09023bb9b95a1d5a38c2f284fa206c1d1d7696f94317)
            check_type(argname="argument alarm_action", value=alarm_action, expected_type=type_hints["alarm_action"])
            check_type(argname="argument insufficient_data_action", value=insufficient_data_action, expected_type=type_hints["insufficient_data_action"])
            check_type(argname="argument ok_action", value=ok_action, expected_type=type_hints["ok_action"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alarm_action is not None:
            self._values["alarm_action"] = alarm_action
        if insufficient_data_action is not None:
            self._values["insufficient_data_action"] = insufficient_data_action
        if ok_action is not None:
            self._values["ok_action"] = ok_action
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluation_periods is not None:
            self._values["evaluation_periods"] = evaluation_periods
        if period is not None:
            self._values["period"] = period

    @builtins.property
    def alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of data points that must be breaching to trigger the alarm.

        :default: 5
        '''
        result = self._values.get("datapoints_to_alarm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''The number of periods over which data is compared to the specified threshold.

        :default: 5
        '''
        result = self._values.get("evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The period over which the specified statistic is applied.

        :default: Duration.minutes(1)
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SnsAlarmBaseConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SnsNumberOfMessagesPublishedAlarm(
    _aws_cdk_aws_cloudwatch_ceddda9d.Alarm,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.SnsNumberOfMessagesPublishedAlarm",
):
    '''An alarm that monitors the number of messages published to an SNS topic.

    This alarm helps you proactively monitor and detect significant drops in
    notification publishing. This helps you identify potential issues with
    your application or business processes, so that you can take appropriate
    actions to maintain the expected flow of notifications. You should create
    this alarm if you expect your system to have a minimum traffic that it
    is serving.

    The alarm is triggered when the number of messages published to the topic
    is less than the specified threshold.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        topic: _aws_cdk_aws_sns_ceddda9d.ITopic,
        threshold: jsii.Number,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param topic: The SNS topic for which to create the alarm.
        :param threshold: The value against which the specified statistic is compared. The number of messages published should be in line with the expected number of published messages for your application. You can also analyze the historical data, trends and traffic to find the right threshold.
        :param alarm_description: The description of the alarm. Default: - This alarm can detect when the number of SNS messages published is too low. For troubleshooting, check why the publishers are sending less traffic.
        :param alarm_name: The alarm name. Default: - topic.topicName + ' - NumberOfMessagesPublished'
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 5
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 5
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98752834db6066573e1bc3fdef96ce5810035499b582fbd50205da8ca10e443a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SnsNumberOfMessagesPublishedAlarmProps(
            topic=topic,
            threshold=threshold,
            alarm_description=alarm_description,
            alarm_name=alarm_name,
            datapoints_to_alarm=datapoints_to_alarm,
            evaluation_periods=evaluation_periods,
            period=period,
            alarm_action=alarm_action,
            insufficient_data_action=insufficient_data_action,
            ok_action=ok_action,
            treat_missing_data=treat_missing_data,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.SnsNumberOfMessagesPublishedAlarmConfig",
    jsii_struct_bases=[SnsAlarmBaseConfig],
    name_mapping={
        "alarm_action": "alarmAction",
        "insufficient_data_action": "insufficientDataAction",
        "ok_action": "okAction",
        "treat_missing_data": "treatMissingData",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluation_periods": "evaluationPeriods",
        "period": "period",
        "threshold": "threshold",
        "alarm_description": "alarmDescription",
        "alarm_name": "alarmName",
    },
)
class SnsNumberOfMessagesPublishedAlarmConfig(SnsAlarmBaseConfig):
    def __init__(
        self,
        *,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        threshold: jsii.Number,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration for the NumberOfMessagesPublished alarm.

        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 5
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 5
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param threshold: The value against which the specified statistic is compared. The number of messages published should be in line with the expected number of published messages for your application. You can also analyze the historical data, trends and traffic to find the right threshold.
        :param alarm_description: The description of the alarm. Default: - This alarm can detect when the number of SNS messages published is too low. For troubleshooting, check why the publishers are sending less traffic.
        :param alarm_name: The alarm name. Default: - topic.topicName + ' - NumberOfMessagesPublished'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02d28bbf6430187b0f9eb1fb025b748f1a32141c7c491a091b9c54a910e6b18e)
            check_type(argname="argument alarm_action", value=alarm_action, expected_type=type_hints["alarm_action"])
            check_type(argname="argument insufficient_data_action", value=insufficient_data_action, expected_type=type_hints["insufficient_data_action"])
            check_type(argname="argument ok_action", value=ok_action, expected_type=type_hints["ok_action"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument alarm_description", value=alarm_description, expected_type=type_hints["alarm_description"])
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "threshold": threshold,
        }
        if alarm_action is not None:
            self._values["alarm_action"] = alarm_action
        if insufficient_data_action is not None:
            self._values["insufficient_data_action"] = insufficient_data_action
        if ok_action is not None:
            self._values["ok_action"] = ok_action
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluation_periods is not None:
            self._values["evaluation_periods"] = evaluation_periods
        if period is not None:
            self._values["period"] = period
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if alarm_name is not None:
            self._values["alarm_name"] = alarm_name

    @builtins.property
    def alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of data points that must be breaching to trigger the alarm.

        :default: 5
        '''
        result = self._values.get("datapoints_to_alarm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''The number of periods over which data is compared to the specified threshold.

        :default: 5
        '''
        result = self._values.get("evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The period over which the specified statistic is applied.

        :default: Duration.minutes(1)
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def threshold(self) -> jsii.Number:
        '''The value against which the specified statistic is compared.

        The number of messages published should be in line with the expected number of
        published messages for your application. You can also analyze the historical data,
        trends and traffic to find the right threshold.
        '''
        result = self._values.get("threshold")
        assert result is not None, "Required property 'threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        '''The description of the alarm.

        :default:

        - This alarm can detect when the number of SNS messages published is too low.
        For troubleshooting, check why the publishers are sending less traffic.
        '''
        result = self._values.get("alarm_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_name(self) -> typing.Optional[builtins.str]:
        '''The alarm name.

        :default: - topic.topicName + ' - NumberOfMessagesPublished'
        '''
        result = self._values.get("alarm_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SnsNumberOfMessagesPublishedAlarmConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.SnsNumberOfMessagesPublishedAlarmProps",
    jsii_struct_bases=[SnsNumberOfMessagesPublishedAlarmConfig],
    name_mapping={
        "alarm_action": "alarmAction",
        "insufficient_data_action": "insufficientDataAction",
        "ok_action": "okAction",
        "treat_missing_data": "treatMissingData",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluation_periods": "evaluationPeriods",
        "period": "period",
        "threshold": "threshold",
        "alarm_description": "alarmDescription",
        "alarm_name": "alarmName",
        "topic": "topic",
    },
)
class SnsNumberOfMessagesPublishedAlarmProps(SnsNumberOfMessagesPublishedAlarmConfig):
    def __init__(
        self,
        *,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        threshold: jsii.Number,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        topic: _aws_cdk_aws_sns_ceddda9d.ITopic,
    ) -> None:
        '''Properties for the SnsNumberOfMessagesPublishedAlarm construct.

        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 5
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 5
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param threshold: The value against which the specified statistic is compared. The number of messages published should be in line with the expected number of published messages for your application. You can also analyze the historical data, trends and traffic to find the right threshold.
        :param alarm_description: The description of the alarm. Default: - This alarm can detect when the number of SNS messages published is too low. For troubleshooting, check why the publishers are sending less traffic.
        :param alarm_name: The alarm name. Default: - topic.topicName + ' - NumberOfMessagesPublished'
        :param topic: The SNS topic for which to create the alarm.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fff028ea41836c29985adfc761cb4e4d9d91324dab443383b2985d7174500a19)
            check_type(argname="argument alarm_action", value=alarm_action, expected_type=type_hints["alarm_action"])
            check_type(argname="argument insufficient_data_action", value=insufficient_data_action, expected_type=type_hints["insufficient_data_action"])
            check_type(argname="argument ok_action", value=ok_action, expected_type=type_hints["ok_action"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument alarm_description", value=alarm_description, expected_type=type_hints["alarm_description"])
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "threshold": threshold,
            "topic": topic,
        }
        if alarm_action is not None:
            self._values["alarm_action"] = alarm_action
        if insufficient_data_action is not None:
            self._values["insufficient_data_action"] = insufficient_data_action
        if ok_action is not None:
            self._values["ok_action"] = ok_action
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluation_periods is not None:
            self._values["evaluation_periods"] = evaluation_periods
        if period is not None:
            self._values["period"] = period
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if alarm_name is not None:
            self._values["alarm_name"] = alarm_name

    @builtins.property
    def alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of data points that must be breaching to trigger the alarm.

        :default: 5
        '''
        result = self._values.get("datapoints_to_alarm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''The number of periods over which data is compared to the specified threshold.

        :default: 5
        '''
        result = self._values.get("evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The period over which the specified statistic is applied.

        :default: Duration.minutes(1)
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def threshold(self) -> jsii.Number:
        '''The value against which the specified statistic is compared.

        The number of messages published should be in line with the expected number of
        published messages for your application. You can also analyze the historical data,
        trends and traffic to find the right threshold.
        '''
        result = self._values.get("threshold")
        assert result is not None, "Required property 'threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        '''The description of the alarm.

        :default:

        - This alarm can detect when the number of SNS messages published is too low.
        For troubleshooting, check why the publishers are sending less traffic.
        '''
        result = self._values.get("alarm_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_name(self) -> typing.Optional[builtins.str]:
        '''The alarm name.

        :default: - topic.topicName + ' - NumberOfMessagesPublished'
        '''
        result = self._values.get("alarm_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def topic(self) -> _aws_cdk_aws_sns_ceddda9d.ITopic:
        '''The SNS topic for which to create the alarm.'''
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return typing.cast(_aws_cdk_aws_sns_ceddda9d.ITopic, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SnsNumberOfMessagesPublishedAlarmProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SnsNumberOfNotificationsDeliveredAlarm(
    _aws_cdk_aws_cloudwatch_ceddda9d.Alarm,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.SnsNumberOfNotificationsDeliveredAlarm",
):
    '''An alarm that monitors the number of notifications delivered by an SNS topic.

    This alarm helps you detect a drop in the volume of messages delivered.
    You should create this alarm if you expect your system to have a
    minimum traffic that it is serving.

    The alarm is triggered when the number of messages delivered by the topic
    is less than the specified threshold.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        topic: _aws_cdk_aws_sns_ceddda9d.ITopic,
        threshold: jsii.Number,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param topic: The SNS topic for which to create the alarm.
        :param threshold: The value against which the specified statistic is compared. The number of messages delivered should be in line with the expected number of messages produced and the number of consumers. You can also analyze the historical data, trends and traffic to find the right threshold.
        :param alarm_description: The description of the alarm. Default: - This alarm can detect when the number of SNS messages delivered is too low. This could be because of unintentional unsubscribing of an endpoint, or because of an SNS event that causes messages to experience delay.
        :param alarm_name: The alarm name. Default: - topic.topicName + ' - NumberOfNotificationsDelivered'
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 5
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 5
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6373f947a105537f03e197d13ae190cc1b538074b51e0b7eccd8b7956fedc0f3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SnsNumberOfNotificationsDeliveredAlarmProps(
            topic=topic,
            threshold=threshold,
            alarm_description=alarm_description,
            alarm_name=alarm_name,
            datapoints_to_alarm=datapoints_to_alarm,
            evaluation_periods=evaluation_periods,
            period=period,
            alarm_action=alarm_action,
            insufficient_data_action=insufficient_data_action,
            ok_action=ok_action,
            treat_missing_data=treat_missing_data,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.SnsNumberOfNotificationsDeliveredAlarmConfig",
    jsii_struct_bases=[SnsAlarmBaseConfig],
    name_mapping={
        "alarm_action": "alarmAction",
        "insufficient_data_action": "insufficientDataAction",
        "ok_action": "okAction",
        "treat_missing_data": "treatMissingData",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluation_periods": "evaluationPeriods",
        "period": "period",
        "threshold": "threshold",
        "alarm_description": "alarmDescription",
        "alarm_name": "alarmName",
    },
)
class SnsNumberOfNotificationsDeliveredAlarmConfig(SnsAlarmBaseConfig):
    def __init__(
        self,
        *,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        threshold: jsii.Number,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration for the NumberOfNotificationsDelivered alarm.

        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 5
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 5
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param threshold: The value against which the specified statistic is compared. The number of messages delivered should be in line with the expected number of messages produced and the number of consumers. You can also analyze the historical data, trends and traffic to find the right threshold.
        :param alarm_description: The description of the alarm. Default: - This alarm can detect when the number of SNS messages delivered is too low. This could be because of unintentional unsubscribing of an endpoint, or because of an SNS event that causes messages to experience delay.
        :param alarm_name: The alarm name. Default: - topic.topicName + ' - NumberOfNotificationsDelivered'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b868a50184ae2ac664cf01403a36fff774472e3686b89e5367994e98b89b7193)
            check_type(argname="argument alarm_action", value=alarm_action, expected_type=type_hints["alarm_action"])
            check_type(argname="argument insufficient_data_action", value=insufficient_data_action, expected_type=type_hints["insufficient_data_action"])
            check_type(argname="argument ok_action", value=ok_action, expected_type=type_hints["ok_action"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument alarm_description", value=alarm_description, expected_type=type_hints["alarm_description"])
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "threshold": threshold,
        }
        if alarm_action is not None:
            self._values["alarm_action"] = alarm_action
        if insufficient_data_action is not None:
            self._values["insufficient_data_action"] = insufficient_data_action
        if ok_action is not None:
            self._values["ok_action"] = ok_action
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluation_periods is not None:
            self._values["evaluation_periods"] = evaluation_periods
        if period is not None:
            self._values["period"] = period
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if alarm_name is not None:
            self._values["alarm_name"] = alarm_name

    @builtins.property
    def alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of data points that must be breaching to trigger the alarm.

        :default: 5
        '''
        result = self._values.get("datapoints_to_alarm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''The number of periods over which data is compared to the specified threshold.

        :default: 5
        '''
        result = self._values.get("evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The period over which the specified statistic is applied.

        :default: Duration.minutes(1)
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def threshold(self) -> jsii.Number:
        '''The value against which the specified statistic is compared.

        The number of messages delivered should be in line with the expected number of
        messages produced and the number of consumers. You can also analyze the historical
        data, trends and traffic to find the right threshold.
        '''
        result = self._values.get("threshold")
        assert result is not None, "Required property 'threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        '''The description of the alarm.

        :default:

        - This alarm can detect when the number of SNS messages delivered is too low.
        This could be because of unintentional unsubscribing of an endpoint, or because of
        an SNS event that causes messages to experience delay.
        '''
        result = self._values.get("alarm_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_name(self) -> typing.Optional[builtins.str]:
        '''The alarm name.

        :default: - topic.topicName + ' - NumberOfNotificationsDelivered'
        '''
        result = self._values.get("alarm_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SnsNumberOfNotificationsDeliveredAlarmConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.SnsNumberOfNotificationsDeliveredAlarmProps",
    jsii_struct_bases=[SnsNumberOfNotificationsDeliveredAlarmConfig],
    name_mapping={
        "alarm_action": "alarmAction",
        "insufficient_data_action": "insufficientDataAction",
        "ok_action": "okAction",
        "treat_missing_data": "treatMissingData",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluation_periods": "evaluationPeriods",
        "period": "period",
        "threshold": "threshold",
        "alarm_description": "alarmDescription",
        "alarm_name": "alarmName",
        "topic": "topic",
    },
)
class SnsNumberOfNotificationsDeliveredAlarmProps(
    SnsNumberOfNotificationsDeliveredAlarmConfig,
):
    def __init__(
        self,
        *,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        threshold: jsii.Number,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        topic: _aws_cdk_aws_sns_ceddda9d.ITopic,
    ) -> None:
        '''Properties for the SnsNumberOfNotificationsDeliveredAlarm construct.

        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 5
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 5
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param threshold: The value against which the specified statistic is compared. The number of messages delivered should be in line with the expected number of messages produced and the number of consumers. You can also analyze the historical data, trends and traffic to find the right threshold.
        :param alarm_description: The description of the alarm. Default: - This alarm can detect when the number of SNS messages delivered is too low. This could be because of unintentional unsubscribing of an endpoint, or because of an SNS event that causes messages to experience delay.
        :param alarm_name: The alarm name. Default: - topic.topicName + ' - NumberOfNotificationsDelivered'
        :param topic: The SNS topic for which to create the alarm.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f42d7a4b791067bced9bc860e1f750a1ceba252cff97a6f74fd0c6a844a539e)
            check_type(argname="argument alarm_action", value=alarm_action, expected_type=type_hints["alarm_action"])
            check_type(argname="argument insufficient_data_action", value=insufficient_data_action, expected_type=type_hints["insufficient_data_action"])
            check_type(argname="argument ok_action", value=ok_action, expected_type=type_hints["ok_action"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument alarm_description", value=alarm_description, expected_type=type_hints["alarm_description"])
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "threshold": threshold,
            "topic": topic,
        }
        if alarm_action is not None:
            self._values["alarm_action"] = alarm_action
        if insufficient_data_action is not None:
            self._values["insufficient_data_action"] = insufficient_data_action
        if ok_action is not None:
            self._values["ok_action"] = ok_action
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluation_periods is not None:
            self._values["evaluation_periods"] = evaluation_periods
        if period is not None:
            self._values["period"] = period
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if alarm_name is not None:
            self._values["alarm_name"] = alarm_name

    @builtins.property
    def alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of data points that must be breaching to trigger the alarm.

        :default: 5
        '''
        result = self._values.get("datapoints_to_alarm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''The number of periods over which data is compared to the specified threshold.

        :default: 5
        '''
        result = self._values.get("evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The period over which the specified statistic is applied.

        :default: Duration.minutes(1)
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def threshold(self) -> jsii.Number:
        '''The value against which the specified statistic is compared.

        The number of messages delivered should be in line with the expected number of
        messages produced and the number of consumers. You can also analyze the historical
        data, trends and traffic to find the right threshold.
        '''
        result = self._values.get("threshold")
        assert result is not None, "Required property 'threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        '''The description of the alarm.

        :default:

        - This alarm can detect when the number of SNS messages delivered is too low.
        This could be because of unintentional unsubscribing of an endpoint, or because of
        an SNS event that causes messages to experience delay.
        '''
        result = self._values.get("alarm_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_name(self) -> typing.Optional[builtins.str]:
        '''The alarm name.

        :default: - topic.topicName + ' - NumberOfNotificationsDelivered'
        '''
        result = self._values.get("alarm_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def topic(self) -> _aws_cdk_aws_sns_ceddda9d.ITopic:
        '''The SNS topic for which to create the alarm.'''
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return typing.cast(_aws_cdk_aws_sns_ceddda9d.ITopic, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SnsNumberOfNotificationsDeliveredAlarmProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SnsNumberOfNotificationsFailedAlarm(
    _aws_cdk_aws_cloudwatch_ceddda9d.Alarm,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.SnsNumberOfNotificationsFailedAlarm",
):
    '''An alarm that monitors the number of notifications failed by an SNS topic.

    This alarm helps you proactively find issues with the delivery of notifications
    and take appropriate actions to address them.

    The alarm is triggered when the number of messages failed by the topic
    is greater than the specified threshold.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        topic: _aws_cdk_aws_sns_ceddda9d.ITopic,
        threshold: jsii.Number,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param topic: The SNS topic for which to create the alarm.
        :param threshold: The value against which the specified statistic is compared. The recommended threshold value for this alarm is highly dependent on the impact of failed notifications. Review the SLAs provided to your end users, fault tolerance and criticality of notifications and analyze historical data, and then select a threshold accordingly. The number of notifications failed should be 0 for topics that have only SQS, Lambda or Firehose subscriptions.
        :param alarm_description: The description of the alarm. Default: - This alarm can detect when the number of failed SNS messages is too high. To troubleshoot failed notifications, enable logging to CloudWatch Logs. Checking the logs can help you find which subscribers are failing, as well as the status codes they are returning.
        :param alarm_name: The alarm name. Default: - topic.topicName + ' - NumberOfNotificationsFailed'
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 5
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 5
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__170e0b0914195c00ff510974ac188dcdce904364b454920cfa694a9c41aea277)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SnsNumberOfNotificationsFailedAlarmProps(
            topic=topic,
            threshold=threshold,
            alarm_description=alarm_description,
            alarm_name=alarm_name,
            datapoints_to_alarm=datapoints_to_alarm,
            evaluation_periods=evaluation_periods,
            period=period,
            alarm_action=alarm_action,
            insufficient_data_action=insufficient_data_action,
            ok_action=ok_action,
            treat_missing_data=treat_missing_data,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.SnsNumberOfNotificationsFailedAlarmConfig",
    jsii_struct_bases=[SnsAlarmBaseConfig],
    name_mapping={
        "alarm_action": "alarmAction",
        "insufficient_data_action": "insufficientDataAction",
        "ok_action": "okAction",
        "treat_missing_data": "treatMissingData",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluation_periods": "evaluationPeriods",
        "period": "period",
        "threshold": "threshold",
        "alarm_description": "alarmDescription",
        "alarm_name": "alarmName",
    },
)
class SnsNumberOfNotificationsFailedAlarmConfig(SnsAlarmBaseConfig):
    def __init__(
        self,
        *,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        threshold: jsii.Number,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration for the NumberOfNotificationsFailed alarm.

        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 5
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 5
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param threshold: The value against which the specified statistic is compared. The recommended threshold value for this alarm is highly dependent on the impact of failed notifications. Review the SLAs provided to your end users, fault tolerance and criticality of notifications and analyze historical data, and then select a threshold accordingly. The number of notifications failed should be 0 for topics that have only SQS, Lambda or Firehose subscriptions.
        :param alarm_description: The description of the alarm. Default: - This alarm can detect when the number of failed SNS messages is too high. To troubleshoot failed notifications, enable logging to CloudWatch Logs. Checking the logs can help you find which subscribers are failing, as well as the status codes they are returning.
        :param alarm_name: The alarm name. Default: - topic.topicName + ' - NumberOfNotificationsFailed'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49e12faa9093bf4d0205ccf60bc9d460839db4afed6958548942f1f348123faa)
            check_type(argname="argument alarm_action", value=alarm_action, expected_type=type_hints["alarm_action"])
            check_type(argname="argument insufficient_data_action", value=insufficient_data_action, expected_type=type_hints["insufficient_data_action"])
            check_type(argname="argument ok_action", value=ok_action, expected_type=type_hints["ok_action"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument alarm_description", value=alarm_description, expected_type=type_hints["alarm_description"])
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "threshold": threshold,
        }
        if alarm_action is not None:
            self._values["alarm_action"] = alarm_action
        if insufficient_data_action is not None:
            self._values["insufficient_data_action"] = insufficient_data_action
        if ok_action is not None:
            self._values["ok_action"] = ok_action
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluation_periods is not None:
            self._values["evaluation_periods"] = evaluation_periods
        if period is not None:
            self._values["period"] = period
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if alarm_name is not None:
            self._values["alarm_name"] = alarm_name

    @builtins.property
    def alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of data points that must be breaching to trigger the alarm.

        :default: 5
        '''
        result = self._values.get("datapoints_to_alarm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''The number of periods over which data is compared to the specified threshold.

        :default: 5
        '''
        result = self._values.get("evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The period over which the specified statistic is applied.

        :default: Duration.minutes(1)
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def threshold(self) -> jsii.Number:
        '''The value against which the specified statistic is compared.

        The recommended threshold value for this alarm is highly dependent on the
        impact of failed notifications. Review the SLAs provided to your end users,
        fault tolerance and criticality of notifications and analyze historical data,
        and then select a threshold accordingly. The number of notifications failed
        should be 0 for topics that have only SQS, Lambda or Firehose subscriptions.
        '''
        result = self._values.get("threshold")
        assert result is not None, "Required property 'threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        '''The description of the alarm.

        :default:

        - This alarm can detect when the number of failed SNS messages is too high.
        To troubleshoot failed notifications, enable logging to CloudWatch Logs. Checking
        the logs can help you find which subscribers are failing, as well as the status
        codes they are returning.
        '''
        result = self._values.get("alarm_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_name(self) -> typing.Optional[builtins.str]:
        '''The alarm name.

        :default: - topic.topicName + ' - NumberOfNotificationsFailed'
        '''
        result = self._values.get("alarm_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SnsNumberOfNotificationsFailedAlarmConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.SnsNumberOfNotificationsFailedAlarmProps",
    jsii_struct_bases=[SnsNumberOfNotificationsFailedAlarmConfig],
    name_mapping={
        "alarm_action": "alarmAction",
        "insufficient_data_action": "insufficientDataAction",
        "ok_action": "okAction",
        "treat_missing_data": "treatMissingData",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluation_periods": "evaluationPeriods",
        "period": "period",
        "threshold": "threshold",
        "alarm_description": "alarmDescription",
        "alarm_name": "alarmName",
        "topic": "topic",
    },
)
class SnsNumberOfNotificationsFailedAlarmProps(
    SnsNumberOfNotificationsFailedAlarmConfig,
):
    def __init__(
        self,
        *,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        threshold: jsii.Number,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        topic: _aws_cdk_aws_sns_ceddda9d.ITopic,
    ) -> None:
        '''Properties for the SnsNumberOfNotificationsFailedAlarm construct.

        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 5
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 5
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param threshold: The value against which the specified statistic is compared. The recommended threshold value for this alarm is highly dependent on the impact of failed notifications. Review the SLAs provided to your end users, fault tolerance and criticality of notifications and analyze historical data, and then select a threshold accordingly. The number of notifications failed should be 0 for topics that have only SQS, Lambda or Firehose subscriptions.
        :param alarm_description: The description of the alarm. Default: - This alarm can detect when the number of failed SNS messages is too high. To troubleshoot failed notifications, enable logging to CloudWatch Logs. Checking the logs can help you find which subscribers are failing, as well as the status codes they are returning.
        :param alarm_name: The alarm name. Default: - topic.topicName + ' - NumberOfNotificationsFailed'
        :param topic: The SNS topic for which to create the alarm.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__892a2b84330c3cd2ff63a79b19f87b73eb88ccfb60ed575de749f562223b34f0)
            check_type(argname="argument alarm_action", value=alarm_action, expected_type=type_hints["alarm_action"])
            check_type(argname="argument insufficient_data_action", value=insufficient_data_action, expected_type=type_hints["insufficient_data_action"])
            check_type(argname="argument ok_action", value=ok_action, expected_type=type_hints["ok_action"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument alarm_description", value=alarm_description, expected_type=type_hints["alarm_description"])
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "threshold": threshold,
            "topic": topic,
        }
        if alarm_action is not None:
            self._values["alarm_action"] = alarm_action
        if insufficient_data_action is not None:
            self._values["insufficient_data_action"] = insufficient_data_action
        if ok_action is not None:
            self._values["ok_action"] = ok_action
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluation_periods is not None:
            self._values["evaluation_periods"] = evaluation_periods
        if period is not None:
            self._values["period"] = period
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if alarm_name is not None:
            self._values["alarm_name"] = alarm_name

    @builtins.property
    def alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of data points that must be breaching to trigger the alarm.

        :default: 5
        '''
        result = self._values.get("datapoints_to_alarm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''The number of periods over which data is compared to the specified threshold.

        :default: 5
        '''
        result = self._values.get("evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The period over which the specified statistic is applied.

        :default: Duration.minutes(1)
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def threshold(self) -> jsii.Number:
        '''The value against which the specified statistic is compared.

        The recommended threshold value for this alarm is highly dependent on the
        impact of failed notifications. Review the SLAs provided to your end users,
        fault tolerance and criticality of notifications and analyze historical data,
        and then select a threshold accordingly. The number of notifications failed
        should be 0 for topics that have only SQS, Lambda or Firehose subscriptions.
        '''
        result = self._values.get("threshold")
        assert result is not None, "Required property 'threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        '''The description of the alarm.

        :default:

        - This alarm can detect when the number of failed SNS messages is too high.
        To troubleshoot failed notifications, enable logging to CloudWatch Logs. Checking
        the logs can help you find which subscribers are failing, as well as the status
        codes they are returning.
        '''
        result = self._values.get("alarm_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_name(self) -> typing.Optional[builtins.str]:
        '''The alarm name.

        :default: - topic.topicName + ' - NumberOfNotificationsFailed'
        '''
        result = self._values.get("alarm_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def topic(self) -> _aws_cdk_aws_sns_ceddda9d.ITopic:
        '''The SNS topic for which to create the alarm.'''
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return typing.cast(_aws_cdk_aws_sns_ceddda9d.ITopic, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SnsNumberOfNotificationsFailedAlarmProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SnsNumberOfNotificationsFailedToRedriveToDlqAlarm(
    _aws_cdk_aws_cloudwatch_ceddda9d.Alarm,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.SnsNumberOfNotificationsFailedToRedriveToDlqAlarm",
):
    '''An alarm that monitors the number of notifications failed to redrive to the dead-letter queue.

    The alarm is used to detect messages that couldn't be moved to a dead-letter
    queue.

    The alarm is triggered when the number of messages failed to redrive to the
    dead-letter queue is greater than the specified threshold.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        topic: _aws_cdk_aws_sns_ceddda9d.ITopic,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        threshold: typing.Optional[jsii.Number] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param topic: The SNS topic for which to create the alarm.
        :param alarm_description: The description of the alarm. Default: - This alarm helps to monitor messages that couldn't be moved to a dead-letter queue. Check whether your dead-letter queue exists and that it's configured correctly. Also, verify that SNS has permissions to access the dead-letter queue. Refer to the dead-letter queue documentation (https://docs.aws.amazon.com/sns/latest/dg/sns-dead-letter-queues.html) to learn more.
        :param alarm_name: The alarm name. Default: - topic.topicName + ' - NumberOfNotificationsFailedToRedriveToDlq'
        :param threshold: The value against which the specified statistic is compared. It's almost always a mistake if messages can't be moved to the dead-letter queue. The recommendation for the threshold is 0, meaning all messages that fail processing must be able to reach the dead-letter queue when the queue has been configured. Default: 0
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 5
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 5
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__328952b7f137facf3708a3106b8d39dc7959798db5ba6df8bb7ee4ef4e058cfb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SnsNumberOfNotificationsFailedToRedriveToDlqAlarmProps(
            topic=topic,
            alarm_description=alarm_description,
            alarm_name=alarm_name,
            threshold=threshold,
            datapoints_to_alarm=datapoints_to_alarm,
            evaluation_periods=evaluation_periods,
            period=period,
            alarm_action=alarm_action,
            insufficient_data_action=insufficient_data_action,
            ok_action=ok_action,
            treat_missing_data=treat_missing_data,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.SnsNumberOfNotificationsFailedToRedriveToDlqAlarmConfig",
    jsii_struct_bases=[SnsAlarmBaseConfig],
    name_mapping={
        "alarm_action": "alarmAction",
        "insufficient_data_action": "insufficientDataAction",
        "ok_action": "okAction",
        "treat_missing_data": "treatMissingData",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluation_periods": "evaluationPeriods",
        "period": "period",
        "alarm_description": "alarmDescription",
        "alarm_name": "alarmName",
        "threshold": "threshold",
    },
)
class SnsNumberOfNotificationsFailedToRedriveToDlqAlarmConfig(SnsAlarmBaseConfig):
    def __init__(
        self,
        *,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Configuration for the NumberOfNotificationsFailedToRedriveToDlq alarm.

        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 5
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 5
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param alarm_description: The description of the alarm. Default: - This alarm helps to monitor messages that couldn't be moved to a dead-letter queue. Check whether your dead-letter queue exists and that it's configured correctly. Also, verify that SNS has permissions to access the dead-letter queue. Refer to the dead-letter queue documentation (https://docs.aws.amazon.com/sns/latest/dg/sns-dead-letter-queues.html) to learn more.
        :param alarm_name: The alarm name. Default: - topic.topicName + ' - NumberOfNotificationsFailedToRedriveToDlq'
        :param threshold: The value against which the specified statistic is compared. It's almost always a mistake if messages can't be moved to the dead-letter queue. The recommendation for the threshold is 0, meaning all messages that fail processing must be able to reach the dead-letter queue when the queue has been configured. Default: 0
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__843a4ee9894a844d5695f53e1c878efbf75b200de41a577d4f371b236240f2e8)
            check_type(argname="argument alarm_action", value=alarm_action, expected_type=type_hints["alarm_action"])
            check_type(argname="argument insufficient_data_action", value=insufficient_data_action, expected_type=type_hints["insufficient_data_action"])
            check_type(argname="argument ok_action", value=ok_action, expected_type=type_hints["ok_action"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument alarm_description", value=alarm_description, expected_type=type_hints["alarm_description"])
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alarm_action is not None:
            self._values["alarm_action"] = alarm_action
        if insufficient_data_action is not None:
            self._values["insufficient_data_action"] = insufficient_data_action
        if ok_action is not None:
            self._values["ok_action"] = ok_action
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluation_periods is not None:
            self._values["evaluation_periods"] = evaluation_periods
        if period is not None:
            self._values["period"] = period
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if alarm_name is not None:
            self._values["alarm_name"] = alarm_name
        if threshold is not None:
            self._values["threshold"] = threshold

    @builtins.property
    def alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of data points that must be breaching to trigger the alarm.

        :default: 5
        '''
        result = self._values.get("datapoints_to_alarm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''The number of periods over which data is compared to the specified threshold.

        :default: 5
        '''
        result = self._values.get("evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The period over which the specified statistic is applied.

        :default: Duration.minutes(1)
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        '''The description of the alarm.

        :default:

        - This alarm helps to monitor messages that couldn't be moved to a dead-letter
        queue. Check whether your dead-letter queue exists and that it's configured correctly.
        Also, verify that SNS has permissions to access the dead-letter queue. Refer to the
        dead-letter queue documentation (https://docs.aws.amazon.com/sns/latest/dg/sns-dead-letter-queues.html)
        to learn more.
        '''
        result = self._values.get("alarm_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_name(self) -> typing.Optional[builtins.str]:
        '''The alarm name.

        :default: - topic.topicName + ' - NumberOfNotificationsFailedToRedriveToDlq'
        '''
        result = self._values.get("alarm_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def threshold(self) -> typing.Optional[jsii.Number]:
        '''The value against which the specified statistic is compared.

        It's almost always a mistake if messages can't be moved to the dead-letter queue.
        The recommendation for the threshold is 0, meaning all messages that fail processing
        must be able to reach the dead-letter queue when the queue has been configured.

        :default: 0
        '''
        result = self._values.get("threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SnsNumberOfNotificationsFailedToRedriveToDlqAlarmConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.SnsNumberOfNotificationsFailedToRedriveToDlqAlarmProps",
    jsii_struct_bases=[SnsNumberOfNotificationsFailedToRedriveToDlqAlarmConfig],
    name_mapping={
        "alarm_action": "alarmAction",
        "insufficient_data_action": "insufficientDataAction",
        "ok_action": "okAction",
        "treat_missing_data": "treatMissingData",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluation_periods": "evaluationPeriods",
        "period": "period",
        "alarm_description": "alarmDescription",
        "alarm_name": "alarmName",
        "threshold": "threshold",
        "topic": "topic",
    },
)
class SnsNumberOfNotificationsFailedToRedriveToDlqAlarmProps(
    SnsNumberOfNotificationsFailedToRedriveToDlqAlarmConfig,
):
    def __init__(
        self,
        *,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        threshold: typing.Optional[jsii.Number] = None,
        topic: _aws_cdk_aws_sns_ceddda9d.ITopic,
    ) -> None:
        '''Properties for the SnsNumberOfNotificationsFailedToRedriveToDlqAlarm construct.

        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 5
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 5
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param alarm_description: The description of the alarm. Default: - This alarm helps to monitor messages that couldn't be moved to a dead-letter queue. Check whether your dead-letter queue exists and that it's configured correctly. Also, verify that SNS has permissions to access the dead-letter queue. Refer to the dead-letter queue documentation (https://docs.aws.amazon.com/sns/latest/dg/sns-dead-letter-queues.html) to learn more.
        :param alarm_name: The alarm name. Default: - topic.topicName + ' - NumberOfNotificationsFailedToRedriveToDlq'
        :param threshold: The value against which the specified statistic is compared. It's almost always a mistake if messages can't be moved to the dead-letter queue. The recommendation for the threshold is 0, meaning all messages that fail processing must be able to reach the dead-letter queue when the queue has been configured. Default: 0
        :param topic: The SNS topic for which to create the alarm.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3739e80c1d6309d7906dad7d9e84785a3a83e15921d956349e5a35ee350151b)
            check_type(argname="argument alarm_action", value=alarm_action, expected_type=type_hints["alarm_action"])
            check_type(argname="argument insufficient_data_action", value=insufficient_data_action, expected_type=type_hints["insufficient_data_action"])
            check_type(argname="argument ok_action", value=ok_action, expected_type=type_hints["ok_action"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument alarm_description", value=alarm_description, expected_type=type_hints["alarm_description"])
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "topic": topic,
        }
        if alarm_action is not None:
            self._values["alarm_action"] = alarm_action
        if insufficient_data_action is not None:
            self._values["insufficient_data_action"] = insufficient_data_action
        if ok_action is not None:
            self._values["ok_action"] = ok_action
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluation_periods is not None:
            self._values["evaluation_periods"] = evaluation_periods
        if period is not None:
            self._values["period"] = period
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if alarm_name is not None:
            self._values["alarm_name"] = alarm_name
        if threshold is not None:
            self._values["threshold"] = threshold

    @builtins.property
    def alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of data points that must be breaching to trigger the alarm.

        :default: 5
        '''
        result = self._values.get("datapoints_to_alarm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''The number of periods over which data is compared to the specified threshold.

        :default: 5
        '''
        result = self._values.get("evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The period over which the specified statistic is applied.

        :default: Duration.minutes(1)
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        '''The description of the alarm.

        :default:

        - This alarm helps to monitor messages that couldn't be moved to a dead-letter
        queue. Check whether your dead-letter queue exists and that it's configured correctly.
        Also, verify that SNS has permissions to access the dead-letter queue. Refer to the
        dead-letter queue documentation (https://docs.aws.amazon.com/sns/latest/dg/sns-dead-letter-queues.html)
        to learn more.
        '''
        result = self._values.get("alarm_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_name(self) -> typing.Optional[builtins.str]:
        '''The alarm name.

        :default: - topic.topicName + ' - NumberOfNotificationsFailedToRedriveToDlq'
        '''
        result = self._values.get("alarm_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def threshold(self) -> typing.Optional[jsii.Number]:
        '''The value against which the specified statistic is compared.

        It's almost always a mistake if messages can't be moved to the dead-letter queue.
        The recommendation for the threshold is 0, meaning all messages that fail processing
        must be able to reach the dead-letter queue when the queue has been configured.

        :default: 0
        '''
        result = self._values.get("threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def topic(self) -> _aws_cdk_aws_sns_ceddda9d.ITopic:
        '''The SNS topic for which to create the alarm.'''
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return typing.cast(_aws_cdk_aws_sns_ceddda9d.ITopic, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SnsNumberOfNotificationsFailedToRedriveToDlqAlarmProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SnsNumberOfNotificationsFilteredOutInvalidAttributesAlarm(
    _aws_cdk_aws_cloudwatch_ceddda9d.Alarm,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.SnsNumberOfNotificationsFilteredOutInvalidAttributesAlarm",
):
    '''An alarm that monitors the number of notifications filtered out due to invalid attributes.

    The alarm is used to detect if the published messages are not valid or
    if inappropriate filters have been applied to a subscriber.

    The alarm is triggered when the number of messages filtered out due to
    invalid attributes is greater than the specified threshold.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        topic: _aws_cdk_aws_sns_ceddda9d.ITopic,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        threshold: typing.Optional[jsii.Number] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param topic: The SNS topic for which to create the alarm.
        :param alarm_description: The description of the alarm. Default: - This alarm helps to monitor and resolve potential problems with the publisher or subscribers. Check if a publisher is publishing messages with invalid attributes or if an inappropriate filter is applied to a subscriber. You can also analyze CloudWatch Logs to help find the root cause of the issue.
        :param alarm_name: The alarm name. Default: - topic.topicName + ' - NumberOfNotificationsFilteredOut-InvalidAttributes'
        :param threshold: The value against which the specified statistic is compared. Invalid attributes are almost always a mistake by the publisher. We recommend to set the threshold to 0 because invalid attributes are not expected in a healthy system. Default: 0
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 5
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 5
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43139b7affdf7f55134351c485459ce357015c4e7c697ae842d1c8d514b65565)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SnsNumberOfNotificationsFilteredOutInvalidAttributesAlarmProps(
            topic=topic,
            alarm_description=alarm_description,
            alarm_name=alarm_name,
            threshold=threshold,
            datapoints_to_alarm=datapoints_to_alarm,
            evaluation_periods=evaluation_periods,
            period=period,
            alarm_action=alarm_action,
            insufficient_data_action=insufficient_data_action,
            ok_action=ok_action,
            treat_missing_data=treat_missing_data,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.SnsNumberOfNotificationsFilteredOutInvalidAttributesAlarmConfig",
    jsii_struct_bases=[SnsAlarmBaseConfig],
    name_mapping={
        "alarm_action": "alarmAction",
        "insufficient_data_action": "insufficientDataAction",
        "ok_action": "okAction",
        "treat_missing_data": "treatMissingData",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluation_periods": "evaluationPeriods",
        "period": "period",
        "alarm_description": "alarmDescription",
        "alarm_name": "alarmName",
        "threshold": "threshold",
    },
)
class SnsNumberOfNotificationsFilteredOutInvalidAttributesAlarmConfig(
    SnsAlarmBaseConfig,
):
    def __init__(
        self,
        *,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Configuration for the NumberOfNotificationsFilteredOutInvalidAttributes alarm.

        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 5
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 5
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param alarm_description: The description of the alarm. Default: - This alarm helps to monitor and resolve potential problems with the publisher or subscribers. Check if a publisher is publishing messages with invalid attributes or if an inappropriate filter is applied to a subscriber. You can also analyze CloudWatch Logs to help find the root cause of the issue.
        :param alarm_name: The alarm name. Default: - topic.topicName + ' - NumberOfNotificationsFilteredOut-InvalidAttributes'
        :param threshold: The value against which the specified statistic is compared. Invalid attributes are almost always a mistake by the publisher. We recommend to set the threshold to 0 because invalid attributes are not expected in a healthy system. Default: 0
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec0121c20b9a0c13a285aa11cf4f02cfa52f0fa656d8e6a0359dce149cf04fcf)
            check_type(argname="argument alarm_action", value=alarm_action, expected_type=type_hints["alarm_action"])
            check_type(argname="argument insufficient_data_action", value=insufficient_data_action, expected_type=type_hints["insufficient_data_action"])
            check_type(argname="argument ok_action", value=ok_action, expected_type=type_hints["ok_action"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument alarm_description", value=alarm_description, expected_type=type_hints["alarm_description"])
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alarm_action is not None:
            self._values["alarm_action"] = alarm_action
        if insufficient_data_action is not None:
            self._values["insufficient_data_action"] = insufficient_data_action
        if ok_action is not None:
            self._values["ok_action"] = ok_action
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluation_periods is not None:
            self._values["evaluation_periods"] = evaluation_periods
        if period is not None:
            self._values["period"] = period
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if alarm_name is not None:
            self._values["alarm_name"] = alarm_name
        if threshold is not None:
            self._values["threshold"] = threshold

    @builtins.property
    def alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of data points that must be breaching to trigger the alarm.

        :default: 5
        '''
        result = self._values.get("datapoints_to_alarm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''The number of periods over which data is compared to the specified threshold.

        :default: 5
        '''
        result = self._values.get("evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The period over which the specified statistic is applied.

        :default: Duration.minutes(1)
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        '''The description of the alarm.

        :default:

        - This alarm helps to monitor and resolve potential problems with the publisher or subscribers.
        Check if a publisher is publishing messages with invalid attributes or if an inappropriate filter is
        applied to a subscriber. You can also analyze CloudWatch Logs to help find the root cause of the issue.
        '''
        result = self._values.get("alarm_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_name(self) -> typing.Optional[builtins.str]:
        '''The alarm name.

        :default: - topic.topicName + ' - NumberOfNotificationsFilteredOut-InvalidAttributes'
        '''
        result = self._values.get("alarm_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def threshold(self) -> typing.Optional[jsii.Number]:
        '''The value against which the specified statistic is compared.

        Invalid attributes are almost always a mistake by the publisher. We recommend
        to set the threshold to 0 because invalid attributes are not expected in a
        healthy system.

        :default: 0
        '''
        result = self._values.get("threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SnsNumberOfNotificationsFilteredOutInvalidAttributesAlarmConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.SnsNumberOfNotificationsFilteredOutInvalidAttributesAlarmProps",
    jsii_struct_bases=[
        SnsNumberOfNotificationsFilteredOutInvalidAttributesAlarmConfig
    ],
    name_mapping={
        "alarm_action": "alarmAction",
        "insufficient_data_action": "insufficientDataAction",
        "ok_action": "okAction",
        "treat_missing_data": "treatMissingData",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluation_periods": "evaluationPeriods",
        "period": "period",
        "alarm_description": "alarmDescription",
        "alarm_name": "alarmName",
        "threshold": "threshold",
        "topic": "topic",
    },
)
class SnsNumberOfNotificationsFilteredOutInvalidAttributesAlarmProps(
    SnsNumberOfNotificationsFilteredOutInvalidAttributesAlarmConfig,
):
    def __init__(
        self,
        *,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        threshold: typing.Optional[jsii.Number] = None,
        topic: _aws_cdk_aws_sns_ceddda9d.ITopic,
    ) -> None:
        '''Properties for the SnsNumberOfNotificationsFilteredOutInvalidAttributesAlarm construct.

        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 5
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 5
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param alarm_description: The description of the alarm. Default: - This alarm helps to monitor and resolve potential problems with the publisher or subscribers. Check if a publisher is publishing messages with invalid attributes or if an inappropriate filter is applied to a subscriber. You can also analyze CloudWatch Logs to help find the root cause of the issue.
        :param alarm_name: The alarm name. Default: - topic.topicName + ' - NumberOfNotificationsFilteredOut-InvalidAttributes'
        :param threshold: The value against which the specified statistic is compared. Invalid attributes are almost always a mistake by the publisher. We recommend to set the threshold to 0 because invalid attributes are not expected in a healthy system. Default: 0
        :param topic: The SNS topic for which to create the alarm.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75001c0fbc3b728c4c377f661f9af34f7b2005073f8201f295eda55eecf79ff2)
            check_type(argname="argument alarm_action", value=alarm_action, expected_type=type_hints["alarm_action"])
            check_type(argname="argument insufficient_data_action", value=insufficient_data_action, expected_type=type_hints["insufficient_data_action"])
            check_type(argname="argument ok_action", value=ok_action, expected_type=type_hints["ok_action"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument alarm_description", value=alarm_description, expected_type=type_hints["alarm_description"])
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "topic": topic,
        }
        if alarm_action is not None:
            self._values["alarm_action"] = alarm_action
        if insufficient_data_action is not None:
            self._values["insufficient_data_action"] = insufficient_data_action
        if ok_action is not None:
            self._values["ok_action"] = ok_action
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluation_periods is not None:
            self._values["evaluation_periods"] = evaluation_periods
        if period is not None:
            self._values["period"] = period
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if alarm_name is not None:
            self._values["alarm_name"] = alarm_name
        if threshold is not None:
            self._values["threshold"] = threshold

    @builtins.property
    def alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of data points that must be breaching to trigger the alarm.

        :default: 5
        '''
        result = self._values.get("datapoints_to_alarm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''The number of periods over which data is compared to the specified threshold.

        :default: 5
        '''
        result = self._values.get("evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The period over which the specified statistic is applied.

        :default: Duration.minutes(1)
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        '''The description of the alarm.

        :default:

        - This alarm helps to monitor and resolve potential problems with the publisher or subscribers.
        Check if a publisher is publishing messages with invalid attributes or if an inappropriate filter is
        applied to a subscriber. You can also analyze CloudWatch Logs to help find the root cause of the issue.
        '''
        result = self._values.get("alarm_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_name(self) -> typing.Optional[builtins.str]:
        '''The alarm name.

        :default: - topic.topicName + ' - NumberOfNotificationsFilteredOut-InvalidAttributes'
        '''
        result = self._values.get("alarm_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def threshold(self) -> typing.Optional[jsii.Number]:
        '''The value against which the specified statistic is compared.

        Invalid attributes are almost always a mistake by the publisher. We recommend
        to set the threshold to 0 because invalid attributes are not expected in a
        healthy system.

        :default: 0
        '''
        result = self._values.get("threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def topic(self) -> _aws_cdk_aws_sns_ceddda9d.ITopic:
        '''The SNS topic for which to create the alarm.'''
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return typing.cast(_aws_cdk_aws_sns_ceddda9d.ITopic, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SnsNumberOfNotificationsFilteredOutInvalidAttributesAlarmProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SnsNumberOfNotificationsFilteredOutInvalidMessageBodyAlarm(
    _aws_cdk_aws_cloudwatch_ceddda9d.Alarm,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.SnsNumberOfNotificationsFilteredOutInvalidMessageBodyAlarm",
):
    '''An alarm that monitors the number of notifications filtered out due to invalid message body.

    The alarm is used to detect if the published messages are not valid or
    if inappropriate filters have been applied to a subscriber.

    The alarm is triggered when the number of messages filtered out due to
    invalid message body is greater than the specified threshold.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        topic: _aws_cdk_aws_sns_ceddda9d.ITopic,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        threshold: typing.Optional[jsii.Number] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param topic: The SNS topic for which to create the alarm.
        :param alarm_description: The description of the alarm. Default: - This alarm helps to monitor and resolve potential problems with the publisher or subscribers. Check if a publisher is publishing messages with invalid message bodies, or if an inappropriate filter is applied to a subscriber. You can also analyze CloudWatch Logs to help find the root cause of the issue.
        :param alarm_name: The alarm name. Default: - topic.topicName + ' - NumberOfNotificationsFilteredOut-InvalidMessageBody'
        :param threshold: The value against which the specified statistic is compared. Invalid message bodies are almost always a mistake by the publisher. We recommend to set the threshold to 0 because invalid message bodies are not expected in a healthy system. Default: 0
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 5
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 5
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b0eb47a2c3fa8f34233ebb68267787d38ab91e5dbd2e593d54eb6b6833c21bb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SnsNumberOfNotificationsFilteredOutInvalidMessageBodyAlarmProps(
            topic=topic,
            alarm_description=alarm_description,
            alarm_name=alarm_name,
            threshold=threshold,
            datapoints_to_alarm=datapoints_to_alarm,
            evaluation_periods=evaluation_periods,
            period=period,
            alarm_action=alarm_action,
            insufficient_data_action=insufficient_data_action,
            ok_action=ok_action,
            treat_missing_data=treat_missing_data,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.SnsNumberOfNotificationsFilteredOutInvalidMessageBodyAlarmConfig",
    jsii_struct_bases=[SnsAlarmBaseConfig],
    name_mapping={
        "alarm_action": "alarmAction",
        "insufficient_data_action": "insufficientDataAction",
        "ok_action": "okAction",
        "treat_missing_data": "treatMissingData",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluation_periods": "evaluationPeriods",
        "period": "period",
        "alarm_description": "alarmDescription",
        "alarm_name": "alarmName",
        "threshold": "threshold",
    },
)
class SnsNumberOfNotificationsFilteredOutInvalidMessageBodyAlarmConfig(
    SnsAlarmBaseConfig,
):
    def __init__(
        self,
        *,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Configuration for the NumberOfNotificationsFilteredOutInvalidMessageBody alarm.

        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 5
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 5
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param alarm_description: The description of the alarm. Default: - This alarm helps to monitor and resolve potential problems with the publisher or subscribers. Check if a publisher is publishing messages with invalid message bodies, or if an inappropriate filter is applied to a subscriber. You can also analyze CloudWatch Logs to help find the root cause of the issue.
        :param alarm_name: The alarm name. Default: - topic.topicName + ' - NumberOfNotificationsFilteredOut-InvalidMessageBody'
        :param threshold: The value against which the specified statistic is compared. Invalid message bodies are almost always a mistake by the publisher. We recommend to set the threshold to 0 because invalid message bodies are not expected in a healthy system. Default: 0
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7144b6b471d3381a8a22ad7e1411624239d41faade4130e5d45a811d5546fe73)
            check_type(argname="argument alarm_action", value=alarm_action, expected_type=type_hints["alarm_action"])
            check_type(argname="argument insufficient_data_action", value=insufficient_data_action, expected_type=type_hints["insufficient_data_action"])
            check_type(argname="argument ok_action", value=ok_action, expected_type=type_hints["ok_action"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument alarm_description", value=alarm_description, expected_type=type_hints["alarm_description"])
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alarm_action is not None:
            self._values["alarm_action"] = alarm_action
        if insufficient_data_action is not None:
            self._values["insufficient_data_action"] = insufficient_data_action
        if ok_action is not None:
            self._values["ok_action"] = ok_action
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluation_periods is not None:
            self._values["evaluation_periods"] = evaluation_periods
        if period is not None:
            self._values["period"] = period
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if alarm_name is not None:
            self._values["alarm_name"] = alarm_name
        if threshold is not None:
            self._values["threshold"] = threshold

    @builtins.property
    def alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of data points that must be breaching to trigger the alarm.

        :default: 5
        '''
        result = self._values.get("datapoints_to_alarm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''The number of periods over which data is compared to the specified threshold.

        :default: 5
        '''
        result = self._values.get("evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The period over which the specified statistic is applied.

        :default: Duration.minutes(1)
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        '''The description of the alarm.

        :default:

        - This alarm helps to monitor and resolve potential problems with the
        publisher or subscribers. Check if a publisher is publishing messages with
        invalid message bodies, or if an inappropriate filter is applied to a subscriber.
        You can also analyze CloudWatch Logs to help find the root cause of the issue.
        '''
        result = self._values.get("alarm_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_name(self) -> typing.Optional[builtins.str]:
        '''The alarm name.

        :default: - topic.topicName + ' - NumberOfNotificationsFilteredOut-InvalidMessageBody'
        '''
        result = self._values.get("alarm_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def threshold(self) -> typing.Optional[jsii.Number]:
        '''The value against which the specified statistic is compared.

        Invalid message bodies are almost always a mistake by the publisher.
        We recommend to set the threshold to 0 because invalid message bodies
        are not expected in a healthy system.

        :default: 0
        '''
        result = self._values.get("threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SnsNumberOfNotificationsFilteredOutInvalidMessageBodyAlarmConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.SnsNumberOfNotificationsFilteredOutInvalidMessageBodyAlarmProps",
    jsii_struct_bases=[
        SnsNumberOfNotificationsFilteredOutInvalidMessageBodyAlarmConfig
    ],
    name_mapping={
        "alarm_action": "alarmAction",
        "insufficient_data_action": "insufficientDataAction",
        "ok_action": "okAction",
        "treat_missing_data": "treatMissingData",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluation_periods": "evaluationPeriods",
        "period": "period",
        "alarm_description": "alarmDescription",
        "alarm_name": "alarmName",
        "threshold": "threshold",
        "topic": "topic",
    },
)
class SnsNumberOfNotificationsFilteredOutInvalidMessageBodyAlarmProps(
    SnsNumberOfNotificationsFilteredOutInvalidMessageBodyAlarmConfig,
):
    def __init__(
        self,
        *,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        threshold: typing.Optional[jsii.Number] = None,
        topic: _aws_cdk_aws_sns_ceddda9d.ITopic,
    ) -> None:
        '''Properties for the SnsNumberOfNotificationsFilteredOutInvalidMessageBodyAlarm construct.

        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 5
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 5
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param alarm_description: The description of the alarm. Default: - This alarm helps to monitor and resolve potential problems with the publisher or subscribers. Check if a publisher is publishing messages with invalid message bodies, or if an inappropriate filter is applied to a subscriber. You can also analyze CloudWatch Logs to help find the root cause of the issue.
        :param alarm_name: The alarm name. Default: - topic.topicName + ' - NumberOfNotificationsFilteredOut-InvalidMessageBody'
        :param threshold: The value against which the specified statistic is compared. Invalid message bodies are almost always a mistake by the publisher. We recommend to set the threshold to 0 because invalid message bodies are not expected in a healthy system. Default: 0
        :param topic: The SNS topic for which to create the alarm.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68a91c07dfcbd0aacb0e3c594d36678ba3a1e134a863504ce2a39c87c7da0221)
            check_type(argname="argument alarm_action", value=alarm_action, expected_type=type_hints["alarm_action"])
            check_type(argname="argument insufficient_data_action", value=insufficient_data_action, expected_type=type_hints["insufficient_data_action"])
            check_type(argname="argument ok_action", value=ok_action, expected_type=type_hints["ok_action"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument alarm_description", value=alarm_description, expected_type=type_hints["alarm_description"])
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "topic": topic,
        }
        if alarm_action is not None:
            self._values["alarm_action"] = alarm_action
        if insufficient_data_action is not None:
            self._values["insufficient_data_action"] = insufficient_data_action
        if ok_action is not None:
            self._values["ok_action"] = ok_action
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluation_periods is not None:
            self._values["evaluation_periods"] = evaluation_periods
        if period is not None:
            self._values["period"] = period
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if alarm_name is not None:
            self._values["alarm_name"] = alarm_name
        if threshold is not None:
            self._values["threshold"] = threshold

    @builtins.property
    def alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of data points that must be breaching to trigger the alarm.

        :default: 5
        '''
        result = self._values.get("datapoints_to_alarm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''The number of periods over which data is compared to the specified threshold.

        :default: 5
        '''
        result = self._values.get("evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The period over which the specified statistic is applied.

        :default: Duration.minutes(1)
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        '''The description of the alarm.

        :default:

        - This alarm helps to monitor and resolve potential problems with the
        publisher or subscribers. Check if a publisher is publishing messages with
        invalid message bodies, or if an inappropriate filter is applied to a subscriber.
        You can also analyze CloudWatch Logs to help find the root cause of the issue.
        '''
        result = self._values.get("alarm_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_name(self) -> typing.Optional[builtins.str]:
        '''The alarm name.

        :default: - topic.topicName + ' - NumberOfNotificationsFilteredOut-InvalidMessageBody'
        '''
        result = self._values.get("alarm_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def threshold(self) -> typing.Optional[jsii.Number]:
        '''The value against which the specified statistic is compared.

        Invalid message bodies are almost always a mistake by the publisher.
        We recommend to set the threshold to 0 because invalid message bodies
        are not expected in a healthy system.

        :default: 0
        '''
        result = self._values.get("threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def topic(self) -> _aws_cdk_aws_sns_ceddda9d.ITopic:
        '''The SNS topic for which to create the alarm.'''
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return typing.cast(_aws_cdk_aws_sns_ceddda9d.ITopic, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SnsNumberOfNotificationsFilteredOutInvalidMessageBodyAlarmProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SnsNumberOfNotificationsRedrivenToDlqAlarm(
    _aws_cdk_aws_cloudwatch_ceddda9d.Alarm,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.SnsNumberOfNotificationsRedrivenToDlqAlarm",
):
    '''An alarm that monitors the number of notifications redriven to the dead-letter queue.

    The alarm is used to detect messages that moved to a dead-letter
    queue. We recommend that you create this alarm when SNS is coupled
    with SQS, Lambda or Firehose.

    The alarm is triggered when the number of messages redriven to the
    dead-letter queue is greater than the specified threshold.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        topic: _aws_cdk_aws_sns_ceddda9d.ITopic,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        threshold: typing.Optional[jsii.Number] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param topic: The SNS topic for which to create the alarm.
        :param alarm_description: The description of the alarm. Default: - This alarm helps to monitor the number of messages that are moved to a dead-letter queue.
        :param alarm_name: The alarm name. Default: - topic.topicName + ' - NumberOfNotificationsRedrivenToDlq'
        :param threshold: The value against which the specified statistic is compared. In a healthy system of any subscriber type, messages should not be moved to the dead-letter queue. We recommend that you be notified if any messages land in the queue, so that you can identify and address the root cause, and potentially redrive the messages in the dead-letter queue to prevent data loss. Default: 0
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 5
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 5
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5333c0338ea3e3f055d2c8daafb1ec07493b232256425a8befa7dc813db863eb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SnsNumberOfNotificationsRedrivenToDlqAlarmProps(
            topic=topic,
            alarm_description=alarm_description,
            alarm_name=alarm_name,
            threshold=threshold,
            datapoints_to_alarm=datapoints_to_alarm,
            evaluation_periods=evaluation_periods,
            period=period,
            alarm_action=alarm_action,
            insufficient_data_action=insufficient_data_action,
            ok_action=ok_action,
            treat_missing_data=treat_missing_data,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.SnsNumberOfNotificationsRedrivenToDlqAlarmConfig",
    jsii_struct_bases=[SnsAlarmBaseConfig],
    name_mapping={
        "alarm_action": "alarmAction",
        "insufficient_data_action": "insufficientDataAction",
        "ok_action": "okAction",
        "treat_missing_data": "treatMissingData",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluation_periods": "evaluationPeriods",
        "period": "period",
        "alarm_description": "alarmDescription",
        "alarm_name": "alarmName",
        "threshold": "threshold",
    },
)
class SnsNumberOfNotificationsRedrivenToDlqAlarmConfig(SnsAlarmBaseConfig):
    def __init__(
        self,
        *,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Configuration for the NumberOfNotificationsRedrivenToDlq alarm.

        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 5
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 5
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param alarm_description: The description of the alarm. Default: - This alarm helps to monitor the number of messages that are moved to a dead-letter queue.
        :param alarm_name: The alarm name. Default: - topic.topicName + ' - NumberOfNotificationsRedrivenToDlq'
        :param threshold: The value against which the specified statistic is compared. In a healthy system of any subscriber type, messages should not be moved to the dead-letter queue. We recommend that you be notified if any messages land in the queue, so that you can identify and address the root cause, and potentially redrive the messages in the dead-letter queue to prevent data loss. Default: 0
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62b63074ae7184f232bd0e5938c481c0494ea3e231fea4a6974e72aca3250ee9)
            check_type(argname="argument alarm_action", value=alarm_action, expected_type=type_hints["alarm_action"])
            check_type(argname="argument insufficient_data_action", value=insufficient_data_action, expected_type=type_hints["insufficient_data_action"])
            check_type(argname="argument ok_action", value=ok_action, expected_type=type_hints["ok_action"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument alarm_description", value=alarm_description, expected_type=type_hints["alarm_description"])
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alarm_action is not None:
            self._values["alarm_action"] = alarm_action
        if insufficient_data_action is not None:
            self._values["insufficient_data_action"] = insufficient_data_action
        if ok_action is not None:
            self._values["ok_action"] = ok_action
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluation_periods is not None:
            self._values["evaluation_periods"] = evaluation_periods
        if period is not None:
            self._values["period"] = period
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if alarm_name is not None:
            self._values["alarm_name"] = alarm_name
        if threshold is not None:
            self._values["threshold"] = threshold

    @builtins.property
    def alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of data points that must be breaching to trigger the alarm.

        :default: 5
        '''
        result = self._values.get("datapoints_to_alarm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''The number of periods over which data is compared to the specified threshold.

        :default: 5
        '''
        result = self._values.get("evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The period over which the specified statistic is applied.

        :default: Duration.minutes(1)
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        '''The description of the alarm.

        :default: - This alarm helps to monitor the number of messages that are moved to a dead-letter queue.
        '''
        result = self._values.get("alarm_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_name(self) -> typing.Optional[builtins.str]:
        '''The alarm name.

        :default: - topic.topicName + ' - NumberOfNotificationsRedrivenToDlq'
        '''
        result = self._values.get("alarm_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def threshold(self) -> typing.Optional[jsii.Number]:
        '''The value against which the specified statistic is compared.

        In a healthy system of any subscriber type, messages should not be moved
        to the dead-letter queue. We recommend that you be notified if any messages
        land in the queue, so that you can identify and address the root cause,
        and potentially redrive the messages in the dead-letter queue to prevent
        data loss.

        :default: 0
        '''
        result = self._values.get("threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SnsNumberOfNotificationsRedrivenToDlqAlarmConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.SnsNumberOfNotificationsRedrivenToDlqAlarmProps",
    jsii_struct_bases=[SnsNumberOfNotificationsRedrivenToDlqAlarmConfig],
    name_mapping={
        "alarm_action": "alarmAction",
        "insufficient_data_action": "insufficientDataAction",
        "ok_action": "okAction",
        "treat_missing_data": "treatMissingData",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluation_periods": "evaluationPeriods",
        "period": "period",
        "alarm_description": "alarmDescription",
        "alarm_name": "alarmName",
        "threshold": "threshold",
        "topic": "topic",
    },
)
class SnsNumberOfNotificationsRedrivenToDlqAlarmProps(
    SnsNumberOfNotificationsRedrivenToDlqAlarmConfig,
):
    def __init__(
        self,
        *,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        threshold: typing.Optional[jsii.Number] = None,
        topic: _aws_cdk_aws_sns_ceddda9d.ITopic,
    ) -> None:
        '''Properties for the SnsNumberOfNotificationsRedrivenToDlqAlarm construct.

        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 5
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 5
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param alarm_description: The description of the alarm. Default: - This alarm helps to monitor the number of messages that are moved to a dead-letter queue.
        :param alarm_name: The alarm name. Default: - topic.topicName + ' - NumberOfNotificationsRedrivenToDlq'
        :param threshold: The value against which the specified statistic is compared. In a healthy system of any subscriber type, messages should not be moved to the dead-letter queue. We recommend that you be notified if any messages land in the queue, so that you can identify and address the root cause, and potentially redrive the messages in the dead-letter queue to prevent data loss. Default: 0
        :param topic: The SNS topic for which to create the alarm.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2f1df38bb641261070fb8b92d0e55844593ac7973d092bf2fd4d6763627299e)
            check_type(argname="argument alarm_action", value=alarm_action, expected_type=type_hints["alarm_action"])
            check_type(argname="argument insufficient_data_action", value=insufficient_data_action, expected_type=type_hints["insufficient_data_action"])
            check_type(argname="argument ok_action", value=ok_action, expected_type=type_hints["ok_action"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument alarm_description", value=alarm_description, expected_type=type_hints["alarm_description"])
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "topic": topic,
        }
        if alarm_action is not None:
            self._values["alarm_action"] = alarm_action
        if insufficient_data_action is not None:
            self._values["insufficient_data_action"] = insufficient_data_action
        if ok_action is not None:
            self._values["ok_action"] = ok_action
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluation_periods is not None:
            self._values["evaluation_periods"] = evaluation_periods
        if period is not None:
            self._values["period"] = period
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if alarm_name is not None:
            self._values["alarm_name"] = alarm_name
        if threshold is not None:
            self._values["threshold"] = threshold

    @builtins.property
    def alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of data points that must be breaching to trigger the alarm.

        :default: 5
        '''
        result = self._values.get("datapoints_to_alarm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''The number of periods over which data is compared to the specified threshold.

        :default: 5
        '''
        result = self._values.get("evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The period over which the specified statistic is applied.

        :default: Duration.minutes(1)
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        '''The description of the alarm.

        :default: - This alarm helps to monitor the number of messages that are moved to a dead-letter queue.
        '''
        result = self._values.get("alarm_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_name(self) -> typing.Optional[builtins.str]:
        '''The alarm name.

        :default: - topic.topicName + ' - NumberOfNotificationsRedrivenToDlq'
        '''
        result = self._values.get("alarm_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def threshold(self) -> typing.Optional[jsii.Number]:
        '''The value against which the specified statistic is compared.

        In a healthy system of any subscriber type, messages should not be moved
        to the dead-letter queue. We recommend that you be notified if any messages
        land in the queue, so that you can identify and address the root cause,
        and potentially redrive the messages in the dead-letter queue to prevent
        data loss.

        :default: 0
        '''
        result = self._values.get("threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def topic(self) -> _aws_cdk_aws_sns_ceddda9d.ITopic:
        '''The SNS topic for which to create the alarm.'''
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return typing.cast(_aws_cdk_aws_sns_ceddda9d.ITopic, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SnsNumberOfNotificationsRedrivenToDlqAlarmProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SnsRecommendedAlarms(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.SnsRecommendedAlarms",
):
    '''A construct that creates recommended alarms for an SNS topic.

    :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Best_Practice_Recommended_Alarms_AWS_Services.html#SNS
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        topic: _aws_cdk_aws_sns_ceddda9d.ITopic,
        config_number_of_messages_published_alarm: typing.Union[SnsNumberOfMessagesPublishedAlarmConfig, typing.Dict[builtins.str, typing.Any]],
        config_number_of_notifications_delivered_alarm: typing.Union[SnsNumberOfNotificationsDeliveredAlarmConfig, typing.Dict[builtins.str, typing.Any]],
        config_number_of_notifications_failed_alarm: typing.Union[SnsNumberOfNotificationsFailedAlarmConfig, typing.Dict[builtins.str, typing.Any]],
        config_number_of_notifications_failed_to_redrive_to_dlq_alarm: typing.Optional[typing.Union[SnsNumberOfNotificationsFailedToRedriveToDlqAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        config_number_of_notifications_filtered_out_invalid_attributes_alarm: typing.Optional[typing.Union[SnsNumberOfNotificationsFilteredOutInvalidAttributesAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        config_number_of_notifications_filtered_out_invalid_message_body_alarm: typing.Optional[typing.Union[SnsNumberOfNotificationsFilteredOutInvalidMessageBodyAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        config_number_of_notifications_redriven_to_dlq_alarm: typing.Optional[typing.Union[SnsNumberOfNotificationsRedrivenToDlqAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        default_alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        default_insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        default_ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        exclude_alarms: typing.Optional[typing.Sequence["SnsRecommendedAlarmsMetrics"]] = None,
        exclude_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param topic: The SNS topic for which to create the alarms.
        :param config_number_of_messages_published_alarm: The configuration for the NumberOfMessagesPublished alarm.
        :param config_number_of_notifications_delivered_alarm: The configuration for the NumberOfNotificationsDelivered alarm.
        :param config_number_of_notifications_failed_alarm: The configuration for the NumberOfNotificationsFailed alarm.
        :param config_number_of_notifications_failed_to_redrive_to_dlq_alarm: The configuration for the NumberOfNotificationsFailedToRedriveToDlq alarm.
        :param config_number_of_notifications_filtered_out_invalid_attributes_alarm: The configuration for the NumberOfNotificationsFilteredOutInvalidAttributes alarm.
        :param config_number_of_notifications_filtered_out_invalid_message_body_alarm: The configuration for the NumberOfNotificationsFilteredOutInvalidMessageBody alarm.
        :param config_number_of_notifications_redriven_to_dlq_alarm: The configuration for the NumberOfNotificationsRedrivenToDlq alarm.
        :param default_alarm_action: The default action to take when an alarm is triggered. Default: - None
        :param default_insufficient_data_action: The default action to take when an alarm has insufficient data. Default: - None
        :param default_ok_action: The default action to take when an alarm enters the ok state. Default: - None
        :param exclude_alarms: Alarm metrics to exclude from the recommended alarms. Default: - None
        :param exclude_resources: The resources to exclude from the recommended alarms. Use a resources id to exclude a specific resource.
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98630e12118de7c882d18933f387c3a322a8c8af12b4b511ecf7e03804a5775d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SnsRecommendedAlarmsProps(
            topic=topic,
            config_number_of_messages_published_alarm=config_number_of_messages_published_alarm,
            config_number_of_notifications_delivered_alarm=config_number_of_notifications_delivered_alarm,
            config_number_of_notifications_failed_alarm=config_number_of_notifications_failed_alarm,
            config_number_of_notifications_failed_to_redrive_to_dlq_alarm=config_number_of_notifications_failed_to_redrive_to_dlq_alarm,
            config_number_of_notifications_filtered_out_invalid_attributes_alarm=config_number_of_notifications_filtered_out_invalid_attributes_alarm,
            config_number_of_notifications_filtered_out_invalid_message_body_alarm=config_number_of_notifications_filtered_out_invalid_message_body_alarm,
            config_number_of_notifications_redriven_to_dlq_alarm=config_number_of_notifications_redriven_to_dlq_alarm,
            default_alarm_action=default_alarm_action,
            default_insufficient_data_action=default_insufficient_data_action,
            default_ok_action=default_ok_action,
            exclude_alarms=exclude_alarms,
            exclude_resources=exclude_resources,
            treat_missing_data=treat_missing_data,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="alarmNumberOfMessagesPublished")
    def alarm_number_of_messages_published(
        self,
    ) -> typing.Optional[SnsNumberOfMessagesPublishedAlarm]:
        '''The NumberOfMessagesPublished alarm.'''
        return typing.cast(typing.Optional[SnsNumberOfMessagesPublishedAlarm], jsii.get(self, "alarmNumberOfMessagesPublished"))

    @builtins.property
    @jsii.member(jsii_name="alarmNumberOfNotificationsDelivered")
    def alarm_number_of_notifications_delivered(
        self,
    ) -> typing.Optional[SnsNumberOfNotificationsDeliveredAlarm]:
        '''The NumberOfNotificationsDelivered alarm.'''
        return typing.cast(typing.Optional[SnsNumberOfNotificationsDeliveredAlarm], jsii.get(self, "alarmNumberOfNotificationsDelivered"))

    @builtins.property
    @jsii.member(jsii_name="alarmNumberOfNotificationsFailed")
    def alarm_number_of_notifications_failed(
        self,
    ) -> typing.Optional[SnsNumberOfNotificationsFailedAlarm]:
        '''The NumberOfNotificationsFailed alarm.'''
        return typing.cast(typing.Optional[SnsNumberOfNotificationsFailedAlarm], jsii.get(self, "alarmNumberOfNotificationsFailed"))

    @builtins.property
    @jsii.member(jsii_name="alarmNumberOfNotificationsFailedToRedriveToDlq")
    def alarm_number_of_notifications_failed_to_redrive_to_dlq(
        self,
    ) -> typing.Optional[SnsNumberOfNotificationsFailedToRedriveToDlqAlarm]:
        '''The NumberOfNotificationsFailedToRedriveToDlq alarm.'''
        return typing.cast(typing.Optional[SnsNumberOfNotificationsFailedToRedriveToDlqAlarm], jsii.get(self, "alarmNumberOfNotificationsFailedToRedriveToDlq"))

    @builtins.property
    @jsii.member(jsii_name="alarmNumberOfNotificationsFilteredOutInvalidAttributes")
    def alarm_number_of_notifications_filtered_out_invalid_attributes(
        self,
    ) -> typing.Optional[SnsNumberOfNotificationsFilteredOutInvalidAttributesAlarm]:
        '''The NumberOfNotificationsFilteredOutInvalidAttributes alarm.'''
        return typing.cast(typing.Optional[SnsNumberOfNotificationsFilteredOutInvalidAttributesAlarm], jsii.get(self, "alarmNumberOfNotificationsFilteredOutInvalidAttributes"))

    @builtins.property
    @jsii.member(jsii_name="alarmNumberOfNotificationsFilteredOutInvalidMessageBody")
    def alarm_number_of_notifications_filtered_out_invalid_message_body(
        self,
    ) -> typing.Optional[SnsNumberOfNotificationsFilteredOutInvalidMessageBodyAlarm]:
        '''The NumberOfNotificationsFilteredOutInvalidMessageBody alarm.'''
        return typing.cast(typing.Optional[SnsNumberOfNotificationsFilteredOutInvalidMessageBodyAlarm], jsii.get(self, "alarmNumberOfNotificationsFilteredOutInvalidMessageBody"))

    @builtins.property
    @jsii.member(jsii_name="alarmNumberOfNotificationsRedrivenToDlq")
    def alarm_number_of_notifications_redriven_to_dlq(
        self,
    ) -> typing.Optional[SnsNumberOfNotificationsRedrivenToDlqAlarm]:
        '''The NumberOfNotificationsRedrivenToDlq alarm.'''
        return typing.cast(typing.Optional[SnsNumberOfNotificationsRedrivenToDlqAlarm], jsii.get(self, "alarmNumberOfNotificationsRedrivenToDlq"))


@jsii.implements(_aws_cdk_ceddda9d.IAspect)
class SnsRecommendedAlarmsAspect(
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.SnsRecommendedAlarmsAspect",
):
    '''An aspect that applies recommended alarms to SNS topics.

    :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Best_Practice_Recommended_Alarms_AWS_Services.html#SNS
    '''

    def __init__(
        self,
        *,
        config_number_of_messages_published_alarm: typing.Union[SnsNumberOfMessagesPublishedAlarmConfig, typing.Dict[builtins.str, typing.Any]],
        config_number_of_notifications_delivered_alarm: typing.Union[SnsNumberOfNotificationsDeliveredAlarmConfig, typing.Dict[builtins.str, typing.Any]],
        config_number_of_notifications_failed_alarm: typing.Union[SnsNumberOfNotificationsFailedAlarmConfig, typing.Dict[builtins.str, typing.Any]],
        config_number_of_notifications_failed_to_redrive_to_dlq_alarm: typing.Optional[typing.Union[SnsNumberOfNotificationsFailedToRedriveToDlqAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        config_number_of_notifications_filtered_out_invalid_attributes_alarm: typing.Optional[typing.Union[SnsNumberOfNotificationsFilteredOutInvalidAttributesAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        config_number_of_notifications_filtered_out_invalid_message_body_alarm: typing.Optional[typing.Union[SnsNumberOfNotificationsFilteredOutInvalidMessageBodyAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        config_number_of_notifications_redriven_to_dlq_alarm: typing.Optional[typing.Union[SnsNumberOfNotificationsRedrivenToDlqAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        default_alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        default_insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        default_ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        exclude_alarms: typing.Optional[typing.Sequence["SnsRecommendedAlarmsMetrics"]] = None,
        exclude_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> None:
        '''
        :param config_number_of_messages_published_alarm: The configuration for the NumberOfMessagesPublished alarm.
        :param config_number_of_notifications_delivered_alarm: The configuration for the NumberOfNotificationsDelivered alarm.
        :param config_number_of_notifications_failed_alarm: The configuration for the NumberOfNotificationsFailed alarm.
        :param config_number_of_notifications_failed_to_redrive_to_dlq_alarm: The configuration for the NumberOfNotificationsFailedToRedriveToDlq alarm.
        :param config_number_of_notifications_filtered_out_invalid_attributes_alarm: The configuration for the NumberOfNotificationsFilteredOutInvalidAttributes alarm.
        :param config_number_of_notifications_filtered_out_invalid_message_body_alarm: The configuration for the NumberOfNotificationsFilteredOutInvalidMessageBody alarm.
        :param config_number_of_notifications_redriven_to_dlq_alarm: The configuration for the NumberOfNotificationsRedrivenToDlq alarm.
        :param default_alarm_action: The default action to take when an alarm is triggered. Default: - None
        :param default_insufficient_data_action: The default action to take when an alarm has insufficient data. Default: - None
        :param default_ok_action: The default action to take when an alarm enters the ok state. Default: - None
        :param exclude_alarms: Alarm metrics to exclude from the recommended alarms. Default: - None
        :param exclude_resources: The resources to exclude from the recommended alarms. Use a resources id to exclude a specific resource.
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        props = SnsRecommendedAlarmsConfig(
            config_number_of_messages_published_alarm=config_number_of_messages_published_alarm,
            config_number_of_notifications_delivered_alarm=config_number_of_notifications_delivered_alarm,
            config_number_of_notifications_failed_alarm=config_number_of_notifications_failed_alarm,
            config_number_of_notifications_failed_to_redrive_to_dlq_alarm=config_number_of_notifications_failed_to_redrive_to_dlq_alarm,
            config_number_of_notifications_filtered_out_invalid_attributes_alarm=config_number_of_notifications_filtered_out_invalid_attributes_alarm,
            config_number_of_notifications_filtered_out_invalid_message_body_alarm=config_number_of_notifications_filtered_out_invalid_message_body_alarm,
            config_number_of_notifications_redriven_to_dlq_alarm=config_number_of_notifications_redriven_to_dlq_alarm,
            default_alarm_action=default_alarm_action,
            default_insufficient_data_action=default_insufficient_data_action,
            default_ok_action=default_ok_action,
            exclude_alarms=exclude_alarms,
            exclude_resources=exclude_resources,
            treat_missing_data=treat_missing_data,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="visit")
    def visit(self, node: _constructs_77d1e7e8.IConstruct) -> None:
        '''All aspects can visit an IConstruct.

        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47c92495ab390db59ffeb1ec15eb639c4bda7f2e6fcc6ab00f48d384d9c0898d)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "visit", [node]))


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.SnsRecommendedAlarmsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "config_number_of_messages_published_alarm": "configNumberOfMessagesPublishedAlarm",
        "config_number_of_notifications_delivered_alarm": "configNumberOfNotificationsDeliveredAlarm",
        "config_number_of_notifications_failed_alarm": "configNumberOfNotificationsFailedAlarm",
        "config_number_of_notifications_failed_to_redrive_to_dlq_alarm": "configNumberOfNotificationsFailedToRedriveToDlqAlarm",
        "config_number_of_notifications_filtered_out_invalid_attributes_alarm": "configNumberOfNotificationsFilteredOutInvalidAttributesAlarm",
        "config_number_of_notifications_filtered_out_invalid_message_body_alarm": "configNumberOfNotificationsFilteredOutInvalidMessageBodyAlarm",
        "config_number_of_notifications_redriven_to_dlq_alarm": "configNumberOfNotificationsRedrivenToDlqAlarm",
        "default_alarm_action": "defaultAlarmAction",
        "default_insufficient_data_action": "defaultInsufficientDataAction",
        "default_ok_action": "defaultOkAction",
        "exclude_alarms": "excludeAlarms",
        "exclude_resources": "excludeResources",
        "treat_missing_data": "treatMissingData",
    },
)
class SnsRecommendedAlarmsConfig:
    def __init__(
        self,
        *,
        config_number_of_messages_published_alarm: typing.Union[SnsNumberOfMessagesPublishedAlarmConfig, typing.Dict[builtins.str, typing.Any]],
        config_number_of_notifications_delivered_alarm: typing.Union[SnsNumberOfNotificationsDeliveredAlarmConfig, typing.Dict[builtins.str, typing.Any]],
        config_number_of_notifications_failed_alarm: typing.Union[SnsNumberOfNotificationsFailedAlarmConfig, typing.Dict[builtins.str, typing.Any]],
        config_number_of_notifications_failed_to_redrive_to_dlq_alarm: typing.Optional[typing.Union[SnsNumberOfNotificationsFailedToRedriveToDlqAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        config_number_of_notifications_filtered_out_invalid_attributes_alarm: typing.Optional[typing.Union[SnsNumberOfNotificationsFilteredOutInvalidAttributesAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        config_number_of_notifications_filtered_out_invalid_message_body_alarm: typing.Optional[typing.Union[SnsNumberOfNotificationsFilteredOutInvalidMessageBodyAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        config_number_of_notifications_redriven_to_dlq_alarm: typing.Optional[typing.Union[SnsNumberOfNotificationsRedrivenToDlqAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        default_alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        default_insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        default_ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        exclude_alarms: typing.Optional[typing.Sequence["SnsRecommendedAlarmsMetrics"]] = None,
        exclude_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> None:
        '''
        :param config_number_of_messages_published_alarm: The configuration for the NumberOfMessagesPublished alarm.
        :param config_number_of_notifications_delivered_alarm: The configuration for the NumberOfNotificationsDelivered alarm.
        :param config_number_of_notifications_failed_alarm: The configuration for the NumberOfNotificationsFailed alarm.
        :param config_number_of_notifications_failed_to_redrive_to_dlq_alarm: The configuration for the NumberOfNotificationsFailedToRedriveToDlq alarm.
        :param config_number_of_notifications_filtered_out_invalid_attributes_alarm: The configuration for the NumberOfNotificationsFilteredOutInvalidAttributes alarm.
        :param config_number_of_notifications_filtered_out_invalid_message_body_alarm: The configuration for the NumberOfNotificationsFilteredOutInvalidMessageBody alarm.
        :param config_number_of_notifications_redriven_to_dlq_alarm: The configuration for the NumberOfNotificationsRedrivenToDlq alarm.
        :param default_alarm_action: The default action to take when an alarm is triggered. Default: - None
        :param default_insufficient_data_action: The default action to take when an alarm has insufficient data. Default: - None
        :param default_ok_action: The default action to take when an alarm enters the ok state. Default: - None
        :param exclude_alarms: Alarm metrics to exclude from the recommended alarms. Default: - None
        :param exclude_resources: The resources to exclude from the recommended alarms. Use a resources id to exclude a specific resource.
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        if isinstance(config_number_of_messages_published_alarm, dict):
            config_number_of_messages_published_alarm = SnsNumberOfMessagesPublishedAlarmConfig(**config_number_of_messages_published_alarm)
        if isinstance(config_number_of_notifications_delivered_alarm, dict):
            config_number_of_notifications_delivered_alarm = SnsNumberOfNotificationsDeliveredAlarmConfig(**config_number_of_notifications_delivered_alarm)
        if isinstance(config_number_of_notifications_failed_alarm, dict):
            config_number_of_notifications_failed_alarm = SnsNumberOfNotificationsFailedAlarmConfig(**config_number_of_notifications_failed_alarm)
        if isinstance(config_number_of_notifications_failed_to_redrive_to_dlq_alarm, dict):
            config_number_of_notifications_failed_to_redrive_to_dlq_alarm = SnsNumberOfNotificationsFailedToRedriveToDlqAlarmConfig(**config_number_of_notifications_failed_to_redrive_to_dlq_alarm)
        if isinstance(config_number_of_notifications_filtered_out_invalid_attributes_alarm, dict):
            config_number_of_notifications_filtered_out_invalid_attributes_alarm = SnsNumberOfNotificationsFilteredOutInvalidAttributesAlarmConfig(**config_number_of_notifications_filtered_out_invalid_attributes_alarm)
        if isinstance(config_number_of_notifications_filtered_out_invalid_message_body_alarm, dict):
            config_number_of_notifications_filtered_out_invalid_message_body_alarm = SnsNumberOfNotificationsFilteredOutInvalidMessageBodyAlarmConfig(**config_number_of_notifications_filtered_out_invalid_message_body_alarm)
        if isinstance(config_number_of_notifications_redriven_to_dlq_alarm, dict):
            config_number_of_notifications_redriven_to_dlq_alarm = SnsNumberOfNotificationsRedrivenToDlqAlarmConfig(**config_number_of_notifications_redriven_to_dlq_alarm)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fecc7466425a3fd89d5693837b979038b44222e821924f36e33e1aea20e4236a)
            check_type(argname="argument config_number_of_messages_published_alarm", value=config_number_of_messages_published_alarm, expected_type=type_hints["config_number_of_messages_published_alarm"])
            check_type(argname="argument config_number_of_notifications_delivered_alarm", value=config_number_of_notifications_delivered_alarm, expected_type=type_hints["config_number_of_notifications_delivered_alarm"])
            check_type(argname="argument config_number_of_notifications_failed_alarm", value=config_number_of_notifications_failed_alarm, expected_type=type_hints["config_number_of_notifications_failed_alarm"])
            check_type(argname="argument config_number_of_notifications_failed_to_redrive_to_dlq_alarm", value=config_number_of_notifications_failed_to_redrive_to_dlq_alarm, expected_type=type_hints["config_number_of_notifications_failed_to_redrive_to_dlq_alarm"])
            check_type(argname="argument config_number_of_notifications_filtered_out_invalid_attributes_alarm", value=config_number_of_notifications_filtered_out_invalid_attributes_alarm, expected_type=type_hints["config_number_of_notifications_filtered_out_invalid_attributes_alarm"])
            check_type(argname="argument config_number_of_notifications_filtered_out_invalid_message_body_alarm", value=config_number_of_notifications_filtered_out_invalid_message_body_alarm, expected_type=type_hints["config_number_of_notifications_filtered_out_invalid_message_body_alarm"])
            check_type(argname="argument config_number_of_notifications_redriven_to_dlq_alarm", value=config_number_of_notifications_redriven_to_dlq_alarm, expected_type=type_hints["config_number_of_notifications_redriven_to_dlq_alarm"])
            check_type(argname="argument default_alarm_action", value=default_alarm_action, expected_type=type_hints["default_alarm_action"])
            check_type(argname="argument default_insufficient_data_action", value=default_insufficient_data_action, expected_type=type_hints["default_insufficient_data_action"])
            check_type(argname="argument default_ok_action", value=default_ok_action, expected_type=type_hints["default_ok_action"])
            check_type(argname="argument exclude_alarms", value=exclude_alarms, expected_type=type_hints["exclude_alarms"])
            check_type(argname="argument exclude_resources", value=exclude_resources, expected_type=type_hints["exclude_resources"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "config_number_of_messages_published_alarm": config_number_of_messages_published_alarm,
            "config_number_of_notifications_delivered_alarm": config_number_of_notifications_delivered_alarm,
            "config_number_of_notifications_failed_alarm": config_number_of_notifications_failed_alarm,
        }
        if config_number_of_notifications_failed_to_redrive_to_dlq_alarm is not None:
            self._values["config_number_of_notifications_failed_to_redrive_to_dlq_alarm"] = config_number_of_notifications_failed_to_redrive_to_dlq_alarm
        if config_number_of_notifications_filtered_out_invalid_attributes_alarm is not None:
            self._values["config_number_of_notifications_filtered_out_invalid_attributes_alarm"] = config_number_of_notifications_filtered_out_invalid_attributes_alarm
        if config_number_of_notifications_filtered_out_invalid_message_body_alarm is not None:
            self._values["config_number_of_notifications_filtered_out_invalid_message_body_alarm"] = config_number_of_notifications_filtered_out_invalid_message_body_alarm
        if config_number_of_notifications_redriven_to_dlq_alarm is not None:
            self._values["config_number_of_notifications_redriven_to_dlq_alarm"] = config_number_of_notifications_redriven_to_dlq_alarm
        if default_alarm_action is not None:
            self._values["default_alarm_action"] = default_alarm_action
        if default_insufficient_data_action is not None:
            self._values["default_insufficient_data_action"] = default_insufficient_data_action
        if default_ok_action is not None:
            self._values["default_ok_action"] = default_ok_action
        if exclude_alarms is not None:
            self._values["exclude_alarms"] = exclude_alarms
        if exclude_resources is not None:
            self._values["exclude_resources"] = exclude_resources
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data

    @builtins.property
    def config_number_of_messages_published_alarm(
        self,
    ) -> SnsNumberOfMessagesPublishedAlarmConfig:
        '''The configuration for the NumberOfMessagesPublished alarm.'''
        result = self._values.get("config_number_of_messages_published_alarm")
        assert result is not None, "Required property 'config_number_of_messages_published_alarm' is missing"
        return typing.cast(SnsNumberOfMessagesPublishedAlarmConfig, result)

    @builtins.property
    def config_number_of_notifications_delivered_alarm(
        self,
    ) -> SnsNumberOfNotificationsDeliveredAlarmConfig:
        '''The configuration for the NumberOfNotificationsDelivered alarm.'''
        result = self._values.get("config_number_of_notifications_delivered_alarm")
        assert result is not None, "Required property 'config_number_of_notifications_delivered_alarm' is missing"
        return typing.cast(SnsNumberOfNotificationsDeliveredAlarmConfig, result)

    @builtins.property
    def config_number_of_notifications_failed_alarm(
        self,
    ) -> SnsNumberOfNotificationsFailedAlarmConfig:
        '''The configuration for the NumberOfNotificationsFailed alarm.'''
        result = self._values.get("config_number_of_notifications_failed_alarm")
        assert result is not None, "Required property 'config_number_of_notifications_failed_alarm' is missing"
        return typing.cast(SnsNumberOfNotificationsFailedAlarmConfig, result)

    @builtins.property
    def config_number_of_notifications_failed_to_redrive_to_dlq_alarm(
        self,
    ) -> typing.Optional[SnsNumberOfNotificationsFailedToRedriveToDlqAlarmConfig]:
        '''The configuration for the NumberOfNotificationsFailedToRedriveToDlq alarm.'''
        result = self._values.get("config_number_of_notifications_failed_to_redrive_to_dlq_alarm")
        return typing.cast(typing.Optional[SnsNumberOfNotificationsFailedToRedriveToDlqAlarmConfig], result)

    @builtins.property
    def config_number_of_notifications_filtered_out_invalid_attributes_alarm(
        self,
    ) -> typing.Optional[SnsNumberOfNotificationsFilteredOutInvalidAttributesAlarmConfig]:
        '''The configuration for the NumberOfNotificationsFilteredOutInvalidAttributes alarm.'''
        result = self._values.get("config_number_of_notifications_filtered_out_invalid_attributes_alarm")
        return typing.cast(typing.Optional[SnsNumberOfNotificationsFilteredOutInvalidAttributesAlarmConfig], result)

    @builtins.property
    def config_number_of_notifications_filtered_out_invalid_message_body_alarm(
        self,
    ) -> typing.Optional[SnsNumberOfNotificationsFilteredOutInvalidMessageBodyAlarmConfig]:
        '''The configuration for the NumberOfNotificationsFilteredOutInvalidMessageBody alarm.'''
        result = self._values.get("config_number_of_notifications_filtered_out_invalid_message_body_alarm")
        return typing.cast(typing.Optional[SnsNumberOfNotificationsFilteredOutInvalidMessageBodyAlarmConfig], result)

    @builtins.property
    def config_number_of_notifications_redriven_to_dlq_alarm(
        self,
    ) -> typing.Optional[SnsNumberOfNotificationsRedrivenToDlqAlarmConfig]:
        '''The configuration for the NumberOfNotificationsRedrivenToDlq alarm.'''
        result = self._values.get("config_number_of_notifications_redriven_to_dlq_alarm")
        return typing.cast(typing.Optional[SnsNumberOfNotificationsRedrivenToDlqAlarmConfig], result)

    @builtins.property
    def default_alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The default action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("default_alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def default_insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The default action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("default_insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def default_ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The default action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("default_ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def exclude_alarms(
        self,
    ) -> typing.Optional[typing.List["SnsRecommendedAlarmsMetrics"]]:
        '''Alarm metrics to exclude from the recommended alarms.

        :default: - None
        '''
        result = self._values.get("exclude_alarms")
        return typing.cast(typing.Optional[typing.List["SnsRecommendedAlarmsMetrics"]], result)

    @builtins.property
    def exclude_resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The resources to exclude from the recommended alarms.

        Use a resources id to exclude a specific resource.
        '''
        result = self._values.get("exclude_resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SnsRecommendedAlarmsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.SnsRecommendedAlarmsMetrics"
)
class SnsRecommendedAlarmsMetrics(enum.Enum):
    '''The recommended metrics for SNS topic alarms.'''

    NUMBER_OF_MESSAGES_PUBLISHED = "NUMBER_OF_MESSAGES_PUBLISHED"
    '''The number of messages published to the topic.'''
    NUMBER_OF_NOTIFICATIONS_DELIVERED = "NUMBER_OF_NOTIFICATIONS_DELIVERED"
    '''The number of notifications delivered.'''
    NUMBER_OF_NOTIFICATIONS_FAILED = "NUMBER_OF_NOTIFICATIONS_FAILED"
    '''The number of notifications failed.'''
    NUMBER_OF_NOTIFICATIONS_FILTERED_OUT_INVALID_ATTRIBUTES = "NUMBER_OF_NOTIFICATIONS_FILTERED_OUT_INVALID_ATTRIBUTES"
    '''The number of notifications filtered out due to invalid attributes.'''
    NUMBER_OF_NOTIFICATIONS_FILTERED_OUT_INVALID_MESSAGE_BODY = "NUMBER_OF_NOTIFICATIONS_FILTERED_OUT_INVALID_MESSAGE_BODY"
    '''The number of notifications filtered out due to invalid message body.'''
    NUMBER_OF_NOTIFICATIONS_REDRIVEN_TO_DLQ = "NUMBER_OF_NOTIFICATIONS_REDRIVEN_TO_DLQ"
    '''The number of notifications redriven to the dead-letter queue.'''
    NUMBER_OF_NOTIFICATIONS_FAILED_TO_REDRIVE_TO_DLQ = "NUMBER_OF_NOTIFICATIONS_FAILED_TO_REDRIVE_TO_DLQ"
    '''The number of notifications failed to redrive to the dead-letter queue.'''


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.SnsRecommendedAlarmsProps",
    jsii_struct_bases=[SnsRecommendedAlarmsConfig],
    name_mapping={
        "config_number_of_messages_published_alarm": "configNumberOfMessagesPublishedAlarm",
        "config_number_of_notifications_delivered_alarm": "configNumberOfNotificationsDeliveredAlarm",
        "config_number_of_notifications_failed_alarm": "configNumberOfNotificationsFailedAlarm",
        "config_number_of_notifications_failed_to_redrive_to_dlq_alarm": "configNumberOfNotificationsFailedToRedriveToDlqAlarm",
        "config_number_of_notifications_filtered_out_invalid_attributes_alarm": "configNumberOfNotificationsFilteredOutInvalidAttributesAlarm",
        "config_number_of_notifications_filtered_out_invalid_message_body_alarm": "configNumberOfNotificationsFilteredOutInvalidMessageBodyAlarm",
        "config_number_of_notifications_redriven_to_dlq_alarm": "configNumberOfNotificationsRedrivenToDlqAlarm",
        "default_alarm_action": "defaultAlarmAction",
        "default_insufficient_data_action": "defaultInsufficientDataAction",
        "default_ok_action": "defaultOkAction",
        "exclude_alarms": "excludeAlarms",
        "exclude_resources": "excludeResources",
        "treat_missing_data": "treatMissingData",
        "topic": "topic",
    },
)
class SnsRecommendedAlarmsProps(SnsRecommendedAlarmsConfig):
    def __init__(
        self,
        *,
        config_number_of_messages_published_alarm: typing.Union[SnsNumberOfMessagesPublishedAlarmConfig, typing.Dict[builtins.str, typing.Any]],
        config_number_of_notifications_delivered_alarm: typing.Union[SnsNumberOfNotificationsDeliveredAlarmConfig, typing.Dict[builtins.str, typing.Any]],
        config_number_of_notifications_failed_alarm: typing.Union[SnsNumberOfNotificationsFailedAlarmConfig, typing.Dict[builtins.str, typing.Any]],
        config_number_of_notifications_failed_to_redrive_to_dlq_alarm: typing.Optional[typing.Union[SnsNumberOfNotificationsFailedToRedriveToDlqAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        config_number_of_notifications_filtered_out_invalid_attributes_alarm: typing.Optional[typing.Union[SnsNumberOfNotificationsFilteredOutInvalidAttributesAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        config_number_of_notifications_filtered_out_invalid_message_body_alarm: typing.Optional[typing.Union[SnsNumberOfNotificationsFilteredOutInvalidMessageBodyAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        config_number_of_notifications_redriven_to_dlq_alarm: typing.Optional[typing.Union[SnsNumberOfNotificationsRedrivenToDlqAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        default_alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        default_insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        default_ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        exclude_alarms: typing.Optional[typing.Sequence[SnsRecommendedAlarmsMetrics]] = None,
        exclude_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
        topic: _aws_cdk_aws_sns_ceddda9d.ITopic,
    ) -> None:
        '''
        :param config_number_of_messages_published_alarm: The configuration for the NumberOfMessagesPublished alarm.
        :param config_number_of_notifications_delivered_alarm: The configuration for the NumberOfNotificationsDelivered alarm.
        :param config_number_of_notifications_failed_alarm: The configuration for the NumberOfNotificationsFailed alarm.
        :param config_number_of_notifications_failed_to_redrive_to_dlq_alarm: The configuration for the NumberOfNotificationsFailedToRedriveToDlq alarm.
        :param config_number_of_notifications_filtered_out_invalid_attributes_alarm: The configuration for the NumberOfNotificationsFilteredOutInvalidAttributes alarm.
        :param config_number_of_notifications_filtered_out_invalid_message_body_alarm: The configuration for the NumberOfNotificationsFilteredOutInvalidMessageBody alarm.
        :param config_number_of_notifications_redriven_to_dlq_alarm: The configuration for the NumberOfNotificationsRedrivenToDlq alarm.
        :param default_alarm_action: The default action to take when an alarm is triggered. Default: - None
        :param default_insufficient_data_action: The default action to take when an alarm has insufficient data. Default: - None
        :param default_ok_action: The default action to take when an alarm enters the ok state. Default: - None
        :param exclude_alarms: Alarm metrics to exclude from the recommended alarms. Default: - None
        :param exclude_resources: The resources to exclude from the recommended alarms. Use a resources id to exclude a specific resource.
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        :param topic: The SNS topic for which to create the alarms.
        '''
        if isinstance(config_number_of_messages_published_alarm, dict):
            config_number_of_messages_published_alarm = SnsNumberOfMessagesPublishedAlarmConfig(**config_number_of_messages_published_alarm)
        if isinstance(config_number_of_notifications_delivered_alarm, dict):
            config_number_of_notifications_delivered_alarm = SnsNumberOfNotificationsDeliveredAlarmConfig(**config_number_of_notifications_delivered_alarm)
        if isinstance(config_number_of_notifications_failed_alarm, dict):
            config_number_of_notifications_failed_alarm = SnsNumberOfNotificationsFailedAlarmConfig(**config_number_of_notifications_failed_alarm)
        if isinstance(config_number_of_notifications_failed_to_redrive_to_dlq_alarm, dict):
            config_number_of_notifications_failed_to_redrive_to_dlq_alarm = SnsNumberOfNotificationsFailedToRedriveToDlqAlarmConfig(**config_number_of_notifications_failed_to_redrive_to_dlq_alarm)
        if isinstance(config_number_of_notifications_filtered_out_invalid_attributes_alarm, dict):
            config_number_of_notifications_filtered_out_invalid_attributes_alarm = SnsNumberOfNotificationsFilteredOutInvalidAttributesAlarmConfig(**config_number_of_notifications_filtered_out_invalid_attributes_alarm)
        if isinstance(config_number_of_notifications_filtered_out_invalid_message_body_alarm, dict):
            config_number_of_notifications_filtered_out_invalid_message_body_alarm = SnsNumberOfNotificationsFilteredOutInvalidMessageBodyAlarmConfig(**config_number_of_notifications_filtered_out_invalid_message_body_alarm)
        if isinstance(config_number_of_notifications_redriven_to_dlq_alarm, dict):
            config_number_of_notifications_redriven_to_dlq_alarm = SnsNumberOfNotificationsRedrivenToDlqAlarmConfig(**config_number_of_notifications_redriven_to_dlq_alarm)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__168fe991294b441d2405431f15f9275f6ff942b8e21e0e325a0459bc7773caf2)
            check_type(argname="argument config_number_of_messages_published_alarm", value=config_number_of_messages_published_alarm, expected_type=type_hints["config_number_of_messages_published_alarm"])
            check_type(argname="argument config_number_of_notifications_delivered_alarm", value=config_number_of_notifications_delivered_alarm, expected_type=type_hints["config_number_of_notifications_delivered_alarm"])
            check_type(argname="argument config_number_of_notifications_failed_alarm", value=config_number_of_notifications_failed_alarm, expected_type=type_hints["config_number_of_notifications_failed_alarm"])
            check_type(argname="argument config_number_of_notifications_failed_to_redrive_to_dlq_alarm", value=config_number_of_notifications_failed_to_redrive_to_dlq_alarm, expected_type=type_hints["config_number_of_notifications_failed_to_redrive_to_dlq_alarm"])
            check_type(argname="argument config_number_of_notifications_filtered_out_invalid_attributes_alarm", value=config_number_of_notifications_filtered_out_invalid_attributes_alarm, expected_type=type_hints["config_number_of_notifications_filtered_out_invalid_attributes_alarm"])
            check_type(argname="argument config_number_of_notifications_filtered_out_invalid_message_body_alarm", value=config_number_of_notifications_filtered_out_invalid_message_body_alarm, expected_type=type_hints["config_number_of_notifications_filtered_out_invalid_message_body_alarm"])
            check_type(argname="argument config_number_of_notifications_redriven_to_dlq_alarm", value=config_number_of_notifications_redriven_to_dlq_alarm, expected_type=type_hints["config_number_of_notifications_redriven_to_dlq_alarm"])
            check_type(argname="argument default_alarm_action", value=default_alarm_action, expected_type=type_hints["default_alarm_action"])
            check_type(argname="argument default_insufficient_data_action", value=default_insufficient_data_action, expected_type=type_hints["default_insufficient_data_action"])
            check_type(argname="argument default_ok_action", value=default_ok_action, expected_type=type_hints["default_ok_action"])
            check_type(argname="argument exclude_alarms", value=exclude_alarms, expected_type=type_hints["exclude_alarms"])
            check_type(argname="argument exclude_resources", value=exclude_resources, expected_type=type_hints["exclude_resources"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "config_number_of_messages_published_alarm": config_number_of_messages_published_alarm,
            "config_number_of_notifications_delivered_alarm": config_number_of_notifications_delivered_alarm,
            "config_number_of_notifications_failed_alarm": config_number_of_notifications_failed_alarm,
            "topic": topic,
        }
        if config_number_of_notifications_failed_to_redrive_to_dlq_alarm is not None:
            self._values["config_number_of_notifications_failed_to_redrive_to_dlq_alarm"] = config_number_of_notifications_failed_to_redrive_to_dlq_alarm
        if config_number_of_notifications_filtered_out_invalid_attributes_alarm is not None:
            self._values["config_number_of_notifications_filtered_out_invalid_attributes_alarm"] = config_number_of_notifications_filtered_out_invalid_attributes_alarm
        if config_number_of_notifications_filtered_out_invalid_message_body_alarm is not None:
            self._values["config_number_of_notifications_filtered_out_invalid_message_body_alarm"] = config_number_of_notifications_filtered_out_invalid_message_body_alarm
        if config_number_of_notifications_redriven_to_dlq_alarm is not None:
            self._values["config_number_of_notifications_redriven_to_dlq_alarm"] = config_number_of_notifications_redriven_to_dlq_alarm
        if default_alarm_action is not None:
            self._values["default_alarm_action"] = default_alarm_action
        if default_insufficient_data_action is not None:
            self._values["default_insufficient_data_action"] = default_insufficient_data_action
        if default_ok_action is not None:
            self._values["default_ok_action"] = default_ok_action
        if exclude_alarms is not None:
            self._values["exclude_alarms"] = exclude_alarms
        if exclude_resources is not None:
            self._values["exclude_resources"] = exclude_resources
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data

    @builtins.property
    def config_number_of_messages_published_alarm(
        self,
    ) -> SnsNumberOfMessagesPublishedAlarmConfig:
        '''The configuration for the NumberOfMessagesPublished alarm.'''
        result = self._values.get("config_number_of_messages_published_alarm")
        assert result is not None, "Required property 'config_number_of_messages_published_alarm' is missing"
        return typing.cast(SnsNumberOfMessagesPublishedAlarmConfig, result)

    @builtins.property
    def config_number_of_notifications_delivered_alarm(
        self,
    ) -> SnsNumberOfNotificationsDeliveredAlarmConfig:
        '''The configuration for the NumberOfNotificationsDelivered alarm.'''
        result = self._values.get("config_number_of_notifications_delivered_alarm")
        assert result is not None, "Required property 'config_number_of_notifications_delivered_alarm' is missing"
        return typing.cast(SnsNumberOfNotificationsDeliveredAlarmConfig, result)

    @builtins.property
    def config_number_of_notifications_failed_alarm(
        self,
    ) -> SnsNumberOfNotificationsFailedAlarmConfig:
        '''The configuration for the NumberOfNotificationsFailed alarm.'''
        result = self._values.get("config_number_of_notifications_failed_alarm")
        assert result is not None, "Required property 'config_number_of_notifications_failed_alarm' is missing"
        return typing.cast(SnsNumberOfNotificationsFailedAlarmConfig, result)

    @builtins.property
    def config_number_of_notifications_failed_to_redrive_to_dlq_alarm(
        self,
    ) -> typing.Optional[SnsNumberOfNotificationsFailedToRedriveToDlqAlarmConfig]:
        '''The configuration for the NumberOfNotificationsFailedToRedriveToDlq alarm.'''
        result = self._values.get("config_number_of_notifications_failed_to_redrive_to_dlq_alarm")
        return typing.cast(typing.Optional[SnsNumberOfNotificationsFailedToRedriveToDlqAlarmConfig], result)

    @builtins.property
    def config_number_of_notifications_filtered_out_invalid_attributes_alarm(
        self,
    ) -> typing.Optional[SnsNumberOfNotificationsFilteredOutInvalidAttributesAlarmConfig]:
        '''The configuration for the NumberOfNotificationsFilteredOutInvalidAttributes alarm.'''
        result = self._values.get("config_number_of_notifications_filtered_out_invalid_attributes_alarm")
        return typing.cast(typing.Optional[SnsNumberOfNotificationsFilteredOutInvalidAttributesAlarmConfig], result)

    @builtins.property
    def config_number_of_notifications_filtered_out_invalid_message_body_alarm(
        self,
    ) -> typing.Optional[SnsNumberOfNotificationsFilteredOutInvalidMessageBodyAlarmConfig]:
        '''The configuration for the NumberOfNotificationsFilteredOutInvalidMessageBody alarm.'''
        result = self._values.get("config_number_of_notifications_filtered_out_invalid_message_body_alarm")
        return typing.cast(typing.Optional[SnsNumberOfNotificationsFilteredOutInvalidMessageBodyAlarmConfig], result)

    @builtins.property
    def config_number_of_notifications_redriven_to_dlq_alarm(
        self,
    ) -> typing.Optional[SnsNumberOfNotificationsRedrivenToDlqAlarmConfig]:
        '''The configuration for the NumberOfNotificationsRedrivenToDlq alarm.'''
        result = self._values.get("config_number_of_notifications_redriven_to_dlq_alarm")
        return typing.cast(typing.Optional[SnsNumberOfNotificationsRedrivenToDlqAlarmConfig], result)

    @builtins.property
    def default_alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The default action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("default_alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def default_insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The default action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("default_insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def default_ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The default action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("default_ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def exclude_alarms(
        self,
    ) -> typing.Optional[typing.List[SnsRecommendedAlarmsMetrics]]:
        '''Alarm metrics to exclude from the recommended alarms.

        :default: - None
        '''
        result = self._values.get("exclude_alarms")
        return typing.cast(typing.Optional[typing.List[SnsRecommendedAlarmsMetrics]], result)

    @builtins.property
    def exclude_resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The resources to exclude from the recommended alarms.

        Use a resources id to exclude a specific resource.
        '''
        result = self._values.get("exclude_resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    @builtins.property
    def topic(self) -> _aws_cdk_aws_sns_ceddda9d.ITopic:
        '''The SNS topic for which to create the alarms.'''
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return typing.cast(_aws_cdk_aws_sns_ceddda9d.ITopic, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SnsRecommendedAlarmsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.SqsAlarmBaseConfig",
    jsii_struct_bases=[AlarmBaseProps],
    name_mapping={
        "alarm_action": "alarmAction",
        "insufficient_data_action": "insufficientDataAction",
        "ok_action": "okAction",
        "treat_missing_data": "treatMissingData",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluation_periods": "evaluationPeriods",
        "period": "period",
    },
)
class SqsAlarmBaseConfig(AlarmBaseProps):
    def __init__(
        self,
        *,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''
        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 15
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 15
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c20302d0dce277cc07fd49ad99fdc8325c29e5d392842004761577330967cdf9)
            check_type(argname="argument alarm_action", value=alarm_action, expected_type=type_hints["alarm_action"])
            check_type(argname="argument insufficient_data_action", value=insufficient_data_action, expected_type=type_hints["insufficient_data_action"])
            check_type(argname="argument ok_action", value=ok_action, expected_type=type_hints["ok_action"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alarm_action is not None:
            self._values["alarm_action"] = alarm_action
        if insufficient_data_action is not None:
            self._values["insufficient_data_action"] = insufficient_data_action
        if ok_action is not None:
            self._values["ok_action"] = ok_action
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluation_periods is not None:
            self._values["evaluation_periods"] = evaluation_periods
        if period is not None:
            self._values["period"] = period

    @builtins.property
    def alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of data points that must be breaching to trigger the alarm.

        :default: 15
        '''
        result = self._values.get("datapoints_to_alarm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''The number of periods over which data is compared to the specified threshold.

        :default: 15
        '''
        result = self._values.get("evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The period over which the specified statistic is applied.

        :default: Duration.minutes(1)
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqsAlarmBaseConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SqsApproximateAgeOfOldestMessageAlarm(
    _aws_cdk_aws_cloudwatch_ceddda9d.Alarm,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.SqsApproximateAgeOfOldestMessageAlarm",
):
    '''An alarm that watches the age of the oldest message in the queue.

    This alarm is used to detect whether the age of the oldest message
    in the QueueName queue is too high. High age can be an indication
    that messages are not processed quickly enough or that there are
    some poison-pill messages that are stuck in the queue and can't
    be processed.

    This alarm is triggered when the age of the oldest message in the
    queue exceeds or is equal to the specified threshold.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        queue: _aws_cdk_aws_sqs_ceddda9d.IQueue,
        threshold: jsii.Number,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param queue: The SQS queue for which to create the alarm.
        :param threshold: The value against which the specified statistic is compared. The recommended threshold value for this alarm is highly dependent on the expected message processing time. You can use historical data to calculate the average message processing time, and then set the threshold to 50% higher than the maximum expected SQS message processing time by queue consumers.
        :param alarm_description: The description of the alarm. Default: - This alarm watches the age of the oldest message in the queue. You can use this alarm to monitor if your consumers are processing SQS messages at the desired speed. Consider increasing the consumer count or consumer throughput to reduce message age. This metric can be used in combination with ApproximateNumberOfMessagesVisible to determine how big the queue backlog is and how quickly messages are being processed. To prevent messages from being deleted before processed, consider configuring the dead-letter queue to sideline potential poison pill messages.
        :param alarm_name: The alarm name. Default: - queue.queueName + ' - ApproximateAgeOfOldestMessage'
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 15
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 15
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c269e40750c6097ce5a8155e6a89289661005b40532df53de2f6994ca311128c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SqsApproximateAgeOfOldestMessageAlarmProps(
            queue=queue,
            threshold=threshold,
            alarm_description=alarm_description,
            alarm_name=alarm_name,
            datapoints_to_alarm=datapoints_to_alarm,
            evaluation_periods=evaluation_periods,
            period=period,
            alarm_action=alarm_action,
            insufficient_data_action=insufficient_data_action,
            ok_action=ok_action,
            treat_missing_data=treat_missing_data,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.SqsApproximateAgeOfOldestMessageAlarmConfig",
    jsii_struct_bases=[SqsAlarmBaseConfig],
    name_mapping={
        "alarm_action": "alarmAction",
        "insufficient_data_action": "insufficientDataAction",
        "ok_action": "okAction",
        "treat_missing_data": "treatMissingData",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluation_periods": "evaluationPeriods",
        "period": "period",
        "threshold": "threshold",
        "alarm_description": "alarmDescription",
        "alarm_name": "alarmName",
    },
)
class SqsApproximateAgeOfOldestMessageAlarmConfig(SqsAlarmBaseConfig):
    def __init__(
        self,
        *,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        threshold: jsii.Number,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration for the ApproximateAgeOfOldestMessage alarm.

        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 15
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 15
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param threshold: The value against which the specified statistic is compared. The recommended threshold value for this alarm is highly dependent on the expected message processing time. You can use historical data to calculate the average message processing time, and then set the threshold to 50% higher than the maximum expected SQS message processing time by queue consumers.
        :param alarm_description: The description of the alarm. Default: - This alarm watches the age of the oldest message in the queue. You can use this alarm to monitor if your consumers are processing SQS messages at the desired speed. Consider increasing the consumer count or consumer throughput to reduce message age. This metric can be used in combination with ApproximateNumberOfMessagesVisible to determine how big the queue backlog is and how quickly messages are being processed. To prevent messages from being deleted before processed, consider configuring the dead-letter queue to sideline potential poison pill messages.
        :param alarm_name: The alarm name. Default: - queue.queueName + ' - ApproximateAgeOfOldestMessage'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aad26aa3cbe4aee8036df6b618af2e6ad6d3e4a19515aee9606ee50dd9af390)
            check_type(argname="argument alarm_action", value=alarm_action, expected_type=type_hints["alarm_action"])
            check_type(argname="argument insufficient_data_action", value=insufficient_data_action, expected_type=type_hints["insufficient_data_action"])
            check_type(argname="argument ok_action", value=ok_action, expected_type=type_hints["ok_action"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument alarm_description", value=alarm_description, expected_type=type_hints["alarm_description"])
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "threshold": threshold,
        }
        if alarm_action is not None:
            self._values["alarm_action"] = alarm_action
        if insufficient_data_action is not None:
            self._values["insufficient_data_action"] = insufficient_data_action
        if ok_action is not None:
            self._values["ok_action"] = ok_action
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluation_periods is not None:
            self._values["evaluation_periods"] = evaluation_periods
        if period is not None:
            self._values["period"] = period
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if alarm_name is not None:
            self._values["alarm_name"] = alarm_name

    @builtins.property
    def alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of data points that must be breaching to trigger the alarm.

        :default: 15
        '''
        result = self._values.get("datapoints_to_alarm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''The number of periods over which data is compared to the specified threshold.

        :default: 15
        '''
        result = self._values.get("evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The period over which the specified statistic is applied.

        :default: Duration.minutes(1)
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def threshold(self) -> jsii.Number:
        '''The value against which the specified statistic is compared.

        The recommended threshold value for this alarm is highly dependent on the expected message
        processing time. You can use historical data to calculate the average message processing time,
        and then set the threshold to 50% higher than the maximum expected SQS message processing
        time by queue consumers.
        '''
        result = self._values.get("threshold")
        assert result is not None, "Required property 'threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        '''The description of the alarm.

        :default:

        - This alarm watches the age of the oldest message in the queue. You can use this alarm
        to monitor if your consumers are processing SQS messages at the desired speed. Consider increasing
        the consumer count or consumer throughput to reduce message age. This metric can be used in
        combination with ApproximateNumberOfMessagesVisible to determine how big the queue backlog is
        and how quickly messages are being processed. To prevent messages from being deleted before processed,
        consider configuring the dead-letter queue to sideline potential poison pill messages.
        '''
        result = self._values.get("alarm_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_name(self) -> typing.Optional[builtins.str]:
        '''The alarm name.

        :default: - queue.queueName + ' - ApproximateAgeOfOldestMessage'
        '''
        result = self._values.get("alarm_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqsApproximateAgeOfOldestMessageAlarmConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.SqsApproximateAgeOfOldestMessageAlarmProps",
    jsii_struct_bases=[SqsApproximateAgeOfOldestMessageAlarmConfig],
    name_mapping={
        "alarm_action": "alarmAction",
        "insufficient_data_action": "insufficientDataAction",
        "ok_action": "okAction",
        "treat_missing_data": "treatMissingData",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluation_periods": "evaluationPeriods",
        "period": "period",
        "threshold": "threshold",
        "alarm_description": "alarmDescription",
        "alarm_name": "alarmName",
        "queue": "queue",
    },
)
class SqsApproximateAgeOfOldestMessageAlarmProps(
    SqsApproximateAgeOfOldestMessageAlarmConfig,
):
    def __init__(
        self,
        *,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        threshold: jsii.Number,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        queue: _aws_cdk_aws_sqs_ceddda9d.IQueue,
    ) -> None:
        '''Properties for the SqsApproximateAgeOfOldestMessageAlarm construct.

        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 15
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 15
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param threshold: The value against which the specified statistic is compared. The recommended threshold value for this alarm is highly dependent on the expected message processing time. You can use historical data to calculate the average message processing time, and then set the threshold to 50% higher than the maximum expected SQS message processing time by queue consumers.
        :param alarm_description: The description of the alarm. Default: - This alarm watches the age of the oldest message in the queue. You can use this alarm to monitor if your consumers are processing SQS messages at the desired speed. Consider increasing the consumer count or consumer throughput to reduce message age. This metric can be used in combination with ApproximateNumberOfMessagesVisible to determine how big the queue backlog is and how quickly messages are being processed. To prevent messages from being deleted before processed, consider configuring the dead-letter queue to sideline potential poison pill messages.
        :param alarm_name: The alarm name. Default: - queue.queueName + ' - ApproximateAgeOfOldestMessage'
        :param queue: The SQS queue for which to create the alarm.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74ca6057ea5178302f3aef8ed4d21ecf4774c7eab9442af8f511543718ffcd83)
            check_type(argname="argument alarm_action", value=alarm_action, expected_type=type_hints["alarm_action"])
            check_type(argname="argument insufficient_data_action", value=insufficient_data_action, expected_type=type_hints["insufficient_data_action"])
            check_type(argname="argument ok_action", value=ok_action, expected_type=type_hints["ok_action"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument alarm_description", value=alarm_description, expected_type=type_hints["alarm_description"])
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
            check_type(argname="argument queue", value=queue, expected_type=type_hints["queue"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "threshold": threshold,
            "queue": queue,
        }
        if alarm_action is not None:
            self._values["alarm_action"] = alarm_action
        if insufficient_data_action is not None:
            self._values["insufficient_data_action"] = insufficient_data_action
        if ok_action is not None:
            self._values["ok_action"] = ok_action
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluation_periods is not None:
            self._values["evaluation_periods"] = evaluation_periods
        if period is not None:
            self._values["period"] = period
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if alarm_name is not None:
            self._values["alarm_name"] = alarm_name

    @builtins.property
    def alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of data points that must be breaching to trigger the alarm.

        :default: 15
        '''
        result = self._values.get("datapoints_to_alarm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''The number of periods over which data is compared to the specified threshold.

        :default: 15
        '''
        result = self._values.get("evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The period over which the specified statistic is applied.

        :default: Duration.minutes(1)
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def threshold(self) -> jsii.Number:
        '''The value against which the specified statistic is compared.

        The recommended threshold value for this alarm is highly dependent on the expected message
        processing time. You can use historical data to calculate the average message processing time,
        and then set the threshold to 50% higher than the maximum expected SQS message processing
        time by queue consumers.
        '''
        result = self._values.get("threshold")
        assert result is not None, "Required property 'threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        '''The description of the alarm.

        :default:

        - This alarm watches the age of the oldest message in the queue. You can use this alarm
        to monitor if your consumers are processing SQS messages at the desired speed. Consider increasing
        the consumer count or consumer throughput to reduce message age. This metric can be used in
        combination with ApproximateNumberOfMessagesVisible to determine how big the queue backlog is
        and how quickly messages are being processed. To prevent messages from being deleted before processed,
        consider configuring the dead-letter queue to sideline potential poison pill messages.
        '''
        result = self._values.get("alarm_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_name(self) -> typing.Optional[builtins.str]:
        '''The alarm name.

        :default: - queue.queueName + ' - ApproximateAgeOfOldestMessage'
        '''
        result = self._values.get("alarm_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def queue(self) -> _aws_cdk_aws_sqs_ceddda9d.IQueue:
        '''The SQS queue for which to create the alarm.'''
        result = self._values.get("queue")
        assert result is not None, "Required property 'queue' is missing"
        return typing.cast(_aws_cdk_aws_sqs_ceddda9d.IQueue, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqsApproximateAgeOfOldestMessageAlarmProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SqsApproximateNumberOfMessagesNotVisibleAlarm(
    _aws_cdk_aws_cloudwatch_ceddda9d.Alarm,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.SqsApproximateNumberOfMessagesNotVisibleAlarm",
):
    '''An alarm that watches the number of messages that are in flight.

    This alarm is used to detect a high number of in-flight messages
    in the queue. If consumers do not delete messages within the
    visibility timeout period, when the queue is polled, messages
    reappear in the queue. For FIFO queues, there can be a maximum
    of 20,000 in-flight messages. If you reach this quota, SQS returns
    no error messages. A FIFO queue looks through the first 20k
    messages to determine available message groups. This means that
    if you have a backlog of messages in a single message group,
    you cannot consume messages from other message groups that were
    sent to the queue at a later time until you successfully
    consume the messages from the backlog.

    This alarm is triggered when the number of messages that are in
    flight exceeds or is equal to the specified threshold.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        queue: _aws_cdk_aws_sqs_ceddda9d.IQueue,
        threshold: jsii.Number,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param queue: The SQS queue for which to create the alarm.
        :param threshold: The value against which the specified statistic is compared. The recommended threshold value for this alarm is highly dependent on the expected number of messages in flight. You can use historical data to calculate the maximum expected number of messages in flight and set the threshold to 50% over this value. If consumers of the queue are processing but not deleting messages from the queue, this number will suddenly increase.
        :param alarm_description: The description of the alarm. Default: - This alarm helps to detect a high number of in-flight messages with respect to QueueName. For troubleshooting, check message backlog decreasing (https://repost.aws/knowledge-center/sqs-message-backlog).
        :param alarm_name: The alarm name. Default: - queue.queueName + ' - ApproximateNumberOfMessagesNotVisible'
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 15
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 15
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8815dfd941d4ca8bcecc45ab9b5be4fc29cb8548dfe235cadc57ffe548606090)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SqsApproximateNumberOfMessagesNotVisibleAlarmProps(
            queue=queue,
            threshold=threshold,
            alarm_description=alarm_description,
            alarm_name=alarm_name,
            datapoints_to_alarm=datapoints_to_alarm,
            evaluation_periods=evaluation_periods,
            period=period,
            alarm_action=alarm_action,
            insufficient_data_action=insufficient_data_action,
            ok_action=ok_action,
            treat_missing_data=treat_missing_data,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.SqsApproximateNumberOfMessagesNotVisibleAlarmConfig",
    jsii_struct_bases=[SqsAlarmBaseConfig],
    name_mapping={
        "alarm_action": "alarmAction",
        "insufficient_data_action": "insufficientDataAction",
        "ok_action": "okAction",
        "treat_missing_data": "treatMissingData",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluation_periods": "evaluationPeriods",
        "period": "period",
        "threshold": "threshold",
        "alarm_description": "alarmDescription",
        "alarm_name": "alarmName",
    },
)
class SqsApproximateNumberOfMessagesNotVisibleAlarmConfig(SqsAlarmBaseConfig):
    def __init__(
        self,
        *,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        threshold: jsii.Number,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration for the ApproximateNumberOfMessagesNotVisible alarm.

        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 15
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 15
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param threshold: The value against which the specified statistic is compared. The recommended threshold value for this alarm is highly dependent on the expected number of messages in flight. You can use historical data to calculate the maximum expected number of messages in flight and set the threshold to 50% over this value. If consumers of the queue are processing but not deleting messages from the queue, this number will suddenly increase.
        :param alarm_description: The description of the alarm. Default: - This alarm helps to detect a high number of in-flight messages with respect to QueueName. For troubleshooting, check message backlog decreasing (https://repost.aws/knowledge-center/sqs-message-backlog).
        :param alarm_name: The alarm name. Default: - queue.queueName + ' - ApproximateNumberOfMessagesNotVisible'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c35ed35809a4360f095271f551791be67f6ca04c5462fdaec844342d7ed06514)
            check_type(argname="argument alarm_action", value=alarm_action, expected_type=type_hints["alarm_action"])
            check_type(argname="argument insufficient_data_action", value=insufficient_data_action, expected_type=type_hints["insufficient_data_action"])
            check_type(argname="argument ok_action", value=ok_action, expected_type=type_hints["ok_action"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument alarm_description", value=alarm_description, expected_type=type_hints["alarm_description"])
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "threshold": threshold,
        }
        if alarm_action is not None:
            self._values["alarm_action"] = alarm_action
        if insufficient_data_action is not None:
            self._values["insufficient_data_action"] = insufficient_data_action
        if ok_action is not None:
            self._values["ok_action"] = ok_action
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluation_periods is not None:
            self._values["evaluation_periods"] = evaluation_periods
        if period is not None:
            self._values["period"] = period
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if alarm_name is not None:
            self._values["alarm_name"] = alarm_name

    @builtins.property
    def alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of data points that must be breaching to trigger the alarm.

        :default: 15
        '''
        result = self._values.get("datapoints_to_alarm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''The number of periods over which data is compared to the specified threshold.

        :default: 15
        '''
        result = self._values.get("evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The period over which the specified statistic is applied.

        :default: Duration.minutes(1)
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def threshold(self) -> jsii.Number:
        '''The value against which the specified statistic is compared.

        The recommended threshold value for this alarm is highly dependent on the expected number
        of messages in flight. You can use historical data to calculate the maximum expected
        number of messages in flight and set the threshold to 50% over this value. If consumers
        of the queue are processing but not deleting messages from the queue, this number will
        suddenly increase.
        '''
        result = self._values.get("threshold")
        assert result is not None, "Required property 'threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        '''The description of the alarm.

        :default:

        - This alarm helps to detect a high number of in-flight messages with respect to QueueName.
        For troubleshooting, check message backlog decreasing (https://repost.aws/knowledge-center/sqs-message-backlog).
        '''
        result = self._values.get("alarm_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_name(self) -> typing.Optional[builtins.str]:
        '''The alarm name.

        :default: - queue.queueName + ' - ApproximateNumberOfMessagesNotVisible'
        '''
        result = self._values.get("alarm_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqsApproximateNumberOfMessagesNotVisibleAlarmConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.SqsApproximateNumberOfMessagesNotVisibleAlarmProps",
    jsii_struct_bases=[SqsApproximateNumberOfMessagesNotVisibleAlarmConfig],
    name_mapping={
        "alarm_action": "alarmAction",
        "insufficient_data_action": "insufficientDataAction",
        "ok_action": "okAction",
        "treat_missing_data": "treatMissingData",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluation_periods": "evaluationPeriods",
        "period": "period",
        "threshold": "threshold",
        "alarm_description": "alarmDescription",
        "alarm_name": "alarmName",
        "queue": "queue",
    },
)
class SqsApproximateNumberOfMessagesNotVisibleAlarmProps(
    SqsApproximateNumberOfMessagesNotVisibleAlarmConfig,
):
    def __init__(
        self,
        *,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        threshold: jsii.Number,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        queue: _aws_cdk_aws_sqs_ceddda9d.IQueue,
    ) -> None:
        '''Properties for the SqsApproximateNumberOfMessagesNotVisibleAlarm construct.

        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 15
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 15
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param threshold: The value against which the specified statistic is compared. The recommended threshold value for this alarm is highly dependent on the expected number of messages in flight. You can use historical data to calculate the maximum expected number of messages in flight and set the threshold to 50% over this value. If consumers of the queue are processing but not deleting messages from the queue, this number will suddenly increase.
        :param alarm_description: The description of the alarm. Default: - This alarm helps to detect a high number of in-flight messages with respect to QueueName. For troubleshooting, check message backlog decreasing (https://repost.aws/knowledge-center/sqs-message-backlog).
        :param alarm_name: The alarm name. Default: - queue.queueName + ' - ApproximateNumberOfMessagesNotVisible'
        :param queue: The SQS queue for which to create the alarm.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9376fa81f847d50cbcd5a89d6f568da884875f0f5dae5fa27c75a88325d354eb)
            check_type(argname="argument alarm_action", value=alarm_action, expected_type=type_hints["alarm_action"])
            check_type(argname="argument insufficient_data_action", value=insufficient_data_action, expected_type=type_hints["insufficient_data_action"])
            check_type(argname="argument ok_action", value=ok_action, expected_type=type_hints["ok_action"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument alarm_description", value=alarm_description, expected_type=type_hints["alarm_description"])
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
            check_type(argname="argument queue", value=queue, expected_type=type_hints["queue"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "threshold": threshold,
            "queue": queue,
        }
        if alarm_action is not None:
            self._values["alarm_action"] = alarm_action
        if insufficient_data_action is not None:
            self._values["insufficient_data_action"] = insufficient_data_action
        if ok_action is not None:
            self._values["ok_action"] = ok_action
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluation_periods is not None:
            self._values["evaluation_periods"] = evaluation_periods
        if period is not None:
            self._values["period"] = period
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if alarm_name is not None:
            self._values["alarm_name"] = alarm_name

    @builtins.property
    def alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of data points that must be breaching to trigger the alarm.

        :default: 15
        '''
        result = self._values.get("datapoints_to_alarm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''The number of periods over which data is compared to the specified threshold.

        :default: 15
        '''
        result = self._values.get("evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The period over which the specified statistic is applied.

        :default: Duration.minutes(1)
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def threshold(self) -> jsii.Number:
        '''The value against which the specified statistic is compared.

        The recommended threshold value for this alarm is highly dependent on the expected number
        of messages in flight. You can use historical data to calculate the maximum expected
        number of messages in flight and set the threshold to 50% over this value. If consumers
        of the queue are processing but not deleting messages from the queue, this number will
        suddenly increase.
        '''
        result = self._values.get("threshold")
        assert result is not None, "Required property 'threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        '''The description of the alarm.

        :default:

        - This alarm helps to detect a high number of in-flight messages with respect to QueueName.
        For troubleshooting, check message backlog decreasing (https://repost.aws/knowledge-center/sqs-message-backlog).
        '''
        result = self._values.get("alarm_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_name(self) -> typing.Optional[builtins.str]:
        '''The alarm name.

        :default: - queue.queueName + ' - ApproximateNumberOfMessagesNotVisible'
        '''
        result = self._values.get("alarm_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def queue(self) -> _aws_cdk_aws_sqs_ceddda9d.IQueue:
        '''The SQS queue for which to create the alarm.'''
        result = self._values.get("queue")
        assert result is not None, "Required property 'queue' is missing"
        return typing.cast(_aws_cdk_aws_sqs_ceddda9d.IQueue, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqsApproximateNumberOfMessagesNotVisibleAlarmProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SqsApproximateNumberOfMessagesVisibleAlarm(
    _aws_cdk_aws_cloudwatch_ceddda9d.Alarm,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.SqsApproximateNumberOfMessagesVisibleAlarm",
):
    '''An alarm that watches the number of messages that are visible in the queue.

    This alarm is used to detect whether the message
    count of the active queue is too high and consumers
    are slow to process the messages or there are not
    enough consumers to process them.

    This alarm is triggered when the number of messages
    that are visible in the queue exceeds or is equal to
    the specified threshold.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        queue: _aws_cdk_aws_sqs_ceddda9d.IQueue,
        threshold: jsii.Number,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param queue: The SQS queue for which to create the alarm.
        :param threshold: The value against which the specified statistic is compared. An unexpectedly high number of messages visible indicates that messages are not being processed by a consumer at the expected rate. You should consider historical data when you set this threshold.
        :param alarm_description: The description of the alarm. Default: - This alarm helps to detect a high number of in-flight messages with respect to QueueName. For troubleshooting, check message backlog decreasing (https://repost.aws/knowledge-center/sqs-message-backlog).
        :param alarm_name: The alarm name. Default: - queue.queueName + ' - ApproximateNumberOfMessagesVisible'
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 15
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 15
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a9188694cd82c03a9454a0975930ea6195f10816b6b12711ce2f5521c048ecc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SqsApproximateNumberOfMessagesVisibleAlarmProps(
            queue=queue,
            threshold=threshold,
            alarm_description=alarm_description,
            alarm_name=alarm_name,
            datapoints_to_alarm=datapoints_to_alarm,
            evaluation_periods=evaluation_periods,
            period=period,
            alarm_action=alarm_action,
            insufficient_data_action=insufficient_data_action,
            ok_action=ok_action,
            treat_missing_data=treat_missing_data,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.SqsApproximateNumberOfMessagesVisibleAlarmConfig",
    jsii_struct_bases=[SqsAlarmBaseConfig],
    name_mapping={
        "alarm_action": "alarmAction",
        "insufficient_data_action": "insufficientDataAction",
        "ok_action": "okAction",
        "treat_missing_data": "treatMissingData",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluation_periods": "evaluationPeriods",
        "period": "period",
        "threshold": "threshold",
        "alarm_description": "alarmDescription",
        "alarm_name": "alarmName",
    },
)
class SqsApproximateNumberOfMessagesVisibleAlarmConfig(SqsAlarmBaseConfig):
    def __init__(
        self,
        *,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        threshold: jsii.Number,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration for the ApproximateNumberOfMessagesVisible alarm.

        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 15
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 15
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param threshold: The value against which the specified statistic is compared. An unexpectedly high number of messages visible indicates that messages are not being processed by a consumer at the expected rate. You should consider historical data when you set this threshold.
        :param alarm_description: The description of the alarm. Default: - This alarm helps to detect a high number of in-flight messages with respect to QueueName. For troubleshooting, check message backlog decreasing (https://repost.aws/knowledge-center/sqs-message-backlog).
        :param alarm_name: The alarm name. Default: - queue.queueName + ' - ApproximateNumberOfMessagesVisible'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9416ae2be0a787ae40fb821ebed1c680e9e73112ef095bf0b4590229ef4ce402)
            check_type(argname="argument alarm_action", value=alarm_action, expected_type=type_hints["alarm_action"])
            check_type(argname="argument insufficient_data_action", value=insufficient_data_action, expected_type=type_hints["insufficient_data_action"])
            check_type(argname="argument ok_action", value=ok_action, expected_type=type_hints["ok_action"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument alarm_description", value=alarm_description, expected_type=type_hints["alarm_description"])
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "threshold": threshold,
        }
        if alarm_action is not None:
            self._values["alarm_action"] = alarm_action
        if insufficient_data_action is not None:
            self._values["insufficient_data_action"] = insufficient_data_action
        if ok_action is not None:
            self._values["ok_action"] = ok_action
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluation_periods is not None:
            self._values["evaluation_periods"] = evaluation_periods
        if period is not None:
            self._values["period"] = period
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if alarm_name is not None:
            self._values["alarm_name"] = alarm_name

    @builtins.property
    def alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of data points that must be breaching to trigger the alarm.

        :default: 15
        '''
        result = self._values.get("datapoints_to_alarm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''The number of periods over which data is compared to the specified threshold.

        :default: 15
        '''
        result = self._values.get("evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The period over which the specified statistic is applied.

        :default: Duration.minutes(1)
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def threshold(self) -> jsii.Number:
        '''The value against which the specified statistic is compared.

        An unexpectedly high number of messages visible indicates that messages are not being
        processed by a consumer at the expected rate. You should consider historical data when
        you set this threshold.
        '''
        result = self._values.get("threshold")
        assert result is not None, "Required property 'threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        '''The description of the alarm.

        :default:

        - This alarm helps to detect a high number of in-flight messages with respect to QueueName.
        For troubleshooting, check message backlog decreasing (https://repost.aws/knowledge-center/sqs-message-backlog).
        '''
        result = self._values.get("alarm_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_name(self) -> typing.Optional[builtins.str]:
        '''The alarm name.

        :default: - queue.queueName + ' - ApproximateNumberOfMessagesVisible'
        '''
        result = self._values.get("alarm_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqsApproximateNumberOfMessagesVisibleAlarmConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.SqsApproximateNumberOfMessagesVisibleAlarmProps",
    jsii_struct_bases=[SqsApproximateNumberOfMessagesVisibleAlarmConfig],
    name_mapping={
        "alarm_action": "alarmAction",
        "insufficient_data_action": "insufficientDataAction",
        "ok_action": "okAction",
        "treat_missing_data": "treatMissingData",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluation_periods": "evaluationPeriods",
        "period": "period",
        "threshold": "threshold",
        "alarm_description": "alarmDescription",
        "alarm_name": "alarmName",
        "queue": "queue",
    },
)
class SqsApproximateNumberOfMessagesVisibleAlarmProps(
    SqsApproximateNumberOfMessagesVisibleAlarmConfig,
):
    def __init__(
        self,
        *,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        threshold: jsii.Number,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        queue: _aws_cdk_aws_sqs_ceddda9d.IQueue,
    ) -> None:
        '''Properties for the SqsApproximateNumberOfMessagesVisibleAlarm construct.

        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 15
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 15
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param threshold: The value against which the specified statistic is compared. An unexpectedly high number of messages visible indicates that messages are not being processed by a consumer at the expected rate. You should consider historical data when you set this threshold.
        :param alarm_description: The description of the alarm. Default: - This alarm helps to detect a high number of in-flight messages with respect to QueueName. For troubleshooting, check message backlog decreasing (https://repost.aws/knowledge-center/sqs-message-backlog).
        :param alarm_name: The alarm name. Default: - queue.queueName + ' - ApproximateNumberOfMessagesVisible'
        :param queue: The SQS queue for which to create the alarm.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fb5bc4d73a65dccff1e81a21bd7c4c930f37e13143da72353844ec71b54e125)
            check_type(argname="argument alarm_action", value=alarm_action, expected_type=type_hints["alarm_action"])
            check_type(argname="argument insufficient_data_action", value=insufficient_data_action, expected_type=type_hints["insufficient_data_action"])
            check_type(argname="argument ok_action", value=ok_action, expected_type=type_hints["ok_action"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument alarm_description", value=alarm_description, expected_type=type_hints["alarm_description"])
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
            check_type(argname="argument queue", value=queue, expected_type=type_hints["queue"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "threshold": threshold,
            "queue": queue,
        }
        if alarm_action is not None:
            self._values["alarm_action"] = alarm_action
        if insufficient_data_action is not None:
            self._values["insufficient_data_action"] = insufficient_data_action
        if ok_action is not None:
            self._values["ok_action"] = ok_action
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluation_periods is not None:
            self._values["evaluation_periods"] = evaluation_periods
        if period is not None:
            self._values["period"] = period
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if alarm_name is not None:
            self._values["alarm_name"] = alarm_name

    @builtins.property
    def alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of data points that must be breaching to trigger the alarm.

        :default: 15
        '''
        result = self._values.get("datapoints_to_alarm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''The number of periods over which data is compared to the specified threshold.

        :default: 15
        '''
        result = self._values.get("evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The period over which the specified statistic is applied.

        :default: Duration.minutes(1)
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def threshold(self) -> jsii.Number:
        '''The value against which the specified statistic is compared.

        An unexpectedly high number of messages visible indicates that messages are not being
        processed by a consumer at the expected rate. You should consider historical data when
        you set this threshold.
        '''
        result = self._values.get("threshold")
        assert result is not None, "Required property 'threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        '''The description of the alarm.

        :default:

        - This alarm helps to detect a high number of in-flight messages with respect to QueueName.
        For troubleshooting, check message backlog decreasing (https://repost.aws/knowledge-center/sqs-message-backlog).
        '''
        result = self._values.get("alarm_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_name(self) -> typing.Optional[builtins.str]:
        '''The alarm name.

        :default: - queue.queueName + ' - ApproximateNumberOfMessagesVisible'
        '''
        result = self._values.get("alarm_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def queue(self) -> _aws_cdk_aws_sqs_ceddda9d.IQueue:
        '''The SQS queue for which to create the alarm.'''
        result = self._values.get("queue")
        assert result is not None, "Required property 'queue' is missing"
        return typing.cast(_aws_cdk_aws_sqs_ceddda9d.IQueue, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqsApproximateNumberOfMessagesVisibleAlarmProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SqsNumberOfMessagesSentAlarm(
    _aws_cdk_aws_cloudwatch_ceddda9d.Alarm,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.SqsNumberOfMessagesSentAlarm",
):
    '''An alarm that watches the number of messages that are sent.

    This alarm is used to detect when a producer stops sending messages.

    This alarm is triggered when the number of messages sent is less than
    or equal to the specified threshold. By default, 0.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        queue: _aws_cdk_aws_sqs_ceddda9d.IQueue,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        threshold: typing.Optional[jsii.Number] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param queue: The SQS queue for which to create the alarm.
        :param alarm_description: The description of the alarm. Default: - This alarm helps to detect a high number of in-flight messages with respect to QueueName. For troubleshooting, check message backlog decreasing (https://repost.aws/knowledge-center/sqs-message-backlog).
        :param alarm_name: The alarm name. Default: - queue.queueName + ' - NumberOfMessagesSent'
        :param threshold: The value against which the specified statistic is compared. If the number of messages sent is 0, the producer is not sending any messages. If this queue has a low TPS, increase the number of EvaluationPeriods accordingly. Default: 0
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 15
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 15
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c83cc6f93b61287db8574d8fe0172a074b7e233a8e19487d23a436aadfc46237)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SqsNumberOfMessagesSentAlarmProps(
            queue=queue,
            alarm_description=alarm_description,
            alarm_name=alarm_name,
            threshold=threshold,
            datapoints_to_alarm=datapoints_to_alarm,
            evaluation_periods=evaluation_periods,
            period=period,
            alarm_action=alarm_action,
            insufficient_data_action=insufficient_data_action,
            ok_action=ok_action,
            treat_missing_data=treat_missing_data,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.SqsNumberOfMessagesSentAlarmConfig",
    jsii_struct_bases=[SqsAlarmBaseConfig],
    name_mapping={
        "alarm_action": "alarmAction",
        "insufficient_data_action": "insufficientDataAction",
        "ok_action": "okAction",
        "treat_missing_data": "treatMissingData",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluation_periods": "evaluationPeriods",
        "period": "period",
        "alarm_description": "alarmDescription",
        "alarm_name": "alarmName",
        "threshold": "threshold",
    },
)
class SqsNumberOfMessagesSentAlarmConfig(SqsAlarmBaseConfig):
    def __init__(
        self,
        *,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Configuration for the NumberOfMessagesSent alarm.

        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 15
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 15
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param alarm_description: The description of the alarm. Default: - This alarm helps to detect a high number of in-flight messages with respect to QueueName. For troubleshooting, check message backlog decreasing (https://repost.aws/knowledge-center/sqs-message-backlog).
        :param alarm_name: The alarm name. Default: - queue.queueName + ' - NumberOfMessagesSent'
        :param threshold: The value against which the specified statistic is compared. If the number of messages sent is 0, the producer is not sending any messages. If this queue has a low TPS, increase the number of EvaluationPeriods accordingly. Default: 0
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5a27b809a4469882ad8e6a5ad6df46efd97d656d0a63ccc9ef71906dc194139)
            check_type(argname="argument alarm_action", value=alarm_action, expected_type=type_hints["alarm_action"])
            check_type(argname="argument insufficient_data_action", value=insufficient_data_action, expected_type=type_hints["insufficient_data_action"])
            check_type(argname="argument ok_action", value=ok_action, expected_type=type_hints["ok_action"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument alarm_description", value=alarm_description, expected_type=type_hints["alarm_description"])
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alarm_action is not None:
            self._values["alarm_action"] = alarm_action
        if insufficient_data_action is not None:
            self._values["insufficient_data_action"] = insufficient_data_action
        if ok_action is not None:
            self._values["ok_action"] = ok_action
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluation_periods is not None:
            self._values["evaluation_periods"] = evaluation_periods
        if period is not None:
            self._values["period"] = period
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if alarm_name is not None:
            self._values["alarm_name"] = alarm_name
        if threshold is not None:
            self._values["threshold"] = threshold

    @builtins.property
    def alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of data points that must be breaching to trigger the alarm.

        :default: 15
        '''
        result = self._values.get("datapoints_to_alarm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''The number of periods over which data is compared to the specified threshold.

        :default: 15
        '''
        result = self._values.get("evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The period over which the specified statistic is applied.

        :default: Duration.minutes(1)
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        '''The description of the alarm.

        :default:

        - This alarm helps to detect a high number of in-flight messages with respect
        to QueueName. For troubleshooting, check message backlog decreasing (https://repost.aws/knowledge-center/sqs-message-backlog).
        '''
        result = self._values.get("alarm_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_name(self) -> typing.Optional[builtins.str]:
        '''The alarm name.

        :default: - queue.queueName + ' - NumberOfMessagesSent'
        '''
        result = self._values.get("alarm_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def threshold(self) -> typing.Optional[jsii.Number]:
        '''The value against which the specified statistic is compared.

        If the number of messages sent is 0, the producer is not sending any messages.
        If this queue has a low TPS, increase the number of EvaluationPeriods accordingly.

        :default: 0
        '''
        result = self._values.get("threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqsNumberOfMessagesSentAlarmConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.SqsNumberOfMessagesSentAlarmProps",
    jsii_struct_bases=[SqsNumberOfMessagesSentAlarmConfig],
    name_mapping={
        "alarm_action": "alarmAction",
        "insufficient_data_action": "insufficientDataAction",
        "ok_action": "okAction",
        "treat_missing_data": "treatMissingData",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluation_periods": "evaluationPeriods",
        "period": "period",
        "alarm_description": "alarmDescription",
        "alarm_name": "alarmName",
        "threshold": "threshold",
        "queue": "queue",
    },
)
class SqsNumberOfMessagesSentAlarmProps(SqsNumberOfMessagesSentAlarmConfig):
    def __init__(
        self,
        *,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        threshold: typing.Optional[jsii.Number] = None,
        queue: _aws_cdk_aws_sqs_ceddda9d.IQueue,
    ) -> None:
        '''Properties for the SqsNumberOfMessagesSentAlarm construct.

        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 15
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 15
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param alarm_description: The description of the alarm. Default: - This alarm helps to detect a high number of in-flight messages with respect to QueueName. For troubleshooting, check message backlog decreasing (https://repost.aws/knowledge-center/sqs-message-backlog).
        :param alarm_name: The alarm name. Default: - queue.queueName + ' - NumberOfMessagesSent'
        :param threshold: The value against which the specified statistic is compared. If the number of messages sent is 0, the producer is not sending any messages. If this queue has a low TPS, increase the number of EvaluationPeriods accordingly. Default: 0
        :param queue: The SQS queue for which to create the alarm.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0793f6ef8158a82e9718505397a2f6f689150450cf683f7dc859408933d841e7)
            check_type(argname="argument alarm_action", value=alarm_action, expected_type=type_hints["alarm_action"])
            check_type(argname="argument insufficient_data_action", value=insufficient_data_action, expected_type=type_hints["insufficient_data_action"])
            check_type(argname="argument ok_action", value=ok_action, expected_type=type_hints["ok_action"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument alarm_description", value=alarm_description, expected_type=type_hints["alarm_description"])
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument queue", value=queue, expected_type=type_hints["queue"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "queue": queue,
        }
        if alarm_action is not None:
            self._values["alarm_action"] = alarm_action
        if insufficient_data_action is not None:
            self._values["insufficient_data_action"] = insufficient_data_action
        if ok_action is not None:
            self._values["ok_action"] = ok_action
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluation_periods is not None:
            self._values["evaluation_periods"] = evaluation_periods
        if period is not None:
            self._values["period"] = period
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if alarm_name is not None:
            self._values["alarm_name"] = alarm_name
        if threshold is not None:
            self._values["threshold"] = threshold

    @builtins.property
    def alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of data points that must be breaching to trigger the alarm.

        :default: 15
        '''
        result = self._values.get("datapoints_to_alarm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''The number of periods over which data is compared to the specified threshold.

        :default: 15
        '''
        result = self._values.get("evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The period over which the specified statistic is applied.

        :default: Duration.minutes(1)
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        '''The description of the alarm.

        :default:

        - This alarm helps to detect a high number of in-flight messages with respect
        to QueueName. For troubleshooting, check message backlog decreasing (https://repost.aws/knowledge-center/sqs-message-backlog).
        '''
        result = self._values.get("alarm_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_name(self) -> typing.Optional[builtins.str]:
        '''The alarm name.

        :default: - queue.queueName + ' - NumberOfMessagesSent'
        '''
        result = self._values.get("alarm_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def threshold(self) -> typing.Optional[jsii.Number]:
        '''The value against which the specified statistic is compared.

        If the number of messages sent is 0, the producer is not sending any messages.
        If this queue has a low TPS, increase the number of EvaluationPeriods accordingly.

        :default: 0
        '''
        result = self._values.get("threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def queue(self) -> _aws_cdk_aws_sqs_ceddda9d.IQueue:
        '''The SQS queue for which to create the alarm.'''
        result = self._values.get("queue")
        assert result is not None, "Required property 'queue' is missing"
        return typing.cast(_aws_cdk_aws_sqs_ceddda9d.IQueue, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqsNumberOfMessagesSentAlarmProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SqsRecommendedAlarms(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.SqsRecommendedAlarms",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        queue: _aws_cdk_aws_sqs_ceddda9d.IQueue,
        config_approximate_age_of_oldest_message_alarm: typing.Union[SqsApproximateAgeOfOldestMessageAlarmConfig, typing.Dict[builtins.str, typing.Any]],
        config_approximate_number_of_messages_not_visible_alarm: typing.Union[SqsApproximateNumberOfMessagesNotVisibleAlarmConfig, typing.Dict[builtins.str, typing.Any]],
        config_approximate_number_of_messages_visible_alarm: typing.Union[SqsApproximateNumberOfMessagesVisibleAlarmConfig, typing.Dict[builtins.str, typing.Any]],
        config_number_of_messages_sent_alarm: typing.Optional[typing.Union[SqsNumberOfMessagesSentAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        default_alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        default_insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        default_ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        exclude_alarms: typing.Optional[typing.Sequence["SqsRecommendedAlarmsMetrics"]] = None,
        exclude_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param queue: The SQS queue for which to create the alarms.
        :param config_approximate_age_of_oldest_message_alarm: The configuration for the approximate age of oldest message alarm.
        :param config_approximate_number_of_messages_not_visible_alarm: The configuration for the approximate number of messages not visible alarm.
        :param config_approximate_number_of_messages_visible_alarm: The configuration for the approximate number of messages visible alarm.
        :param config_number_of_messages_sent_alarm: The configuration for the number of messages sent alarm.
        :param default_alarm_action: The default action to take when an alarm is triggered. Default: - None
        :param default_insufficient_data_action: The default action to take when an alarm has insufficient data. Default: - None
        :param default_ok_action: The default action to take when an alarm enters the ok state. Default: - None
        :param exclude_alarms: Alarm metrics to exclude from the recommended alarms. Default: - None
        :param exclude_resources: The resources to exclude from the recommended alarms. Use a resources id to exclude a specific resource.
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a37434be382ee9bdf1fa47a726cbedf3dab305255578301f29d8d0427d0ed9d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SqsRecommendedAlarmsProps(
            queue=queue,
            config_approximate_age_of_oldest_message_alarm=config_approximate_age_of_oldest_message_alarm,
            config_approximate_number_of_messages_not_visible_alarm=config_approximate_number_of_messages_not_visible_alarm,
            config_approximate_number_of_messages_visible_alarm=config_approximate_number_of_messages_visible_alarm,
            config_number_of_messages_sent_alarm=config_number_of_messages_sent_alarm,
            default_alarm_action=default_alarm_action,
            default_insufficient_data_action=default_insufficient_data_action,
            default_ok_action=default_ok_action,
            exclude_alarms=exclude_alarms,
            exclude_resources=exclude_resources,
            treat_missing_data=treat_missing_data,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="alarmApproximateAgeOfOldestMessage")
    def alarm_approximate_age_of_oldest_message(
        self,
    ) -> typing.Optional[SqsApproximateAgeOfOldestMessageAlarm]:
        '''The approximate age of oldest message alarm.'''
        return typing.cast(typing.Optional[SqsApproximateAgeOfOldestMessageAlarm], jsii.get(self, "alarmApproximateAgeOfOldestMessage"))

    @builtins.property
    @jsii.member(jsii_name="alarmApproximateNumberOfMessagesNotVisible")
    def alarm_approximate_number_of_messages_not_visible(
        self,
    ) -> typing.Optional[SqsApproximateNumberOfMessagesNotVisibleAlarm]:
        '''The approximate number of messages not visible alarm.'''
        return typing.cast(typing.Optional[SqsApproximateNumberOfMessagesNotVisibleAlarm], jsii.get(self, "alarmApproximateNumberOfMessagesNotVisible"))

    @builtins.property
    @jsii.member(jsii_name="alarmApproximateNumberOfMessagesVisible")
    def alarm_approximate_number_of_messages_visible(
        self,
    ) -> typing.Optional[SqsApproximateNumberOfMessagesVisibleAlarm]:
        '''The approximate number of messages visible alarm.'''
        return typing.cast(typing.Optional[SqsApproximateNumberOfMessagesVisibleAlarm], jsii.get(self, "alarmApproximateNumberOfMessagesVisible"))

    @builtins.property
    @jsii.member(jsii_name="alarmNumberOfMessagesSent")
    def alarm_number_of_messages_sent(
        self,
    ) -> typing.Optional[SqsNumberOfMessagesSentAlarm]:
        '''The number of messages sent alarm.'''
        return typing.cast(typing.Optional[SqsNumberOfMessagesSentAlarm], jsii.get(self, "alarmNumberOfMessagesSent"))


@jsii.implements(_aws_cdk_ceddda9d.IAspect)
class SqsRecommendedAlarmsAspect(
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.SqsRecommendedAlarmsAspect",
):
    '''Configured the recommended alarms for an SQS queue.

    Requires defining thresholds for some alarms.

    :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Best_Practice_Recommended_Alarms_AWS_Services.html#SQS
    '''

    def __init__(
        self,
        *,
        config_approximate_age_of_oldest_message_alarm: typing.Union[SqsApproximateAgeOfOldestMessageAlarmConfig, typing.Dict[builtins.str, typing.Any]],
        config_approximate_number_of_messages_not_visible_alarm: typing.Union[SqsApproximateNumberOfMessagesNotVisibleAlarmConfig, typing.Dict[builtins.str, typing.Any]],
        config_approximate_number_of_messages_visible_alarm: typing.Union[SqsApproximateNumberOfMessagesVisibleAlarmConfig, typing.Dict[builtins.str, typing.Any]],
        config_number_of_messages_sent_alarm: typing.Optional[typing.Union[SqsNumberOfMessagesSentAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        default_alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        default_insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        default_ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        exclude_alarms: typing.Optional[typing.Sequence["SqsRecommendedAlarmsMetrics"]] = None,
        exclude_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> None:
        '''
        :param config_approximate_age_of_oldest_message_alarm: The configuration for the approximate age of oldest message alarm.
        :param config_approximate_number_of_messages_not_visible_alarm: The configuration for the approximate number of messages not visible alarm.
        :param config_approximate_number_of_messages_visible_alarm: The configuration for the approximate number of messages visible alarm.
        :param config_number_of_messages_sent_alarm: The configuration for the number of messages sent alarm.
        :param default_alarm_action: The default action to take when an alarm is triggered. Default: - None
        :param default_insufficient_data_action: The default action to take when an alarm has insufficient data. Default: - None
        :param default_ok_action: The default action to take when an alarm enters the ok state. Default: - None
        :param exclude_alarms: Alarm metrics to exclude from the recommended alarms. Default: - None
        :param exclude_resources: The resources to exclude from the recommended alarms. Use a resources id to exclude a specific resource.
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        props = SqsRecommendedAlarmsConfig(
            config_approximate_age_of_oldest_message_alarm=config_approximate_age_of_oldest_message_alarm,
            config_approximate_number_of_messages_not_visible_alarm=config_approximate_number_of_messages_not_visible_alarm,
            config_approximate_number_of_messages_visible_alarm=config_approximate_number_of_messages_visible_alarm,
            config_number_of_messages_sent_alarm=config_number_of_messages_sent_alarm,
            default_alarm_action=default_alarm_action,
            default_insufficient_data_action=default_insufficient_data_action,
            default_ok_action=default_ok_action,
            exclude_alarms=exclude_alarms,
            exclude_resources=exclude_resources,
            treat_missing_data=treat_missing_data,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="visit")
    def visit(self, node: _constructs_77d1e7e8.IConstruct) -> None:
        '''All aspects can visit an IConstruct.

        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f45c71a79fad93ee92684dc7ebe5ea477b90eedb43380589ebe7c41ecb444281)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "visit", [node]))


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.SqsRecommendedAlarmsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "config_approximate_age_of_oldest_message_alarm": "configApproximateAgeOfOldestMessageAlarm",
        "config_approximate_number_of_messages_not_visible_alarm": "configApproximateNumberOfMessagesNotVisibleAlarm",
        "config_approximate_number_of_messages_visible_alarm": "configApproximateNumberOfMessagesVisibleAlarm",
        "config_number_of_messages_sent_alarm": "configNumberOfMessagesSentAlarm",
        "default_alarm_action": "defaultAlarmAction",
        "default_insufficient_data_action": "defaultInsufficientDataAction",
        "default_ok_action": "defaultOkAction",
        "exclude_alarms": "excludeAlarms",
        "exclude_resources": "excludeResources",
        "treat_missing_data": "treatMissingData",
    },
)
class SqsRecommendedAlarmsConfig:
    def __init__(
        self,
        *,
        config_approximate_age_of_oldest_message_alarm: typing.Union[SqsApproximateAgeOfOldestMessageAlarmConfig, typing.Dict[builtins.str, typing.Any]],
        config_approximate_number_of_messages_not_visible_alarm: typing.Union[SqsApproximateNumberOfMessagesNotVisibleAlarmConfig, typing.Dict[builtins.str, typing.Any]],
        config_approximate_number_of_messages_visible_alarm: typing.Union[SqsApproximateNumberOfMessagesVisibleAlarmConfig, typing.Dict[builtins.str, typing.Any]],
        config_number_of_messages_sent_alarm: typing.Optional[typing.Union[SqsNumberOfMessagesSentAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        default_alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        default_insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        default_ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        exclude_alarms: typing.Optional[typing.Sequence["SqsRecommendedAlarmsMetrics"]] = None,
        exclude_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> None:
        '''Configuration for the recommended alarms for an SQS queue.

        :param config_approximate_age_of_oldest_message_alarm: The configuration for the approximate age of oldest message alarm.
        :param config_approximate_number_of_messages_not_visible_alarm: The configuration for the approximate number of messages not visible alarm.
        :param config_approximate_number_of_messages_visible_alarm: The configuration for the approximate number of messages visible alarm.
        :param config_number_of_messages_sent_alarm: The configuration for the number of messages sent alarm.
        :param default_alarm_action: The default action to take when an alarm is triggered. Default: - None
        :param default_insufficient_data_action: The default action to take when an alarm has insufficient data. Default: - None
        :param default_ok_action: The default action to take when an alarm enters the ok state. Default: - None
        :param exclude_alarms: Alarm metrics to exclude from the recommended alarms. Default: - None
        :param exclude_resources: The resources to exclude from the recommended alarms. Use a resources id to exclude a specific resource.
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        if isinstance(config_approximate_age_of_oldest_message_alarm, dict):
            config_approximate_age_of_oldest_message_alarm = SqsApproximateAgeOfOldestMessageAlarmConfig(**config_approximate_age_of_oldest_message_alarm)
        if isinstance(config_approximate_number_of_messages_not_visible_alarm, dict):
            config_approximate_number_of_messages_not_visible_alarm = SqsApproximateNumberOfMessagesNotVisibleAlarmConfig(**config_approximate_number_of_messages_not_visible_alarm)
        if isinstance(config_approximate_number_of_messages_visible_alarm, dict):
            config_approximate_number_of_messages_visible_alarm = SqsApproximateNumberOfMessagesVisibleAlarmConfig(**config_approximate_number_of_messages_visible_alarm)
        if isinstance(config_number_of_messages_sent_alarm, dict):
            config_number_of_messages_sent_alarm = SqsNumberOfMessagesSentAlarmConfig(**config_number_of_messages_sent_alarm)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__407cc33cddff7246efd0e7d0b66c4c79e9d85a4263615880ce742c9bc4fc1820)
            check_type(argname="argument config_approximate_age_of_oldest_message_alarm", value=config_approximate_age_of_oldest_message_alarm, expected_type=type_hints["config_approximate_age_of_oldest_message_alarm"])
            check_type(argname="argument config_approximate_number_of_messages_not_visible_alarm", value=config_approximate_number_of_messages_not_visible_alarm, expected_type=type_hints["config_approximate_number_of_messages_not_visible_alarm"])
            check_type(argname="argument config_approximate_number_of_messages_visible_alarm", value=config_approximate_number_of_messages_visible_alarm, expected_type=type_hints["config_approximate_number_of_messages_visible_alarm"])
            check_type(argname="argument config_number_of_messages_sent_alarm", value=config_number_of_messages_sent_alarm, expected_type=type_hints["config_number_of_messages_sent_alarm"])
            check_type(argname="argument default_alarm_action", value=default_alarm_action, expected_type=type_hints["default_alarm_action"])
            check_type(argname="argument default_insufficient_data_action", value=default_insufficient_data_action, expected_type=type_hints["default_insufficient_data_action"])
            check_type(argname="argument default_ok_action", value=default_ok_action, expected_type=type_hints["default_ok_action"])
            check_type(argname="argument exclude_alarms", value=exclude_alarms, expected_type=type_hints["exclude_alarms"])
            check_type(argname="argument exclude_resources", value=exclude_resources, expected_type=type_hints["exclude_resources"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "config_approximate_age_of_oldest_message_alarm": config_approximate_age_of_oldest_message_alarm,
            "config_approximate_number_of_messages_not_visible_alarm": config_approximate_number_of_messages_not_visible_alarm,
            "config_approximate_number_of_messages_visible_alarm": config_approximate_number_of_messages_visible_alarm,
        }
        if config_number_of_messages_sent_alarm is not None:
            self._values["config_number_of_messages_sent_alarm"] = config_number_of_messages_sent_alarm
        if default_alarm_action is not None:
            self._values["default_alarm_action"] = default_alarm_action
        if default_insufficient_data_action is not None:
            self._values["default_insufficient_data_action"] = default_insufficient_data_action
        if default_ok_action is not None:
            self._values["default_ok_action"] = default_ok_action
        if exclude_alarms is not None:
            self._values["exclude_alarms"] = exclude_alarms
        if exclude_resources is not None:
            self._values["exclude_resources"] = exclude_resources
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data

    @builtins.property
    def config_approximate_age_of_oldest_message_alarm(
        self,
    ) -> SqsApproximateAgeOfOldestMessageAlarmConfig:
        '''The configuration for the approximate age of oldest message alarm.'''
        result = self._values.get("config_approximate_age_of_oldest_message_alarm")
        assert result is not None, "Required property 'config_approximate_age_of_oldest_message_alarm' is missing"
        return typing.cast(SqsApproximateAgeOfOldestMessageAlarmConfig, result)

    @builtins.property
    def config_approximate_number_of_messages_not_visible_alarm(
        self,
    ) -> SqsApproximateNumberOfMessagesNotVisibleAlarmConfig:
        '''The configuration for the approximate number of messages not visible alarm.'''
        result = self._values.get("config_approximate_number_of_messages_not_visible_alarm")
        assert result is not None, "Required property 'config_approximate_number_of_messages_not_visible_alarm' is missing"
        return typing.cast(SqsApproximateNumberOfMessagesNotVisibleAlarmConfig, result)

    @builtins.property
    def config_approximate_number_of_messages_visible_alarm(
        self,
    ) -> SqsApproximateNumberOfMessagesVisibleAlarmConfig:
        '''The configuration for the approximate number of messages visible alarm.'''
        result = self._values.get("config_approximate_number_of_messages_visible_alarm")
        assert result is not None, "Required property 'config_approximate_number_of_messages_visible_alarm' is missing"
        return typing.cast(SqsApproximateNumberOfMessagesVisibleAlarmConfig, result)

    @builtins.property
    def config_number_of_messages_sent_alarm(
        self,
    ) -> typing.Optional[SqsNumberOfMessagesSentAlarmConfig]:
        '''The configuration for the number of messages sent alarm.'''
        result = self._values.get("config_number_of_messages_sent_alarm")
        return typing.cast(typing.Optional[SqsNumberOfMessagesSentAlarmConfig], result)

    @builtins.property
    def default_alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The default action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("default_alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def default_insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The default action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("default_insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def default_ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The default action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("default_ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def exclude_alarms(
        self,
    ) -> typing.Optional[typing.List["SqsRecommendedAlarmsMetrics"]]:
        '''Alarm metrics to exclude from the recommended alarms.

        :default: - None
        '''
        result = self._values.get("exclude_alarms")
        return typing.cast(typing.Optional[typing.List["SqsRecommendedAlarmsMetrics"]], result)

    @builtins.property
    def exclude_resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The resources to exclude from the recommended alarms.

        Use a resources id to exclude a specific resource.
        '''
        result = self._values.get("exclude_resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqsRecommendedAlarmsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.SqsRecommendedAlarmsMetrics"
)
class SqsRecommendedAlarmsMetrics(enum.Enum):
    '''The recommended metrics for SQS queue alarms.'''

    APPROXIMATE_AGE_OF_OLDEST_MESSAGE = "APPROXIMATE_AGE_OF_OLDEST_MESSAGE"
    APPROXIMATE_NUMBER_OF_MESSAGES_NOT_VISIBLE = "APPROXIMATE_NUMBER_OF_MESSAGES_NOT_VISIBLE"
    APPROXIMATE_NUMBER_OF_MESSAGES_VISIBLE = "APPROXIMATE_NUMBER_OF_MESSAGES_VISIBLE"
    NUMBER_OF_MESSAGES_SENT = "NUMBER_OF_MESSAGES_SENT"


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.SqsRecommendedAlarmsProps",
    jsii_struct_bases=[SqsRecommendedAlarmsConfig],
    name_mapping={
        "config_approximate_age_of_oldest_message_alarm": "configApproximateAgeOfOldestMessageAlarm",
        "config_approximate_number_of_messages_not_visible_alarm": "configApproximateNumberOfMessagesNotVisibleAlarm",
        "config_approximate_number_of_messages_visible_alarm": "configApproximateNumberOfMessagesVisibleAlarm",
        "config_number_of_messages_sent_alarm": "configNumberOfMessagesSentAlarm",
        "default_alarm_action": "defaultAlarmAction",
        "default_insufficient_data_action": "defaultInsufficientDataAction",
        "default_ok_action": "defaultOkAction",
        "exclude_alarms": "excludeAlarms",
        "exclude_resources": "excludeResources",
        "treat_missing_data": "treatMissingData",
        "queue": "queue",
    },
)
class SqsRecommendedAlarmsProps(SqsRecommendedAlarmsConfig):
    def __init__(
        self,
        *,
        config_approximate_age_of_oldest_message_alarm: typing.Union[SqsApproximateAgeOfOldestMessageAlarmConfig, typing.Dict[builtins.str, typing.Any]],
        config_approximate_number_of_messages_not_visible_alarm: typing.Union[SqsApproximateNumberOfMessagesNotVisibleAlarmConfig, typing.Dict[builtins.str, typing.Any]],
        config_approximate_number_of_messages_visible_alarm: typing.Union[SqsApproximateNumberOfMessagesVisibleAlarmConfig, typing.Dict[builtins.str, typing.Any]],
        config_number_of_messages_sent_alarm: typing.Optional[typing.Union[SqsNumberOfMessagesSentAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        default_alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        default_insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        default_ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        exclude_alarms: typing.Optional[typing.Sequence[SqsRecommendedAlarmsMetrics]] = None,
        exclude_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
        queue: _aws_cdk_aws_sqs_ceddda9d.IQueue,
    ) -> None:
        '''Properties for the SqsRecommendedAlarms construct.

        :param config_approximate_age_of_oldest_message_alarm: The configuration for the approximate age of oldest message alarm.
        :param config_approximate_number_of_messages_not_visible_alarm: The configuration for the approximate number of messages not visible alarm.
        :param config_approximate_number_of_messages_visible_alarm: The configuration for the approximate number of messages visible alarm.
        :param config_number_of_messages_sent_alarm: The configuration for the number of messages sent alarm.
        :param default_alarm_action: The default action to take when an alarm is triggered. Default: - None
        :param default_insufficient_data_action: The default action to take when an alarm has insufficient data. Default: - None
        :param default_ok_action: The default action to take when an alarm enters the ok state. Default: - None
        :param exclude_alarms: Alarm metrics to exclude from the recommended alarms. Default: - None
        :param exclude_resources: The resources to exclude from the recommended alarms. Use a resources id to exclude a specific resource.
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        :param queue: The SQS queue for which to create the alarms.
        '''
        if isinstance(config_approximate_age_of_oldest_message_alarm, dict):
            config_approximate_age_of_oldest_message_alarm = SqsApproximateAgeOfOldestMessageAlarmConfig(**config_approximate_age_of_oldest_message_alarm)
        if isinstance(config_approximate_number_of_messages_not_visible_alarm, dict):
            config_approximate_number_of_messages_not_visible_alarm = SqsApproximateNumberOfMessagesNotVisibleAlarmConfig(**config_approximate_number_of_messages_not_visible_alarm)
        if isinstance(config_approximate_number_of_messages_visible_alarm, dict):
            config_approximate_number_of_messages_visible_alarm = SqsApproximateNumberOfMessagesVisibleAlarmConfig(**config_approximate_number_of_messages_visible_alarm)
        if isinstance(config_number_of_messages_sent_alarm, dict):
            config_number_of_messages_sent_alarm = SqsNumberOfMessagesSentAlarmConfig(**config_number_of_messages_sent_alarm)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32e30f379dd47a0ddb371ae48cd5f2d74faa779b4377f94f691abc36732d99fc)
            check_type(argname="argument config_approximate_age_of_oldest_message_alarm", value=config_approximate_age_of_oldest_message_alarm, expected_type=type_hints["config_approximate_age_of_oldest_message_alarm"])
            check_type(argname="argument config_approximate_number_of_messages_not_visible_alarm", value=config_approximate_number_of_messages_not_visible_alarm, expected_type=type_hints["config_approximate_number_of_messages_not_visible_alarm"])
            check_type(argname="argument config_approximate_number_of_messages_visible_alarm", value=config_approximate_number_of_messages_visible_alarm, expected_type=type_hints["config_approximate_number_of_messages_visible_alarm"])
            check_type(argname="argument config_number_of_messages_sent_alarm", value=config_number_of_messages_sent_alarm, expected_type=type_hints["config_number_of_messages_sent_alarm"])
            check_type(argname="argument default_alarm_action", value=default_alarm_action, expected_type=type_hints["default_alarm_action"])
            check_type(argname="argument default_insufficient_data_action", value=default_insufficient_data_action, expected_type=type_hints["default_insufficient_data_action"])
            check_type(argname="argument default_ok_action", value=default_ok_action, expected_type=type_hints["default_ok_action"])
            check_type(argname="argument exclude_alarms", value=exclude_alarms, expected_type=type_hints["exclude_alarms"])
            check_type(argname="argument exclude_resources", value=exclude_resources, expected_type=type_hints["exclude_resources"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
            check_type(argname="argument queue", value=queue, expected_type=type_hints["queue"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "config_approximate_age_of_oldest_message_alarm": config_approximate_age_of_oldest_message_alarm,
            "config_approximate_number_of_messages_not_visible_alarm": config_approximate_number_of_messages_not_visible_alarm,
            "config_approximate_number_of_messages_visible_alarm": config_approximate_number_of_messages_visible_alarm,
            "queue": queue,
        }
        if config_number_of_messages_sent_alarm is not None:
            self._values["config_number_of_messages_sent_alarm"] = config_number_of_messages_sent_alarm
        if default_alarm_action is not None:
            self._values["default_alarm_action"] = default_alarm_action
        if default_insufficient_data_action is not None:
            self._values["default_insufficient_data_action"] = default_insufficient_data_action
        if default_ok_action is not None:
            self._values["default_ok_action"] = default_ok_action
        if exclude_alarms is not None:
            self._values["exclude_alarms"] = exclude_alarms
        if exclude_resources is not None:
            self._values["exclude_resources"] = exclude_resources
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data

    @builtins.property
    def config_approximate_age_of_oldest_message_alarm(
        self,
    ) -> SqsApproximateAgeOfOldestMessageAlarmConfig:
        '''The configuration for the approximate age of oldest message alarm.'''
        result = self._values.get("config_approximate_age_of_oldest_message_alarm")
        assert result is not None, "Required property 'config_approximate_age_of_oldest_message_alarm' is missing"
        return typing.cast(SqsApproximateAgeOfOldestMessageAlarmConfig, result)

    @builtins.property
    def config_approximate_number_of_messages_not_visible_alarm(
        self,
    ) -> SqsApproximateNumberOfMessagesNotVisibleAlarmConfig:
        '''The configuration for the approximate number of messages not visible alarm.'''
        result = self._values.get("config_approximate_number_of_messages_not_visible_alarm")
        assert result is not None, "Required property 'config_approximate_number_of_messages_not_visible_alarm' is missing"
        return typing.cast(SqsApproximateNumberOfMessagesNotVisibleAlarmConfig, result)

    @builtins.property
    def config_approximate_number_of_messages_visible_alarm(
        self,
    ) -> SqsApproximateNumberOfMessagesVisibleAlarmConfig:
        '''The configuration for the approximate number of messages visible alarm.'''
        result = self._values.get("config_approximate_number_of_messages_visible_alarm")
        assert result is not None, "Required property 'config_approximate_number_of_messages_visible_alarm' is missing"
        return typing.cast(SqsApproximateNumberOfMessagesVisibleAlarmConfig, result)

    @builtins.property
    def config_number_of_messages_sent_alarm(
        self,
    ) -> typing.Optional[SqsNumberOfMessagesSentAlarmConfig]:
        '''The configuration for the number of messages sent alarm.'''
        result = self._values.get("config_number_of_messages_sent_alarm")
        return typing.cast(typing.Optional[SqsNumberOfMessagesSentAlarmConfig], result)

    @builtins.property
    def default_alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The default action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("default_alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def default_insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The default action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("default_insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def default_ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The default action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("default_ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def exclude_alarms(
        self,
    ) -> typing.Optional[typing.List[SqsRecommendedAlarmsMetrics]]:
        '''Alarm metrics to exclude from the recommended alarms.

        :default: - None
        '''
        result = self._values.get("exclude_alarms")
        return typing.cast(typing.Optional[typing.List[SqsRecommendedAlarmsMetrics]], result)

    @builtins.property
    def exclude_resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The resources to exclude from the recommended alarms.

        Use a resources id to exclude a specific resource.
        '''
        result = self._values.get("exclude_resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    @builtins.property
    def queue(self) -> _aws_cdk_aws_sqs_ceddda9d.IQueue:
        '''The SQS queue for which to create the alarms.'''
        result = self._values.get("queue")
        assert result is not None, "Required property 'queue' is missing"
        return typing.cast(_aws_cdk_aws_sqs_ceddda9d.IQueue, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqsRecommendedAlarmsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Topic(
    _aws_cdk_aws_sns_ceddda9d.Topic,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.Topic",
):
    '''An extension of the SNS topic construct that provides helper methods to create recommended alarms.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        content_based_deduplication: typing.Optional[builtins.bool] = None,
        display_name: typing.Optional[builtins.str] = None,
        enforce_ssl: typing.Optional[builtins.bool] = None,
        fifo: typing.Optional[builtins.bool] = None,
        logging_configs: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_sns_ceddda9d.LoggingConfig, typing.Dict[builtins.str, typing.Any]]]] = None,
        master_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        message_retention_period_in_days: typing.Optional[jsii.Number] = None,
        signature_version: typing.Optional[builtins.str] = None,
        topic_name: typing.Optional[builtins.str] = None,
        tracing_config: typing.Optional[_aws_cdk_aws_sns_ceddda9d.TracingConfig] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param content_based_deduplication: Enables content-based deduplication for FIFO topics. Default: None
        :param display_name: A developer-defined string that can be used to identify this SNS topic. The display name must be maximum 100 characters long, including hyphens (-), underscores (_), spaces, and tabs. Default: None
        :param enforce_ssl: Adds a statement to enforce encryption of data in transit when publishing to the topic. Default: false
        :param fifo: Set to true to create a FIFO topic. Default: None
        :param logging_configs: The list of delivery status logging configurations for the topic. Default: None
        :param master_key: A KMS Key, either managed by this CDK app, or imported. Default: None
        :param message_retention_period_in_days: The number of days Amazon SNS retains messages. It can only be set for FIFO topics. Default: - do not archive messages
        :param signature_version: The signature version corresponds to the hashing algorithm used while creating the signature of the notifications, subscription confirmations, or unsubscribe confirmation messages sent by Amazon SNS. Default: 1
        :param topic_name: A name for the topic. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the topic name. For more information, see Name Type. Default: Generated name
        :param tracing_config: Tracing mode of an Amazon SNS topic. Default: TracingConfig.PASS_THROUGH
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70e505f14a1afa0f6a7236955dba568672dc67b4c2ceacb436fde882a2d66c49)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = _aws_cdk_aws_sns_ceddda9d.TopicProps(
            content_based_deduplication=content_based_deduplication,
            display_name=display_name,
            enforce_ssl=enforce_ssl,
            fifo=fifo,
            logging_configs=logging_configs,
            master_key=master_key,
            message_retention_period_in_days=message_retention_period_in_days,
            signature_version=signature_version,
            topic_name=topic_name,
            tracing_config=tracing_config,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="alarmNumberOfMessagesPublished")
    def alarm_number_of_messages_published(
        self,
        *,
        threshold: jsii.Number,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> SnsNumberOfMessagesPublishedAlarm:
        '''Creates an alarm for the NumberOfMessagesPublished metric.

        :param threshold: The value against which the specified statistic is compared. The number of messages published should be in line with the expected number of published messages for your application. You can also analyze the historical data, trends and traffic to find the right threshold.
        :param alarm_description: The description of the alarm. Default: - This alarm can detect when the number of SNS messages published is too low. For troubleshooting, check why the publishers are sending less traffic.
        :param alarm_name: The alarm name. Default: - topic.topicName + ' - NumberOfMessagesPublished'
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 5
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 5
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        props = SnsNumberOfMessagesPublishedAlarmConfig(
            threshold=threshold,
            alarm_description=alarm_description,
            alarm_name=alarm_name,
            datapoints_to_alarm=datapoints_to_alarm,
            evaluation_periods=evaluation_periods,
            period=period,
            alarm_action=alarm_action,
            insufficient_data_action=insufficient_data_action,
            ok_action=ok_action,
            treat_missing_data=treat_missing_data,
        )

        return typing.cast(SnsNumberOfMessagesPublishedAlarm, jsii.invoke(self, "alarmNumberOfMessagesPublished", [props]))

    @jsii.member(jsii_name="alarmNumberOfNotificationsDelivered")
    def alarm_number_of_notifications_delivered(
        self,
        *,
        threshold: jsii.Number,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> SnsNumberOfNotificationsDeliveredAlarm:
        '''Creates an alarm for the NumberOfNotificationsDelivered metric.

        :param threshold: The value against which the specified statistic is compared. The number of messages delivered should be in line with the expected number of messages produced and the number of consumers. You can also analyze the historical data, trends and traffic to find the right threshold.
        :param alarm_description: The description of the alarm. Default: - This alarm can detect when the number of SNS messages delivered is too low. This could be because of unintentional unsubscribing of an endpoint, or because of an SNS event that causes messages to experience delay.
        :param alarm_name: The alarm name. Default: - topic.topicName + ' - NumberOfNotificationsDelivered'
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 5
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 5
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        props = SnsNumberOfNotificationsDeliveredAlarmConfig(
            threshold=threshold,
            alarm_description=alarm_description,
            alarm_name=alarm_name,
            datapoints_to_alarm=datapoints_to_alarm,
            evaluation_periods=evaluation_periods,
            period=period,
            alarm_action=alarm_action,
            insufficient_data_action=insufficient_data_action,
            ok_action=ok_action,
            treat_missing_data=treat_missing_data,
        )

        return typing.cast(SnsNumberOfNotificationsDeliveredAlarm, jsii.invoke(self, "alarmNumberOfNotificationsDelivered", [props]))

    @jsii.member(jsii_name="alarmNumberOfNotificationsFailed")
    def alarm_number_of_notifications_failed(
        self,
        *,
        threshold: jsii.Number,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> SnsNumberOfNotificationsFailedAlarm:
        '''Creates an alarm for the NumberOfNotificationsFailed metric.

        :param threshold: The value against which the specified statistic is compared. The recommended threshold value for this alarm is highly dependent on the impact of failed notifications. Review the SLAs provided to your end users, fault tolerance and criticality of notifications and analyze historical data, and then select a threshold accordingly. The number of notifications failed should be 0 for topics that have only SQS, Lambda or Firehose subscriptions.
        :param alarm_description: The description of the alarm. Default: - This alarm can detect when the number of failed SNS messages is too high. To troubleshoot failed notifications, enable logging to CloudWatch Logs. Checking the logs can help you find which subscribers are failing, as well as the status codes they are returning.
        :param alarm_name: The alarm name. Default: - topic.topicName + ' - NumberOfNotificationsFailed'
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 5
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 5
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        props = SnsNumberOfNotificationsFailedAlarmConfig(
            threshold=threshold,
            alarm_description=alarm_description,
            alarm_name=alarm_name,
            datapoints_to_alarm=datapoints_to_alarm,
            evaluation_periods=evaluation_periods,
            period=period,
            alarm_action=alarm_action,
            insufficient_data_action=insufficient_data_action,
            ok_action=ok_action,
            treat_missing_data=treat_missing_data,
        )

        return typing.cast(SnsNumberOfNotificationsFailedAlarm, jsii.invoke(self, "alarmNumberOfNotificationsFailed", [props]))

    @jsii.member(jsii_name="alarmNumberOfNotificationsFailedToRedriveToDlq")
    def alarm_number_of_notifications_failed_to_redrive_to_dlq(
        self,
        *,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        threshold: typing.Optional[jsii.Number] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> SnsNumberOfNotificationsFailedToRedriveToDlqAlarm:
        '''Creates an alarm for the NumberOfNotificationsFailedToRedriveToDlq metric.

        :param alarm_description: The description of the alarm. Default: - This alarm helps to monitor messages that couldn't be moved to a dead-letter queue. Check whether your dead-letter queue exists and that it's configured correctly. Also, verify that SNS has permissions to access the dead-letter queue. Refer to the dead-letter queue documentation (https://docs.aws.amazon.com/sns/latest/dg/sns-dead-letter-queues.html) to learn more.
        :param alarm_name: The alarm name. Default: - topic.topicName + ' - NumberOfNotificationsFailedToRedriveToDlq'
        :param threshold: The value against which the specified statistic is compared. It's almost always a mistake if messages can't be moved to the dead-letter queue. The recommendation for the threshold is 0, meaning all messages that fail processing must be able to reach the dead-letter queue when the queue has been configured. Default: 0
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 5
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 5
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        props = SnsNumberOfNotificationsFailedToRedriveToDlqAlarmConfig(
            alarm_description=alarm_description,
            alarm_name=alarm_name,
            threshold=threshold,
            datapoints_to_alarm=datapoints_to_alarm,
            evaluation_periods=evaluation_periods,
            period=period,
            alarm_action=alarm_action,
            insufficient_data_action=insufficient_data_action,
            ok_action=ok_action,
            treat_missing_data=treat_missing_data,
        )

        return typing.cast(SnsNumberOfNotificationsFailedToRedriveToDlqAlarm, jsii.invoke(self, "alarmNumberOfNotificationsFailedToRedriveToDlq", [props]))

    @jsii.member(jsii_name="alarmNumberOfNotificationsFilteredOutInvalidAttributes")
    def alarm_number_of_notifications_filtered_out_invalid_attributes(
        self,
        *,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        threshold: typing.Optional[jsii.Number] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> SnsNumberOfNotificationsFilteredOutInvalidAttributesAlarm:
        '''Creates an alarm for the NumberOfNotificationsFilteredOutInvalidAttributes metric.

        :param alarm_description: The description of the alarm. Default: - This alarm helps to monitor and resolve potential problems with the publisher or subscribers. Check if a publisher is publishing messages with invalid attributes or if an inappropriate filter is applied to a subscriber. You can also analyze CloudWatch Logs to help find the root cause of the issue.
        :param alarm_name: The alarm name. Default: - topic.topicName + ' - NumberOfNotificationsFilteredOut-InvalidAttributes'
        :param threshold: The value against which the specified statistic is compared. Invalid attributes are almost always a mistake by the publisher. We recommend to set the threshold to 0 because invalid attributes are not expected in a healthy system. Default: 0
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 5
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 5
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        props = SnsNumberOfNotificationsFilteredOutInvalidAttributesAlarmConfig(
            alarm_description=alarm_description,
            alarm_name=alarm_name,
            threshold=threshold,
            datapoints_to_alarm=datapoints_to_alarm,
            evaluation_periods=evaluation_periods,
            period=period,
            alarm_action=alarm_action,
            insufficient_data_action=insufficient_data_action,
            ok_action=ok_action,
            treat_missing_data=treat_missing_data,
        )

        return typing.cast(SnsNumberOfNotificationsFilteredOutInvalidAttributesAlarm, jsii.invoke(self, "alarmNumberOfNotificationsFilteredOutInvalidAttributes", [props]))

    @jsii.member(jsii_name="alarmNumberOfNotificationsFilteredOutInvalidMessageBody")
    def alarm_number_of_notifications_filtered_out_invalid_message_body(
        self,
        *,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        threshold: typing.Optional[jsii.Number] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> SnsNumberOfNotificationsFilteredOutInvalidMessageBodyAlarm:
        '''Creates an alarm for the NumberOfNotificationsFilteredOutInvalidMessageBody metric.

        :param alarm_description: The description of the alarm. Default: - This alarm helps to monitor and resolve potential problems with the publisher or subscribers. Check if a publisher is publishing messages with invalid message bodies, or if an inappropriate filter is applied to a subscriber. You can also analyze CloudWatch Logs to help find the root cause of the issue.
        :param alarm_name: The alarm name. Default: - topic.topicName + ' - NumberOfNotificationsFilteredOut-InvalidMessageBody'
        :param threshold: The value against which the specified statistic is compared. Invalid message bodies are almost always a mistake by the publisher. We recommend to set the threshold to 0 because invalid message bodies are not expected in a healthy system. Default: 0
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 5
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 5
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        props = SnsNumberOfNotificationsFilteredOutInvalidMessageBodyAlarmConfig(
            alarm_description=alarm_description,
            alarm_name=alarm_name,
            threshold=threshold,
            datapoints_to_alarm=datapoints_to_alarm,
            evaluation_periods=evaluation_periods,
            period=period,
            alarm_action=alarm_action,
            insufficient_data_action=insufficient_data_action,
            ok_action=ok_action,
            treat_missing_data=treat_missing_data,
        )

        return typing.cast(SnsNumberOfNotificationsFilteredOutInvalidMessageBodyAlarm, jsii.invoke(self, "alarmNumberOfNotificationsFilteredOutInvalidMessageBody", [props]))

    @jsii.member(jsii_name="alarmNumberOfNotificationsRedrivenToDlq")
    def alarm_number_of_notifications_redriven_to_dlq(
        self,
        *,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        threshold: typing.Optional[jsii.Number] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> SnsNumberOfNotificationsRedrivenToDlqAlarm:
        '''Creates an alarm for the NumberOfNotificationsRedrivenToDlq metric.

        :param alarm_description: The description of the alarm. Default: - This alarm helps to monitor the number of messages that are moved to a dead-letter queue.
        :param alarm_name: The alarm name. Default: - topic.topicName + ' - NumberOfNotificationsRedrivenToDlq'
        :param threshold: The value against which the specified statistic is compared. In a healthy system of any subscriber type, messages should not be moved to the dead-letter queue. We recommend that you be notified if any messages land in the queue, so that you can identify and address the root cause, and potentially redrive the messages in the dead-letter queue to prevent data loss. Default: 0
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 5
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 5
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        '''
        props = SnsNumberOfNotificationsRedrivenToDlqAlarmConfig(
            alarm_description=alarm_description,
            alarm_name=alarm_name,
            threshold=threshold,
            datapoints_to_alarm=datapoints_to_alarm,
            evaluation_periods=evaluation_periods,
            period=period,
            alarm_action=alarm_action,
            insufficient_data_action=insufficient_data_action,
            ok_action=ok_action,
            treat_missing_data=treat_missing_data,
        )

        return typing.cast(SnsNumberOfNotificationsRedrivenToDlqAlarm, jsii.invoke(self, "alarmNumberOfNotificationsRedrivenToDlq", [props]))

    @jsii.member(jsii_name="applyRecommendedAlarms")
    def apply_recommended_alarms(
        self,
        *,
        config_number_of_messages_published_alarm: typing.Union[SnsNumberOfMessagesPublishedAlarmConfig, typing.Dict[builtins.str, typing.Any]],
        config_number_of_notifications_delivered_alarm: typing.Union[SnsNumberOfNotificationsDeliveredAlarmConfig, typing.Dict[builtins.str, typing.Any]],
        config_number_of_notifications_failed_alarm: typing.Union[SnsNumberOfNotificationsFailedAlarmConfig, typing.Dict[builtins.str, typing.Any]],
        config_number_of_notifications_failed_to_redrive_to_dlq_alarm: typing.Optional[typing.Union[SnsNumberOfNotificationsFailedToRedriveToDlqAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        config_number_of_notifications_filtered_out_invalid_attributes_alarm: typing.Optional[typing.Union[SnsNumberOfNotificationsFilteredOutInvalidAttributesAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        config_number_of_notifications_filtered_out_invalid_message_body_alarm: typing.Optional[typing.Union[SnsNumberOfNotificationsFilteredOutInvalidMessageBodyAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        config_number_of_notifications_redriven_to_dlq_alarm: typing.Optional[typing.Union[SnsNumberOfNotificationsRedrivenToDlqAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        default_alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        default_insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        default_ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        exclude_alarms: typing.Optional[typing.Sequence[SnsRecommendedAlarmsMetrics]] = None,
        exclude_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    ) -> SnsRecommendedAlarms:
        '''Creates recommended alarms for the SNS topic.

        :param config_number_of_messages_published_alarm: The configuration for the NumberOfMessagesPublished alarm.
        :param config_number_of_notifications_delivered_alarm: The configuration for the NumberOfNotificationsDelivered alarm.
        :param config_number_of_notifications_failed_alarm: The configuration for the NumberOfNotificationsFailed alarm.
        :param config_number_of_notifications_failed_to_redrive_to_dlq_alarm: The configuration for the NumberOfNotificationsFailedToRedriveToDlq alarm.
        :param config_number_of_notifications_filtered_out_invalid_attributes_alarm: The configuration for the NumberOfNotificationsFilteredOutInvalidAttributes alarm.
        :param config_number_of_notifications_filtered_out_invalid_message_body_alarm: The configuration for the NumberOfNotificationsFilteredOutInvalidMessageBody alarm.
        :param config_number_of_notifications_redriven_to_dlq_alarm: The configuration for the NumberOfNotificationsRedrivenToDlq alarm.
        :param default_alarm_action: The default action to take when an alarm is triggered. Default: - None
        :param default_insufficient_data_action: The default action to take when an alarm has insufficient data. Default: - None
        :param default_ok_action: The default action to take when an alarm enters the ok state. Default: - None
        :param exclude_alarms: Alarm metrics to exclude from the recommended alarms. Default: - None
        :param exclude_resources: The resources to exclude from the recommended alarms. Use a resources id to exclude a specific resource.
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Best_Practice_Recommended_Alarms_AWS_Services.html#SNS
        '''
        props = SnsRecommendedAlarmsConfig(
            config_number_of_messages_published_alarm=config_number_of_messages_published_alarm,
            config_number_of_notifications_delivered_alarm=config_number_of_notifications_delivered_alarm,
            config_number_of_notifications_failed_alarm=config_number_of_notifications_failed_alarm,
            config_number_of_notifications_failed_to_redrive_to_dlq_alarm=config_number_of_notifications_failed_to_redrive_to_dlq_alarm,
            config_number_of_notifications_filtered_out_invalid_attributes_alarm=config_number_of_notifications_filtered_out_invalid_attributes_alarm,
            config_number_of_notifications_filtered_out_invalid_message_body_alarm=config_number_of_notifications_filtered_out_invalid_message_body_alarm,
            config_number_of_notifications_redriven_to_dlq_alarm=config_number_of_notifications_redriven_to_dlq_alarm,
            default_alarm_action=default_alarm_action,
            default_insufficient_data_action=default_insufficient_data_action,
            default_ok_action=default_ok_action,
            exclude_alarms=exclude_alarms,
            exclude_resources=exclude_resources,
            treat_missing_data=treat_missing_data,
        )

        return typing.cast(SnsRecommendedAlarms, jsii.invoke(self, "applyRecommendedAlarms", [props]))


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.S3Bucket4xxErrorsAlarmConfig",
    jsii_struct_bases=[S3BucketHttpErrorsAlarmConfig],
    name_mapping={
        "alarm_action": "alarmAction",
        "insufficient_data_action": "insufficientDataAction",
        "ok_action": "okAction",
        "treat_missing_data": "treatMissingData",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluation_periods": "evaluationPeriods",
        "period": "period",
        "threshold": "threshold",
        "alarm_description": "alarmDescription",
        "alarm_name": "alarmName",
    },
)
class S3Bucket4xxErrorsAlarmConfig(S3BucketHttpErrorsAlarmConfig):
    def __init__(
        self,
        *,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        threshold: typing.Optional[jsii.Number] = None,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration for the 4xx errors alarm.

        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 15
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 15
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param threshold: The value against which the specified statistic is compared. Default: 0.05
        :param alarm_description: The alarm description. Default: - This alarm helps us report the total number of 4xx error status codes that are made in response to client requests. 403 error codes might indicate an incorrect IAM policy, and 404 error codes might indicate mis-behaving client application, for example. Enabling S3 server access logging on a temporary basis will help you to pinpoint the issue's origin using the fields HTTP status and Error Code. To understand more about the error code, see Error Responses (https://docs.aws.amazon.com/AmazonS3/latest/API/ErrorResponses.html).
        :param alarm_name: The alarm name. Default: - bucket.bucketName + ' - 4xxErrors'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d45cfb8defe415c756707cf35150f504c3ca42a23dece0314de672338d762779)
            check_type(argname="argument alarm_action", value=alarm_action, expected_type=type_hints["alarm_action"])
            check_type(argname="argument insufficient_data_action", value=insufficient_data_action, expected_type=type_hints["insufficient_data_action"])
            check_type(argname="argument ok_action", value=ok_action, expected_type=type_hints["ok_action"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument alarm_description", value=alarm_description, expected_type=type_hints["alarm_description"])
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alarm_action is not None:
            self._values["alarm_action"] = alarm_action
        if insufficient_data_action is not None:
            self._values["insufficient_data_action"] = insufficient_data_action
        if ok_action is not None:
            self._values["ok_action"] = ok_action
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluation_periods is not None:
            self._values["evaluation_periods"] = evaluation_periods
        if period is not None:
            self._values["period"] = period
        if threshold is not None:
            self._values["threshold"] = threshold
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if alarm_name is not None:
            self._values["alarm_name"] = alarm_name

    @builtins.property
    def alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of data points that must be breaching to trigger the alarm.

        :default: 15
        '''
        result = self._values.get("datapoints_to_alarm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''The number of periods over which data is compared to the specified threshold.

        :default: 15
        '''
        result = self._values.get("evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The period over which the specified statistic is applied.

        :default: Duration.minutes(1)
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def threshold(self) -> typing.Optional[jsii.Number]:
        '''The value against which the specified statistic is compared.

        :default: 0.05
        '''
        result = self._values.get("threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        '''The alarm description.

        :default:

        - This alarm helps us report the total number of 4xx error status codes
        that are made in response to client requests. 403 error codes might indicate an
        incorrect IAM policy, and 404 error codes might indicate mis-behaving client application,
        for example. Enabling S3 server access logging on a temporary basis will help you to
        pinpoint the issue's origin using the fields HTTP status and Error Code. To understand
        more about the error code, see Error Responses
        (https://docs.aws.amazon.com/AmazonS3/latest/API/ErrorResponses.html).
        '''
        result = self._values.get("alarm_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_name(self) -> typing.Optional[builtins.str]:
        '''The alarm name.

        :default: - bucket.bucketName + ' - 4xxErrors'
        '''
        result = self._values.get("alarm_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3Bucket4xxErrorsAlarmConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.S3Bucket4xxErrorsAlarmProps",
    jsii_struct_bases=[S3Bucket4xxErrorsAlarmConfig],
    name_mapping={
        "alarm_action": "alarmAction",
        "insufficient_data_action": "insufficientDataAction",
        "ok_action": "okAction",
        "treat_missing_data": "treatMissingData",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluation_periods": "evaluationPeriods",
        "period": "period",
        "threshold": "threshold",
        "alarm_description": "alarmDescription",
        "alarm_name": "alarmName",
        "bucket": "bucket",
    },
)
class S3Bucket4xxErrorsAlarmProps(S3Bucket4xxErrorsAlarmConfig):
    def __init__(
        self,
        *,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        threshold: typing.Optional[jsii.Number] = None,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    ) -> None:
        '''Properties for the S3Bucket4xxErrorsAlarm construct.

        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 15
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 15
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param threshold: The value against which the specified statistic is compared. Default: 0.05
        :param alarm_description: The alarm description. Default: - This alarm helps us report the total number of 4xx error status codes that are made in response to client requests. 403 error codes might indicate an incorrect IAM policy, and 404 error codes might indicate mis-behaving client application, for example. Enabling S3 server access logging on a temporary basis will help you to pinpoint the issue's origin using the fields HTTP status and Error Code. To understand more about the error code, see Error Responses (https://docs.aws.amazon.com/AmazonS3/latest/API/ErrorResponses.html).
        :param alarm_name: The alarm name. Default: - bucket.bucketName + ' - 4xxErrors'
        :param bucket: The S3 bucket to monitor.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42ecd95425c9d23d522911d78398932e1d8493d1db2971c7b392f778fbcdb03f)
            check_type(argname="argument alarm_action", value=alarm_action, expected_type=type_hints["alarm_action"])
            check_type(argname="argument insufficient_data_action", value=insufficient_data_action, expected_type=type_hints["insufficient_data_action"])
            check_type(argname="argument ok_action", value=ok_action, expected_type=type_hints["ok_action"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument alarm_description", value=alarm_description, expected_type=type_hints["alarm_description"])
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
        }
        if alarm_action is not None:
            self._values["alarm_action"] = alarm_action
        if insufficient_data_action is not None:
            self._values["insufficient_data_action"] = insufficient_data_action
        if ok_action is not None:
            self._values["ok_action"] = ok_action
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluation_periods is not None:
            self._values["evaluation_periods"] = evaluation_periods
        if period is not None:
            self._values["period"] = period
        if threshold is not None:
            self._values["threshold"] = threshold
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if alarm_name is not None:
            self._values["alarm_name"] = alarm_name

    @builtins.property
    def alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of data points that must be breaching to trigger the alarm.

        :default: 15
        '''
        result = self._values.get("datapoints_to_alarm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''The number of periods over which data is compared to the specified threshold.

        :default: 15
        '''
        result = self._values.get("evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The period over which the specified statistic is applied.

        :default: Duration.minutes(1)
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def threshold(self) -> typing.Optional[jsii.Number]:
        '''The value against which the specified statistic is compared.

        :default: 0.05
        '''
        result = self._values.get("threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        '''The alarm description.

        :default:

        - This alarm helps us report the total number of 4xx error status codes
        that are made in response to client requests. 403 error codes might indicate an
        incorrect IAM policy, and 404 error codes might indicate mis-behaving client application,
        for example. Enabling S3 server access logging on a temporary basis will help you to
        pinpoint the issue's origin using the fields HTTP status and Error Code. To understand
        more about the error code, see Error Responses
        (https://docs.aws.amazon.com/AmazonS3/latest/API/ErrorResponses.html).
        '''
        result = self._values.get("alarm_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_name(self) -> typing.Optional[builtins.str]:
        '''The alarm name.

        :default: - bucket.bucketName + ' - 4xxErrors'
        '''
        result = self._values.get("alarm_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket(self) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        '''The S3 bucket to monitor.'''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3Bucket4xxErrorsAlarmProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.S3Bucket5xxErrorsAlarmConfig",
    jsii_struct_bases=[S3BucketHttpErrorsAlarmConfig],
    name_mapping={
        "alarm_action": "alarmAction",
        "insufficient_data_action": "insufficientDataAction",
        "ok_action": "okAction",
        "treat_missing_data": "treatMissingData",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluation_periods": "evaluationPeriods",
        "period": "period",
        "threshold": "threshold",
        "alarm_description": "alarmDescription",
        "alarm_name": "alarmName",
    },
)
class S3Bucket5xxErrorsAlarmConfig(S3BucketHttpErrorsAlarmConfig):
    def __init__(
        self,
        *,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        threshold: typing.Optional[jsii.Number] = None,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration for the 5xx errors alarm.

        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 15
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 15
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param threshold: The value against which the specified statistic is compared. Default: 0.05
        :param alarm_description: The alarm description. Default: - This alarm helps you detect a high number of server-side errors. These errors indicate that a client made a request that the server couldn’t complete. This can help you correlate the issue your application is facing because of S3. For more information to help you efficiently handle or reduce errors, see Optimizing performance design patterns (https://docs.aws.amazon.com/AmazonS3/latest/userguide/optimizing-performance-design-patterns.html#optimizing-performance-timeouts-retries). Errors might also be caused by an the issue with S3, check AWS service health dashboard for the status of Amazon S3 in your Region.
        :param alarm_name: The alarm name. Default: - bucket.bucketName + ' - 5xxErrors'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1679196b0a9e5117c7a636cfb7f006fee301925d2a4605be64b230bdd8dd1a0a)
            check_type(argname="argument alarm_action", value=alarm_action, expected_type=type_hints["alarm_action"])
            check_type(argname="argument insufficient_data_action", value=insufficient_data_action, expected_type=type_hints["insufficient_data_action"])
            check_type(argname="argument ok_action", value=ok_action, expected_type=type_hints["ok_action"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument alarm_description", value=alarm_description, expected_type=type_hints["alarm_description"])
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alarm_action is not None:
            self._values["alarm_action"] = alarm_action
        if insufficient_data_action is not None:
            self._values["insufficient_data_action"] = insufficient_data_action
        if ok_action is not None:
            self._values["ok_action"] = ok_action
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluation_periods is not None:
            self._values["evaluation_periods"] = evaluation_periods
        if period is not None:
            self._values["period"] = period
        if threshold is not None:
            self._values["threshold"] = threshold
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if alarm_name is not None:
            self._values["alarm_name"] = alarm_name

    @builtins.property
    def alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of data points that must be breaching to trigger the alarm.

        :default: 15
        '''
        result = self._values.get("datapoints_to_alarm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''The number of periods over which data is compared to the specified threshold.

        :default: 15
        '''
        result = self._values.get("evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The period over which the specified statistic is applied.

        :default: Duration.minutes(1)
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def threshold(self) -> typing.Optional[jsii.Number]:
        '''The value against which the specified statistic is compared.

        :default: 0.05
        '''
        result = self._values.get("threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        '''The alarm description.

        :default:

        - This alarm helps you detect a high number of server-side errors. These errors indicate
        that a client made a request that the server couldn’t complete. This can help you correlate the
        issue your application is facing because of S3. For more information to help you efficiently
        handle or reduce errors, see Optimizing performance design patterns
        (https://docs.aws.amazon.com/AmazonS3/latest/userguide/optimizing-performance-design-patterns.html#optimizing-performance-timeouts-retries).
        Errors might also be caused by an the issue with S3, check AWS service health dashboard for the status of Amazon S3 in your Region.
        '''
        result = self._values.get("alarm_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_name(self) -> typing.Optional[builtins.str]:
        '''The alarm name.

        :default: - bucket.bucketName + ' - 5xxErrors'
        '''
        result = self._values.get("alarm_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3Bucket5xxErrorsAlarmConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-cloudwatch-alarms.S3Bucket5xxErrorsAlarmProps",
    jsii_struct_bases=[S3Bucket5xxErrorsAlarmConfig],
    name_mapping={
        "alarm_action": "alarmAction",
        "insufficient_data_action": "insufficientDataAction",
        "ok_action": "okAction",
        "treat_missing_data": "treatMissingData",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluation_periods": "evaluationPeriods",
        "period": "period",
        "threshold": "threshold",
        "alarm_description": "alarmDescription",
        "alarm_name": "alarmName",
        "bucket": "bucket",
    },
)
class S3Bucket5xxErrorsAlarmProps(S3Bucket5xxErrorsAlarmConfig):
    def __init__(
        self,
        *,
        alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
        treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        threshold: typing.Optional[jsii.Number] = None,
        alarm_description: typing.Optional[builtins.str] = None,
        alarm_name: typing.Optional[builtins.str] = None,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    ) -> None:
        '''Properties for the S3Bucket5xxErrorsAlarm construct.

        :param alarm_action: The action to take when an alarm is triggered. Default: - None
        :param insufficient_data_action: The action to take when an alarm has insufficient data. Default: - None
        :param ok_action: The action to take when an alarm enters the ok state. Default: - None
        :param treat_missing_data: How to handle missing data for this alarm. Default: TreatMissingData.MISSING
        :param datapoints_to_alarm: The number of data points that must be breaching to trigger the alarm. Default: 15
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold. Default: 15
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(1)
        :param threshold: The value against which the specified statistic is compared. Default: 0.05
        :param alarm_description: The alarm description. Default: - This alarm helps you detect a high number of server-side errors. These errors indicate that a client made a request that the server couldn’t complete. This can help you correlate the issue your application is facing because of S3. For more information to help you efficiently handle or reduce errors, see Optimizing performance design patterns (https://docs.aws.amazon.com/AmazonS3/latest/userguide/optimizing-performance-design-patterns.html#optimizing-performance-timeouts-retries). Errors might also be caused by an the issue with S3, check AWS service health dashboard for the status of Amazon S3 in your Region.
        :param alarm_name: The alarm name. Default: - bucket.bucketName + ' - 5xxErrors'
        :param bucket: The S3 bucket to monitor.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1804ab3695bf52f69bd745c3d4ab5e213eb7fb6b4cc260c31532a53abb2b3d7f)
            check_type(argname="argument alarm_action", value=alarm_action, expected_type=type_hints["alarm_action"])
            check_type(argname="argument insufficient_data_action", value=insufficient_data_action, expected_type=type_hints["insufficient_data_action"])
            check_type(argname="argument ok_action", value=ok_action, expected_type=type_hints["ok_action"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument alarm_description", value=alarm_description, expected_type=type_hints["alarm_description"])
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
        }
        if alarm_action is not None:
            self._values["alarm_action"] = alarm_action
        if insufficient_data_action is not None:
            self._values["insufficient_data_action"] = insufficient_data_action
        if ok_action is not None:
            self._values["ok_action"] = ok_action
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluation_periods is not None:
            self._values["evaluation_periods"] = evaluation_periods
        if period is not None:
            self._values["period"] = period
        if threshold is not None:
            self._values["threshold"] = threshold
        if alarm_description is not None:
            self._values["alarm_description"] = alarm_description
        if alarm_name is not None:
            self._values["alarm_name"] = alarm_name

    @builtins.property
    def alarm_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm is triggered.

        :default: - None
        '''
        result = self._values.get("alarm_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def insufficient_data_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm has insufficient data.

        :default: - None
        '''
        result = self._values.get("insufficient_data_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def ok_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction]:
        '''The action to take when an alarm enters the ok state.

        :default: - None
        '''
        result = self._values.get("ok_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction], result)

    @builtins.property
    def treat_missing_data(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData]:
        '''How to handle missing data for this alarm.

        :default: TreatMissingData.MISSING
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData], result)

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of data points that must be breaching to trigger the alarm.

        :default: 15
        '''
        result = self._values.get("datapoints_to_alarm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''The number of periods over which data is compared to the specified threshold.

        :default: 15
        '''
        result = self._values.get("evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The period over which the specified statistic is applied.

        :default: Duration.minutes(1)
        '''
        result = self._values.get("period")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def threshold(self) -> typing.Optional[jsii.Number]:
        '''The value against which the specified statistic is compared.

        :default: 0.05
        '''
        result = self._values.get("threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def alarm_description(self) -> typing.Optional[builtins.str]:
        '''The alarm description.

        :default:

        - This alarm helps you detect a high number of server-side errors. These errors indicate
        that a client made a request that the server couldn’t complete. This can help you correlate the
        issue your application is facing because of S3. For more information to help you efficiently
        handle or reduce errors, see Optimizing performance design patterns
        (https://docs.aws.amazon.com/AmazonS3/latest/userguide/optimizing-performance-design-patterns.html#optimizing-performance-timeouts-retries).
        Errors might also be caused by an the issue with S3, check AWS service health dashboard for the status of Amazon S3 in your Region.
        '''
        result = self._values.get("alarm_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_name(self) -> typing.Optional[builtins.str]:
        '''The alarm name.

        :default: - bucket.bucketName + ' - 5xxErrors'
        '''
        result = self._values.get("alarm_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket(self) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        '''The S3 bucket to monitor.'''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3Bucket5xxErrorsAlarmProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AlarmBaseProps",
    "Bucket",
    "Function",
    "LambdaAlarmBaseConfig",
    "LambdaConcurrentExecutionsAlarm",
    "LambdaConcurrentExecutionsAlarmConfig",
    "LambdaConcurrentExecutionsAlarmProps",
    "LambdaDurationAlarm",
    "LambdaDurationAlarmConfig",
    "LambdaDurationAlarmProps",
    "LambdaErrorsAlarm",
    "LambdaErrorsAlarmConfig",
    "LambdaErrorsAlarmProps",
    "LambdaRecommendedAlarms",
    "LambdaRecommendedAlarmsAspect",
    "LambdaRecommendedAlarmsConfig",
    "LambdaRecommendedAlarmsMetrics",
    "LambdaRecommendedAlarmsProps",
    "LambdaThrottlesAlarm",
    "LambdaThrottlesAlarmConfig",
    "LambdaThrottlesAlarmProps",
    "Queue",
    "S3Bucket4xxErrorsAlarm",
    "S3Bucket4xxErrorsAlarmConfig",
    "S3Bucket4xxErrorsAlarmProps",
    "S3Bucket5xxErrorsAlarm",
    "S3Bucket5xxErrorsAlarmConfig",
    "S3Bucket5xxErrorsAlarmProps",
    "S3BucketHttpErrorsAlarmConfig",
    "S3RecommendedAlarms",
    "S3RecommendedAlarmsAspect",
    "S3RecommendedAlarmsConfig",
    "S3RecommendedAlarmsMetrics",
    "S3RecommendedAlarmsProps",
    "SnsAlarmBaseConfig",
    "SnsNumberOfMessagesPublishedAlarm",
    "SnsNumberOfMessagesPublishedAlarmConfig",
    "SnsNumberOfMessagesPublishedAlarmProps",
    "SnsNumberOfNotificationsDeliveredAlarm",
    "SnsNumberOfNotificationsDeliveredAlarmConfig",
    "SnsNumberOfNotificationsDeliveredAlarmProps",
    "SnsNumberOfNotificationsFailedAlarm",
    "SnsNumberOfNotificationsFailedAlarmConfig",
    "SnsNumberOfNotificationsFailedAlarmProps",
    "SnsNumberOfNotificationsFailedToRedriveToDlqAlarm",
    "SnsNumberOfNotificationsFailedToRedriveToDlqAlarmConfig",
    "SnsNumberOfNotificationsFailedToRedriveToDlqAlarmProps",
    "SnsNumberOfNotificationsFilteredOutInvalidAttributesAlarm",
    "SnsNumberOfNotificationsFilteredOutInvalidAttributesAlarmConfig",
    "SnsNumberOfNotificationsFilteredOutInvalidAttributesAlarmProps",
    "SnsNumberOfNotificationsFilteredOutInvalidMessageBodyAlarm",
    "SnsNumberOfNotificationsFilteredOutInvalidMessageBodyAlarmConfig",
    "SnsNumberOfNotificationsFilteredOutInvalidMessageBodyAlarmProps",
    "SnsNumberOfNotificationsRedrivenToDlqAlarm",
    "SnsNumberOfNotificationsRedrivenToDlqAlarmConfig",
    "SnsNumberOfNotificationsRedrivenToDlqAlarmProps",
    "SnsRecommendedAlarms",
    "SnsRecommendedAlarmsAspect",
    "SnsRecommendedAlarmsConfig",
    "SnsRecommendedAlarmsMetrics",
    "SnsRecommendedAlarmsProps",
    "SqsAlarmBaseConfig",
    "SqsApproximateAgeOfOldestMessageAlarm",
    "SqsApproximateAgeOfOldestMessageAlarmConfig",
    "SqsApproximateAgeOfOldestMessageAlarmProps",
    "SqsApproximateNumberOfMessagesNotVisibleAlarm",
    "SqsApproximateNumberOfMessagesNotVisibleAlarmConfig",
    "SqsApproximateNumberOfMessagesNotVisibleAlarmProps",
    "SqsApproximateNumberOfMessagesVisibleAlarm",
    "SqsApproximateNumberOfMessagesVisibleAlarmConfig",
    "SqsApproximateNumberOfMessagesVisibleAlarmProps",
    "SqsNumberOfMessagesSentAlarm",
    "SqsNumberOfMessagesSentAlarmConfig",
    "SqsNumberOfMessagesSentAlarmProps",
    "SqsRecommendedAlarms",
    "SqsRecommendedAlarmsAspect",
    "SqsRecommendedAlarmsConfig",
    "SqsRecommendedAlarmsMetrics",
    "SqsRecommendedAlarmsProps",
    "Topic",
]

publication.publish()

def _typecheckingstub__dc8826645a1e265ceca74e67c468d47f270a951fd40c4c3bcf8922d80e34f685(
    *,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__997fd23e9dec2f8580d4a0f3905a7216624c6b51043d6491f7523aa123af316d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    access_control: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketAccessControl] = None,
    auto_delete_objects: typing.Optional[builtins.bool] = None,
    block_public_access: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BlockPublicAccess] = None,
    bucket_key_enabled: typing.Optional[builtins.bool] = None,
    bucket_name: typing.Optional[builtins.str] = None,
    cors: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.CorsRule, typing.Dict[builtins.str, typing.Any]]]] = None,
    encryption: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketEncryption] = None,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    enforce_ssl: typing.Optional[builtins.bool] = None,
    event_bridge_enabled: typing.Optional[builtins.bool] = None,
    intelligent_tiering_configurations: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.IntelligentTieringConfiguration, typing.Dict[builtins.str, typing.Any]]]] = None,
    inventories: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.Inventory, typing.Dict[builtins.str, typing.Any]]]] = None,
    lifecycle_rules: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.LifecycleRule, typing.Dict[builtins.str, typing.Any]]]] = None,
    metrics: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.BucketMetrics, typing.Dict[builtins.str, typing.Any]]]] = None,
    minimum_tls_version: typing.Optional[jsii.Number] = None,
    notifications_handler_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    notifications_skip_destination_validation: typing.Optional[builtins.bool] = None,
    object_lock_default_retention: typing.Optional[_aws_cdk_aws_s3_ceddda9d.ObjectLockRetention] = None,
    object_lock_enabled: typing.Optional[builtins.bool] = None,
    object_ownership: typing.Optional[_aws_cdk_aws_s3_ceddda9d.ObjectOwnership] = None,
    public_read_access: typing.Optional[builtins.bool] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    server_access_logs_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
    server_access_logs_prefix: typing.Optional[builtins.str] = None,
    target_object_key_format: typing.Optional[_aws_cdk_aws_s3_ceddda9d.TargetObjectKeyFormat] = None,
    transfer_acceleration: typing.Optional[builtins.bool] = None,
    versioned: typing.Optional[builtins.bool] = None,
    website_error_document: typing.Optional[builtins.str] = None,
    website_index_document: typing.Optional[builtins.str] = None,
    website_redirect: typing.Optional[typing.Union[_aws_cdk_aws_s3_ceddda9d.RedirectTarget, typing.Dict[builtins.str, typing.Any]]] = None,
    website_routing_rules: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.RoutingRule, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__300e1b7b513ed361a8dde12f23c6adb84738ebf013386259a5dbea5024022ffa(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    code: _aws_cdk_aws_lambda_ceddda9d.Code,
    handler: builtins.str,
    runtime: _aws_cdk_aws_lambda_ceddda9d.Runtime,
    adot_instrumentation: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.AdotInstrumentationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    allow_all_outbound: typing.Optional[builtins.bool] = None,
    allow_public_subnet: typing.Optional[builtins.bool] = None,
    application_log_level: typing.Optional[builtins.str] = None,
    application_log_level_v2: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.ApplicationLogLevel] = None,
    architecture: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture] = None,
    code_signing_config: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.ICodeSigningConfig] = None,
    current_version_options: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.VersionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    dead_letter_queue_enabled: typing.Optional[builtins.bool] = None,
    dead_letter_topic: typing.Optional[_aws_cdk_aws_sns_ceddda9d.ITopic] = None,
    description: typing.Optional[builtins.str] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    environment_encryption: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    ephemeral_storage_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    events: typing.Optional[typing.Sequence[_aws_cdk_aws_lambda_ceddda9d.IEventSource]] = None,
    filesystem: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.FileSystem] = None,
    function_name: typing.Optional[builtins.str] = None,
    initial_policy: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]] = None,
    insights_version: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.LambdaInsightsVersion] = None,
    ipv6_allowed_for_dual_stack: typing.Optional[builtins.bool] = None,
    layers: typing.Optional[typing.Sequence[_aws_cdk_aws_lambda_ceddda9d.ILayerVersion]] = None,
    log_format: typing.Optional[builtins.str] = None,
    logging_format: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.LoggingFormat] = None,
    log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    log_retention_retry_options: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.LogRetentionRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    log_retention_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    memory_size: typing.Optional[jsii.Number] = None,
    params_and_secrets: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.ParamsAndSecretsLayerVersion] = None,
    profiling: typing.Optional[builtins.bool] = None,
    profiling_group: typing.Optional[_aws_cdk_aws_codeguruprofiler_ceddda9d.IProfilingGroup] = None,
    recursive_loop: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.RecursiveLoop] = None,
    reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    runtime_management_mode: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.RuntimeManagementMode] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    snap_start: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.SnapStartConf] = None,
    system_log_level: typing.Optional[builtins.str] = None,
    system_log_level_v2: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.SystemLogLevel] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    tracing: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Tracing] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    on_failure: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination] = None,
    on_success: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__716b419718f93d506f3a8f28e319b9f808eddee3d4641ebd195dccca8d474eec(
    *,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bfb27966b8b66696e58f0cdca63f38b3e4abd2f029e1dcdd883870f471a74c7(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    lambda_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    threshold: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f6d24fc2ab7dcff701615e4987ae78b3dd173cefd3eb98f56fd3cd288d75b47(
    *,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d8926f47d763f0933cbd527860988a8a2749c891924dcd36c2f3f1e29039d6f(
    *,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    threshold: typing.Optional[jsii.Number] = None,
    lambda_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e14f288432f1c93dade6ca87e081a4cf16901cbcbef6b7c783c411f561140323(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    lambda_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
    threshold: jsii.Number,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16f9aa6367d9f62672010c74b9c77970e9a4ad803a8333d788aa6ea4f74dfb61(
    *,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    threshold: jsii.Number,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c35e2842ae53ffd154b79e7db69c642434d4bb574cd771ed7bdc184108099771(
    *,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    threshold: jsii.Number,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    lambda_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f5d57bf581f2eea2bb19216346016a8105d14c7a16a9ac673410b280a87fc3a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    lambda_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
    threshold: jsii.Number,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a80f94cd00993ff5508c02a09a080a5e3dfe40d123f162a15591a81b8faf940(
    *,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    threshold: jsii.Number,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__065075f4736ec308df17eee0d6a5100064d7a899d094aeb4533fdde663ffc607(
    *,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    threshold: jsii.Number,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    lambda_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27101909e8d5207062982ebba2ceaa835aa71fc168b8d767b66d1a5c1a11d99b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    lambda_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
    config_duration_alarm: typing.Union[LambdaDurationAlarmConfig, typing.Dict[builtins.str, typing.Any]],
    config_errors_alarm: typing.Union[LambdaErrorsAlarmConfig, typing.Dict[builtins.str, typing.Any]],
    config_throttles_alarm: typing.Union[LambdaThrottlesAlarmConfig, typing.Dict[builtins.str, typing.Any]],
    config_concurrent_executions_alarm: typing.Optional[typing.Union[LambdaConcurrentExecutionsAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    default_alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    default_insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    default_ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    exclude_alarms: typing.Optional[typing.Sequence[LambdaRecommendedAlarmsMetrics]] = None,
    exclude_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ac98314bcd4923aabdf6919cacbc99fe09b02e5eba9973007f013c04c677d9e(
    node: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cd52c68a63a1358db1966d2a14b5e03f18458ff71753842a0c469174dd15066(
    *,
    config_duration_alarm: typing.Union[LambdaDurationAlarmConfig, typing.Dict[builtins.str, typing.Any]],
    config_errors_alarm: typing.Union[LambdaErrorsAlarmConfig, typing.Dict[builtins.str, typing.Any]],
    config_throttles_alarm: typing.Union[LambdaThrottlesAlarmConfig, typing.Dict[builtins.str, typing.Any]],
    config_concurrent_executions_alarm: typing.Optional[typing.Union[LambdaConcurrentExecutionsAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    default_alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    default_insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    default_ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    exclude_alarms: typing.Optional[typing.Sequence[LambdaRecommendedAlarmsMetrics]] = None,
    exclude_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2028de2c7bc54f62581b4499458b79fb36fb2c32306e074814ca31178c7a120(
    *,
    config_duration_alarm: typing.Union[LambdaDurationAlarmConfig, typing.Dict[builtins.str, typing.Any]],
    config_errors_alarm: typing.Union[LambdaErrorsAlarmConfig, typing.Dict[builtins.str, typing.Any]],
    config_throttles_alarm: typing.Union[LambdaThrottlesAlarmConfig, typing.Dict[builtins.str, typing.Any]],
    config_concurrent_executions_alarm: typing.Optional[typing.Union[LambdaConcurrentExecutionsAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    default_alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    default_insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    default_ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    exclude_alarms: typing.Optional[typing.Sequence[LambdaRecommendedAlarmsMetrics]] = None,
    exclude_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    lambda_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__488351c06ad0ced06f68b654c629b883306654b7e2b923062e130cd249a4ad16(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    lambda_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
    threshold: jsii.Number,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73e2fd37e074d8437164ecec0a7146e6185d991ab6cce0ab1f03a6d551db8a84(
    *,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    threshold: jsii.Number,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e1cacf0523a9e7229f0a95e8fd3bb47e8e7bceca45491724237db0109dd5b93(
    *,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    threshold: jsii.Number,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    lambda_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e63632b9287782cde140e2fa25c2d500852c1e3fdad4c8d2118b305c4ebd894d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    content_based_deduplication: typing.Optional[builtins.bool] = None,
    data_key_reuse: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    dead_letter_queue: typing.Optional[typing.Union[_aws_cdk_aws_sqs_ceddda9d.DeadLetterQueue, typing.Dict[builtins.str, typing.Any]]] = None,
    deduplication_scope: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.DeduplicationScope] = None,
    delivery_delay: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    encryption: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.QueueEncryption] = None,
    encryption_master_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    enforce_ssl: typing.Optional[builtins.bool] = None,
    fifo: typing.Optional[builtins.bool] = None,
    fifo_throughput_limit: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.FifoThroughputLimit] = None,
    max_message_size_bytes: typing.Optional[jsii.Number] = None,
    queue_name: typing.Optional[builtins.str] = None,
    receive_message_wait_time: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    redrive_allow_policy: typing.Optional[typing.Union[_aws_cdk_aws_sqs_ceddda9d.RedriveAllowPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    retention_period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    visibility_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9d4f29388ca9807519ae0412e8634338d955302b834578576dc547f464049e6(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    threshold: typing.Optional[jsii.Number] = None,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e32caa975316b8e881679f0e3ca0297c5c175dcc49fcb62b683c66bf9f5782bb(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    threshold: typing.Optional[jsii.Number] = None,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2fd29de3b481f2cfa00b9af24444e83bc204407864373f5dd40399adff9991d(
    *,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47bd74a1f4cc68aa49abcb9ddefc859f62a8d650ec660e1f1dc076405de12203(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    config4xx_errors_alarm: typing.Optional[typing.Union[S3Bucket4xxErrorsAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    config5xx_errors_alarm: typing.Optional[typing.Union[S3Bucket5xxErrorsAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    default_alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    default_insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    default_ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    exclude_alarms: typing.Optional[typing.Sequence[S3RecommendedAlarmsMetrics]] = None,
    exclude_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81cb56b973536fefe93bd8cdf5503a61b0f7a86c873b9ea667e56303d99c024b(
    node: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a54261617c599ef9e038be027b2446bed17b11cfdf8002aee30d2b71f6ea7868(
    *,
    config4xx_errors_alarm: typing.Optional[typing.Union[S3Bucket4xxErrorsAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    config5xx_errors_alarm: typing.Optional[typing.Union[S3Bucket5xxErrorsAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    default_alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    default_insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    default_ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    exclude_alarms: typing.Optional[typing.Sequence[S3RecommendedAlarmsMetrics]] = None,
    exclude_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bffe2626f56a0b42370556b496eae7b36c626ba33a4d8d3b6ee7cf6c6e78caeb(
    *,
    config4xx_errors_alarm: typing.Optional[typing.Union[S3Bucket4xxErrorsAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    config5xx_errors_alarm: typing.Optional[typing.Union[S3Bucket5xxErrorsAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    default_alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    default_insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    default_ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    exclude_alarms: typing.Optional[typing.Sequence[S3RecommendedAlarmsMetrics]] = None,
    exclude_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6357da9f37e3e6b457ad09023bb9b95a1d5a38c2f284fa206c1d1d7696f94317(
    *,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98752834db6066573e1bc3fdef96ce5810035499b582fbd50205da8ca10e443a(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    topic: _aws_cdk_aws_sns_ceddda9d.ITopic,
    threshold: jsii.Number,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02d28bbf6430187b0f9eb1fb025b748f1a32141c7c491a091b9c54a910e6b18e(
    *,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    threshold: jsii.Number,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fff028ea41836c29985adfc761cb4e4d9d91324dab443383b2985d7174500a19(
    *,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    threshold: jsii.Number,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    topic: _aws_cdk_aws_sns_ceddda9d.ITopic,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6373f947a105537f03e197d13ae190cc1b538074b51e0b7eccd8b7956fedc0f3(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    topic: _aws_cdk_aws_sns_ceddda9d.ITopic,
    threshold: jsii.Number,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b868a50184ae2ac664cf01403a36fff774472e3686b89e5367994e98b89b7193(
    *,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    threshold: jsii.Number,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f42d7a4b791067bced9bc860e1f750a1ceba252cff97a6f74fd0c6a844a539e(
    *,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    threshold: jsii.Number,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    topic: _aws_cdk_aws_sns_ceddda9d.ITopic,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__170e0b0914195c00ff510974ac188dcdce904364b454920cfa694a9c41aea277(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    topic: _aws_cdk_aws_sns_ceddda9d.ITopic,
    threshold: jsii.Number,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49e12faa9093bf4d0205ccf60bc9d460839db4afed6958548942f1f348123faa(
    *,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    threshold: jsii.Number,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__892a2b84330c3cd2ff63a79b19f87b73eb88ccfb60ed575de749f562223b34f0(
    *,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    threshold: jsii.Number,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    topic: _aws_cdk_aws_sns_ceddda9d.ITopic,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__328952b7f137facf3708a3106b8d39dc7959798db5ba6df8bb7ee4ef4e058cfb(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    topic: _aws_cdk_aws_sns_ceddda9d.ITopic,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    threshold: typing.Optional[jsii.Number] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__843a4ee9894a844d5695f53e1c878efbf75b200de41a577d4f371b236240f2e8(
    *,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3739e80c1d6309d7906dad7d9e84785a3a83e15921d956349e5a35ee350151b(
    *,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    threshold: typing.Optional[jsii.Number] = None,
    topic: _aws_cdk_aws_sns_ceddda9d.ITopic,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43139b7affdf7f55134351c485459ce357015c4e7c697ae842d1c8d514b65565(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    topic: _aws_cdk_aws_sns_ceddda9d.ITopic,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    threshold: typing.Optional[jsii.Number] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec0121c20b9a0c13a285aa11cf4f02cfa52f0fa656d8e6a0359dce149cf04fcf(
    *,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75001c0fbc3b728c4c377f661f9af34f7b2005073f8201f295eda55eecf79ff2(
    *,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    threshold: typing.Optional[jsii.Number] = None,
    topic: _aws_cdk_aws_sns_ceddda9d.ITopic,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b0eb47a2c3fa8f34233ebb68267787d38ab91e5dbd2e593d54eb6b6833c21bb(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    topic: _aws_cdk_aws_sns_ceddda9d.ITopic,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    threshold: typing.Optional[jsii.Number] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7144b6b471d3381a8a22ad7e1411624239d41faade4130e5d45a811d5546fe73(
    *,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68a91c07dfcbd0aacb0e3c594d36678ba3a1e134a863504ce2a39c87c7da0221(
    *,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    threshold: typing.Optional[jsii.Number] = None,
    topic: _aws_cdk_aws_sns_ceddda9d.ITopic,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5333c0338ea3e3f055d2c8daafb1ec07493b232256425a8befa7dc813db863eb(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    topic: _aws_cdk_aws_sns_ceddda9d.ITopic,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    threshold: typing.Optional[jsii.Number] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62b63074ae7184f232bd0e5938c481c0494ea3e231fea4a6974e72aca3250ee9(
    *,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2f1df38bb641261070fb8b92d0e55844593ac7973d092bf2fd4d6763627299e(
    *,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    threshold: typing.Optional[jsii.Number] = None,
    topic: _aws_cdk_aws_sns_ceddda9d.ITopic,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98630e12118de7c882d18933f387c3a322a8c8af12b4b511ecf7e03804a5775d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    topic: _aws_cdk_aws_sns_ceddda9d.ITopic,
    config_number_of_messages_published_alarm: typing.Union[SnsNumberOfMessagesPublishedAlarmConfig, typing.Dict[builtins.str, typing.Any]],
    config_number_of_notifications_delivered_alarm: typing.Union[SnsNumberOfNotificationsDeliveredAlarmConfig, typing.Dict[builtins.str, typing.Any]],
    config_number_of_notifications_failed_alarm: typing.Union[SnsNumberOfNotificationsFailedAlarmConfig, typing.Dict[builtins.str, typing.Any]],
    config_number_of_notifications_failed_to_redrive_to_dlq_alarm: typing.Optional[typing.Union[SnsNumberOfNotificationsFailedToRedriveToDlqAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    config_number_of_notifications_filtered_out_invalid_attributes_alarm: typing.Optional[typing.Union[SnsNumberOfNotificationsFilteredOutInvalidAttributesAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    config_number_of_notifications_filtered_out_invalid_message_body_alarm: typing.Optional[typing.Union[SnsNumberOfNotificationsFilteredOutInvalidMessageBodyAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    config_number_of_notifications_redriven_to_dlq_alarm: typing.Optional[typing.Union[SnsNumberOfNotificationsRedrivenToDlqAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    default_alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    default_insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    default_ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    exclude_alarms: typing.Optional[typing.Sequence[SnsRecommendedAlarmsMetrics]] = None,
    exclude_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47c92495ab390db59ffeb1ec15eb639c4bda7f2e6fcc6ab00f48d384d9c0898d(
    node: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fecc7466425a3fd89d5693837b979038b44222e821924f36e33e1aea20e4236a(
    *,
    config_number_of_messages_published_alarm: typing.Union[SnsNumberOfMessagesPublishedAlarmConfig, typing.Dict[builtins.str, typing.Any]],
    config_number_of_notifications_delivered_alarm: typing.Union[SnsNumberOfNotificationsDeliveredAlarmConfig, typing.Dict[builtins.str, typing.Any]],
    config_number_of_notifications_failed_alarm: typing.Union[SnsNumberOfNotificationsFailedAlarmConfig, typing.Dict[builtins.str, typing.Any]],
    config_number_of_notifications_failed_to_redrive_to_dlq_alarm: typing.Optional[typing.Union[SnsNumberOfNotificationsFailedToRedriveToDlqAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    config_number_of_notifications_filtered_out_invalid_attributes_alarm: typing.Optional[typing.Union[SnsNumberOfNotificationsFilteredOutInvalidAttributesAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    config_number_of_notifications_filtered_out_invalid_message_body_alarm: typing.Optional[typing.Union[SnsNumberOfNotificationsFilteredOutInvalidMessageBodyAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    config_number_of_notifications_redriven_to_dlq_alarm: typing.Optional[typing.Union[SnsNumberOfNotificationsRedrivenToDlqAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    default_alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    default_insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    default_ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    exclude_alarms: typing.Optional[typing.Sequence[SnsRecommendedAlarmsMetrics]] = None,
    exclude_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__168fe991294b441d2405431f15f9275f6ff942b8e21e0e325a0459bc7773caf2(
    *,
    config_number_of_messages_published_alarm: typing.Union[SnsNumberOfMessagesPublishedAlarmConfig, typing.Dict[builtins.str, typing.Any]],
    config_number_of_notifications_delivered_alarm: typing.Union[SnsNumberOfNotificationsDeliveredAlarmConfig, typing.Dict[builtins.str, typing.Any]],
    config_number_of_notifications_failed_alarm: typing.Union[SnsNumberOfNotificationsFailedAlarmConfig, typing.Dict[builtins.str, typing.Any]],
    config_number_of_notifications_failed_to_redrive_to_dlq_alarm: typing.Optional[typing.Union[SnsNumberOfNotificationsFailedToRedriveToDlqAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    config_number_of_notifications_filtered_out_invalid_attributes_alarm: typing.Optional[typing.Union[SnsNumberOfNotificationsFilteredOutInvalidAttributesAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    config_number_of_notifications_filtered_out_invalid_message_body_alarm: typing.Optional[typing.Union[SnsNumberOfNotificationsFilteredOutInvalidMessageBodyAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    config_number_of_notifications_redriven_to_dlq_alarm: typing.Optional[typing.Union[SnsNumberOfNotificationsRedrivenToDlqAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    default_alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    default_insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    default_ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    exclude_alarms: typing.Optional[typing.Sequence[SnsRecommendedAlarmsMetrics]] = None,
    exclude_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    topic: _aws_cdk_aws_sns_ceddda9d.ITopic,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c20302d0dce277cc07fd49ad99fdc8325c29e5d392842004761577330967cdf9(
    *,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c269e40750c6097ce5a8155e6a89289661005b40532df53de2f6994ca311128c(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    queue: _aws_cdk_aws_sqs_ceddda9d.IQueue,
    threshold: jsii.Number,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aad26aa3cbe4aee8036df6b618af2e6ad6d3e4a19515aee9606ee50dd9af390(
    *,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    threshold: jsii.Number,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74ca6057ea5178302f3aef8ed4d21ecf4774c7eab9442af8f511543718ffcd83(
    *,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    threshold: jsii.Number,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    queue: _aws_cdk_aws_sqs_ceddda9d.IQueue,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8815dfd941d4ca8bcecc45ab9b5be4fc29cb8548dfe235cadc57ffe548606090(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    queue: _aws_cdk_aws_sqs_ceddda9d.IQueue,
    threshold: jsii.Number,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c35ed35809a4360f095271f551791be67f6ca04c5462fdaec844342d7ed06514(
    *,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    threshold: jsii.Number,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9376fa81f847d50cbcd5a89d6f568da884875f0f5dae5fa27c75a88325d354eb(
    *,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    threshold: jsii.Number,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    queue: _aws_cdk_aws_sqs_ceddda9d.IQueue,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a9188694cd82c03a9454a0975930ea6195f10816b6b12711ce2f5521c048ecc(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    queue: _aws_cdk_aws_sqs_ceddda9d.IQueue,
    threshold: jsii.Number,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9416ae2be0a787ae40fb821ebed1c680e9e73112ef095bf0b4590229ef4ce402(
    *,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    threshold: jsii.Number,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fb5bc4d73a65dccff1e81a21bd7c4c930f37e13143da72353844ec71b54e125(
    *,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    threshold: jsii.Number,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    queue: _aws_cdk_aws_sqs_ceddda9d.IQueue,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c83cc6f93b61287db8574d8fe0172a074b7e233a8e19487d23a436aadfc46237(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    queue: _aws_cdk_aws_sqs_ceddda9d.IQueue,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    threshold: typing.Optional[jsii.Number] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5a27b809a4469882ad8e6a5ad6df46efd97d656d0a63ccc9ef71906dc194139(
    *,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0793f6ef8158a82e9718505397a2f6f689150450cf683f7dc859408933d841e7(
    *,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    threshold: typing.Optional[jsii.Number] = None,
    queue: _aws_cdk_aws_sqs_ceddda9d.IQueue,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a37434be382ee9bdf1fa47a726cbedf3dab305255578301f29d8d0427d0ed9d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    queue: _aws_cdk_aws_sqs_ceddda9d.IQueue,
    config_approximate_age_of_oldest_message_alarm: typing.Union[SqsApproximateAgeOfOldestMessageAlarmConfig, typing.Dict[builtins.str, typing.Any]],
    config_approximate_number_of_messages_not_visible_alarm: typing.Union[SqsApproximateNumberOfMessagesNotVisibleAlarmConfig, typing.Dict[builtins.str, typing.Any]],
    config_approximate_number_of_messages_visible_alarm: typing.Union[SqsApproximateNumberOfMessagesVisibleAlarmConfig, typing.Dict[builtins.str, typing.Any]],
    config_number_of_messages_sent_alarm: typing.Optional[typing.Union[SqsNumberOfMessagesSentAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    default_alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    default_insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    default_ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    exclude_alarms: typing.Optional[typing.Sequence[SqsRecommendedAlarmsMetrics]] = None,
    exclude_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f45c71a79fad93ee92684dc7ebe5ea477b90eedb43380589ebe7c41ecb444281(
    node: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__407cc33cddff7246efd0e7d0b66c4c79e9d85a4263615880ce742c9bc4fc1820(
    *,
    config_approximate_age_of_oldest_message_alarm: typing.Union[SqsApproximateAgeOfOldestMessageAlarmConfig, typing.Dict[builtins.str, typing.Any]],
    config_approximate_number_of_messages_not_visible_alarm: typing.Union[SqsApproximateNumberOfMessagesNotVisibleAlarmConfig, typing.Dict[builtins.str, typing.Any]],
    config_approximate_number_of_messages_visible_alarm: typing.Union[SqsApproximateNumberOfMessagesVisibleAlarmConfig, typing.Dict[builtins.str, typing.Any]],
    config_number_of_messages_sent_alarm: typing.Optional[typing.Union[SqsNumberOfMessagesSentAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    default_alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    default_insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    default_ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    exclude_alarms: typing.Optional[typing.Sequence[SqsRecommendedAlarmsMetrics]] = None,
    exclude_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32e30f379dd47a0ddb371ae48cd5f2d74faa779b4377f94f691abc36732d99fc(
    *,
    config_approximate_age_of_oldest_message_alarm: typing.Union[SqsApproximateAgeOfOldestMessageAlarmConfig, typing.Dict[builtins.str, typing.Any]],
    config_approximate_number_of_messages_not_visible_alarm: typing.Union[SqsApproximateNumberOfMessagesNotVisibleAlarmConfig, typing.Dict[builtins.str, typing.Any]],
    config_approximate_number_of_messages_visible_alarm: typing.Union[SqsApproximateNumberOfMessagesVisibleAlarmConfig, typing.Dict[builtins.str, typing.Any]],
    config_number_of_messages_sent_alarm: typing.Optional[typing.Union[SqsNumberOfMessagesSentAlarmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    default_alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    default_insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    default_ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    exclude_alarms: typing.Optional[typing.Sequence[SqsRecommendedAlarmsMetrics]] = None,
    exclude_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    queue: _aws_cdk_aws_sqs_ceddda9d.IQueue,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70e505f14a1afa0f6a7236955dba568672dc67b4c2ceacb436fde882a2d66c49(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    content_based_deduplication: typing.Optional[builtins.bool] = None,
    display_name: typing.Optional[builtins.str] = None,
    enforce_ssl: typing.Optional[builtins.bool] = None,
    fifo: typing.Optional[builtins.bool] = None,
    logging_configs: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_sns_ceddda9d.LoggingConfig, typing.Dict[builtins.str, typing.Any]]]] = None,
    master_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    message_retention_period_in_days: typing.Optional[jsii.Number] = None,
    signature_version: typing.Optional[builtins.str] = None,
    topic_name: typing.Optional[builtins.str] = None,
    tracing_config: typing.Optional[_aws_cdk_aws_sns_ceddda9d.TracingConfig] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d45cfb8defe415c756707cf35150f504c3ca42a23dece0314de672338d762779(
    *,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    threshold: typing.Optional[jsii.Number] = None,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42ecd95425c9d23d522911d78398932e1d8493d1db2971c7b392f778fbcdb03f(
    *,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    threshold: typing.Optional[jsii.Number] = None,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1679196b0a9e5117c7a636cfb7f006fee301925d2a4605be64b230bdd8dd1a0a(
    *,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    threshold: typing.Optional[jsii.Number] = None,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1804ab3695bf52f69bd745c3d4ab5e213eb7fb6b4cc260c31532a53abb2b3d7f(
    *,
    alarm_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    insufficient_data_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    ok_action: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.IAlarmAction] = None,
    treat_missing_data: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.TreatMissingData] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    threshold: typing.Optional[jsii.Number] = None,
    alarm_description: typing.Optional[builtins.str] = None,
    alarm_name: typing.Optional[builtins.str] = None,
    bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
) -> None:
    """Type checking stubs"""
    pass
