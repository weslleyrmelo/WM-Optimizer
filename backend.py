import os
import shutil
import subprocess

def limpar_pasta(caminho):
    apagados = 0
    if not caminho or not os.path.exists(caminho):
        return 0
        
    try:
        itens = os.listdir(caminho)
    except PermissionError:
        return 0

    for item in itens:
        item_path = os.path.join(caminho, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)
                apagados += 1
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                apagados += 1
        except Exception:
            pass
            
    return apagados

def executar_limpeza_geral(log_callback=None):
    local_app_data = os.environ.get("LOCALAPPDATA", "")
    
    alvos = [
        ("Windows Temp", r"C:\Windows\Temp"),
        ("Temp do Usuário (%TEMP%)", os.environ.get("TEMP")),
        ("Prefetch do Sistema", r"C:\Windows\Prefetch"),
        ("Cache Windows Update", r"C:\Windows\SoftwareDistribution\Download"),
        ("Relatórios de Erro (WER)", r"C:\ProgramData\Microsoft\Windows\WER\ReportArchive"),
        ("Fila de Erros (WER)", r"C:\ProgramData\Microsoft\Windows\WER\ReportQueue"),
        ("Cache DirectX (D3DSCache)", os.path.join(local_app_data, r"D3DSCache")),
        ("Cache Shaders NVIDIA (DX)", os.path.join(local_app_data, r"NVIDIA\DXCache")),
        ("Cache Shaders NVIDIA (GL)", os.path.join(local_app_data, r"NVIDIA\GLCache")),
    ]
    
    total_apagado = 0
    for nome, pasta in alvos:
        qtd = limpar_pasta(pasta)
        total_apagado += qtd
        if log_callback:
            log_callback(f"✔ {nome}: {qtd} itens removidos")
        
    subprocess.run(
        ["powershell", "-Command", "Clear-RecycleBin -Force -ErrorAction SilentlyContinue"],
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    if log_callback:
        log_callback("✔ Lixeira do Windows esvaziada")

    subprocess.run(
        ["ipconfig", "/flushdns"],
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    if log_callback:
        log_callback("✔ Cache de DNS limpo")
            
    return total_apagado

def ativar_desempenho_maximo():
    subprocess.run(
        ["powercfg", "-duplicatescheme", "e9a42b02-d5df-448d-aa00-03f14749eb61"],
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    resultado = subprocess.check_output(["powercfg", "/list"], text=True, creationflags=subprocess.CREATE_NO_WINDOW)
    for linha in resultado.splitlines():
        if "e9a42b02-d5df-448d-aa00-03f14749eb61" in linha or "Desempenho Máximo" in linha or "Ultimate Performance" in linha:
            guid = linha.split()[3]
            subprocess.run(["powercfg", "/setactive", guid], creationflags=subprocess.CREATE_NO_WINDOW)
            return True
    return False

def otimizar_windows_gamer(log_callback=None):
    etapas = [
        ("Serviço DiagTrack (Telemetria) desativado", [
            ["sc", "stop", "DiagTrack"],
            ["sc", "config", "DiagTrack", "start=", "disabled"],
        ]),
        ("Serviço dmwappushservice desativado", [
            ["sc", "stop", "dmwappushservice"],
            ["sc", "config", "dmwappushservice", "start=", "disabled"],
        ]),
        ("Coleta de dados bloqueada no Registro", [
            ["reg", "add", r"HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection", "/v", "AllowTelemetry", "/t", "REG_DWORD", "/d", "0", "/f"],
        ]),
        ("Xbox Game Bar / GameDVR em 2º plano desativado", [
            ["reg", "add", r"HKCU\System\GameConfigStore", "/v", "GameDVR_Enabled", "/t", "REG_DWORD", "/d", "0", "/f"],
            ["reg", "add", r"HKLM\SOFTWARE\Policies\Microsoft\Windows\GameDVR", "/v", "AllowGameDVR", "/t", "REG_DWORD", "/d", "0", "/f"],
        ]),
        ("Prioridade de GPU e Jogos ajustada (MMCSS)", [
            ["reg", "add", r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile", "/v", "SystemResponsiveness", "/t", "REG_DWORD", "/d", "0", "/f"],
            ["reg", "add", r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games", "/v", "GPU Priority", "/t", "REG_DWORD", "/d", "8", "/f"],
            ["reg", "add", r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games", "/v", "Priority", "/t", "REG_DWORD", "/d", "6", "/f"],
        ]),
    ]
    
    for descricao, comandos in etapas:
        for cmd in comandos:
            subprocess.run(cmd, creationflags=subprocess.CREATE_NO_WINDOW)
        if log_callback:
            log_callback(f"✔ {descricao}")
        
    energia_ok = ativar_desempenho_maximo()
    if log_callback:
        if energia_ok:
            log_callback("✔ Plano de Energia: Desempenho Máximo ativado")
        else:
            log_callback("⚠ Plano de Energia: Verifique manualmente no Painel")
    return energia_ok

def restaurar_padrao_windows(log_callback=None):
    etapas = [
        ("Serviços de Telemetria reativados", [
            ["sc", "config", "DiagTrack", "start=", "auto"],
            ["sc", "start", "DiagTrack"],
            ["sc", "config", "dmwappushservice", "start=", "demand"],
            ["reg", "delete", r"HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection", "/v", "AllowTelemetry", "/f"],
        ]),
        ("Xbox Game Bar / GameDVR reativados", [
            ["reg", "add", r"HKCU\System\GameConfigStore", "/v", "GameDVR_Enabled", "/t", "REG_DWORD", "/d", "1", "/f"],
            ["reg", "delete", r"HKLM\SOFTWARE\Policies\Microsoft\Windows\GameDVR", "/v", "AllowGameDVR", "/f"],
        ]),
        ("Prioridades do sistema restauradas ao padrão", [
            ["reg", "add", r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile", "/v", "SystemResponsiveness", "/t", "REG_DWORD", "/d", "20", "/f"],
            ["reg", "add", r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games", "/v", "GPU Priority", "/t", "REG_DWORD", "/d", "2", "/f"],
            ["reg", "add", r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games", "/v", "Priority", "/t", "REG_DWORD", "/d", "2", "/f"],
        ]),
        ("Plano de Energia restaurado para Equilibrado", [
            ["powercfg", "/setactive", "381b4222-f694-41f0-9685-ff5bb260df2e"],
        ]),
    ]
    
    for descricao, comandos in etapas:
        for cmd in comandos:
            subprocess.run(cmd, creationflags=subprocess.CREATE_NO_WINDOW)
        if log_callback:
            log_callback(f"↩ {descricao}")
        
    return True