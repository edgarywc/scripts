import boto3

def get_codebuild_logs(build_id, search_term="AccessDeniedException"):
    """
    Busca logs de um build específico do AWS CodeBuild e procura por um termo.
    """
    client = boto3.client("codebuild")
    logs_client = boto3.client("logs")

    # Pega informações do build
    build_info = client.batch_get_builds(ids=[build_id])["builds"][0]
    log_info = build_info["logs"]

    group_name = log_info["groupName"]
    stream_name = log_info["streamName"]

    # Busca eventos do CloudWatch Logs
    next_token = None
    found_lines = []

    while True:
        kwargs = {
            "logGroupName": group_name,
            "logStreamName": stream_name,
            "limit": 10000
        }
        if next_token:
            kwargs["nextToken"] = next_token

        response = logs_client.get_log_events(**kwargs)

        for event in response["events"]:
            message = event["message"]
            if search_term in message:
                found_lines.append(message.strip())

        next_token = response.get("nextForwardToken")
        if not response["events"] or not next_token:
            break

    return found_lines


if __name__ == "__main__":
    # Exemplo de uso: substitua pelo ID do build
    build_id = "codebuild-exemplo:12345678-aaaa-bbbb-cccc-1234567890ab"
    erros = get_codebuild_logs(build_id)

    if erros:
        print("⚠️ Erros encontrados:")
        for e in erros:
            print(e)
    else:
        print("✅ Nenhum AccessDeniedException encontrado.")
