# 🗂️ AQUA Guardian - Dataset Collection Guide

**Last Updated:** November 21, 2025  
**Phase:** 1 - AI Model Training  
**Priority:** CRITICAL

---

## 📊 Dataset Requirements

### What You Need

**5 Classes of Images:**
1. **Plastic** - Plastic bottles, bags, packaging in water
2. **Sewage** - Sewage discharge, contaminated water
3. **Oil Spill** - Oil slicks, petroleum pollution
4. **Foam** - Chemical foam, detergent pollution
5. **Clean** - Clear, unpolluted water bodies

**Quantity:**
- **Minimum:** 500 images per class = 2,500 total
- **Recommended:** 1,000 images per class = 5,000 total
- **Ideal:** 2,000+ images per class = 10,000+ total

**Quality Requirements:**
- Format: JPEG or PNG
- Size: At least 224x224 pixels (will be resized)
- Good lighting and clarity
- Variety of angles and environments
- Diverse geographic locations

---

## 🎯 Option 1: Use Kaggle Datasets (EASIEST - 1 hour)

### Step 1: Search Kaggle

Visit these datasets:

1. **Water Quality Dataset**
   - URL: https://www.kaggle.com/search?q=water+pollution
   - Search terms: "water pollution", "river pollution", "plastic ocean"

2. **Specific Recommendations:**
   - "Plastic in Water" dataset
   - "River Water Quality" dataset  
   - "Ocean Pollution Images"
   - "Waste Floating on Water"

### Step 2: Download & Organize

```bash
# 1. Download from Kaggle (requires account)
# Click "Download" button on dataset page

# 2. Extract ZIP file
# You'll get a folder with images

# 3. Organize by class
# Move images into our structure
```

### Step 3: Run Organization Script

I'll create a script to help organize Kaggle datasets:

```python
# See: organize_kaggle_dataset.py (below)
python organize_kaggle_dataset.py --input "downloaded_dataset" --output "backend/ml/dataset"
```

**Time Required:** 1-2 hours  
**Pros:** Quick, large datasets available  
**Cons:** May not perfectly match our 5 classes

---

## 🔍 Option 2: Google Images (MODERATE - 3-4 hours)

### Step 1: Install Image Downloader

**Option A: Browser Extension**
- Chrome: "Download All Images" extension
- Firefox: "DownThemAll!" extension

**Option B: Python Script (Recommended)**
Install google-images-download:
```bash
pip install google_images_download
```

### Step 2: Download Images

Use the script I'll provide below (`download_images.py`):

```bash
python download_images.py
```

This will automatically download:
- 1,000 images per search term
- Organized by class
- Filtered by size (>224px)

**Search Terms to Use:**
```
Plastic:
- "plastic bottles in river"
- "plastic pollution water"
- "plastic waste floating"
- "plastic bags in ocean"

Sewage:
- "sewage discharge water"
- "sewage pollution river"
- "wastewater contamination"
- "sewage in water body"

Oil Spill:
- "oil spill water"
- "oil slick ocean"
- "petroleum pollution"
- "oil contaminated water"

Foam:
- "foam pollution river"
- "chemical foam water"
- "detergent pollution water"
- "surfactant foam river"

Clean:
- "clear river water"
- "clean lake"
- "pristine water body"
- "unpolluted natural water"
```

**Time Required:** 3-4 hours (mostly automated)  
**Pros:** Free, customizable, diverse images  
**Cons:** Quality varies, need manual cleanup

---

## 📸 Option 3: Manual Collection (COMPREHENSIVE - 1-2 weeks)

### Step 1: Field Collection

**Equipment Needed:**
- Smartphone camera (12MP+)
- Access to various water bodies

**Where to Collect:**
1. **Local Rivers/Streams** - Urban pollution
2. **Lakes/Ponds** - Different pollution types
3. **Beaches** - Plastic and oil pollution
4. **Industrial Areas** - Sewage and chemical foam
5. **Rural Water Bodies** - Clean water samples

**Collection Tips:**
- Take 50-100 photos per location
- Multiple angles per pollution type
- Different times of day (lighting variety)
- Include close-ups and wide shots
- Note GPS coordinates (optional)

### Step 2: Crowdsourcing

