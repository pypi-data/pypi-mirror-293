import subprocess
import pyautogui
import asyncio
import os
from rich.console import Console
from worker_automate_hub.utils.logger import logger
import time
import pygetwindow as gw

console = Console()

def tirar_screenshot(nome_etapa):
    caminho_screenshot = f"{nome_etapa}_{int(time.time())}.png"
    pyautogui.screenshot(caminho_screenshot)
    console.print(f"Screenshot tirada: {caminho_screenshot}")
    return caminho_screenshot

def deletar_screenshots(caminhos_screenshots):
    for caminho in caminhos_screenshots:
        try:
            os.remove(caminho)
            console.print(f"Screenshot deletada: {caminho}")
        except OSError as e:
            console.print(f"Erro ao deletar screenshot {caminho}: {e}")

def fechar_janela_existente(ip):
    try:
        janelas_encontradas = gw.getAllTitles()
        for titulo in janelas_encontradas:
            if ip in titulo:
                janela = gw.getWindowsWithTitle(titulo)[0]
                console.print(f"Fechando janela existente: {titulo}")
                janela.activate()

                # Tentar fechar a janela usando Alt+F4
                pyautogui.hotkey('alt', 'f4')
                pyautogui.press('enter')
                time.sleep(2)
                
                # Verificar se a janela foi fechada
                if titulo in gw.getAllTitles():
                    console.print(f"Falha ao fechar a janela: {titulo}")
                    for _ in range(len(janelas_encontradas)):
                        pyautogui.hotkey('alt', 'tab')
                        time.sleep(1)
                        if gw.getActiveWindowTitle() == titulo:
                            x, y = janela.center
                            pyautogui.click(x, y)
                            pyautogui.hotkey('alt', 'f4')
                            pyautogui.press('enter')
                            time.sleep(2)
                            break
                
                    if titulo in gw.getAllTitles():
                        console.print(f"Falha repetida ao fechar a janela: {titulo}")
                    else:
                        console.print(f"Janela fechada com sucesso após Alt+Tab: {titulo}")
                else:
                    console.print(f"Janela fechada com sucesso: {titulo}")

                time.sleep(2)
                break
        else:
            console.print(f"Nenhuma janela encontrada com o IP: {ip}")
    
    except Exception as e:
        console.print(f"Erro ao tentar fechar a janela: {e}", style="bold red")

def restaurar_janelas_rdp():
    janelas_rdp = [win for win in gw.getAllTitles() if "Conexão de Área de Trabalho Remota" in win or "Remote Desktop Connection" in win]
    
    for titulo in janelas_rdp:
        janela = gw.getWindowsWithTitle(titulo)[0]
        console.print(f"Processando janela: {titulo}")
        if janela.isMinimized:
            janela.restore()
            console.print(f"Janela restaurada: {titulo}")
        else:
            console.print(f"Janela já está aberta: {titulo}")
        janela.activate()
        time.sleep(2)

def redimensionar_janela_rdp(largura, altura):
    janelas_rdp = [win for win in gw.getAllTitles() if "Conexão de Área de Trabalho Remota" in win or "Remote Desktop Connection" in win]
    
    if janelas_rdp:
        janela_rdp = gw.getWindowsWithTitle(janelas_rdp[0])[0]
        janela_rdp.resizeTo(largura, altura)
        janela_rdp.moveTo(0, 0)
        console.print(f"Janela redimensionada para {largura}x{altura}.")
        janela_rdp.activate()
        time.sleep(1)
    else:
        console.print("Não foi possível encontrar a janela RDP para redimensionar.")

async def conexao_rdp(task):
    caminhos_screenshots = []
    try:
        ip = task["configEntrada"].get("ip", "")
        user = task["configEntrada"].get("user", "")
        password = task["configEntrada"].get("password", "")

        # Minimizar todas as janelas antes de iniciar a conexão
        pyautogui.hotkey('win', 'd')
        console.print("1 - Minimizando todas as telas...")
        await asyncio.sleep(2)

        # Fechar janelas existentes que possam interferir
        fechar_janela_existente(ip)

        # Abrir o Remote Desktop Connection
        subprocess.Popen('mstsc')
        console.print("2 - Abrindo conexão de trabalho remota...")
        await asyncio.sleep(2)

        # Redimensionar a janela RDP para garantir que está visível
        redimensionar_janela_rdp(800, 600)

        # Inserir o endereço IP
        caminhos_screenshots.append(tirar_screenshot("antes_de_inserir_ip"))
        console.print("3 - Inserindo o IP...")
        pyautogui.write(ip)
        await asyncio.sleep(2)
        caminhos_screenshots.append(tirar_screenshot("depois_de_inserir_ip"))

        # Inserir o usuário
        pyautogui.press('tab')
        await asyncio.sleep(2)
        console.print("4 - Inserindo o Usuario...")
        pyautogui.write(user)
        pyautogui.press('enter')
        await asyncio.sleep(5)
        caminhos_screenshots.append(tirar_screenshot("depois_de_inserir_usuario"))

        # Inserir a senha
        console.print("5 - Inserindo a Senha...")
        pyautogui.write(password)
        pyautogui.press('enter')
        await asyncio.sleep(10)
        caminhos_screenshots.append(tirar_screenshot("depois_de_inserir_senha"))

        # Lidar com o pop-up de certificado
        console.print("6 - Apertando left...")
        pyautogui.press('left')
        await asyncio.sleep(2)
        console.print("7 - Apertando Enter...")
        pyautogui.press('enter')
        await asyncio.sleep(20)
        caminhos_screenshots.append(tirar_screenshot("depois_do_certificado"))

        # Minimizar todas as janelas e restaurar a RDP para foreground
        console.print("8 - Minimizando todas as telas no final...")
        pyautogui.hotkey('win', 'd')
        await asyncio.sleep(2)
        caminhos_screenshots.append(tirar_screenshot("depois_de_minimizar_todas"))

        # Restaurar janelas RDP se necessário
        restaurar_janelas_rdp()
        caminhos_screenshots.append(tirar_screenshot("depois_de_restaurar_janelas"))

        # Deletar as screenshots após finalizar o processo
        deletar_screenshots(caminhos_screenshots)

        return {"sucesso": True, "retorno": "Processo de conexão ao RDP executado com sucesso."}

    except Exception as ex:
        err_msg = f"Erro ao executar conexao_rdp: {ex}"
        logger.error(err_msg)
        console.print(err_msg, style="bold red")
        caminhos_screenshots.append(tirar_screenshot("erro"))
        deletar_screenshots(caminhos_screenshots)
        return {"sucesso": False, "retorno": err_msg}
