import os
import gradio as gr
from brain import encode_image, analyze_image_with_query
from voice import record_audio, transcribe_with_groq
from doc_voice import text_to_speech_with_gtts, text_to_speech_with_elevenlabs

# Enhanced TTS function with language support
def text_to_speech_multilingual(input_text, output_filepath, language='en', use_elevenlabs=False):
    """
    Enhanced text-to-speech with Hindi and Marathi support
    
    Args:
        input_text: Text to convert to speech
        output_filepath: Path to save audio file
        language: Language code ('en', 'hi', 'mr')
        use_elevenlabs: Whether to use ElevenLabs (True) or gTTS (False)
    """
    if use_elevenlabs:
        # ElevenLabs supports multilingual voices but requires specific voice IDs
        # You'll need to find Hindi/Marathi voice IDs from ElevenLabs
        return text_to_speech_with_elevenlabs(input_text, output_filepath)
    else:
        # Use gTTS with language support
        from gtts import gTTS
        import subprocess
        import platform
        
        # Language mapping
        lang_codes = {
            'english': 'en',
            'hindi': 'hi', 
            'marathi': 'mr'
        }
        
        lang_code = lang_codes.get(language, 'en')
        
        try:
            audioobj = gTTS(
                text=input_text,
                lang=lang_code,
                slow=False
            )
            audioobj.save(output_filepath)
            
            # Auto-play the audio (same as your existing code)
            os_name = platform.system()
            if os_name == "Darwin":  # macOS
                subprocess.run(['afplay', output_filepath])
            elif os_name == "Windows":  # Windows
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
                    
        except Exception as e:
            print(f"Error in multilingual TTS: {e}")
            return None

# Enhanced system prompts for different languages
system_prompts = {
    'english': """You have to act as a professional doctor, i know you are not but this is for learning purpose.
             What's in this image?. Do you find anything wrong with it medically?
             If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in
             your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Donot say 'In the image I see' but say 'With what I see, I think you have ....'
            Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot,
             Keep your answer concise (max 2 sentences). No preamble, start your answer right away please""",
    
    'hindi': """आपको एक पेशेवर डॉक्टर की तरह काम करना है, मुझे पता है कि आप नहीं हैं लेकिन यह सीखने के उद्देश्य से है।
             इस तस्वीर में क्या है? क्या आपको इसमें चिकित्सा की दृष्टि से कुछ गलत लगता है?
             यदि आप कोई निदान करते हैं, तो उसके लिए कुछ उपचार सुझाएं। अपने उत्तर में कोई संख्या या विशेष वर्ण न जोड़ें।
             आपका उत्तर एक लंबे पैराग्राफ में होना चाहिए। हमेशा ऐसे उत्तर दें जैसे आप किसी वास्तविक व्यक्ति को जवाब दे रहे हों।
             'तस्वीर में मुझे दिखता है' न कहें बल्कि 'जो मुझे दिखता है, मुझे लगता है कि आपको... है'
             AI मॉडल की तरह मार्कडाउन में जवाब न दें, आपका उत्तर वास्तविक डॉक्टर का होना चाहिए न कि AI बॉट का।
             अपना उत्तर संक्षिप्त रखें (अधिकतम 2 वाक्य)। कोई प्रस्तावना नहीं, अपना उत्तर तुरंत शुरू करें। हिंदी में उत्तर दें।""",
    
    'marathi': """तुम्हाला एक व्यावसायिक डॉक्टर म्हणून काम करावे लागेल, मला माहित आहे की तुम्ही नाही पण हे शिकण्याच्या उद्देशाने आहे।
             या चित्रात काय आहे? तुम्हाला यात वैद्यकीय दृष्टीने काही चुकीचं वाटतं का?
             जर तुम्ही निदान करता तर त्यासाठी काही उपचार सुचवा. तुमच्या उत्तरात कोणतेही संख्या किंवा विशेष वर्ण जोडू नका.
             तुमचे उत्तर एका लांब परिच्छेदात असावे. नेहमी असे उत्तर द्या जसे तुम्ही खऱ्या व्यक्तीला उत्तर देत आहात.
             'चित्रात मला दिसतं' असं म्हणू नका तर 'जे मला दिसतं त्यावरून मला वाटतं तुम्हाला... आहे'
             AI मॉडेल सारखं मार्कडाउनमध्ये उत्तर देऊ नका, तुमचं उत्तर खऱ्या डॉक्टरासारखं असावं.
             तुमचं उत्तर थोडक्यात ठेवा (जास्तीत जास्त 2 वाक्य). कोणतीही प्रस्तावना नाही, लगेच उत्तर सुरू करा. मराठीत उत्तर द्या."""
}

