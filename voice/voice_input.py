import speech_recognition as sr
from voice.voice_output import speak_text  # Assuming you have TTS

def get_voice_input(timeout=5, phrase_time_limit=8, confirm=False, export_audio=False):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening for input... (say something)")
        speak_text("Listening. Please speak now.")
        
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            text = recognizer.recognize_google(audio)
            text = text.strip().lower()
            print("✅ Recognized:", text)

            if export_audio:
                with open("voice_input.wav", "wb") as f:
                    f.write(audio.get_wav_data())
                print("📁 Saved voice input to voice_input.wav")

            if confirm:
                speak_text(f"You said: {text}. Is this correct?")
                # optionally add logic to confirm/redo

            return text

        except sr.WaitTimeoutError:
            print("⌛ Timeout: No speech detected.")
            return "[No input - timeout]"
        except sr.UnknownValueError:
            print("🤷 Could not understand the audio.")
            return "[Voice not understood]"
        except sr.RequestError as e:
            print(f"⚠️ Speech Recognition service error: {e}")
            return "[Speech service unavailable]"
