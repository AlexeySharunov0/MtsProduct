#!/bin/sh
# Создание JSON-объекта для allure-notifications.
# Значения берутся из переменных окружения, секреты в репозитории не хранятся.
JSON_OBJECT="{\
    \"base\": {\
        \"logo\": \"notifications/logo.png\",\
        \"project\": \"PPInfo\",\
        \"environment\": \"\",\
        \"comment\": \"PPInfo monitoring\",\
        \"reportLink\": \"${ALLURE_REPORT_URL}\",\
        \"language\": \"ru\",\
        \"allureFolder\": \"allure-report\",\
        \"enableChart\": true\
    },\
    \"telegram\": {\
        \"token\": \"$TELEGRAM_TOKEN\",\
        \"chat\": \"$TELEGRAM_CHAT\",\
        \"replyTo\": \"\"\
    },\
    \"proxy\": {\
        \"host\": \"$PROXY_HOST\",\
        \"port\": ${PROXY_PORT:-3128},\
        \"username\": \"$PROXY_USERNAME\",\
        \"password\": \"$PROXY_PASSWORD\"\
    }\
}\
"

echo $JSON_OBJECT > ./notifications/telegram.json
