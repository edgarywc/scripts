@echo off
setlocal enabledelayedexpansion

REM Config AWS credentials aqui ou exporte antes
set AWS_ACCESS_KEY_ID=SEU_ACCESS_KEY
set AWS_SECRET_ACCESS_KEY=SUA_SECRET_KEY
set AWS_DEFAULT_REGION=us-east-1

set LOGFILE=resultado_testes.log
echo ====== Resultados dos Testes de SCP ====== > %LOGFILE%
echo. >> %LOGFILE%

REM Função auxiliar para rodar teste
REM %1 = Numero do teste
REM %2 = Descrição
REM %3 = Tags usadas (passadas no -var)
REM %4 = Esperado (OK ou BLOQUEIO)
call :runtest 1 "Criar sem nenhuma tag" "{}" "OK"
call :runtest 2 "Criar com Restrita" "{Restrita='true'}" "BLOQUEIO"
call :runtest 3 "Criar com Puppet" "{Puppet='enabled'}" "OK"
call :runtest 4 "Criar com Restrita + Puppet" "{Restrita='true', Puppet='enabled'}" "OK"

REM Testes de update precisam de mais de um apply
call :runtest_update 5 "Criar com Puppet e depois adicionar Restrita" "{Puppet='enabled'}" "{Puppet='enabled', Restrita='true'}" "OK"
call :runtest_update 6 "Criar sem tag e depois adicionar Restrita" "{}" "{Restrita='true'}" "BLOQUEIO"
call :runtest_update 7 "Criar sem tag e depois adicionar Puppet" "{}" "{Puppet='enabled'}" "OK"
call :runtest_update 8 "Criar sem tag, adicionar Puppet e depois Restrita" "{}" "{Puppet='enabled'}" "{Puppet='enabled', Restrita='true'}" "OK"

echo. >> %LOGFILE%
echo ====== Testes finalizados ====== >> %LOGFILE%
echo Resultados salvos em %LOGFILE%
goto :eof


:runtest
    echo ======================================
    echo Teste %1: %2 (esperado: %4)
    echo ======================================
    terraform apply -auto-approve -var "tags=%~3" >nul 2>&1
    if %errorlevel%==0 (
        set RESULT=OK
    ) else (
        set RESULT=BLOQUEIO
    )
    echo Teste %1: %2 - Resultado: !RESULT! | Esperado: %4 >> %LOGFILE%
    terraform destroy -auto-approve >nul 2>&1
    goto :eof

:runtest_update
    echo ======================================
    echo Teste %1: %2 (esperado: %5)
    echo ======================================
    terraform apply -auto-approve -var "tags=%~3" >nul 2>&1
    terraform apply -auto-approve -var "tags=%~4" >nul 2>&1

    REM se tiver um 3º step (caso 8)
    if not "%~5"=="" (
        terraform apply -auto-approve -var "tags=%~5" >nul 2>&1
    )

    if %errorlevel%==0 (
        set RESULT=OK
    ) else (
        set RESULT=BLOQUEIO
    )
    echo Teste %1: %2 - Resultado: !RESULT! | Esperado: %~5 >> %LOGFILE%
    terraform destroy -auto-approve >nul 2>&1
    goto :eof
