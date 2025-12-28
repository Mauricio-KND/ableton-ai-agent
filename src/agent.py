import os
import json
from openai import OpenAI  # DeepSeek usa el mismo cliente
from scanner import AbletonScanner
from ableton_driver import AbletonDriver
from config import Config
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
        snapshot = self.scanner.scan()
        
        # Prompt directivo para modelos locales
        system_prompt = f"""
        You are an Ableton Live controller. Current session: {json.dumps(snapshot)}
        Respond ONLY with a JSON object.
        Example: {{"thought": "lowering bass", "commands": [{{"action": "set_volume", "track_id": 3, "value": 0.5}}]}}
        """

        response = self.client.chat.completions.create(
            model="llama3.2:3b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={'type': 'json_object'}
        )

        result = json.loads(response.choices[0].message.content)
        print(f"\n> IA Pensando: {result['thought']}")
        
        for cmd in result.get("commands", []):
            if cmd["action"] == "set_volume":
                self.driver.set_track_volume(cmd["track_id"], cmd["value"])
            elif cmd["action"] == "fire_clip":
                self.driver.fire_clip(cmd["track_id"], cmd["clip_id"])
        
        return result

if __name__ == "__main__":
    agent = AbletonAgent()
    prompt = input("¿Qué quieres hacer en Ableton? (ej: 'Baja el volumen del BASS a la mitad'): ")
    agent.execute(prompt)