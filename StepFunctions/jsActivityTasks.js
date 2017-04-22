var AWS = require('aws-sdk');
AWS.config.update({ region: 'us-east-1' });
var stepfunctions = new AWS.StepFunctions();

var params = {
    activityArn: 'arn:aws:states:us-east-1:620428855768:activity:get-greeting',
    workerName: 'nodeworker'
};

stepfunctions.getActivityTask(params, function (err, data, myfunction) {
    if (err) {
        console.log(err, err.stack); // an error occurred
    } else {
        function myfunction(input) {
            console.log(input);
            return '{ "foo": "bar" }';
        }
        output = myfunction(data.input);
        var outputParams = {
            output: output,
            taskToken: data.taskToken
        };
        stepfunctions.sendTaskSuccess(outputParams, function (err, data) {
            if (err) console.log(err, err.stack); // an error occurred
            else console.log(data);           // successful response
        });
    }
});