def process_inputs(recorded_audio, uploaded_audio, text_input, image_filepath, language_choice, voice_service):
    """
    Process inputs from multiple sources: recorded audio, uploaded audio, or text input
    """
    try:
        user_query = ""
        
        # Priority order: text input > recorded audio > uploaded audio
        if text_input and text_input.strip():
            # Use text input directly
            user_query = text_input.strip()
            speech_to_text_output = f"Text input: {user_query}"
        elif recorded_audio:
            # Use recorded audio
            speech_to_text_output = transcribe_with_groq(
                GROQ_API_KEY=os.environ.get("GROQ_API_KEY"),
                audio_filepath=recorded_audio,
                stt_model="whisper-large-v3"
            )
            user_query = speech_to_text_output
        elif uploaded_audio:
            # Use uploaded audio file
            speech_to_text_output = transcribe_with_groq(
                GROQ_API_KEY=os.environ.get("GROQ_API_KEY"),
                audio_filepath=uploaded_audio,
                stt_model="whisper-large-v3"
            )
            user_query = speech_to_text_output
        else:
            # No input provided
            no_input_messages = {
                'english': "Please provide a question via text, recorded audio, or uploaded audio file.",
                'hindi': "कृपया टेक्स्ट, रिकॉर्ड की गई ऑडियो, या अपलोड की गई ऑडियो फ़ाइल के द्वारा प्रश्न दें।",
                'marathi': "कृपया मजकूर, रेकॉर्ड केलेला ऑडिओ किंवा अपलोड केलेल्या ऑडिओ फाइलद्वारे प्रश्न द्या."
            }
            error_msg = no_input_messages.get(language_choice.lower(), no_input_messages['english'])
            return error_msg, error_msg, None
        
        # Get appropriate system prompt based on language
        system_prompt = system_prompts.get(language_choice.lower(), system_prompts['english'])
        
        # Handle the image input
        if image_filepath:
            doctor_response = analyze_image_with_query(
                query=system_prompt + " " + user_query, 
                encoded_image=encode_image(image_filepath), 
                model="meta-llama/llama-4-scout-17b-16e-instruct"
            )
        else:
            # Provide language-appropriate "no image" message
            no_image_messages = {
                'english': "No image provided for me to analyze. Please describe your symptoms or upload a medical image.",
                'hindi': "विश्लेषण के लिए कोई छवि प्रदान नहीं की गई। कृपया अपने लक्षणों का वर्णन करें या चिकित्सा छवि अपलोड करें।",
                'marathi': "विश्लेषणासाठी कोणतीही प्रतिमा दिली नाही. कृपया तुमच्या लक्षणांचे वर्णन करा किंवा वैद्यकीय प्रतिमा अपलोड करा."
            }
            
            # If there's a user query but no image, try to respond to the text query
            if user_query:
                # Create a text-only medical consultation prompt
                text_only_prompts = {
                    'english': f"As a doctor, based on the symptoms or question: '{user_query}', provide a brief medical consultation response. Keep it concise and suggest seeing a healthcare professional for proper diagnosis.",
                    'hindi': f"एक डॉक्टर के रूप में, लक्षणों या प्रश्न के आधार पर: '{user_query}', एक संक्षिप्त चिकित्सा परामर्श प्रतिक्रिया प्रदान करें। इसे संक्षिप्त रखें और उचित निदान के लिए स्वास्थ्य सेवा पेशेवर से मिलने का सुझाव दें।",
                    'marathi': f"डॉक्टर म्हणून, लक्षणे किंवा प्रश्नाच्या आधारे: '{user_query}', थोडक्यात वैद्यकीय सल्ला द्या. योग्य निदानासाठी आरोग्य सेवा व्यावसायिकाला भेटण्याचा सल्ला द्या."
                }
                
                # For text-only queries, we can still provide some medical guidance
                doctor_response = text_only_prompts.get(language_choice.lower(), text_only_prompts['english'])
            else:
                doctor_response = no_image_messages.get(language_choice.lower(), no_image_messages['english'])
        
        # Generate audio response with language support
        output_audio_path = f"doctor_response_{language_choice.lower()}.mp3"
        
        # Choose TTS service
        use_elevenlabs = (voice_service == "ElevenLabs (Premium)")
        
        text_to_speech_multilingual(
            input_text=doctor_response, 
            output_filepath=output_audio_path,
            language=language_choice.lower(),
            use_elevenlabs=use_elevenlabs
        )
        
        # Return results
        if os.path.exists(output_audio_path):
            return (speech_to_text_output if 'speech_to_text_output' in locals() else f"Text input: {user_query}"), doctor_response, output_audio_path
        else:
            return (speech_to_text_output if 'speech_to_text_output' in locals() else f"Text input: {user_query}"), doctor_response, None
            
    except Exception as e:
        error_msg = f"Error processing: {str(e)}"
        return error_msg, error_msg, None

