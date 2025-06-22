import os
from gtts import gTTS
import subprocess
import platform

def text_to_speech_with_gtts_old(input_text, output_filepath):
    language="en"

    audioobj= gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)


def text_to_speech_with_gtts(input_text, output_filepath):
    language="en"

    audioobj= gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":  # Windows
            # Use Windows Media Player for MP3 support
            subprocess.run(['powershell', '-c', f'Add-Type -AssemblyName presentationCore; $mediaPlayer = New-Object system.windows.media.mediaplayer; $mediaPlayer.open([uri]::new((Resolve-Path "{output_filepath}").Path)); $mediaPlayer.Play(); Start-Sleep 5'])
            # Alternative: Use built-in start command
            # subprocess.run(['start', '/wait', output_filepath], shell=True)
        elif os_name == "Linux":  # Linux
            # Try different players in order of preference
            players = ['mpg123', 'ffplay', 'aplay']
            for player in players:
                try:
                    subprocess.run([player, output_filepath], check=True)
                    break
                except (subprocess.CalledProcessError, FileNotFoundError):
                    continue
            else:
                raise OSError("No suitable audio player found")
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")


# Step1b: Setup Text to Speech–TTS–model with ElevenLabs
try:
    from elevenlabs.client import ElevenLabs
    ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
    
    def text_to_speech_with_elevenlabs_old(input_text, output_filepath):
        if not ELEVENLABS_API_KEY:
            print("ElevenLabs API key not found in environment variables")
            return
            
        client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        audio = client.text_to_speech.convert(
            text=input_text,
            voice_id="JBFqnCBsd6RMkjVDRZzb",  # Using a specific voice ID
            model_id="eleven_turbo_v2_5",
            output_format="mp3_44100_128"
        )
        
        # Save the audio to file
        with open(output_filepath, "wb") as f:
            for chunk in audio:
                f.write(chunk)
        
        os_name = platform.system()
        try:
            if os_name == "Darwin":  # macOS
                subprocess.run(['afplay', output_filepath])
            elif os_name == "Windows":  # Windows
                # Use Windows Media Player for MP3 support
                subprocess.run(['powershell', '-c', f'Add-Type -AssemblyName presentationCore; $mediaPlayer = New-Object system.windows.media.mediaplayer; $mediaPlayer.open([uri]::new((Resolve-Path "{output_filepath}").Path)); $mediaPlayer.Play(); Start-Sleep 5'])
            elif os_name == "Linux":  # Linux
                players = ['mpg123', 'ffplay', 'aplay']
                for player in players:
                    try:
                        subprocess.run([player, output_filepath], check=True)
                        break
                    except (subprocess.CalledProcessError, FileNotFoundError):
                        continue
                else:
                    raise OSError("No suitable audio player found")
            else:
                raise OSError("Unsupported operating system")
        except Exception as e:
            print(f"An error occurred while trying to play the audio: {e}")

    def text_to_speech_with_elevenlabs(input_text, output_filepath):
        if not ELEVENLABS_API_KEY:
            print("ElevenLabs API key not found in environment variables")
            return
            
        client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        audio = client.text_to_speech.convert(
            text=input_text,
            voice_id="JBFqnCBsd6RMkjVDRZzb",  # Using a specific voice ID
            model_id="eleven_turbo_v2_5",
            output_format="mp3_44100_128"
        )
        
        # Save the audio to file
        with open(output_filepath, "wb") as f:
            for chunk in audio:
                f.write(chunk)
        
        os_name = platform.system()
        try:
            if os_name == "Darwin":  # macOS
                subprocess.run(['afplay', output_filepath])
            elif os_name == "Windows":  # Windows
                # Use Windows Media Player for MP3 support
                subprocess.run(['powershell', '-c', f'Add-Type -AssemblyName presentationCore; $mediaPlayer = New-Object system.windows.media.mediaplayer; $mediaPlayer.open([uri]::new((Resolve-Path "{output_filepath}").Path)); $mediaPlayer.Play(); Start-Sleep 5'])
            elif os_name == "Linux":  # Linux
                players = ['mpg123', 'ffplay', 'aplay']
                for player in players:
                    try:
                        subprocess.run([player, output_filepath], check=True)
                        break
                    except (subprocess.CalledProcessError, FileNotFoundError):
                        continue
                else:
                    raise OSError("No suitable audio player found")
            else:
                raise OSError("Unsupported operating system")
        except Exception as e:
            print(f"An error occurred while trying to play the audio: {e}")

except ImportError as e:
    print(f"ElevenLabs library import error: {e}")
    print("Try: pip install elevenlabs --upgrade")
    def text_to_speech_with_elevenlabs_old(input_text, output_filepath):
        print("ElevenLabs not available")
    def text_to_speech_with_elevenlabs(input_text, output_filepath):
        print("ElevenLabs not available")


# Test the functions
if __name__ == "__main__":
    input_text = "Hi this is Ai with Hassan!"
    
    # Test gTTS without autoplay
    text_to_speech_with_gtts_old(input_text=input_text, output_filepath="gtts_testing.mp3")
    print("gTTS file saved successfully")
    
    # Test gTTS with autoplay
    input_text_autoplay = "Hi this is Ai with Hassan, autoplay testing!"
    text_to_speech_with_gtts(input_text=input_text_autoplay, output_filepath="gtts_testing_autoplay.mp3")
    
    # # Test ElevenLabs with autoplay (if API key is available)
    text_to_speech_with_elevenlabs(input_text_autoplay, output_filepath="elevenlabs_testing_autoplay.mp3")