**Create a Data Collection Campaign:**

1. **Social Media Post:**
   ```
   📸 Help Fight Water Pollution!
   
   We're building an AI to detect water pollution.
   Can you help by sharing photos?
   
   What we need:
   - Photos of polluted water (plastic, sewage, oil, foam)
   - Photos of clean water
   
   Email: dataset@aquaguardian.org
   
   #WaterPollution #AIForGood #CleanWater
   ```

2. **Google Forms for Upload:**
   - Create form with image upload field
   - Ask for pollution type
   - Optional: location information

3. **Partner with NGOs:**
   - Reach out to environmental organizations
   - They often have pollution documentation
   - Request permission to use images

**Time Required:** 1-2 weeks  
**Pros:** High quality, specific to your use case, real-world data  
**Cons:** Time-consuming, requires effort

---

## 🌐 Option 4: Open Source Datasets (QUICK - 1 hour)

### Free Dataset Sources

1. **Roboflow Universe**
   - URL: https://universe.roboflow.com/
   - Search: "water pollution", "plastic detection"
   - Download in "folder" format

2. **ImageNet**
   - URL: http://www.image-net.org/
   - Search for water-related categories
   - Download specific synsets

3. **Open Images by Google**
   - URL: https://storage.googleapis.com/openimages/web/index.html
   - Search for pollution-related labels

4. **Flickr Creative Commons**
   - URL: https://www.flickr.com/creativecommons/
   - Search with our search terms
   - Filter: "Commercial use allowed"

5. **Unsplash/Pexels (Stock Photos)**
   - URL: https://unsplash.com / https://pexels.com
   - Search terms: pollution, sewage, oil spill
   - Free for commercial use

---

## 🤖 Dataset Collection Scripts

### Script 1: Google Images Downloader

**File: `backend/ml/download_images.py`**

```python
from google_images_download import google_images_download
from pathlib import Path

# Configuration
OUTPUT_DIR = Path("dataset_raw")
IMAGES_PER_CLASS = 1000

# Search queries for each class
SEARCH_QUERIES = {
    "plastic": [
        "plastic bottles in river",
        "plastic pollution water",
        "plastic waste floating ocean",
        "plastic bags in water"
    ],
    "sewage": [
        "sewage discharge water",
        "sewage pollution river",
        "wastewater contamination",
        "sewage in lake"
    ],
    "oil_spill": [
        "oil spill water surface",
        "oil slick ocean",
        "petroleum pollution water",
        "oil contaminated river"
    ],
    "foam": [
        "foam pollution river",
        "chemical foam water",
        "detergent pollution lake",
        "surfactant foam water"
    ],
    "clean": [
        "clear river water",
        "clean lake pristine",
        "unpolluted natural water",
        "crystal clear water body"
    ]
}

def download_class_images(class_name, queries):
    """Download images for a specific class."""
    print(f"\n📥 Downloading {class_name.upper()} images...")
    
    response = google_images_download.googleimagesdownload()
    
    for i, query in enumerate(queries):
        print(f"  Query {i+1}/{len(queries)}: {query}")
        
        arguments = {
            "keywords": query,
            "limit": IMAGES_PER_CLASS // len(queries),
            "print_urls": False,
            "format": "jpg",
            "size": "medium",  # >400px
            "output_directory": str(OUTPUT_DIR),
            "image_directory": class_name,
            "no_directory": False
        }
        
        try:
            response.download(arguments)
            print(f"    ✅ Downloaded")
        except Exception as e:
            print(f"    ❌ Error: {e}")

def main():
    """Download images for all classes."""
    print("=" * 60)
    print("AQUA Guardian - Image Dataset Downloader")
    print("=" * 60)
    
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    for class_name, queries in SEARCH_QUERIES.items():
        download_class_images(class_name, queries)
    
    print("\n" + "=" * 60)
    print("✅ Download complete!")
    print(f"📁 Images saved to: {OUTPUT_DIR}")
    print("\nNext step: Run organize_dataset.py to split into train/val/test")
    print("=" * 60)

if __name__ == "__main__":
    main()
```

**Usage:**
```bash
pip install google_images_download
python backend/ml/download_images.py
```

---

### Script 2: Dataset Organizer