# Create the enhanced interface with multiple input options
with gr.Blocks(title="AI Doctor with Vision and Voice") as iface:
    gr.Markdown("# 🩺 AI Doctor with Vision and Voice")
    gr.Markdown("Upload an image and ask a question via **text**, **voice recording**, or **audio file** to get medical analysis in English, Hindi, or Marathi")
    
    with gr.Row():
        with gr.Column(scale=1):
            # Input section
            gr.Markdown("### 📝 Ask Your Question")
            
            # Text input
            text_input = gr.Textbox(
                label="Type your question here",
                placeholder="e.g., What do you see in this image? or Describe the symptoms...",
                lines=3
            )
            
            gr.Markdown("**OR**")
            
            # Audio inputs
            recorded_audio = gr.Audio(
                sources=["microphone"], 
                type="filepath", 
                label="Record your question"
            )
            
            gr.Markdown("**OR**")
            
            uploaded_audio = gr.Audio(
                sources=["upload"], 
                type="filepath", 
                label="Upload audio file"
            )
            
            # Image input
            image_input = gr.Image(
                type="filepath", 
                label="Upload medical image (optional)"
            )
            
            # Settings
            gr.Markdown("### ⚙️ Settings")
            language_choice = gr.Dropdown(
                choices=["English", "Hindi", "Marathi"], 
                value="English", 
                label="Response Language"
            )
            
            voice_service = gr.Radio(
                choices=["gTTS (Free)", "ElevenLabs (Premium)"], 
                value="gTTS (Free)", 
                label="Voice Service"
            )
            
            # Submit button
            submit_btn = gr.Button("🔍 Analyze", variant="primary", size="lg")
        
        with gr.Column(scale=1):
            # Output section
            gr.Markdown("### 📋 Results")
            
            input_text_output = gr.Textbox(
                label="Your Input (Transcribed)",
                interactive=False
            )
            
            doctor_response_output = gr.Textbox(
                label="Doctor's Response",
                interactive=False,
                lines=5
            )
            
            audio_response_output = gr.Audio(
                label="Doctor's Voice Response",
                type="filepath"
            )
    
    # Examples section
    gr.Markdown("### 💡 Example Questions")
    gr.Examples(
        examples=[
            ["What do you see in this X-ray image?", None, None],
            ["I have a persistent headache for 3 days", None, None],
            ["Can you analyze this skin condition?", None, None],
            ["मुझे बुखार और खांसी है", None, None],
            ["माझ्या डोळ्यात दुखत आहे", None, None]
        ],
        inputs=[text_input, recorded_audio, uploaded_audio]
    )
    
    # Connect the function to the interface
    submit_btn.click(
        fn=process_inputs,
        inputs=[
            recorded_audio,
            uploaded_audio, 
            text_input,
            image_input,
            language_choice,
            voice_service
        ],
        outputs=[
            input_text_output,
            doctor_response_output,
            audio_response_output
        ]
    )

if __name__ == "__main__":
    iface.launch(debug=True)