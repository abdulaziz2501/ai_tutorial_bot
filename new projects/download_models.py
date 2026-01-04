"""
Whisper Models Download Script
===============================
Whisper modellarni oldindan yuklab, keyingi ishlatishda tezroq ishlash

Foydalanish:
    python scripts/download_models.py --models base medium large
"""

import os
import argparse
import whisper
from pathlib import Path


def download_whisper_models(models: list, cache_dir: str = None):
    """
    Whisper modellarni yuklab olish
    
    Args:
        models (list): Model nomlari ro'yxati
        cache_dir (str): Modellar saqlanadigan papka
    """
    
    if cache_dir:
        os.environ['WHISPER_CACHE_DIR'] = cache_dir
        print(f"📁 Modellar saqlanish papkasi: {cache_dir}")
    else:
        cache_dir = os.path.join(os.path.expanduser("~"), ".cache", "whisper")
        print(f"📁 Default cache: {cache_dir}")
    
    os.makedirs(cache_dir, exist_ok=True)
    
    available_models = ['tiny', 'base', 'small', 'medium', 'large']
    
    print("\n" + "="*60)
    print("🤖 WHISPER MODELLARNI YUKLASH")
    print("="*60)
    
    for model_name in models:
        if model_name not in available_models:
            print(f"\n⚠️ Noto'g'ri model: {model_name}")
            print(f"Mavjud modellar: {', '.join(available_models)}")
            continue
        
        print(f"\n{'='*60}")
        print(f"📥 Model yuklanmoqda: {model_name}")
        print(f"{'='*60}")
        
        try:
            # Modelni yuklash
            model = whisper.load_model(model_name, download_root=cache_dir)
            
            # Model ma'lumotlari
            model_path = os.path.join(cache_dir, f"{model_name}.pt")
            if os.path.exists(model_path):
                size_mb = os.path.getsize(model_path) / (1024 * 1024)
                print(f"✅ Model yuklandi: {model_name}")
                print(f"📊 Hajmi: {size_mb:.2f} MB")
                print(f"📂 Yo'l: {model_path}")
            else:
                print(f"✅ Model yuklandi: {model_name}")
            
            # Modelni tozalash (RAM'dan)
            del model
            
        except Exception as e:
            print(f"❌ Xatolik: {str(e)}")
    
    print("\n" + "="*60)
    print("✅ YUKLASH TUGALLANDI")
    print("="*60)
    
    # Barcha yuklangan modellarni ko'rsatish
    print("\n📋 Yuklangan modellar:")
    for model_name in available_models:
        model_path = os.path.join(cache_dir, f"{model_name}.pt")
        if os.path.exists(model_path):
            size_mb = os.path.getsize(model_path) / (1024 * 1024)
            print(f"  ✅ {model_name:8} - {size_mb:8.2f} MB - {model_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Whisper modellarni oldindan yuklash'
    )
    
    parser.add_argument(
        '--models',
        nargs='+',
        default=['base', 'medium'],
        choices=['tiny', 'base', 'small', 'medium', 'large'],
        help='Yuklanadigan modellar (default: base medium)'
    )
    
    parser.add_argument(
        '--cache-dir',
        type=str,
        default='./models/whisper',
        help='Modellar saqlanadigan papka (default: ./models/whisper)'
    )
    
    parser.add_argument(
        '--all',
        action='store_true',
        help='Barcha modellarni yuklash'
    )
    
    args = parser.parse_args()
    
    # Barcha modellarni yuklash
    if args.all:
        models_to_download = ['tiny', 'base', 'small', 'medium', 'large']
    else:
        models_to_download = args.models
    
    print(f"\n🎯 Yuklanadigan modellar: {', '.join(models_to_download)}")
    
    # Tasdiqlash
    response = input("\n❓ Davom etishni xohlaysizmi? (yes/no): ").lower()
    if response not in ['yes', 'y', 'ha']:
        print("❌ Bekor qilindi")
        return
    
    # Yuklash
    download_whisper_models(models_to_download, args.cache_dir)
    
    print("\n💡 Foydalanish uchun:")
    print(f"   export WHISPER_CACHE_DIR={os.path.abspath(args.cache_dir)}")
    print("   yoki .env faylida:")
    print(f"   WHISPER_CACHE_DIR={os.path.abspath(args.cache_dir)}")


if __name__ == "__main__":
    main()