**File: `backend/ml/organize_dataset.py`**

```python
import os
import shutil
from pathlib import Path
import random
from PIL import Image

# Configuration
RAW_DIR = Path("dataset_raw")
OUTPUT_DIR = Path("dataset")
TRAIN_SPLIT = 0.7
VAL_SPLIT = 0.2
TEST_SPLIT = 0.1
MIN_IMAGE_SIZE = 224

def is_valid_image(image_path):
    """Check if image is valid and meets size requirements."""
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            return width >= MIN_IMAGE_SIZE and height >= MIN_IMAGE_SIZE
    except:
        return False

def organize_class(class_name):
    """Organize images for one class into train/val/test."""
    print(f"\n📂 Processing {class_name.upper()}...")
    
    # Get all images in class folder
    class_dir = RAW_DIR / class_name
    if not class_dir.exists():
        print(f"  ⚠️ Folder not found: {class_dir}")
        return
    
    # Find all image files
    image_files = []
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']:
        image_files.extend(class_dir.glob(f"**/{ext}"))
    
    # Filter valid images
    valid_images = [img for img in image_files if is_valid_image(img)]
    print(f"  Found {len(valid_images)} valid images (filtered from {len(image_files)})")
    
    if len(valid_images) < 100:
        print(f"  ⚠️ Warning: Only {len(valid_images)} images (recommend 500+)")
    
    # Shuffle
    random.shuffle(valid_images)
    
    # Split
    num_images = len(valid_images)
    train_end = int(num_images * TRAIN_SPLIT)
    val_end = int(num_images * (TRAIN_SPLIT + VAL_SPLIT))
    
    train_images = valid_images[:train_end]
    val_images = valid_images[train_end:val_end]
    test_images = valid_images[val_end:]
    
    print(f"  Split: Train={len(train_images)}, Val={len(val_images)}, Test={len(test_images)}")
    
    # Copy to organized structure
    for split_name, images in [("train", train_images), ("val", val_images), ("test", test_images)]:
        split_dir = OUTPUT_DIR / split_name / class_name
        split_dir.mkdir(parents=True, exist_ok=True)
        
        for i, img_path in enumerate(images):
            dest_path = split_dir / f"{class_name}_{i:04d}{img_path.suffix}"
            shutil.copy2(img_path, dest_path)
        
        print(f"    ✅ {split_name}: {len(images)} images")

def main():
    """Organize all classes."""
    print("=" * 60)
    print("AQUA Guardian - Dataset Organizer")
    print("=" * 60)
    print(f"Input: {RAW_DIR}")
    print(f"Output: {OUTPUT_DIR}")
    print(f"Split: {TRAIN_SPLIT*100}% train, {VAL_SPLIT*100}% val, {TEST_SPLIT*100}% test")
    print("=" * 60)
    
    # Set random seed for reproducibility
    random.seed(42)
    
    # Expected classes
    classes = ["plastic", "sewage", "oil_spill", "foam", "clean"]
    
    # Organize each class
    for class_name in classes:
        organize_class(class_name)
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ Dataset organized!")
    print("\n📊 Final Structure:")
    
    for split in ["train", "val", "test"]:
        print(f"\n{split}/")
        for class_name in classes:
            class_dir = OUTPUT_DIR / split / class_name
            if class_dir.exists():
                count = len(list(class_dir.glob("*")))
                print(f"  ├── {class_name}/  ({count} images)")
    
    print("\n" + "=" * 60)
    print("🚀 Ready to train!")
    print("Next: python train_v2.py")
    print("=" * 60)

if __name__ == "__main__":
    main()
```

**Usage:**
```bash
python backend/ml/organize_dataset.py
```

---

## ✅ Step-by-Step Process (Recommended)

### Day 1: Collection (2-3 hours)

**Choose ONE method:**
- ✅ **Kaggle** (easiest) - Download 2-3 relevant datasets
- ✅ **Google Images** (moderate) - Run `download_images.py`
- ✅ **Manual** (best quality) - Start field collection

### Day 2: Organization (1-2 hours)

1. **Install Pillow:**
   ```bash
   pip install Pillow
   ```

2. **Organize raw images:**
   ```bash
   python backend/ml/organize_dataset.py
   ```

