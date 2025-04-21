import subprocess
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os
import sys

def check_ffmpeg():
    """Verify FFmpeg is installed"""
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, 
                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except:
        print("Error: FFmpeg not found. Please install it first.")
        print("Download from: https://ffmpeg.org/download.html")
        return False

def split_audio_diary(input_path, output_dir="output", silence_threshold=-40, min_silence_len=1500):
    """Split audio file on silence periods"""
    try:
        # Verify input file exists
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")
            
        # Load audio (automatic format detection)
        audio = AudioSegment.from_file(input_path)
        print(f"✅ Successfully loaded {len(audio)/1000}s audio")
        
        # Split on silence
        chunks = split_on_silence(
            audio,
            min_silence_len=min_silence_len,
            silence_thresh=silence_threshold,
            keep_silence=500
        )
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Export chunks
        for i, chunk in enumerate(chunks):
            output_path = os.path.join(output_dir, f"entry_{i+1:03d}.mp3")
            chunk.export(output_path, format="mp3")
            print(f"  ▸ Saved {len(chunk)/1000:.1f}s segment as {output_path}")
            
        print(f"\n🎉 Success! Created {len(chunks)} files in '{output_dir}'")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if not check_ffmpeg():
        sys.exit(1)
        
    import argparse
    parser = argparse.ArgumentParser(
        description="Split audio diaries into separate entries",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('input_file', help='Path to input audio file (MP3/WAV)')
    parser.add_argument('-o', '--output', default="output", 
                       help='Output directory')
    parser.add_argument('-t', '--threshold', type=int, default=-40,
                       help='Silence threshold in dB')
    parser.add_argument('-l', '--length', type=int, default=1500,
                       help='Minimum silence length in milliseconds')
    
    args = parser.parse_args()
    split_audio_diary(
        args.input_file,
        args.output,
        args.threshold,
        args.length
    )