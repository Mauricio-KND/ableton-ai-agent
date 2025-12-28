from src.ableton_driver import AbletonDriver

def test_osc_connection():
    driver = AbletonDriver()
    print("Intentando conectar con Ableton Live...")
    
    try:
        # Probar un comando de volumen directamente
        track_id = 0
        value = 0.5
        driver.set_track_volume(track_id, value)
        print(f"✓ Comando de volumen enviado al track {track_id} con valor {value}")

        # Probar disparo de clip
        clip_track = 0
        clip_slot = 0
        driver.fire_clip(clip_track, clip_slot)
        print(f"✓ Disparado clip en track {clip_track}, slot {clip_slot}")
        
        return True
    except Exception as e:
        print(f"✗ Error en la conexión OSC: {str(e)}")
        return False

if __name__ == "__main__":
    test_osc_connection()
