# Deploy to AWS (App Runner + DynamoDB + Bedrock)

> Status: files written but **not yet deployed/tested** — no AWS account was available when they were authored.
> Record every snag in `docs/friction_log.csv` (judging bonus).

1. Enable Bedrock model access for the model in `HOMEPILOT_MODEL_ID` in your region.
2. Build & push: `aws ecr create-repository --repository-name homepilot`, then `docker build -t <acct>.dkr.ecr.<region>.amazonaws.com/homepilot:latest .` and `docker push` it.
3. `aws cloudformation deploy --template-file infra/template.yaml --stack-name homepilot --capabilities CAPABILITY_IAM --parameter-overrides ImageUri=<image>`
4. Open the `Url` output. `/api/health` should report `"agent":"bedrock"`.
5. Logs (tool name, latency, status, trace_id) appear in CloudWatch Logs for the App Runner service.
6. Tear down after judging: `aws cloudformation delete-stack --stack-name homepilot` (cost control).

Notes: the container runs the MCP server on loopback and the API on `$PORT`; the DynamoDB table is selected via `HOMEPILOT_DDB_TABLE`.
The public demo URL is open to anyone and only holds the synthetic household. Put it behind Cognito before using real data.
