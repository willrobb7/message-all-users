# message-all-users

## To use:
1) Define a variable called 'Message'
2) Put all the emails you want to message into the 'lll' variable. ( In CSV Form )
3) Assume role into AWS IT Dev
4) Run command `AWS_PROFILE=sts sls deploy`
5) Hit the Test button on the Lambda dashboard.
6) If the logs show that the lambda "Should be messaging" all the users in your 'lll' list
  - Uncomment line 142 and repeat stage 4 and 5, this will send your message to all the users on your list.