3. **Verify structure:**
   ```bash
   backend/ml/dataset/
   ├── train/
   │   ├── plastic/ (700 images)
   │   ├── sewage/ (700 images)
   │   ├── oil_spill/ (700 images)
   │   ├── foam/ (700 images)
   │   └── clean/ (700 images)
   ├── val/
   │   ├── plastic/ (200 images)
   │   └── ... (200 each)
   └── test/
       ├── plastic/ (100 images)
       └── ... (100 each)
   ```

### Day 3: Cleanup (1 hour)

1. **Manual review:**
   - Open each folder
   - Remove obviously wrong images
   - Remove duplicates
   - Fix mislabeled images

2. **Quality check:**
   ```python
   # Quick check script
   from pathlib import Path
   
   dataset_dir = Path("backend/ml/dataset")
   
   for split in ["train", "val", "test"]:
       print(f"\n{split.upper()}:")
       for class_dir in (dataset_dir / split).iterdir():
           count = len(list(class_dir.glob("*")))
           print(f"  {class_dir.name}: {count} images")
   ```

3. **Minimum requirements check:**
   - Train: 500+ per class ✅
   - Val: 100+ per class ✅
   - Test: 50+ per class ✅

### Day 4-5: Training

Now you're ready to train!
```bash
cd backend/ml
python train_v2.py
```

---

## 🎯 Quick Start (2 Hours Total)

**Absolute Fastest Path:**

1. **Download Kaggle dataset** (30 min)
   - Go to Kaggle
   - Search "water pollution dataset"
   - Download first relevant one

2. **Manual organization** (60 min)
   - Create folders: `dataset/train/{plastic,sewage,oil_spill,foam,clean}`
   - Manually sort ~500 images into each class
   - Copy 20% to `val/` folders
   - Copy 10% to `test/` folders

3. **Verify & Train** (10 min)
   - Check folder structure
   - Run `python train_v2.py`

**You'll have a trained model in 3-8 hours!**

---

## 📋 Data Quality Checklist

Before training, verify:

- [ ] At least 500 images per class in train/
- [ ] At least 100 images per class in val/
- [ ] At least 50 images per class in test/
- [ ] Images are varied (different angles, lighting)
- [ ] No corrupted files
- [ ] No duplicates
- [ ] Correctly labeled
- [ ] Mix of geographic locations
- [ ] Good image quality (not blurry)

---

## 🆘 Troubleshooting

**Issue:** Can't find good datasets on Kaggle
- **Solution:** Try Option 2 (Google Images) or combine multiple small datasets

**Issue:** Download script fails
- **Solution:** Use manual download with browser extensions, organize manually

**Issue:** Images too small
- **Solution:** Filter by size in download settings, manually remove small images

**Issue:** Not enough clean water images
- **Solution:** Search "clear lake", "pristine river", use stock photo sites

**Issue:** Classes imbalanced (different numbers)
- **Solution:** It's OK! PyTorch handles this. Or use data augmentation to balance.

---

## 💡 Pro Tips

1. **Quality over Quantity:** 500 good images > 2000 bad images
2. **Diversity Matters:** Different locations, lighting, angles
3. **Start Small:** Begin with 500 per class, expand later if needed
4. **Augmentation Helps:** Our training script does augmentation automatically
5. **Real Data is Best:** Field-collected data performs better than stock photos
6. **Label Carefully:** Mislabeled data hurts more than no data

---

## 🎓 Recommended Approach for Students

**Week 1:**
- Days 1-2: Collect from Kaggle + Google Images (1000 images/class)
- Days 3-4: Manual cleanup and organization
- Day 5: Start training

**Week 2:**
- Days 1-2: Field collection (200 images/class of real pollution)
- Days 3-4: Add to dataset, retrain
- Day 5: Evaluate and deploy

**Result:** High-quality model with both web data and real-world data!

---

## ✅ Success Metrics

After collection, you should have:
- ✅ 2,500-5,000 total images
- ✅ Balanced across 5 classes
- ✅ 70/20/10 train/val/test split
- ✅ All images >224x224 pixels
- ✅ Good variety per class

**You're now ready for AI training! 🚀**

---

*Last Updated: November 21, 2025*  
*Next Step: Run `python train_v2.py`*
