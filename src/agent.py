import os
import json
from openai import OpenAI  # DeepSeek usa el mismo cliente
from src.scanner import AbletonScanner
from src.ableton_driver import AbletonDriver
from src.config import Config
from dotenv import load_dotenv

load_dotenv()

class AbletonAgent:
    def __init__(self):
        
        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url=os.getenv("DEEPSEEK_BASE_URL"),
        )
        self.scanner = AbletonScanner()
        self.driver = AbletonDriver()

    def execute(self, user_prompt: str):
        try:
            snapshot = self.scanner.scan()
            
            # Prompt optimizado para modelos locales
            system_prompt = f"""
            You are an Ableton Live controller. Current session: {json.dumps(snapshot)}
            Respond ONLY with a JSON object following this exact schema:
            {{
              "thought": "Brief explanation of the action",
              "commands": [
                {{
                  "action": "set_volume",
                  "track_id": integer,
                  "value": number (0.0-1.0 for volume)
                }}
              ]
            }}
            Example response for "Baja el volumen del BASS a la mitad":
            {{
              "thought": "Bajando el volumen del track BASS al 50%",
              "commands": [
                {{
                  "action": "set_volume",
                  "track_id": 3,
                  "value": 0.5
                }}
              ]
            }}
            """
        except Exception as e:
            print(f"✗ Error al escanear estado de Ableton: {str(e)}")
            return {"error": "unable_to_connect", "message": str(e)}

        response = self.client.chat.completions.create(
            model="llama3.2:3b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={'type': 'json_object'}
        )

        result = json.loads(response.choices[0].message.content)
        
        # Validar estructura de respuesta
        if not isinstance(result, dict):
            print("✗ Error: Respuesta del modelo no es un diccionario")
            return {"error": "invalid_model_response", "message": "Respuesta no es un diccionario"}
            
        thought = result.get("thought", "Sin pensamiento")
        commands = result.get("commands", [])
        
        print(f"\n> IA Pensando: {thought}")
        
        # Validar y ejecutar comandos
        if not isinstance(commands, list):
            print("✗ Error: Comandos no son una lista")
            return {"error": "invalid_commands", "message": "Comandos no son una lista"}
            
        for cmd in commands:
            if not isinstance(cmd, dict):
                print("✗ Error: Comando no es un diccionario")
                continue
                
            action = cmd.get("action")
            if action == "set_volume":
                try:
                    track_id = int(cmd["track_id"])
                    value = float(cmd["value"])
                    self.driver.set_track_volume(track_id, value)
                except (KeyError, TypeError) as e:
                    print(f"✗ Error en comando set_volume: {str(e)}")
            elif action == "fire_clip":
                try:
                    track_id = int(cmd["track_id"])
                    clip_id = int(cmd["clip_id"])
                    self.driver.fire_clip(track_id, clip_id)
                except (KeyError, TypeError) as e:
                    print(f"✗ Error en comando fire_clip: {str(e)}")
            else:
                print(f"✗ Acción desconocida: {action}")
        
        return {"thought": thought, "commands_executed": len(commands)}

if __name__ == "__main__":
    agent = AbletonAgent()
    prompt = input("¿Qué quieres hacer en Ableton? (ej: 'Baja el volumen del BASS a la mitad'): ")
    agent.execute(prompt)
